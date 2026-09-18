#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "reconcile_systematic_pragmatic_source_gaps.py"

spec = importlib.util.spec_from_file_location("g4_reconcile", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


def bindings():
    return {
        "schema": "rafaelia.systematic-pragmatic-routing-bindings/v1",
        "claim_allowed": False,
        "gap_binding_candidates": [
            {
                "binding_candidate_id": "GB-a",
                "source_gap_id": "GAP-A",
                "record_count": 1,
                "source_paths": ["data/routing/operational-gaps/a.json"],
            },
            {
                "binding_candidate_id": "GB-b",
                "source_gap_id": "GAP-B",
                "record_count": 1,
                "source_paths": ["data/routing/operational-gaps/b.json"],
            },
            {
                "binding_candidate_id": "GB-c",
                "source_gap_id": "GAP-C",
                "record_count": 2,
                "source_paths": [
                    "data/routing/operational-gaps/c.json",
                    "data/routing/operational-gaps/c-delta.json",
                ],
            },
        ],
    }


def atlas():
    return {
        "schema": "RAFAELIA_EFFECTIVE_GAP_ATLAS_V1",
        "claim_allowed": False,
        "records": [
            {
                "gap_id": "GAP-A",
                "source_refs": ["repo: unrelated/path.json"],
                "predecessors": [],
                "successors": [],
                "effective_state": "TOKEN_VAZIO",
                "priority": "P1",
            },
            {
                "gap_id": "ATLAS-B",
                "source_refs": [
                    "rafaelmeloreisnovo/Mapa: data/routing/operational-gaps/b.json"
                ],
                "predecessors": [],
                "successors": [],
                "effective_state": "BLOCKED",
                "priority": "P0",
            },
            {
                "gap_id": "ATLAS-C1",
                "source_refs": [],
                "predecessors": ["GAP-C"],
                "successors": [],
                "effective_state": "TOKEN_VAZIO",
                "priority": "P2",
            },
            {
                "gap_id": "ATLAS-C2",
                "source_refs": [],
                "predecessors": [],
                "successors": ["GAP-C"],
                "effective_state": "TOKEN_VAZIO",
                "priority": "P2",
            },
        ],
    }


class G4ReconciliationTest(unittest.TestCase):
    def test_exact_id_and_exact_path_are_candidates_not_bindings(self):
        payload = mod.reconcile(bindings(), atlas())
        mod.validate_output(payload)
        rows = {row["source_gap_id"]: row for row in payload["reconciliation"]}

        self.assertEqual(rows["GAP-A"]["status"], "CANDIDATE_EXACT_MATCH")
        self.assertEqual(rows["GAP-A"]["candidate_atlas_gap_ids"], ["GAP-A"])
        self.assertEqual(rows["GAP-A"]["g4"]["atlas_gap_id"], "TOKEN_VAZIO")

        self.assertEqual(rows["GAP-B"]["status"], "CANDIDATE_EXACT_MATCH")
        self.assertEqual(rows["GAP-B"]["candidate_atlas_gap_ids"], ["ATLAS-B"])
        self.assertEqual(rows["GAP-B"]["g4"]["atlas_gap_id"], "TOKEN_VAZIO")

    def test_multiple_exact_lineage_targets_are_ambiguous(self):
        payload = mod.reconcile(bindings(), atlas())
        rows = {row["source_gap_id"]: row for row in payload["reconciliation"]}
        self.assertEqual(rows["GAP-C"]["status"], "AMBIGUOUS_EXACT_EVIDENCE")
        self.assertEqual(
            rows["GAP-C"]["candidate_atlas_gap_ids"],
            ["ATLAS-C1", "ATLAS-C2"],
        )
        self.assertEqual(rows["GAP-C"]["g4"]["state"], "BLOCKED_AMBIGUOUS")

    def test_no_fuzzy_substring_match(self):
        b = bindings()
        b["gap_binding_candidates"] = [
            {
                "binding_candidate_id": "GB-x",
                "source_gap_id": "GAP-X",
                "record_count": 1,
                "source_paths": ["data/routing/operational-gaps/x.json"],
            }
        ]
        a = atlas()
        a["records"] = [
            {
                "gap_id": "PREFIX-GAP-X-SUFFIX",
                "source_refs": [
                    "repo: archive/data/routing/operational-gaps/x.json.backup"
                ],
                "predecessors": ["OLD-GAP-X"],
                "successors": [],
            }
        ]
        payload = mod.reconcile(b, a)
        row = payload["reconciliation"][0]
        self.assertEqual(row["status"], "NO_EXACT_EVIDENCE")
        self.assertEqual(row["candidate_atlas_gap_ids"], [])

    def test_validator_rejects_automatic_binding(self):
        payload = mod.reconcile(bindings(), atlas())
        payload["reconciliation"][0]["g4"]["atlas_gap_id"] = "GAP-A"
        with self.assertRaises(ValueError):
            mod.validate_output(payload)


if __name__ == "__main__":
    unittest.main()
