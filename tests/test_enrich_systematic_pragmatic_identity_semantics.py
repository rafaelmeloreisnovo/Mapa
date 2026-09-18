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
