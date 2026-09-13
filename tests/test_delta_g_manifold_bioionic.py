import unittest
from tools.validate_delta_g_manifold_bioionic import validate_rows

BASE = {
    "id": "DGMB-T",
    "statement": "typed relation",
    "status": "HYPOTHESIS",
    "claim_allowed": False,
    "source_class": "AUTHOR_HYPOTHESIS",
    "falsifier": "out-of-sample failure",
    "quantity_types": ["pressure", "voltage"],
}

class TestDeltaGManifold(unittest.TestCase):
    def test_valid_hypothesis(self):
        self.assertEqual(validate_rows([dict(BASE)]), [])

    def test_hypothesis_cannot_be_claim_allowed(self):
        row = dict(BASE)
        row["claim_allowed"] = True
        self.assertTrue(validate_rows([row]))

    def test_identity_collapse_rejected(self):
        row = dict(BASE)
        row["identity_collapse"] = True
        self.assertTrue(validate_rows([row]))

    def test_shannon_thermo_identity_rejected(self):
        row = dict(BASE)
        row["shannon_equals_thermo"] = True
        self.assertTrue(validate_rows([row]))

    def test_ionizing_collapse_rejected(self):
        row = dict(BASE)
        row["physiologic_mv_equals_ionizing"] = True
        self.assertTrue(validate_rows([row]))

if __name__ == "__main__":
    unittest.main()
