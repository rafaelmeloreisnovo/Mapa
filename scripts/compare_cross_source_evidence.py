#!/usr/bin/env python3
"""Compare two sealed cross-source evidence bundles against the real floor file."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FLOOR = ROOT / "indices" / "CROSS_SOURCE_GATE_FLOOR.json"
REPORT_NAMES = (
    "cross-source-test-validation.json",
    "cross-source-record-validation.json",
    "cross-source-registry-validation.json",
    "chain-of-custody-validation.json",
    "quality-floor-validation.json",
)
MANIFEST_NAME = "LOCAL_GATE_STATUS.json"
CHECKSUMS_NAME = "CHECKSUMS.sha256"
HEX = set("0123456789abcdef")


def is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(char in HEX for char in value)
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name}: top-level JSON value must be an object")
    return value


def load_floor(path: Path) -> tuple[dict[str, Any], str, list[str]]:
    defects: list[str] = []
    floor: dict[str, Any] = {}
    if not path.is_file():
        return floor, "", [f"quality floor not found: {path}"]
    try:
        floor = load_object(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return floor, "", [f"quality floor: {exc}"]

    if floor.get("schema_version") != "rafaelia.cross-source-gate-floor/v2":
        defects.append("quality floor schema_version must be v2")
    minimums = floor.get("minimums")
    invariants = floor.get("invariants")
    if not isinstance(minimums, dict):
        defects.append("quality floor minimums must be an object")
        minimums = {}
    if not isinstance(invariants, dict):
        defects.append("quality floor invariants must be an object")
        invariants = {}

    for field in ("test_files", "tests_discovered", "tests_run"):
        value = minimums.get(field)
        if not is_int(value) or value <= 0:
            defects.append(f"quality floor minimums.{field} must be a positive integer")
    for field in ("complete_execution", "clean_outcomes"):
        if invariants.get(field) is not True:
            defects.append(f"quality floor must require {field}=true")
    for field in (
        "skipped",
        "expected_failures",
        "unexpected_successes",
    ):
        if invariants.get(field) != 0:
            defects.append(f"quality floor must require {field}=0")
    if invariants.get("claim_allowed") is not False:
        defects.append("quality floor must require claim_allowed=false")
    if invariants.get("remote_ci_substituted") is not False:
        defects.append("quality floor must require remote_ci_substituted=false")

    return floor, sha256_file(path), defects


def parse_checksum_file(path: Path) -> tuple[dict[str, str], list[str]]:
    entries: dict[str, str] = {}
    defects: list[str] = []
    if not path.is_file():
        return entries, [f"missing {CHECKSUMS_NAME}"]

    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        parts = raw.split("  ", 1)
        if len(parts) != 2:
            defects.append(f"{CHECKSUMS_NAME} line {line_number}: invalid format")
            continue
        digest, name = parts
        if not is_sha256(digest):
            defects.append(f"{CHECKSUMS_NAME} line {line_number}: invalid sha256")
            continue
        if name not in REPORT_NAMES:
            defects.append(f"{CHECKSUMS_NAME} line {line_number}: unexpected path {name}")
            continue
        if name in entries:
            defects.append(f"{CHECKSUMS_NAME} line {line_number}: duplicate path {name}")
            continue
        entries[name] = digest

    missing = sorted(set(REPORT_NAMES) - set(entries))
    if missing:
        defects.append("checksum entries missing: " + ", ".join(missing))
    return entries, defects


def validate_manifest(
    manifest: dict[str, Any],
    expected_checksums: list[dict[str, str]],
    floor: dict[str, Any],
    floor_sha256: str,
) -> list[str]:
    defects: list[str] = []
    minimums = floor.get("minimums")
    minimums = minimums if isinstance(minimums, dict) else {}

    exact_checks = (
        ("schema_version", manifest.get("schema_version"), "rafaelia.cross-source-local-gate/v3"),
        ("status", manifest.get("status"), "PASS"),
        ("complete_test_execution", manifest.get("complete_test_execution"), True),
        ("clean_test_outcomes", manifest.get("clean_test_outcomes"), True),
        ("minimum_test_file_count", manifest.get("minimum_test_file_count"), minimums.get("test_files")),
        ("minimum_test_count", manifest.get("minimum_test_count"), minimums.get("tests_run")),
        ("report_count", manifest.get("report_count"), len(REPORT_NAMES)),
        ("quality_floor_status", manifest.get("quality_floor_status"), "PASS"),
        ("promotion_state", manifest.get("promotion_state"), "LOCAL_PASS_REMOTE_TOKEN_VAZIO"),
        ("claim_allowed", manifest.get("claim_allowed"), False),
        ("remote_ci_substituted", manifest.get("remote_ci_substituted"), False),
        ("checksums", manifest.get("checksums"), expected_checksums),
    )
    for field, observed, required in exact_checks:
        if observed != required:
            defects.append(
                f"manifest {field}: observed {observed!r}; required {required!r}"
            )

    integer_fields = (
        "test_file_count",
        "minimum_test_file_count",
        "test_count_discovered",
        "test_count_observed",
        "minimum_test_count",
    )
    values: dict[str, int] = {}
    for field in integer_fields:
        observed = manifest.get(field)
        if not is_int(observed) or observed < 0:
            defects.append(f"manifest {field}: must be a non-negative integer")
        else:
            values[field] = observed

    if len(values) == len(integer_fields):
        if values["test_file_count"] < minimums.get("test_files", -1):
            defects.append("manifest test_file_count is below versioned floor")
        if values["test_count_discovered"] < minimums.get("tests_discovered", -1):
            defects.append("manifest test_count_discovered is below versioned floor")
        if values["test_count_observed"] < minimums.get("tests_run", -1):
            defects.append("manifest test_count_observed is below versioned floor")
        if values["test_count_observed"] != values["test_count_discovered"]:
            defects.append("manifest observed test count differs from discovered test count")

    floor_meta = manifest.get("quality_floor")
    if not isinstance(floor_meta, dict):
        defects.append("manifest quality_floor must be an object")
    else:
        expected_path = "indices/CROSS_SOURCE_GATE_FLOOR.json"
        if floor_meta.get("path") != expected_path:
            defects.append("manifest quality_floor.path is not canonical")
        if floor_meta.get("schema_version") != floor.get("schema_version"):
            defects.append("manifest quality_floor.schema_version differs from floor file")
        if floor_meta.get("sha256") != floor_sha256:
            defects.append("manifest quality_floor.sha256 differs from floor file")
        if floor_meta.get("status") != "PASS":
            defects.append("manifest quality_floor.status must be PASS")

    return defects


def validate_bundle(
    directory: Path,
    floor_path: Path = DEFAULT_FLOOR,
) -> dict[str, Any]:
    defects: list[str] = []
    report_hashes: dict[str, str] = {}
    reports: dict[str, dict[str, Any]] = {}
    floor, floor_sha256, floor_defects = load_floor(floor_path)
    defects.extend(floor_defects)

    checksum_entries, checksum_defects = parse_checksum_file(directory / CHECKSUMS_NAME)
    defects.extend(checksum_defects)

    for name in REPORT_NAMES:
        path = directory / name
        if not path.is_file():
            defects.append(f"missing report: {name}")
            continue
        try:
            reports[name] = load_object(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            defects.append(f"{name}: {exc}")
            continue
        digest = sha256_file(path)
        report_hashes[name] = digest
        if checksum_entries.get(name) != digest:
            defects.append(f"checksum mismatch: {name}")

    manifest_path = directory / MANIFEST_NAME
    manifest: dict[str, Any] = {}
    if not manifest_path.is_file():
        defects.append(f"missing {MANIFEST_NAME}")
    else:
        try:
            manifest = load_object(manifest_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            defects.append(f"{MANIFEST_NAME}: {exc}")

    if manifest:
        expected_manifest_checksums = [
            {"path": name, "sha256": report_hashes[name]}
            for name in REPORT_NAMES
            if name in report_hashes
        ]
        defects.extend(
            validate_manifest(
                manifest,
                expected_manifest_checksums,
                floor,
                floor_sha256,
            )
        )

    for name, report in reports.items():
        if report.get("status") != "PASS":
            defects.append(f"{name}: status must be PASS")
        if report.get("claim_allowed") is not False:
            defects.append(f"{name}: claim_allowed must be false")

    return {
        "directory": directory.as_posix(),
        "floor_path": floor_path.as_posix(),
        "floor_sha256": floor_sha256,
        "status": "PASS" if not defects else "FAIL",
        "defect_count": len(defects),
        "defects": defects,
        "report_hashes": report_hashes,
        "manifest": manifest,
    }


def compare_bundles(
    left_directory: Path,
    right_directory: Path,
    floor_path: Path = DEFAULT_FLOOR,
) -> dict[str, Any]:
    left = validate_bundle(left_directory, floor_path)
    right = validate_bundle(right_directory, floor_path)
    defects: list[str] = []

    if left["status"] != "PASS":
        defects.extend(f"left: {item}" for item in left["defects"])
    if right["status"] != "PASS":
        defects.extend(f"right: {item}" for item in right["defects"])

    hash_matches: dict[str, bool] = {}
    for name in REPORT_NAMES:
        left_hash = left["report_hashes"].get(name)
        right_hash = right["report_hashes"].get(name)
        matches = bool(left_hash) and left_hash == right_hash
        hash_matches[name] = matches
        if not matches:
            defects.append(f"report differs or is absent: {name}")

    floor_matches = (
        bool(left["floor_sha256"])
        and left["floor_sha256"] == right["floor_sha256"]
        and left["floor_sha256"] == sha256_file(floor_path)
    )
    if not floor_matches:
        defects.append("quality floor sha256 differs or is absent")

    status = "PASS" if not defects else "FAIL"
    return {
        "schema_version": "rafaelia.cross-source-evidence-comparison/v3",
        "status": status,
        "floor_path": floor_path.as_posix(),
        "floor_sha256": left["floor_sha256"],
        "left_bundle_status": left["status"],
        "right_bundle_status": right["status"],
        "report_count": len(REPORT_NAMES),
        "matching_report_count": sum(hash_matches.values()),
        "report_hash_matches": hash_matches,
        "quality_floor_sha256_match": floor_matches,
        "defect_count": len(defects),
        "defects": defects,
        "claim_allowed": False,
        "remote_ci_substituted": False,
        "next_verifiable_step": (
            "Append a VALIDATE custody event referencing both sealed bundles."
            if status == "PASS"
            else "Preserve both bundles and resolve mismatches without rewriting evidence."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--left", type=Path, required=True)
    parser.add_argument("--right", type=Path, required=True)
    parser.add_argument("--floor", type=Path, default=DEFAULT_FLOOR)
    parser.add_argument("--write-report", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = compare_bundles(args.left, args.right, args.floor)
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
