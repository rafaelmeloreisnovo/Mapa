#!/usr/bin/env python3
"""Build deterministic D-dimensional amplifier fixtures without external dependencies."""

from __future__ import annotations
import heapq
import json
import itertools
import pathlib
import sys
from typing import Any

MAX_RAPPORT_RANK = 16


def require_int(value: Any, name: str, minimum: int, maximum: int) -> int:
    """Validate integer configuration without permissive coercion."""
    if type(value) is not int:
        raise ValueError(f"{name} must be an integer")
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be in [{minimum},{maximum}]")
    return value


def coord_to_node_id(values: tuple[int, int, int, int], dmax: int) -> str:
    """Map a 4-D structural coordinate to the canonical deterministic node id."""
    idx = 0
    for value in values:
        idx = idx * dmax + value
    return f"C-{idx:04d}"


def nearest_neighbors(
    source_coord: tuple[int, int, int, int],
    dmax: int,
    k: int,
) -> list[tuple[int, str]]:
    """Return up to k L1-nearest nodes without scanning the full graph."""
    if k == 0:
        return []

    frontier: list[tuple[int, str, tuple[int, int, int, int]]] = []
    queued = {source_coord}

    def push(coord: tuple[int, int, int, int]) -> None:
        if coord in queued:
            return
        queued.add(coord)
        distance = sum(abs(a - b) for a, b in zip(source_coord, coord))
        heapq.heappush(frontier, (distance, coord_to_node_id(coord, dmax), coord))

    def push_axis_neighbors(coord: tuple[int, int, int, int]) -> None:
        for axis in range(4):
            for step in (-1, 1):
                candidate = list(coord)
                candidate[axis] += step
                if 0 <= candidate[axis] < dmax:
                    push(tuple(candidate))

    push_axis_neighbors(source_coord)
    selected: list[tuple[int, str]] = []
    while frontier and len(selected) < k:
        distance, target, coord = heapq.heappop(frontier)
        selected.append((distance, target))
        push_axis_neighbors(coord)
    return selected


def build_fixture(config: dict[str, Any]) -> dict[str, Any]:
    dmax = require_int(config["arity"], "arity", 1, 7)
    iteration = require_int(config["iteration"], "iteration", 0, 1_000_000)
    k = require_int(config["graph_policy"]["k"], "graph_policy.k", 0, MAX_RAPPORT_RANK)
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
        for rank, (distance, target) in enumerate(
            nearest_neighbors(source_coord, dmax, k), start=1
        ):
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
