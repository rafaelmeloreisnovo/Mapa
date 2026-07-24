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
            },
            "invariants": {
                "complete_execution": True,
                "claim_allowed": False,
                "remote_ci_substituted": False,
            },
        },
    )
    return path


def build_bundle(
    directory: Path,
    floor_path: Path,
    *,
    changed_report: str | None = None,
    manifest_overrides: dict[str, Any] | None = None,
    environment_marker: str = "local",
) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    checksums = []
    for index, name in enumerate(comparator.REPORT_NAMES):
        report = {
            "schema_version": f"fixture/{index}",
            "status": "PASS",
            "payload": "changed" if name == changed_report else "stable",
            "claim_allowed": False,
        }
        path = directory / name
        write_json(path, report)
        checksums.append({"path": name, "sha256": comparator.sha256_file(path)})

    (directory / comparator.CHECKSUMS_NAME).write_text(
        "".join(f"{item['sha256']}  {item['path']}\n" for item in checksums),
        encoding="utf-8",
    )
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
        "report_count": len(comparator.REPORT_NAMES),
        "checksums": checksums,
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
            build_bundle(right, floor, changed_report="cross-source-registry-validation.json")
            report = comparator.compare_bundles(left, right, floor)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn(
            "report differs or is absent: cross-source-registry-validation.json",
            report["defects"],
        )

    def test_equal_absence_never_counts_as_a_hash_match(self) -> None:
        missing = "cross-source-record-validation.json"
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
            target = right / "quality-floor-validation.json"
            target.write_text(target.read_text(encoding="utf-8") + " ", encoding="utf-8")
            report = comparator.compare_bundles(left, right, floor)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("checksum mismatch" in item for item in report["defects"]))

    def test_claim_promotion_in_manifest_is_rejected(self) -> None:
        overrides = (
            {"claim_allowed": True},
            {"complete_test_execution": False},
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
            any("quality_floor.sha256 differs" in item for item in report["defects"])
        )


if __name__ == "__main__":
    unittest.main()
