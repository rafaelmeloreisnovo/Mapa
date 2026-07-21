from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_claim_vocabulary import (
    ClaimValidationError,
    load_json,
    scan_repository,
    validate_claim_record,
    validate_policy,
)

POLICY_PATH = Path("indices/CLAIM_VOCABULARY_POLICY.json")


class ClaimVocabularyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = load_json(POLICY_PATH)

    def test_valid_policy(self):
        result = validate_policy(copy.deepcopy(self.policy))
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["claim_allowed"])

    def test_complete_with_full_chain_passes(self):
        record = {
            "claim_state": "COMPLETE",
            "claim_allowed": False,
            "certification_claim": False,
            "implementation_state": "IMPLEMENTED",
            "execution_state": "EXECUTED",
            "evidence_state": "EVIDENCED",
            "implementation_pointer": "src/module.c@abc123",
            "execution_pointer": "runs/local-001.json",
            "evidence_pointer": "evidence/local-001.sha256",
        }
        self.assertEqual(validate_claim_record(record, self.policy)["status"], "PASS")

    def test_complete_missing_execution_pointer_rejected(self):
        record = {
            "claim_state": "COMPLETE",
            "claim_allowed": False,
            "certification_claim": False,
            "implementation_state": "IMPLEMENTED",
            "execution_state": "EXECUTED",
            "evidence_state": "EVIDENCED",
            "implementation_pointer": "src/module.c@abc123",
            "evidence_pointer": "evidence/local-001.sha256",
        }
        with self.assertRaises(ClaimValidationError):
            validate_claim_record(record, self.policy)

    def test_complete_with_token_vazio_pointer_rejected(self):
        record = {
            "claim_state": "COMPLETE",
            "claim_allowed": False,
            "certification_claim": False,
            "implementation_state": "IMPLEMENTED",
            "execution_state": "EXECUTED",
            "evidence_state": "EVIDENCED",
            "implementation_pointer": "src/module.c@abc123",
            "execution_pointer": "TOKEN_VAZIO",
            "evidence_pointer": "evidence/local-001.sha256",
        }
        with self.assertRaises(ClaimValidationError):
            validate_claim_record(record, self.policy)

    def test_compliant_without_authority_rejected(self):
        record = {
            "claim_state": "COMPLIANT",
            "claim_allowed": False,
            "certification_claim": False,
            "implementation_state": "IMPLEMENTED",
            "execution_state": "EXECUTED",
            "evidence_state": "INDEPENDENTLY_ASSURED",
            "implementation_pointer": "src/module.c@abc123",
            "execution_pointer": "runs/independent-001.json",
            "evidence_pointer": "evidence/independent-001.sha256",
            "criteria_pointer": "criteria/bounded-profile-v1.json",
            "scope_pointer": "scope/bounded-profile-v1.json",
        }
        with self.assertRaises(ClaimValidationError):
            validate_claim_record(record, self.policy)

    def test_certified_always_rejected(self):
        record = {
            "claim_state": "CERTIFIED",
            "claim_allowed": False,
            "certification_claim": False,
        }
        with self.assertRaises(ClaimValidationError):
            validate_claim_record(record, self.policy)

    def test_aligned_requires_bounded_basis_and_no_conformity(self):
        record = {
            "claim_state": "ALIGNED",
            "claim_allowed": False,
            "certification_claim": False,
            "conformity_claim": False,
            "alignment_basis_pointer": "docs/control-crosswalk.md",
            "alignment_scope": "Mapa/G006",
        }
        self.assertEqual(validate_claim_record(record, self.policy)["state"], "ALIGNED")

    def test_prose_contradiction_is_reported_not_promoted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "note.md").write_text(
                "The integration is COMPLETE, but device evidence is TOKEN_VAZIO.\n",
                encoding="utf-8",
            )
            result = scan_repository(root, self.policy)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["prose_contradiction_candidate_count"], 1)
            self.assertFalse(result["portfolio_exit_criteria_met"])

    def test_inline_explicit_claim_without_chain_fails_scan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "note.md").write_text(
                '<!-- CLAIM_RECORD {"claim_state":"COMPLETE","claim_allowed":false,"certification_claim":false} -->\n',
                encoding="utf-8",
            )
            result = scan_repository(root, self.policy)
            self.assertEqual(result["status"], "FAIL")
            self.assertEqual(result["explicit_claim_error_count"], 1)

    def test_policy_tampering_rejected(self):
        policy = copy.deepcopy(self.policy)
        policy["rollout_mode"] = "SILENT_PROMOTION"
        with self.assertRaises(ClaimValidationError):
            validate_policy(policy)


if __name__ == "__main__":
    unittest.main()
