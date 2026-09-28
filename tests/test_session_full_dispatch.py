import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"tools"/"validate_session_full_dispatch.py"
spec=importlib.util.spec_from_file_location("dispatch_validator",MOD)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class SessionFullDispatchTests(unittest.TestCase):
    def test_manifest(self):
        out=m.validate(ROOT/"data"/"dispatch"/"session_full_20260928")
        self.assertEqual(out["status"],"PASS")
        self.assertEqual(out["workstreams"],11)
        self.assertEqual(out["agents"],11)
        self.assertGreaterEqual(out["routes"],4)
        self.assertFalse(out["claim_allowed"])

if __name__=="__main__":
    unittest.main()
