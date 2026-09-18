#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "enrich_systematic_pragmatic_identity_semantics.py"

spec = importlib.util.spec_from_file_location("identity_semantics", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


class IdentitySemanticsEnrichmentTest(unittest.TestCase):
    def _write(self, root: Path, name: str, obj: dict) -> str:
        path = root / f"data/routing/operational-gaps/{name}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(obj), encoding="utf-8")
        return str(path.relative_to(root))

    def _completion(self, source_gap_id: str, source_paths: list[str]) -> dict:
        return {
            "schema": "rafaelia.systematic-pragmatic-canonical-completion/v1",
            "claim_allowed": False,
            "atlas_mutation_allowed": False,
            "summary": {"completion_candidates": 1},
            "completions": [
                {
                    "completion_id": "G4C-" + source_gap_id,
                    "source_gap_id": source_gap_id,
                    "source_paths": source_paths,
                }
            ],
        }

    def test_nested_provider_and_evidence_needed_are_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = self._write(
                root,
                "a",
                {
                    "gap_id": "GAP-A",
                    "claim_allowed": False,
                    "source_pointer": {
                        "provider": "github",
                        "repository": "org/repo",
                    },
                    "detector": {
                        "evidence_needed": "workflow run + job steps + artifact digest"
                    },
                    "context": {
                        "scope": "PR exact-head governance evidence"
                    },
                },
            )
            out = mod.build(self._completion("GAP-A", [rel]), root)
            mod.validate(out)
            fields = out["enrichments"][0]["target_fields"]

            self.assertEqual(
                fields["provider"]["state"], "NORMALIZED_ENUM_CANDIDATE"
            )
            self.assertEqual(fields["provider"]["value"], "GitHub")
            self.assertEqual(fields["scope"]["state"], "EXACT_STRUCTURED")
            self.assertEqual(
                fields["scope"]["value"], "PR exact-head governance evidence"
            )
            self.assertEqual(
                fields["evidence_required"]["state"], "ALIAS_CANDIDATE"
            )
            self.assertEqual(
                fields["evidence_required"]["value"],
                ["workflow run + job steps + artifact digest"],
            )
            self.assertEqual(fields["artifact_id"]["state"], "TOKEN_VAZIO")

    def test_repository_owner_derives_github_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = self._write(
                root,
                "repo-owner",
                {
                    "claim_allowed": False,
                    "owner": "rafaelmeloreisnovo/RafGitTools",
                },
            )
            out = mod.build(self._completion("GAP-REPO", [rel]), root)
            field = out["enrichments"][0]["target_fields"]["provider"]
            self.assertEqual(
                field["state"], "STRUCTURED_DERIVATION_CANDIDATE"
            )
            self.assertEqual(field["value"], "GitHub")

    def test_multiple_evidence_needed_are_unioned_not_conflicted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = self._write(
                root,
                "evidence",
                {
                    "claim_allowed": False,
                    "detector": {"evidence_needed": "run + job"},
                    "closure_gate": {"evidence_needed": "artifact + digest"},
                },
            )
            out = mod.build(self._completion("GAP-EVIDENCE", [rel]), root)
            field = out["enrichments"][0]["target_fields"]["evidence_required"]
            self.assertEqual(field["state"], "ALIAS_CANDIDATE")
            self.assertEqual(
                field["value"], ["run + job", "artifact + digest"]
            )
            self.assertEqual(
                field["combination"], "UNION_OF_COMPLEMENTARY_REQUIREMENTS"
            )

    def test_affected_routes_derive_scope_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = self._write(
                root,
                "scope",
                {
                    "claim_allowed": False,
                    "affected_routes": ["MAPA_TO_RGT", "RGT_TO_TERMUX"],
                },
            )
            out = mod.build(self._completion("GAP-SCOPE", [rel]), root)
            field = out["enrichments"][0]["target_fields"]["scope"]
            self.assertEqual(
                field["state"], "STRUCTURED_DERIVATION_CANDIDATE"
            )
            self.assertEqual(field["value"], ["MAPA_TO_RGT", "RGT_TO_TERMUX"])

    def test_exact_provider_enum_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = self._write(
                root,
                "a",
                {
                    "provider": "Cross-Provider",
                    "claim_allowed": False,
                    "source_pointer": {"provider": "github"},
                },
            )
            out = mod.build(self._completion("GAP-A", [rel]), root)
            field = out["enrichments"][0]["target_fields"]["provider"]
            self.assertEqual(field["state"], "EXACT_STRUCTURED")
            self.assertEqual(field["value"], "Cross-Provider")

    def test_conflicting_exact_scope_fails_closed_to_conflict(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            a = self._write(root, "a", {"claim_allowed": False, "scope": "A"})
            b = self._write(root, "b", {"claim_allowed": False, "scope": "B"})
            out = mod.build(self._completion("GAP-X", [a, b]), root)
            field = out["enrichments"][0]["target_fields"]["scope"]
            self.assertEqual(field["state"], "CONFLICT")
            self.assertEqual(field["value"], "TOKEN_VAZIO")

    def test_artifact_alias_is_not_exact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = self._write(
                root,
                "a",
                {
                    "claim_allowed": False,
                    "receipt_id": "receipt-123",
                },
            )
            out = mod.build(self._completion("GAP-A", [rel]), root)
            field = out["enrichments"][0]["target_fields"]["artifact_id"]
            self.assertEqual(field["state"], "ALIAS_CANDIDATE")
            self.assertEqual(field["value"], "receipt-123")

    def test_validator_rejects_premature_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = self._write(root, "a", {"claim_allowed": False})
            out = mod.build(self._completion("GAP-A", [rel]), root)
            out["enrichments"][0]["proposed_atlas_gap_id"] = "GAP-AUTO"
            with self.assertRaises(ValueError):
                mod.validate(out)


if __name__ == "__main__":
    unittest.main()
