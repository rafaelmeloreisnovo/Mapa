import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("vrc", ROOT / "tools" / "validate_replay_contract.py")
vrc = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(vrc)

BASE = json.loads((ROOT / "data" / "contracts" / "replay-contract.v1.json").read_text(encoding="utf-8"))

class ReplayContractTests(unittest.TestCase):
    def test_current_contract_passes_limited_structure(self):
        self.assertEqual(vrc.validate(BASE), [])

    def test_token_vazio_cannot_be_coerced_to_zero(self):
        d = copy.deepcopy(BASE)
        d["token_vazio_policy"]["forbidden_coercions"].remove("0")
        self.assertTrue(any("coercion" in e for e in vrc.validate(d)))

    def test_search_miss_is_not_absence(self):
        d = copy.deepcopy(BASE)
        d["token_vazio_policy"]["search_miss_is_absence"] = True
        self.assertIn("SEARCH_MISS != ABSENCE", vrc.validate(d))

    def test_exact_replay_requires_hash_equality(self):
        d = copy.deepcopy(BASE)
        d["reconstruction"]["result"] = "PASS_EXACT"
        d["reconstruction"]["expected_hash"] = "a"
        d["reconstruction"]["observed_hash"] = "b"
        self.assertTrue(any("PASS_EXACT" in e for e in vrc.validate(d)))

    def test_unicode_confusable_policy_is_fail_closed(self):
        d = copy.deepcopy(BASE)
        d["unicode_policy"]["confusable_policy"] = "NORMALIZE_AND_MERGE"
        self.assertTrue(any("unicode confusable" in e for e in vrc.validate(d)))

    def test_dictionary_correction_must_append_and_supersede(self):
        d = copy.deepcopy(BASE)
        d["dictionary_policy"]["correction_policy"] = "OVERWRITE"
        self.assertTrue(any("append-only" in e for e in vrc.validate(d)))

    def test_uncalibrated_weights_cannot_enable_weighting(self):
        d = copy.deepcopy(BASE)
        d["uncertainty"]["weighted_paths_state"] = "TOKEN_VAZIO_CALIBRATION"
        d["uncertainty"]["calibration_required_before_weights"] = False
        self.assertTrue(any("uncalibrated" in e for e in vrc.validate(d)))

    def test_human_study_remains_aborted_until_ethics(self):
        d = copy.deepcopy(BASE)
        d["human_validation"]["state"] = "ACTIVE"
        self.assertTrue(any("human validation" in e for e in vrc.validate(d)))

    def test_historical_plect_cannot_self_promote(self):
        d = copy.deepcopy(BASE)
        d["operator_observations"][0]["formal_binding"] = True
        self.assertTrue(any("PLECT" in e for e in vrc.validate(d)))

if __name__ == "__main__":
    unittest.main()
