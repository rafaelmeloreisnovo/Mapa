import copy
import unittest

from tools.validate_global_reconciliation_v1 import load, validate_manifest


class GlobalReconciliationV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = load()

    def test_canonical_manifest_passes(self):
        self.assertEqual(validate_manifest(copy.deepcopy(self.base)), [])

    def test_token_vazio_cannot_collapse_to_numeric_zero(self):
        m = copy.deepcopy(self.base)
        for item in m["typed_absence"]:
            if item["type"] == "TOKEN_VAZIO":
                item["numeric_payload"] = 0
        self.assertIn("token_vazio_collapsed_to_zero", validate_manifest(m))

    def test_post_merge_ci_cannot_be_promoted_without_evidence(self):
        m = copy.deepcopy(self.base)
        m["seed_gate"]["post_merge_ci"] = "PASS"
        self.assertIn("post_merge_pass_without_evidence", validate_manifest(m))

    def test_unprotected_main_cannot_global_promote(self):
        m = copy.deepcopy(self.base)
        m["provider_gate"]["global_promotion"] = True
        self.assertIn("unprotected_main_cannot_global_promote", validate_manifest(m))

    def test_seed_merge_identity_is_pinned(self):
        m = copy.deepcopy(self.base)
        m["seed_gate"]["merge_commit"] = "0" * 40
        self.assertIn("seed_merge_mismatch", validate_manifest(m))

    def test_scaled_fraction_keeps_representation_identity(self):
        m = copy.deepcopy(self.base)
        m["representation_semantics"][0]["right"] = "7/3"
        self.assertIn("scaled_fraction_representation_not_distinct", validate_manifest(m))

    def test_physical_analogy_cannot_promote(self):
        m = copy.deepcopy(self.base)
        m["formal_boundaries"]["fluid_wave_energy"]["claim_allowed"] = True
        self.assertIn("fluid_analogy_boundary_broken", validate_manifest(m))

    def test_local_input_custody_is_complete(self):
        m = copy.deepcopy(self.base)
        m["local_input_custody"].pop()
        self.assertIn("local_input_custody_incomplete", validate_manifest(m))


if __name__ == "__main__":
    unittest.main()
