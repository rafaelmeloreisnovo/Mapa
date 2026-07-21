#!/usr/bin/env python3
"""Tests for the conservative custody-baseline measurement."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "measure_custody_baseline.py"
SPEC = importlib.util.spec_from_file_location("custody_baseline", MODULE_PATH)
assert SPEC and SPEC.loader
baseline = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(baseline)


def event() -> dict:
    return {
        "schema_version": "mapa.custody-event.v1",
        "event_id": "COC-20260721T122734Z-BASELINE_TEST",
        "timestamp_utc": "2026-07-21T12:27:34Z",
        "repository": "rafaelmeloreisnovo/Mapa",
        "branch": "test/baseline",
        "source_ref": "main",
        "previous_event_id": None,
        "actor": {"type": "automation", "id": "unittest"},
        "operation": "VALIDATE",
        "object": {
            "path": "evidence.txt",
            "media_type": "text/plain",
            "size_bytes": 1,
            "sha256": hashlib.sha256(b"x").hexdigest(),
            "blake3": None,
        },
        "epistemic_state": "FATO",
        "claim_allowed": True,
        "evidence": [{"kind": "file", "reference": "evidence.txt"}],
        "controls": {
            "integrity": "verified",
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
        "next_verifiable_step": "Repeat the measurement.",
        "event_hash_sha256": None,
    }


class BaselineTests(unittest.TestCase):
    def test_valid_pilot_is_measured_without_sigma_claim(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "evidence.txt").write_bytes(b"x")
            ledger = root / "ledger.jsonl"
            ledger.write_text(json.dumps(event()) + "\n", encoding="utf-8")
            report = baseline.measure(
                ledger,
                root,
                measured_at_utc="2026-07-21T12:40:00Z",
            )

        self.assertEqual(report["observed"]["defect_count"], 0)
        self.assertEqual(report["observed"]["integrity"], 1.0)
        self.assertEqual(report["observed"]["dpmo_observed"], 0.0)
        self.assertEqual(report["six_sigma"]["sigma_level"], "TOKEN_VAZIO")
        self.assertTrue(report["claim_allowed"])

    def test_defect_blocks_baseline_claim(self) -> None:
        broken = event()
        broken["evidence"] = []
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "evidence.txt").write_bytes(b"x")
            ledger = root / "ledger.jsonl"
            ledger.write_text(json.dumps(broken) + "\n", encoding="utf-8")
            report = baseline.measure(ledger, root)

        self.assertGreater(report["observed"]["defect_count"], 0)
        self.assertFalse(report["claim_allowed"])

    def test_integrity_remains_token_vazio_without_declared_hashes(self) -> None:
        payload = event()
        payload["object"]["sha256"] = None
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "evidence.txt").write_bytes(b"x")
            ledger = root / "ledger.jsonl"
            ledger.write_text(json.dumps(payload) + "\n", encoding="utf-8")
            report = baseline.measure(ledger, root)

        self.assertEqual(report["observed"]["integrity"], "TOKEN_VAZIO")


if __name__ == "__main__":
    unittest.main()
