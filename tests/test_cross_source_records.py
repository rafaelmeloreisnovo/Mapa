#!/usr/bin/env python3
"""Adversarial tests for the cross-source record validator."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_cross_source_records.py"
SPEC = importlib.util.spec_from_file_location("cross_source_validator", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)

VALID_GITHUB = (
    ROOT
    / "tests"
    / "fixtures"
    / "cross_source"
    / "valid"
    / "github_architecture_record.json"
)
VALID_DRIVE_TOKEN = (
    ROOT
    / "tests"
    / "fixtures"
    / "cross_source"
    / "valid"
    / "google_drive_token_vazio_record.json"
)
INVALID_TOKEN_CLAIM = (
    ROOT
    / "tests"
    / "fixtures"
    / "cross_source"
    / "invalid"
    / "token_vazio_claim_allowed_true.json"
)
VALID_DIRECTIVE = (
    ROOT
    / "tests"
    / "fixtures"
    / "cross_source"
    / "valid"
    / "session_directive_record.json"
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class CrossSourceRecordTests(unittest.TestCase):
    def test_valid_github_fixture_passes(self) -> None:
        self.assertEqual(validator.validate_record(load(VALID_GITHUB)), [])

    def test_valid_drive_token_vazio_fixture_passes(self) -> None:
        self.assertEqual(validator.validate_record(load(VALID_DRIVE_TOKEN)), [])

    def test_valid_session_directive_fixture_passes(self) -> None:
        self.assertEqual(validator.validate_record(load(VALID_DIRECTIVE)), [])

    def test_token_vazio_cannot_allow_claim(self) -> None:
        errors = validator.validate_record(load(INVALID_TOKEN_CLAIM))
        self.assertTrue(
            any(
                "TOKEN_VAZIO requires classification.claim_allowed=false" in item
                for item in errors
            )
        )

    def test_provider_specific_fields_are_exclusive(self) -> None:
        record = load(VALID_GITHUB)
        record["source"]["drive_file_id"] = "leaked-drive-id"
        errors = validator.validate_record(record)
        self.assertTrue(any("drive_file_id must be null" in item for item in errors))

    def test_claim_requires_demonstration_and_evidence(self) -> None:
        record = load(VALID_DRIVE_TOKEN)
        record["classification"] = {
            "domain": "fixture.cross_source",
            "epistemic_state": "HIPOTESE",
            "evidence_mode": "HIPOTESE",
            "claim_allowed": True,
            "sensitivity": "PRIVATE",
        }
        errors = validator.validate_record(record)
        self.assertTrue(any("FATO or VERIFIED_LIMITED" in item for item in errors))
        self.assertTrue(any("evidence_mode DEMONSTRACAO" in item for item in errors))
        self.assertTrue(any("requires at least one evidence_ref" in item for item in errors))

    def test_relation_evidence_must_resolve(self) -> None:
        record = load(VALID_DRIVE_TOKEN)
        record["relations"][0]["evidence_id"] = "ev:missing.local"
        errors = validator.validate_record(record)
        self.assertTrue(any("must resolve locally" in item for item in errors))

    def test_q16_weight_is_bounded(self) -> None:
        record = load(VALID_DRIVE_TOKEN)
        record["relations"][0]["weight_q16"] = 65536
        errors = validator.validate_record(record)
        self.assertTrue(any("0 to 65535" in item for item in errors))

    def test_termux_parent_traversal_is_rejected(self) -> None:
        record = load(VALID_DRIVE_TOKEN)
        record["source"] = {
            "provider": "termux",
            "account_scope": "fixture",
            "locator": "termux:../secret",
            "url": None,
            "observed_at": "2026-07-23T08:30:00Z",
            "repository_full_name": None,
            "path": None,
            "drive_file_id": None,
            "termux_path": "../secret",
            "session_id": None,
        }
        errors = validator.validate_record(record)
        self.assertTrue(any("parent traversal" in item for item in errors))

    def test_fixture_sets_have_expected_polarity(self) -> None:
        report = validator.validate_fixture_sets(
            VALID_GITHUB.parent.glob("*.json"),
            INVALID_TOKEN_CLAIM.parent.glob("*.json"),
        )
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["unexpected_failures"], 0)
        self.assertEqual(report["unexpected_passes"], 0)
        self.assertFalse(report["claim_allowed"])


if __name__ == "__main__":
    unittest.main()
