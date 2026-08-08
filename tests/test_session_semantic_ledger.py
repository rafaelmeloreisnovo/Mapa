from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools/validate_session_semantic_ledger.py"
spec = importlib.util.spec_from_file_location("validate_session_semantic_ledger", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class SessionSemanticLedgerTests(unittest.TestCase):
    def test_seed_passes(self) -> None:
        report = module.validate()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["coverage"]["sessions"], 13)
        self.assertEqual(report["coverage"]["provider_id_gaps"], 13)
        self.assertEqual(report["coverage"]["claim_allowed_true"], 0)

    def test_all_providerless_sessions_are_fail_closed(self) -> None:
        manifest = module.load_json(module.DEFAULT_MANIFEST)
        sessions = module.load_jsonl(ROOT / manifest["shards"]["sessions"])
        for session in sessions:
            self.assertIsNone(session["provider_id"])
            self.assertEqual(session["source_state"], "OBSERVED_CONTEXT_PROVIDER_ID_UNAVAILABLE")
            self.assertTrue(any(g["gap_class"] == "TV-SOURCE" and g["blocking"] for g in session["gaps"]))
            self.assertFalse(session["claim_allowed"])

    def test_relations_resolve_to_known_nodes(self) -> None:
        manifest = module.load_json(module.DEFAULT_MANIFEST)
        concepts = module.load_jsonl(ROOT / manifest["shards"]["concepts"])
        sessions = module.load_jsonl(ROOT / manifest["shards"]["sessions"])
        relations = module.load_jsonl(ROOT / manifest["shards"]["relations"])
        known = {x["concept_id"] for x in concepts} | {x["session_id"] for x in sessions}
        for relation in relations:
            self.assertIn(relation["subject"], known)
            self.assertIn(relation["object"], known)


if __name__ == "__main__":
    unittest.main()
