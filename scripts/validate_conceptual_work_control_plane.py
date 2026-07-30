#!/usr/bin/env python3
"""Validate CONCEPTUAL_WORK_CONTROL_PLANE.json using Python stdlib only."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

REQUIRED_LAYER_IDS = {f"L{i:02d}" for i in range(1, 21)}
REQUIRED_DECISION_IDS = {f"D{i:03d}" for i in range(1, 19)}


def load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("root must be object")
    return data


def validate(data: dict) -> dict:
    errors = []
    if data.get("schema") != "conceptual_work_control_plane_v1":
        errors.append("invalid schema")
    scope = data.get("scope", {})
    if scope.get("claim_allowed") is not False:
        errors.append("claim_allowed must remain false")
    if scope.get("certification_claim") is not False:
        errors.append("certification_claim must remain false")
    if scope.get("legal_compliance_claim") is not False:
        errors.append("legal_compliance_claim must remain false")

    invariants = set(data.get("invariants", []))
    for invariant in (
        "concept != implementation",
        "image != proof",
        "hash != truth",
        "TOKEN_VAZIO != zero",
    ):
        if invariant not in invariants:
            errors.append(f"missing invariant: {invariant}")

    layers = data.get("layers", [])
    layer_ids = [x.get("id") for x in layers if isinstance(x, dict)]
    if set(layer_ids) != REQUIRED_LAYER_IDS or len(layer_ids) != len(set(layer_ids)):
        errors.append("layers must be exactly L01..L20 and unique")
    if not all(x.get("mandatory") is True for x in layers if isinstance(x, dict)):
        errors.append("all layers must be mandatory")

    decisions = data.get("decisions", [])
    decision_ids = [x.get("id") for x in decisions if isinstance(x, dict)]
    if set(decision_ids) != REQUIRED_DECISION_IDS or len(decision_ids) != len(set(decision_ids)):
        errors.append("decisions must be exactly D001..D018 and unique")
    if any(x.get("claim_allowed") is not False for x in decisions if isinstance(x, dict)):
        errors.append("decision entries cannot enable claims")

    ladder = data.get("promotion_ladder", [])
    levels = [x.get("level") for x in ladder if isinstance(x, dict)]
    if levels != [f"P{i}" for i in range(7)]:
        errors.append("promotion ladder must be ordered P0..P6")

    journal = data.get("journal_contract", {})
    if journal.get("append_only") is not True:
        errors.append("journal must be append-only")
    required = set(journal.get("required_fields", []))
    for field in (
        "event_id",
        "previous_event_sha256",
        "event_sha256",
        "residual",
        "next_action",
    ):
        if field not in required:
            errors.append(f"journal missing field: {field}")

    blockers = data.get("open_blockers", [])
    if len(blockers) < 5:
        errors.append("at least five explicit blockers required")
    for item in blockers:
        if not str(item.get("state", "")).startswith("TOKEN_VAZIO"):
            errors.append(f"blocker {item.get('id')} must remain TOKEN_VAZIO")
        if not item.get("exit"):
            errors.append(f"blocker {item.get('id')} missing exit criterion")

    refs = data.get("references", [])
    if len(refs) < 4 or any(x.get("claim") != "REFERENCE_ONLY" for x in refs):
        errors.append("rights/UNESCO references must be REFERENCE_ONLY")

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "layer_count": len(layers),
        "decision_count": len(decisions),
        "blocker_count": len(blockers),
        "claim_allowed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="indices/CONCEPTUAL_WORK_CONTROL_PLANE.json")
    parser.add_argument("--write-report")
    args = parser.parse_args()
    report = validate(load(Path(args.input)))
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.write_report:
        Path(args.write_report).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
