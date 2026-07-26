#!/usr/bin/env python3
"""Validate the Mapa federated memory pointer registry."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

DEFAULT = Path("indices/MEMORY_COHESION_REGISTRY.v1.jsonl")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
RECORD_RE = re.compile(r"^MAP-RMU-[0-9]{3}$")
UNIT_RE = re.compile(r"^RMU-[A-Z0-9_-]+-[0-9]{3}$")

REQUIRED = {
    "schema_version", "map_record_id", "control_plane", "producer",
    "producer_ref", "producer_path", "producer_blob_sha", "source_digest",
    "unit_id", "relation_class", "source_state", "map_state", "authority",
    "required_next", "claim_allowed",
}


def load(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    if not path.is_file():
        return records, [f"missing registry: {path}"]
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"line {number}: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(f"line {number}: object required")
            continue
        records.append(value)
    return records, errors


def validate_registry(path: Path) -> list[str]:
    records, errors = load(path)
    if not records:
        return errors + ["registry contains no records"]

    record_ids: set[str] = set()
    unit_ids: set[str] = set()
    pins: set[tuple[str, str, str, str]] = set()

    for record in records:
        record_id = str(record.get("map_record_id", "<missing>"))
        missing = sorted(REQUIRED - record.keys())
        if missing:
            errors.append(f"{record_id}: missing {', '.join(missing)}")
        if record.get("schema_version") != "federated-memory-pointer.v1":
            errors.append(f"{record_id}: invalid schema_version")
        if not RECORD_RE.fullmatch(record_id):
            errors.append(f"{record_id}: invalid map_record_id")
        if record_id in record_ids:
            errors.append(f"{record_id}: duplicate record")
        record_ids.add(record_id)

        unit_id = record.get("unit_id")
        if not isinstance(unit_id, str) or not UNIT_RE.fullmatch(unit_id):
            errors.append(f"{record_id}: invalid unit_id")
        elif unit_id in unit_ids:
            errors.append(f"{record_id}: duplicate unit pointer")
        unit_ids.add(str(unit_id))

        if record.get("control_plane") != "rafaelmeloreisnovo/Mapa":
            errors.append(f"{record_id}: invalid control plane")
        if record.get("claim_allowed") is not False:
            errors.append(f"{record_id}: claim_allowed must remain false")
        if record.get("map_state") not in {"PINNED", "STALE", "TOKEN_VAZIO", "CONTRADICTION"}:
            errors.append(f"{record_id}: invalid map_state")
        if not SHA_RE.fullmatch(str(record.get("producer_ref", ""))):
            errors.append(f"{record_id}: invalid producer_ref")
        if not SHA_RE.fullmatch(str(record.get("producer_blob_sha", ""))):
            errors.append(f"{record_id}: invalid producer_blob_sha")

        authority = record.get("authority")
        if not isinstance(authority, dict):
            errors.append(f"{record_id}: authority object required")
        else:
            for key in ("implementation", "research_memory", "control_plane", "execution"):
                if not isinstance(authority.get(key), str) or not authority[key].strip():
                    errors.append(f"{record_id}: authority.{key} required")
            if authority.get("research_memory") != record.get("producer"):
                errors.append(f"{record_id}: research memory authority mismatch")
            if authority.get("control_plane") != record.get("control_plane"):
                errors.append(f"{record_id}: control plane authority mismatch")

        actions = record.get("required_next")
        if not isinstance(actions, list) or not actions:
            errors.append(f"{record_id}: required_next must not be empty")

        if record.get("map_state") == "PINNED":
            pins.add((
                str(record.get("producer")), str(record.get("producer_ref")),
                str(record.get("producer_path")), str(record.get("producer_blob_sha")),
            ))
        if record.get("source_state") == "CONTRADICTION" and record.get("map_state") != "CONTRADICTION":
            errors.append(f"{record_id}: contradiction must remain contradiction")

    if len(pins) > 1:
        errors.append("pinned records disagree on producer ref/path/blob")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry", nargs="?", type=Path, default=DEFAULT)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    errors = validate_registry(args.registry)
    report = {"schema": "memory-cohesion-map-validation.v1", "status": "FAIL" if errors else "PASS", "claim_allowed": False, "errors": errors}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {args.registry}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
