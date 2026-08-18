#!/usr/bin/env python3
"""Audit the canonical RAFAELIA Mapa invariant graph.

The auditor is intentionally stdlib-only and fail-closed. It validates the
registry and typed edges, checks repository-relative references and Git blob
identity, detects dependency cycles/orphans/drift/false promotion, preserves
TOKEN_VAZIO, discovers unregistered invariant-like sources as typed warnings,
and emits a deterministic receipt suitable for CI artifacts.

A PASS receipt proves only that this registry contract was satisfied for the
observed checkout. It is not physical/scientific proof and does not promote any
source invariant by itself.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

RECORD_SCHEMA = "map.invariant/v1"
EDGE_SCHEMA = "map.invariant-edge/v1"
AUDIT_SCHEMA = "map.invariant-audit-receipt/v1"
ID_RE = re.compile(r"^MAP-INV-[A-Z0-9_-]{3,64}$")
EDGE_ID_RE = re.compile(r"^MAP-EDGE-[0-9]{4,}$")
HEX40_RE = re.compile(r"^[0-9a-f]{40}$")
TOKEN_RE = re.compile(r"^TOKEN_VAZIO_[A-Z0-9_]+$")
GATE_RE = re.compile(r"^(PASS|NOT_APPLICABLE|TOKEN_VAZIO_[A-Z0-9_]+)$")
PRIORITIES = ["P0_CRITICAL", "P1_URGENT", "P2_NECESSARY", "P3_IMPORTANT", "P4_BACKLOG"]
FAMILIES = {
    "epistemic", "provenance", "topology", "execution", "context",
    "longitudinal", "federation", "branch", "supply_chain", "scientific",
}
RELATIONS = {
    "requires", "contradicts", "supersedes", "implements",
    "tests", "falsifies", "evidenced_by",
}
VECTOR_KEYS = ("D", "I", "T", "C", "X", "F")
REQUIRED_RECORD = {
    "schema_version", "invariant_id", "version", "family",
    "canonical_statement", "scope", "authority", "source", "validators",
    "tests", "workflows", "receipts", "dependencies", "falsifiers",
    "verification_vector", "urgency", "urgency_reason", "claim_allowed",
    "token_vazio_reason", "next_verifiable_step",
}
REQUIRED_EDGE = {
    "schema_version", "edge_id", "relation", "from", "to",
    "evidence_refs", "claim_allowed",
}
DISCOVERY_RE = re.compile(
    r"INVARIANTS\s*=|required_invariants|\binvariants\s*:|!=|"
    r"not.{0,40}(?:evidence|proof|claim|replication|truth)|"
    r"n[aã]o.{0,40}(?:prova|evid[eê]ncia|equivale|implica)",
    re.IGNORECASE,
)
DISCOVERY_SUFFIXES = {".py", ".md", ".yml", ".yaml", ".json", ".jsonl", ".txt"}


class AuditError(ValueError):
    pass


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def safe_relative(value: str) -> bool:
    if not isinstance(value, str) or not value:
        return False
    p = PurePosixPath(value)
    return not p.is_absolute() and ".." not in p.parts and "\\" not in value


def artifact_path(endpoint: str) -> str | None:
    if isinstance(endpoint, str) and endpoint.startswith("artifact:"):
        return endpoint[len("artifact:"):]
    return None


def load_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return [], [f"cannot read {path}: {exc}"]
    for line_no, raw in enumerate(lines, 1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{line_no}: invalid JSON: {exc.msg}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{path}:{line_no}: object required")
            continue
        rows.append(value)
    if not rows:
        errors.append(f"{path}: no records")
    return rows, errors


def existing_ref(root: Path, ref: str) -> bool:
    return safe_relative(ref) and (root / ref).is_file()


def normalize_statement(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().casefold())


def validate_record(record: dict[str, Any], root: Path, prefix: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    missing = sorted(REQUIRED_RECORD - set(record))
    if missing:
        return [f"{prefix}: missing fields: {', '.join(missing)}"], warnings
    extras = sorted(set(record) - REQUIRED_RECORD)
    if extras:
        errors.append(f"{prefix}: unexpected fields: {', '.join(extras)}")

    iid = record.get("invariant_id")
    if record.get("schema_version") != RECORD_SCHEMA:
        errors.append(f"{prefix}: invalid schema_version")
    if not isinstance(iid, str) or not ID_RE.fullmatch(iid):
        errors.append(f"{prefix}: invalid invariant_id")
    if not isinstance(record.get("version"), int) or isinstance(record.get("version"), bool) or record["version"] < 1:
        errors.append(f"{prefix}: version must be positive integer")
    if record.get("family") not in FAMILIES:
        errors.append(f"{prefix}: invalid family")
    statement = record.get("canonical_statement")
    if not isinstance(statement, str) or len(statement.strip()) < 12:
        errors.append(f"{prefix}: canonical_statement too short")
    scope = record.get("scope")
    if not isinstance(scope, list) or not scope or any(not isinstance(x, str) or not x.strip() for x in scope):
        errors.append(f"{prefix}: scope must be non-empty string array")
    elif len(scope) != len(set(scope)):
        errors.append(f"{prefix}: scope contains duplicates")

    authority = record.get("authority")
    if not isinstance(authority, dict) or set(authority) != {"control_plane", "implementation", "evidence"}:
        errors.append(f"{prefix}: invalid authority object")
    elif any(not isinstance(authority.get(k), str) or not authority[k].strip() for k in authority):
        errors.append(f"{prefix}: authority values must be non-empty")

    source = record.get("source")
    if not isinstance(source, dict) or set(source) != {"path", "blob_sha", "producer_commit_sha", "observed_at_commit_sha"}:
        errors.append(f"{prefix}: invalid source object")
    else:
        source_path = source.get("path")
        if not isinstance(source_path, str) or not safe_relative(source_path):
            errors.append(f"{prefix}: unsafe source.path")
        else:
            candidate = root / source_path
            if not candidate.is_file():
                errors.append(f"{prefix}: broken source reference: {source_path}")
            else:
                observed_blob = git_blob_sha1(candidate)
                if source.get("blob_sha") != observed_blob:
                    errors.append(
                        f"{prefix}: SOURCE_DRIFT blob mismatch for {source_path}: "
                        f"declared={source.get('blob_sha')} observed={observed_blob}"
                    )
        producer = source.get("producer_commit_sha")
        if not isinstance(producer, str) or not (HEX40_RE.fullmatch(producer) or TOKEN_RE.fullmatch(producer)):
            errors.append(f"{prefix}: invalid producer_commit_sha")
        observed = source.get("observed_at_commit_sha")
        if not isinstance(observed, str) or not HEX40_RE.fullmatch(observed):
            errors.append(f"{prefix}: invalid observed_at_commit_sha")

    for field in ("validators", "tests", "workflows", "receipts", "dependencies", "falsifiers"):
        value = record.get(field)
        if not isinstance(value, list):
            errors.append(f"{prefix}: {field} must be an array")
            continue
        if len(value) != len(set(map(str, value))):
            errors.append(f"{prefix}: {field} contains duplicates")
    if isinstance(record.get("falsifiers"), list):
        if not record["falsifiers"] or any(not isinstance(x, str) or len(x.strip()) < 8 for x in record["falsifiers"]):
            errors.append(f"{prefix}: falsifiers must contain explicit non-empty conditions")

    for field in ("validators", "tests", "workflows", "receipts"):
        for ref in record.get(field, []) if isinstance(record.get(field), list) else []:
            if not isinstance(ref, str) or not existing_ref(root, ref):
                errors.append(f"{prefix}: broken {field} reference: {ref!r}")

    deps = record.get("dependencies", [])
    if isinstance(deps, list):
        for dep in deps:
            if not isinstance(dep, str) or not ID_RE.fullmatch(dep):
                errors.append(f"{prefix}: invalid dependency id: {dep!r}")
            if dep == iid:
                errors.append(f"{prefix}: invariant cannot require itself")

    vector = record.get("verification_vector")
    token_states: list[str] = []
    if not isinstance(vector, dict) or set(vector) != set(VECTOR_KEYS):
        errors.append(f"{prefix}: verification_vector must contain exactly D,I,T,C,X,F")
        vector = {}
    else:
        for key in VECTOR_KEYS:
            value = vector.get(key)
            if not isinstance(value, str) or not GATE_RE.fullmatch(value):
                errors.append(f"{prefix}: invalid verification state {key}={value!r}")
            elif value.startswith("TOKEN_VAZIO_"):
                token_states.append(value)

    if record.get("urgency") not in PRIORITIES:
        errors.append(f"{prefix}: invalid urgency")
    if not isinstance(record.get("urgency_reason"), str) or len(record["urgency_reason"].strip()) < 8:
        errors.append(f"{prefix}: urgency_reason required")
    if not isinstance(record.get("claim_allowed"), bool):
        errors.append(f"{prefix}: claim_allowed must be boolean")
    if not isinstance(record.get("next_verifiable_step"), str) or len(record["next_verifiable_step"].strip()) < 8:
        errors.append(f"{prefix}: next_verifiable_step required")

    reason = record.get("token_vazio_reason")
    if token_states and (not isinstance(reason, str) or not reason.strip()):
        errors.append(f"{prefix}: TOKEN_VAZIO states require token_vazio_reason")
    if not token_states and reason not in {None, ""}:
        warnings.append(f"{prefix}: token_vazio_reason present although vector has no TOKEN_VAZIO")

    if vector.get("I") == "PASS" and not record.get("validators"):
        errors.append(f"{prefix}: FALSE_PROMOTION I=PASS requires validator reference")
    if vector.get("T") == "PASS" and not record.get("tests"):
        errors.append(f"{prefix}: FALSE_PROMOTION T=PASS requires test reference")
    if vector.get("C") == "PASS" and not record.get("workflows"):
        errors.append(f"{prefix}: FALSE_PROMOTION C=PASS requires workflow reference")
    if record.get("claim_allowed") is True:
        if any(str(vector.get(k, "")).startswith("TOKEN_VAZIO_") for k in VECTOR_KEYS):
            errors.append(f"{prefix}: FALSE_PROMOTION claim_allowed=true with TOKEN_VAZIO vector")
        if vector.get("F") != "PASS":
            errors.append(f"{prefix}: FALSE_PROMOTION claim_allowed=true requires F=PASS")

    return errors, warnings


def validate_edge(edge: dict[str, Any], root: Path, invariant_ids: set[str], prefix: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    missing = sorted(REQUIRED_EDGE - set(edge))
    if missing:
        return [f"{prefix}: missing fields: {', '.join(missing)}"], warnings
    extras = sorted(set(edge) - REQUIRED_EDGE)
    if extras:
        errors.append(f"{prefix}: unexpected fields: {', '.join(extras)}")
    if edge.get("schema_version") != EDGE_SCHEMA:
        errors.append(f"{prefix}: invalid schema_version")
    if not isinstance(edge.get("edge_id"), str) or not EDGE_ID_RE.fullmatch(edge["edge_id"]):
        errors.append(f"{prefix}: invalid edge_id")
    relation = edge.get("relation")
    if relation not in RELATIONS:
        errors.append(f"{prefix}: invalid relation")
    if edge.get("claim_allowed") is not False:
        errors.append(f"{prefix}: edge claim_allowed must remain false")

    def endpoint_ok(value: Any) -> bool:
        if isinstance(value, str) and value in invariant_ids:
            return True
        path = artifact_path(value) if isinstance(value, str) else None
        return bool(path and existing_ref(root, path))

    left, right = edge.get("from"), edge.get("to")
    if not endpoint_ok(left):
        errors.append(f"{prefix}: unresolved from endpoint: {left!r}")
    if not endpoint_ok(right):
        errors.append(f"{prefix}: unresolved to endpoint: {right!r}")
    if left == right:
        errors.append(f"{prefix}: self-edge forbidden")

    if relation in {"requires", "contradicts", "supersedes"}:
        if left not in invariant_ids or right not in invariant_ids:
            errors.append(f"{prefix}: {relation} requires invariant endpoints")
    if relation in {"implements", "tests", "evidenced_by"}:
        if left not in invariant_ids or artifact_path(right) is None:
            errors.append(f"{prefix}: {relation} requires invariant -> artifact")
    if relation == "falsifies":
        if artifact_path(left) is None or right not in invariant_ids:
            errors.append(f"{prefix}: falsifies requires artifact -> invariant")

    refs = edge.get("evidence_refs")
    if not isinstance(refs, list):
        errors.append(f"{prefix}: evidence_refs must be array")
    else:
        for ref in refs:
            if not isinstance(ref, str) or not existing_ref(root, ref):
                errors.append(f"{prefix}: broken evidence_ref: {ref!r}")
    return errors, warnings


def requires_topology(invariant_ids: set[str], edges: list[dict[str, Any]]) -> tuple[list[str], int, list[str]]:
    deps: dict[str, set[str]] = {iid: set() for iid in invariant_ids}
    children: dict[str, set[str]] = {iid: set() for iid in invariant_ids}
    for edge in edges:
        if edge.get("relation") != "requires":
            continue
        left, right = edge.get("from"), edge.get("to")
        if left in invariant_ids and right in invariant_ids:
            deps[left].add(right)
            children[right].add(left)

    indegree = {iid: len(deps[iid]) for iid in invariant_ids}
    queue = deque(sorted(iid for iid, degree in indegree.items() if degree == 0))
    order: list[str] = []
    depth = {iid: 0 for iid in queue}
    while queue:
        current = queue.popleft()
        order.append(current)
        for child in sorted(children[current]):
            depth[child] = max(depth.get(child, 0), depth[current] + 1)
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    cyclic = sorted(iid for iid, degree in indegree.items() if degree > 0)
    return order, max(depth.values(), default=0), cyclic


def discover_candidates(root: Path, linked_paths: set[str], limit: int = 256) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for base in (root / "scripts", root / "docs", root / "data" / "contracts"):
        if not base.exists():
            continue
        for path in sorted(p for p in base.rglob("*") if p.is_file() and p.suffix.lower() in DISCOVERY_SUFFIXES):
            try:
                if path.stat().st_size > 2_000_000:
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            rel = path.relative_to(root).as_posix()
            for line_no, line in enumerate(text.splitlines(), 1):
                if not DISCOVERY_RE.search(line):
                    continue
                if rel in linked_paths:
                    break
                candidates.append({
                    "state": "TOKEN_VAZIO_DISCOVERY_CANDIDATE",
                    "path": rel,
                    "line": line_no,
                    "excerpt_sha256": hashlib.sha256(line.strip().encode("utf-8")).hexdigest(),
                    "next_verifiable_step": "Classify as new invariant, implementation detail, duplicate, contradiction or non-invariant before registration.",
                })
                break
            if len(candidates) >= limit:
                return candidates
    return candidates


def audit_repository(root: Path, registry_path: Path, edges_path: Path, *, source_sha: str, run_id: str, generated_at: str) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    records, record_load_errors = load_jsonl(registry_path)
    edges, edge_load_errors = load_jsonl(edges_path)
    errors.extend(record_load_errors)
    errors.extend(edge_load_errors)

    by_id: dict[str, dict[str, Any]] = {}
    normalized_statements: dict[str, str] = {}
    urgency_counts: Counter[str] = Counter()
    token_counts: Counter[str] = Counter()

    for index, record in enumerate(records, 1):
        prefix = f"registry[{index}]"
        rec_errors, rec_warnings = validate_record(record, root, prefix)
        errors.extend(rec_errors); warnings.extend(rec_warnings)
        iid = record.get("invariant_id")
        if isinstance(iid, str):
            if iid in by_id:
                errors.append(f"{prefix}: duplicate invariant_id {iid}")
            by_id[iid] = record
        statement = record.get("canonical_statement")
        if isinstance(statement, str):
            normalized = normalize_statement(statement)
            previous = normalized_statements.get(normalized)
            if previous and previous != iid:
                errors.append(f"SEMANTIC_DUPLICATE exact normalized statement: {previous} and {iid}")
            else:
                normalized_statements[normalized] = str(iid)
        urgency_counts[str(record.get("urgency"))] += 1
        vector = record.get("verification_vector", {})
        if isinstance(vector, dict):
            for value in vector.values():
                if isinstance(value, str) and value.startswith("TOKEN_VAZIO_"):
                    token_counts[value] += 1

    invariant_ids = set(by_id)
    edge_ids: set[str] = set()
    incident: Counter[str] = Counter()
    requires_from: dict[str, set[str]] = defaultdict(set)
    supersedes_from: dict[str, set[str]] = defaultdict(set)
    registered_test_paths: set[str] = set()
    linked_paths: set[str] = set()

    for record in records:
        source = record.get("source", {})
        if isinstance(source, dict) and isinstance(source.get("path"), str):
            linked_paths.add(source["path"])
        for field in ("validators", "tests", "workflows", "receipts"):
            for ref in record.get(field, []) if isinstance(record.get(field), list) else []:
                if isinstance(ref, str):
                    linked_paths.add(ref)
                    if field == "tests":
                        registered_test_paths.add(ref)

    for index, edge in enumerate(edges, 1):
        prefix = f"edges[{index}]"
        edge_errors, edge_warnings = validate_edge(edge, root, invariant_ids, prefix)
        errors.extend(edge_errors); warnings.extend(edge_warnings)
        eid = edge.get("edge_id")
        if isinstance(eid, str):
            if eid in edge_ids:
                errors.append(f"{prefix}: duplicate edge_id {eid}")
            edge_ids.add(eid)
        for endpoint in (edge.get("from"), edge.get("to")):
            if endpoint in invariant_ids:
                incident[str(endpoint)] += 1
            path = artifact_path(endpoint) if isinstance(endpoint, str) else None
            if path:
                linked_paths.add(path)
                if path.startswith("tests/"):
                    registered_test_paths.add(path)
        if edge.get("relation") == "requires" and edge.get("from") in invariant_ids and edge.get("to") in invariant_ids:
            requires_from[str(edge["from"])].add(str(edge["to"]))
        if edge.get("relation") == "supersedes" and edge.get("from") in invariant_ids and edge.get("to") in invariant_ids:
            supersedes_from[str(edge["from"])].add(str(edge["to"]))

    for iid, record in by_id.items():
        declared = set(record.get("dependencies", [])) if isinstance(record.get("dependencies"), list) else set()
        edged = requires_from.get(iid, set())
        if declared != edged:
            errors.append(f"DEPENDENCY_DRIFT {iid}: record={sorted(declared)} edges={sorted(edged)}")
        if incident[iid] == 0:
            errors.append(f"ORPHAN_INVARIANT {iid}: no typed edges")
        if record.get("version", 1) > 1 and not supersedes_from.get(iid):
            errors.append(f"VERSION_DRIFT {iid}: version>1 requires explicit supersedes edge")

    order, max_depth, cyclic = requires_topology(invariant_ids, edges)
    if cyclic:
        errors.append("REQUIRES_CYCLE: " + ", ".join(cyclic))

    all_test_candidates: list[str] = []
    tests_dir = root / "tests"
    if tests_dir.is_dir():
        for path in sorted(tests_dir.glob("test_*invariant*.py")):
            rel = path.relative_to(root).as_posix()
            all_test_candidates.append(rel)
            if rel not in registered_test_paths:
                warnings.append(f"TEST_WITHOUT_INVARIANT_MAPPING {rel}")
    meta_test = "tests/test_map_invariant_registry.py"
    if (root / meta_test).is_file() and meta_test not in registered_test_paths:
        warnings.append(f"TEST_WITHOUT_INVARIANT_MAPPING {meta_test}")

    for iid, record in by_id.items():
        for receipt_ref in record.get("receipts", []) if isinstance(record.get("receipts"), list) else []:
            path = root / receipt_ref
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if isinstance(payload, dict):
                receipt_source = payload.get("source_commit_sha")
                record_source = record.get("source", {}).get("observed_at_commit_sha") if isinstance(record.get("source"), dict) else None
                if isinstance(receipt_source, str) and isinstance(record_source, str) and receipt_source != record_source:
                    warnings.append(f"STALE_RECEIPT_SOURCE_SHA {iid}: {receipt_ref}")

    discovery = discover_candidates(root, linked_paths)
    for candidate in discovery:
        warnings.append(f"TOKEN_VAZIO_DISCOVERY_CANDIDATE {candidate['path']}:{candidate['line']}")

    registry_sha = hashlib.sha256(registry_path.read_bytes()).hexdigest() if registry_path.is_file() else "TOKEN_VAZIO_REGISTRY_UNREADABLE"
    edges_sha = hashlib.sha256(edges_path.read_bytes()).hexdigest() if edges_path.is_file() else "TOKEN_VAZIO_EDGES_UNREADABLE"

    receipt: dict[str, Any] = {
        "schema_version": AUDIT_SCHEMA,
        "status": "PASS" if not errors else "FAIL",
        "claim_allowed": False,
        "repository": "rafaelmeloreisnovo/Mapa",
        "source_commit_sha": source_sha,
        "run_id": run_id,
        "generated_at": generated_at,
        "source_mode": "READ_ONLY_AUDIT",
        "automatic_mutation": False,
        "automatic_merge": False,
        "registry_sha256": registry_sha,
        "edges_sha256": edges_sha,
        "metrics": {
            "invariant_count": len(by_id),
            "edge_count": len(edges),
            "requires_edge_count": sum(edge.get("relation") == "requires" for edge in edges),
            "max_dependency_depth": max_depth,
            "orphan_count": sum(incident[iid] == 0 for iid in invariant_ids),
            "cycle_count": 1 if cyclic else 0,
            "discovery_candidate_count": len(discovery),
            "error_count": len(errors),
            "warning_count": len(warnings),
            "urgency_counts": {key: urgency_counts.get(key, 0) for key in PRIORITIES},
            "token_vazio_state_counts": dict(sorted(token_counts.items())),
        },
        "topological_order": order,
        "discovery_candidates": discovery,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "epistemic_boundary": [
            "audit PASS != physical runtime proof",
            "audit PASS != scientific validation",
            "hash match != truth",
            "CI reproduction != independent replication",
            "TOKEN_VAZIO is preserved until the missing observation exists",
        ],
        "next_verifiable_step": (
            "Bind the generated receipt to the exact CI run and classify discovery candidates without automatic promotion."
            if not errors else
            "Correct every fail-closed error before merge; preserve unresolved observations as TOKEN_VAZIO."
        ),
    }
    unsigned = dict(receipt)
    receipt["receipt_sha256"] = sha256_json(unsigned)
    return receipt


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path("."))
    p.add_argument("--registry", type=Path, default=Path("data/invariants/map_invariant_registry.v1.jsonl"))
    p.add_argument("--edges", type=Path, default=Path("data/invariants/map_invariant_edges.v1.jsonl"))
    p.add_argument("--output", type=Path)
    p.add_argument("--source-sha", default=os.environ.get("GITHUB_SHA", "TOKEN_VAZIO_SOURCE_SHA_NOT_PROVIDED"))
    p.add_argument("--run-id", default=os.environ.get("GITHUB_RUN_ID", "TOKEN_VAZIO_RUN_ID_NOT_PROVIDED"))
    p.add_argument("--generated-at", default=os.environ.get("RAFAELIA_GENERATED_AT", "TOKEN_VAZIO_RUNTIME_TIME_NOT_PROVIDED"))
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    registry = args.registry if args.registry.is_absolute() else root / args.registry
    edges = args.edges if args.edges.is_absolute() else root / args.edges
    receipt = audit_repository(
        root,
        registry,
        edges,
        source_sha=args.source_sha,
        run_id=args.run_id,
        generated_at=args.generated_at,
    )
    rendered = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
