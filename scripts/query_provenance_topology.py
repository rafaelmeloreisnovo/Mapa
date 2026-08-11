#!/usr/bin/env python3
import argparse
import json
from collections import deque
from pathlib import Path

DEFAULT = "data/governance/provenance_topology.v1.json"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def compact(node):
    v = node["vector"]
    return {
        "id": node["id"],
        "kind": node["kind"],
        "state": node["state"],
        "gate": v["gate"],
        "time": v["time"],
        "identity": v["identity"],
        "evidence": v["evidence"],
        "execution": v["execution"],
        "receipt": v["receipt"],
        "title": node["title"],
        "next_verifiable_step": node["next_verifiable_step"],
    }


def traverse(data, start, direction, max_depth):
    by_id = {n["id"]: n for n in data["nodes"]}
    adj = {}
    for edge in data["edges"]:
        src, dst = edge["from"], edge["to"]
        a, b = (src, dst) if direction == "out" else (dst, src)
        adj.setdefault(a, []).append((b, edge["type"]))

    if start not in by_id:
        raise SystemExit(f"unknown node: {start}")

    out = []
    q = deque([(start, 0)])
    seen = {start}
    while q:
        current, depth = q.popleft()
        if depth >= max_depth:
            continue
        for nxt, typ in sorted(adj.get(current, [])):
            out.append({"depth": depth + 1, "from": current, "to": nxt, "type": typ})
            if nxt not in seen:
                seen.add(nxt)
                q.append((nxt, depth + 1))
    return out


def main():
    ap = argparse.ArgumentParser(description="Query RAFAELIA provenance topology without inferring missing evidence.")
    ap.add_argument("--file", default=DEFAULT)
    ap.add_argument("--id")
    ap.add_argument("--kind")
    ap.add_argument("--state")
    ap.add_argument("--gate")
    ap.add_argument("--time")
    ap.add_argument("--token-vazio", action="store_true")
    ap.add_argument("--traverse", choices=["in", "out"])
    ap.add_argument("--depth", type=int, default=3)
    args = ap.parse_args()

    data = load(args.file)
    nodes = data["nodes"]

    if args.id and args.traverse:
        print(json.dumps(traverse(data, args.id, args.traverse, args.depth), ensure_ascii=False, indent=2))
        return

    selected = []
    for node in nodes:
        v = node["vector"]
        if args.id and node["id"] != args.id:
            continue
        if args.kind and node["kind"] != args.kind:
            continue
        if args.state and node["state"] != args.state:
            continue
        if args.gate and v["gate"] != args.gate:
            continue
        if args.time and v["time"] != args.time:
            continue
        if args.token_vazio and not (node["state"] == "TOKEN_VAZIO" or "TOKEN_VAZIO" in v.values()):
            continue
        selected.append(compact(node))

    print(json.dumps(selected, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
