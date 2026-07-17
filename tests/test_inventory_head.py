#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_repository_inventory_head import (
    canonical_head_digest,
    validate_head,
)


class RepositoryInventoryHeadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.head = json.loads(
            (ROOT / "indices/REPOSITORY_INVENTORY_HEAD.json").read_text(
                encoding="utf-8"
            )
        )

    @staticmethod
    def reseal(head: dict) -> dict:
        head["integrity"]["digest"] = ""
        head["integrity"]["digest"] = canonical_head_digest(head)
        return head

    def test_committed_head_is_valid(self) -> None:
        errors, report = validate_head(ROOT, copy.deepcopy(self.head))
        self.assertEqual(errors, [])
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["materialized_count"], 51)
        self.assertEqual(report["remaining_token_vazio"], 75)
        self.assertTrue(report["all_delta_batches_fixed_points"])
        self.assertFalse(report["claim_allowed"])

    def test_head_digest_tampering_is_rejected(self) -> None:
        head = copy.deepcopy(self.head)
        head["integrity"]["digest"] = "0" * 64
        errors, _ = validate_head(ROOT, head)
        self.assertTrue(any("head integrity.digest mismatch" in item for item in errors))

    def test_checkpoint_digest_tampering_is_rejected(self) -> None:
        head = copy.deepcopy(self.head)
        head["checkpoint"]["digest_blake2b_256"] = "0" * 64
        self.reseal(head)
        errors, _ = validate_head(ROOT, head)
        self.assertTrue(any("checkpoint digest mismatch" in item for item in errors))

    def test_batch_digest_tampering_is_rejected(self) -> None:
        head = copy.deepcopy(self.head)
        head["delta_batches"][0]["digest_blake2b_256"] = "0" * 64
        self.reseal(head)
        errors, _ = validate_head(ROOT, head)
        self.assertTrue(any("digest mismatch" in item for item in errors))

    def test_derived_count_tampering_is_rejected(self) -> None:
        head = copy.deepcopy(self.head)
        head["derived"]["materialized_count"] = 52
        self.reseal(head)
        errors, _ = validate_head(ROOT, head)
        self.assertTrue(any("derived state mismatch" in item for item in errors))

    def test_duplicate_delta_batch_is_rejected(self) -> None:
        head = copy.deepcopy(self.head)
        head["delta_batches"].append(copy.deepcopy(head["delta_batches"][0]))
        self.reseal(head)
        errors, _ = validate_head(ROOT, head)
        self.assertTrue(any("duplicate batch_id" in item for item in errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
