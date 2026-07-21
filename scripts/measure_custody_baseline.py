#!/usr/bin/env python3
"""Measure a conservative pilot baseline for the custody ledger.

This module reports observed process metrics. It deliberately does not convert a
small finite sample into a Six Sigma capability level. Certification and sigma
level remain TOKEN_VAZIO until the statistical convention, sample sufficiency,
and process stability requirements are approved.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_chain_of_custody.py"
SPEC = importlib.util.spec_from_file_location("custody_validator", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load validator: {VALIDATOR_PATH}")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)

OPPORTUNITY_DEFINITIONS = [
    "required_structure",
    "identity_and_uniqueness",
    "utc_time_and_monotonicity",
    "safe_repository_path",
    "evidence_and_claim_consistency",
    "control_state_consistency",
    "chain_link_integrity",
    "declared_hash_and_size_integrity",
]
LINE_RE = re.compile(r"^line ([0-9]+):")


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            stripped = raw.strip()
            if not stripped:
                continue
            value = json.loads(stripped)
            if isinstance(value, dict):
                events.append(value)
    return events


def ratio(numerator: int, denominator: int) -> float | str:
    if denominator == 0:
        return "TOKEN_VAZIO"
    return round(numerator / denominator, 6)


def measure(
    ledger: Path,
    repo_root: Path | None = None,
    measured_at_utc: str | None = None,
) -> dict[str, Any]:
    event_count, defects = validator.validate_ledger(ledger, repo_root)
    events = load_events(ledger)

    defective_lines = {
        int(match.group(1))
        for defect in defects
        if (match := LINE_RE.match(defect)) is not None
    }
    valid_events = max(event_count - len(defective_lines), 0)

    traceable_events = sum(
        1
        for event in events
        if isinstance(event.get("evidence"), list) and bool(event["evidence"])
    )
    reproducible_events = sum(
        1
        for event in events
        if isinstance(event.get("controls"), dict)
        and event["controls"].get("reproducibility") == "verified"
    )
    token_vazio_events = sum(
        1 for event in events if event.get("epistemic_state") == "TOKEN_VAZIO"
    )

    declared_hashes = 0
    verified_hashes = 0
    hash_mismatch_lines = {
        int(match.group(1))
        for defect in defects
        if "object.sha256 mismatch" in defect
        and (match := LINE_RE.match(defect)) is not None
    }
    for line_no, event in enumerate(events, start=1):
        obj = event.get("object")
        if isinstance(obj, dict) and isinstance(obj.get("sha256"), str):
            declared_hashes += 1
            if repo_root is not None and line_no not in hash_mismatch_lines:
                verified_hashes += 1

    opportunities = event_count * len(OPPORTUNITY_DEFINITIONS)
    defect_count = len(defects)
    dpmo = (
        round(defect_count / opportunities * 1_000_000, 3)
        if opportunities
        else "TOKEN_VAZIO"
    )

    timestamp = measured_at_utc or datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    return {
        "schema": "mapa.custody-baseline.v1",
        "measured_at_utc": timestamp,
        "ledger": ledger.as_posix(),
        "repo_root_verification": repo_root is not None,
        "window": {
            "type": "current_ledger_snapshot",
            "event_count": event_count,
            "quality_opportunities_per_event": len(OPPORTUNITY_DEFINITIONS),
            "opportunity_definitions": OPPORTUNITY_DEFINITIONS,
            "total_opportunities": opportunities,
        },
        "observed": {
            "valid_events": valid_events,
            "defective_events": len(defective_lines),
            "defect_count": defect_count,
            "defects": defects,
            "completeness": ratio(valid_events, event_count),
            "traceability": ratio(traceable_events, event_count),
            "integrity": ratio(verified_hashes, declared_hashes),
            "declared_sha256": declared_hashes,
            "verified_sha256": verified_hashes,
            "reproducibility": ratio(reproducible_events, event_count),
            "token_vazio_events": token_vazio_events,
            "token_vazio_resolution": "TOKEN_VAZIO",
            "dpmo_observed": dpmo,
        },
        "six_sigma": {
            "baseline_status": "MEASURED_PILOT",
            "sigma_level": "TOKEN_VAZIO",
            "certification": "TOKEN_VAZIO",
            "reason": (
                "A finite pilot snapshot does not establish process stability, "
                "a confidence-bound convention, or an approved sigma conversion."
            ),
            "next_verifiable_step": (
                "Collect repeated windows, approve the statistical convention, "
                "and evaluate process stability before estimating sigma level."
            ),
        },
        "claim_allowed": defect_count == 0,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Measure the pilot custody-ledger quality baseline"
    )
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.ledger.is_file():
        print(f"ERROR: ledger not found: {args.ledger}", file=sys.stderr)
        return 2
    if args.repo_root is not None and not args.repo_root.is_dir():
        print(f"ERROR: repo root not found: {args.repo_root}", file=sys.stderr)
        return 2

    report = measure(args.ledger, args.repo_root)
    encoded = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0 if report["claim_allowed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
