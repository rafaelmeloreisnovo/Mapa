from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "tools" / "validate_cgen_assurance_10x_v1.py"
CONTRACT_PATH = ROOT / "data" / "governance" / "cgen-assurance-10x10.v1.json"

spec = importlib.util.spec_from_file_location("cgen_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


class CgenAssurance10x10Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    def assertInvalid(self, data, needle=None):
        with self.assertRaises(validator.ValidationError) as ctx:
            validator.validate_contract(data)
        if needle:
            self.assertIn(needle, str(ctx.exception))

    def test_base_contract_passes(self):
        messages = validator.validate_contract(copy.deepcopy(self.base))
        self.assertTrue(any("10 depth levels" in m for m in messages))

    def test_claim_allowed_cannot_be_promoted(self):
        data = copy.deepcopy(self.base)
        data["policy"]["claim_allowed"] = True
        self.assertInvalid(data, "claim_allowed")

    def test_token_vazio_cannot_disappear_from_level(self):
        data = copy.deepcopy(self.base)
        data["depth_levels"][2]["hard_unknown"] = "PASS"
        self.assertInvalid(data, "typed TOKEN_VAZIO")

    def test_p0_cannot_become_compensatory(self):
        data = copy.deepcopy(self.base)
        data["urgency"]["P0"]["cannot_be_compensated"] = False
        self.assertInvalid(data, "non-compensatory")

    def test_censorship_guard_is_required(self):
        data = copy.deepcopy(self.base)
        data["invariants"].remove("CENSORSHIP != VALIDATION")
        self.assertInvalid(data, "missing invariants")

    def test_history_cannot_erase_refuted_or_censored_classes(self):
        data = copy.deepcopy(self.base)
        data["attention_history_states"].remove("HISTORICALLY_CENSORED")
        self.assertInvalid(data, "history-state")

    def test_normative_snapshot_is_bounded(self):
        data = copy.deepcopy(self.base)
        data["normative_snapshot_extension"]["bounded_not_universal"] = False
        self.assertInvalid(data, "bounded")

    def test_nist_ai_rmf_revision_state_is_not_silenced(self):
        data = copy.deepcopy(self.base)
        for source in data["normative_snapshot_extension"]["sources"]:
            if source["id"] == "NIST-AI-RMF-1.0":
                source["state"] = "CURRENT"
        self.assertInvalid(data, "revision state")

    def test_privacy_framework_1_1_is_not_promoted_from_draft(self):
        data = copy.deepcopy(self.base)
        for source in data["normative_snapshot_extension"]["sources"]:
            if source["id"] == "NIST-PRIVACY-FRAMEWORK-1.0":
                source["state"] = "PUBLISHED_1.1"
        self.assertInvalid(data, "1.1 pending")

    def test_eu_ai_act_phased_application_is_preserved(self):
        data = copy.deepcopy(self.base)
        for source in data["normative_snapshot_extension"]["sources"]:
            if source["id"] == "EU-AI-ACT-2024-1689-AMENDED-2026-1744":
                source["state"] = "FULLY_APPLICABLE_ALL_HIGH_RISK"
        self.assertInvalid(data, "phased application")

    def test_external_p0_cannot_be_removed(self):
        data = copy.deepcopy(self.base)
        data["external_p0_preserved"] = []
        self.assertInvalid(data, "external P0")

    def test_open_token_cannot_be_coerced_to_fail(self):
        data = copy.deepcopy(self.base)
        data["open_tokens"][0]["state"] = "FAIL"
        self.assertInvalid(data, "must remain TOKEN_VAZIO")

    def test_gate_count_is_exact(self):
        data = copy.deepcopy(self.base)
        data["gates"].pop()
        self.assertInvalid(data, "exactly 10 gates")


if __name__ == "__main__":
    unittest.main()
