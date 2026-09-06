from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_CONTRACT_IDS = {
    "CONTRACT:PERMANENT_MEMORY",
    "CONTRACT:OMEGA_ACTIVATE",
}
REQUIRED_PROJECTIONS = {
    "PROJECTION:PAPERS",
    "PROJECTION:MATHEMATICA",
    "PROJECTION:CHIPQUANTUM",
    "PROJECTION:RLL",
}
REQUIRED_LANES = {
    "L1_PROVENANCE_AUTHORITY",
    "L2_CODE_RUNTIME",
    "L3_TESTS_FALSIFICATION",
    "L4_PERFORMANCE_MEASUREMENT",
    "L5_CONCURRENCY_RESILIENCE",
    "L6_SEMANTIC_SYNTHESIS",
    "L7_GOVERNANCE_INDEX_RECEIPT",
}


def _load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value must be an object")
    return value


def validate(path: Path) -> dict[str, Any]:
    errors: list[str] = []
    try:
        data = _load(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return {"state": "FAIL", "errors": [str(exc)], "nodes": 0, "edges": 0}

    if data.get("schema") != "rafaelia.omega-dual-contract-execution.v1":
        errors.append("unexpected schema")
    if data.get("append_only") is not True:
        errors.append("append_only must be true")
    if data.get("claim_allowed") is not False:
        errors.append("claim_allowed must remain false")
    if data.get("automatic_merge") is not False:
        errors.append("automatic_merge must remain false")
    if data.get("publication_effect") != "NONE":
        errors.append("publication_effect must be NONE")

    contracts = data.get("contract_types")
    if not isinstance(contracts, list):
        errors.append("contract_types must be a list")
        contract_ids: set[str] = set()
    else:
        contract_ids = {item.get("id") for item in contracts if isinstance(item, dict)}
        if contract_ids != REQUIRED_CONTRACT_IDS:
            errors.append("dual contract identities are incomplete or changed")
        for item in contracts:
            authority = item.get("authority") if isinstance(item, dict) else None
            if not isinstance(authority, dict) or not all(
                isinstance(authority.get(key), str) and authority[key]
                for key in ("repository", "path", "blob_sha")
            ):
                errors.append("contract authority must pin repository, path, and blob_sha")

    projections = data.get("domain_projections")
    if not isinstance(projections, list):
        errors.append("domain_projections must be a list")
    else:
        ids = {item.get("id") for item in projections if isinstance(item, dict)}
        if ids != REQUIRED_PROJECTIONS:
            errors.append("domain projections are incomplete or changed")

    lanes = data.get("technical_lanes")
    if not isinstance(lanes, list):
        errors.append("technical_lanes must be a list")
    else:
        lane_ids = {item.get("id") for item in lanes if isinstance(item, dict)}
        if lane_ids != REQUIRED_LANES:
            errors.append("all seven orchestration lanes must be explicit")

    graph = data.get("graph")
    if not isinstance(graph, dict):
        errors.append("graph must be an object")
        nodes: list[Any] = []
        edges: list[Any] = []
    else:
        nodes = graph.get("nodes") if isinstance(graph.get("nodes"), list) else []
        edges = graph.get("edges") if isinstance(graph.get("edges"), list) else []

    node_ids = [node.get("id") for node in nodes if isinstance(node, dict)]
    if len(node_ids) != len(nodes) or any(not isinstance(node_id, str) or not node_id for node_id in node_ids):
        errors.append("every graph node needs a non-empty id")
    if len(set(node_ids)) != len(node_ids):
        errors.append("duplicate graph node id")
    node_set = set(node_ids)

    edge_ids: list[str] = []
    degree = {node_id: 0 for node_id in node_set}
    for edge in edges:
        if not isinstance(edge, dict):
            errors.append("graph edge must be an object")
            continue
        edge_id = edge.get("id")
        if not isinstance(edge_id, str) or not edge_id:
            errors.append("every graph edge needs a non-empty id")
        else:
            edge_ids.append(edge_id)
        source = edge.get("source")
        target = edge.get("target")
        relation = edge.get("type")
        evidence_state = edge.get("evidence_state")
        if source not in node_set or target not in node_set:
            errors.append(f"edge {edge_id!r} has an undefined endpoint")
            continue
        if source == target:
            errors.append(f"edge {edge_id!r} is a self-loop")
        if not isinstance(relation, str) or not relation:
            errors.append(f"edge {edge_id!r} has no type")
        if evidence_state != "DOCUMENTED":
            errors.append(f"edge {edge_id!r} lacks DOCUMENTED evidence state")
        degree[source] += 1
        degree[target] += 1

    if len(set(edge_ids)) != len(edge_ids):
        errors.append("duplicate graph edge id")
    isolated = sorted(node_id for node_id, count in degree.items() if count == 0)
    if isolated:
        errors.append("isolated graph node(s): " + ", ".join(isolated))

    boundaries = data.get("boundaries")
    if not isinstance(boundaries, list) or "branch write != merge != main" not in boundaries:
        errors.append("branch/merge/main boundary is required")
    r3 = data.get("R3")
    if not isinstance(r3, dict) or not all(isinstance(r3.get(key), list) and r3[key] for key in ("F_ok", "F_gap", "F_next")):
        errors.append("R3 must contain non-empty F_ok, F_gap, and F_next lists")

    return {
        "state": "PASS" if not errors else "FAIL",
        "errors": errors,
        "nodes": len(nodes),
        "edges": len(edges),
        "isolated_nodes": isolated,
    }


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "data/governance/OMEGA_DUAL_CONTRACT_EXECUTION_20260906.v1.json"
    )
    result = validate(target)
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["state"] == "PASS" else 1)
