import json
import unittest
from pathlib import Path
from tools.resolve_manifold_route import load_routes, resolve

ROOT=Path(__file__).resolve().parents[1]

class RouteResolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.routes=load_routes(ROOT/"data/manifold/routes_omega_v1.jsonl")
        cls.fx=json.loads((ROOT/"tests/fixtures/manifold_route_resolver_cases.json").read_text(encoding="utf-8"))

    def test_positive_fixtures(self):
        for case in self.fx["positives"]:
            with self.subTest(case=case):
                out=resolve(case["query"],self.routes)
                self.assertEqual(out["status"],case["expect_status"])
                self.assertEqual(out["route_id"],case["expect_route"])
                self.assertEqual(out["catalog_reduction"]["before"],"NP_CATALOG")
                self.assertEqual(out["catalog_reduction"]["after"],"P_CATALOG")
                self.assertFalse(out["catalog_reduction"]["complexity_claim"])
                self.assertEqual(out["catalog_delta"]["route_universe"],len(self.routes))
                self.assertEqual(out["catalog_delta"]["candidate_count_after"],1)
                self.assertEqual(out["catalog_delta"]["delta_np_catalog"],len(self.routes)-1)
                self.assertEqual(out["catalog_delta"]["delta_p_catalog"],1)
                self.assertFalse(out["catalog_delta"]["complexity_claim"])
                self.assertFalse(out["catalog_delta"]["evidence_claim"])
                self.assertFalse(out["claim_allowed"])

    def test_negative_fixtures(self):
        for case in self.fx["negatives"]:
            with self.subTest(case=case):
                out=resolve(case["query"],self.routes)
                self.assertEqual(out["status"],case["expect_status"])
                self.assertEqual(out["catalog_reduction"]["before"],"NP_CATALOG")
                self.assertEqual(out["catalog_reduction"]["after"],"NP_CATALOG")
                self.assertFalse(out["catalog_reduction"]["complexity_claim"])
                self.assertEqual(out["catalog_delta"]["delta_p_catalog"],0)
                self.assertFalse(out["catalog_delta"]["complexity_claim"])
                self.assertFalse(out["catalog_delta"]["evidence_claim"])
                self.assertFalse(out["claim_allowed"])
                if "expect_candidates" in case:
                    self.assertEqual(sorted(out["candidates"]),sorted(case["expect_candidates"]))

    def test_ambiguous_delta_is_measured_not_promoted(self):
        out=resolve("math code",self.routes)
        self.assertEqual(out["catalog_delta"]["candidate_count_after"],2)
        self.assertEqual(out["catalog_delta"]["delta_np_catalog"],len(self.routes)-2)
        self.assertEqual(out["catalog_delta"]["delta_p_catalog"],0)

    def test_unknown_query_preserves_full_candidate_space(self):
        out=resolve("banana azul",self.routes)
        self.assertEqual(out["catalog_delta"]["candidate_count_after"],len(self.routes))
        self.assertEqual(out["catalog_delta"]["delta_np_catalog"],0)
        self.assertEqual(out["catalog_delta"]["delta_p_catalog"],0)
        self.assertEqual(out["catalog_delta"]["delta_section_noise"],2)
        self.assertEqual(out["catalog_delta"]["residual_tokens"],["banana","azul"])

if __name__=="__main__":
    unittest.main()
