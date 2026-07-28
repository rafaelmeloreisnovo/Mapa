from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validator", ROOT / "scripts" / "validate_longitudinal_vector_evolution.py")
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(validator)
BASE = json.loads((ROOT / "examples" / "longitudinal-vector-evolution.v1.json").read_text(encoding="utf-8"))


class VectorEvolutionTests(unittest.TestCase):
    def test_valid_fixture(self):
        self.assertEqual(validator.validate(copy.deepcopy(BASE))["state"], "PASS")

    def test_claim_allowed_is_blocked(self):
        p = copy.deepcopy(BASE); p["claim_allowed"] = True
        with self.assertRaises(validator.ValidationError): validator.validate(p)

    def test_hidden_model_access_is_blocked(self):
        p = copy.deepcopy(BASE); p["source"]["hidden_model_access"] = True
        with self.assertRaises(validator.ValidationError): validator.validate(p)

    def test_new_dimension_requires_semantics(self):
        p = copy.deepcopy(BASE); p["delta"]["added_dimensions"][0]["semantics"] = "x"
        with self.assertRaises(validator.ValidationError): validator.validate(p)

    def test_duplicate_dimension_is_blocked(self):
        p = copy.deepcopy(BASE); p["delta"]["added_dimensions"].append(copy.deepcopy(p["delta"]["added_dimensions"][0]))
        with self.assertRaises(validator.ValidationError): validator.validate(p)

    def test_removal_requires_receipt(self):
        p = copy.deepcopy(BASE); p["delta"]["removed_dimensions"] = ["origin"]
        with self.assertRaises(validator.ValidationError): validator.validate(p)

    def test_uncalibrated_weight_cannot_have_value(self):
        p = copy.deepcopy(BASE); p["weights"][0]["value"] = 0.9
        with self.assertRaises(validator.ValidationError): validator.validate(p)

    def test_calibrated_weight_requires_evidence(self):
        p = copy.deepcopy(BASE); p["weights"][0] = {"name": "x", "status": "CALIBRATED", "value": 0.5, "evidence_refs": []}
        with self.assertRaises(validator.ValidationError): validator.validate(p)

    def test_evolved_state_requires_all_gates(self):
        p = copy.deepcopy(BASE); p["gates"]["reversibility"] = False
        with self.assertRaises(validator.ValidationError): validator.validate(p)

    def test_symbolic_view_must_block_promotion(self):
        p = copy.deepcopy(BASE); p["layers"]["polysemic"][2]["forbidden_promotions"] = []
        with self.assertRaises(validator.ValidationError): validator.validate(p)

    def test_relation_requires_source(self):
        p = copy.deepcopy(BASE); p["layers"]["relational"][0]["source_ref"] = ""
        with self.assertRaises(validator.ValidationError): validator.validate(p)

    def test_later_revision_requires_lineage(self):
        p = copy.deepcopy(BASE); p["revision"] = 2; p["previous_revision"] = 1; p["previous_event_hash"] = None
        with self.assertRaises(validator.ValidationError): validator.validate(p)

    def test_typed_gap_is_required(self):
        p = copy.deepcopy(BASE); p["layers"]["epistemic"]["typed_gaps"] = ["unknown"]
        with self.assertRaises(validator.ValidationError): validator.validate(p)


if __name__ == "__main__":
    unittest.main()
