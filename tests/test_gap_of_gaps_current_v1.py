import json
import pathlib
import subprocess
import sys
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
P=ROOT/"data"/"governance"/"gap_of_gaps_current_v1.json"

class GapOfGapsCurrentV1Test(unittest.TestCase):
    def test_contract(self):
        o=json.loads(P.read_text(encoding="utf-8"))
        self.assertFalse(o["claim_allowed"])
        self.assertEqual(o["architecture_state"]["state"],"STRUCTURAL_PASS_MERGED")
        self.assertTrue(o["architecture_state"]["provider_governance_is_separate"])
        self.assertGreaterEqual(o["counts"]["indexed_entries"], 1)
        self.assertTrue(any("TOKEN_VAZIO" in e["state"] for e in o["entries"]))

    def test_validator(self):
        cp=subprocess.run([sys.executable,str(ROOT/"tools"/"validate_gap_of_gaps_current_v1.py")],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
        self.assertIn("PASS gap_of_gaps_current_v1",cp.stdout)

if __name__=="__main__":
    unittest.main()
