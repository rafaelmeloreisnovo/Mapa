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
        self.report=mod.trace(self.ontology,self.contract)

    def test_all_unresolved_are_traced(self):
        expected=sum(r["epistemic_state"]=="TOKEN_VAZIO" for r in self.ontology["records"])
        self.assertEqual(len(self.report["records"]),expected)
        self.assertEqual(expected,10)

    def test_no_promotion_is_generated(self):
        self.assertTrue(all(r["promotion_allowed"] is False for r in self.report["records"]))
        self.assertTrue(all(r["root_cause_state"]=="ROOT_CAUSE_NOT_PROVEN" for r in self.report["records"]))

    def test_editorial_status_is_preserved_not_reinterpreted(self):
        src={r["id"]:r["status"] for r in self.ontology["records"]}
        self.assertTrue(all(r["editorial_status_preserved"]==src[r["record_id"]] for r in self.report["records"]))

    def test_weights_trace_starts_at_benchmark_gap(self):
        r=next(x for x in self.report["records"] if x["record_id"]=="R-WEIGHTS-CALIBRATION")
        self.assertEqual(r["first_observed_blocker"],"NO_BLINDED_BENCHMARK_OR_GROUND_TRUTH")

    def test_antiderivative_trace_starts_at_boundary(self):
        r=next(x for x in self.report["records"] if x["record_id"]=="R-ANTIDERIVATIVE-BOUNDARY")
        self.assertEqual(r["blocker_family"],"MISSING_BOUNDARY_CONTRACT")

    def test_vector_corpus_is_access_blocked_not_censored(self):
        r=next(x for x in self.report["records"] if x["record_id"]=="R-VECTOR-CORPUS")
        self.assertEqual(r["overlay_state"],"BLOCKED_BY_ACCESS")
        self.assertNotIn("CENSORED",r["first_observed_blocker"])

    def test_human_study_remains_governance_blocked(self):
        r=next(x for x in self.report["records"] if x["record_id"]=="R-SEMANTIC-HUMAN-STUDY")
        self.assertEqual(r["overlay_state"],"BLOCKED_BY_GOVERNANCE")

if __name__=="__main__":
    unittest.main()
