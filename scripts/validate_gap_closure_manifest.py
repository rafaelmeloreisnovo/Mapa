#!/usr/bin/env python3
"""Validate bounded RAFAELIA gap-closure manifests with Python stdlib only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ALLOWED_STATES = {
    "OBSERVED",
    "WIRED",
    "BUILD_PROVEN",
    "RUNTIME_PROVEN",
    "DEVICE_PROVEN",
    "REPRODUCED",
    "TOKEN_VAZIO",
    "BLOCKED",
    "FALSIFIED",
    "CLOSED",
}

SENSITIVE_CLASSES = {
    "physical_runtime",
    "scientific_proof",
    "reproduction",
    "prior_art",
    "coverage",
}


def fail(message: str) -> None:
    raise ValueError(message)


def validate(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))

    if data.get("claim_allowed") is not False:
        fail("claim_allowed must remain false in a gap-closure manifest")
    if not isinstance(data.get("schema"), str) or not data["schema"]:
        fail("schema is required")
    if not isinstance(data.get("wave_id"), str) or not data["wave_id"]:
        fail("wave_id is required")

    gaps = data.get("gaps", [])
    if gaps is not None and not isinstance(gaps, list):
        fail("gaps must be an array when present")

    seen: set[str] = set()
    for index, gap in enumerate(gaps):
        if not isinstance(gap, dict):
            fail(f"gap[{index}] must be an object")
        gap_id = gap.get("id")
        gap_class = gap.get("class")
        state = gap.get("state")
        if not isinstance(gap_id, str) or not gap_id:
            fail(f"gap[{index}].id is required")
        if gap_id in seen:
            fail(f"duplicate gap id: {gap_id}")
        seen.add(gap_id)
        if not isinstance(gap_class, str) or not gap_class:
            fail(f"{gap_id}: class is required")
        if state not in ALLOWED_STATES:
            fail(f"{gap_id}: unsupported state {state!r}")

        if gap_class in SENSITIVE_CLASSES and state == "CLOSED":
            evidence = gap.get("evidence")
            if not isinstance(evidence, list) or not evidence:
                fail(f"{gap_id}: sensitive CLOSED gap requires non-empty evidence")
            producer = gap.get("producer")
            if not isinstance(producer, str) or not producer:
                fail(f"{gap_id}: sensitive CLOSED gap requires producer authority")

        if state == "TOKEN_VAZIO" and not (gap.get("next_gate") or gap.get("required_evidence")):
            fail(f"{gap_id}: TOKEN_VAZIO requires next_gate or required_evidence")

    print(f"PASS {path}: {len(gaps)} gaps; claim_allowed=false")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: validate_gap_closure_manifest.py <manifest.json> [...]", file=sys.stderr)
        return 2
    try:
        for raw in argv[1:]:
            validate(Path(raw))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
