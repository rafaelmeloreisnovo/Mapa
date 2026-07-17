#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_repository_inventory_batch import canonical_batch_digest
from validate_repository_inventory import canonical_digest
from validate_repository_inventory_batch_chain import validate_batch_chain


class InventoryBatchChainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.inventory = json.loads(
            (ROOT / "indices/REPOSITORY_INVENTORY.json").read_text(encoding="utf-8")
        )
        cls.batches = [
            (path, json.loads(path.read_text(encoding="utf-8")))
            for path in sorted((ROOT / "indices/inventory_batches").glob("*.json"))
        ]

    def test_current_chain_passes(self) -> None:
        errors, report = validate_batch_chain(self.inventory, self.batches)
        self.assertEqual(errors, [])
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["batch_count"], 2)
        self.assertEqual(report["total_batch_records"], 20)
        self.assertEqual(report["baseline_unbatched_records"], 11)
        self.assertTrue(report["all_batches_fixed_points"])
        self.assertFalse(report["claim_allowed"])

    def test_missing_inventory_record_is_rejected(self) -> None:
        bad_inventory = copy.deepcopy(self.inventory)
        target = self.batches[-1][1]["records"][0]["repository_full_name"]
        bad_inventory["repositories"] = [
            record
            for record in bad_inventory["repositories"]
            if record["repository_full_name"] != target
        ]
        bad_inventory["scope"]["materialized_count"] -= 1
        bad_inventory["statistics"]["materialized_count"] -= 1
        bad_inventory["statistics"]["public_count"] -= 1
        bad_inventory["statistics"]["owner_counts"]["instituto-Rafael"] -= 1
        bad_inventory["scope"]["completeness_ratio"] = round(
            bad_inventory["scope"]["materialized_count"]
            / bad_inventory["scope"]["accessible_total_observed"],
            12,
        )
        bad_inventory["absence_ledger"]["missing_materialized_records"] += 1
        bad_inventory["integrity"]["digest"] = canonical_digest(bad_inventory)
        errors, _ = validate_batch_chain(bad_inventory, self.batches)
        self.assertTrue(any("inventory missing" in error for error in errors))

    def test_divergent_inventory_evidence_is_rejected(self) -> None:
        bad_inventory = copy.deepcopy(self.inventory)
        target = self.batches[-1][1]["records"][0]["repository_full_name"]
        for record in bad_inventory["repositories"]:
            if record["repository_full_name"] == target:
                record["size_kib"] += 1
                break
        bad_inventory["integrity"]["digest"] = canonical_digest(bad_inventory)
        errors, _ = validate_batch_chain(bad_inventory, self.batches)
        self.assertTrue(any("divergent inventory evidence" in error for error in errors))

    def test_duplicate_repository_across_batches_is_rejected(self) -> None:
        duplicate = copy.deepcopy(self.batches[-1][1])
        duplicate["batch_id"] = "BATCH_003_DUPLICATE"
        duplicate["observed_at"] = "2026-07-17T17:22:00Z"
        duplicate["integrity"]["digest"] = canonical_batch_digest(duplicate)
        errors, _ = validate_batch_chain(
            self.inventory, self.batches + [(Path("BATCH_003_DUPLICATE.json"), duplicate)]
        )
        self.assertTrue(any("repeated across batches" in error for error in errors))

    def test_duplicate_batch_id_is_rejected(self) -> None:
        duplicate = copy.deepcopy(self.batches[-1][1])
        duplicate["observed_at"] = "2026-07-17T17:22:00Z"
        duplicate["records"] = []
        duplicate["record_count"] = 0
        duplicate["owner_counts"] = {
            "instituto-Rafael": 0,
            "rafaelmeloreisnovo": 0,
        }
        duplicate["integrity"]["digest"] = canonical_batch_digest(duplicate)
        errors, _ = validate_batch_chain(
            self.inventory, self.batches + [(Path("BATCH_DUPLICATE_ID.json"), duplicate)]
        )
        self.assertTrue(any("duplicate batch_id" in error for error in errors))

    def test_tampered_batch_digest_is_rejected(self) -> None:
        bad_batches = copy.deepcopy(self.batches)
        bad_batches[-1][1]["records"][0]["size_kib"] += 1
        errors, _ = validate_batch_chain(self.inventory, bad_batches)
        self.assertTrue(any("digest mismatch" in error for error in errors))

    def test_non_monotonic_timestamp_is_rejected(self) -> None:
        bad_batches = copy.deepcopy(self.batches)
        bad_batches[-1][1]["observed_at"] = "2026-07-17T16:00:00Z"
        bad_batches[-1][1]["integrity"]["digest"] = canonical_batch_digest(
            bad_batches[-1][1]
        )
        errors, _ = validate_batch_chain(self.inventory, bad_batches)
        self.assertIn(
            "batch observed_at timestamps are not monotonic in filename order", errors
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
