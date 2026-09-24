#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

EDGE_RELATIONS = {
    "ROUTES_TO", "INDEXES", "RECONSTRUCTS_FROM", "POINTS_TO", "DEPENDS_ON",
    "EVIDENCES", "GATES", "RECEIPTS", "SUPERSEDES", "ROLLBACK_TO",
    "CONTEXTUALIZES", "RELATES_TO", "EXPANDS_TO", "SOURCE_OF",
    "CROSS_PROVIDER_BRIDGE", "RESOLVES_TO", "VALIDATED_BY",
    "HAS_GAP", "GAP_OF",
}
EDGE_STATES = {
    "OBSERVED_SOURCE", "OBSERVED_SOURCE_ROLE", "OBSERVED_CONCEPTUAL_ROUTE",
    "MATERIALIZED", "OPERATIONAL_ROUTE_DEFINED", "VALIDATED_BOUNDED",
    "TOKEN_VAZIO", "SUPERSEDED",
}
ROUTE_STATES = {"ROUTE_DEFINED", "VALIDATED_BOUNDED", "SUPERSEDED"}

def read_jsonl(path):
    out = []
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{n}: invalid JSON: {exc}")
    return out

def require(obj, keys, ctx):
    missing = [key for key in keys if key not in obj]
    if missing:
        raise SystemExit(f"{ctx}: missing {missing}")

def validate_edges(path):
    rows = read_jsonl(path)
    seen = set()
    for i, obj in enumerate(rows, 1):
        ctx = f"edge[{i}]"
        require(
            obj,
            ["edge_id", "source_id", "relation_type", "target_id", "scope",
             "evidence_ref", "state", "contradiction", "gap"],
            ctx,
        )
        if not re.fullmatch(r"E\d{4,}", obj["edge_id"]):
            raise SystemExit(f"{ctx}: bad edge_id")
        if obj["edge_id"] in seen:
            raise SystemExit(f"{ctx}: duplicate edge_id")
        seen.add(obj["edge_id"])
        if obj["relation_type"] not in EDGE_RELATIONS:
            raise SystemExit(f"{ctx}: bad relation_type")
        if obj["state"] not in EDGE_STATES:
            raise SystemExit(f"{ctx}: bad state")
        for key in ("source_id", "target_id", "scope", "evidence_ref"):
            if not isinstance(obj[key], str) or not obj[key]:
                raise SystemExit(f"{ctx}: empty {key}")
    return len(rows)

def validate_routes(path):
    rows = read_jsonl(path)
    seen = set()
    for i, obj in enumerate(rows, 1):
        ctx = f"route[{i}]"
        require(
            obj,
            ["route_id", "trigger", "path", "minimum_sources",
             "expansion_condition", "evidence_gate", "rollback", "state"],
            ctx,
        )
        if not re.fullmatch(r"R\d{4,}", obj["route_id"]):
            raise SystemExit(f"{ctx}: bad route_id")
        if obj["route_id"] in seen:
            raise SystemExit(f"{ctx}: duplicate route_id")
        seen.add(obj["route_id"])
        if obj["state"] not in ROUTE_STATES:
            raise SystemExit(f"{ctx}: bad state")
        for key in ("trigger", "path", "minimum_sources", "evidence_gate", "rollback"):
            if (
                not isinstance(obj[key], list)
                or not obj[key]
                or not all(isinstance(value, str) and value for value in obj[key])
            ):
                raise SystemExit(f"{ctx}: bad {key}")
    return len(rows)

def validate_gap_edges(edge_path, gap_path):
    edges = read_jsonl(edge_path)
    gaps = read_jsonl(gap_path)
    gap_by_id = {gap["gap_id"]: gap for gap in gaps}

    has_gap = [edge for edge in edges if edge["relation_type"] == "HAS_GAP"]
    gap_of = [edge for edge in edges if edge["relation_type"] == "GAP_OF"]

    seen_gap_bindings = set()
    for edge in has_gap:
        if not edge["target_id"].startswith("gap:"):
            raise SystemExit(f"{edge['edge_id']}: HAS_GAP target must be gap:Gxxxx")
        gid = edge["target_id"].split(":", 1)[1]
        gap = gap_by_id.get(gid)
        if gap is None:
            raise SystemExit(f"{edge['edge_id']}: unknown target gap {gid}")
        if gap["parent_gap_id"] is not None:
            raise SystemExit(f"{edge['edge_id']}: nested gap must use GAP_OF")
        if edge["source_id"] != gap["origin_ref"]:
            raise SystemExit(
                f"{edge['edge_id']}: HAS_GAP source {edge['source_id']} "
                f"!= origin_ref {gap['origin_ref']}"
            )
        if gid in seen_gap_bindings:
            raise SystemExit(f"{edge['edge_id']}: duplicate HAS_GAP for {gid}")
        seen_gap_bindings.add(gid)

    seen_parent_bindings = set()
    for edge in gap_of:
        if not edge["source_id"].startswith("gap:") or not edge["target_id"].startswith("gap:"):
            raise SystemExit(f"{edge['edge_id']}: GAP_OF endpoints must be gap:Gxxxx")
        child_id = edge["source_id"].split(":", 1)[1]
        parent_id = edge["target_id"].split(":", 1)[1]
        child = gap_by_id.get(child_id)
        parent = gap_by_id.get(parent_id)
        if child is None or parent is None:
            raise SystemExit(f"{edge['edge_id']}: GAP_OF references unknown gap")
        if child["parent_gap_id"] != parent_id:
            raise SystemExit(
                f"{edge['edge_id']}: child {child_id} parent "
                f"{child['parent_gap_id']} != {parent_id}"
            )
        if child["origin_ref"] != f"gap:{parent_id}":
            raise SystemExit(
                f"{edge['edge_id']}: child {child_id} origin_ref "
                f"{child['origin_ref']} != gap:{parent_id}"
            )
        if child_id in seen_parent_bindings:
            raise SystemExit(f"{edge['edge_id']}: duplicate GAP_OF for {child_id}")
        seen_parent_bindings.add(child_id)

    expected_top = {gap["gap_id"] for gap in gaps if gap["parent_gap_id"] is None}
    expected_nested = {gap["gap_id"] for gap in gaps if gap["parent_gap_id"] is not None}

    missing_top = sorted(expected_top - seen_gap_bindings)
    missing_nested = sorted(expected_nested - seen_parent_bindings)
    if missing_top:
        raise SystemExit(f"missing HAS_GAP bindings: {missing_top}")
    if missing_nested:
        raise SystemExit(f"missing GAP_OF bindings: {missing_nested}")

    return {
        "has_gap": len(has_gap),
        "gap_of": len(gap_of),
        "bound_gaps": len(seen_gap_bindings) + len(seen_parent_bindings),
    }

def main(argv):
    if len(argv) not in {3, 4}:
        raise SystemExit(
            "usage: validate_manifold_registry.py EDGES.jsonl ROUTES.jsonl [GAPS.jsonl]"
        )
    edge_count = validate_edges(argv[1])
    route_count = validate_routes(argv[2])
    out = {
        "status": "PASS",
        "edges": edge_count,
        "routes": route_count,
        "claim_allowed": False,
    }
    if len(argv) == 4:
        out["gap_subgraph"] = validate_gap_edges(argv[1], argv[3])
    print(json.dumps(out, sort_keys=True))

if __name__ == "__main__":
    main(sys.argv)
