#!/usr/bin/env python3
"""Adversarial tests for the append-only cross-source registry."""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_cross_source_registry.py"
SPEC = importlib.util.spec_from_file_location("cross_source_registry_validator", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)

REGISTRY = ROOT / "indices" / "CROSS_SOURCE_REGISTRY.jsonl"


def load_registry() -> list[dict]:
    records, errors = validator.load_jsonl(REGISTRY)
    if errors:
        raise AssertionError(errors)
    return records


def write_registry(directory: str, records: list[dict]) -> Path:
    path = Path(directory) / "registry.jsonl"
    path.write_text(
        "".join(
            json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
            for record in records
        ),
        encoding="utf-8",
    )
    return path


class CrossSourceRegistryTests(unittest.TestCase):
    def test_canonical_registry_passes(self) -> None:
        report = validator.build_report(REGISTRY)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["record_count"], 12)
        self.assertEqual(
            report["provider_counts"],
            {"github": 3, "google_drive": 8, "session": 1},
        )
        self.assertEqual(report["token_vazio_count"], 1)
        self.assertEqual(report["registry"], "indices/CROSS_SOURCE_REGISTRY.jsonl")
        self.assertFalse(report["claim_allowed"])

    def test_reports_are_identical_across_external_checkout_paths(self) -> None:
        records = load_registry()
        with tempfile.TemporaryDirectory() as left_directory:
            with tempfile.TemporaryDirectory() as right_directory:
                left = validator.build_report(write_registry(left_directory, records))
                right = validator.build_report(write_registry(right_directory, records))
        self.assertEqual(left, right)
        self.assertEqual(left["registry"], "external://registry.jsonl")

    def test_missing_external_path_does_not_leak_host_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.jsonl"
            report = validator.build_report(path)
        rendered = json.dumps(report, sort_keys=True)
        self.assertEqual(report["registry"], "external://missing.jsonl")
        self.assertNotIn(directory, rendered)

    def test_duplicate_record_id_is_rejected(self) -> None:
        records = load_registry()
        duplicate = copy.deepcopy(records[0])
        duplicate["custody"]["event_id"] = "evt:duplicate.record-id.test"
        records.append(duplicate)
        errors = validator.validate_registry_records(records)
        self.assertTrue(any("duplicate record_id" in item for item in errors))

    def test_dangling_relation_target_is_rejected(self) -> None:
        records = load_registry()
        records[0]["relations"][0]["target_id"] = "rec:missing.cross-source-record"
        errors = validator.validate_registry_records(records)
        self.assertTrue(any("dangling target_id" in item for item in errors))

    def test_duplicate_custody_event_is_rejected(self) -> None:
        records = load_registry()
        records[1]["custody"]["event_id"] = records[0]["custody"]["event_id"]
        errors = validator.validate_registry_records(records)
        self.assertTrue(any("duplicate custody event_id" in item for item in errors))

    def test_duplicate_drive_file_id_is_rejected(self) -> None:
        records = load_registry()
        records[4]["source"]["drive_file_id"] = records[3]["source"]["drive_file_id"]
        errors = validator.validate_registry_records(records)
        self.assertTrue(any("duplicate Drive file ID" in item for item in errors))

    def test_token_vazio_never_authorizes_deletion(self) -> None:
        records = load_registry()
        duplicate_root = next(
            record
            for record in records
            if record["record_id"] == "rec:drive.omega-nav-root-duplicate"
        )
        duplicate_root["metadata"]["deletion_allowed"] = True
        errors = validator.validate_registry_records(records)
        self.assertTrue(any("cannot authorize deletion" in item for item in errors))

    def test_malformed_jsonl_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken.jsonl"
            path.write_text('{"record_id":"ok"}\n{broken\n', encoding="utf-8")
            report = validator.build_report(path)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("invalid JSON" in item for item in report["defects"]))


if __name__ == "__main__":
    unittest.main()
