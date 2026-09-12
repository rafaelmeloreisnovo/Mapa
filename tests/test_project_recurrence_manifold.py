import json
import tempfile
import unittest
from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("prm", ROOT/"tools/validate_project_recurrence_manifold.py")
MOD=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MOD)

class TestProjectRecurrenceManifold(unittest.TestCase):
    def test_seed_passes(self):
        result=MOD.validate(MOD.load(ROOT/"data/memory/project-recurrence/seed.v1.jsonl"))
        self.assertEqual(result["status"],"PASS")
        self.assertEqual(result["records"],9)
        self.assertFalse(result["claim_allowed"])

    def test_causal_promotion_fails_without_evidence(self):
        rows=MOD.load(ROOT/"data/memory/project-recurrence/seed.v1.jsonl")
        rows[0]["relations"][0]["validity"]="CAUSAL_PROVEN"
        with self.assertRaises(SystemExit):
            MOD.validate(rows)

    def test_privacy_boundary_fails_closed(self):
        rows=MOD.load(ROOT/"data/memory/project-recurrence/seed.v1.jsonl")
        rows[0]["public_privacy"]["raw_session_ids"]=True
        with self.assertRaises(SystemExit):
            MOD.validate(rows)

if __name__=="__main__":
    unittest.main()
