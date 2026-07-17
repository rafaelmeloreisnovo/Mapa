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
        cls.batch_paths = sorted((ROOT / "indices/inventory_batches").glob("*.json"))
        cls.batches = [
            json.loads(path.read_text(encoding="utf-8")) for path in cls.batch_paths
        ]
        cls.batch = cls.batches[-1]
        batch_names = {record["repository_full_name"] for record in cls.batch["records"]}
        baseline = copy.deepcopy(cls.current)
        baseline["repositories"] = [
            record
            for record in baseline["repositories"]
            if record["repository_full_name"] not in batch_names
        ]
        previous_time = (
            cls.batches[-2]["observed_at"]
            if len(cls.batches) > 1
            else cls.batch["observed_at"]
        )
        cls.baseline = recalculate_inventory(baseline, previous_time)

    def test_all_batch_contracts_pass(self) -> None:
        for batch in self.batches:
            with self.subTest(batch=batch["batch_id"]):
                self.assertEqual(validate_batch(batch), [])

    def test_latest_batch_reconstructs_canonical_inventory(self) -> None:
        output, audit = apply_batch(self.baseline, self.batch)
        self.assertEqual(audit["added_count"], self.batch["record_count"])
        self.assertEqual(audit["skipped_idempotent_count"], 0)
        self.assertEqual(output, self.current)
        self.assertEqual(validate_inventory(output), [])

    def test_every_committed_batch_is_current_fixed_point(self) -> None:
        for batch in self.batches:
            with self.subTest(batch=batch["batch_id"]):
                output, audit = apply_batch(self.current, batch)
                self.assertEqual(audit["added_count"], 0)
                self.assertEqual(
                    audit["skipped_idempotent_count"], batch["record_count"]
                )
                self.assertEqual(output, self.current)

    def test_historical_replay_does_not_rewind_timestamp_or_digest(self) -> None:
        output, _ = apply_batch(self.current, self.batches[0])
        self.assertEqual(output["generated_at"], self.current["generated_at"])
        self.assertEqual(output["integrity"]["digest"], self.current["integrity"]["digest"])

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
        bad["owner_counts"]["instituto-Rafael"] -= 1
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
        final_owner_counts = self.current["statistics"]["owner_counts"]
        baseline["scope"]["accessible_total_observed"] = len(self.current["repositories"])
        for account in baseline["scope"]["included_accounts"]:
            account["accessible_count_observed"] = final_owner_counts[account["account"]]
        baseline = recalculate_inventory(baseline, self.baseline["generated_at"])
        baseline["integrity"]["digest"] = canonical_digest(baseline)
        output, _ = apply_batch(baseline, self.batch)
        self.assertEqual(
            output["scope"]["materialized_count"], len(self.current["repositories"])
        )
        self.assertEqual(output["absence_ledger"]["missing_materialized_records"], 0)
        self.assertEqual(output["scope"]["state"], "PARTIAL")
        self.assertFalse(output["scope"]["claim_allowed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
