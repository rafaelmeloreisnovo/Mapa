#!/usr/bin/env python3
"""Tests for local versus remote cross-source evidence comparison."""

from __future__ import annotations

import hashlib
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
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_bundle(
    directory: Path,
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
        "schema_version": "rafaelia.cross-source-local-gate/v2",
        "generated_at": f"2026-07-24T00:00:0{environment_marker == 'remote'}Z",
        "platform": environment_marker,
        "status": "PASS",
        "report_count": len(comparator.REPORT_NAMES),
        "checksums": checksums,
        "quality_floor": {
            "path": "indices/CROSS_SOURCE_GATE_FLOOR.json",
            "schema_version": "rafaelia.cross-source-gate-floor/v1",
            "sha256": "a" * 64,
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
        with tempfile.TemporaryDirectory() as root:
            left = Path(root) / "termux"
            right = Path(root) / "actions"
            build_bundle(left, environment_marker="local")
            build_bundle(right, environment_marker="remote")
            report = comparator.compare_bundles(left, right)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["matching_report_count"], 5)
        self.assertTrue(report["quality_floor_sha256_match"])
        self.assertFalse(report["claim_allowed"])

    def test_resealed_content_difference_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            left = Path(root) / "left"
            right = Path(root) / "right"
            build_bundle(left)
            build_bundle(right, changed_report="cross-source-registry-validation.json")
            report = comparator.compare_bundles(left, right)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn(
            "report differs: cross-source-registry-validation.json",
            report["defects"],
        )

    def test_unsealed_tampering_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            left = Path(root) / "left"
            right = Path(root) / "right"
            build_bundle(left)
            build_bundle(right)
            target = right / "quality-floor-validation.json"
            target.write_text(target.read_text(encoding="utf-8") + " ", encoding="utf-8")
            report = comparator.compare_bundles(left, right)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("checksum mismatch" in item for item in report["defects"]))

    def test_claim_promotion_in_manifest_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            left = Path(root) / "left"
            right = Path(root) / "right"
            build_bundle(left)
            build_bundle(right, manifest_overrides={"claim_allowed": True})
            report = comparator.compare_bundles(left, right)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("claim_allowed" in item for item in report["defects"]))

    def test_quality_floor_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            left = Path(root) / "left"
            right = Path(root) / "right"
            build_bundle(left)
            build_bundle(
                right,
                manifest_overrides={
                    "quality_floor": {
                        "path": "indices/CROSS_SOURCE_GATE_FLOOR.json",
                        "schema_version": "rafaelia.cross-source-gate-floor/v1",
                        "sha256": "b" * 64,
                        "status": "PASS",
                    }
                },
            )
            report = comparator.compare_bundles(left, right)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("quality floor sha256 differs or is absent", report["defects"])


if __name__ == "__main__":
    unittest.main()
