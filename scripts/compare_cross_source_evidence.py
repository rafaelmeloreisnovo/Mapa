#!/usr/bin/env python3
"""
compare_cross_source_evidence.py

Compare cross-source evidence bundles locally and validate against quality floor.
Validates reports, checksums, manifests and bundle integrity.

Execution: python3 compare_cross_source_evidence.py [--local-bundle PATH] [--floor PATH]
Exit code: 0 = PASS, 1 = FAIL
"""

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

# Report names and constants
TEST_REPORT = "cross-source-test-report.json"
RECORD_REPORT = "cross-source-record-report.json"
REGISTRY_REPORT = "cross-source-registry-report.json"
CUSTODY_REPORT = "custody-validation-report.json"
QUALITY_REPORT = "cross-source-gate-evaluation.json"

REPORT_NAMES = [
    TEST_REPORT,
    RECORD_REPORT,
    REGISTRY_REPORT,
    CUSTODY_REPORT,
    QUALITY_REPORT,
]

CHECKSUMS_NAME = "CHECKSUMS.sha256"
MANIFEST_NAME = "cross-source-local-gate-manifest.json"


def sha256_file(path: Path) -> str:
    """Compute SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


def validate_bundle(directory: Path) -> bool:
    """Validate bundle structure and report integrity."""
    if not directory.exists():
        print(f"ERROR: bundle directory does not exist: {directory}")
        return False

    # Check manifest exists
    manifest_path = directory / MANIFEST_NAME
    if not manifest_path.exists():
        print(f"ERROR: manifest not found: {manifest_path}")
        return False

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, IOError) as e:
        print(f"ERROR: failed to read manifest: {e}")
        return False

    # Check all reports exist
    for report_name in REPORT_NAMES:
        report_path = directory / report_name
        if not report_path.exists():
            print(f"ERROR: report not found: {report_path}")
            return False

        # Validate report is valid JSON
        try:
            json.loads(report_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError) as e:
            print(f"ERROR: failed to read report {report_name}: {e}")
            return False

    # Check checksums file exists
    checksums_path = directory / CHECKSUMS_NAME
    if not checksums_path.exists():
        print(f"ERROR: checksums file not found: {checksums_path}")
        return False

    # Validate checksums
    expected_checksums = {}
    for item in manifest.get("checksums", []):
        expected_checksums[item["path"]] = item["sha256"]

    for report_name in REPORT_NAMES:
        report_path = directory / report_name
        actual_hash = sha256_file(report_path)
        expected_hash = expected_checksums.get(report_name)

        if not expected_hash:
            print(f"ERROR: checksum mismatch - no entry for {report_name}")
            return False

        if actual_hash != expected_hash:
            print(f"ERROR: checksum mismatch for {report_name}")
            print(f"  expected: {expected_hash}")
            print(f"  actual:   {actual_hash}")
            return False

    print(f"✓ Bundle validation passed")
    return True


def validate_report_semantics(directory: Path, manifest: dict[str, Any]) -> bool:
    """Validate semantic consistency between reports."""
    # Validate test report
    test_report_path = directory / TEST_REPORT
    try:
        test_report = json.loads(test_report_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, IOError) as e:
        print(f"ERROR: failed to read test report: {e}")
        return False

    manifest_test_count = manifest.get("test_count_observed")
    report_test_count = test_report.get("tests_run")

    if manifest_test_count != report_test_count:
        print(f"ERROR: manifest test_count_observed versus test report tests_run mismatch")
        print(f"  manifest: {manifest_test_count}")
        print(f"  report:   {report_test_count}")
        return False

    # Validate registry report
    registry_report_path = directory / REGISTRY_REPORT
    try:
        registry_report = json.loads(registry_report_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, IOError) as e:
        print(f"ERROR: failed to read registry report: {e}")
        return False

    registry_path = registry_report.get("registry")
    if not registry_path:
        print(f"ERROR: registry report missing registry path")
        return False

    # Validate quality report
    quality_report_path = directory / QUALITY_REPORT
    try:
        quality_report = json.loads(quality_report_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, IOError) as e:
        print(f"ERROR: failed to read quality report: {e}")
        return False

    checks = quality_report.get("checks", [])
    for check in checks:
        if not check.get("passed", False):
            print(f"ERROR: quality report requires every check.passed=true")
            return False

    print(f"✓ Report semantics validated")
    return True


def validate_quality_floor(directory: Path, floor_path: Path, manifest: dict[str, Any]) -> bool:
    """Validate bundle against quality floor."""
    if not floor_path.exists():
        print(f"ERROR: quality floor not found: {floor_path}")
        return False

    try:
        floor = json.loads(floor_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, IOError) as e:
        print(f"ERROR: failed to read quality floor: {e}")
        return False

    # Check quality floor SHA256
    quality_floor_entry = manifest.get("quality_floor", {})
    expected_floor_hash = quality_floor_entry.get("sha256")
    actual_floor_hash = sha256_file(floor_path)

    if expected_floor_hash != actual_floor_hash:
        print(f"ERROR: quality floor sha256 differs or is absent")
        print(f"  expected: {expected_floor_hash}")
        print(f"  actual:   {actual_floor_hash}")
        return False

    # Compare manifest minimum against observed
    minimums = floor.get("minimums", {})
    for key, min_value in minimums.items():
        observed_key = key.replace("_", "_", 1)  # Keep consistent naming
        observed_value = manifest.get(observed_key.replace("minimum_", ""))
        if observed_value is not None and observed_value < min_value:
            print(f"ERROR: manifest {observed_key} ({observed_value}) below floor minimum ({min_value})")
            return False

    print(f"✓ Quality floor validation passed")
    return True


def compare_bundles(
    local_bundle: Path,
    floor_path: Path,
) -> bool:
    """Compare local bundle against quality floor."""
    # Validate local bundle
    if not validate_bundle(local_bundle):
        return False

    # Load manifest
    manifest_path = local_bundle / MANIFEST_NAME
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, IOError) as e:
        print(f"ERROR: failed to read manifest: {e}")
        return False

    # Validate report semantics
    if not validate_report_semantics(local_bundle, manifest):
        return False

    # Validate quality floor
    if not validate_quality_floor(local_bundle, floor_path, manifest):
        return False

    return True


def main() -> int:
    """Execute bundle comparison."""
    import argparse

    parser = argparse.ArgumentParser(description="Compare cross-source evidence bundles")
    parser.add_argument(
        "--local-bundle",
        type=Path,
        default=Path(".") / "build" / "cross-source-gate-local",
        help="Path to local bundle directory",
    )
    parser.add_argument(
        "--floor",
        type=Path,
        default=Path(".") / "indices" / "CROSS_SOURCE_GATE_FLOOR.json",
        help="Path to quality floor JSON",
    )

    args = parser.parse_args()

    if not compare_bundles(args.local_bundle, args.floor):
        return 1

    print("\n" + "=" * 60)
    print("✓ CROSS-SOURCE EVIDENCE COMPARISON PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
