import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "validate_reproducibility_seed_v1.py"
SPEC = importlib.util.spec_from_file_location("validate_reproducibility_seed_v1", MODULE)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class ReproducibilitySeedV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = mod.load()

    def test_repository_manifest_passes(self):
        receipt = mod.run(self.manifest)
        self.assertEqual("PASS", receipt["status"], receipt["errors"])
        self.assertEqual(1748365262, receipt["canonical_seed"])
        self.assertFalse(receipt["claim_allowed"])

    def test_seed_identity_is_exactly_bound_to_lockfile(self):
        self.assertEqual(1748365262, self.manifest["seed"])
        self.assertEqual(
            "RAFAELIA_SEED_1748365262_a6a1f608-b889-4803-8f59-d57ce00dba1b",
            self.manifest["seed_identity"],
        )
        self.assertEqual(
            "d5e32a4c07c5f0c328a8dd85d1b3302e930dae47",
            self.manifest["source"]["commit"],
        )
        self.assertEqual(
            "8c04ed93932d00efff94c03d98bc572b8cff9afe",
            self.manifest["source"]["blob_sha"],
        )

    def test_n_to_n_plus_1_seed_mutation_is_killed(self):
        mutant = copy.deepcopy(self.manifest)
        mutant["seed"] += 1
        receipt = mod.run(mutant)
        self.assertEqual("FAIL", receipt["status"])
        self.assertIn("canonical_seed_mismatch", receipt["errors"])
        self.assertIn("seed_identity_numeric_mismatch", receipt["errors"])

    def test_coordinated_seed_and_identity_rewrite_is_still_killed(self):
        mutant = copy.deepcopy(self.manifest)
        mutant["seed"] += 1
        mutant["seed_identity"] = "RAFAELIA_SEED_1748365263_a6a1f608-b889-4803-8f59-d57ce00dba1b"
        mutant["mutation_falsifier"]["baseline_seed"] += 1
        mutant["mutation_falsifier"]["mutant_seed"] += 1
        receipt = mod.run(mutant)
        self.assertEqual("FAIL", receipt["status"])
        self.assertIn("canonical_seed_mismatch", receipt["errors"])
        self.assertIn("canonical_seed_identity_mismatch", receipt["errors"])

    def test_source_commit_or_blob_drift_is_killed(self):
        mutant = copy.deepcopy(self.manifest)
        mutant["source"]["commit"] = "0" * 40
        mutant["source"]["blob_sha"] = "f" * 40
        receipt = mod.run(mutant)
        self.assertEqual("FAIL", receipt["status"])
        self.assertIn("source_commit_mismatch", receipt["errors"])
        self.assertIn("source_blob_sha_mismatch", receipt["errors"])

    def test_claim_cannot_be_promoted_by_seed_gate(self):
        mutant = copy.deepcopy(self.manifest)
        mutant["claim_allowed"] = True
        receipt = mod.run(mutant)
        self.assertEqual("FAIL", receipt["status"])
        self.assertIn("claim_allowed_must_remain_false", receipt["errors"])

    def test_required_scientific_boundaries_cannot_disappear(self):
        mutant = copy.deepcopy(self.manifest)
        mutant["boundaries"] = []
        receipt = mod.run(mutant)
        self.assertEqual("FAIL", receipt["status"])
        self.assertIn("required_boundaries_missing", receipt["errors"])

    def test_derivation_is_deterministic_and_seed_sensitive(self):
        label = "GAP-MAPA-SERVER-ENFORCEMENT"
        a = mod.derive_u64(1748365262, label)
        b = mod.derive_u64(1748365262, label)
        c = mod.derive_u64(1748365263, label)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_method_anchors_are_required(self):
        mutant = copy.deepcopy(self.manifest)
        mutant["method_anchors"] = []
        receipt = mod.run(mutant)
        self.assertEqual("FAIL", receipt["status"])
        self.assertIn("required_method_anchors_missing", receipt["errors"])


if __name__ == "__main__":
    unittest.main()
