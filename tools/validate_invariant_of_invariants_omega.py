#!/usr/bin/env python3
"""Fail-closed validator for the RAFAELIA invariant-of-invariants contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


EVIDENCE_WITH_RECEIPT = {"PROVADO", "EVIDENCIADO", "OBSERVADO_LIMITADO"}
ALLOWED_RELATIONS = {
    "GOVERNS",
    "RECONSTRUCTS",
    "CUSTODIES",
    "DERIVES_TO",
    "CATALOGS",
    "ROUTES",
    "NOTIFIES",
    "PERSISTS",
    "RENDERS",
    "PRESENTS",
    "EXECUTES",
    "VALIDATES",
    "FALSIFIES",
    "SUPERSEDES",
    "REFERENCES",
}
ALLOWED_EVIDENCE = {
    "PROVADO",
    "EVIDENCIADO",
    "OBSERVADO_LIMITADO",
    "HIPOTESE",
    "MODELO_ANALOGICO",
    "REFUTADO",
    "TOKEN_VAZIO",
}
REQUIRED_FACTORS = {"ID", "C", "H", "P", "E", "F", "Q", "G", "R", "D"}


def fail(message: str) -> None:
    print(
        json.dumps(
            {"ok": False, "state": "TOKEN_VAZIO", "error": message},
            ensure_ascii=False,
        )
    )
    raise SystemExit(1)


def unique_ids(records: list[dict[str, Any]], field: str, label: str) -> set[str]:
    ids = [record.get(field) for record in records]
    if any(not item for item in ids):
        fail(f"{label} contains empty {field}")
    if len(ids) != len(set(ids)):
        fail(f"{label} contains duplicate {field}")
    return set(ids)


def load_json(path: str) -> dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load JSON: {exc}")
    if not isinstance(value, dict):
        fail("root must be an object")
    return value


def validate(data: dict[str, Any]) -> dict[str, Any]:
    if data.get("schema_version") != "1.0.0":
        fail("schema_version must be 1.0.0")
    if data.get("claim_allowed") is not False:
        fail("claim_allowed must be false")
    if data.get("privacy_default") != "DENY":
        fail("privacy_default must be DENY")

    equation = data.get("core_equation", {})
    if equation.get("zero_rule") != "TOKEN_VAZIO":
        fail("core equation must fail to TOKEN_VAZIO")
    factors = {item.get("factor") for item in data.get("invariants", [])}
    if not REQUIRED_FACTORS.issubset(factors):
        fail("core invariant factors are incomplete")

    surfaces = data.get("surfaces", [])
    surface_ids = unique_ids(surfaces, "id", "surfaces")
    if len(surface_ids) < 8:
        fail("at least eight surfaces are required")
    for surface in surfaces:
        if not surface.get("locator"):
            fail(f"surface {surface.get('id')} has no locator")
        if surface.get("privacy_class") == "P3_PRIVATE_BODY":
            if surface.get("kind") not in {"GOOGLE_DRIVE", "MEMORY", "LIBRARY"}:
                fail(f"private body placed on disallowed surface {surface.get('id')}")

    relations = data.get("relations", [])
    unique_ids(relations, "id", "relations")
    for relation in relations:
        relation_id = relation.get("id")
        if relation.get("from") not in surface_ids or relation.get("to") not in surface_ids:
            fail(f"dangling relation {relation_id}")
        if relation.get("type") not in ALLOWED_RELATIONS:
            fail(f"invalid relation type {relation_id}")
        evidence = relation.get("evidence_state")
        if evidence not in ALLOWED_EVIDENCE:
            fail(f"invalid evidence state {relation_id}")
        if evidence in EVIDENCE_WITH_RECEIPT and not relation.get("receipt_locator"):
            fail(f"evidenced relation without receipt {relation_id}")

    symbols = data.get("symbols", [])
    unique_ids(symbols, "token", "symbols")
    if len(symbols) < 16:
        fail("symbol algebra is incomplete")
    for symbol in symbols:
        if symbol.get("evidence_weight") != 0:
            fail(f"symbol promoted as evidence: {symbol.get('token')}")

    topologies = data.get("topologies", [])
    methodologies = data.get("methodologies", [])
    unique_ids(topologies, "id", "topologies")
    unique_ids(methodologies, "id", "methodologies")
    if len(topologies) < 30:
        fail("at least 30 topologies are required")
    if len(methodologies) < 56:
        fail("at least 56 methodologies are required")

    freshness = data.get("freshness_contract", {})
    if freshness.get("comparison_scope") != "SAME_LOGICAL_IDENTITY":
        fail("freshness may only compare the same logical identity")
    if freshness.get("timestamp_only_forbidden") is not True:
        fail("timestamp-only freshness must be forbidden")
    required_vector = {"logical_id", "provider_revision", "content_hash", "source_family"}
    if not required_vector.issubset(set(freshness.get("vector", []))):
        fail("freshness vector is incomplete")
    if freshness.get("conflict_state") != "TOKEN_VAZIO":
        fail("freshness conflicts must remain TOKEN_VAZIO")

    query = data.get("query_contract", {})
    if query.get("allow_arbitrary_eval") is not False:
        fail("arbitrary query evaluation is forbidden")
    if not 1 <= query.get("max_limit", 0) <= 1000:
        fail("query max_limit must be in 1..1000")
    if not 0 <= query.get("max_depth", -1) <= 16:
        fail("query max_depth must be in 0..16")
    if not 1 <= query.get("timeout_ms", 0) <= 60000:
        fail("query timeout must be in 1..60000 ms")

    latencies = data.get("latency_receipts", [])
    unique_ids(latencies, "id", "latency_receipts")
    for latency in latencies:
        if latency.get("classification") not in {
            "MEASURED_CONFOUNDED",
            "MEASURED_ISOLATED",
            "TOKEN_VAZIO",
        }:
            fail(f"invalid latency classification {latency.get('id')}")
        if latency.get("wall_ms", -1) < 0:
            fail(f"negative latency {latency.get('id')}")
        if (
            latency.get("classification") == "MEASURED_CONFOUNDED"
            and latency.get("throughput") != "TOKEN_VAZIO"
        ):
            fail(f"confounded latency promoted to throughput {latency.get('id')}")

    gates = data.get("gates", [])
    unique_ids(gates, "id", "gates")
    if len(gates) < 8:
        fail("execution gates are incomplete")

    gaps = data.get("gaps", [])
    unique_ids(gaps, "id", "gaps")
    for gap in gaps:
        if gap.get("state") != "TOKEN_VAZIO":
            fail(f"gap promoted without evidence {gap.get('id')}")
        if not gap.get("falsifier") or not gap.get("next_gate"):
            fail(f"gap lacks falsifier or next gate {gap.get('id')}")

    return {
        "ok": True,
        "state": "PASS_LOCAL_LIMITED",
        "claim_allowed": False,
        "surfaces": len(surfaces),
        "relations": len(relations),
        "symbols": len(symbols),
        "topologies": len(topologies),
        "methodologies": len(methodologies),
        "latency_receipts": len(latencies),
        "gaps": len(gaps),
    }


def main(path: str) -> None:
    print(json.dumps(validate(load_json(path)), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail("usage: validate_invariant_of_invariants_omega.py ARCHITECTURE.json")
    main(sys.argv[1])
