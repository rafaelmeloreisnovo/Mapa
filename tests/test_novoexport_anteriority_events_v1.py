#!/usr/bin/env python3
"""Dedicated falsifiers for MAP-INV-PROV-002.

Boundary under test:
internal occurrence != invention != public disclosure != legal priority != scientific novelty.

These tests deliberately do not provide external/public/legal/scientific evidence and
therefore require TOKEN_VAZIO plus claim_allowed=false for those dimensions.
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "extract_novoexport_anteriority_events_v1.py"
SPEC = importlib.util.spec_from_file_location("novoexport_anteriority", MODULE_PATH)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


CONFIG = {
    "families": [
        {
            "family_id": "FAM-RAFAELIA",
            "canonical_name": "RAFAELIA",
            "aliases": ["RAFAELIA", "RafaelIA"],
        },
        {
            "family_id": "FAM-BITRAF",
            "canonical_name": "BITRAF64",
            "aliases": ["BITRAF64"],
        },
    ]
}


def conversation(*, role="user", text="RAFAELIA", create_time=100.0, message_id="m1"):
    return {
        "id": "conv-1",
        "title": "synthetic",
        "mapping": {
            "node-1": {
                "message": {
                    "id": message_id,
                    "author": {"role": role},
                    "create_time": create_time,
                    "content": {"parts": [text]},
                }
            }
        },
    }


class TestNovoexportAnteriorityEventsV1(unittest.TestCase):
    def write_payload(self, root: Path, payload, name="conversations-000.json") -> Path:
        path = root / name
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def test_internal_match_never_promotes_external_claim_dimensions(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            shard = self.write_payload(root, [conversation(text="RAFAELIA aparece aqui")])
            events = mod.scan_shard(shard, CONFIG)

        self.assertEqual(1, len(events))
        event = events[0]
        self.assertTrue(event["internal_documented"])
        self.assertEqual("E2_CONTENT_FINGERPRINTED", event["evidence_class"])
        self.assertEqual("TOKEN_VAZIO", event["public_disclosure"])
        self.assertEqual("TOKEN_VAZIO", event["legal_priority"])
        self.assertEqual("TOKEN_VAZIO", event["scientific_novelty"])
        self.assertFalse(event["claim_allowed"])

    def test_assistant_occurrence_is_not_user_anteriority_event(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            shard = self.write_payload(root, [conversation(role="assistant")])
            events = mod.scan_shard(shard, CONFIG)
        self.assertEqual([], events)

    def test_alias_matching_deduplicates_case_insensitively_without_retrodating(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            shard = self.write_payload(
                root,
                [conversation(text="RAFAELIA rafaelia RafaelIA", create_time=200.0)],
            )
            events = mod.scan_shard(shard, CONFIG)

        self.assertEqual(1, len(events))
        self.assertEqual("FAM-RAFAELIA", events[0]["family_id"])
        self.assertEqual(200.0, events[0]["created_time"])
        self.assertFalse(events[0]["claim_allowed"])

    def test_first_event_is_chronological_not_input_order(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            shard_a = self.write_payload(
                root,
                [conversation(text="RAFAELIA later", create_time=300.0, message_id="later")],
                "conversations-000.json",
            )
            shard_b = self.write_payload(
                root,
                [conversation(text="RAFAELIA earlier", create_time=100.0, message_id="earlier")],
                "conversations-001.json",
            )
            events = mod.scan_shard(shard_a, CONFIG) + mod.scan_shard(shard_b, CONFIG)
            summary = mod.build_summary(events, CONFIG)

        fam = next(x for x in summary["families"] if x["family_id"] == "FAM-RAFAELIA")
        self.assertEqual("earlier", fam["first_event"]["message_id"])
        self.assertEqual("INTERNAL_DOCUMENTED", fam["state"])
        self.assertFalse(fam["claim_allowed"])

    def test_absent_family_stays_token_vazio(self):
        summary = mod.build_summary([], CONFIG)
        for fam in summary["families"]:
            self.assertEqual("TOKEN_VAZIO_IN_SCANNED_INPUT", fam["state"])
            self.assertIsNone(fam["first_event"])
            self.assertFalse(fam["claim_allowed"])

    def test_source_and_text_hashes_are_stable_and_distinct_objects(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            shard = self.write_payload(root, [conversation(text="BITRAF64 evidence")])
            events = mod.scan_shard(shard, CONFIG)
            source_hash = mod.sha256_file(shard)

        self.assertEqual(1, len(events))
        event = events[0]
        self.assertEqual(source_hash, event["source_file_sha256"])
        self.assertEqual(
            mod.sha256_bytes("BITRAF64 evidence".encode("utf-8")),
            event["text_sha256"],
        )
        self.assertNotEqual(event["source_file_sha256"], event["text_sha256"])

    def test_policy_explicitly_preserves_non_equivalence(self):
        summary = mod.build_summary([], CONFIG)
        policy = summary["policy"]
        self.assertTrue(policy["append_only"])
        self.assertTrue(policy["evidence_first"])
        self.assertTrue(policy["first_mention_not_first_invention"])
        self.assertTrue(policy["internal_anteriority_not_public_disclosure"])
        self.assertTrue(policy["public_disclosure_not_legal_priority"])
        self.assertFalse(policy["claim_allowed_default"])


if __name__ == "__main__":
    unittest.main()
