#!/usr/bin/env python3
"""Dependency-free preflight for RAFAELIA orchestrator contracts.

This script intentionally does not claim full JSON Schema validation. It proves
that schemas and canonical fixtures parse, that high-value identifiers conform,
and that Product Graph edges reference existing nodes. Full draft-2020-12
validation remains a separate gate.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "orquestrador" / "contracts"
FIXTURES = ROOT / "orquestrador" / "fixtures"

MODULE_ID_RE = re.compile(r"^MOD-[A-Z0-9][A-Z0-9_-]{2,127}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
TOKEN_REF_RE = re.compile(r"^TOKEN_VAZIO_[A-Z0-9_]+$")
PRODUCT_ID_RE = re.compile(r"^PDT-[0-9]{2,4}$")


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, name: str, detail: str, checks: list[Check]) -> None:
    checks.append(Check(name=name, ok=condition, detail=detail))


def validate_schema_documents(checks: list[Check]) -> None:
    expected = {
        "module_registry.schema.json": "https://json-schema.org/draft/2020-12/schema",
        "event_envelope.schema.json": "https://json-schema.org/draft/2020-12/schema",
        "product_graph.schema.json": "https://json-schema.org/draft/2020-12/schema",
    }
    for filename, draft in expected.items():
        path = CONTRACTS / filename
        try:
            document = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            require(False, f"schema:{filename}:parse", str(exc), checks)
            continue
        require(document.get("$schema") == draft, f"schema:{filename}:draft", f"$schema={document.get('$schema')!r}", checks)
        require(bool(document.get("$id")), f"schema:{filename}:id", "$id must be non-empty", checks)
        require(document.get("additionalProperties") is False, f"schema:{filename}:closed", "top-level additionalProperties must be false", checks)


def validate_module_fixture(checks: list[Check]) -> None:
    path = FIXTURES / "module_registry.valid.json"
    data = load_json(path)
    require(data.get("schema") == "rafaelia.module-registry.v1", "module:schema", str(data.get("schema")), checks)
    require(data.get("claim_allowed") is False, "module:claim_allowed", "must remain false at registry level", checks)

    modules = data.get("modules")
    require(isinstance(modules, list) and bool(modules), "module:items", "modules must be a non-empty array", checks)
    if not isinstance(modules, list):
        return

    seen: set[str] = set()
    for index, module in enumerate(modules):
        module_id = module.get("module_id", "")
        require(bool(MODULE_ID_RE.fullmatch(module_id)), f"module:{index}:id", module_id, checks)
        require(module_id not in seen, f"module:{index}:unique", module_id, checks)
        seen.add(module_id)

        observed_ref = module.get("observed_ref", "")
        ref_ok = bool(COMMIT_RE.fullmatch(observed_ref) or TOKEN_REF_RE.fullmatch(observed_ref))
        require(ref_ok, f"module:{module_id}:observed_ref", observed_ref, checks)

        repository = module.get("repository", "")
        require(repository.count("/") == 1 and " " not in repository, f"module:{module_id}:repository", repository, checks)

        capabilities = module.get("capabilities", [])
        require(isinstance(capabilities, list) and len(capabilities) == len(set(capabilities)), f"module:{module_id}:capabilities", "capabilities must be unique", checks)

        for product_id in module.get("product_ids", []):
            require(bool(PRODUCT_ID_RE.fullmatch(product_id)), f"module:{module_id}:product:{product_id}", product_id, checks)

        require(bool(module.get("safe_state")), f"module:{module_id}:safe_state", "safe_state required", checks)
        require(bool(module.get("rollback")), f"module:{module_id}:rollback", "rollback or TOKEN_VAZIO reason required", checks)
        require(bool(module.get("next_action")), f"module:{module_id}:next_action", "next_action required", checks)


def validate_event_fixture(checks: list[Check]) -> None:
    path = FIXTURES / "event_envelope.valid.json"
    event = load_json(path)
    require(event.get("schema") == "rafaelia.event.v1", "event:schema", str(event.get("schema")), checks)
    require(str(event.get("event_id", "")).startswith("EVT-"), "event:event_id", str(event.get("event_id")), checks)
    require(str(event.get("run_id", "")).startswith("RUN-"), "event:run_id", str(event.get("run_id")), checks)
    require(str(event.get("trace_id", "")).startswith("TRACE-"), "event:trace_id", str(event.get("trace_id")), checks)
    require(bool(MODULE_ID_RE.fullmatch(event.get("source_module", ""))), "event:source_module", str(event.get("source_module")), checks)

    observed_ref = event.get("source_commit", "")
    ref_ok = bool(COMMIT_RE.fullmatch(observed_ref) or TOKEN_REF_RE.fullmatch(observed_ref) or observed_ref == "NOT_APPLICABLE")
    require(ref_ok, "event:source_commit", str(observed_ref), checks)

    gaps = event.get("token_vazio", [])
    require(isinstance(gaps, list), "event:token_vazio:type", "must be an array", checks)
    if isinstance(gaps, list):
        for index, gap in enumerate(gaps):
            required = {"gap_id", "field", "reason", "context_preserved", "next_verifiable_step"}
            missing = sorted(required.difference(gap)) if isinstance(gap, dict) else sorted(required)
            require(not missing, f"event:gap:{index}", f"missing={missing}", checks)

    r3 = event.get("r3", {})
    require(all(bool(r3.get(key)) for key in ("F_ok", "F_gap", "F_next")), "event:r3", "F_ok, F_gap and F_next required", checks)

    if event.get("status") == "PASS":
        require(not gaps, "event:pass_without_gaps", "PASS cannot retain unresolved token_vazio gaps", checks)


def validate_product_graph_fixture(checks: list[Check]) -> None:
    path = FIXTURES / "product_graph.valid.json"
    graph = load_json(path)
    require(graph.get("schema") == "rafaelia.product-graph.v1", "graph:schema", str(graph.get("schema")), checks)

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    require(isinstance(nodes, list) and bool(nodes), "graph:nodes", "nodes must be non-empty", checks)
    require(isinstance(edges, list), "graph:edges", "edges must be an array", checks)
    if not isinstance(nodes, list) or not isinstance(edges, list):
        return

    node_ids: list[str] = [str(node.get("id", "")) for node in nodes if isinstance(node, dict)]
    require(len(node_ids) == len(set(node_ids)), "graph:node_ids_unique", f"count={len(node_ids)}", checks)
    known = set(node_ids)

    edge_ids: set[str] = set()
    for index, edge in enumerate(edges):
        edge_id = str(edge.get("edge_id", ""))
        require(bool(edge_id), f"graph:edge:{index}:id", edge_id, checks)
        require(edge_id not in edge_ids, f"graph:edge:{index}:unique", edge_id, checks)
        edge_ids.add(edge_id)
        require(edge.get("from") in known, f"graph:edge:{edge_id}:from", str(edge.get("from")), checks)
        require(edge.get("to") in known, f"graph:edge:{edge_id}:to", str(edge.get("to")), checks)
        require(edge.get("direction") == "directed", f"graph:edge:{edge_id}:direction", str(edge.get("direction")), checks)
        strength = edge.get("strength")
        require(isinstance(strength, (int, float)) and 0 <= strength <= 1, f"graph:edge:{edge_id}:strength", str(strength), checks)
        if edge.get("state") == "TOKEN_VAZIO":
            require(bool(edge.get("next_verifiable_step")), f"graph:edge:{edge_id}:next", "TOKEN_VAZIO edge needs next step", checks)


def main() -> int:
    checks: list[Check] = []
    try:
        validate_schema_documents(checks)
        validate_module_fixture(checks)
        validate_event_fixture(checks)
        validate_product_graph_fixture(checks)
    except (OSError, json.JSONDecodeError, TypeError, AttributeError) as exc:
        checks.append(Check(name="preflight:exception", ok=False, detail=f"{type(exc).__name__}: {exc}"))

    failed = [check for check in checks if not check.ok]
    report = {
        "schema": "rafaelia.orchestrator-preflight.v1",
        "status": "PASS" if not failed else "FAIL",
        "checks_total": len(checks),
        "checks_failed": len(failed),
        "limitations": [
            "This is a dependency-free structural preflight, not full JSON Schema draft-2020-12 validation.",
            "No Android, Termux, VM, network or cross-repository runtime is executed."
        ],
        "checks": [asdict(check) for check in checks]
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
