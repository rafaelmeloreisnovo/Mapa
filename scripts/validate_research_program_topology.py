#!/usr/bin/env python3
"""Fail-closed validator for the RAFAELIA 7D research-program topology."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ALLOWED_MODULE_STATES = {
    "PROGRAMA_CONJECTURAL",
    "REFUTED_AS_SAME_EQUATION",
    "REFUTED_UNIVERSALITY",
}
ALLOWED_EDGE_TYPES = {
    "derived_from",
    "defines",
    "acts_on",
    "conjectures_equivalence_with",
    "requires_gate",
    "supported_by",
    "contradicted_by",
    "falsified_by",
    "implemented_by",
    "executed_by",
    "reviewed_by",
    "supersedes_state",
    "next_gate",
    "routes_to",
}
REQUIRED_INVARIANTS = {
    "APPEND_ONLY",
    "CLAIM_FAIL_CLOSED",
    "DOMAIN_EXPLICIT",
    "EDGE_TYPED",
    "AXIS_SPECIFIC_GATES",
    "NO_NUMERICAL_PROOF",
    "NO_IP_INFLATION",
    "RECEIPT_BOUND",
    "REVERSIBLE_CHANGES",
    "MEMORY_RETURN",
}
EXPECTED_MODULES = {
    "UTM-194": "PROGRAMA_CONJECTURAL",
    "UTM-198-239": "PROGRAMA_CONJECTURAL",
    "UTM-199-NS": "REFUTED_AS_SAME_EQUATION",
    "UTM-200-YM": "PROGRAMA_CONJECTURAL",
    "UTM-201-HODGE": "PROGRAMA_CONJECTURAL",
    "UTM-203-GOLDBACH": "PROGRAMA_CONJECTURAL",
    "UTM-PNP": "PROGRAMA_CONJECTURAL",
    "UTM-KAM": "REFUTED_UNIVERSALITY",
}


class ValidationError(ValueError):
    """Raised when an epistemic or topological invariant is broken."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate(payload: dict[str, Any]) -> dict[str, int]:
    _require(payload.get("schema_version") == "1.0.0", "schema_version must be 1.0.0")
    _require(
        payload.get("event_id") == "AUDIT-OMEGA-ACCEPTED-7D-TOPOLOGY-V1-20260728",
        "unexpected event_id",
    )

    governance = payload.get("governance")
    _require(isinstance(governance, dict), "governance must be an object")
    _require(governance.get("claim_allowed") is False, "claim_allowed must be false")
    _require(governance.get("append_only") is True, "append_only must be true")
    _require(governance.get("edge_typed") is True, "edge_typed must be true")
    _require(governance.get("axis_specific_gates") is True, "axis_specific_gates must be true")
    _require(governance.get("prior_art_complete") is False, "prior_art_complete must be false")
    _require(governance.get("patent_status") == "TOKEN_VAZIO_IP", "patent status must remain TOKEN_VAZIO_IP")

    modules = payload.get("modules")
    _require(isinstance(modules, list) and len(modules) == 8, "exactly eight affected modules are required")
    module_ids = [m.get("id") for m in modules if isinstance(m, dict)]
    _require(len(module_ids) == 8 and len(set(module_ids)) == 8, "module ids must be unique")
    _require(set(module_ids) == set(EXPECTED_MODULES), "affected module set does not match the accepted audit")
    for module in modules:
        _require(module.get("claim_allowed") is False, f"{module.get('id')}: claim_allowed must be false")
        _require(module.get("current_state") in ALLOWED_MODULE_STATES, f"{module.get('id')}: invalid state")
        _require(module.get("current_state") == EXPECTED_MODULES[module["id"]], f"{module['id']}: incorrect reclassification")
        _require(bool(module.get("gap")), f"{module['id']}: gap is required")
        _require(bool(module.get("source_refs")), f"{module['id']}: source_refs are required")

    rp = payload.get("riemann_program")
    _require(isinstance(rp, dict), "riemann_program must be an object")
    _require(rp.get("module_id") == "UTM-194", "Riemann program must point to UTM-194")
    _require(rp.get("claim_allowed") is False, "Riemann claim must remain closed")
    _require(
        rp.get("identity_target") == "det_reg(H - s(1-s)) = C(s) xi(s)",
        "identity target changed",
    )
    gates = rp.get("gates")
    _require(isinstance(gates, list) and len(gates) == 11, "R0..R10 are required")
    expected_gate_ids = [f"R{i}" for i in range(11)]
    _require([g.get("id") for g in gates] == expected_gate_ids, "gates must be ordered R0..R10")
    for idx, gate in enumerate(gates):
        _require(gate.get("claim_allowed") is False, f"{gate.get('id')}: claim_allowed must be false")
        expected_next = f"R{idx + 1}" if idx < 10 else None
        _require(gate.get("next") == expected_next, f"{gate.get('id')}: invalid next gate")
        _require(gate.get("state") in {"DEFINED", "TOKEN_VAZIO"}, f"{gate.get('id')}: invalid state")

    nodes = payload.get("nodes")
    _require(isinstance(nodes, list) and nodes, "nodes are required")
    node_ids = [n.get("id") for n in nodes if isinstance(n, dict)]
    _require(len(node_ids) == len(nodes) and len(set(node_ids)) == len(node_ids), "node ids must be unique")
    _require(all(n.get("claim_allowed") is False for n in nodes), "all nodes must be fail-closed")
    node_set = set(node_ids)

    edges = payload.get("edges")
    _require(isinstance(edges, list) and edges, "edges are required")
    edge_ids = [e.get("id") for e in edges if isinstance(e, dict)]
    _require(len(edge_ids) == len(edges) and len(set(edge_ids)) == len(edge_ids), "edge ids must be unique")
    for edge in edges:
        _require(edge.get("claim_allowed") is False, f"{edge.get('id')}: claim_allowed must be false")
        _require(edge.get("type") in ALLOWED_EDGE_TYPES, f"{edge.get('id')}: untyped/unknown relation")
        _require(edge.get("from") in node_set, f"{edge.get('id')}: missing source node")
        _require(edge.get("to") in node_set, f"{edge.get('id')}: missing target node")

    observed = {(e["from"], e["to"], e["type"]) for e in edges}
    required_gate_edges = {("UTM-194", f"R{i}", "requires_gate") for i in range(11)}
    _require(required_gate_edges <= observed, "UTM-194 must require every R0..R10 gate")
    chain_edges = {(f"R{i}", f"R{i+1}", "next_gate") for i in range(10)}
    _require(chain_edges <= observed, "R0..R10 next_gate chain is incomplete")

    invariants = set(payload.get("invariants", []))
    _require(REQUIRED_INVARIANTS <= invariants, "required invariants are missing")

    authorities = payload.get("authorities")
    _require(isinstance(authorities, list) and len(authorities) >= 6, "six authority boundaries are required")

    return {
        "modules": len(modules),
        "gates": len(gates),
        "nodes": len(nodes),
        "edges": len(edges),
        "claim_allowed_true": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        default="data/sementeira/graphs/formalismo-7d-research-topology.v1.json",
    )
    args = parser.parse_args()
    path = Path(args.path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    summary = validate(payload)
    print("RESEARCH_PROGRAM_TOPOLOGY: PASS")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
