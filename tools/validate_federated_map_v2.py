#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

COORDS = {"evidence", "reproducibility", "runtime", "formal_rigor", "privacy", "reversibility"}
FORBIDDEN = {"private_payload", "payload", "secret", "password", "access_token", "private_key"}


def digest(data: dict) -> str:
    return hashlib.sha256(
        json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != "mapa.rafaelia_federated_projection.v2":
        errors.append("invalid schema")
    if data.get("claim_allowed") is not False:
        errors.append("claim_allowed must be false")

    source = data.get("machine_source", {})
    if (
        source.get("repository") != "rafaelmeloreisnovo/RafGitTools"
        or len(source.get("commit_sha", "")) != 40
        or len(source.get("blob_sha", "")) != 40
    ):
        errors.append("exact control-plane commit and blob required")

    nodes = data.get("nodes", [])
    ids = {node.get("id") for node in nodes}
    if len(ids) != 15:
        errors.append("expected 15 unique nodes")

    coordinates = data.get("coordinates", [])
    if {item.get("node_id") for item in coordinates} != ids:
        errors.append("one coordinate record per node required")

    records = data.get("measurement_records", [])
    for item in coordinates:
        weights = item.get("weights", {})
        if set(weights) != COORDS:
            errors.append(f"{item.get('node_id')}: incomplete coordinates")
        for coordinate, value in weights.items():
            if value != "TOKEN_VAZIO" and not any(
                record.get("node_id") == item.get("node_id")
                and record.get("coordinate") == coordinate
                and record.get("weight") == value
                for record in records
            ):
                errors.append(f"{item.get('node_id')}/{coordinate}: weight lacks measurement record")

    for overlay in data.get("implementation_overlays", []):
        if (
            len(overlay.get("commit_sha", "")) != 40
            or overlay.get("local_tests", -1) < 0
            or not overlay.get("boundary")
        ):
            errors.append("invalid implementation overlay")

    def walk(value: object, path: str = "root") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key.lower() in FORBIDDEN:
                    errors.append(f"forbidden private key {path}/{key}")
                walk(child, f"{path}/{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{path}/{index}")
    walk(data)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("map", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.map.read_text(encoding="utf-8"))
        errors = validate(data)
    except Exception as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({
        "status": "PASS" if not errors else "FAIL",
        "nodes": len(data.get("nodes", [])),
        "overlays": len(data.get("implementation_overlays", [])),
        "semantic_digest": digest(data),
        "errors": errors,
        "claim_allowed": False,
    }, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
