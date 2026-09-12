import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class TestLicensingGovernance(unittest.TestCase):
    def test_validator_passes(self):
        p=subprocess.run(
            [sys.executable,str(ROOT/"tools/validate_licensing_governance.py")],
            cwd=ROOT,text=True,capture_output=True
        )
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        result=json.loads(p.stdout)
        self.assertEqual(result["status"],"PASS")
        self.assertFalse(result["third_party_override"])
        self.assertFalse(result["blanket_relicense"])
        self.assertTrue(result["usd1_is_licensor_cap"])

if __name__=="__main__": unittest.main()
