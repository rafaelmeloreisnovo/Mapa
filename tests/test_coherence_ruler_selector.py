#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("selector", ROOT / "scripts/select_coherence_ruler.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MOD)


def read_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class CoherenceRulerSelectorTests(unittest.TestCase):
    def setUp(self):
        self.control = read_json("data/control-plane/coherence-ruler-selector.v1.json")
        self.fixture = read_json("fixtures/coherence_ruler/session_aggregate.v1.json")

    def test_selects_first_governed_ruler(self):
        receipt = MOD.select_ruler(self.control, self.fixture)
        self.assertEqual(receipt["status"], "RULER_FOUND_REGION_RESTRICTED")
        self.assertEqual(receipt["selected_ruler"], "R-INDICES-PLURAL-ORTHOGONAL")
        self.assertEqual(receipt["selected_region"], "PROVENANCE_INDEX_VECTOR")
        self.assertFalse(receipt["random_total_permutation_sweep_required"])
        self.assertFalse(receipt["claim_allowed"])

    def test_similarity_without_evidence_cannot_promote(self):
        fixture = copy.deepcopy(self.fixture)
        fixture["candidates"] = [{
            "id": "HIGH-SIMILARITY-ONLY",
            "priority": 1,
            "region": "PROVENANCE_INDEX_VECTOR",
            "support_axes": ["semantic", "lexical", "visual", "temporal"],
            "evidence_class": "HEURISTIC_ONLY",
            "identity_bound": True,
            "scope_declared": True,
            "falsifier_defined": True,
            "privacy_safe": True,
            "unresolved_contradictions": 0
        }]
        receipt = MOD.select_ruler(self.control, fixture)
        self.assertEqual(receipt["status"], "FAILSAFE_HOLD")
        self.assertEqual(receipt["hold_reason"], "NO_GOVERNED_RULER")

    def test_unresolved_contradiction_holds(self):
        fixture = copy.deepcopy(self.fixture)
        fixture["candidates"] = [copy.deepcopy(fixture["candidates"][0])]
        fixture["candidates"][0]["unresolved_contradictions"] = 1
        receipt = MOD.select_ruler(self.control, fixture)
        self.assertEqual(receipt["status"], "FAILSAFE_HOLD")

    def test_public_safe_boundary_is_fail_closed(self):
        fixture = copy.deepcopy(self.fixture)
        fixture["raw_content_included"] = True
        receipt = MOD.select_ruler(self.control, fixture)
        self.assertEqual(receipt["status"], "FAILSAFE_HOLD")
        self.assertEqual(receipt["hold_reason"], "PUBLIC_SAFE_BOUNDARY_FAILED")

    def test_watchdog_budget_is_enforced(self):
        fixture = copy.deepcopy(self.fixture)
        fixture["relation_edges"] = self.control["limits"]["relations"] + 1
        receipt = MOD.select_ruler(self.control, fixture)
        self.assertEqual(receipt["status"], "FAILSAFE_HOLD")
        self.assertEqual(receipt["hold_reason"], "RELATION_BUDGET_EXCEEDED")


if __name__ == "__main__":
    unittest.main()
