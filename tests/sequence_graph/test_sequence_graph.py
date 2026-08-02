#!/usr/bin/env python3
import json
import unittest
from pathlib import Path

from build_sequence_graph import build_graph


ROOT = Path(__file__).resolve().parent


class SequenceGraphContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registry = json.loads(
            (ROOT / "sequence_family_registry.v1.json").read_text(encoding="utf-8")
        )
        cls.graph = build_graph(registry)

    def test_cardinality(self):
        self.assertEqual(len(self.graph["nodes"]), 27)
        self.assertEqual(len(self.graph["edges"]), 26)

    def test_fibonacci_from_123(self):
        nodes = [
            node["parsed_value"]
            for node in self.graph["nodes"]
            if node["family_id"] == "FIB_FROM_123"
        ]
        self.assertEqual(nodes, [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233])

    def test_tribonacci_from_123(self):
        nodes = [
            node["parsed_value"]
            for node in self.graph["nodes"]
            if node["family_id"] == "TRIB_FROM_123"
        ]
        self.assertEqual(nodes, [1, 2, 3, 6, 11, 20, 37, 68, 125, 230, 423, 778])

    def test_raw_seed_and_claim_boundary(self):
        for node in self.graph["nodes"]:
            self.assertEqual(node["raw_token"], "123")
            self.assertFalse(node["claim_allowed"])
        for edge in self.graph["edges"]:
            self.assertFalse(edge["claim_allowed"])

    def test_edge_endpoints_exist(self):
        ids = {node["node_id"] for node in self.graph["nodes"]}
        for edge in self.graph["edges"]:
            self.assertIn(edge["from"], ids)
            self.assertIn(edge["to"], ids)

    def test_deterministic_hash(self):
        registry = json.loads(
            (ROOT / "sequence_family_registry.v1.json").read_text(encoding="utf-8")
        )
        second = build_graph(registry)
        self.assertEqual(self.graph["graph_sha256"], second["graph_sha256"])


if __name__ == "__main__":
    unittest.main()
