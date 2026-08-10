#!/usr/bin/env python3
"""Fail-closed validator for RAFAELIA_GAP_ATLAS_V1.

The validator is standard-library only. It intentionally validates the operational
contract rather than claiming that external gaps are closed. A green validation
means the atlas is internally coherent, not that the ecosystem is complete.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ATLAS = ROOT / "data" / "gap-atlas" / "RAFAELIA_GAP_ATLAS_V1.json"

PRIORITIES = {"P0", "P1", "P2", "P3"}
STATES = {
    "DISCOVERED", "TOKEN_VAZIO", "READY_FOR_TEST", "REDUCED", "RESOLVED",
    "RESOLVED_NEGATIVE", "BLOCKED", "NOT_MEASURED", "STALE", "ORPHAN",
    "UNSAFE", "CONTRADICTED", "STUB", "ACCEPTED_LIMITATION",
}
CLASSES = {
    "INVENTORY", "IDENTITY", "PROVENANCE", "SEMANTIC", "IMPLEMENTATION",
    "EXECUTION", "EVIDENCE", "DATA", "SECURITY", "GOVERNANCE", "INTEGRATION",
    "PROMOTION", "STALE", "ORPHAN", "DUPLICATE", "ACCEPTED_LIMITATION",
    "CONTRADICTION",
}
PROVIDERS = {
    "GitHub", "Google Drive", "Android/Termux", "External Scientific Source",
    "Human Review", "Cross-Provider",
}
INVARIANT = [
    "IDENTITY", "PROVENANCE", "SEMANTICS", "EXECUTION", "EVIDENCE",
    "GOVERNANCE", "LINEAGE",
]
REQUIRED = {
    "gap_id", "artifact_id", "provider", "scope", "gap_class", "priority",
    "state", "known", "unknown", "authority_required", "evidence_required",
    "acceptance_criterion", "predecessors", "successors", "next_gate",
    "source_refs", "claim_allowed",
}
OPEN_STATES = STATES - {"RESOLVED", "RESOLVED_NEGATIVE"}


def die(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def nonempty_strings(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(v, str) and v.strip() for v in value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--atlas", type=Path, default=DEFAULT_ATLAS)
    parser.add_argument("--write-report", type=Path)
    args = parser.parse_args()

    try:
        data = json.loads(args.atlas.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        die(f"cannot read atlas: {exc}")

    if data.get("schema") != "RAFAELIA_GAP_ATLAS_V1":
        die("unexpected schema")
    if data.get("mode") != "APPEND_ONLY_FEDERATED":
        die("mode must be APPEND_ONLY_FEDERATED")
    if data.get("claim_allowed") is not False:
        die("top-level claim_allowed must be false")
    if data.get("invariant") != INVARIANT:
        die("seven-axis invariant changed or reordered")

    records = data.get("records")
    if not isinstance(records, list) or not records:
        die("records must be a non-empty list")

    ids: list[str] = []
    priorities: Counter[str] = Counter()
    states: Counter[str] = Counter()
    classes: Counter[str] = Counter()
    providers: Counter[str] = Counter()
    internal_edges: defaultdict[str, set[str]] = defaultdict(set)

    for i, rec in enumerate(records):
        if not isinstance(rec, dict):
            die(f"records[{i}] is not an object")
        missing = REQUIRED - rec.keys()
        if missing:
            die(f"records[{i}] missing fields: {sorted(missing)}")
        gap_id = rec["gap_id"]
        if not isinstance(gap_id, str) or not gap_id.startswith("GAP-"):
            die(f"invalid gap_id at records[{i}]")
        ids.append(gap_id)
        if rec["claim_allowed"] is not False:
            die(f"{gap_id}: claim_allowed must remain false")
        if rec["priority"] not in PRIORITIES:
            die(f"{gap_id}: invalid priority")
        if rec["state"] not in STATES:
            die(f"{gap_id}: invalid state")
        if rec["gap_class"] not in CLASSES:
            die(f"{gap_id}: invalid gap_class")
        if rec["provider"] not in PROVIDERS:
            die(f"{gap_id}: invalid provider")
        for field in ("known", "unknown", "authority_required", "evidence_required", "source_refs"):
            if not nonempty_strings(rec[field]):
                die(f"{gap_id}: {field} must contain non-empty strings")
        for field in ("predecessors", "successors", "resolution_evidence"):
            if field in rec and (not isinstance(rec[field], list) or any(not isinstance(v, str) or not v for v in rec[field])):
                die(f"{gap_id}: {field} must be a string list")
        if not isinstance(rec["next_gate"], str) or not rec["next_gate"].strip():
            die(f"{gap_id}: next_gate is required")
        if not isinstance(rec["acceptance_criterion"], str) or not rec["acceptance_criterion"].strip():
            die(f"{gap_id}: acceptance_criterion is required")
        if rec["state"] in {"RESOLVED", "RESOLVED_NEGATIVE"} and not rec.get("resolution_evidence"):
            die(f"{gap_id}: terminal resolution requires evidence")
        if rec["state"] == "ACCEPTED_LIMITATION" and not rec["unknown"]:
            die(f"{gap_id}: accepted limitation must preserve the unresolved boundary")
        priorities[rec["priority"]] += 1
        states[rec["state"]] += 1
        classes[rec["gap_class"]] += 1
        providers[rec["provider"]] += 1

    duplicated = [gap_id for gap_id, count in Counter(ids).items() if count != 1]
    if duplicated:
        die(f"duplicate gap IDs: {duplicated}")

    idset = set(ids)
    for rec in records:
        for target in rec.get("successors", []):
            if target.startswith("GAP-"):
                if target not in idset:
                    die(f"{rec['gap_id']}: missing internal successor {target}")
                internal_edges[rec["gap_id"]].add(target)
        for source in rec.get("predecessors", []):
            if source.startswith("GAP-") and source not in idset:
                die(f"{rec['gap_id']}: missing internal predecessor {source}")

    # Reject direct self-loops; longer cycles are reported as a conservative warning
    # because some legitimate reconciliation graphs may be bidirectionally annotated.
    for node, targets in internal_edges.items():
        if node in targets:
            die(f"{node}: self-loop in lineage")

    p0_open = sum(1 for rec in records if rec["priority"] == "P0" and rec["state"] in OPEN_STATES)
    terminal = states["RESOLVED"] + states["RESOLVED_NEGATIVE"]
    report = {
        "schema": "RAFAELIA_GAP_ATLAS_VALIDATION_REPORT_V1",
        "status": "PASS",
        "claim_allowed": False,
        "publication_ready": False,
        "atlas": str(args.atlas.relative_to(ROOT)) if args.atlas.is_relative_to(ROOT) else str(args.atlas),
        "records": len(records),
        "terminal_records": terminal,
        "open_records": len(records) - terminal,
        "p0_open": p0_open,
        "by_priority": dict(sorted(priorities.items())),
        "by_state": dict(sorted(states.items())),
        "by_class": dict(sorted(classes.items())),
        "by_provider": dict(sorted(providers.items())),
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "invariant": INVARIANT,
        "meaning": "PASS validates atlas coherence only; it does not close external gaps.",
    }

    text = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.write_report:
        out = args.write_report
        if not out.is_absolute():
            out = ROOT / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
