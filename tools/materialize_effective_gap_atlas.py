#!/usr/bin/env python3
"""Materialize the effective RAFAELIA Gap Atlas without rewriting history.

Composition order:
  immutable seed -> append-only gap records -> append-only state overrides

The materialized output is derived evidence. Source ledgers remain authoritative and
claim_allowed is always false.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SEED = ROOT / "data/gap-atlas/RAFAELIA_GAP_ATLAS_V1.json"
DEFAULT_APPEND = ROOT / "data/gap-atlas/RAFAELIA_GAP_RECORD_APPEND_V1.jsonl"
DEFAULT_OVERRIDES = ROOT / "data/gap-atlas/GAP_STATE_OVERRIDES_V1.json"


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read {path}: {exc}")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out: list[dict] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as exc:
            fail(f"invalid JSONL {path}:{lineno}: {exc}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=Path, default=DEFAULT_SEED)
    ap.add_argument("--append", type=Path, default=DEFAULT_APPEND)
    ap.add_argument("--overrides", type=Path, default=DEFAULT_OVERRIDES)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    seed = read_json(args.seed)
    if seed.get("schema") != "RAFAELIA_GAP_ATLAS_V1" or seed.get("claim_allowed") is not False:
        fail("invalid seed atlas boundary")

    records = [dict(rec) for rec in seed.get("records", [])]
    by_id: dict[str, dict] = {}
    for rec in records:
        gap_id = rec.get("gap_id")
        if not gap_id or gap_id in by_id:
            fail(f"duplicate/invalid seed gap_id: {gap_id}")
        rec["base_state"] = rec.get("state")
        rec["effective_state"] = rec.get("state")
        rec["state_events"] = []
        by_id[gap_id] = rec

    append_entries = read_jsonl(args.append)
    append_ids: set[str] = set()
    for entry in append_entries:
        if entry.get("schema") != "RAFAELIA_GAP_RECORD_APPEND_V1" or entry.get("claim_allowed") is not False:
            fail("invalid append boundary")
        append_id = entry.get("append_id")
        if not append_id or append_id in append_ids:
            fail(f"duplicate/invalid append_id: {append_id}")
        append_ids.add(append_id)
        rec = entry.get("record")
        if not isinstance(rec, dict) or rec.get("claim_allowed") is not False:
            fail(f"{append_id}: invalid record")
        gap_id = rec.get("gap_id")
        if not gap_id or gap_id in by_id:
            fail(f"{append_id}: duplicate/invalid gap_id {gap_id}")
        rec = dict(rec)
        rec["base_state"] = rec.get("state")
        rec["effective_state"] = rec.get("state")
        rec["state_events"] = [{"type":"APPENDED","append_id":append_id,"at":entry.get("appended_at")}]
        records.append(rec)
        by_id[gap_id] = rec

    overrides = read_json(args.overrides) if args.overrides.exists() else {"overrides": [], "claim_allowed": False}
    if overrides.get("claim_allowed") is not False:
        fail("override claim boundary must remain false")
    seen_override_targets: set[str] = set()
    for index, override in enumerate(overrides.get("overrides", [])):
        gap_id = override.get("gap_id")
        if gap_id not in by_id:
            fail(f"override[{index}] references unknown gap {gap_id}")
        if override.get("claim_allowed") is not False:
            fail(f"override[{index}] promotes claim boundary")
        rec = by_id[gap_id]
        expected_from = override.get("from_state")
        if expected_from and rec["effective_state"] != expected_from:
            fail(f"override[{index}] from_state mismatch for {gap_id}: expected {expected_from}, current {rec['effective_state']}")
        target = override.get("target_state")
        if not target:
            fail(f"override[{index}] missing target_state")
        if gap_id in seen_override_targets:
            fail(f"multiple overrides for {gap_id} require a newer registry version")
        seen_override_targets.add(gap_id)
        rec["effective_state"] = target
        rec["state_events"].append(
            {
                "type": "STATE_OVERRIDE",
                "from": expected_from,
                "to": target,
                "evidence": override.get("evidence", []),
                "next_gate": override.get("next_gate"),
            }
        )

    states = Counter(rec["effective_state"] for rec in records)
    priorities = Counter(rec.get("priority") for rec in records)
    p0_open = sum(1 for rec in records if rec.get("priority") == "P0" and rec["effective_state"] not in {"RESOLVED", "RESOLVED_NEGATIVE"})
    output = {
        "schema": "RAFAELIA_EFFECTIVE_GAP_ATLAS_V1",
        "materialized_at": datetime.now(timezone.utc).isoformat(),
        "claim_allowed": False,
        "publication_ready": False,
        "sources": {
            "seed": str(args.seed),
            "append": str(args.append),
            "overrides": str(args.overrides),
        },
        "counts": {
            "seed_records": len(seed.get("records", [])),
            "appended_records": len(append_entries),
            "effective_records": len(records),
            "p0_open": p0_open,
            "by_state": dict(sorted(states.items())),
            "by_priority": {str(k): v for k, v in sorted(priorities.items())},
        },
        "records": records,
        "semantic_boundary": "derived materialization does not supersede source evidence or authorize scientific/runtime claims",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output["counts"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
