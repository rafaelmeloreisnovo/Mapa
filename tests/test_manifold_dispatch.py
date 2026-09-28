import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_manifold_dispatch import validate_dispatch

ROOT = Path(__file__).resolve().parents[1]

class ManifoldDispatchTests(unittest.TestCase):
    def test_repository_dispatch_is_bounded_and_legacy_free(self):
        out = validate_dispatch(
            ROOT / "data/manifold/dispatch_omega_v1.json",
            ROOT / "data/manifold/routes_omega_v1.jsonl",
        )
        self.assertEqual(out["status"], "PASS")
        self.assertEqual(out["dispatch_version"], "V2.1")
        self.assertEqual(out["legacy_active_routes"], 0)
        self.assertEqual(out["mu_read_roots"], 3)
        self.assertEqual(out["mu_read_depth"], 1)
        self.assertEqual(out["hotstate_max_lines"], 80)
        self.assertEqual(out["hotstate_max_active_nodes"], 3)
        self.assertFalse(out["claim_allowed"])

    def test_active_start_lite_route_fails_closed(self):
        manifest = ROOT / "data/manifold/dispatch_omega_v1.json"
        row = {
            "route_id": "R9999",
            "trigger": ["bad"],
            "path": ["START_LITE", "SOURCE"],
            "minimum_sources": ["SOURCE"],
            "expansion_condition": ["missing evidence"],
            "evidence_gate": ["x"],
            "rollback": ["x"],
            "state": "ROUTE_DEFINED",
        }
        with tempfile.TemporaryDirectory() as td:
            routes = Path(td) / "routes.jsonl"
            routes.write_text(json.dumps(row) + "\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                validate_dispatch(manifest, routes)

    def test_missing_authority_gate_fails_closed(self):
        source = json.loads(
            (ROOT / "data/manifold/dispatch_omega_v1.json").read_text(encoding="utf-8")
        )
        source["gates"] = [g for g in source["gates"] if g != "authority_resolved"]
        with tempfile.TemporaryDirectory() as td:
            manifest = Path(td) / "dispatch.json"
            manifest.write_text(json.dumps(source), encoding="utf-8")
            with self.assertRaises(SystemExit):
                validate_dispatch(
                    manifest,
                    ROOT / "data/manifold/routes_omega_v1.jsonl",
                )

    def test_hotstate_budget_fails_closed(self):
        source = json.loads(
            (ROOT / "data/manifold/dispatch_omega_v1.json").read_text(encoding="utf-8")
        )
        source["hotstate_policy"]["max_lines"] = 81
        with tempfile.TemporaryDirectory() as td:
            manifest = Path(td) / "dispatch.json"
            manifest.write_text(json.dumps(source), encoding="utf-8")
            with self.assertRaises(SystemExit):
                validate_dispatch(
                    manifest,
                    ROOT / "data/manifold/routes_omega_v1.jsonl",
                )

    def test_current_state_predecessor_must_be_preserved(self):
        source = json.loads(
            (ROOT / "data/manifold/dispatch_omega_v1.json").read_text(encoding="utf-8")
        )
        source["superseded"] = [
            row
            for row in source["superseded"]
            if row["id"] != "1KHzF3yA8B5RSLiTAGnbJ9lVmEc5rn-l6gOcsdmT5YwQ"
        ]
        with tempfile.TemporaryDirectory() as td:
            manifest = Path(td) / "dispatch.json"
            manifest.write_text(json.dumps(source), encoding="utf-8")
            with self.assertRaises(SystemExit):
                validate_dispatch(
                    manifest,
                    ROOT / "data/manifold/routes_omega_v1.jsonl",
                )

if __name__ == "__main__":
    unittest.main()
