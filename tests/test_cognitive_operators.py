#!/usr/bin/env python3
"""Adversarial tests for the cognitive operator invariant."""
from __future__ import annotations
import importlib.util, json, sys, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MODULE=ROOT/"scripts"/"validate_cognitive_operators.py"
MANIFEST=ROOT/"data"/"ontology"/"cognitive-operators.v1.json"
SPEC=importlib.util.spec_from_file_location("validate_cognitive_operators",MODULE)
assert SPEC and SPEC.loader
validator=importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name]=validator
SPEC.loader.exec_module(validator)

def load():
    return validator.load_registry(MANIFEST)

def find(operators,n):
    return next(x for x in operators if x["n"]==n)

class CognitiveOperatorTests(unittest.TestCase):
    def test_registry_valid(self):
        manifest,operators,segment_errors=load()
        self.assertEqual(validator.validate(manifest,operators,segment_errors),[])

    def test_counts_are_honest(self):
        manifest,operators,segment_errors=load()
        summary=validator.build_report(manifest,operators,segment_errors)["summary"]
        self.assertEqual(summary["operators"],56)
        self.assertEqual(summary["implementable"],33)
        self.assertEqual(summary["token_vazio"],23)
        self.assertEqual(summary["physical_bridges"],11)
        self.assertFalse(summary["claim_allowed"])

    def test_ordinals_are_contiguous(self):
        _,operators,_=load()
        self.assertEqual([x["n"] for x in operators],list(range(15,71)))

    def test_token_vazio_requires_gap(self):
        manifest,operators,segment_errors=load()
        find(operators,70).pop("gap")
        self.assertTrue(any("COG-070: TOKEN_VAZIO requires gap" in e for e in validator.validate(manifest,operators,segment_errors)))

    def test_token_vazio_requires_next_gate(self):
        manifest,operators,segment_errors=load()
        find(operators,58).pop("next_gate")
        self.assertTrue(any("COG-058: TOKEN_VAZIO requires next_gate" in e for e in validator.validate(manifest,operators,segment_errors)))

    def test_invalid_formula_cannot_be_implementable(self):
        manifest,operators,segment_errors=load()
        op=find(operators,58); op["execution"]="IMPLEMENTABLE"; op["route"]="RafPolimata"; op["physical_bridge"]=False
        self.assertTrue(any("COG-058: INVALID_AS_STATED cannot be IMPLEMENTABLE" in e for e in validator.validate(manifest,operators,segment_errors)))

    def test_physical_bridge_cannot_be_implementation(self):
        manifest,operators,segment_errors=load()
        op=find(operators,69); op["execution"]="IMPLEMENTABLE"; op["route"]="RafPolimata"
        self.assertTrue(any("COG-069: physical bridge cannot be IMPLEMENTABLE" in e for e in validator.validate(manifest,operators,segment_errors)))

    def test_implementable_routes_to_rafpolimata(self):
        manifest,operators,segment_errors=load()
        find(operators,24)["route"]="Mapa"
        self.assertTrue(any("COG-024: IMPLEMENTABLE must route to RafPolimata" in e for e in validator.validate(manifest,operators,segment_errors)))

    def test_claim_gate_remains_closed(self):
        manifest,operators,segment_errors=load()
        find(operators,16)["claim_allowed"]=True
        self.assertTrue(any("COG-016: claim_allowed must be false" in e for e in validator.validate(manifest,operators,segment_errors)))

    def test_cli_writes_report(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/"audit.json"
            rc=validator.main(["--manifest",str(MANIFEST),"--output",str(output)])
            self.assertEqual(rc,0)
            self.assertTrue(json.loads(output.read_text(encoding="utf-8"))["valid"])

if __name__=="__main__":
    unittest.main()
