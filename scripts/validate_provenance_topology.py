#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

NODE_ID = re.compile(r"^[A-Z][A-Z0-9_-]{2,}$")
SIGIL = re.compile(r"^ΣΩΔΦ::[A-Z0-9_-]+$")
AXES = ["source", "identity", "claim", "evidence", "execution", "receipt", "gate", "time"]


def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    return 1


def has_token_vazio(vector):
    return any(v == "TOKEN_VAZIO" for v in vector.values())


def main(path):
    p = Path(path)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"cannot parse {p}: {exc}")

    if data.get("schema_version") != "1.0.0":
        return fail("schema_version must be 1.0.0")
    if data.get("claim_allowed") is not False:
        return fail("claim_allowed must remain false")
    if data.get("vector_axes") != AXES:
        return fail(f"vector_axes must equal {AXES}")

    nodes = data.get("nodes")
    edges = data.get("edges")
    if not isinstance(nodes, list) or not nodes:
        return fail("nodes must be a non-empty list")
    if not isinstance(edges, list):
        return fail("edges must be a list")

    by_id = {}
    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            return fail(f"nodes[{i}] is not an object")
        nid = node.get("id", "")
        if not NODE_ID.fullmatch(nid):
            return fail(f"invalid node id at index {i}: {nid!r}")
        if nid in by_id:
            return fail(f"duplicate node id: {nid}")
        by_id[nid] = node

        if node.get("claim_allowed") is not False:
            return fail(f"{nid}: claim_allowed must remain false")
        if node.get("sigil") != f"ΣΩΔΦ::{nid}":
            return fail(f"{nid}: sigil must be symbolic label ΣΩΔΦ::<node-id>")
        if not SIGIL.fullmatch(node["sigil"]):
            return fail(f"{nid}: invalid sigil syntax")

        vector = node.get("vector")
        if not isinstance(vector, dict) or list(vector.keys()) != AXES:
            return fail(f"{nid}: vector must contain axes in canonical order {AXES}")

        anchor = node.get("anchor")
        if not isinstance(anchor, dict) or not anchor.get("provider"):
            return fail(f"{nid}: anchor.provider is required")

        state = node.get("state")
        gate = vector.get("gate")
        time = vector.get("time")

        if time == "FUTURE_PLANNED" and gate == "F_OK":
            return fail(f"{nid}: future plan cannot be F_OK")
        if state == "PLANNED_FUTURE" and vector.get("execution") == "EXECUTED":
            return fail(f"{nid}: PLANNED_FUTURE cannot claim EXECUTED")

        if gate == "F_OK":
            if vector.get("identity") != "BOUND":
                return fail(f"{nid}: F_OK requires identity=BOUND")
            if vector.get("evidence") not in {"EXECUTED", "REPRODUCED"}:
                return fail(f"{nid}: F_OK requires executed/reproduced evidence")
            if vector.get("execution") not in {"EXECUTED", "NOT_APPLICABLE"}:
                return fail(f"{nid}: F_OK requires execution evidence or NOT_APPLICABLE")
            if vector.get("receipt") not in {"PRESENT", "NOT_APPLICABLE"}:
                return fail(f"{nid}: F_OK requires receipt PRESENT/NOT_APPLICABLE")
            if has_token_vazio(vector):
                return fail(f"{nid}: F_OK cannot contain TOKEN_VAZIO")
            if time in {"FUTURE_PLANNED", "TOKEN_VAZIO"}:
                return fail(f"{nid}: F_OK requires observed/past-recorded time")

        if state == "CLOSED" and gate != "F_OK":
            return fail(f"{nid}: CLOSED requires gate=F_OK")

    seen_edges = set()
    for i, edge in enumerate(edges):
        if not isinstance(edge, dict):
            return fail(f"edges[{i}] is not an object")
        src, dst, typ = edge.get("from"), edge.get("to"), edge.get("type")
        if src not in by_id or dst not in by_id:
            return fail(f"edges[{i}]: dangling endpoint {src!r}->{dst!r}")
        key = (src, dst, typ)
        if key in seen_edges:
            return fail(f"duplicate edge: {key}")
        seen_edges.add(key)

    expected = {
        "nodes": len(nodes),
        "edges": len(edges),
        "f_ok": sum(n["vector"]["gate"] == "F_OK" for n in nodes),
        "token_vazio": sum(
            n.get("state") == "TOKEN_VAZIO" or has_token_vazio(n["vector"])
            for n in nodes
        ),
        "future_planned": sum(n["vector"]["time"] == "FUTURE_PLANNED" for n in nodes),
    }
    if data.get("summary") != expected:
        return fail(f"summary mismatch: got={data.get('summary')} expected={expected}")

    print(
        "PASS: "
        f"{p} nodes={expected['nodes']} edges={expected['edges']} "
        f"F_OK={expected['f_ok']} TOKEN_VAZIO={expected['token_vazio']} "
        f"future_planned={expected['future_planned']} claim_allowed=false"
    )
    return 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "data/governance/provenance_topology.v1.json"
    raise SystemExit(main(target))
