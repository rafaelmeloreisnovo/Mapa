import copy
import json
import unittest
from pathlib import Path

from tools.validate_empty_state_ontology import OntologyError, validate_data

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "semantics" / "empty-state-ontology.v1.json"


class EmptyStateOntologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_canonical_registry_passes(self):
        out = validate_data(copy.deepcopy(self.data))
        self.assertEqual(out["status"], "PASS")
        self.assertEqual(out["states"], 13)
        self.assertEqual(out["omega8_directions"], 8)
        self.assertFalse(out["claim_allowed"])

    def test_token_vazio_is_not_zero_or_null_or_empty_set(self):
        pairs = {frozenset(p) for p in self.data["hard_distinctions"]}
        for other in ("ZERO", "NULL", "EMPTY_SET"):
            self.assertIn(frozenset(("TOKEN_VAZIO", other)), pairs)

    def test_unobserved_is_not_absence(self):
        pairs = {frozenset(p) for p in self.data["hard_distinctions"]}
        self.assertIn(frozenset(("UNOBSERVED", "ABSENCE")), pairs)

    def test_center_refines_marker_without_rewriting_history(self):
        center = self.data["center_binding"]
        self.assertEqual(center["legacy_expression"], "CENTER=TOKEN_VAZIO")
        self.assertEqual(center["refined_semantic_type"], "VOID")
        self.assertEqual(center["representation_marker"], "TOKEN_VAZIO")

    def test_nothing_absolute_cannot_be_promoted(self):
        bad = copy.deepcopy(self.data)
        row = next(x for x in bad["states"] if x["id"] == "NOTHING_ABSOLUTE")
        row["promotable"] = True
        with self.assertRaises(OntologyError):
            validate_data(bad)

    def test_silent_coercion_is_rejected(self):
        bad = copy.deepcopy(self.data)
        bad["coercion_policy"]["default"] = "ALLOW"
        with self.assertRaises(OntologyError):
            validate_data(bad)

    def test_absence_without_scope_is_rejected(self):
        bad = copy.deepcopy(self.data)
        row = next(x for x in bad["states"] if x["id"] == "ABSENCE")
        row["requires_context"].remove("scope")
        with self.assertRaises(OntologyError):
            validate_data(bad)

    def test_conditional_transition_without_evidence_is_rejected(self):
        bad = copy.deepcopy(self.data)
        tr = next(x for x in bad["transitions"] if x["from"] == "UNOBSERVED" and x["to"] == "ABSENCE")
        tr["requires"] = []
        with self.assertRaises(OntologyError):
            validate_data(bad)

    def test_metaphysical_to_absence_must_stay_denied(self):
        bad = copy.deepcopy(self.data)
        tr = next(x for x in bad["transitions"] if x["from"] == "NOTHING_ABSOLUTE" and x["to"] == "ABSENCE")
        tr["allowed"] = "CONDITIONAL"
        tr["requires"] = ["invented_bridge"]
        with self.assertRaises(OntologyError):
            validate_data(bad)

    def test_duplicate_state_is_rejected(self):
        bad = copy.deepcopy(self.data)
        bad["states"][1]["id"] = "TOKEN_VAZIO"
        with self.assertRaises(OntologyError):
            validate_data(bad)

    def test_omega8_projection_must_remain_complete(self):
        bad = copy.deepcopy(self.data)
        bad["omega8_projection"].pop()
        with self.assertRaises(OntologyError):
            validate_data(bad)


if __name__ == "__main__":
    unittest.main()
