#!/usr/bin/env python3
"""Regression tests for the chain-of-custody semantic validator."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_chain_of_custody.py"
SPEC = importlib.util.spec_from_file_location("custody_validator", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def base_event() -> dict:
    return {
        "schema_version": "mapa.custody-event.v1",
        "event_id": "COC-20260721T122734Z-TEST_EVENT",
        "timestamp_utc": "2026-07-21T12:27:34Z",
        "repository": "rafaelmeloreisnovo/Mapa",
        "branch": "test/custody",
        "source_ref": "main",
        "previous_event_id": None,
        "actor": {"type": "automation", "id": "unittest"},
        "operation": "VALIDATE",
        "object": {
            "path": "indices/example.jsonl",
            "media_type": "application/x-ndjson",
            "size_bytes": 1,
            "sha256": None,
            "blake3": None,
        },
        "epistemic_state": "FATO",
        "claim_allowed": True,
        "evidence": [
            {"kind": "file", "reference": "indices/example.jsonl"}
        ],
        "controls": {
            "integrity": "partial",
            "traceability": "verified",
            "reproducibility": "verified",
            "confidentiality": "public",
        },
        "sigma": {
            "phase": "MEASURE",
            "defect_definition": "invalid event",
            "metric": "defects per event",
            "baseline": None,
            "target": 0,
        },
        "next_verifiable_step": "Run the validator again.",
        "event_hash_sha256": None,
    }


def write_ledger(directory: str, *events: dict) -> Path:
    ledger = Path(directory) / "ledger.jsonl"
    ledger.write_text(
        "".join(json.dumps(event) + "\n" for event in events),
        encoding="utf-8",
    )
    return ledger


class CustodyValidatorTests(unittest.TestCase):
    def test_valid_event_has_no_defects(self) -> None:
        errors = validator.validate_event(base_event(), 1, set())
        self.assertEqual(errors, [])

    def test_token_vazio_blocks_claim(self) -> None:
        event = base_event()
        event["epistemic_state"] = "TOKEN_VAZIO"
        event["operation"] = "TOKEN_VAZIO"
        event["claim_allowed"] = True
        errors = validator.validate_event(event, 1, set())
        self.assertTrue(any("claim_allowed=false" in item for item in errors))

    def test_token_vazio_state_and_operation_must_agree(self) -> None:
        event = base_event()
        event["operation"] = "TOKEN_VAZIO"
        errors = validator.validate_event(event, 1, set())
        self.assertTrue(
            any("requires epistemic_state TOKEN_VAZIO" in item for item in errors)
        )

    def test_claim_requires_evidence(self) -> None:
        event = base_event()
        event["evidence"] = []
        errors = validator.validate_event(event, 1, set())
        self.assertTrue(any("requires evidence" in item for item in errors))

    def test_evidence_shape_is_validated(self) -> None:
        event = base_event()
        event["evidence"] = [{"kind": "unknown", "reference": ""}]
        errors = validator.validate_event(event, 1, set())
        self.assertTrue(any("kind is invalid" in item for item in errors))
        self.assertTrue(any("reference must be non-empty" in item for item in errors))

    def test_path_traversal_is_rejected(self) -> None:
        event = base_event()
        event["object"]["path"] = "../secret.txt"
        errors = validator.validate_event(event, 1, set())
        self.assertTrue(
            any("safe and repository-relative" in item for item in errors)
        )

    def test_windows_path_escape_is_rejected(self) -> None:
        event = base_event()
        event["object"]["path"] = r"..\secret.txt"
        errors = validator.validate_event(event, 1, set())
        self.assertTrue(
            any("safe and repository-relative" in item for item in errors)
        )

    def test_non_utc_timestamp_is_rejected(self) -> None:
        event = base_event()
        event["timestamp_utc"] = "2026-07-21T09:27:34-03:00"
        errors = validator.validate_event(event, 1, set())
        self.assertTrue(any("ending in Z" in item for item in errors))

    def test_event_id_timestamp_must_match_timestamp(self) -> None:
        event = base_event()
        event["timestamp_utc"] = "2026-07-21T12:27:35Z"
        errors = validator.validate_event(event, 1, set())
        self.assertTrue(any("timestamp must match" in item for item in errors))

    def test_broken_previous_event_is_rejected(self) -> None:
        event = base_event()
        event["previous_event_id"] = "COC-20260721T120000Z-MISSING"
        errors = validator.validate_event(event, 2, set())
        self.assertTrue(any("earlier event" in item for item in errors))

    def test_declared_event_hash_is_verified(self) -> None:
        event = base_event()
        event["event_hash_sha256"] = validator.canonical_event_hash(event)
        errors = validator.validate_event(event, 1, set())
        self.assertEqual(errors, [])

    def test_correction_requires_explicit_superseded_event(self) -> None:
        first = base_event()
        correction = base_event()
        correction["event_id"] = "COC-20260721T122735Z-CORRECTION"
        correction["timestamp_utc"] = "2026-07-21T12:27:35Z"
        correction["previous_event_id"] = first["event_id"]
        correction["operation"] = "CORRECT"
        errors = validator.validate_event(
            correction,
            2,
            {first["event_id"]},
        )
        self.assertTrue(any("supersedes_event_id" in item for item in errors))

    def test_ledger_accepts_ordered_chain(self) -> None:
        first = base_event()
        second = base_event()
        second["event_id"] = "COC-20260721T122735Z-TEST_EVENT_2"
        second["timestamp_utc"] = "2026-07-21T12:27:35Z"
        second["previous_event_id"] = first["event_id"]

        with tempfile.TemporaryDirectory() as directory:
            ledger = write_ledger(directory, first, second)
            count, errors = validator.validate_ledger(ledger)

        self.assertEqual(count, 2)
        self.assertEqual(errors, [])

    def test_ledger_rejects_non_immediate_predecessor(self) -> None:
        first = base_event()
        second = base_event()
        second["event_id"] = "COC-20260721T122735Z-TEST_EVENT_2"
        second["timestamp_utc"] = "2026-07-21T12:27:35Z"
        second["previous_event_id"] = first["event_id"]
        third = base_event()
        third["event_id"] = "COC-20260721T122736Z-TEST_EVENT_3"
        third["timestamp_utc"] = "2026-07-21T12:27:36Z"
        third["previous_event_id"] = first["event_id"]

        with tempfile.TemporaryDirectory() as directory:
            ledger = write_ledger(directory, first, second, third)
            _, errors = validator.validate_ledger(ledger)

        self.assertTrue(any("immediately preceding" in item for item in errors))

    def test_invalid_event_does_not_become_chain_anchor(self) -> None:
        invalid = base_event()
        invalid["evidence"] = []
        second = base_event()
        second["event_id"] = "COC-20260721T122735Z-TEST_EVENT_2"
        second["timestamp_utc"] = "2026-07-21T12:27:35Z"
        second["previous_event_id"] = invalid["event_id"]

        with tempfile.TemporaryDirectory() as directory:
            ledger = write_ledger(directory, invalid, second)
            _, errors = validator.validate_ledger(ledger)

        self.assertTrue(any("earlier event" in item for item in errors))
        self.assertTrue(any("immediately preceding" in item for item in errors))

    def test_object_hash_and_size_can_be_verified(self) -> None:
        event = base_event()
        with tempfile.TemporaryDirectory() as directory:
            repo_root = Path(directory)
            target = repo_root / "indices" / "example.jsonl"
            target.parent.mkdir(parents=True)
            target.write_bytes(b"x")
            event["object"]["sha256"] = hashlib.sha256(b"x").hexdigest()
            ledger = write_ledger(directory, event)
            count, errors = validator.validate_ledger(ledger, repo_root)

        self.assertEqual(count, 1)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
