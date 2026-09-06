import importlib.util
import math
import sys
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "sementeira_convergence_engine.py"
SPEC = importlib.util.spec_from_file_location("sementeira_convergence_engine", MODULE_PATH)
MOD = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MOD
assert SPEC.loader is not None
SPEC.loader.exec_module(MOD)

class SementeiraConvergenceV5Tests(unittest.TestCase):
    def test_candidate_partition(self):
        self.assertEqual(len(MOD.CANDIDATES), 27)
        self.assertEqual(sum(c.mode == MOD.LOCAL for c in MOD.CANDIDATES), 20)
        self.assertEqual(sum(c.mode != MOD.LOCAL for c in MOD.CANDIDATES), 7)

    def test_fixed_point(self):
        r = MOD.audit_fixed_point()
        self.assertTrue(r["fixed_point"])
        self.assertEqual(r["local_deterministic_remaining"], [])
        self.assertEqual(r["resolved_candidate_count"], 20)
        self.assertEqual(r["unresolved_candidate_count"], 7)

    def test_final_round_zero_gain(self):
        r = MOD.audit_fixed_point()
        self.assertEqual(r["rounds"][-1]["gain"], 0)
        self.assertEqual(r["rounds"][-1]["effort_per_gain"], "INF")
        self.assertEqual(r["marginal_effort_per_gain_at_stop"], "INF")

    def test_gain_curve(self):
        gains = [r["gain"] for r in MOD.audit_fixed_point()["rounds"]]
        self.assertEqual(gains, [6, 8, 3, 2, 1, 0])

    def test_token_vazio_preserved(self):
        r = MOD.audit_fixed_point()
        tokens = {x["token"] for x in r["token_vazio"]}
        self.assertIn("TOKEN_VAZIO_C7_TO_42_CANONICAL_MAP", tokens)
        self.assertIn("TOKEN_VAZIO_T2_TO_T7_PHYSICAL_BRIDGE", tokens)
        self.assertIn("TOKEN_VAZIO_PROVIDER_CI_V5", tokens)
        self.assertNotIn(None, tokens)

    def test_coverage_dimensions(self):
        c = MOD.audit_fixed_point()["coverage"]
        self.assertEqual(len(c["domains"]), 8)
        self.assertEqual(len(c["axes"]), 7)
        self.assertEqual(c["cells"], 56)

    def test_saturation_curve(self):
        xs = [0,1,2,4,8]
        ys = [MOD.saturation_curve(x) for x in xs]
        self.assertTrue(all(a < b for a,b in zip(ys,ys[1:])))
        ds = [MOD.saturation_derivative(x) for x in xs]
        self.assertTrue(all(a > b for a,b in zip(ds,ds[1:])))

    def test_db_calibration(self):
        self.assertAlmostEqual(MOD.ideal_db_power_factor(1), 10**0.1)
        self.assertAlmostEqual(MOD.ideal_db_pressure_factor(1), 10**0.05)
        self.assertAlmostEqual(10*math.log10(2), 3.010299956639812)

    def test_nibiguire_not_token_vazio(self):
        r=MOD.audit_fixed_point()
        self.assertIn("missed structural relation", r["definition"]["NIBIGUIRE"])
        self.assertIn("missing evidence", r["definition"]["TOKEN_VAZIO"])

    def test_claim_scope(self):
        r=MOD.audit_fixed_point()
        self.assertTrue(r["claim_allowed"])
        self.assertIn("local deterministic closure only", r["claim_scope"])

if __name__ == "__main__":
    unittest.main()
