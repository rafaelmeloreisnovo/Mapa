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
        self.assertGreaterEqual(out["token_vazio"],15)

if __name__=="__main__":
    unittest.main()
