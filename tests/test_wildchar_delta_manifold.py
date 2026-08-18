#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.validate_wildchar_delta_manifold import validate

FIXTURE = Path("data/routing/wildchar-delta-manifold.synthetic.v1.json")
REAL_FIXTURE = Path("data/routing/quantum-echoes-otoc-2025.v1.json")


class WildcharDeltaManifoldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_canonical_fixture_passes(self) -> None:
        defects, report = validate(copy.deepcopy(self.base))
        self.assertEqual([], defects)
        self.assertEqual("PASS", report["status"])
        self.assertEqual(0, report["claim_allowed_count"])

    def test_real_quantum_route_passes_and_advances_next_step(self) -> None:
        doc = json.loads(REAL_FIXTURE.read_text(encoding="utf-8"))
        defects, report = validate(doc)
        self.assertEqual([], defects)
        self.assertEqual("PASS", report["status"])
        self.assertEqual(3, report["real_route_count"])
        self.assertEqual(7, report["wildchar_candidate_count"])
        self.assertIn("highest-priority open F_next/falsifier", report["next_verifiable_step"])

    def test_wildchar_cannot_promote_directly(self) -> None:
        doc = copy.deepcopy(self.base)
        doc["routes"][0]["claim_allowed"] = True
        doc["routes"][0]["epistemic_state"] = "VERIFIED_LIMITED"
        doc["routes"][0]["evidence_for"] = ["synthetic evidence"]
        defects, _ = validate(doc)
        self.assertTrue(any("WILDCHAR candidates cannot be promoted directly" in d for d in defects))

    def test_parabola_cannot_be_literal_mechanism(self) -> None:
        doc = copy.deepcopy(self.base)
        doc["routes"][1]["literal_claim"] = True
        defects, _ = validate(doc)
        self.assertTrue(any("analogy/parabola requires literal_claim=false" in d for d in defects))

    def test_token_vazio_requires_reason_and_next_test(self) -> None:
        doc = copy.deepcopy(self.base)
        doc["routes"][0]["token_vazio"] = []
        defects, _ = validate(doc)
        self.assertTrue(any("TOKEN_VAZIO state requires" in d for d in defects))

    def test_numeric_weights_cannot_be_invented(self) -> None:
        doc = copy.deepcopy(self.base)
        doc["wildchar"]["numeric_weights_state"] = "0.91"
        defects, _ = validate(doc)
        self.assertTrue(any("numeric weights must remain TOKEN_VAZIO_CALIBRATION" in d for d in defects))

    def test_anti_regression_sequence_must_be_monotonic(self) -> None:
        doc = copy.deepcopy(self.base)
        doc["anti_regression"][1]["seq"] = 1
        defects, _ = validate(doc)
        self.assertTrue(any("strictly increasing and unique" in d for d in defects))


if __name__ == "__main__":
    unittest.main()
