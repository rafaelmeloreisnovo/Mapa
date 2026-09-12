import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("licscope",ROOT/"tools/validate_license_scope_registry.py")
MOD=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MOD)

class TestLicenseScopeRegistry(unittest.TestCase):
    def test_registry_passes(self):
        out=MOD.validate(MOD.load())
        self.assertEqual(out["status"],"PASS")
        self.assertFalse(out["claim_allowed"])

    def test_gpl_noncommercial_conflict_fails(self):
        rows=MOD.load()
        rows[0]["custom_rnc_allowed"]="YES_AFTER_FILE_SCOPE_AUDIT"
        with self.assertRaises(SystemExit):
            MOD.validate(rows)

if __name__=="__main__":
    unittest.main()
