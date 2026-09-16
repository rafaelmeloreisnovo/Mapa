#!/usr/bin/env python3
import importlib.util
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "sustento_t_observation", ROOT / "tools" / "sustento_t_observation.py"
)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class SustentoTTests(unittest.TestCase):
    def test_majority_and_abstention(self):
        self.assertEqual(mod.majority3([0, 1, 1]), 1)
        self.assertEqual(mod.majority3([0, 0, 1]), 0)
        self.assertEqual(mod.majority4_abstain([0, 0, 1, 1]), mod.TV_TIE)
        self.assertEqual(mod.gate4of5([1, 1, 1, 1, 0]), 1)
        self.assertEqual(mod.gate4of5([1, 1, 1, 0, 0]), mod.TV_INSUFFICIENT)

    def test_iid_exact_formulas(self):
        p = 0.1
        m = mod.iid_metrics(p)
        self.assertAlmostEqual(m["majority3_error"], 0.028)
        self.assertAlmostEqual(m["u4_wrong_with_tie_abstain"], 0.0037)
        self.assertAlmostEqual(m["u4_tie"], 0.0486)
        self.assertAlmostEqual(m["majority5_error"], 0.00856)
        self.assertAlmostEqual(m["gate4of5_wrong"], 0.00046)
        self.assertAlmostEqual(m["gate4of5_abstain"], 0.081)

    def test_sqrt3_contraction(self):
        g = mod.geometry_reference()
        self.assertAlmostEqual(g["sqrt3_over_2"], math.sqrt(3) / 2)
        self.assertAlmostEqual(g["r2"], 3 / 4)
        self.assertAlmostEqual(g["r6"], 27 / 64)
        self.assertAlmostEqual(g["one_minus_r6"], 37 / 64)
        self.assertAlmostEqual(g["difference_complement_minus_r6"], 5 / 32)

    def test_window_is_nested(self):
        prev = mod.contracted_window(0.0, 10.0, 0)
        for level in range(1, 8):
            cur = mod.contracted_window(0.0, 10.0, level)
            self.assertEqual(cur["center"], prev["center"])
            self.assertLess(cur["width"], prev["width"])
            self.assertGreater(cur["left"], prev["left"])
            self.assertLess(cur["right"], prev["right"])
            prev = cur

    def test_gate_fail_closed_and_pass(self):
        missing = {
            "provenance": 1.0,
            "context": 1.0,
            "evidence": 1.0,
            "contradiction": 0.0,
            "uncertainty": 0.0,
            "reproduction": None,
            "rollback": 1.0,
        }
        self.assertEqual(mod.sustento_gate(missing, 0.8)["state"], mod.TV_GATE_INPUT)

        strong = {
            "provenance": 0.95,
            "context": 0.95,
            "evidence": 0.90,
            "contradiction": 0.05,
            "uncertainty": 0.10,
            "reproduction": 0.90,
            "rollback": 1.0,
        }
        result = mod.sustento_gate(strong, 0.8)
        self.assertEqual(result["state"], "PASS")
        self.assertTrue(result["pass"])

    def test_zero_is_not_void(self):
        self.assertEqual(mod.majority3([0, 0, None]), 0)
        self.assertEqual(mod.robust_summary([]), "TOKEN_VAZIO_UNOBSERVED")


if __name__ == "__main__":
    unittest.main()
