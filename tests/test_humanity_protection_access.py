import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "humanity_policy",
    ROOT / "tools/validate_humanity_protection_access.py",
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

class TestHumanityProtectionAccess(unittest.TestCase):
    def test_policy_passes(self):
        out = MOD.validate(MOD.load())
        self.assertEqual(out["status"], "PASS")
        self.assertFalse(out["claim_allowed"])
        self.assertFalse(out["blanket_relicense"])

    def test_blanket_relicense_fails(self):
        p = copy.deepcopy(MOD.load())
        p["access"]["blanket_relicense"] = True
        with self.assertRaises(SystemExit):
            MOD.validate(p)

    def test_removed_privacy_gate_fails(self):
        p = copy.deepcopy(MOD.load())
        p["blocked_by_default"].remove("PERSONAL_OR_SENSITIVE_DATA_UNCLEARED")
        with self.assertRaises(SystemExit):
            MOD.validate(p)

if __name__ == "__main__":
    unittest.main()
