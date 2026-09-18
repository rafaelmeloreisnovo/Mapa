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
