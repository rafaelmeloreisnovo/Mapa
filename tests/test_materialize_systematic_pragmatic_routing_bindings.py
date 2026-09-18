#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "materialize_systematic_pragmatic_routing_bindings.py"

spec = importlib.util.spec_from_file_location("routing_bindings", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


def action(path: str):
    return {
        "path": path,
        "service": "SEMANTIC_TRIAGE",
        "nibiguiri_state": "NIBIGUIRI:CAUSA_DESCONHECIDA",
        "markers": ["TOKEN_VAZIO"],
    }


class RoutingBindingsTest(unittest.TestCase):
    def test_materializes_schema_families_and_gap_id_groups(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data/routing/cycles").mkdir(parents=True)
            (root / "data/routing/operational-gaps").mkdir(parents=True)
            (root / "data/routing/cycles/a.json").write_text(
                '{"schema":"cycle/a","claim_allowed":false,"F_gap":["TOKEN_VAZIO"]}',
                encoding="utf-8",
            )
            (root / "data/routing/cycles/b.json").write_text(
                '{"schema":"cycle/a","claim_allowed":false,"F_gap":["TOKEN_VAZIO"]}',
                encoding="utf-8",
            )
            (root / "data/routing/cycles/c.json").write_text(
                '{"schema":"cycle/b","claim_allowed":false,"F_gap":["TOKEN_VAZIO"]}',
                encoding="utf-8",
            )
            for name, gid in [
                ("g1.json", "GAP-A"),
                ("g1-delta.json", "GAP-A"),
                ("g2.json", "GAP-B"),
            ]:
                (root / f"data/routing/operational-gaps/{name}").write_text(
                    json.dumps(
                        {
                            "schema": "gap/v1",
                            "gap_id": gid,
                            "claim_allowed": False,
                            "owner": "owner",
                            "status": "TOKEN_VAZIO",
                            "closure_gate": "receipt",
                        }
                    ),
                    encoding="utf-8",
                )

            action_map = {
                "schema": "rafaelia.systematic-pragmatic-map/v1",
                "claim_allowed": False,
                "actions": [
                    action("data/routing/cycles/a.json"),
                    action("data/routing/cycles/b.json"),
                    action("data/routing/cycles/c.json"),
                    action("data/routing/operational-gaps/g1.json"),
                    action("data/routing/operational-gaps/g1-delta.json"),
                    action("data/routing/operational-gaps/g2.json"),
                ],
            }
            decisions = [
                {
                    "decision": "SPLIT_REQUIRED",
                    "split_strategy": "SEMANTIC_SCHEMA",
                    "cluster_id": "CL-cycles",
                    "observed": {
                        "domain": "data/routing/cycles",
                        "service": "SEMANTIC_TRIAGE",
                        "nibiguiri_state": "NIBIGUIRI:CAUSA_DESCONHECIDA",
                        "markers": ["TOKEN_VAZIO"],
                    },
                },
                {
                    "decision": "DISTINCT_GAP",
                    "binding_strategy": "PER_EXISTING_GAP_ID",
                    "cluster_id": "CL-gaps",
                    "observed": {
                        "domain": "data/routing/operational-gaps",
                        "service": "SEMANTIC_TRIAGE",
                        "nibiguiri_state": "NIBIGUIRI:CAUSA_DESCONHECIDA",
                        "markers": ["TOKEN_VAZIO"],
                    },
                },
            ]
            result = mod.materialize(action_map, decisions, root)
            self.assertFalse(result["claim_allowed"])
            self.assertEqual(result["summary"]["schema_families"], 2)
            self.assertEqual(result["summary"]["source_gap_binding_candidates"], 2)
            self.assertEqual(result["summary"]["multi_record_gap_ids"], 1)

            families = {row["schema_family"]: row for row in result["schema_families"]}
            self.assertEqual(families["cycle/a"]["record_count"], 2)
            self.assertEqual(families["cycle/a"]["g3"]["state"], "REVIEW_REQUIRED")
            self.assertEqual(
                families["cycle/a"]["g4"]["state"], "BLOCKED_BY_G3"
            )

            gaps = {
                row["source_gap_id"]: row for row in result["gap_binding_candidates"]
            }
            self.assertEqual(gaps["GAP-A"]["record_count"], 2)
            self.assertEqual(
                gaps["GAP-A"]["g4"]["state"], "REVIEW_EXISTING_GAP_ID_BINDING"
            )
            self.assertEqual(gaps["GAP-A"]["g4"]["atlas_gap_id"], "TOKEN_VAZIO")
            self.assertFalse(gaps["GAP-A"]["g4"]["auto_create_gap_id"])

    def test_missing_source_gap_id_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data/routing/operational-gaps").mkdir(parents=True)
            (root / "data/routing/operational-gaps/bad.json").write_text(
                '{"claim_allowed":false,"status":"TOKEN_VAZIO"}',
                encoding="utf-8",
            )
            action_map = {
                "schema": "rafaelia.systematic-pragmatic-map/v1",
                "claim_allowed": False,
                "actions": [action("data/routing/operational-gaps/bad.json")],
            }
            decision = {
                "decision": "DISTINCT_GAP",
                "binding_strategy": "PER_EXISTING_GAP_ID",
                "cluster_id": "CL-gaps",
                "observed": {
                    "domain": "data/routing/operational-gaps",
                    "service": "SEMANTIC_TRIAGE",
                    "nibiguiri_state": "NIBIGUIRI:CAUSA_DESCONHECIDA",
                    "markers": ["TOKEN_VAZIO"],
                },
            }
            with self.assertRaises(ValueError):
                mod.materialize(action_map, [decision], root)


if __name__ == "__main__":
    unittest.main()
