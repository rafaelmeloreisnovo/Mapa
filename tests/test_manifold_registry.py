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
            46,
        )
        self.assertEqual(
            validate_routes(ROOT / "data/manifold/routes_omega_v1.jsonl"),
            11,
        )

    def test_gap_subgraph_is_complete_and_bounded(self):
        out = validate_gap_edges(
            ROOT / "data/manifold/edges_omega_v1.jsonl",
            ROOT / "data/manifold/gaps_omega_v1.jsonl",
        )
        self.assertEqual(out["has_gap"], 19)
        self.assertEqual(out["gap_of"], 8)
        self.assertEqual(out["bound_gaps"], 27)

    def test_eight_directions_bridge_preserves_cultural_provenance_gap(self):
        edges = [
            json.loads(line)
            for line in (ROOT / "data/manifold/edges_omega_v1.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        ]
        gaps = [
            json.loads(line)
            for line in (ROOT / "data/manifold/gaps_omega_v1.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        ]

        edge = next(row for row in edges if row["edge_id"] == "E0043")
        gap = next(row for row in gaps if row["gap_id"] == "G0026")

        self.assertEqual(edge["relation_type"], "HAS_GAP")
        self.assertEqual(edge["target_id"], "gap:G0026")
        self.assertEqual(gap["kind"], "MISSING_SOURCE")
        self.assertEqual(gap["state"], "TOKEN_VAZIO_NAVIGABLE")
        self.assertFalse(gap["claim_allowed"])
        self.assertIn("CULTURAL_PROVENANCE", gap["markers"])

    def test_empty_state_ontology_bridge_preserves_metaphysical_gap(self):
        edges = [
            json.loads(line)
            for line in (ROOT / "data/manifold/edges_omega_v1.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        ]
        gaps = [
            json.loads(line)
            for line in (ROOT / "data/manifold/gaps_omega_v1.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        ]
        bridge = next(row for row in edges if row["edge_id"] == "E0044")
        validator = next(row for row in edges if row["edge_id"] == "E0045")
        gap_edge = next(row for row in edges if row["edge_id"] == "E0046")
        gap = next(row for row in gaps if row["gap_id"] == "G0027")

        self.assertEqual(bridge["relation_type"], "CONTEXTUALIZES")
        self.assertEqual(validator["relation_type"], "VALIDATED_BY")
        self.assertEqual(gap_edge["source_id"], "edge:E0044")
        self.assertEqual(gap_edge["target_id"], "gap:G0027")
        self.assertEqual(gap["kind"], "MISSING_EVIDENCE")
        self.assertEqual(gap["state"], "TOKEN_VAZIO_NAVIGABLE")
        self.assertFalse(gap["claim_allowed"])
        self.assertIn("NOTHING_ABSOLUTE", gap["markers"])

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
