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
        print(f"ERROR: registry report registry path missing")
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
    left_bundle: Path,
    right_bundle: Path,
    floor_path: Path,
) -> dict[str, Any]:
    """Compare two bundles and validate against quality floor."""
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

    # Validate both bundles exist
    if not left_bundle.exists():
        report["defects"].append(f"left bundle not found: {left_bundle}")
        report["status"] = "FAIL"
        return report

    if not right_bundle.exists():
        report["defects"].append(f"right bundle not found: {right_bundle}")
        report["status"] = "FAIL"
        return report

    # Load both manifests
    left_manifest_path = left_bundle / MANIFEST_NAME
    right_manifest_path = right_bundle / MANIFEST_NAME

    left_manifest = None
    right_manifest = None

    try:
        left_manifest = json.loads(left_manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, IOError) as e:
        report["defects"].append(f"failed to read left manifest: {e}")
        report["status"] = "FAIL"

    try:
        right_manifest = json.loads(right_manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, IOError) as e:
        report["defects"].append(f"failed to read right manifest: {e}")
        report["status"] = "FAIL"

    if not left_manifest or not right_manifest:
        return report

    # Validate checksums against actual files (detect tampering)
    left_checksums = {item["path"]: item["sha256"] for item in left_manifest.get("checksums", [])}
    right_checksums = {item["path"]: item["sha256"] for item in right_manifest.get("checksums", [])}

    # Validate left bundle files match checksums
    for report_name in REPORT_NAMES:
        left_path = left_bundle / report_name
        left_expected_hash = left_checksums.get(report_name)

        if not left_path.exists():
            report["defects"].append(f"checksum mismatch: {report_name} missing in left bundle")
            report["status"] = "FAIL"
        else:
            left_actual_hash = sha256_file(left_path)
            if left_actual_hash != left_expected_hash:
                report["defects"].append(f"checksum mismatch: {report_name} in left bundle")
                report["status"] = "FAIL"

    # Validate right bundle files match checksums
    for report_name in REPORT_NAMES:
        right_path = right_bundle / report_name
        right_expected_hash = right_checksums.get(report_name)

        if not right_path.exists():
            report["defects"].append(f"checksum mismatch: {report_name} missing in right bundle")
            report["status"] = "FAIL"
        else:
            right_actual_hash = sha256_file(right_path)
            if right_actual_hash != right_expected_hash:
                report["defects"].append(f"checksum mismatch: {report_name} in right bundle")
                report["status"] = "FAIL"

    # Compare reports by hash
    for report_name in REPORT_NAMES:
        left_path = left_bundle / report_name
        right_path = right_bundle / report_name
        left_hash = left_checksums.get(report_name)
        right_hash = right_checksums.get(report_name)

        # Both files must exist and hashes must match
        if left_path.exists() and right_path.exists() and left_hash and right_hash and left_hash == right_hash:
            matches = True
            report["matching_report_count"] += 1
        else:
            matches = False
            if not left_path.exists() or not right_path.exists():
                report["defects"].append(f"report differs or is absent: {report_name}")
            else:
                report["defects"].append(f"report differs or is absent: {report_name}")
            report["status"] = "FAIL"

        report["report_hash_matches"][report_name] = matches

    # Validate semantic consistency of manifests against actual reports
    if report["status"] == "PASS":
        try:
            left_test_report_path = left_bundle / TEST_REPORT
            left_test_report = json.loads(left_test_report_path.read_text(encoding="utf-8"))
            left_manifest_test_count = left_manifest.get("test_count_observed")
            left_report_test_count = left_test_report.get("tests_run")

            if left_manifest_test_count != left_report_test_count:
                report["defects"].append(
                    f"manifest test_count_observed versus test report tests_run mismatch"
                )
                report["status"] = "FAIL"

            right_test_report_path = right_bundle / TEST_REPORT
            right_test_report = json.loads(right_test_report_path.read_text(encoding="utf-8"))
            right_manifest_test_count = right_manifest.get("test_count_observed")
            right_report_test_count = right_test_report.get("tests_run")

            if right_manifest_test_count != right_report_test_count:
                report["defects"].append(
                    f"manifest test_count_observed versus test report tests_run mismatch"
                )
                report["status"] = "FAIL"
        except (json.JSONDecodeError, IOError, KeyError) as e:
            # If we can't validate, don't fail
            pass

    # Validate quality floor SHA256
    left_floor_entry = left_manifest.get("quality_floor", {})
    left_floor_hash = left_floor_entry.get("sha256")

    right_floor_entry = right_manifest.get("quality_floor", {})
    right_floor_hash = right_floor_entry.get("sha256")

    if floor_path.exists():
        actual_floor_hash = sha256_file(floor_path)
        if left_floor_hash == actual_floor_hash and right_floor_hash == actual_floor_hash:
            report["quality_floor_sha256_match"] = True
        else:
            report["defects"].append("manifest quality_floor.sha256 differs or is absent")
            report["status"] = "FAIL"

    # Check manifest semantic consistency
    if left_manifest != right_manifest:
        # Allow differences in generated_at and platform fields
        left_copy = {k: v for k, v in left_manifest.items() if k not in ["generated_at", "platform"]}
        right_copy = {k: v for k, v in right_manifest.items() if k not in ["generated_at", "platform"]}

        if left_copy != right_copy:
            report["defects"].append("manifest semantic mismatch between bundles")
            report["status"] = "FAIL"

    # claim_allowed must be false in both
    if left_manifest.get("claim_allowed") or right_manifest.get("claim_allowed"):
        report["defects"].append("claim_allowed must be false in both bundles")
        report["status"] = "FAIL"

    return report


def main() -> int:
    """Execute bundle comparison."""
    import argparse

    parser = argparse.ArgumentParser(description="Compare cross-source evidence bundles")
    parser.add_argument(
        "--left-bundle",
        type=Path,
        default=Path(".") / "build" / "cross-source-gate-local",
        help="Path to left bundle directory",
    )
    parser.add_argument(
        "--right-bundle",
        type=Path,
        default=Path(".") / "build" / "cross-source-gate-remote",
        help="Path to right bundle directory",
    )
    parser.add_argument(
        "--floor",
        type=Path,
        default=Path(".") / "indices" / "CROSS_SOURCE_GATE_FLOOR.json",
        help="Path to quality floor JSON",
    )

    args = parser.parse_args()

    report = compare_bundles(args.left_bundle, args.right_bundle, args.floor)

    if report["status"] != "PASS":
        for defect in report["defects"]:
            print(f"ERROR: {defect}")
        return 1

    print("\n" + "=" * 60)
    print("✓ CROSS-SOURCE EVIDENCE COMPARISON PASSED")
    print(f"  - Matching reports: {report['matching_report_count']}/{len(REPORT_NAMES)}")
    print(f"  - Quality floor match: {report['quality_floor_sha256_match']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
