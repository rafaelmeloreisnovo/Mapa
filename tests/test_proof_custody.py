#!/usr/bin/env python3

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.verify_proof_custody import validate_receipt  # noqa: E402


class ProofCustodyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = json.loads(
            (ROOT / "data/control-plane/proof-custody-gate.v1.json").read_text(encoding="utf-8")
        )
        cls.receipt = json.loads(
            (ROOT / "data/receipts/external/openai-ten-proofs.94bc0feb.audit.json").read_text(
                encoding="utf-8"
            )
        )

    def test_observed_receipt_is_valid_but_not_promoted(self) -> None:
        result = validate_receipt(copy.deepcopy(self.receipt), self.policy)
        self.assertTrue(result["receipt_valid"], result["errors"])
        self.assertFalse(result["token_valid"])
        self.assertIn("TOKEN_VAZIO_COMPARATOR_RECEIPT", result["blocking_token_vazio"])

    def test_claim_cannot_be_allowed_without_token_valid(self) -> None:
        receipt = copy.deepcopy(self.receipt)
        receipt["decision"]["claim_allowed"] = True
        result = validate_receipt(receipt, self.policy)
        self.assertFalse(result["receipt_valid"])

    def test_pass_boolean_without_receipt_fails_closed(self) -> None:
        receipt = copy.deepcopy(self.receipt)
        receipt["verification"]["build"]["pass"] = True
        result = validate_receipt(receipt, self.policy)
        self.assertFalse(result["receipt_valid"])
        self.assertFalse(result["predicate"]["build_pass"])

    def test_review_without_exact_sha_fails_closed(self) -> None:
        receipt = copy.deepcopy(self.receipt)
        receipt["governance"]["reviews_observed"] = 1
        receipt["governance"]["reviewer_identity"] = "independent-reviewer"
        receipt["governance"]["reviewed_commit_sha"] = "0" * 40
        receipt["governance"]["approval_receipt"] = "review://approval/1"
        receipt["governance"]["independent_review_approved"] = True
        result = validate_receipt(receipt, self.policy)
        self.assertFalse(result["receipt_valid"])
        self.assertFalse(result["predicate"]["independent_review_approved"])

    def test_all_evidence_bound_gates_produce_token_valid(self) -> None:
        receipt = copy.deepcopy(self.receipt)

        receipt["verification"]["build"].update({
            "status": "PASS",
            "executed_in_this_audit": True,
            "pass": True,
            "receipt": "receipt://build/sha256-example",
        })
        receipt["verification"]["independent_checker"].update({
            "status": "PASS",
            "executed_in_this_audit": True,
            "pass": True,
            "receipt": "receipt://checker/sha256-example",
        })

        receipt["governance"].update({
            "reviews_observed": 1,
            "combined_status_checks": ["proof-custody-tests"],
            "reviewer_identity": "independent-reviewer",
            "reviewed_commit_sha": receipt["source"]["commit_sha"],
            "approval_receipt": "review://approval/sha256-example",
            "merge_commit_sha": "1" * 40,
            "independent_review_approved": True,
            "merged_on_protected_edge": True,
            "required_checks_pass": True,
        })

        receipt["decision"].update({
            "receipt_digest_present": True,
            "receipt_payload_sha256": "2" * 64,
            "blocking_token_vazio": [],
            "token_valid": True,
        })

        result = validate_receipt(receipt, self.policy)
        self.assertTrue(result["receipt_valid"], result["errors"])
        self.assertTrue(result["token_valid"])

    def test_invalid_blob_sha_fails(self) -> None:
        receipt = copy.deepcopy(self.receipt)
        receipt["artifacts"][0]["blob_sha"] = "TOKEN_VAZIO"
        result = validate_receipt(receipt, self.policy)
        self.assertFalse(result["receipt_valid"])


if __name__ == "__main__":
    unittest.main()
