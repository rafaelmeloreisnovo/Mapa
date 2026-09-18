#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "materialize_systematic_pragmatic_children.py"

spec = importlib.util.spec_from_file_location("child_materializer", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


def action(path: str):
    return {
        "root": "Mapa",
        "path": path,
        "priority": "P2",
        "service": "SEMANTIC_TRIAGE",
        "markers": ["TOKEN_VAZIO"],
        "nibiguiri_state": "NIBIGUIRI:CAUSA_DESCONHECIDA",
        "authority_required": ["Gap Atlas governance"],
        "evidence_required": ["Triage receipt"],
    }


class ChildMaterializerTest(unittest.TestCase):
    def setUp(self):
        self.parent_id = mod.child_cluster_id("ROOT", "data")
        self.action_map = {
            "schema": "rafaelia.systematic-pragmatic-map/v1",
            "claim_allowed": False,
            "clusters": [
                {
                    "cluster_id": self.parent_id,
                    "root": "Mapa",
                    "domain": "data",
                    "service": "SEMANTIC_TRIAGE",
                    "markers": ["TOKEN_VAZIO"],
                    "nibiguiri_state": "NIBIGUIRI:CAUSA_DESCONHECIDA",
                }
            ],
            "actions": [
                action("data/routing/cycles/a.json"),
                action("data/routing/cycles/b.json"),
                action("data/routing/operational-gaps/c.json"),
                action("data/receipts/x.json"),
            ],
        }
        routing_id = mod.child_cluster_id(self.parent_id, "routing")
        self.routing_id = routing_id
        self.decisions = {
            self.parent_id: {
                "schema": mod.DECISION_SCHEMA,
                "cluster_id": self.parent_id,
                "decision": "SPLIT_REQUIRED",
                "claim_allowed": False,
            },
            routing_id: {
                "schema": mod.DECISION_SCHEMA,
                "cluster_id": routing_id,
                "decision": "SPLIT_REQUIRED",
                "claim_allowed": False,
            },
        }

    def test_recursive_split_materializes_children_and_grandchildren(self):
        result = mod.materialize(self.action_map, self.decisions)
        self.assertFalse(result["claim_allowed"])
        self.assertTrue(result["policy"]["child_is_not_equivalence"])
        scopes = {row["scope_prefix"]: row for row in result["children"]}
        self.assertIn("data/routing", scopes)
        self.assertIn("data/receipts", scopes)
        self.assertIn("data/routing/cycles", scopes)
        self.assertIn("data/routing/operational-gaps", scopes)
        self.assertEqual(scopes["data/routing"]["action_count"], 3)
        self.assertEqual(scopes["data/routing"]["g3"]["state"], "SPLIT_REQUIRED")
        self.assertEqual(
            scopes["data/routing"]["g4"]["state"], "BLOCKED_BY_G3_SPLIT"
        )
        self.assertEqual(scopes["data/receipts"]["g3"]["state"], "REVIEW_REQUIRED")
        self.assertFalse(
            scopes["data/routing/cycles"]["g4"]["auto_create_gap_id"]
        )

    def test_ids_are_deterministic(self):
        first = mod.materialize(self.action_map, self.decisions)
        second = mod.materialize(self.action_map, self.decisions)
        self.assertEqual(first["children"], second["children"])
        self.assertEqual(
            first["children_digest_sha256"], second["children_digest_sha256"]
        )

    def test_orphan_split_decision_fails_closed(self):
        decisions = dict(self.decisions)
        decisions["CL-deadbeefdeadbeef"] = {
            "schema": mod.DECISION_SCHEMA,
            "cluster_id": "CL-deadbeefdeadbeef",
            "decision": "SPLIT_REQUIRED",
            "claim_allowed": False,
        }
        with self.assertRaises(ValueError):
            mod.materialize(self.action_map, decisions)


if __name__ == "__main__":
    unittest.main()
