from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.verify_authorship_provenance import (
    build_report,
    load_jsonl,
    validate_record,
)

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/control-plane/authorship-provenance-policy.v1.json"
SCHEMA = ROOT / "schemas/authorship-provenance-record.schema.json"
REGISTRY = ROOT / "data/authorship/authorship_registry.delta.20260803.jsonl"


class AuthorshipProvenanceTests(unittest.TestCase):
    def test_repository_registry_is_structurally_valid(self) -> None:
        report = build_report(POLICY, SCHEMA, REGISTRY)
        self.assertEqual(report["status"], "PASS", report["defects"])
        self.assertEqual(report["record_count"], 3)
        self.assertEqual(report["promoted_count"], 0)
        self.assertGreater(report["blocking_token_vazio_count"], 0)

    def test_unknown_author_cannot_be_promoted(self) -> None:
        record = copy.deepcopy(load_jsonl(REGISTRY)[0])
        record["record_id"] = "test:unknown-author"
        record["roles"][0]["role"] = "UNKNOWN"
        record["roles"][0]["identity_state"] = "TOKEN_VAZIO"
        record["decision"]["authorship_complete"] = False
        record["decision"]["promotion_allowed"] = True
        record["decision"]["claim_allowed"] = True
        record["decision"]["blocking_token_vazio"] = ["TOKEN_VAZIO_AUTHORSHIP"]
        errors = validate_record(record)
        self.assertTrue(any("cannot be promoted" in error for error in errors))
        self.assertTrue(any("cannot allow claims" in error for error in errors))

    def test_ai_tool_cannot_be_accountable_author(self) -> None:
        record = copy.deepcopy(load_jsonl(REGISTRY)[2])
        record["record_id"] = "test:ai-accountability"
        ai_role = next(role for role in record["roles"] if role["role"] == "AI_ASSISTED_TOOL")
        ai_role["accountable"] = True
        errors = validate_record(record)
        self.assertTrue(any("AI_ASSISTED_TOOL must not be accountable" in error for error in errors))

    def test_unresolved_permission_blocks_promotion(self) -> None:
        record = copy.deepcopy(load_jsonl(REGISTRY)[0])
        record["record_id"] = "test:unresolved-permission"
        record["rights_state"]["permission_state"] = "TOKEN_VAZIO"
        record["decision"]["promotion_allowed"] = True
        record["decision"]["claim_allowed"] = True
        record["decision"]["blocking_token_vazio"] = []
        errors = validate_record(record)
        self.assertTrue(any("cannot be promoted" in error for error in errors))
        self.assertTrue(any("cannot allow claims" in error for error in errors))

    def test_valid_promotion_requires_no_blockers(self) -> None:
        record = copy.deepcopy(load_jsonl(REGISTRY)[0])
        record["record_id"] = "test:clean-promotion"
        record["decision"] = {
            "authorship_complete": True,
            "attribution_complete": True,
            "plagiarism_risk": "NONE_OBSERVED",
            "promotion_allowed": True,
            "claim_allowed": True,
            "blocking_token_vazio": [],
        }
        record["rights_state"]["permission_state"] = "CONFIRMED"
        self.assertEqual(validate_record(record), [])

    def test_correction_must_preserve_previous_record_link(self) -> None:
        record = copy.deepcopy(load_jsonl(REGISTRY)[0])
        record["record_id"] = "test:correction"
        record["previous_record_id"] = "auth:directive.authorship-invariant.20260803T014500-0300"
        record["origin_chain"] = [
            {
                "relation": "SUPERSEDES_WITHOUT_ERASURE",
                "source_locator": "context://conversation/2026-08-03/authorship-directive",
                "source_revision": "2026-08-03T01:45:00-03:00",
                "source_author_state": "IDENTIFIED",
                "source_author": "Rafael Melo Reis / ∆RafaelVerboΩ",
                "scope_used": "Correction preserving the prior attribution record.",
                "source_digest": "sha256:8ae13334f6305ca4de3089c11f630fe9237aba7231290198fe310bd09288e230",
                "citation_anchor": "previous_record_id",
            }
        ]
        self.assertEqual(validate_record(record), [])


if __name__ == "__main__":
    unittest.main()
