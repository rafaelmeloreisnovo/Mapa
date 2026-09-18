#!/usr/bin/env python3
import json,subprocess,tempfile,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts/validate_systematic_pragmatic_terminal_assurance.py"
DATA=ROOT/"data/governance/SYSTEMATIC_PRAGMATIC_TERMINAL_ASSURANCE_V1.json"

class TerminalAssuranceTest(unittest.TestCase):
    def test_canonical_passes(self):
        r=subprocess.run(["python3",str(SCRIPT),str(DATA)],capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr+r.stdout)

    def test_fake_external_local_change_fails(self):
        d=json.loads(DATA.read_text())
        d["external_gates"][0]["local_code_change_authorized"]=True
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"bad.json"; p.write_text(json.dumps(d))
            r=subprocess.run(["python3",str(SCRIPT),str(p)],capture_output=True,text=True)
            self.assertNotEqual(r.returncode,0)

if __name__=="__main__":
    unittest.main()
