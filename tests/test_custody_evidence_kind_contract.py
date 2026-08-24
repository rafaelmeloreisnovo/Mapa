#!/usr/bin/env python3
"""Regression contract for custody evidence kinds and the historical ledger."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_chain_of_custody.py"
SCHEMA_PATH = ROOT / "schemas" / "cadeia_custodia_evento.schema.json"
LEDGER_PATH = ROOT / "indices" / "CADEIA_CUSTODIA_EVENTOS.jsonl"

SPEC = importlib.util.spec_from_file_location("custody_validator", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def base_event(kind: str) -> dict:
    return {
        "schema_version": "mapa.custody-event.v1",
        "event_id": "COC-20260824T223000Z-EVIDENCE_KIND_TEST",
        "timestamp_utc": "2026-08-24T22:30:00Z",
        "repository": "rafaelmeloreisnovo/Mapa",
        "branch": "test/custody-evidence-kind",
        "source_ref": "main",
        "previous_event_id": None,
        "actor": {"type": "automation", "id": "unittest"},
        "operation": "VALIDATE",
        "object": {
            "path": "indices/CADEIA_CUSTODIA_EVENTOS.jsonl",
            "media_type": "application/x-ndjson",
            "size_bytes": None,
            "sha256": None,
            "blake3": None,
        },
        "epistemic_state": "FATO",
        "claim_allowed": False,
        "evidence": [{"kind": kind, "reference": "fixture"}],
        "controls": {
            "integrity": "partial",
            "traceability": "verified",
            "reproducibility": "partial",
            "confidentiality": "public",
        },
        "sigma": {
            "phase": "CONTROL",
            "defect_definition": "custody evidence-kind contract drift",
            "metric": "schema-validator parity",
            "baseline": 1,
            "target": 0,
        },
        "next_verifiable_step": "Keep schema and validator evidence-kind sets in parity.",
        "event_hash_sha256": None,
    }


class CustodyEvidenceKindContractTests(unittest.TestCase):
    def test_schema_and_validator_evidence_kinds_are_identical(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        schema_kinds = set(
            schema["properties"]["evidence"]["items"]["properties"]["kind"]["enum"]
        )
        self.assertEqual(schema_kinds, validator.EVIDENCE_KINDS)
        self.assertIn("test", schema_kinds)

    def test_test_evidence_kind_is_accepted(self) -> None:
        errors = validator.validate_event(base_event("test"), 1, set())
        self.assertEqual(errors, [])

    def test_unknown_evidence_kind_remains_rejected(self) -> None:
        errors = validator.validate_event(base_event("unknown"), 1, set())
        self.assertTrue(any("kind is invalid" in error for error in errors))

    def test_historical_ledger_validates_after_contract_alignment(self) -> None:
        count, errors = validator.validate_ledger(LEDGER_PATH)
        self.assertGreater(count, 0)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
