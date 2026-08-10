#!/usr/bin/env python3
"""Normalize specialized RAFAELIA ledgers into discovery candidates.

This tool is intentionally discovery-only. It never mutates the Gap Atlas and never
sets claim_allowed=true. Three bounded input modes are supported:

* rll-json: machine-readable RLL epistemic-void style JSON with records[];
* token-kv: KEY=VALUE ledgers such as OPCORE94 TOKEN_VAZIO itemizations;
* markdown-states: Markdown/text lines containing explicit operational state markers.

The output is a candidate receipt requiring subsequent mapping/review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

STATE_MARKERS = (
    "TOKEN_VAZIO",
    "BLOCKED",
    "NOT_MEASURED",
    "STALE",
    "ORPHAN",
    "UNSAFE",
    "CONTRADICTION",
    "CONTRADICTED",
    "STUB",
    "PARTIAL",
    "ACCEPTED_LIMITATION",
    "CI_PENDING",
    "RUNTIME TOKEN_VAZIO",
)
TOKEN_KV_RE = re.compile(r"^([A-Z][A-Z0-9_\-]{2,})=(.*)$")


def stable_id(source: str, native_id: str, raw: str) -> str:
    payload = f"{source}\0{native_id}\0{raw}".encode("utf-8", errors="replace")
    return "DISC-" + hashlib.sha256(payload).hexdigest()[:24].upper()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_rll_json(path: Path, source: str) -> list[dict]:
    data = load_json(path)
    records = data.get("records")
    if not isinstance(records, list):
        raise SystemExit("ERROR: rll-json input must contain records[]")
    out: list[dict] = []
    for index, rec in enumerate(records):
        if not isinstance(rec, dict):
            continue
        state = str(rec.get("state", "TOKEN_VAZIO"))
        if state in {"RESOLVED", "RESOLVED_NEGATIVE"}:
            # terminal records are retained as context but not emitted as open candidates
            continue
        native_id = str(rec.get("id") or f"record-{index}")
        raw = json.dumps(rec, ensure_ascii=False, sort_keys=True)
        out.append(
            {
                "candidate_id": stable_id(source, native_id, raw),
                "native_id": native_id,
                "source_state": state,
                "priority": rec.get("priority"),
                "domain": rec.get("domain"),
                "question": rec.get("question"),
                "unknowns": rec.get("unknowns", []),
                "next_gate": rec.get("next_gate"),
                "source_refs": rec.get("source_refs", []),
                "disposition": "REQUIRES_GAP_ATLAS_MAPPING",
            }
        )
    return out


def normalize_token_kv(path: Path, source: str) -> list[dict]:
    out: list[dict] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        match = TOKEN_KV_RE.match(line.strip())
        if not match:
            continue
        key, value = match.groups()
        if not (key.startswith("TOKEN_VAZIO") or any(marker in key for marker in STATE_MARKERS)):
            continue
        raw = line.strip()
        out.append(
            {
                "candidate_id": stable_id(source, key, raw),
                "native_id": key,
                "source_state": "TOKEN_VAZIO" if key.startswith("TOKEN_VAZIO") else "DISCOVERED",
                "line": lineno,
                "raw": raw,
                "description": value.strip(),
                "disposition": "REQUIRES_GAP_ATLAS_MAPPING",
            }
        )
    return out


def markers_in(line: str) -> list[str]:
    upper = line.upper()
    return sorted({marker for marker in STATE_MARKERS if marker in upper})


def normalize_markdown_states(path: Path, source: str) -> list[dict]:
    out: list[dict] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        markers = markers_in(line)
        if not markers:
            continue
        raw = line.rstrip()
        native_id = f"line-{lineno}"
        out.append(
            {
                "candidate_id": stable_id(source, native_id, raw),
                "native_id": native_id,
                "source_state_markers": markers,
                "line": lineno,
                "raw": raw,
                "disposition": "REQUIRES_GAP_ATLAS_MAPPING_OR_EXPLICIT_FALSE_POSITIVE",
            }
        )
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=["rll-json", "token-kv", "markdown-states"])
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--source", required=True, help="Stable provider/repository/path identifier")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fail-on-empty", action="store_true")
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(f"ERROR: input does not exist: {args.input}")

    if args.mode == "rll-json":
        candidates = normalize_rll_json(args.input, args.source)
    elif args.mode == "token-kv":
        candidates = normalize_token_kv(args.input, args.source)
    else:
        candidates = normalize_markdown_states(args.input, args.source)

    receipt = {
        "schema": "RAFAELIA_SPECIALIZED_LEDGER_DISCOVERY_V1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "claim_allowed": False,
        "mode": args.mode,
        "source": args.source,
        "input": str(args.input),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "semantic_boundary": "candidate extraction is not gap resolution and not source truth promotion",
        "next_gate": "Map each candidate to an existing gap_id, create a new typed gap, or record an explicit false-positive/accepted-limitation disposition.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "candidates": len(candidates), "claim_allowed": False}, sort_keys=True))
    return 1 if args.fail_on_empty and not candidates else 0


if __name__ == "__main__":
    raise SystemExit(main())
