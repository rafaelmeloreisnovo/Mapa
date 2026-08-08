#!/usr/bin/env python3
"""Deterministic stdlib validator for RAFAELIA ordinal-memory seed JSONL.

This intentionally validates the operational subset used by the seed without
pretending to be a complete JSON Schema implementation.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

NODE_CLASSES = {"ROOT", "TRUNK", "BRANCH", "NODE", "LEAF", "SEED", "FRUIT"}
STATUSES = {
    "SOURCE_CLAIM", "CANONICAL_DRAFT", "PARTIAL", "PASS", "FAIL", "BLOCKED",
    "TOKEN_VAZIO", "TOKEN_VAZIO_LINEAGE", "TOKEN_VAZIO_METRIC", "CLOSED_PASS",
    "CLOSED_FAIL", "ARCHIVED",
}
TV_STATES = {"OPEN", "TESTABLE", "RUNNING", "CLOSED_PASS", "CLOSED_FAIL", "BLOCKED_EXTERNAL"}
PRIORITIES = {"P0", "P1", "P2", "P3", "P4"}
EDGE_TYPES = {
    "DERIVED_FROM", "DUPLICATES", "ALIASES", "DEPENDS_ON", "SUPPORTS", "FALSIFIES",
    "CONTRADICTS", "REPLACES", "EXECUTED_BY", "PRODUCES", "BLOCKED_BY",
    "CLOSES_TOKEN_VAZIO",
}
QUALITY_KEYS = (
    "provenance", "semantics", "evidence", "reproducibility", "dependency",
    "contradiction", "security", "freshness", "uncertainty", "urgency",
)
REQUIRED = {
    "schema_version", "semantic_id", "ordinal_path", "node_class", "primary_parent",
    "source_refs", "status", "claim_allowed", "vector", "measurement_basis",
    "created_at", "revision",
}
TV_REQUIRED = {
    "token_vazio_id", "reason", "blocked_claims", "missing_object", "expected_evidence",
    "closure_test", "owner_domain", "priority", "state",
}
UNRESOLVED = {"TOKEN_VAZIO", "TOKEN_VAZIO_LINEAGE", "TOKEN_VAZIO_METRIC", "BLOCKED", "PARTIAL"}


def uncertainty(v: dict[str, float]) -> float:
    return (
        0.20 * (1 - v["provenance"])
        + 0.15 * (1 - v["semantics"])
        + 0.25 * (1 - v["evidence"])
        + 0.15 * (1 - v["reproducibility"])
        + 0.10 * v["contradiction"]
        + 0.10 * (1 - v["security"])
        + 0.05 * (1 - v["freshness"])
    )


def validate(path: Path) -> tuple[list[str], dict[str, object]]:
    errors: list[str] = []
    nodes: list[dict[str, object]] = []

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            node = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"L{lineno}: invalid JSON: {exc}")
            continue
        node["__line"] = lineno
        nodes.append(node)

    ids: set[str] = set()
    ordinals: set[tuple[int, ...]] = set()

    for node in nodes:
        line = int(node["__line"])
        missing = REQUIRED - node.keys()
        if missing:
            errors.append(f"L{line}: missing required keys: {sorted(missing)}")
            continue

        if node["schema_version"] != "ordinal-memory-node.v1":
            errors.append(f"L{line}: invalid schema_version")

        sid = node["semantic_id"]
        if not isinstance(sid, str) or len(sid) < 3:
            errors.append(f"L{line}: invalid semantic_id")
        elif sid in ids:
            errors.append(f"L{line}: duplicate semantic_id {sid}")
        else:
            ids.add(sid)

        op = node["ordinal_path"]
        if not (
            isinstance(op, list) and len(op) == 6
            and all(isinstance(x, int) and not isinstance(x, bool) and x >= 0 for x in op)
        ):
            errors.append(f"L{line}: ordinal_path must be 6 non-negative integers")
        else:
            key = tuple(op)
            if key in ordinals:
                errors.append(f"L{line}: duplicate ordinal_path {op}")
            ordinals.add(key)

        if node["node_class"] not in NODE_CLASSES:
            errors.append(f"L{line}: invalid node_class {node['node_class']}")
        if node["status"] not in STATUSES:
            errors.append(f"L{line}: invalid status {node['status']}")
        if not isinstance(node["claim_allowed"], bool):
            errors.append(f"L{line}: claim_allowed must be boolean")
        if node["claim_allowed"] and node["status"] in UNRESOLVED:
            errors.append(f"L{line}: unresolved node cannot have claim_allowed=true")

        refs = node["source_refs"]
        if not isinstance(refs, list) or not refs:
            errors.append(f"L{line}: source_refs must be a non-empty list")

        vector = node["vector"]
        if not isinstance(vector, dict):
            errors.append(f"L{line}: vector must be object")
        else:
            for key in QUALITY_KEYS:
                if key not in vector:
                    errors.append(f"L{line}: vector missing {key}")
                    continue
                value = vector[key]
                if value is None:
                    continue
                if key == "urgency":
                    if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 100:
                        errors.append(f"L{line}: urgency outside 0..100")
                elif not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= 1:
                    errors.append(f"L{line}: {key} outside 0..1")

            base_keys = ("provenance", "semantics", "evidence", "reproducibility", "contradiction", "security", "freshness")
            if all(vector.get(k) is not None for k in base_keys):
                expected = uncertainty(vector)  # type: ignore[arg-type]
                actual = vector.get("uncertainty")
                if actual is None:
                    errors.append(f"L{line}: computable uncertainty must not be null")
                elif not math.isclose(float(actual), expected, abs_tol=1e-9):
                    errors.append(f"L{line}: uncertainty={actual} expected={expected:.12f}")

        tv = node.get("token_vazio")
        if tv is not None:
            if not isinstance(tv, dict):
                errors.append(f"L{line}: token_vazio must be object or null")
            else:
                missing_tv = TV_REQUIRED - tv.keys()
                if missing_tv:
                    errors.append(f"L{line}: token_vazio missing {sorted(missing_tv)}")
                if tv.get("priority") not in PRIORITIES:
                    errors.append(f"L{line}: invalid token_vazio priority")
                if tv.get("state") not in TV_STATES:
                    errors.append(f"L{line}: invalid token_vazio state")
                if tv.get("state") == "CLOSED_PASS" and node["status"] in UNRESOLVED:
                    errors.append(f"L{line}: CLOSED_PASS token cannot remain unresolved without revision")

        for edge in node.get("edges", []):
            if edge.get("type") not in EDGE_TYPES:
                errors.append(f"L{line}: invalid edge type {edge.get('type')}")
            conf = edge.get("confidence")
            if not isinstance(conf, (int, float)) or isinstance(conf, bool) or not 0 <= conf <= 1:
                errors.append(f"L{line}: edge confidence outside 0..1")

    # Graph closure checks after all IDs are known.
    for node in nodes:
        line = int(node["__line"])
        parent = node.get("primary_parent")
        if parent is not None and parent not in ids:
            errors.append(f"L{line}: primary_parent not present in seed: {parent}")
        for edge in node.get("edges", []):
            target = edge.get("target")
            if target not in ids:
                errors.append(f"L{line}: edge target not present in seed: {target}")

    summary = {
        "file": str(path),
        "nodes": len(nodes),
        "unique_semantic_ids": len(ids),
        "unique_ordinal_paths": len(ordinals),
        "token_vazio_nodes": sum(1 for n in nodes if n.get("token_vazio") is not None),
        "claim_allowed_true": sum(1 for n in nodes if n.get("claim_allowed") is True),
        "errors": len(errors),
        "status": "PASS" if not errors else "FAIL",
    }
    return errors, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        default="data/memory/ordinal-memory.seed.v1.jsonl",
        type=Path,
    )
    args = parser.parse_args()
    errors, summary = validate(args.path)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    for error in errors:
        print(error, file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
