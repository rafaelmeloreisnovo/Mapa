import copy
import json
import unittest
from pathlib import Path

from scripts.validate_branch_evolution_anti_regression_v2 import validate_manifest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/governance/branch_evolution_anti_regression_v2.json"


class BranchEvolutionV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def errors_after(self, mutate):
        data = copy.deepcopy(self.base)
        mutate(data)
        return validate_manifest(data)

    def test_valid_snapshot(self):
        self.assertEqual([], validate_manifest(copy.deepcopy(self.base)))

    def test_claim_cannot_promote(self):
        self.assertTrue(self.errors_after(lambda d: d.__setitem__("claim_allowed", True)))

    def test_automatic_merge_stays_false(self):
        self.assertTrue(self.errors_after(lambda d: d.__setitem__("automatic_merge", True)))

    def test_base_sha_must_be_exact(self):
        self.assertTrue(self.errors_after(lambda d: d["base"].__setitem__("sha", "main")))

    def test_ancestor_cannot_have_ahead_commit(self):
        def mutate(d):
            d["observations"][0]["relation_to_main"]["ahead_by"] = 1
        self.assertTrue(self.errors_after(mutate))

    def test_shadow_requires_main_enhancement_boundary(self):
        def mutate(d):
            x = next(o for o in d["observations"] if o["classification"] == "SHADOWED_BY_MAIN_ENHANCED")
            x["artifact_equivalence"]["main_state"] = "ABSENT"
        self.assertTrue(self.errors_after(mutate))

    def test_noncanonical_merge_cannot_claim_main_base(self):
        def mutate(d):
            x = next(o for o in d["observations"] if o["classification"] == "MERGED_NONCANONICAL_BASE_PENDING_CANONICALIZATION")
            x["source_pr"]["base"] = "main"
        self.assertTrue(self.errors_after(mutate))

    def test_missing_main_artifact_is_required_for_pending_canonicalization(self):
        def mutate(d):
            x = next(o for o in d["observations"] if o["classification"] == "MERGED_NONCANONICAL_BASE_PENDING_CANONICALIZATION")
            x["main_presence"]["all_present"] = True
        self.assertTrue(self.errors_after(mutate))

    def test_duplicate_branch_rejected(self):
        def mutate(d):
            d["observations"].append(copy.deepcopy(d["observations"][0]))
        self.assertTrue(self.errors_after(mutate))

    def test_token_vazio_cannot_be_erased(self):
        self.assertTrue(self.errors_after(lambda d: d["token_vazio"].__setitem__("open", [])))


if __name__ == "__main__":
    unittest.main()
