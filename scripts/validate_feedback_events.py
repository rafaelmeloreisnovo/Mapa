#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA = "rafaelia.feedback-event/v1"
STATES = {"TOKEN_VAZIO", "PENDING", "PARTIAL", "VERIFIED_LIMITED", "VERIFIED", "PASS", "FAIL", "CONTRADICTION"}
TRANSITIONS = {"OBSERVATION", "EXECUTION", "PROMOTION", "CORRECTION", "CONTRADICTION", "REGRESSION"}
LEVERAGE = {"LOCAL", "SYSTEMIC", "MULTIPLICATIVE", "EXPONENTIAL_CANDIDATE", "FACTORIAL_CANDIDATE"}
RANK = {"TOKEN_VAZIO": 0, "PENDING": 1, "PARTIAL": 2, "VERIFIED_LIMITED": 3, "VERIFIED": 4, "PASS": 5}
DOWNGRADE_KINDS = {"CORRECTION", "CONTRADICTION", "REGRESSION"}


def canonical_hash(event: dict[str, Any]) -> str:
    payload = dict(event)
    payload.pop("event_hash", None)
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_no}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"line {line_no}: event must be object")
        events.append(value)
    return events


def validate(path: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        events = load_jsonl(path)
    except Exception as exc:
        return {"status": "FAIL", "errors": [str(exc)], "warnings": [], "metrics": {"events": 0}, "claim_allowed": False}

    seen: dict[str, int] = {}
    previous_hash: str | None = None
    latest_state_by_objective: dict[str, str] = {}
    promotions = 0

    for index, event in enumerate(events, 1):
        prefix = f"event[{index}]"
        if event.get("schema") != SCHEMA:
            errors.append(f"{prefix}.schema invalid")
        if event.get("sequence") != index:
            errors.append(f"{prefix}.sequence must equal append order {index}")

        event_id = event.get("event_id")
        if not isinstance(event_id, str) or not event_id:
            errors.append(f"{prefix}.event_id missing")
        elif event_id in seen:
            errors.append(f"duplicate event_id {event_id}")
        else:
            seen[event_id] = index

        if event.get("transition_kind") not in TRANSITIONS:
            errors.append(f"{prefix}.transition_kind invalid")
        prior = event.get("prior_state")
        observed = event.get("observed_state")
        if prior not in STATES or observed not in STATES:
            errors.append(f"{prefix}.state invalid")

        source_refs = event.get("source_refs")
        evidence_refs = event.get("evidence_refs")
        if not isinstance(source_refs, list) or not source_refs:
            errors.append(f"{prefix}.source_refs must be non-empty")
        if not isinstance(evidence_refs, list):
            errors.append(f"{prefix}.evidence_refs must be array")
            evidence_refs = []
        if not isinstance(event.get("F_ok"), list):
            errors.append(f"{prefix}.F_ok must be array")
        if not isinstance(event.get("F_gap"), list):
            errors.append(f"{prefix}.F_gap must be array")
        if not isinstance(event.get("F_next"), list) or not event.get("F_next"):
            errors.append(f"{prefix}.F_next must be non-empty")

        predecessors = event.get("predecessor_event_ids")
        if not isinstance(predecessors, list):
            errors.append(f"{prefix}.predecessor_event_ids must be array")
            predecessors = []
        for predecessor in predecessors:
            if predecessor not in seen:
                errors.append(f"{prefix} predecessor {predecessor} must reference an earlier event")

        if event.get("prev_event_hash") != previous_hash:
            errors.append(f"{prefix}.prev_event_hash chain mismatch")
        actual_hash = event.get("event_hash")
        calculated_hash = canonical_hash(event)
        if actual_hash != calculated_hash:
            errors.append(f"{prefix}.event_hash mismatch")
        previous_hash = actual_hash if isinstance(actual_hash, str) else None

        if event.get("leverage_class") not in LEVERAGE:
            errors.append(f"{prefix}.leverage_class invalid")
        if not isinstance(event.get("leverage_basis"), str) or len(event.get("leverage_basis", "").strip()) < 8:
            errors.append(f"{prefix}.leverage_basis missing")

        objective = event.get("objective")
        prior_objective_state = latest_state_by_objective.get(objective)
        if prior_objective_state is not None and prior != prior_objective_state:
            warnings.append(f"{prefix}.prior_state differs from previous observed state for same objective")

        kind = event.get("transition_kind")
        if prior in RANK and observed in RANK and RANK[observed] < RANK[prior]:
            if kind not in DOWNGRADE_KINDS:
                errors.append(f"{prefix} silent evidence downgrade is forbidden")
            if not evidence_refs:
                errors.append(f"{prefix} evidence-backed reason required for downgrade")

        if observed in {"FAIL", "CONTRADICTION"} and kind not in {"EXECUTION", "CORRECTION", "CONTRADICTION", "REGRESSION"}:
            warnings.append(f"{prefix} terminal negative state should use an evidential transition kind")

        if event.get("claim_allowed") is True:
            promotions += 1
            if observed not in {"VERIFIED", "PASS"}:
                errors.append(f"{prefix} claim_allowed requires VERIFIED or PASS")
            if not evidence_refs:
                errors.append(f"{prefix} claim_allowed requires evidence_refs")
            if not event.get("gate_id"):
                errors.append(f"{prefix} claim_allowed requires gate_id")
            if kind not in {"PROMOTION", "EXECUTION"}:
                errors.append(f"{prefix} claim_allowed requires PROMOTION or EXECUTION")

        if kind == "PROMOTION" and event.get("claim_allowed") is not True:
            errors.append(f"{prefix} PROMOTION requires claim_allowed=true")
        if observed == "TOKEN_VAZIO" and not event.get("F_gap"):
            warnings.append(f"{prefix} TOKEN_VAZIO should state F_gap")
        if isinstance(objective, str):
            latest_state_by_objective[objective] = observed

    return {
        "schema_version": "rafaelia.feedback-event-validation/v1",
        "status": "PASS" if not errors else "FAIL",
        "claim_allowed": False,
        "errors": errors,
        "warnings": warnings,
        "metrics": {"events": len(events), "promotions": promotions, "chain_head": previous_hash},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", default="data/feedback-events/feedback-events.v1.jsonl")
    parser.add_argument("--write-report")
    args = parser.parse_args()
    report = validate(Path(args.ledger))
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.write_report:
        output = Path(args.write_report)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
