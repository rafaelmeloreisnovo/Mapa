from __future__ import annotations

import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "governance" / "validate_operational_excellence_gate.py"
CONTRACT = ROOT / "data" / "contracts" / "operational-excellence-gate.v1.json"

spec = importlib.util.spec_from_file_location("oecg", SCRIPT)
oecg = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(oecg)


class OperationalExcellenceGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def base_receipt(self):
        fields = self.contract["receipt_required_fields"]
        r = {field: "BOUND" for field in fields}
        r["seven_guards"] = {g: "BOUND" for g in oecg.REQUIRED_GUARDS}
        r["gates"] = {
            "DIGNITY": "PASS",
            "CHILD_SAFETY": "NOT_APPLICABLE",
            "PRIVACY": "PASS",
            "AUTHORITY": "PASS",
            "TRUTH_GAP": "PASS",
        }
        r["claim_allowed"] = False
        r["promotion_requested"] = False
        return r

    def test_contract_is_valid(self):
        self.assertEqual([], oecg.validate_contract(self.contract))

    def test_complete_receipt_passes(self):
        self.assertEqual([], oecg.validate_receipt(self.contract, self.base_receipt()))

    def test_unknown_gate_fails_closed(self):
        r = self.base_receipt()
        r["gates"]["AUTHORITY"] = "TOKEN_VAZIO_AUTHORITY"
        errors = oecg.validate_receipt(self.contract, r)
        self.assertTrue(any("AUTHORITY unresolved" in e for e in errors))

    def test_missing_guard_fails(self):
        r = self.base_receipt()
        r["seven_guards"]["ROLLBACK"] = ""
        errors = oecg.validate_receipt(self.contract, r)
        self.assertIn("guard missing/empty: ROLLBACK", errors)

    def test_promotion_cannot_override_unknown(self):
        r = self.base_receipt()
        r["promotion_requested"] = True
        r["gates"]["PRIVACY"] = "TOKEN_VAZIO_PRIVACY"
        errors = oecg.validate_receipt(self.contract, r)
        self.assertTrue(any("promotion blocked by PRIVACY" in e for e in errors))

    def test_autonomous_goal_creation_forbidden(self):
        c = json.loads(json.dumps(self.contract))
        c["objective_boundary"]["autonomous_goal_creation_allowed"] = True
        self.assertIn("autonomous goal creation must be false", oecg.validate_contract(c))


if __name__ == "__main__":
    unittest.main()
