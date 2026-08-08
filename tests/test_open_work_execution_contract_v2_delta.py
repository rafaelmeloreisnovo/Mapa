from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools/validate_open_work_execution_contract_v2_delta.py"
DELTA = ROOT / "data/gaps/open_work_execution_contract.delta.20260808.v2.json"

spec = importlib.util.spec_from_file_location("open_work_v2_delta_validator", VALIDATOR)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class OpenWorkExecutionContractV2DeltaTests(unittest.TestCase):
    def load(self):
        return json.loads(DELTA.read_text(encoding="utf-8"))

    def test_delta_passes_fail_closed_validator(self):
        result = module.validate(DELTA)
        self.assertEqual(result["state"], "PASS")
        self.assertEqual(result["transitions"], 3)
        self.assertEqual(result["unique_patch_semantic_review_refs"], 32)

    def test_release_authority_is_not_promoted_from_lab(self):
        boundary = self.load()["authority_boundary"]
        self.assertTrue(boundary["rll_lab_v2_observed"])
        self.assertFalse(boundary["rll_release_v2_promoted"])
        self.assertFalse(boundary["rll_main_v2_promoted"])
        self.assertFalse(boundary["release_authority_mutated_by_this_delta"])

    def test_ref_accounting_is_closed_without_semantic_overclaim(self):
        data = self.load()
        counts = data["counts"]
        self.assertEqual(counts["patch_equivalent_refs"] + counts["unique_patch_semantic_review_refs"], counts["frozen_diverged_ref_cohort"])
        ref = next(row for row in data["transitions"] if row["predecessor_token"] == "TOKEN_VAZIO_NOT_YET_CLASSIFIED_ALL_582_REFS")
        self.assertEqual(ref["patch_equivalent"], 3)
        self.assertEqual(ref["unique_patch_review"], 32)
        self.assertIn("not semantic equivalence", ref["boundary"])

    def test_scientific_successors_remain_open(self):
        rows = {row["successor_token"]: row for row in self.load()["transitions"]}
        self.assertEqual(rows["TOKEN_VAZIO_ACT_DR6_LCDM_POSTERIOR_CHAIN_REPRODUCTION"]["successor_state"], "OPEN_INTERNAL")
        self.assertEqual(rows["TOKEN_VAZIO_H0_RD_FULL_BOLTZMANN_INFERENCE_INTEGRATION"]["successor_state"], "OPEN_INTERNAL")

    def test_claim_and_merge_remain_disabled(self):
        data = self.load()
        self.assertFalse(data["claim_allowed"])
        self.assertFalse(data["automatic_merge"])
        self.assertTrue(data["append_only"])


if __name__ == "__main__":
    unittest.main()
