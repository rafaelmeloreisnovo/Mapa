import copy, importlib.util, json, pathlib, unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validator", ROOT/"scripts"/"validate_profile_os_registry.py")
validator = importlib.util.module_from_spec(spec); spec.loader.exec_module(validator)
REG = json.loads((ROOT/"data"/"control-plane"/"PROFILE_OS_REGISTRY.v1.json").read_text(encoding="utf-8"))
SUP = validator.load_jsonl(ROOT/"data"/"control-plane"/"PROFILE_OS_SUPERSESSION.v1.jsonl")
GAPS = validator.load_jsonl(ROOT/"data"/"control-plane"/"PROFILE_OS_GAPS.v1.jsonl")

class ProfileOSRegistryTests(unittest.TestCase):
    def test_current_registry_passes(self): self.assertEqual([], validator.validate(REG, SUP, GAPS))
    def test_duplicate_provider_id_rejected(self):
        r=copy.deepcopy(REG); r["objects"].append(copy.deepcopy(r["objects"][0])); self.assertTrue(any("duplicate object provider_id" in e for e in validator.validate(r,SUP,GAPS)))
    def test_same_title_different_ids_allowed(self):
        r=copy.deepcopy(REG); clone=copy.deepcopy(r["objects"][0]); clone["provider_id"]="different-id"; r["objects"].append(clone); self.assertFalse(any("duplicate object provider_id" in e for e in validator.validate(r,SUP,GAPS)))
    def test_delete_policy_rejected(self):
        r=copy.deepcopy(REG); r["delete_policy"]="DELETE_DUPLICATES"; self.assertIn("delete_policy must be NO_DELETE", validator.validate(r,SUP,GAPS))
    def test_claim_promotion_rejected(self):
        r=copy.deepcopy(REG); r["claim_allowed"]=True; self.assertIn("claim_allowed must be false", validator.validate(r,SUP,GAPS))
    def test_supersession_self_loop_rejected(self):
        s=copy.deepcopy(SUP); s[0]["target"]["provider_id"]=s[0]["source"]["provider_id"]; self.assertTrue(any("invalid supersession endpoints" in e for e in validator.validate(REG,s,GAPS)))
    def test_token_zero_rejected(self):
        g=copy.deepcopy(GAPS); g[0]["state"]=0; self.assertTrue(any("cannot encode TOKEN_VAZIO as zero" in e for e in validator.validate(REG,SUP,g)))

if __name__ == "__main__": unittest.main()
