#!/usr/bin/env python3
"""Validate and compare sealed RAFAELIA cross-source evidence bundles."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

TEST_REPORT = "cross-source-test-validation.json"
RECORD_REPORT = "cross-source-record-validation.json"
REGISTRY_REPORT = "cross-source-registry-validation.json"
CUSTODY_REPORT = "chain-of-custody-validation.json"
QUALITY_REPORT = "quality-floor-validation.json"
REPORT_NAMES = [TEST_REPORT, RECORD_REPORT, REGISTRY_REPORT, CUSTODY_REPORT, QUALITY_REPORT]
CHECKSUMS_NAME = "CHECKSUMS.sha256"
MANIFEST_NAME = "LOCAL_GATE_STATUS.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: JSON root must be an object")
    return value


def _manifest_checksums(manifest: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in manifest.get("checksums", []):
        if isinstance(item, dict) and isinstance(item.get("path"), str) and isinstance(item.get("sha256"), str):
            result[item["path"]] = item["sha256"]
    return result


def _checksums_file(directory: Path) -> dict[str, str]:
    path = directory / CHECKSUMS_NAME
    result: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        digest, separator, name = raw.partition("  ")
        if not separator or not digest or not name:
            raise ValueError(f"{path}: malformed checksum line")
        result[name] = digest
    return result


def validate_report_semantics(directory: Path, manifest: dict[str, Any]) -> list[str]:
    defects: list[str] = []
    try:
        test_report = _load_json(directory / TEST_REPORT)
        registry_report = _load_json(directory / REGISTRY_REPORT)
        custody_report = _load_json(directory / CUSTODY_REPORT)
        quality_report = _load_json(directory / QUALITY_REPORT)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"report semantic read failed: {exc}"]

    if manifest.get("test_count_observed") != test_report.get("tests_run"):
        defects.append("manifest test_count_observed versus test report tests_run mismatch")
    if manifest.get("test_count_discovered") != test_report.get("tests_discovered"):
        defects.append("manifest test_count_discovered versus test report tests_discovered mismatch")
    if manifest.get("test_file_count") != test_report.get("test_file_count"):
        defects.append("manifest test_file_count versus test report test_file_count mismatch")
    if manifest.get("complete_test_execution") is not True or test_report.get("complete_execution") is not True:
        defects.append("complete test execution must be true in manifest and test report")
    if manifest.get("clean_test_outcomes") is not True or test_report.get("clean_outcomes") is not True:
        defects.append("clean test outcomes must be true in manifest and test report")
    if manifest.get("claim_allowed") is not False or test_report.get("claim_allowed") is not False:
        defects.append("claim_allowed must remain false")
    if manifest.get("remote_ci_substituted") is not False or test_report.get("remote_ci_substituted") is not False:
        defects.append("remote_ci_substituted must remain false")

    if not registry_report.get("registry"):
        defects.append("registry report registry path missing")
    if registry_report.get("status") != "PASS" or registry_report.get("defect_count") != 0:
        defects.append("registry report must be PASS with zero defects")
    if custody_report.get("status") != "PASS" or custody_report.get("defect_count") != 0:
        defects.append("custody report must be PASS with zero defects")
    if quality_report.get("status") != "PASS" or quality_report.get("failed_check_count") != 0:
        defects.append("quality report must be PASS with zero failed checks")
    for check in quality_report.get("checks", []):
        if not isinstance(check, dict) or check.get("passed") is not True:
            defects.append("quality report requires every check.passed=true")
            break
    if quality_report.get("claim_allowed") is not False:
        defects.append("quality report claim_allowed must be false")
    return defects


def validate_quality_floor(directory: Path, floor_path: Path, manifest: dict[str, Any]) -> list[str]:
    defects: list[str] = []
    try:
        floor = _load_json(floor_path)
        registry = _load_json(directory / REGISTRY_REPORT)
        custody = _load_json(directory / CUSTODY_REPORT)
        tests = _load_json(directory / TEST_REPORT)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"quality floor validation read failed: {exc}"]

    quality_floor = manifest.get("quality_floor", {})
    actual_floor_hash = sha256_file(floor_path)
    if not isinstance(quality_floor, dict) or quality_floor.get("sha256") != actual_floor_hash:
        defects.append("quality floor sha256 differs or is absent; manifest quality_floor.sha256 must bind the exact floor")

    minimums = floor.get("minimums", {})
    if tests.get("test_file_count", -1) < minimums.get("test_files", 0):
        defects.append("test_file_count below quality floor")
    if tests.get("tests_discovered", -1) < minimums.get("tests_discovered", 0):
        defects.append("tests_discovered below quality floor")
    if tests.get("tests_run", -1) < minimums.get("tests_run", 0):
        defects.append("tests_run below quality floor")
    if registry.get("record_count", -1) < minimums.get("registry_records", 0):
        defects.append("registry_records below quality floor")
    for provider, required in minimums.get("provider_counts", {}).items():
        if registry.get("provider_counts", {}).get(provider, 0) < required:
            defects.append(f"provider {provider} below quality floor")
    if custody.get("event_count", -1) < minimums.get("custody_events", 0):
        defects.append("custody_events below quality floor")
    return defects


def validate_bundle(directory: Path, floor_path: Path | None = None) -> dict[str, Any]:
    """Validate one bundle exactly as produced by run_cross_source_gate.sh."""
    report: dict[str, Any] = {
        "schema_version": "rafaelia.cross-source-bundle-validation/v1",
        "status": "PASS",
        "defects": [],
        "claim_allowed": False,
    }
    defects: list[str] = report["defects"]
    if not directory.is_dir():
        defects.append(f"bundle directory does not exist: {directory}")
        report["status"] = "FAIL"
        return report

    required = [MANIFEST_NAME, CHECKSUMS_NAME, *REPORT_NAMES]
    for name in required:
        if not (directory / name).is_file():
            defects.append(f"required bundle file missing: {name}")
    if defects:
        report["status"] = "FAIL"
        return report

    try:
        manifest = _load_json(directory / MANIFEST_NAME)
        for name in REPORT_NAMES:
            _load_json(directory / name)
        manifest_checksums = _manifest_checksums(manifest)
        file_checksums = _checksums_file(directory)
    except (OSError, ValueError, json.JSONDecodeError, KeyError) as exc:
        defects.append(f"bundle parse failure: {exc}")
        report["status"] = "FAIL"
        return report

    if manifest.get("schema_version") != "rafaelia.cross-source-local-gate/v3":
        defects.append("unexpected local gate manifest schema")
    if manifest.get("status") != "PASS":
        defects.append("local gate manifest status must be PASS")
    if manifest.get("report_count") != len(REPORT_NAMES):
        defects.append("local gate manifest report_count mismatch")
    if manifest.get("claim_allowed") is not False:
        defects.append("local gate manifest claim_allowed must be false")

    for name in REPORT_NAMES:
        actual = sha256_file(directory / name)
        if manifest_checksums.get(name) != actual:
            defects.append(f"checksum mismatch for {name} in manifest")
        if file_checksums.get(name) != actual:
            defects.append(f"checksum mismatch for {name} in {CHECKSUMS_NAME}")

    defects.extend(validate_report_semantics(directory, manifest))
    if floor_path is not None:
        defects.extend(validate_quality_floor(directory, floor_path, manifest))

    if defects:
        report["status"] = "FAIL"
    report["report_count"] = len(REPORT_NAMES)
    return report


def _normalized_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in manifest.items() if key not in {"generated_at", "platform"}}


def compare_bundles(left_bundle: Path, right_bundle: Path, floor_path: Path) -> dict[str, Any]:
    report: dict[str, Any] = {
        "schema_version": "rafaelia.cross-source-evidence-comparison/v4",
        "status": "PASS",
        "matching_report_count": 0,
        "report_hash_matches": {},
        "quality_floor_sha256_match": False,
        "clean_test_outcomes": True,
        "claim_allowed": False,
        "remote_ci_substituted": False,
        "defects": [],
    }
    defects: list[str] = report["defects"]

    left_validation = validate_bundle(left_bundle, floor_path)
    right_validation = validate_bundle(right_bundle, floor_path)
    if left_validation["status"] != "PASS":
        defects.extend(f"left: {item}" for item in left_validation["defects"])
    if right_validation["status"] != "PASS":
        defects.extend(f"right: {item}" for item in right_validation["defects"])

    if defects:
        report["status"] = "FAIL"

    for name in REPORT_NAMES:
        left_path = left_bundle / name
        right_path = right_bundle / name
        match = left_path.is_file() and right_path.is_file() and sha256_file(left_path) == sha256_file(right_path)
        report["report_hash_matches"][name] = match
        if match:
            report["matching_report_count"] += 1
        else:
            defects.append(f"report differs or is absent: {name}")
            report["status"] = "FAIL"

    try:
        left_manifest = _load_json(left_bundle / MANIFEST_NAME)
        right_manifest = _load_json(right_bundle / MANIFEST_NAME)
        floor_hash = sha256_file(floor_path)
        left_floor_hash = left_manifest.get("quality_floor", {}).get("sha256")
        right_floor_hash = right_manifest.get("quality_floor", {}).get("sha256")
        report["quality_floor_sha256_match"] = left_floor_hash == floor_hash == right_floor_hash
        if not report["quality_floor_sha256_match"]:
            defects.append("manifest quality_floor.sha256 differs or is absent")
            report["status"] = "FAIL"
        if _normalized_manifest(left_manifest) != _normalized_manifest(right_manifest):
            defects.append("manifest semantic mismatch between bundles")
            report["status"] = "FAIL"
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        defects.append(f"manifest comparison failed: {exc}")
        report["status"] = "FAIL"

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--left-bundle", type=Path, required=True)
    parser.add_argument("--right-bundle", type=Path, required=True)
    parser.add_argument("--floor", type=Path, required=True)
    args = parser.parse_args()
    report = compare_bundles(args.left_bundle, args.right_bundle, args.floor)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
