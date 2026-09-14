from fractions import Fraction
import math
import unittest

from tools.geometry.typed_crosswalk_v2 import (
    TOPOLOGY,
    angular_cover_state,
    modular_state,
    poincare_metric_scale_k_minus_1,
    poincare_radial_distance_k_minus_1,
    quadratic_root_class,
    rational_with_provenance,
    subdivision_can_preserve_target_topology,
)


class TypedCrosswalkV2Tests(unittest.TestCase):
    def test_7_over_3_and_77_over_33_same_value_different_representation_scale(self):
        a = rational_with_provenance(7, 3)
        b = rational_with_provenance(77, 33)
        self.assertEqual(a["value"], b["value"])
        self.assertEqual(a["value"], Fraction(7, 3))
        self.assertEqual(a["representation_scale"], 1)
        self.assertEqual(b["representation_scale"], 11)

    def test_mod_zero_is_valid_residue_and_quotient_preserves_history(self):
        s = modular_state(70, 7)
        self.assertEqual(s["residue"], 0)
        self.assertEqual(s["quotient"], 10)
        self.assertEqual(s["reconstructed"], 70)

    def test_poincare_standard_k_minus_1_metric_has_factor_four(self):
        scale = poincare_metric_scale_k_minus_1(0.0)
        self.assertEqual(scale, 2.0)
        self.assertAlmostEqual(poincare_radial_distance_k_minus_1(0.5), math.log(3.0))

    def test_negative_discriminant_means_complex_roots_not_hyperbolic_geometry(self):
        out = quadratic_root_class(1, 0, 1)
        self.assertEqual(out["discriminant"], -4)
        self.assertEqual(out["root_space"], "COMPLEX_CONJUGATE")

    def test_angular_cover_preserves_winding_separately_from_remainder(self):
        out = angular_cover_state(360, 7, cover=7)
        self.assertEqual(out["winding_360"], 7)
        self.assertEqual(out["angle_remainder_360"], 0)
        self.assertEqual(out["cover_remainder_degrees"], 0)

    def test_subdivision_does_not_turn_torus_into_sphere(self):
        self.assertEqual(TOPOLOGY["torus_T2"]["chi"], 0)
        self.assertEqual(TOPOLOGY["sphere_S2"]["chi"], 2)
        self.assertFalse(
            subdivision_can_preserve_target_topology("torus_T2", "sphere_S2")
        )


if __name__ == "__main__":
    unittest.main()
