#!/usr/bin/env python3
"""Regression tests for the chain-of-custody semantic validator."""

from __future__ import annotations

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
        "evidence": [{"kind": "file", "reference": "indices/example.jsonl"}],
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

    def test_claim_requires_evidence(self) -> None:
        event = base_event()
        event["evidence"] = []
        errors = validator.validate_event(event, 1, set())
        self.assertTrue(any("requires evidence" in item for item in errors))

    def test_path_traversal_is_rejected(self) -> None:
        event = base_event()
        event["object"]["path"] = "../secret.txt"
        errors = validator.validate_event(event, 1, set())
        self.assertTrue(any("safe and repository-relative" in item for item in errors))

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

    def test_ledger_accepts_ordered_chain(self) -> None:
        first = base_event()
        second = base_event()
        second["event_id"] = "COC-20260721T122735Z-TEST_EVENT_2"
        second["previous_event_id"] = first["event_id"]

        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "ledger.jsonl"
            ledger.write_text(
                json.dumps(first) + "\n" + json.dumps(second) + "\n",
                encoding="utf-8",
            )
            count, errors = validator.validate_ledger(ledger)

        self.assertEqual(count, 2)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
