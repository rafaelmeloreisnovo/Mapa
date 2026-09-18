#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "materialize_systematic_pragmatic_field_review_queue.py"

spec = importlib.util.spec_from_file_location("field_review_queue", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


def enrichment():
    return {
        "schema": "rafaelia.systematic-pragmatic-identity-semantics-enrichment/v1",
        "claim_allowed": False,
        "atlas_mutation_allowed": False,
        "enrichments": [
            {
                "source_gap_id": "GAP-A",
                "target_fields": {
                    "artifact_id": {
                        "state": "TOKEN_VAZIO",
                        "value": "TOKEN_VAZIO",
                        "evidence": [],
                    },
                    "provider": {
                        "state": "STRUCTURED_DERIVATION_CANDIDATE",
                        "value": "GitHub",
                        "evidence": [{"source_key": "owner"}],
                    },
                    "scope": {
                        "state": "EXACT_STRUCTURED",
                        "value": "bounded scope",
                        "evidence": [{"source_key": "scope"}],
                    },
                    "evidence_required": {
                        "state": "ALIAS_CANDIDATE",
                        "value": ["run + artifact"],
                        "evidence": [{"source_key": "evidence_needed"}],
                    },
                },
            }
        ],
    }


class FieldReviewQueueTest(unittest.TestCase):
    def test_builds_four_work_items_with_fail_closed_actions(self):
        out = mod.build(enrichment())
        mod.validate(out)
        self.assertEqual(out["summary"]["work_items"], 4)
        by_field = {row["field"]: row for row in out["items"]}
        self.assertEqual(
            by_field["artifact_id"]["required_action"],
            "ACQUIRE_EXPLICIT_EVIDENCE",
        )
        self.assertEqual(
            by_field["provider"]["required_action"],
            "REVIEW_STRUCTURED_DERIVATION",
        )
        self.assertEqual(
            by_field["scope"]["required_action"],
            "REVIEW_STRUCTURED_EVIDENCE",
        )
        self.assertEqual(
            by_field["evidence_required"]["required_action"],
            "REVIEW_ALIAS_MAPPING",
        )
        self.assertEqual(by_field["artifact_id"]["priority"], "P0")
        self.assertEqual(by_field["provider"]["priority"], "P0")
        self.assertFalse(out["atlas_mutation_allowed"])
        self.assertTrue(out["policy"]["candidate_requires_governed_review"])

    def test_work_ids_are_deterministic(self):
        first = mod.build(enrichment())
        second = mod.build(enrichment())
        self.assertEqual(
            [row["work_id"] for row in first["items"]],
            [row["work_id"] for row in second["items"]],
        )

    def test_validator_rejects_premature_promotion(self):
        out = mod.build(enrichment())
        out["items"][0]["governance"]["promotion_allowed"] = True
        with self.assertRaises(ValueError):
            mod.validate(out)

    def test_token_vazio_cannot_carry_candidate_value(self):
        out = mod.build(enrichment())
        item = next(row for row in out["items"] if row["field"] == "artifact_id")
        item["candidate_value"] = "invented"
        with self.assertRaises(ValueError):
            mod.validate(out)


if __name__ == "__main__":
    unittest.main()
