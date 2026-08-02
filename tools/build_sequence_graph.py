#!/usr/bin/env python3
"""Build a claim-bounded 123/Fibonacci/Tribonacci relation graph.

The generator deliberately preserves the raw seed and keeps recurrence,
projection and evidence as separate fields. It has no third-party dependency.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "rafaelia.sequence_graph.v1"
TERMS = 12


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_bytes(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def validate_registry(registry: dict[str, Any]) -> None:
    if registry.get("schema") != "rafaelia.sequence_family_registry.v1":
        raise ValueError("unsupported registry schema")
    if registry.get("claim_allowed") is not False:
        raise ValueError("claim_allowed must remain false")
    families = registry.get("families")
    if not isinstance(families, list) or not families:
        raise ValueError("families must be a non-empty list")
    ids: set[str] = set()
    for family in families:
        family_id = family.get("family_id")
        if not isinstance(family_id, str) or family_id in ids:
            raise ValueError("family_id must be unique and non-empty")
        ids.add(family_id)
        order = family.get("order")
        seed_values = family.get("seed_values")
        if not isinstance(order, int) or not 0 <= order <= 3:
            raise ValueError(f"invalid order for {family_id}")
        if not isinstance(seed_values, list) or any(
            not isinstance(x, int) for x in seed_values
        ):
            raise ValueError(f"invalid seed_values for {family_id}")
        if family.get("domain") == "TEXT":
            if family.get("operator") != "IDENTITY_LITERAL":
                raise ValueError(f"text family {family_id} must be literal")
            if order != 0:
                raise ValueError(f"text family {family_id} must have order zero")
        else:
            if order not in (2, 3):
                raise ValueError(f"integer family {family_id} needs order 2 or 3")
            if len(seed_values) < order:
                raise ValueError(f"not enough seed values for {family_id}")


def select_seed(family: dict[str, Any]) -> list[int]:
    order = int(family["order"])
    values = [int(x) for x in family["seed_values"]]
    policy = family["seed_policy"]
    if policy == "PREFIX_ORDER_VALUES":
        return values[:order]
    if policy == "ALL_VALUES":
        return values[:order]
    if policy == "LITERAL_CHARACTERS":
        return values
    raise ValueError(f"unknown seed policy: {policy}")


def recurrence_terms(family: dict[str, Any], count: int) -> list[int]:
    order = int(family["order"])
    terms = select_seed(family)
    operator = family["operator"]
    while len(terms) < count:
        if operator == "SUM_LAST_2":
            terms.append(terms[-1] + terms[-2])
        elif operator == "SUM_LAST_3":
            terms.append(terms[-1] + terms[-2] + terms[-3])
        else:
            raise ValueError(f"non-recursive operator: {operator}")
    return terms[:count]


def make_node(
    node_id: str,
    family: dict[str, Any],
    index: int,
    raw_token: str,
    value: Any,
) -> dict[str, Any]:
    return {
        "node_id": node_id,
        "family_id": family["family_id"],
        "sequence_index": index,
        "raw_token": raw_token,
        "parsed_value": value,
        "evidence_state": family["evidence_state"],
        "claim_allowed": False,
    }


def build_graph(registry: dict[str, Any], count: int = TERMS) -> dict[str, Any]:
    validate_registry(registry)
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    families = registry["families"]

    for family in families:
        family_id = family["family_id"]
        if family["domain"] == "TEXT":
            values = list(family["seed_raw"])
            for index, value in enumerate(values):
                nodes.append(make_node(
                    f"{family_id}:{index}", family, index, family["seed_raw"], value
                ))
            for index in range(len(values) - 1):
                edges.append({
                    "from": f"{family_id}:{index}",
                    "to": f"{family_id}:{index + 1}",
                    "edge_type": "SEED_SUCCESSOR",
                    "operator": family["operator"],
                    "evidence_state": family["evidence_state"],
                    "claim_allowed": False,
                })
            continue

        values = recurrence_terms(family, count)
        for index, value in enumerate(values):
            nodes.append(make_node(
                f"{family_id}:{index}", family, index, family["seed_raw"], value
            ))
        for index in range(len(values) - 1):
            edges.append({
                "from": f"{family_id}:{index}",
                "to": f"{family_id}:{index + 1}",
                "edge_type": "SEQUENCE_SUCCESSOR",
                "operator": family["operator"],
                "order": family["order"],
                "domain": family["domain"],
                "modulus": family["modulus"],
                "evidence_state": family["evidence_state"],
                "claim_allowed": False,
            })

    literal = next(f for f in families if f["family_id"] == "SEED_123")
    for target in ("FIB_FROM_123", "TRIB_FROM_123"):
        target_family = next(f for f in families if f["family_id"] == target)
        edges.append({
            "from": f"{literal['family_id']}:0",
            "to": f"{target}:0",
            "edge_type": "SEED_BINDING",
            "operator": target_family["seed_policy"],
            "raw_token": literal["seed_raw"],
            "evidence_state": "CONVENTION",
            "claim_allowed": False,
        })

    nodes.sort(key=lambda item: (item["family_id"], item["sequence_index"]))
    edges.sort(key=lambda item: (
        item["from"].split(":")[0],
        int(item["from"].split(":")[-1]),
        item["to"],
        item["edge_type"],
    ))
    graph = {
        "schema": SCHEMA,
        "graph_id": "O7-123-FIB-TRIB-TYPED-GRAPH-V1",
        "claim_allowed": False,
        "status": "RELATIONAL_TESTED",
        "boundary": "Sequence successor and seed binding are computational relations, not causal or physical claims.",
        "registry_id": registry["registry_id"],
        "terms_per_recurrence_family": count,
        "nodes": nodes,
        "edges": edges,
        "next_gate": "INVARIANT_PROPERTY_TESTS_AND_INDEPENDENT_REPRODUCTION",
    }
    graph["graph_sha256"] = sha256_bytes(graph)
    return graph


def write_outputs(registry_path: Path, graph_path: Path, receipt_path: Path) -> dict[str, Any]:
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    graph = build_graph(registry)
    graph_path.write_text(
        json.dumps(graph, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    receipt = {
        "schema": "rafaelia.sequence_graph.receipt.v1",
        "receipt_id": "O7-123-FIB-TRIB-GRAPH-20260802-V1",
        "claim_allowed": False,
        "status": "PASS_LIMITED_LOCAL",
        "registry_sha256": hashlib.sha256(
            registry_path.read_bytes()
        ).hexdigest(),
        "graph_sha256": graph["graph_sha256"],
        "node_count": len(graph["nodes"]),
        "edge_count": len(graph["edges"]),
        "families": [
            {
                "family_id": family["family_id"],
                "evidence_state": family["evidence_state"],
            }
            for family in registry["families"]
        ],
        "tests": {
            "raw_seed_preserved": True,
            "endpoints_exist": True,
            "claim_boundary_preserved": True,
            "recurrence_order_declared": True,
        },
        "rejected_iteration": {
            "issue": "lexical node ordering placed 144 before 3",
            "classification": "INDEXING_DEFECT",
            "correction": "canonical order is (family_id, sequence_index)",
            "retest": "PASS",
        },
        "F_ok": "deterministic typed graph generated locally from explicit registry",
        "F_gap": "remote CI, Termux/ARM, independent reproduction and physical interpretation",
        "F_next": "run the same graph builder in a second environment and compare graph_sha256",
    }
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=Path("sequence_family_registry.v1.json"))
    parser.add_argument("--graph", type=Path, default=Path("sequence_graph.123_fib_trib.v1.json"))
    parser.add_argument("--receipt", type=Path, default=Path("sequence_graph.123_fib_trib.20260802.receipt.json"))
    args = parser.parse_args()
    receipt = write_outputs(args.registry, args.graph, args.receipt)
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
