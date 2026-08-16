import copy
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_rafaelia_session_7d360.py"
DOC = ROOT / "data" / "control-plane" / "RAFAELIA_SESSION_7D360_EVOLUTION_CYCLE.v1.json"

namespace = {}
exec(SCRIPT.read_text(encoding="utf-8"), namespace)
validate = namespace["validate"]


class Session7D360Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(DOC.read_text(encoding="utf-8"))

    def test_canonical_document_passes(self):
        self.assertEqual(validate(self.doc), [])

    def test_claim_promotion_is_blocked(self):
        bad = copy.deepcopy(self.doc)
        bad["claim_allowed"] = True
        self.assertTrue(any("claim_allowed" in e for e in validate(bad)))

    def test_seven_directions_are_mandatory(self):
        bad = copy.deepcopy(self.doc)
        bad["directions"] = bad["directions"][:-1]
        self.assertTrue(any("seven directions" in e for e in validate(bad)))

    def test_full_360_sweep_is_mandatory(self):
        bad = copy.deepcopy(self.doc)
        bad["angular_sweep"]["base_bins"] = 359
        self.assertTrue(any("360" in e for e in validate(bad)))

    def test_uncalibrated_weights_cannot_be_fabricated(self):
        bad = copy.deepcopy(self.doc)
        bad["weight_policy"]["numeric_weights"] = {"D1": 0.9}
        self.assertTrue(any("TOKEN_VAZIO_UNCALIBRATED" in e for e in validate(bad)))

    def test_formula_scope_conflict_must_survive(self):
        bad = copy.deepcopy(self.doc)
        bad["known_scope_conflicts"] = []
        self.assertTrue(any("486-vs-653" in e for e in validate(bad)))

    def test_each_direction_preserves_seven_tokens(self):
        bad = copy.deepcopy(self.doc)
        bad["directions"][0]["session_tokens"] = ["only_one"]
        self.assertTrue(any("seven session tokens" in e for e in validate(bad)))


if __name__ == "__main__":
    unittest.main()
