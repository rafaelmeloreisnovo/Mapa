#!/usr/bin/env python3
"""Compare two sealed cross-source evidence bundles without trusting metadata alone."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

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
        if len(digest) != 64 or any(char not in HEX for char in digest):
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


def validate_bundle(directory: Path) -> dict[str, Any]:
    defects: list[str] = []
    report_hashes: dict[str, str] = {}
    reports: dict[str, dict[str, Any]] = {}

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
        checks = (
            ("status", manifest.get("status"), "PASS"),
            ("report_count", manifest.get("report_count"), len(REPORT_NAMES)),
            ("quality_floor_status", manifest.get("quality_floor_status"), "PASS"),
            ("promotion_state", manifest.get("promotion_state"), "LOCAL_PASS_REMOTE_TOKEN_VAZIO"),
            ("claim_allowed", manifest.get("claim_allowed"), False),
            ("remote_ci_substituted", manifest.get("remote_ci_substituted"), False),
            ("checksums", manifest.get("checksums"), expected_manifest_checksums),
        )
        for field, observed, required in checks:
            if observed != required:
                defects.append(
                    f"manifest {field}: observed {observed!r}; required {required!r}"
                )

    for name, report in reports.items():
        if report.get("status") != "PASS":
            defects.append(f"{name}: status must be PASS")
        if report.get("claim_allowed") is not False:
            defects.append(f"{name}: claim_allowed must be false")

    return {
        "directory": directory.as_posix(),
        "status": "PASS" if not defects else "FAIL",
        "defect_count": len(defects),
        "defects": defects,
        "report_hashes": report_hashes,
        "manifest": manifest,
    }


def compare_bundles(left_directory: Path, right_directory: Path) -> dict[str, Any]:
    left = validate_bundle(left_directory)
    right = validate_bundle(right_directory)
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

    left_floor = left["manifest"].get("quality_floor", {})
    right_floor = right["manifest"].get("quality_floor", {})
    left_floor_sha = left_floor.get("sha256") if isinstance(left_floor, dict) else None
    right_floor_sha = right_floor.get("sha256") if isinstance(right_floor, dict) else None
    floor_matches = bool(left_floor_sha) and left_floor_sha == right_floor_sha
    if not floor_matches:
        defects.append("quality floor sha256 differs or is absent")

    status = "PASS" if not defects else "FAIL"
    return {
        "schema_version": "rafaelia.cross-source-evidence-comparison/v1",
        "status": status,
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
    parser.add_argument("--write-report", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = compare_bundles(args.left, args.right)
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
