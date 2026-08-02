#!/usr/bin/env python3
"""Build deterministic D-dimensional amplifier fixtures without external dependencies."""

from __future__ import annotations
import json
import itertools
import pathlib
import sys
from typing import Any

def build_fixture(config: dict[str, Any]) -> dict[str, Any]:
    dmax = int(config["arity"])
    iteration = int(config["iteration"])
    k = int(config["graph_policy"]["k"])
    if not 1 <= dmax <= 7:
        raise ValueError("arity must be in [1,7]")
    expected = dmax ** 4
    nodes: list[dict[str, Any]] = []
    coords: dict[str, tuple[int, int, int, int]] = {}
    for idx, values in enumerate(itertools.product(range(dmax), repeat=4)):
        d, v, line, condition = values
        node_id = f"C-{idx:04d}"
        x = (d + 1) / (2 * dmax + 2)
        y = (v + 1) / (2 * dmax + 2)
        z = 1.0 - x - y
        node = {
            "id": node_id,
            "index": {"d": d, "v": v, "l": line, "c": condition},
            "barycentric": {"x": x, "y": y, "z": z},
            "iteration": iteration,
        }
        nodes.append(node)
        coords[node_id] = values

    edges: list[dict[str, Any]] = []
    denom = max(1, 4 * (dmax - 1))
    for node in nodes:
        source = node["id"]
        source_coord = coords[source]
        candidates: list[tuple[int, str]] = []
        for target, target_coord in coords.items():
            if source == target:
                continue
            distance = sum(abs(a - b) for a, b in zip(source_coord, target_coord))
            candidates.append((distance, target))
        candidates.sort(key=lambda item: (item[0], item[1]))
        for rank, (distance, target) in enumerate(candidates[:k], start=1):
            score = round(1.0 - distance / denom, 6)
            edges.append({
                "source": source,
                "target": target,
                "edge_type": "PROXIMITY",
                "score": score,
                "distance": distance,
                "rank": rank,
            })

    if len(nodes) != expected:
        raise AssertionError("cell count mismatch")
    return {
        "schema": "rafaelia.amplifier-generated-fixture.v1",
        "fixture_id": config["fixture_id"],
        "arity": dmax,
        "iteration": iteration,
        "cell_count": len(nodes),
        "graph_policy": config["graph_policy"],
        "nodes": nodes,
        "edges": edges,
        "claim_allowed": False,
    }

def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def main(argv: list[str]) -> int:
    if len(argv) not in {2, 3}:
        print("usage: build_amplifier_fixture.py CONFIG.json [OUTPUT.json]", file=sys.stderr)
        return 2
    config_path = pathlib.Path(argv[1])
    config = json.loads(config_path.read_text(encoding="utf-8"))
    fixture = build_fixture(config)
    output = canonical_json(fixture) + "\n"
    if len(argv) == 3:
        pathlib.Path(argv[2]).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
