from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "tools" / "validate_serpent_dove_gap_metabolism_v1.py"
SPEC = importlib.util.spec_from_file_location("validate_serpent_dove_gap_metabolism_v1", MODULE)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


class SerpentDoveGapMetabolismTests(unittest.TestCase):
    def test_bundle_passes_fail_closed_validator(self):
        result = mod.run()
        self.assertEqual(result["status"], "PASS", result["errors"])
        self.assertIs(result["claim_allowed"], False)
        self.assertGreaterEqual(result["gap_count"], 15)
        self.assertGreaterEqual(result["learning_count"], 2)
        self.assertGreaterEqual(result["fixture_count"], 14)

    def test_search_miss_does_not_become_absence(self):
        decision, reason = mod.policy_decision({
            "signal": "SEARCH_MISS", "proposed_conclusion": "ABSENT",
            "action": "WATCH", "authority": "ALLOW", "certainty": "AMBIGUOUS",
            "reversibility": "READY", "evidence_age": "FRESH",
            "source_role": "PROVIDER_OBSERVATION",
        })
        self.assertEqual(decision, "REJECT")
        self.assertEqual(reason, "search miss cannot prove absence")

    def test_ambiguous_signal_can_watch_but_cannot_act(self):
        common = {
            "signal": "AMBIGUOUS_SIGNAL", "proposed_conclusion": "TOKEN_VAZIO",
            "authority": "ALLOW", "certainty": "AMBIGUOUS", "reversibility": "READY",
            "evidence_age": "FRESH", "source_role": "LOCAL_OBSERVATION",
        }
        decision_watch, _ = mod.policy_decision({**common, "action": "WATCH"})
        decision_act, reason = mod.policy_decision({**common, "action": "ACT_BOUNDED"})
        self.assertEqual(decision_watch, "ALLOW")
        self.assertEqual(decision_act, "REJECT")
        self.assertEqual(reason, "ambiguous evidence cannot trigger ACT_BOUNDED")

    def test_unknown_authority_and_unknown_rollback_hold_action(self):
        base = {
            "signal": "EVIDENCED_BOUNDED_RISK", "proposed_conclusion": "CONTAIN",
            "action": "ACT_BOUNDED", "certainty": "MEASURED", "evidence_age": "FRESH",
            "source_role": "EXECUTION_RECEIPT",
        }
        d1, _ = mod.policy_decision({**base, "authority": "TOKEN_VAZIO", "reversibility": "READY"})
        d2, _ = mod.policy_decision({**base, "authority": "ALLOW", "reversibility": "TOKEN_VAZIO"})
        self.assertEqual(d1, "REJECT")
        self.assertEqual(d2, "REJECT")

    def test_skipped_check_is_not_execution(self):
        decision, reason = mod.policy_decision({
            "signal": "SKIPPED", "proposed_conclusion": "EXECUTED", "action": "WATCH",
            "authority": "ALLOW", "certainty": "MEASURED", "reversibility": "NOT_APPLICABLE",
            "evidence_age": "FRESH", "source_role": "CI_CHECK",
        })
        self.assertEqual(decision, "REJECT")
        self.assertEqual(reason, "skipped is not executed")

    def test_historical_evidence_is_not_current_pass(self):
        decision, reason = mod.policy_decision({
            "signal": "HISTORICAL_PASS", "proposed_conclusion": "CURRENT_PASS",
            "action": "WATCH", "authority": "ALLOW", "certainty": "MEASURED",
            "reversibility": "NOT_APPLICABLE", "evidence_age": "HISTORICAL_ONLY",
            "source_role": "HISTORICAL_RECEIPT",
        })
        self.assertEqual(decision, "REJECT")
        self.assertEqual(reason, "historical or stale evidence cannot promote current PASS")

    def test_parable_is_zero_weight_for_engineering_proof(self):
        conduct = mod.load(mod.CONDUCT)
        self.assertEqual(conduct["source_metaphor"]["epistemic_type"], "PARABLE")
        self.assertEqual(conduct["source_metaphor"]["engineering_evidence_weight"], 0)
        decision, _ = mod.policy_decision({
            "signal": "PARABLE_REFERENCE", "proposed_conclusion": "ENGINEERING_PROOF",
            "action": "WATCH", "authority": "ALLOW", "certainty": "BOUNDED",
            "reversibility": "NOT_APPLICABLE", "evidence_age": "FRESH", "source_role": "PARABLE",
        })
        self.assertEqual(decision, "REJECT")

    def test_p0_gaps_are_non_compensatory_hold(self):
        registry = mod.load(mod.GAPS)
        p0 = [g for g in registry["gaps"] if g["urgency"] == "P0"]
        self.assertGreaterEqual(len(p0), 2)
        self.assertTrue(all(g["action_mode"] == "HOLD" for g in p0))

    def test_every_gap_has_all_eight_analysis_operators(self):
        registry = mod.load(mod.GAPS)
        for gap in registry["gaps"]:
            self.assertEqual(set(gap["operators"]), mod.EXPECTED_OPERATORS)
            self.assertTrue(all(str(value).strip() for value in gap["operators"].values()))

    def test_public_registry_contains_no_drive_locator(self):
        registry = mod.load(mod.GAPS)
        text = json.dumps(registry, ensure_ascii=False)
        self.assertFalse(any(locator in text for locator in mod.PRIVATE_LOCATORS))

    def test_rll_merge_learning_does_not_close_scientific_gaps(self):
        registry = mod.load(mod.GAPS)
        learning = next(x for x in registry["closed_learnings"] if x["id"] == "LEARN-RLL-PR772-CI-HISTORICAL-PENDING")
        self.assertEqual(learning["current_state"], "CLOSED_SCOPED")
        self.assertIn("skipped", learning["boundary"].lower())
        scientific = {g["id"]: g for g in registry["gaps"] if g["domain"] == "RLL_COSMOLOGY"}
        self.assertEqual(scientific["GAP-RLL-FULL-PRIMORDIAL-VERDICT"]["state"], "TOKEN_VAZIO")
        self.assertEqual(scientific["GAP-RLL-FULL-PRIMORDIAL-VERDICT"]["action_mode"], "HOLD")

    def test_novo_fast_crosscheck_remains_distinct_from_exact_run(self):
        registry = mod.load(mod.GAPS)
        gap = next(x for x in registry["gaps"] if x["id"] == "GAP-NOVO-EXACT-ARCH-PIPELINE-FULL-RUN")
        self.assertEqual(gap["state"], "TOKEN_VAZIO_EXACT_PIPELINE_FULL_RUN")
        decision, _ = mod.policy_decision({
            "signal": "FAST_SEMANTIC_CROSSCHECK", "proposed_conclusion": "EXACT_PIPELINE_PASS",
            "action": "WARN", "authority": "ALLOW", "certainty": "MEASURED",
            "reversibility": "NOT_APPLICABLE", "evidence_age": "FRESH",
            "source_role": "DERIVED_AGGREGATE",
        })
        self.assertEqual(decision, "REJECT")


if __name__ == "__main__":
    unittest.main()
