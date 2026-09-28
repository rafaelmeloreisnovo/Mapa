import importlib.util
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("gap_validator", ROOT/"tools"/"validate_model_gap_matrix.py")
MOD=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

class ManifoldModelGapMatrixTests(unittest.TestCase):
    def test_matrix_is_complete_and_fail_closed(self):
        out=MOD.validate(ROOT/"data"/"manifold"/"model_gap_matrix_v1.json")
        self.assertEqual(out["status"],"PASS")
        self.assertEqual(out["models"],15)
        self.assertFalse(out["claim_allowed"])
        self.assertGreaterEqual(out["token_vazio"],14)

    def test_closed_model_can_have_no_token_vazio(self):
        import json, tempfile
        source=json.loads((ROOT/"data"/"manifold"/"model_gap_matrix_v1.json").read_text(encoding="utf-8"))
        source["models"][0]["state"]="PASS_BOUNDED"
        source["models"][0]["token_vazio"]=[]
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/"matrix.json"
            p.write_text(json.dumps(source),encoding="utf-8")
            out=MOD.validate(p)
            self.assertEqual(out["status"],"PASS")

    def test_open_model_without_token_vazio_fails_closed(self):
        import json, tempfile
        source=json.loads((ROOT/"data"/"manifold"/"model_gap_matrix_v1.json").read_text(encoding="utf-8"))
        source["models"][0]["token_vazio"]=[]
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/"matrix.json"
            p.write_text(json.dumps(source),encoding="utf-8")
            with self.assertRaises(SystemExit):
                MOD.validate(p)

if __name__=="__main__":
    unittest.main()
