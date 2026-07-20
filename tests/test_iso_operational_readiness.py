from __future__ import annotations
import copy, json, unittest
from pathlib import Path
from scripts.validate_iso_operational_readiness import ValidationError, load, validate

BASE = Path("indices/ISO_OPERATIONAL_READINESS_BASELINE.json")

class IsoOperationalReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load(BASE)

    def test_valid_baseline(self):
        result = validate(copy.deepcopy(self.data))
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["heuristic_count"], 30)
        self.assertFalse(result["claim_allowed"])

    def test_claim_promotion_rejected(self):
        data = copy.deepcopy(self.data)
        data["claim_allowed"] = True
        with self.assertRaises(ValidationError):
            validate(data)

    def test_certification_claim_rejected(self):
        data = copy.deepcopy(self.data)
        data["certification_claim"] = True
        with self.assertRaises(ValidationError):
            validate(data)

    def test_inventory_arithmetic_rejected(self):
        data = copy.deepcopy(self.data)
        data["observed_state"]["repositories_token_vazio"] = 74
        with self.assertRaises(ValidationError):
            validate(data)

    def test_missing_heuristic_rejected(self):
        data = copy.deepcopy(self.data)
        data["heuristics"].pop()
        with self.assertRaises(ValidationError):
            validate(data)

    def test_duplicate_heuristic_rejected(self):
        data = copy.deepcopy(self.data)
        data["heuristics"][1][0] = data["heuristics"][0][0]
        with self.assertRaises(ValidationError):
            validate(data)

    def test_bad_effort_range_rejected(self):
        data = copy.deepcopy(self.data)
        data["effort_scenarios"][0][4] = data["effort_scenarios"][0][5] + 1
        with self.assertRaises(ValidationError):
            validate(data)

    def test_gap_without_exit_criteria_rejected(self):
        data = copy.deepcopy(self.data)
        data["gap_ledger"][0][5] = ""
        with self.assertRaises(ValidationError):
            validate(data)

    def test_unknown_owner_role_rejected(self):
        data = copy.deepcopy(self.data)
        data["gap_ledger"][0][6] = ["R99"]
        with self.assertRaises(ValidationError):
            validate(data)

    def test_invalid_maturity_range_rejected(self):
        data = copy.deepcopy(self.data)
        data["maturity_areas"][0][2] = 4
        data["maturity_areas"][0][3] = 2
        with self.assertRaises(ValidationError):
            validate(data)

    def test_integrity_tampering_rejected(self):
        data = copy.deepcopy(self.data)
        data["derived"]["next_gate"] = "UNSEALED_CHANGE"
        with self.assertRaises(ValidationError):
            validate(data)

if __name__ == "__main__":
    unittest.main()
