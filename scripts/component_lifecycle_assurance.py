#!/usr/bin/env python3
"""RAFAELIA Component Lifecycle Assurance V1.

Models component validity with multiple clocks and event-triggered revalidation.
Unknown clocks are explicit TOKEN_VAZIO values, never silently converted to zero.
This is an engineering assurance model, not an aviation certification claim.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

CLOCKS = {
    "calendar_age", "execution_hours", "cycles", "starts_stops", "builds",
    "test_cycles", "deployments", "commits_since_validation", "dependency_changes",
    "environment_exposure", "load_stress_proxy", "incident_count", "near_miss_count",
    "maintenance_actions", "corrective_actions", "software_schema_version",
    "evidence_age", "provenance_age", "last_verified_at",
}
RULE_TYPES = {"HARD_LIMIT", "RECOMMENDED_INTERVAL", "CONDITION_BASED", "EVENT_TRIGGERED", "HEURISTIC_LIMIT"}
PROPAGATION_STATES = {"DIRECT", "POTENTIAL_PROPAGATION", "NOT_AFFECTED_BY_EVIDENCE", "REVALIDATION_REQUIRED", "TOKEN_VAZIO"}


def nonempty(v: Any) -> bool:
    return v is not None and (not isinstance(v, (str, list, dict)) or bool(v))


def validate(record: dict[str, Any]) -> list[str]:
    e: list[str] = []
    required = ["schema_version", "component_id", "observed_at", "source_pointer", "owner_authority",
                "lifecycle_clocks", "revalidation_rules", "event_history", "impact_radius",
                "next_review_gate", "retirement_or_revalidation_criteria", "claim_allowed"]
    for k in required:
        if k not in record:
            e.append(f"missing required field: {k}")
    if record.get("schema_version") != "rafaelia.component-lifecycle-assurance/v1":
        e.append("invalid schema_version")

    clocks = record.get("lifecycle_clocks")
    if not isinstance(clocks, dict):
        e.append("lifecycle_clocks must be object")
        clocks = {}
    missing = sorted(CLOCKS - set(clocks))
    if missing:
        e.append("missing lifecycle clocks: " + ", ".join(missing))
    for name in CLOCKS & set(clocks):
        c = clocks[name]
        if not isinstance(c, dict):
            e.append(f"clock {name} must be object")
            continue
        if "value" not in c or "state" not in c or "source" not in c:
            e.append(f"clock {name} requires value,state,source")
            continue
        if c.get("state") not in {"OBSERVED", "DERIVED", "TOKEN_VAZIO"}:
            e.append(f"clock {name} invalid state")
        if c.get("state") == "TOKEN_VAZIO" and c.get("value") != "TOKEN_VAZIO":
            e.append(f"clock {name} TOKEN_VAZIO state requires TOKEN_VAZIO value")
        if c.get("state") != "TOKEN_VAZIO" and not nonempty(c.get("source")):
            e.append(f"clock {name} observed/derived value requires source")

    rules = record.get("revalidation_rules")
    if not isinstance(rules, list):
        e.append("revalidation_rules must be list")
        rules = []
    for i, r in enumerate(rules):
        if not isinstance(r, dict):
            e.append(f"rule[{i}] must be object")
            continue
        if r.get("type") not in RULE_TYPES:
            e.append(f"rule[{i}] invalid type")
        for k in ("trigger", "origin", "action", "evidence_needed", "falsifier"):
            if not nonempty(r.get(k)):
                e.append(f"rule[{i}].{k} required")

    events = record.get("event_history")
    radius = record.get("impact_radius")
    if not isinstance(events, list):
        e.append("event_history must be list")
        events = []
    if not isinstance(radius, list):
        e.append("impact_radius must be list")
        radius = []
    if events and not radius:
        e.append("event_history requires non-empty impact_radius")
    for i, n in enumerate(radius):
        if not isinstance(n, dict):
            e.append(f"impact_radius[{i}] must be object")
            continue
        for k in ("component", "relation", "propagation_state", "direct_exposure", "transmitted_effect",
                  "hidden_state_possible", "inspection_required", "revalidation_required",
                  "replacement_or_retirement_candidate", "evidence_needed", "false_positive_cost", "false_negative_cost"):
            if k not in n:
                e.append(f"impact_radius[{i}].{k} required")
        if n.get("propagation_state") not in PROPAGATION_STATES:
            e.append(f"impact_radius[{i}] invalid propagation_state")
        if n.get("propagation_state") == "POTENTIAL_PROPAGATION" and not n.get("revalidation_required"):
            e.append(f"impact_radius[{i}] potential propagation must require revalidation")

    if record.get("claim_allowed") is not False:
        e.append("component lifecycle ledger is assurance evidence only; claim_allowed must remain false")
    for k in ("component_id", "observed_at", "source_pointer", "owner_authority", "next_review_gate", "retirement_or_revalidation_criteria"):
        if not nonempty(record.get(k)):
            e.append(f"{k} must be non-empty")
    return e


def report(record: dict[str, Any]) -> dict[str, Any]:
    errors = validate(record)
    tv = [k for k, v in (record.get("lifecycle_clocks") or {}).items() if isinstance(v, dict) and v.get("state") == "TOKEN_VAZIO"]
    reval = [n.get("component") for n in (record.get("impact_radius") or []) if isinstance(n, dict) and n.get("revalidation_required")]
    return {
        "schema_version": "rafaelia.component-lifecycle-assurance-report/v1",
        "component_id": record.get("component_id"),
        "valid": not errors,
        "errors": errors,
        "token_vazio_clocks": sorted(tv),
        "revalidation_required": sorted(x for x in reval if x),
        "claim_allowed": False,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("record")
    p.add_argument("--write-report")
    a = p.parse_args()
    r = json.loads(Path(a.record).read_text(encoding="utf-8"))
    out = report(r)
    payload = json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if a.write_report:
        Path(a.write_report).write_text(payload, encoding="utf-8")
    sys.stdout.write(payload)
    return 0 if out["valid"] else 2


if __name__ == "__main__":
    sys.exit(main())
