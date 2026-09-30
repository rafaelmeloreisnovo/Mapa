import copy
import importlib.util
import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
VALIDATOR=ROOT/"tools"/"validate_authorial_omega_hypervisor_federation_v1.py"
MANIFEST=ROOT/"data"/"manifold"/"authorial_omega_hypervisor_federation_v1.json"
spec=importlib.util.spec_from_file_location("ohv", VALIDATOR)
M=importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

class AuthorialOmegaHypervisorFederationV1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.obj=json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_current_manifest(self):
        self.assertTrue(M.validate(copy.deepcopy(self.obj)))

    def test_reject_whole_vectra_authorship(self):
        bad=copy.deepcopy(self.obj)
        for x in bad["model_references"]:
            if x["id"]=="VECTRA_STRUCTURAL_MODEL":
                x["whole_repo_authorial"]=True
        with self.assertRaises(M.ValidationError):
            M.validate(bad)

    def test_reject_bl0_mirror_drift(self):
        bad=copy.deepcopy(self.obj)
        bad["proven_authorial_assets"][0]["proof"]["byte_identical_mirrors"][0]["blob"]="0"*40
        with self.assertRaises(M.ValidationError):
            M.validate(bad)

    def test_reject_public_raw_payload(self):
        bad=copy.deepcopy(self.obj)
        bad["mounts"][3]["raw_payload_publication"]=True
        with self.assertRaises(M.ValidationError):
            M.validate(bad)

    def test_reject_missing_gap_index(self):
        bad=copy.deepcopy(self.obj)
        bad["F_gap"]=bad["F_gap"][:-1]
        with self.assertRaises(M.ValidationError):
            M.validate(bad)

if __name__=="__main__":
    unittest.main()
