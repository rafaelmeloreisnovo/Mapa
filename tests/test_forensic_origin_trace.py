#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json, sys, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("forensic_origin_trace",ROOT/"tools"/"forensic_origin_trace.py")
assert SPEC and SPEC.loader
mod=importlib.util.module_from_spec(SPEC); sys.modules[SPEC.name]=mod; SPEC.loader.exec_module(mod)

def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))

class ForensicOriginTraceTests(unittest.TestCase):
    def setUp(self):
        self.ontology=load("data/ontology/rafaelia-operational-ontology.v1.json")
        self.contract=load("data/contracts/forensic-origin-trace.v1.json")
        self.scope=load("data/contracts/gap-scope-lineage.v1.json")
        self.report=mod.trace(self.ontology,self.contract,self.scope)

    def item(self, record_id):
        return next(x for x in self.report["records"] if x["record_id"]==record_id)

    def test_all_unresolved_are_traced_and_scoped(self):
        expected=sum(r["epistemic_state"]=="TOKEN_VAZIO" for r in self.ontology["records"])
        self.assertEqual(len(self.report["records"]),expected)
        self.assertEqual(expected,10)
        self.assertEqual(self.report["summary"]["scope_reconciled"],10)

    def test_no_promotion_is_generated(self):
        self.assertTrue(all(r["promotion_allowed"] is False for r in self.report["records"]))
        self.assertTrue(all(r["root_cause_state"]=="ROOT_CAUSE_NOT_PROVEN" for r in self.report["records"]))

    def test_editorial_status_is_preserved_not_reinterpreted(self):
        src={r["id"]:r["status"] for r in self.ontology["records"]}
        self.assertTrue(all(r["editorial_status_preserved"]==src[r["record_id"]] for r in self.report["records"]))

    def test_dag_original_code_gap_is_resolved_at_engine_scope(self):
        r=self.item("R-DAG-CAUSAL")
        self.assertEqual(r["current_scope_state"],"RESOLVED_AT_ENGINE_TEST_SCOPE")
        self.assertIsNone(r["current_scoped_blocker"])
        self.assertEqual(r["overlay_state"],"HISTORICAL_GAP_RESOLVED_AT_SCOPE")

    def test_bootstrap_engine_pass_does_not_close_replay_fixture(self):
        r=self.item("R-BOOTSTRAP-UQ")
        self.assertEqual(r["current_scope_state"],"OPEN_AT_REPLAY_RECONSTRUCTION_SCOPE")
        self.assertEqual(r["current_scoped_blocker"],"REPLAY_SPECIFIC_DETERMINISTIC_FIXTURE_MISSING")
        self.assertTrue(any(s["scope_id"]=="BOOTSTRAP_ENGINE" and s["state"]=="PASS" for s in r["scope_history"]))

    def test_boundary_schema_pass_does_not_close_replay_execution(self):
        r=self.item("R-ANTIDERIVATIVE-BOUNDARY")
        self.assertEqual(r["current_scoped_blocker"],"BOUNDARY_SENSITIVE_REPLAY_NOT_EXECUTED")
        self.assertTrue(any(s["scope_id"]=="BOUNDARY_SCHEMA" and s["state"]=="PASS" for s in r["scope_history"]))

    def test_locked_weights_are_not_called_calibrated(self):
        r=self.item("R-WEIGHTS-CALIBRATION")
        self.assertEqual(r["current_scoped_blocker"],"BLINDED_CALIBRATION_NOT_EXECUTED")
        self.assertTrue(any(s["scope_id"]=="WEIGHT_ARTIFACT_FREEZE" and s["state"]=="PASS" for s in r["scope_history"]))

    def test_six_repo_lineage_pass_does_not_close_expanded_replay_scope(self):
        r=self.item("R-SOURCE-INDEPENDENCE")
        self.assertEqual(r["current_scope_state"],"OPEN_AT_EXPANDED_SOURCE_SCOPE")
        self.assertTrue(any(s["scope_id"]=="SIX_REPO_TOROID" and s["state"]=="PASS" for s in r["scope_history"]))

    def test_loglog_determinism_is_not_model_competition(self):
        r=self.item("R-LOGLOG-COMPETITION")
        self.assertEqual(r["current_scope_state"],"PARTIAL_SCOPE_PASS_MODEL_COMPETITION_OPEN")

    def test_vector_corpus_is_access_blocked_not_censored(self):
        r=self.item("R-VECTOR-CORPUS")
        self.assertEqual(r["overlay_state"],"BLOCKED_BY_ACCESS")
        self.assertNotIn("CENSORED",r["current_scoped_blocker"])

    def test_human_study_remains_governance_blocked(self):
        r=self.item("R-SEMANTIC-HUMAN-STUDY")
        self.assertEqual(r["overlay_state"],"BLOCKED_BY_GOVERNANCE")

if __name__=="__main__":
    unittest.main()
