#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "materialize_systematic_pragmatic_g4_proposals.py"

spec = importlib.util.spec_from_file_location("g4_proposals", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


class G4ProposalTest(unittest.TestCase):
    def _source(self, root: Path, name: str, *, owner=True, gate=True):
        path = root / f"data/routing/operational-gaps/{name}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        obj = {
            "gap_id": name.upper(),
            "claim_allowed": False,
            "status": "TOKEN_VAZIO",
        }
        if owner:
            obj["owner"] = "producer"
        if gate:
            obj["closure_gate"] = "bounded receipt"
        path.write_text(json.dumps(obj), encoding="utf-8")
        return str(path.relative_to(root))

    def test_no_exact_evidence_becomes_append_proposal_only_when_source_is_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            complete = self._source(root, "complete")
            incomplete = self._source(root, "incomplete", owner=False)
            reconciliation = {
                "schema": "rafaelia.systematic-pragmatic-g4-reconciliation/v1",
                "claim_allowed": False,
                "reconciliation": [
                    {
                        "source_gap_id": "COMPLETE",
                        "source_paths": [complete],
                        "status": "NO_EXACT_EVIDENCE",
                        "candidate_atlas_gap_ids": [],
                    },
                    {
                        "source_gap_id": "INCOMPLETE",
                        "source_paths": [incomplete],
                        "status": "NO_EXACT_EVIDENCE",
                        "candidate_atlas_gap_ids": [],
                    },
                ],
            }
            out = mod.build_proposals(reconciliation, root)
            mod.validate(out)
            by_id = {row["source_gap_id"]: row for row in out["proposals"]}
            self.assertEqual(
                by_id["COMPLETE"]["proposal_action"], "PROPOSE_APPEND_NEW"
            )
            self.assertEqual(
                by_id["INCOMPLETE"]["proposal_action"], "NEEDS_MORE_EVIDENCE"
            )
            self.assertEqual(
                by_id["COMPLETE"]["proposed_atlas_gap_id"], "TOKEN_VAZIO"
            )
            self.assertFalse(by_id["COMPLETE"]["g4"]["atlas_mutation_allowed"])

    def test_structured_and_list_valued_gates_count_as_closure_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "data/routing/operational-gaps/structured.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                json.dumps(
                    {
                        "gap_id": "STRUCTURED",
                        "claim_allowed": False,
                        "owner": "producer",
                        "next_probe": ["run A", "run B"],
                        "closure_gate": {"one": "receipt A", "two": "receipt B"},
                    }
                ),
                encoding="utf-8",
            )
            rel = str(path.relative_to(root))
            reconciliation = {
                "schema": "rafaelia.systematic-pragmatic-g4-reconciliation/v1",
                "claim_allowed": False,
                "reconciliation": [
                    {
                        "source_gap_id": "STRUCTURED",
                        "source_paths": [rel],
                        "status": "NO_EXACT_EVIDENCE",
                        "candidate_atlas_gap_ids": [],
                    }
                ],
            }
            out = mod.build_proposals(reconciliation, root)
            row = out["proposals"][0]
            self.assertEqual(row["proposal_action"], "PROPOSE_APPEND_NEW")
            self.assertEqual(row["source_evidence"]["closure_or_next_gate_records"], 1)
            self.assertTrue(row["source_evidence"]["source_next_gates"])

    def test_scoped_authority_resolution_unblocks_missing_owner_without_closing_gap(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = self._source(root, "resolved", owner=False)
            reconciliation = {
                "schema": "rafaelia.systematic-pragmatic-g4-reconciliation/v1",
                "claim_allowed": False,
                "reconciliation": [
                    {
                        "source_gap_id": "RESOLVED",
                        "source_paths": [source],
                        "status": "NO_EXACT_EVIDENCE",
                        "candidate_atlas_gap_ids": [],
                    }
                ],
            }
            resolutions = {
                "RESOLVED": {
                    "schema": mod.AUTH_SCHEMA,
                    "resolution_id": "AUTH-1",
                    "subject_gap_id": "RESOLVED",
                    "source_path": source,
                    "decision": "AUTHORITY_RESOLVED_SCOPED",
                    "owner_repository": "rafaelmeloreisnovo/Mapa",
                    "lanes": {
                        "evidence_and_validation": "04_validacao",
                        "approval": "00_governanca",
                    },
                    "atlas_mutation_allowed": False,
                    "claim_allowed": False,
                }
            }
            out = mod.build_proposals(reconciliation, root, resolutions)
            row = out["proposals"][0]
            self.assertEqual(row["proposal_action"], "PROPOSE_APPEND_NEW")
            self.assertTrue(row["source_evidence"]["authority_resolution_applied"])
            self.assertEqual(row["source_evidence"]["authority_resolution_id"], "AUTH-1")
            self.assertIn(
                "rafaelmeloreisnovo/Mapa",
                row["source_evidence"]["effective_authority_values"],
            )
            self.assertEqual(row["proposed_atlas_gap_id"], "TOKEN_VAZIO")
            self.assertFalse(row["g4"]["atlas_mutation_allowed"])

    def test_exact_match_proposes_link_but_does_not_bind(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = self._source(root, "link")
            reconciliation = {
                "schema": "rafaelia.systematic-pragmatic-g4-reconciliation/v1",
                "claim_allowed": False,
                "reconciliation": [
                    {
                        "source_gap_id": "LINK",
                        "source_paths": [source],
                        "status": "CANDIDATE_EXACT_MATCH",
                        "candidate_atlas_gap_ids": ["GAP-ATLAS-1"],
                    }
                ],
            }
            out = mod.build_proposals(reconciliation, root)
            row = out["proposals"][0]
            self.assertEqual(row["proposal_action"], "PROPOSE_LINK_EXISTING")
            self.assertEqual(row["candidate_atlas_gap_ids"], ["GAP-ATLAS-1"])
            self.assertEqual(row["proposed_atlas_gap_id"], "TOKEN_VAZIO")
            self.assertFalse(out["atlas_mutation_allowed"])

    def test_validator_rejects_premature_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = self._source(root, "x")
            reconciliation = {
                "schema": "rafaelia.systematic-pragmatic-g4-reconciliation/v1",
                "claim_allowed": False,
                "reconciliation": [
                    {
                        "source_gap_id": "X",
                        "source_paths": [source],
                        "status": "NO_EXACT_EVIDENCE",
                        "candidate_atlas_gap_ids": [],
                    }
                ],
            }
            out = mod.build_proposals(reconciliation, root)
            out["proposals"][0]["proposed_atlas_gap_id"] = "GAP-AUTO-001"
            with self.assertRaises(ValueError):
                mod.validate(out)


if __name__ == "__main__":
    unittest.main()
