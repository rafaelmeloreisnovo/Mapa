import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/validate_rll_session_avalanche_route.py"
ROUTE = ROOT / "data/federation/rll-session-avalanche-route-v2.json"
spec = importlib.util.spec_from_file_location("route_validator", SCRIPT)
m = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(m)


class TestRLLSessionAvalancheRouteV2(unittest.TestCase):
    def setUp(self):
        self.route = json.loads(ROUTE.read_text())

    def test_route_valid(self):
        self.assertEqual(m.validate(self.route), [])

    def test_route_supersedes_v1(self):
        self.assertEqual(
            self.route["supersedes"],
            "data/federation/rll-session-avalanche-route-v1.json",
        )

    def test_three_external_commits_pinned(self):
        external = [node for node in self.route["nodes"] if node["role"] != "POINTER_ONLY"]
        self.assertEqual(len(external), 3)
        self.assertTrue(all(m.SHA40.fullmatch(node["commit"]) for node in external))

    def test_compression_bridge_mapped(self):
        rll = next(node for node in self.route["nodes"] if node["id"] == "RLL_PHYSICS")
        self.assertIn(
            "data/pipelines/strong_gravity/relativistic_compression_radiation_bridge.py",
            rll["artifacts"],
        )

    def test_capsule_v2_mapped(self):
        gov = next(node for node in self.route["nodes"] if node["id"] == "RAFGITTOOLS_GOVERNANCE")
        self.assertIn("configs/session-single-subtokenization-v2.json", gov["artifacts"])

    def test_map_remains_pointer_only(self):
        pointer = next(node for node in self.route["nodes"] if node["id"] == "MAPA_POINTER")
        self.assertEqual(pointer["role"], "POINTER_ONLY")
        self.assertFalse(self.route["invariants"]["map_is_source_authority"])

    def test_claim_closed(self):
        self.assertFalse(self.route["invariants"]["claim_allowed"])


if __name__ == "__main__":
    unittest.main()
