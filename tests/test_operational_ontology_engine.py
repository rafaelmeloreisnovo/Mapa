#!/usr/bin/env python3
"""Tests for the conservative RAFAELIA operational ontology engine."""
from __future__ import annotations
import importlib.util, json, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "operational_ontology_engine.py"
SPEC = importlib.util.spec_from_file_location("operational_ontology_engine", MODULE_PATH)
assert SPEC and SPEC.loader
engine = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = engine
SPEC.loader.exec_module(engine)
ONTOLOGY = ROOT / "data" / "ontology" / "rafaelia-operational-ontology.v1.json"

def load(): return json.loads(ONTOLOGY.read_text(encoding="utf-8"))
def first_gap(data): return next(r for r in data["records"] if r["epistemic_state"] == "TOKEN_VAZIO")
def codes(data): return {x["heuristic"] for x in engine.heuristics(data)}

class OperationalOntologyTests(unittest.TestCase):
    def test_canonical_ontology_valid(self): self.assertEqual(engine.validate(load()), [])
    def test_canonical_ontology_has_no_structural_findings(self): self.assertEqual(engine.heuristics(load()), [])
    def test_token_vazio_is_preserved(self):
        report=engine.build_report(load(),"2026-07-23T00:00:00Z")
        self.assertEqual(report["summary"]["states"]["TOKEN_VAZIO"],10)
        self.assertFalse(report["closure"]["claim_allowed"])
    def test_unknown_is_not_zero(self):
        data=load(); r=first_gap(data); r["value"]=0; r["measurement_status"]="UNMEASURED"
        self.assertIn("H-EMPTY-NOT-ZERO",codes(data))
    def test_token_vazio_requires_gap_class(self):
        data=load(); first_gap(data).pop("gap_class")
        self.assertIn("H-GAP-CLASS",codes(data))
    def test_token_vazio_requires_reason(self):
        data=load(); first_gap(data).pop("reason")
        self.assertIn("H-GAP-REASON",codes(data))
    def test_token_vazio_requires_next_gate(self):
        data=load(); first_gap(data)["next_gate"]=""
        self.assertIn("H-DEAD-END",codes(data))
    def test_censorship_not_inferred(self):
        data=load(); r=first_gap(data); r["status"]="CENSORED"; r["decision_context"]="not found"; r.pop("censorship_evidence",None)
        self.assertIn("H-CENSORSHIP",codes(data))
    def test_recursive_operator_requires_exit(self):
        data=load(); data["records"][0]["relations"][0]={"target":"R-SESSION-INVENTORY","operator":"RECURSIVE","scope":"test"}
        self.assertIn("H-LOOP",codes(data))
    def test_reversive_operator_requires_metric(self):
        data=load(); data["records"][0]["relations"][0]={"target":"R-SESSION-INVENTORY","operator":"REVERSIVE","scope":"test"}
        self.assertIn("H-RECON",codes(data))
    def test_antiderivative_requires_boundary(self):
        data=load(); data["records"][0]["relations"][0]={"target":"R-SESSION-INVENTORY","operator":"ANTIDERIVATIVE","scope":"test"}
        self.assertIn("H-ANTIDERIVATIVE",codes(data))
    def test_loglog_requires_competing_models(self):
        data=load(); data["records"][0]["relations"][0]={"target":"R-SESSION-INVENTORY","operator":"LOG_LOG","scope":"test","domain":"positive"}
        self.assertIn("H-LOGLOG",codes(data))
    def test_parallel_bridges_are_methodological(self):
        report=engine.build_report(load(),"2026-07-23T00:00:00Z")
        self.assertTrue(report["trajectory_analysis"]["bridges"])
        self.assertTrue(all(b["classification"]=="METHODOLOGICAL_BRIDGE_NOT_PHYSICAL_EQUIVALENCE" for b in report["trajectory_analysis"]["bridges"]))
    def test_cli_writes_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d); rc=engine.main(["--ontology",str(ONTOLOGY),"--output-json",str(out/"r.json"),"--output-md",str(out/"r.md"),"--generated-at","2026-07-23T00:00:00Z","--strict"])
            self.assertEqual(rc,0); self.assertTrue((out/"r.json").is_file()); self.assertTrue((out/"r.md").is_file())

if __name__ == "__main__": unittest.main()
