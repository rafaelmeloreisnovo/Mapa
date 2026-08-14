#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from datetime import datetime, timezone
from pathlib import Path

HEX = re.compile(r"^[0-9a-f]+$")
HASH_LENGTHS = {"GIT_COMMIT_SHA1": 40, "GIT_BLOB_SHA1": 40, "SHA256_RECEIPT_BODY": 64}
EDGE_TYPES = {"CONTAINS", "EVIDENCED_BY"}

def _parse_utc(value):
    if not isinstance(value, str) or not value.endswith("Z"):
        return None
    try:
        dt = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return None
    return dt if dt.tzinfo == timezone.utc else None

def validate(doc):
    errors = []
    if doc.get("schema") != "RAFAELIA_CROSS_PROVIDER_CHAIN_V1":
        errors.append("schema")
    if doc.get("claim_allowed") is not False:
        errors.append("claim_allowed")
    nodes = doc.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        return errors + ["nodes"]

    ids, providers, by_id = set(), set(), {}
    for i, n in enumerate(nodes):
        p = f"nodes[{i}]"
        for k in ("id","provider","provider_id","hash","observed_at","generator","parent_ids"):
            if k not in n:
                errors.append(f"{p}.{k}")
        nid = n.get("id")
        if not isinstance(nid, str) or not nid:
            errors.append(f"{p}.id")
        elif nid in ids:
            errors.append(f"{p}.duplicate_id")
        else:
            ids.add(nid); by_id[nid] = n
        provider = n.get("provider")
        providers.add(provider)
        if not isinstance(n.get("provider_id"), str) or not n["provider_id"].strip():
            errors.append(f"{p}.provider_id")
        if not isinstance(n.get("generator"), str) or not n["generator"].strip():
            errors.append(f"{p}.generator")
        if _parse_utc(n.get("observed_at")) is None:
            errors.append(f"{p}.observed_at")
        h = n.get("hash")
        if not isinstance(h, dict):
            errors.append(f"{p}.hash")
        else:
            alg, value = h.get("algorithm"), h.get("value")
            if alg not in HASH_LENGTHS:
                errors.append(f"{p}.hash_algorithm")
            elif not isinstance(value, str) or len(value) != HASH_LENGTHS[alg] or not HEX.fullmatch(value):
                errors.append(f"{p}.hash_value")
        if not isinstance(n.get("parent_ids"), list):
            errors.append(f"{p}.parent_ids")

    if not {"GITHUB", "GOOGLE_DRIVE"}.issubset(providers):
        errors.append("cross_provider")

    for i, n in enumerate(nodes):
        child_time = _parse_utc(n.get("observed_at"))
        for parent in n.get("parent_ids", []):
            if parent not in ids:
                errors.append(f"nodes[{i}].parent_missing:{parent}")
            else:
                parent_time = _parse_utc(by_id[parent].get("observed_at"))
                if parent_time and child_time and parent_time > child_time:
                    errors.append(f"nodes[{i}].causal_time:{parent}")

    edges = doc.get("edges")
    if not isinstance(edges, list) or not edges:
        return errors + ["edges"]

    edge_pairs = set()
    adjacency = {nid: [] for nid in ids}
    undirected = {nid: set() for nid in ids}
    has_cross_provider_transition = False
    for i, e in enumerate(edges):
        src, dst, etype = e.get("from"), e.get("to"), e.get("type")
        if src not in ids or dst not in ids:
            errors.append(f"edges[{i}].unknown_node")
            continue
        pair = (src, dst)
        if pair in edge_pairs:
            errors.append(f"edges[{i}].duplicate_edge")
        edge_pairs.add(pair)
        adjacency[src].append(dst)
        undirected[src].add(dst)
        undirected[dst].add(src)
        if by_id[src].get("provider") != by_id[dst].get("provider"):
            has_cross_provider_transition = True
        if etype not in EDGE_TYPES:
            errors.append(f"edges[{i}].type")
        elif etype == "CONTAINS" and by_id[src].get("provider") != by_id[dst].get("provider"):
            errors.append(f"edges[{i}].contains_cross_provider")
        elif etype == "EVIDENCED_BY" and by_id[src].get("provider") == by_id[dst].get("provider"):
            errors.append(f"edges[{i}].evidenced_by_same_provider")
        if src not in by_id[dst].get("parent_ids", []):
            errors.append(f"edges[{i}].parent_mismatch")

    for n in nodes:
        dst = n.get("id")
        for src in n.get("parent_ids", []):
            if src in ids and (src, dst) not in edge_pairs:
                errors.append(f"nodes[{dst}].edge_missing:{src}->{dst}")

    state = {nid: 0 for nid in ids}
    def visit(nid):
        if state[nid] == 1:
            return True
        if state[nid] == 2:
            return False
        state[nid] = 1
        for nxt in adjacency.get(nid, []):
            if visit(nxt):
                return True
        state[nid] = 2
        return False
    if any(visit(nid) for nid in ids if state[nid] == 0):
        errors.append("cycle_detected")

    if ids:
        start = next(iter(ids))
        seen = {start}
        stack = [start]
        while stack:
            cur = stack.pop()
            for nxt in undirected.get(cur, set()):
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        if seen != ids:
            errors.append("disconnected_graph")
    if not has_cross_provider_transition:
        errors.append("no_cross_provider_transition")
    return errors

def main():
    doc = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = validate(doc)
    if errors:
        for e in errors:
            print("REJECT", e)
        return 1
    print("PASS cross-provider-chain-v1")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
