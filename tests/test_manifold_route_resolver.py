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
                self.assertFalse(out["claim_allowed"])

    def test_negative_fixtures(self):
        for case in self.fx["negatives"]:
            with self.subTest(case=case):
                out=resolve(case["query"],self.routes)
                self.assertEqual(out["status"],case["expect_status"])
                self.assertFalse(out["claim_allowed"])
                if "expect_candidates" in case:
                    self.assertEqual(sorted(out["candidates"]),sorted(case["expect_candidates"]))

if __name__=="__main__":
    unittest.main()
