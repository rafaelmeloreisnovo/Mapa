from __future__ import annotations

import copy
import unittest
from pathlib import Path

from scripts.validate_claim_contradiction_ledger import (
    LedgerValidationError,
    load,
    validate,
)

BASE = Path("indices/CLAIM_CONTRADICTION_LEDGER.json")


class ClaimContradictionLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load(BASE)

    def test_valid_ledger(self):
        result = validate(copy.deepcopy(self.data))
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["candidate_count"], 36)
        self.assertEqual(result["reviewed_safe_count"], 6)
        self.assertEqual(result["token_vazio_count"], 30)
        self.assertFalse(result["portfolio_exit_criteria_met"])

    def test_exhaustive_search_claim_rejected(self):
        data = copy.deepcopy(self.data)
        data["source_snapshot"]["exhaustive"] = True
        with self.assertRaises(LedgerValidationError):
            validate(data)

    def test_candidate_count_drift_rejected(self):
        data = copy.deepcopy(self.data)
        data["source_snapshot"]["candidate_count"] = 35
        with self.assertRaises(LedgerValidationError):
            validate(data)

    def test_duplicate_path_rejected(self):
        data = copy.deepcopy(self.data)
        data["entries"][1]["path"] = data["entries"][0]["path"]
        with self.assertRaises(LedgerValidationError):
            validate(data)

    def test_safe_without_evidence_pointer_rejected(self):
        data = copy.deepcopy(self.data)
        entry = next(item for item in data["entries"] if item["review_state"] == "REVIEWED_SAFE")
        entry.pop("evidence_pointer")
        with self.assertRaises(LedgerValidationError):
            validate(data)

    def test_safe_pointer_commit_drift_rejected(self):
        data = copy.deepcopy(self.data)
        entry = next(item for item in data["entries"] if item["review_state"] == "REVIEWED_SAFE")
        entry["evidence_pointer"] = entry["path"] + "@" + "0" * 40
        with self.assertRaises(LedgerValidationError):
            validate(data)

    def test_token_vazio_without_exit_criteria_rejected(self):
        data = copy.deepcopy(self.data)
        entry = next(item for item in data["entries"] if item["review_state"] == "TOKEN_VAZIO")
        entry["exit_criteria"] = []
        with self.assertRaises(LedgerValidationError):
            validate(data)

    def test_token_vazio_with_fake_evidence_rejected(self):
        data = copy.deepcopy(self.data)
        entry = next(item for item in data["entries"] if item["review_state"] == "TOKEN_VAZIO")
        entry["evidence_pointer"] = entry["path"] + "@" + data["source_snapshot"]["commit"]
        with self.assertRaises(LedgerValidationError):
            validate(data)

    def test_automatic_dismissal_rejected(self):
        data = copy.deepcopy(self.data)
        data["review_policy"]["automatic_dismissal"] = True
        with self.assertRaises(LedgerValidationError):
            validate(data)

    def test_claim_promotion_rejected(self):
        data = copy.deepcopy(self.data)
        data["claim_allowed"] = True
        with self.assertRaises(LedgerValidationError):
            validate(data)

    def test_integrity_tampering_rejected(self):
        data = copy.deepcopy(self.data)
        data["derived"]["next_gate"] = "SILENT_PROMOTION"
        with self.assertRaises(LedgerValidationError):
            validate(data)


if __name__ == "__main__":
    unittest.main()
