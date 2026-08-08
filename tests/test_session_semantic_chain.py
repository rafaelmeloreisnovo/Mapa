from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools/session_semantic_chain.py"
spec = importlib.util.spec_from_file_location("session_semantic_chain", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class SessionSemanticChainTests(unittest.TestCase):
    def test_projection_has_exact_1to1_chain_coverage(self) -> None:
        rows, report = module.build()
        sessions = module.load_jsonl(ROOT / "data/memory/session-semantic/sessions.v1.jsonl")
        expected = sum(
            len(block["concept_refs"])
            for session in sessions
            for block in session["semantic_blocks"]
        )
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["sessions"], 13)
        self.assertEqual(report["semantic_pairs_expected"], expected)
        self.assertEqual(report["chain_rows"], expected)
        self.assertEqual(report["projected_semantic_coverage"], 1.0)
        self.assertEqual(len(rows), expected)

    def test_current_seed_cannot_promote_without_provider_binding(self) -> None:
        rows, report = module.build()
        self.assertEqual(report["identity_bindings_exact"], 0)
        self.assertEqual(report["identity_pending_sessions"], 13)
        self.assertEqual(report["promotable_sessions"], 0)
        self.assertEqual(report["raw_export_coverage"], "TOKEN_VAZIO")
        for row in rows:
            self.assertEqual(row["identity_status"], "UNRESOLVED_PROVIDER_ID")
            self.assertEqual(row["evidence_state"], "PROJECTED_CONTEXT_ONLY")
            self.assertEqual(row["promotion_state"], "IDENTITY_PENDING")
            self.assertFalse(row["claim_allowed"])
            self.assertFalse(row["promotion_allowed"])
            self.assertIsNone(row["source_sha256"])

    def test_every_chain_identifier_is_unique_and_stable(self) -> None:
        rows_a, _ = module.build()
        rows_b, _ = module.build()
        self.assertEqual(rows_a, rows_b)
        for key in (
            "occurrence_id",
            "relation_id",
            "claim_id",
            "evidence_id",
            "state_id",
            "artifact_id",
        ):
            values = [row[key] for row in rows_a]
            self.assertEqual(len(values), len(set(values)), key)

    def test_title_similarity_is_not_an_accepted_identity_basis(self) -> None:
        invalid = {
            "session_id": "session:test",
            "provider_session_id": "provider-session",
            "provider_message_id": "provider-message",
            "export_artifact_id": "export-file",
            "chunk_coordinate": "message[0]",
            "source_sha256": "0" * 64,
            "match_basis": "TITLE_SIMILARITY",
            "verified": True,
        }
        with self.assertRaises(module.ChainError):
            module.validate_binding(invalid, {"EXACT_PROVIDER_EXPORT"})

    def test_exact_binding_shape_is_accepted_but_does_not_exist_in_seed(self) -> None:
        valid = {
            "session_id": "session:test",
            "provider_session_id": "provider-session",
            "provider_message_id": "provider-message",
            "export_artifact_id": "export-file",
            "chunk_coordinate": "message[0]/content[0]",
            "source_sha256": "a" * 64,
            "match_basis": "EXACT_PROVIDER_EXPORT",
            "verified": True,
        }
        module.validate_binding(valid, {"EXACT_PROVIDER_EXPORT"})


if __name__ == "__main__":
    unittest.main()
