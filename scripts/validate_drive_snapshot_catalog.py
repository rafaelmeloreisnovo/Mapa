#!/usr/bin/env python3
"""Deterministic validator for the metadata-only Drive snapshot catalog."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

FORBIDDEN_KEYS = {
    "body", "content", "parts", "message_text", "user_profile",
    "conversation_title", "prompt", "response", "email", "phone"
}
ALLOWED_STATUSES = {
    "CANONICAL_RAW", "HISTORICAL_CHECKPOINT", "ASSET_POOL",
    "DUPLICATE_CANDIDATE", "TOKEN_VAZIO"
}
ALLOWED_TYPES = {"complete_export", "asset_pool", "conversation_asset_tree"}


class CatalogError(ValueError):
    pass


def fail(message: str) -> None:
    raise CatalogError(message)


def walk_keys(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            found.add(str(key))
            found.update(walk_keys(child))
    elif isinstance(value, list):
        for child in value:
            found.update(walk_keys(child))
    return found


def parse_utc(value: str, field: str) -> dt.datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        fail(f"{field} must be an UTC timestamp ending in Z")
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        fail(f"{field} is not a valid timestamp: {exc}")
    raise AssertionError("unreachable")


def validate_catalog(data: dict[str, Any]) -> dict[str, Any]:
    if data.get("schema_version") != "mapa.drive-memory-snapshot-catalog.v1":
        fail("unsupported schema_version")
    if data.get("source_scope") != "google_drive_private":
        fail("source_scope must remain google_drive_private")
    if data.get("privacy_boundary") != "metadata_only":
        fail("privacy_boundary must remain metadata_only")
    if data.get("content_claim_allowed") is not False:
        fail("content_claim_allowed must be false")
    parse_utc(data.get("generated_at_utc"), "generated_at_utc")

    active = data.get("active_context")
    if not isinstance(active, dict) or len(active) != 5:
        fail("active_context must contain exactly five variables")

    forbidden = walk_keys(data).intersection(FORBIDDEN_KEYS)
    if forbidden:
        fail(f"forbidden private/content keys present: {sorted(forbidden)}")

    snapshots = data.get("snapshots")
    if not isinstance(snapshots, list) or not snapshots:
        fail("snapshots must be a non-empty list")

    ids: set[str] = set()
    folder_ids: set[str] = set()
    canonicals: list[str] = []
    complete_counts: list[int] = []

    for index, item in enumerate(snapshots):
        if not isinstance(item, dict):
            fail(f"snapshots[{index}] must be an object")
        sid = item.get("snapshot_id")
        fid = item.get("folder_id")
        if not isinstance(sid, str) or not sid:
            fail(f"snapshots[{index}].snapshot_id is required")
        if sid in ids:
            fail(f"duplicate snapshot_id: {sid}")
        ids.add(sid)
        if not isinstance(fid, str) or len(fid) < 10:
            fail(f"{sid}: invalid folder_id")
        if fid in folder_ids:
            fail(f"duplicate folder_id: {fid}")
        folder_ids.add(fid)
        if item.get("privacy") != "restricted":
            fail(f"{sid}: privacy must be restricted")
        if item.get("status") not in ALLOWED_STATUSES:
            fail(f"{sid}: unsupported status")
        if item.get("container_type") not in ALLOWED_TYPES:
            fail(f"{sid}: unsupported container_type")
        if not item.get("evidence"):
            fail(f"{sid}: evidence is required")
        if not item.get("next_verifiable_step"):
            fail(f"{sid}: next_verifiable_step is required")

        if item.get("status") == "CANONICAL_RAW":
            canonicals.append(sid)

        cj = item.get("conversations_json")
        if item.get("container_type") == "complete_export":
            if not isinstance(cj, dict):
                fail(f"{sid}: complete_export requires conversations_json")
            size = cj.get("size_bytes")
            if not isinstance(size, int) or size <= 0:
                fail(f"{sid}: size_bytes must be positive")
            parse_utc(cj.get("modified_at_utc"), f"{sid}.modified_at_utc")
            count = cj.get("conversation_count")
            if count is not None:
                if not isinstance(count, int) or count < 0:
                    fail(f"{sid}: conversation_count must be null or non-negative")
                complete_counts.append(count)
            digest = cj.get("sha256")
            if digest is not None and (
                not isinstance(digest, str)
                or len(digest) != 64
                or any(ch not in "0123456789abcdef" for ch in digest)
            ):
                fail(f"{sid}: invalid sha256")
        elif cj is not None:
            fail(f"{sid}: asset containers must not declare conversations_json")

        if item.get("status") == "DUPLICATE_CANDIDATE":
            if not item.get("duplicate_candidate_group"):
                fail(f"{sid}: duplicate candidate group required")
            if cj.get("sha256") is not None:
                fail(f"{sid}: status must be resolved after hash is known")

    if len(canonicals) != 1:
        fail("exactly one CANONICAL_RAW snapshot is required")
    if data.get("canonical_snapshot_id") != canonicals[0]:
        fail("canonical_snapshot_id does not match CANONICAL_RAW")

    canonical = next(x for x in snapshots if x["snapshot_id"] == canonicals[0])
    canonical_count = canonical["conversations_json"].get("conversation_count")
    if canonical_count is not None and complete_counts and canonical_count < max(complete_counts):
        fail("canonical conversation_count cannot be lower than a checkpoint count")

    gates = data.get("open_gates")
    if not isinstance(gates, list) or not gates:
        fail("open_gates must be non-empty")
    gate_ids: set[str] = set()
    for gate in gates:
        if gate.get("gate_id") in gate_ids:
            fail(f"duplicate gate_id: {gate.get('gate_id')}")
        gate_ids.add(gate.get("gate_id"))
        if gate.get("state") != "TOKEN_VAZIO" or gate.get("claim_allowed") is not False:
            fail(f"{gate.get('gate_id')}: open gate must be fail-closed")
        if not gate.get("condition"):
            fail(f"{gate.get('gate_id')}: condition is required")

    return {
        "ok": True,
        "schema_version": data["schema_version"],
        "snapshots": len(snapshots),
        "canonical_snapshot_id": canonicals[0],
        "open_gates": len(gates),
        "privacy_boundary": data["privacy_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--catalog",
        default="indices/memoria-longitudinal/drive_snapshot_catalog.v1.json",
    )
    parser.add_argument("--write-report")
    args = parser.parse_args()

    path = Path(args.catalog)
    data = json.loads(path.read_text(encoding="utf-8"))
    try:
        report = validate_catalog(data)
    except (CatalogError, json.JSONDecodeError) as exc:
        report = {"ok": False, "error": str(exc)}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    print(payload, end="")
    if args.write_report:
        out = Path(args.write_report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
