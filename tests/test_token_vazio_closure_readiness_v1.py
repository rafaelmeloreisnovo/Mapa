import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "validate_token_vazio_closure_readiness_v1.py"
SPEC = importlib.util.spec_from_file_location("validate_token_vazio_closure_readiness_v1", MODULE)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

LEGACY_MODULE = ROOT / "tools" / "resolve_token_vazio.py"
LEGACY_SPEC = importlib.util.spec_from_file_location("resolve_token_vazio", LEGACY_MODULE)
assert LEGACY_SPEC and LEGACY_SPEC.loader
legacy = importlib.util.module_from_spec(LEGACY_SPEC)
LEGACY_SPEC.loader.exec_module(legacy)


class TokenVazioClosureReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = mod.load(mod.CONTRACT)
        cls.gaps = mod.load(mod.GAPS)
        cls.gap_by_id = {
            g["id"]: g for g in cls.gaps["gaps"] if isinstance(g, dict) and "id" in g
        }

    def test_repository_contract_is_structurally_valid(self):
        receipt = mod.run(self.contract, self.gaps)
        self.assertEqual("PASS", receipt["status"], receipt["structural_errors"])
        self.assertFalse(receipt["claim_allowed"])
        self.assertFalse(receipt["closure_is_automatic"])

    def test_current_p0_is_selected_without_scalar_score(self):
        receipt = mod.run(self.contract, self.gaps)
        self.assertIsNotNone(receipt["selected_next"])
        self.assertEqual("GAP-MAPA-SERVER-ENFORCEMENT", receipt["selected_next"]["gap_id"])
        self.assertEqual("P0", receipt["selected_next"]["urgency"])

    def test_unknown_execution_path_remains_token_vazio(self):
        receipt = mod.run(self.contract, self.gaps)
        selected = receipt["selected_next"]
        self.assertEqual("TOKEN_VAZIO_BLOCKED", selected["state"])
        self.assertIn("execution_path_state", selected["missing_dimensions"])
        self.assertIn("effort_class", selected["missing_dimensions"])

    def test_ready_contract_is_not_closed(self):
        profile = copy.deepcopy(self.contract["profiles"][0])
        profile["execution_path_state"] = "AUTHORIZED_REVERSIBLE_PROVIDER_PATH"
        profile["effort_class"] = "LOW"
        assessment = mod.assess_profile(
            self.contract, profile, self.gap_by_id[profile["gap_id"]]
        )
        self.assertEqual("CONTRACT_READY_NOT_EXECUTED", assessment["state"])
        self.assertNotIn("CLOSED", assessment["state"])
        self.assertFalse(assessment["claim_allowed"])

    def test_missing_authority_cannot_be_inferred(self):
        profile = copy.deepcopy(self.contract["profiles"][0])
        profile["authority_ref"] = "TOKEN_VAZIO"
        assessment = mod.assess_profile(
            self.contract, profile, self.gap_by_id[profile["gap_id"]]
        )
        self.assertEqual("TOKEN_VAZIO_BLOCKED", assessment["state"])
        self.assertIn("authority_ref", assessment["missing_dimensions"])

    def test_dependency_or_bump_needs_exception_evidence(self):
        altered = copy.deepcopy(self.contract)
        altered["profiles"][0]["dependency_policy"]["version_bumps"] = True
        altered["profiles"][0]["dependency_policy"]["exception_ref"] = "TOKEN_VAZIO"
        receipt = mod.run(altered, self.gaps)
        self.assertEqual("FAIL", receipt["status"])
        self.assertTrue(
            any("dependency_or_bump_requires_exception_ref" in e for e in receipt["structural_errors"])
        )

    def test_claim_cannot_be_promoted_by_contract(self):
        altered = copy.deepcopy(self.contract)
        altered["profiles"][0]["claim_allowed"] = True
        receipt = mod.run(altered, self.gaps)
        self.assertEqual("FAIL", receipt["status"])
        self.assertTrue(
            any("claim_allowed_must_remain_false" in e for e in receipt["structural_errors"])
        )

    def test_falsifier_drift_is_rejected(self):
        altered = copy.deepcopy(self.contract)
        altered["profiles"][0]["falsifier"] = "A convenient success narrative."
        receipt = mod.run(altered, self.gaps)
        self.assertEqual("FAIL", receipt["status"])
        self.assertTrue(
            any("falsifier_drift_from_source_registry" in e for e in receipt["structural_errors"])
        )

    def test_unprofiled_gaps_are_exposed_not_silently_filled(self):
        receipt = mod.run(self.contract, self.gaps)
        self.assertGreater(receipt["unprofiled_token_vazio_count"], 0)
        self.assertEqual(
            receipt["unprofiled_token_vazio_count"], len(receipt["unprofiled_token_vazio"])
        )

    def test_legacy_direct_close_is_blocked_without_writing(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "decisions.jsonl"
            ok = legacy.record_decision(
                "TV-DEMO", "APPROVED_CLOSED", path, "authorized-human", {"evidence": "demo"}
            )
            self.assertFalse(ok)
            self.assertFalse(path.exists())

    def test_legacy_nonclosing_decision_requires_explicit_authority(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "decisions.jsonl"
            ok = legacy.record_decision(
                "TV-DEMO", "APPROVED_PRESERVED", path, "", None, "preserve uncertainty"
            )
            self.assertFalse(ok)
            self.assertFalse(path.exists())

    def test_legacy_preserved_decision_is_append_only_and_claim_false(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "decisions.jsonl"
            ok = legacy.record_decision(
                "TV-DEMO",
                "APPROVED_PRESERVED",
                path,
                "authorized-human",
                {"evidence_ref": "receipt:demo"},
                "preserve until falsifier runs",
            )
            self.assertTrue(ok)
            rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(1, len(rows))
            self.assertEqual("APPROVED_PRESERVED", rows[0]["decision"])
            self.assertFalse(rows[0]["claim_allowed"])
            self.assertEqual("authorized-human", rows[0]["approved_by"])


if __name__ == "__main__":
    unittest.main()
