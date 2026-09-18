#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "probe_systematic_pragmatic_routing.py"

spec = importlib.util.spec_from_file_location("routing_probe", SCRIPT)
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


class RoutingSemanticProbeTest(unittest.TestCase):
    def test_probe_separates_cycle_context_from_operational_gap_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data/routing/cycles").mkdir(parents=True)
            (root / "data/routing/operational-gaps").mkdir(parents=True)

            (root / "data/routing/cycles/cycle.json").write_text(
                json.dumps(
                    {
                        "schema": "cycle/v1",
                        "claim_allowed": False,
                        "F_gap": [{"state": "TOKEN_VAZIO_RUNTIME"}],
                        "F_next": ["run device gate"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "data/routing/operational-gaps/gap-a.json").write_text(
                json.dumps(
                    {
                        "schema": "gap/v1",
                        "gap_id": "GAP-A",
                        "claim_allowed": False,
                        "owner": "repo-a",
                        "status": "TOKEN_VAZIO",
                        "closure_gate": "receipt-a",
                    }
                ),
                encoding="utf-8",
            )
            (root / "data/routing/operational-gaps/gap-a-delta.json").write_text(
                json.dumps(
                    {
                        "schema": "gap/v1",
                        "gap_id": "GAP-A",
                        "claim_allowed": False,
                        "owner": "repo-a",
                        "state": "TOKEN_VAZIO",
                        "next_verifiable_step": "receipt-b",
                    }
                ),
                encoding="utf-8",
            )

            action_map = {
                "schema": "rafaelia.systematic-pragmatic-map/v1",
                "claim_allowed": False,
                "actions": [
                    action("data/routing/cycles/cycle.json"),
                    action("data/routing/operational-gaps/gap-a.json"),
                    action("data/routing/operational-gaps/gap-a-delta.json"),
                ],
            }

            report = mod.build_report(action_map, root)
            self.assertFalse(report["claim_allowed"])
            self.assertEqual(report["cycles"]["selected_actions"], 1)
            self.assertEqual(report["cycles"]["structured_open_context"], 1)
            self.assertEqual(report["cycles"]["closure_or_next_gate"], 1)
            self.assertEqual(report["operational_gaps"]["selected_actions"], 2)
            self.assertEqual(report["operational_gaps"]["with_gap_id"], 2)
            self.assertEqual(report["operational_gaps"]["unique_gap_ids"], 1)
            self.assertEqual(
                report["operational_gaps"]["duplicate_gap_id_groups"],
                {"GAP-A": 2},
            )

    def test_probe_does_not_auto_decide(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data/routing/cycles").mkdir(parents=True)
            (root / "data/routing/cycles/cycle.json").write_text(
                '{"claim_allowed":false,"F_gap":["TOKEN_VAZIO"]}',
                encoding="utf-8",
            )
            action_map = {
                "schema": "rafaelia.systematic-pragmatic-map/v1",
                "claim_allowed": False,
                "actions": [action("data/routing/cycles/cycle.json")],
            }
            report = mod.build_report(action_map, root)
            raw = json.dumps(report)
            self.assertNotIn('"decision"', raw)
            self.assertIn("never assigns G3 or G4 automatically", raw)


if __name__ == "__main__":
    unittest.main()
