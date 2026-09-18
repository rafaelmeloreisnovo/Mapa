#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "materialize_systematic_pragmatic_canonical_completion.py"

spec = importlib.util.spec_from_file_location("canonical_completion", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


class CanonicalCompletionTest(unittest.TestCase):
    def _write_source(self, root: Path, name: str, obj: dict) -> str:
        path = root / f"data/routing/operational-gaps/{name}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(obj), encoding="utf-8")
        return str(path.relative_to(root))

    def test_exact_alias_and_token_vazio_are_separated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = self._write_source(
                root,
                "a",
                {
                    "gap_id": "GAP-A",
                    "claim_allowed": False,
                    "priority": "P1",
                    "classification": "NEAR_MISS",
                    "evidence_for": ["fact-a"],
                    "F_gap": ["unknown-a"],
                    "next_probe": ["probe-a"],
                },
            )
            proposals = {
                "schema": "rafaelia.systematic-pragmatic-g4-proposals/v1",
                "claim_allowed": False,
                "atlas_mutation_allowed": False,
                "proposals": [
                    {
                        "proposal_id": "G4P-GAP-A",
                        "source_gap_id": "GAP-A",
                        "source_paths": [rel],
                        "proposal_action": "PROPOSE_APPEND_NEW",
                        "source_evidence": {
                            "effective_authority_values": ["owner-a"],
                            "authority_resolution_applied": False,
                        },
                    }
                ],
            }

            out = mod.build_completion(proposals, root)
            mod.validate(out)
            row = out["completions"][0]
            fields = row["canonical_field_candidates"]

            self.assertEqual(fields["priority"]["state"], "EXACT_SOURCE_FIELD")
            self.assertEqual(fields["priority"]["value"], "P1")
            self.assertEqual(
                fields["gap_class"]["state"], "SOURCE_ALIAS_CANDIDATE"
            )
            self.assertEqual(fields["gap_class"]["value"], "NEAR_MISS")
            self.assertEqual(
                fields["known"]["state"], "SOURCE_ALIAS_CANDIDATE"
            )
            self.assertEqual(
                fields["authority_required"]["state"],
                "SOURCE_ALIAS_CANDIDATE",
            )
            self.assertEqual(fields["artifact_id"]["state"], "TOKEN_VAZIO")
            self.assertEqual(fields["artifact_id"]["value"], "TOKEN_VAZIO")
            self.assertFalse(row["g4"]["atlas_mutation_allowed"])

    def test_conflicting_exact_fields_require_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            a = self._write_source(
                root,
                "a",
                {
                    "gap_id": "GAP-X",
                    "claim_allowed": False,
                    "priority": "P1",
                },
            )
            b = self._write_source(
                root,
                "b",
                {
                    "gap_id": "GAP-X",
                    "claim_allowed": False,
                    "priority": "P2",
                },
            )
            proposals = {
                "schema": "rafaelia.systematic-pragmatic-g4-proposals/v1",
                "claim_allowed": False,
                "atlas_mutation_allowed": False,
                "proposals": [
                    {
                        "proposal_id": "G4P-GAP-X",
                        "source_gap_id": "GAP-X",
                        "source_paths": [a, b],
                        "proposal_action": "PROPOSE_APPEND_NEW",
                        "source_evidence": {
                            "effective_authority_values": ["owner-x"],
                            "authority_resolution_applied": False,
                        },
                    }
                ],
            }
            out = mod.build_completion(proposals, root)
            field = out["completions"][0]["canonical_field_candidates"]["priority"]
            self.assertEqual(field["state"], "MULTI_SOURCE_REVIEW")
            self.assertEqual(field["value"], "TOKEN_VAZIO")

    def test_authority_unblocked_count_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            a = self._write_source(
                root,
                "resolved",
                {"gap_id": "RESOLVED", "claim_allowed": False},
            )
            proposals = {
                "schema": "rafaelia.systematic-pragmatic-g4-proposals/v1",
                "claim_allowed": False,
                "atlas_mutation_allowed": False,
                "proposals": [
                    {
                        "proposal_id": "G4P-RESOLVED",
                        "source_gap_id": "RESOLVED",
                        "source_paths": [a],
                        "proposal_action": "PROPOSE_APPEND_NEW",
                        "source_evidence": {
                            "effective_authority_values": [
                                "rafaelmeloreisnovo/Mapa",
                                "approval:00_governanca",
                            ],
                            "authority_resolution_applied": True,
                        },
                    }
                ],
            }
            out = mod.build_completion(proposals, root)
            self.assertEqual(out["summary"]["baseline_existing_proposals"], 0)
            self.assertEqual(out["summary"]["newly_unblocked_by_authority"], 1)
            self.assertEqual(out["summary"]["completion_candidates"], 1)

    def test_validator_rejects_premature_atlas_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = self._write_source(
                root,
                "bad",
                {"gap_id": "BAD", "claim_allowed": False},
            )
            proposals = {
                "schema": "rafaelia.systematic-pragmatic-g4-proposals/v1",
                "claim_allowed": False,
                "atlas_mutation_allowed": False,
                "proposals": [
                    {
                        "proposal_id": "G4P-BAD",
                        "source_gap_id": "BAD",
                        "source_paths": [rel],
                        "proposal_action": "PROPOSE_APPEND_NEW",
                        "source_evidence": {
                            "effective_authority_values": ["owner"],
                            "authority_resolution_applied": False,
                        },
                    }
                ],
            }
            out = mod.build_completion(proposals, root)
            out["completions"][0]["proposed_atlas_gap_id"] = "GAP-AUTO"
            with self.assertRaises(ValueError):
                mod.validate(out)


if __name__ == "__main__":
    unittest.main()
