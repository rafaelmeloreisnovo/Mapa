from __future__ import annotations

import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from build_living_system_index import (  # noqa: E402
    LivingSystemError,
    build_index,
    canonical_digest,
)
from validate_living_system_index import validate_index  # noqa: E402


class LivingSystemIndexTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        (self.root / "indices/inventory_deltas").mkdir(parents=True)
        (self.root / "data/mechanisms/profiles").mkdir(parents=True)

        base_record = {
            "repository_full_name": "example/alpha",
            "repository_id": 1,
            "owner": "example",
            "repository_name": "alpha",
            "clone_url": "https://example.invalid/alpha.git",
            "default_branch": "main",
            "visibility": "private",
            "archived": False,
            "size_kib": 1,
            "metadata_status": "FATO",
            "claim_scope": "repository_identity_only",
            "observed_via": "fixture",
        }
        delta_record = deepcopy(base_record)
        delta_record.update(
            repository_full_name="example/beta",
            repository_id=2,
            repository_name="beta",
        )
        checkpoint = {
            "schema": "repository_inventory_v2",
            "repositories": [base_record],
        }
        delta = {
            "schema": "repository_inventory_batch_v1",
            "records": [delta_record],
        }
        head = {
            "schema": "repository_inventory_head_v1",
            "generated_at": "2026-07-21T00:00:00Z",
            "checkpoint": {"path": "indices/REPOSITORY_INVENTORY.json"},
            "delta_batches": [{"path": "indices/inventory_deltas/BATCH.json"}],
            "derived": {
                "materialized_count": 2,
                "inventory_state": "PARTIAL",
                "claim_allowed": False,
                "accessible_total_observed": 3,
                "remaining_token_vazio": 1,
            },
        }
        (self.root / "indices/REPOSITORY_INVENTORY.json").write_text(
            json.dumps(checkpoint), encoding="utf-8"
        )
        (self.root / "indices/inventory_deltas/BATCH.json").write_text(
            json.dumps(delta), encoding="utf-8"
        )
        (self.root / "indices/REPOSITORY_INVENTORY_HEAD.json").write_text(
            json.dumps(head), encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def build(self):
        return build_index(
            self.root,
            self.root / "indices/REPOSITORY_INVENTORY_HEAD.json",
            self.root / "data/mechanisms/profiles",
        )

    def test_unread_repositories_become_first_class_token_vazio(self) -> None:
        document = self.build()
        self.assertEqual(document["statistics"]["repository_count"], 2)
        self.assertEqual(document["statistics"]["token_vazio_cell_count"], 22)
        self.assertFalse(document["repositories"][0]["claim_allowed"])
        self.assertEqual(
            document["repositories"][0]["mechanisms"]["purpose"]["state"],
            "TOKEN_VAZIO",
        )
        self.assertTrue(validate_index(document)["ok"])

    def test_profile_promotes_only_evidenced_fields(self) -> None:
        profile = {
            "schema": "repository_mechanism_profile_v1",
            "schema_version": "1.0.0",
            "repository_full_name": "example/alpha",
            "profile_source": "manual-fixture",
            "mechanisms": {
                "purpose": {
                    "state": "FATO",
                    "value": "demonstrate deterministic indexing",
                    "evidence": [
                        {
                            "kind": "repository_file",
                            "locator": "README.md#purpose",
                            "claim_scope": "declared project purpose",
                        }
                    ],
                },
                "risks": {
                    "state": "HIPOTESE",
                    "confidence": 0.4,
                    "value": ["fixture risk"],
                    "evidence": [
                        {
                            "kind": "analysis",
                            "locator": "fixture-review-1",
                            "claim_scope": "test-only hypothesis",
                        }
                    ],
                },
            },
        }
        (self.root / "data/mechanisms/profiles/example__alpha.json").write_text(
            json.dumps(profile), encoding="utf-8"
        )
        document = self.build()
        alpha = document["repositories"][0]
        self.assertEqual(alpha["completeness"]["resolved_fields"], 2)
        self.assertEqual(alpha["completeness"]["hypothesis_fields"], 1)
        self.assertFalse(alpha["claim_allowed"])
        self.assertTrue(validate_index(document)["ok"])

    def test_token_vazio_cannot_hide_a_claim(self) -> None:
        profile = {
            "schema": "repository_mechanism_profile_v1",
            "repository_full_name": "example/alpha",
            "profile_source": "bad-fixture",
            "mechanisms": {
                "purpose": {
                    "state": "TOKEN_VAZIO",
                    "reason": "unknown",
                    "next_action": "read",
                    "exit_criteria": "evidence",
                    "value": "hidden assertion",
                }
            },
        }
        (self.root / "data/mechanisms/profiles/bad.json").write_text(
            json.dumps(profile), encoding="utf-8"
        )
        with self.assertRaises(LivingSystemError):
            self.build()

    def test_digest_is_deterministic_and_tamper_evident(self) -> None:
        first = self.build()
        second = self.build()
        self.assertEqual(first["integrity"]["digest"], second["integrity"]["digest"])
        tampered = deepcopy(first)
        tampered["repositories"][0]["identity"]["owner"] = "other"
        report = validate_index(tampered)
        self.assertFalse(report["ok"])
        self.assertIn("integrity digest mismatch", report["errors"])
        self.assertNotEqual(tampered["integrity"]["digest"], canonical_digest(tampered))

    def test_inventory_count_mismatch_fails_closed(self) -> None:
        head_path = self.root / "indices/REPOSITORY_INVENTORY_HEAD.json"
        head = json.loads(head_path.read_text(encoding="utf-8"))
        head["derived"]["materialized_count"] = 99
        head_path.write_text(json.dumps(head), encoding="utf-8")
        with self.assertRaises(LivingSystemError):
            self.build()


if __name__ == "__main__":
    unittest.main()
