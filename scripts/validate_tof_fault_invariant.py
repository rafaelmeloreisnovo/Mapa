#!/usr/bin/env python3
"""Deterministic validator for the RAFAELIA TOF fault invariant V1."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "tof-namespace-allocation-fault.v1"
AXES = ["INDEX", "NAME", "BLOCK"]
AXIS_STATES = {"ZERO", "POSITIVE", "NEGATIVE"}
SEMANTIC_STATES = {
    "NORMAL",
    "EMPTY_FILE",
    "PAYLOAD_FAULT",
    "NAME_FAULT",
    "ORPHANED_OBJECT",
    "RESIDUAL_BLOCKS",
    "TOMBSTONE",
    "ABSENT",
    "TOKEN_VAZIO",
}
FAULT_STATES = {
    "GOOD_OBSERVED",
    "CORRECTED",
    "SUSPECT",
    "BAD",
    "REMAPPED",
    "POISONED",
    "ABSENT",
    "TOKEN_VAZIO",
}
COMPOSITE_RE = re.compile(r"^\(I[0+-],N[0+-],B[0+-]\)$")


class ValidationError(ValueError):
    """Raised when a record violates an invariant."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate(record: dict[str, Any]) -> dict[str, Any]:
    require(record.get("schema_version") == SCHEMA_VERSION, "schema_version inválida")
    require(record.get("claim_allowed") is False, "claim_allowed deve permanecer false")

    state = record.get("object_state_model")
    require(isinstance(state, dict), "object_state_model ausente")
    require(state.get("axes") == AXES, "axes devem ser INDEX, NAME, BLOCK")

    axis_states = state.get("axis_states")
    require(isinstance(axis_states, list) and len(axis_states) == 3, "axis_states deve conter 3 estados")
    require(all(item in AXIS_STATES for item in axis_states), "axis_state desconhecido")

    composite = state.get("composite_state")
    require(isinstance(composite, str) and COMPOSITE_RE.fullmatch(composite), "composite_state inválido")
    require(state.get("semantic_state") in SEMANTIC_STATES, "semantic_state desconhecido")

    namespace = record.get("namespace")
    require(isinstance(namespace, dict), "namespace ausente")
    require(isinstance(namespace.get("object_id"), str) and namespace["object_id"], "object_id vazio")
    require(isinstance(namespace.get("logical_size"), int) and namespace["logical_size"] >= 0, "logical_size inválido")
    name_hex = namespace.get("name_hex")
    require(isinstance(name_hex, str) and len(name_hex) % 2 == 0, "name_hex deve conter bytes completos")
    require(re.fullmatch(r"(?:[0-9A-Fa-f]{2})*", name_hex) is not None, "name_hex inválido")

    allocation = record.get("allocation")
    require(isinstance(allocation, dict), "allocation ausente")
    require(isinstance(allocation.get("mapping_epoch"), int) and allocation["mapping_epoch"] >= 0, "mapping_epoch inválido")
    extents = allocation.get("logical_extents")
    require(isinstance(extents, list), "logical_extents deve ser lista")

    semantic_state = state["semantic_state"]
    if semantic_state == "EMPTY_FILE":
        require(namespace["logical_size"] == 0, "EMPTY_FILE exige logical_size=0")
        require(extents == [], "EMPTY_FILE não pode possuir extent alocado")
        require(composite == "(I+,N+,B0)", "EMPTY_FILE exige (I+,N+,B0)")
    if semantic_state == "ABSENT":
        require(composite == "(I0,N0,B0)", "ABSENT exige (I0,N0,B0)")

    fault_overlay = record.get("fault_overlay")
    require(isinstance(fault_overlay, dict), "fault_overlay ausente")
    require(fault_overlay.get("representation") == "SPARSE_APPEND_ONLY", "fault overlay deve ser append-only esparso")
    events = fault_overlay.get("events")
    require(isinstance(events, list), "events deve ser lista")

    event_ids: set[str] = set()
    for event in events:
        require(isinstance(event, dict), "evento inválido")
        event_id = event.get("event_id")
        require(isinstance(event_id, str) and event_id, "event_id vazio")
        require(event_id not in event_ids, f"event_id duplicado: {event_id}")
        event_ids.add(event_id)
        require(event.get("state_after") in FAULT_STATES, f"state_after inválido em {event_id}")
        require(event.get("claim_allowed") is False, f"claim_allowed deve ser false em {event_id}")
        require(isinstance(event.get("block"), int) and event["block"] >= 0, f"block inválido em {event_id}")
        require(isinstance(event.get("epoch"), int) and event["epoch"] >= 0, f"epoch inválido em {event_id}")
        refs = event.get("evidence_refs")
        require(isinstance(refs, list) and refs, f"evidence_refs vazio em {event_id}")

    boundary = record.get("claim_boundary")
    require(isinstance(boundary, dict), "claim_boundary ausente")
    require(boundary.get("implementation_state") in {"TOKEN_VAZIO", "PARTIAL", "VERIFIED_LIMITED"}, "implementation_state inválido")
    require(boundary.get("runtime_evidence") in {"TOKEN_VAZIO", "VERIFIED_LIMITED"}, "runtime_evidence inválido")
    limitations = boundary.get("limitations")
    require(isinstance(limitations, list) and limitations, "limitations não pode ser vazio")

    if boundary.get("runtime_evidence") == "TOKEN_VAZIO":
        require(record["claim_allowed"] is False, "runtime TOKEN_VAZIO bloqueia promoção")

    return {
        "validator": "validate_tof_fault_invariant.v1",
        "record_id": record.get("record_id"),
        "status": "PASS",
        "claim_allowed": False,
        "events": len(events),
        "logical_extents": len(extents),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "record",
        nargs="?",
        default="data/control-plane/tof-namespace-allocation-fault.v1.json",
    )
    parser.add_argument("--write-report")
    args = parser.parse_args()

    try:
        record = json.loads(Path(args.record).read_text(encoding="utf-8"))
        report = validate(record)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1

    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if args.write_report:
        target = Path(args.write_report)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
