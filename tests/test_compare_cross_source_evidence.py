#!/usr/bin/env python3
"""Tests for local versus remote cross-source evidence comparison."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "compare_cross_source_evidence.py"
SPEC = importlib.util.spec_from_file_location("cross_source_evidence_comparator", MODULE_PATH)
assert SPEC and SPEC.loader
comparator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(comparator)

TEST_FILES = [
    "tests/test_compare_cross_source_evidence.py",
    "tests/test_cross_source_gate_evaluator.py",
    "tests/test_cross_source_local_gate_contract.py",
    "tests/test_cross_source_records.py",
    "tests/test_cross_source_registry.py",
    "tests/test_cross_source_test_runner.py",
    "tests/test_validate_chain_of_custody.py",
]


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_floor(root: Path) -> Path:
    path = root / "indices" / "CROSS_SOURCE_GATE_FLOOR.json"
    write_json(
        path,
        {
            "schema_version": "rafaelia.cross-source-gate-floor/v2",
            "minimums": {
                "test_files": 7,
                "tests_discovered": 58,
                "tests_run": 58,
                "valid_fixtures": 2,
                "invalid_fixtures": 1,
                "registry_records": 10,
                "provider_counts": {"github": 2, "google_drive": 8},
                "custody_events": 13,
            },
            "invariants": {
                "unexpected_failures": 0,
                "unexpected_passes": 0,
                "defect_count": 0,
                "complete_execution": True,
                "clean_outcomes": True,
                "skipped": 0,
                "expected_failures": 0,
                "unexpected_successes": 0,
                "claim_allowed": False,
                "remote_ci_substituted": False,
            },
        },
    )
    return path


def build_reports(changed_report: str | None = None) -> dict[str, dict[str, Any]]:
    reports: dict[str, dict[str, Any]] = {
        comparator.TEST_REPORT: {
            "schema_version": "rafaelia.cross-source-test-report/v4",
            "status": "PASS",
            "test_patterns": ["test_cross_source*.py"],
            "test_files": TEST_FILES,
            "test_file_count": 7,
            "tests_discovered": 58,
            "tests_run": 58,
            "complete_execution": True,
            "clean_outcomes": True,
            "failures": 0,
            "errors": 0,
            "skipped": 0,
            "expected_failures": 0,
            "unexpected_successes": 0,
            "claim_allowed": False,
            "remote_ci_substituted": False,
        },
        comparator.RECORD_REPORT: {
            "schema_version": "rafaelia.cross-source-record/v1",
            "status": "PASS",
            "valid_fixture_count": 2,
            "invalid_fixture_count": 1,
            "unexpected_failures": 0,
            "unexpected_passes": 0,
            "claim_allowed": False,
        },
        comparator.REGISTRY_REPORT: {
            "schema_version": "rafaelia.cross-source-registry-report/v1",
            "registry": "indices/CROSS_SOURCE_REGISTRY.jsonl",
            "status": "PASS",
            "record_count": 10,
            "provider_counts": {"github": 2, "google_drive": 8},
            "token_vazio_count": 1,
            "defect_count": 0,
            "defects": [],
            "claim_allowed": False,
        },
        comparator.CUSTODY_REPORT: {
            "schema_version": "rafaelia.custody-validation-report/v1",
            "ledger": "indices/CADEIA_CUSTODIA_EVENTOS.jsonl",
            "status": "PASS",
            "event_count": 14,
            "defect_count": 0,
            "defects": [],
            "claim_allowed": False,
        },
        comparator.QUALITY_REPORT: {
            "schema_version": "rafaelia.cross-source-gate-evaluation/v3",
            "status": "PASS",
            "floor_schema_version": "rafaelia.cross-source-gate-floor/v2",
            "comparison": "observed_greater_than_or_equal_to_minimum",
            "check_count": 1,
            "failed_check_count": 0,
            "checks": [
                {
                    "name": "fixture",
                    "observed": 1,
                    "operator": "eq",
                    "required": 1,
                    "passed": True,
                }
            ],
            "promotion_state": "LOCAL_PASS_REMOTE_TOKEN_VAZIO",
            "claim_allowed": False,
            "remote_ci_substituted": False,
        },
    }
    if changed_report:
        reports[changed_report]["payload"] = "changed"
    return reports


def reseal_bundle(directory: Path) -> None:
    checksums = []
    for name in comparator.REPORT_NAMES:
        path = directory / name
        checksums.append({"path": name, "sha256": comparator.sha256_file(path)})
    (directory / comparator.CHECKSUMS_NAME).write_text(
        "".join(f"{item['sha256']}  {item['path']}\n" for item in checksums),
        encoding="utf-8",
    )
    manifest_path = directory / comparator.MANIFEST_NAME
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["checksums"] = checksums
    write_json(manifest_path, manifest)


def build_bundle(
    directory: Path,
    floor_path: Path,
    *,
    changed_report: str | None = None,
    manifest_overrides: dict[str, Any] | None = None,
    environment_marker: str = "local",
) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for name, report in build_reports(changed_report).items():
        write_json(directory / name, report)

    manifest = {
        "schema_version": "rafaelia.cross-source-local-gate/v3",
        "generated_at": f"2026-07-24T00:00:0{environment_marker == 'remote'}Z",
        "platform": environment_marker,
        "status": "PASS",
        "test_file_count": 7,
        "minimum_test_file_count": 7,
        "test_count_discovered": 58,
        "test_count_observed": 58,
        "minimum_test_count": 58,
        "complete_test_execution": True,
        "clean_test_outcomes": True,
        "report_count": len(comparator.REPORT_NAMES),
        "checksums": [],
        "quality_floor": {
            "path": "indices/CROSS_SOURCE_GATE_FLOOR.json",
            "schema_version": "rafaelia.cross-source-gate-floor/v2",
            "sha256": comparator.sha256_file(floor_path),
            "status": "PASS",
        },
        "quality_floor_status": "PASS",
        "promotion_state": "LOCAL_PASS_REMOTE_TOKEN_VAZIO",
        "claim_allowed": False,
        "remote_ci_substituted": False,
    }
    if manifest_overrides:
        manifest.update(manifest_overrides)
    write_json(directory / comparator.MANIFEST_NAME, manifest)
    reseal_bundle(directory)


class CrossSourceEvidenceComparatorTests(unittest.TestCase):
    def test_identical_reports_pass_despite_environment_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as root_text:
            root = Path(root_text)
            floor = build_floor(root)
            left = root / "termux"
            right = root / "actions"
            build_bundle(left, floor, environment_marker="local")
            build_bundle(right, floor, environment_marker="remote")
            report = comparator.compare_bundles(left, right, floor)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["matching_report_count"], 5)
        self.assertTrue(report["quality_floor_sha256_match"])
        self.assertFalse(report["claim_allowed"])

    def test_resealed_content_difference_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as root_text:
            root = Path(root_text)
            floor = build_floor(root)
            left = root / "left"
            right = root / "right"
            build_bundle(left, floor)
            build_bundle(right, floor, changed_report=comparator.REGISTRY_REPORT)
            report = comparator.compare_bundles(left, right, floor)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn(
            f"report differs or is absent: {comparator.REGISTRY_REPORT}",
            report["defects"],
        )

    def test_equal_absence_never_counts_as_a_hash_match(self) -> None:
        missing = comparator.RECORD_REPORT
        with tempfile.TemporaryDirectory() as root_text:
            root = Path(root_text)
            floor = build_floor(root)
            left = root / "left"
            right = root / "right"
            build_bundle(left, floor)
            build_bundle(right, floor)
            (left / missing).unlink()
            (right / missing).unlink()
            report = comparator.compare_bundles(left, right, floor)
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["report_hash_matches"][missing])
        self.assertEqual(report["matching_report_count"], 4)

    def test_unsealed_tampering_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as root_text:
            root = Path(root_text)
            floor = build_floor(root)
            left = root / "left"
            right = root / "right"
            build_bundle(left, floor)
            build_bundle(right, floor)
            target = right / comparator.QUALITY_REPORT
            target.write_text(target.read_text(encoding="utf-8") + " ", encoding="utf-8")
            report = comparator.compare_bundles(left, right, floor)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("checksum mismatch" in item for item in report["defects"]))

    def test_claim_promotion_in_manifest_is_rejected(self) -> None:
        overrides = (
            {"claim_allowed": True},
            {"complete_test_execution": False},
            {"clean_test_outcomes": False},
            {"test_count_observed": 57},
            {"test_file_count": 6},
        )
        for override in overrides:
            with self.subTest(override=override):
                with tempfile.TemporaryDirectory() as root_text:
                    root = Path(root_text)
                    floor = build_floor(root)
                    left = root / "left"
                    right = root / "right"
                    build_bundle(left, floor)
                    build_bundle(right, floor, manifest_overrides=override)
                    report = comparator.compare_bundles(left, right, floor)
                self.assertEqual(report["status"], "FAIL")

        with self.subTest(case="identically_resealed_semantic_forgery"):
            with tempfile.TemporaryDirectory() as root_text:
                root = Path(root_text)
                floor = build_floor(root)
                left = root / "left"
                right = root / "right"
                build_bundle(left, floor)
                build_bundle(right, floor)
                for directory in (left, right):
                    path = directory / comparator.TEST_REPORT
                    tests = json.loads(path.read_text(encoding="utf-8"))
                    tests["tests_discovered"] = 57
                    tests["tests_run"] = 57
                    write_json(path, tests)
                    reseal_bundle(directory)
                report = comparator.compare_bundles(left, right, floor)
            self.assertEqual(report["matching_report_count"], 5)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(
                any("versus test report" in defect for defect in report["defects"])
            )

    def test_quality_floor_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as root_text:
            root = Path(root_text)
            floor = build_floor(root)
            left = root / "left"
            right = root / "right"
            build_bundle(left, floor)
            build_bundle(right, floor)
            changed_floor = json.loads(floor.read_text(encoding="utf-8"))
            changed_floor["minimums"]["tests_run"] = 59
            write_json(floor, changed_floor)
            report = comparator.compare_bundles(left, right, floor)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(
            any("quality_floor.sha256" in item for item in report["defects"])
        )


if __name__ == "__main__":
    unittest.main()
