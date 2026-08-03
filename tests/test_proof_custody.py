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

    def test_all_gates_produce_token_valid(self) -> None:
        receipt = copy.deepcopy(self.receipt)
        receipt["verification"]["build"]["pass"] = True
        receipt["verification"]["independent_checker"]["pass"] = True
        receipt["governance"]["independent_review_approved"] = True
        receipt["governance"]["merged_on_protected_edge"] = True
        receipt["governance"]["required_checks_pass"] = True
        receipt["decision"]["receipt_digest_present"] = True
        receipt["decision"]["blocking_token_vazio"] = []
        receipt["decision"]["token_valid"] = True
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
