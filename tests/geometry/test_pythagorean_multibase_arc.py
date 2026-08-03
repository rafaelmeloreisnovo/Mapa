#!/usr/bin/env python3
"""Regression tests for the 5-12-13 multibase/circular-arc artifact."""

from __future__ import annotations

import importlib.util
import json
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "generate_pythagorean_multibase_arc.py"
SPEC = importlib.util.spec_from_file_location("pythagorean_multibase_arc", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PythagoreanMultibaseArcTests(unittest.TestCase):
    def test_exact_discovery(self) -> None:
        self.assertEqual(5**2 + 12**2, 13**2)
        self.assertEqual(13**2 - 12**2, 5**2)
        self.assertEqual((12**2, 13**2), (144, 169))

    def test_general_odd_leg_family_contains_5_12_13(self) -> None:
        odd_leg = 5
        adjacent_leg = (odd_leg**2 - 1) // 2
        hypotenuse = (odd_leg**2 + 1) // 2
        self.assertEqual((odd_leg, adjacent_leg, hypotenuse), (5, 12, 13))
        self.assertEqual(odd_leg**2 + adjacent_leg**2, hypotenuse**2)

    def test_known_representations(self) -> None:
        self.assertEqual(MODULE.positional_digits(144, 2), [1, 0, 0, 1, 0, 0, 0, 0])
        self.assertEqual(MODULE.positional_digits(144, 7), [2, 6, 4])
        self.assertEqual(MODULE.positional_digits(144, 12), [1, 0, 0])
        self.assertEqual(MODULE.positional_digits(144, 20), [7, 4])
        self.assertEqual(MODULE.positional_digits(169, 12), [1, 2, 1])
        self.assertEqual(MODULE.positional_digits(169, 13), [1, 0, 0])
        self.assertEqual(MODULE.positional_digits(225, 15), [1, 0, 0])

    def test_value_round_trip_for_every_materialized_base(self) -> None:
        for base in range(2, MODULE.MAX_MATERIALIZED_BASE + 1):
            for _, value in MODULE.VALUES:
                digits = MODULE.positional_digits(value, base)
                self.assertEqual(MODULE.evaluate_digits(digits, base), value)

    def test_corrected_identity_survives_every_materialized_modulus(self) -> None:
        for base in range(2, MODULE.MAX_MATERIALIZED_BASE + 1):
            self.assertEqual((25 % base + 144 % base) % base, 169 % base)

    def test_wrong_15_is_hidden_only_by_divisors_of_56(self) -> None:
        aliases = [
            base
            for base in range(2, MODULE.MAX_MATERIALIZED_BASE + 1)
            if (25 % base + 144 % base) % base == 225 % base
        ]
        self.assertEqual(aliases, [2, 4, 7, 8, 14, 28, 56])

    def test_base_7_exposes_projection_aliasing(self) -> None:
        self.assertEqual(5 % 7, 12 % 7)
        self.assertEqual(25 % 7, 144 % 7)
        self.assertEqual(169 % 7, 225 % 7)

    def test_base_13_wraps_previous_and_gap_squares_to_zero(self) -> None:
        self.assertEqual(25 % 13, 12)
        self.assertEqual(144 % 13, 1)
        self.assertEqual(169 % 13, 0)
        self.assertEqual((25 % 13 + 144 % 13) % 13, 0)

    def test_144_is_a_fixed_numeric_marker_on_clock_60_circle(self) -> None:
        angle = 6 * (144 % 60)
        self.assertEqual(angle, 144)
        fixed = [value for value in range(360) if 6 * (value % 60) == value]
        self.assertEqual(fixed, [0, 72, 144, 216, 288])

    def test_conditional_models_remain_distinct(self) -> None:
        rho = Fraction(225 - 25 - 144, 2 * 5 * 12)
        self.assertEqual(rho, Fraction(7, 15))
        self.assertEqual(225 - 169, 56)

    def test_rendered_jsonl_is_parseable_and_complete(self) -> None:
        lines = MODULE.render_jsonl().splitlines()
        records = [json.loads(line) for line in lines]
        self.assertEqual(len(records), 229)
        self.assertEqual(records[0]["record_type"], "manifest")
        self.assertEqual(records[-1]["record_type"], "summary")
        bases = [record["base"] for record in records if record["record_type"] == "base"]
        self.assertEqual(bases, list(range(1, 226)))


if __name__ == "__main__":
    unittest.main()
