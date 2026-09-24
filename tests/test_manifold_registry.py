import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_manifold_registry import (
    validate_edges,
    validate_gap_edges,
    validate_routes,
)

ROOT = Path(__file__).resolve().parents[1]


class ManifoldRegistryTests(unittest.TestCase):
    def test_repository_seeds(self):
        self.assertEqual(
            validate_edges(ROOT / "data/manifold/edges_omega_v1.jsonl"),
            40,
        )
        self.assertEqual(
            validate_routes(ROOT / "data/manifold/routes_omega_v1.jsonl"),
            10,
        )

    def test_gap_subgraph_is_complete_and_bounded(self):
        out = validate_gap_edges(
            ROOT / "data/manifold/edges_omega_v1.jsonl",
            ROOT / "data/manifold/gaps_omega_v1.jsonl",
        )
        self.assertEqual(out["has_gap"], 17)
        self.assertEqual(out["gap_of"], 8)
        self.assertEqual(out["bound_gaps"], 25)

    def test_duplicate_edge_rejected(self):
        row = {
            "edge_id": "E9999",
            "source_id": "a",
            "relation_type": "RELATES_TO",
            "target_id": "b",
            "scope": "x",
            "evidence_ref": "e",
            "state": "VALIDATED_BOUNDED",
            "contradiction": "",
            "gap": "",
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "e.jsonl"
            path.write_text(
                json.dumps(row) + "\n" + json.dumps(row) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(SystemExit):
                validate_edges(path)

    def test_bad_route_state_rejected(self):
        row = {
            "route_id": "R9999",
            "trigger": ["x"],
            "path": ["a", "b"],
            "minimum_sources": ["a"],
            "expansion_condition": [],
            "evidence_gate": ["g"],
            "rollback": ["a"],
            "state": "PASS",
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "r.jsonl"
            path.write_text(json.dumps(row) + "\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                validate_routes(path)


if __name__ == "__main__":
    unittest.main()
