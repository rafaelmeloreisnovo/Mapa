#!/usr/bin/env python3
"""Dependency-free structural validator for the RAFAELIA Procedure Ledger.

This validator checks high-value orchestration invariants without claiming full
JSON Schema draft-2020-12 validation. It verifies identity, dependencies,
acyclic ordering, temporal honesty, TOKEN_VAZIO structure and evidence required
for terminal success states.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = ROOT / "orquestrador" / "fixtures" / "procedure_ledger.valid.json"
SCHEMA_PATH = ROOT / "orquestrador" / "contracts" / "procedure_ledger.schema.json"

PROC_ID_RE = re.compile(r"^PROC-[A-Z0-9][A-Z0-9_-]{2,127}$")
VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
RUN_ID_RE = re.compile(r"^RUN-[A-Za-z0-9._:-]{8,200}$")
TERMINAL_SUCCESS = {"PASS", "PASS_LIMITED"}
PLANNING_STATES = {"DRAFT", "DECLARED", "READY", "BLOCKED", "TOKEN_VAZIO"}


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def add(checks: list[Check], name: str, ok: bool, detail: str) -> None:
    checks.append(Check(name=name, ok=ok, detail=detail))


def detect_cycle(graph: dict[str, list[str]]) -> list[str] | None:
    WHITE, GRAY, BLACK = 0, 1, 2
    state = {node: WHITE for node in graph}
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        state[node] = GRAY
        stack.append(node)
        for dependency in graph[node]:
            if dependency not in graph:
                continue
            if state[dependency] == WHITE:
                cycle = visit(dependency)
                if cycle:
                    return cycle
            elif state[dependency] == GRAY:
                start = stack.index(dependency)
                return stack[start:] + [dependency]
        stack.pop()
        state[node] = BLACK
        return None

    for node in graph:
        if state[node] == WHITE:
            cycle = visit(node)
            if cycle:
                return cycle
    return None


def validate_schema(checks: list[Check]) -> None:
    schema = load_json(SCHEMA_PATH)
    add(checks, "schema:draft", schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", str(schema.get("$schema")))
    add(checks, "schema:id", bool(schema.get("$id")), str(schema.get("$id")))
    add(checks, "schema:closed", schema.get("additionalProperties") is False, "top-level additionalProperties must be false")


def validate_ledger(path: Path, checks: list[Check]) -> None:
    ledger = load_json(path)
    add(checks, "ledger:schema", ledger.get("schema") == "rafaelia.procedure-ledger.v1", str(ledger.get("schema")))
    add(checks, "ledger:claim_allowed", ledger.get("claim_allowed") is False, "claim_allowed must remain false")

    procedures = ledger.get("procedures")
    add(checks, "ledger:procedures", isinstance(procedures, list) and bool(procedures), "procedures must be a non-empty array")
    if not isinstance(procedures, list):
        return

    ids: list[str] = []
    versions: set[tuple[str, str]] = set()
    graph: dict[str, list[str]] = {}

    for index, procedure in enumerate(procedures):
        if not isinstance(procedure, dict):
            add(checks, f"procedure:{index}:object", False, "procedure must be an object")
            continue

        proc_id = str(procedure.get("proc_id", ""))
        version = str(procedure.get("version", ""))
        add(checks, f"procedure:{index}:id", bool(PROC_ID_RE.fullmatch(proc_id)), proc_id)
        add(checks, f"procedure:{proc_id}:version", bool(VERSION_RE.fullmatch(version)), version)
        add(checks, f"procedure:{proc_id}:identity_unique", (proc_id, version) not in versions, f"{proc_id}@{version}")
        versions.add((proc_id, version))
        ids.append(proc_id)

        dependencies = procedure.get("depends_on", [])
        add(checks, f"procedure:{proc_id}:depends_type", isinstance(dependencies, list), str(type(dependencies).__name__))
        if not isinstance(dependencies, list):
            dependencies = []
        add(checks, f"procedure:{proc_id}:no_self_dependency", proc_id not in dependencies, str(dependencies))
        graph[proc_id] = [str(item) for item in dependencies]

        timing_mode = procedure.get("timing_mode")
        if dependencies:
            add(checks, f"procedure:{proc_id}:dependency_timing", timing_mode in {"AFTER_GATE", "WHEN_CONDITION", "BLOCKED", "MANUAL_DECISION"}, str(timing_mode))

        steps = procedure.get("steps", [])
        add(checks, f"procedure:{proc_id}:steps", isinstance(steps, list) and bool(steps), "at least one finite step required")
        if isinstance(steps, list):
            orders = [step.get("order") for step in steps if isinstance(step, dict)]
            add(checks, f"procedure:{proc_id}:step_orders_unique", len(orders) == len(set(orders)), str(orders))
            add(checks, f"procedure:{proc_id}:step_orders_positive", all(isinstance(order, int) and order > 0 for order in orders), str(orders))

        current_state = procedure.get("current_state")
        run_ids = procedure.get("run_ids", [])
        evidence_refs = procedure.get("evidence_refs", [])
        artifact_refs = procedure.get("artifact_refs", [])
        if current_state in TERMINAL_SUCCESS:
            add(checks, f"procedure:{proc_id}:success_run", isinstance(run_ids, list) and bool(run_ids), "success requires at least one RUN_ID")
            add(checks, f"procedure:{proc_id}:success_evidence", bool(evidence_refs or artifact_refs), "success requires evidence or artifacts")
        if isinstance(run_ids, list):
            for run_id in run_ids:
                add(checks, f"procedure:{proc_id}:run:{run_id}", bool(RUN_ID_RE.fullmatch(str(run_id))), str(run_id))

        gaps = procedure.get("token_vazio", [])
        add(checks, f"procedure:{proc_id}:gaps_type", isinstance(gaps, list), str(type(gaps).__name__))
        if isinstance(gaps, list):
            for gap_index, gap in enumerate(gaps):
                required = {"gap_id", "field", "reason", "context_preserved", "next_verifiable_step"}
                missing = sorted(required.difference(gap)) if isinstance(gap, dict) else sorted(required)
                add(checks, f"procedure:{proc_id}:gap:{gap_index}", not missing, f"missing={missing}")

        r3 = procedure.get("r3", {})
        add(checks, f"procedure:{proc_id}:r3", isinstance(r3, dict) and all(bool(r3.get(key)) for key in ("F_ok", "F_gap", "F_next")), "F_ok, F_gap and F_next required")

        if current_state in PLANNING_STATES:
            add(checks, f"procedure:{proc_id}:planning_not_executed", not run_ids or current_state == "TOKEN_VAZIO", f"state={current_state}, run_ids={run_ids}")

    known = set(ids)
    add(checks, "ledger:procedure_ids_unique", len(ids) == len(known), f"count={len(ids)}, unique={len(known)}")
    for proc_id, dependencies in graph.items():
        for dependency in dependencies:
            add(checks, f"procedure:{proc_id}:dependency:{dependency}", dependency in known, dependency)

    cycle = detect_cycle(graph)
    add(checks, "ledger:dependency_acyclic", cycle is None, "none" if cycle is None else " -> ".join(cycle))


def main() -> int:
    ledger_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_LEDGER
    checks: list[Check] = []
    try:
        validate_schema(checks)
        validate_ledger(ledger_path, checks)
    except (OSError, json.JSONDecodeError, TypeError, AttributeError, ValueError) as exc:
        checks.append(Check(name="validator:exception", ok=False, detail=f"{type(exc).__name__}: {exc}"))

    failed = [check for check in checks if not check.ok]
    report = {
        "schema": "rafaelia.procedure-ledger-preflight.v1",
        "ledger": str(ledger_path),
        "status": "PASS" if not failed else "FAIL",
        "checks_total": len(checks),
        "checks_failed": len(failed),
        "limitations": [
            "This is a dependency-free structural validator, not full JSON Schema draft-2020-12 validation.",
            "No procedure, command, CI workflow, Android runtime, Termux job or VM is executed."
        ],
        "checks": [asdict(check) for check in checks]
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
