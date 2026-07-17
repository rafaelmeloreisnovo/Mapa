#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_repository_inventory_batch import (
    apply_batch,
    canonical_batch_digest,
    recalculate_inventory,
    validate_batch,
)
from validate_repository_inventory import canonical_digest, validate_inventory


class InventoryBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.current = json.loads(
            (ROOT / "indices/REPOSITORY_INVENTORY.json").read_text(encoding="utf-8")
        )
        cls.batch = json.loads(
            (ROOT / "indices/inventory_batches/BATCH_001_2026-07-17.json").read_text(
                encoding="utf-8"
            )
        )
        batch_names = {record["repository_full_name"] for record in cls.batch["records"]}
        baseline = copy.deepcopy(cls.current)
        baseline["repositories"] = [
            record
            for record in baseline["repositories"]
            if record["repository_full_name"] not in batch_names
        ]
        cls.baseline = recalculate_inventory(baseline, "2026-07-17T16:47:07Z")

    def test_batch_contract_passes(self) -> None:
        self.assertEqual(validate_batch(self.batch), [])

    def test_apply_adds_ten_records(self) -> None:
        output, audit = apply_batch(self.baseline, self.batch)
        self.assertEqual(audit["added_count"], 10)
        self.assertEqual(audit["skipped_idempotent_count"], 0)
        self.assertEqual(output["scope"]["materialized_count"], 21)
        self.assertEqual(output["absence_ledger"]["missing_materialized_records"], 105)
        self.assertFalse(output["scope"]["claim_allowed"])
        self.assertEqual(validate_inventory(output), [])

    def test_canonical_inventory_is_batch_fixed_point(self) -> None:
        output, audit = apply_batch(self.current, self.batch)
        self.assertEqual(audit["added_count"], 0)
        self.assertEqual(audit["skipped_idempotent_count"], 10)
        self.assertEqual(output, self.current)

    def test_name_collision_is_rejected(self) -> None:
        bad = copy.deepcopy(self.batch)
        bad["records"][0]["size_kib"] += 1
        bad["integrity"]["digest"] = canonical_batch_digest(bad)
        with self.assertRaisesRegex(ValueError, "name collision"):
            apply_batch(self.current, bad)

    def test_repository_id_collision_is_rejected(self) -> None:
        bad = copy.deepcopy(self.batch)
        bad["records"][0]["repository_id"] = self.baseline["repositories"][0]["repository_id"]
        bad["records"][0]["repository_full_name"] = "instituto-Rafael/OTHER"
        bad["records"][0]["repository_name"] = "OTHER"
        bad["records"][0]["clone_url"] = "https://github.com/instituto-Rafael/OTHER.git"
        bad["integrity"]["digest"] = canonical_batch_digest(bad)
        with self.assertRaisesRegex(ValueError, "repository_id collision"):
            apply_batch(self.baseline, bad)

    def test_record_count_mismatch_is_rejected(self) -> None:
        bad = copy.deepcopy(self.batch)
        bad["record_count"] = 99
        bad["integrity"]["digest"] = canonical_batch_digest(bad)
        self.assertIn("batch record_count mismatch", validate_batch(bad))

    def test_owner_count_mismatch_is_rejected(self) -> None:
        bad = copy.deepcopy(self.batch)
        bad["owner_counts"]["instituto-Rafael"] = 4
        bad["integrity"]["digest"] = canonical_batch_digest(bad)
        self.assertTrue(any("owner_counts mismatch" in error for error in validate_batch(bad)))

    def test_digest_tampering_is_rejected(self) -> None:
        bad = copy.deepcopy(self.batch)
        bad["records"][0]["size_kib"] += 1
        self.assertIn("batch integrity.digest mismatch", validate_batch(bad))

    def test_source_must_be_direct_connector_get_repo(self) -> None:
        bad = copy.deepcopy(self.batch)
        bad["source"] = "manual"
        bad["integrity"]["digest"] = canonical_batch_digest(bad)
        self.assertIn("batch source must be github_connector.get_repo", validate_batch(bad))

    def test_ingestion_never_auto_promotes_complete(self) -> None:
        baseline = copy.deepcopy(self.baseline)
        baseline["scope"]["accessible_total_observed"] = 21
        for account in baseline["scope"]["included_accounts"]:
            account["accessible_count_observed"] = (
                11 if account["account"] == "rafaelmeloreisnovo" else 10
            )
        baseline = recalculate_inventory(baseline, "2026-07-17T16:47:07Z")
        baseline["integrity"]["digest"] = canonical_digest(baseline)
        output, _ = apply_batch(baseline, self.batch)
        self.assertEqual(output["scope"]["materialized_count"], 21)
        self.assertEqual(output["absence_ledger"]["missing_materialized_records"], 0)
        self.assertEqual(output["scope"]["state"], "PARTIAL")
        self.assertFalse(output["scope"]["claim_allowed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
