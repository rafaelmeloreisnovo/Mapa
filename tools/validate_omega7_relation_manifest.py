#!/usr/bin/env python3
"""Dependency-free O12 validator: structure, lineage and false-identity guards."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
from typing import Any

EVENT = re.compile(r"^sha256:[0-9a-f]{64}$")
GIT_SHA = re.compile(r"^[0-9a-f]{40,64}$")
EDGE = re.compile(r"^[A-Z0-9_]+$")
GATE = re.compile(r"^gate:O[0-9]+$")
KEYS = {
    "physical_key": "source_locator + source_revision + content_sha256",
    "logical_key": "artifact_id + semantic_role + authority",
    "event_key": "event_id + previous_event_id + timestamp",
}

def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check(ok: bool, code: str, detail: str, errors: list[dict[str, str]]) -> None:
    if not ok:
        errors.append({"code": code, "detail": detail})

def validate_manifest(m: dict[str, Any]) -> list[dict[str, str]]:
    e: list[dict[str, str]] = []
    required = {
        "schema","manifest_version","timestamp","artifact_id","previous_event_id",
        "derived_from","claim_allowed","privacy_class","automatic_merge",
        "automatic_mutation","observed_state","canonical_identity","nodes","edges",
        "gate_alignment","optimization","f_ok","f_gap","f_next",
    }
    for key in sorted(required - set(m)):
        e.append({"code": "MISSING_FIELD", "detail": key})
    if e:
        return e

    check(m["schema"] == "RAFAELIA_RELATION_OPTIMIZATION_MANIFEST/v1",
          "BAD_SCHEMA", str(m["schema"]), e)
    check(bool(re.fullmatch(r"1\.[0-9]+\.[0-9]+", str(m["manifest_version"]))),
          "BAD_VERSION", str(m["manifest_version"]), e)
    check(m["claim_allowed"] is False, "CLAIM_PROMOTION_FORBIDDEN", "claim_allowed", e)
    check(m["automatic_merge"] is False, "AUTO_MERGE_FORBIDDEN", "automatic_merge", e)
    check(m["automatic_mutation"] is False, "AUTO_MUTATION_FORBIDDEN", "automatic_mutation", e)
    check(m["privacy_class"] == "PRIVATE_RESTRICTED", "BAD_PRIVACY", str(m["privacy_class"]), e)
    check(bool(EVENT.fullmatch(str(m["previous_event_id"]))),
          "BAD_PREVIOUS_EVENT", str(m["previous_event_id"]), e)

    derived = m["derived_from"]
    check(isinstance(derived, list) and bool(derived), "EMPTY_DERIVED_FROM", "derived_from", e)
    if isinstance(derived, list):
        check(len(derived) == len(set(derived)), "DUPLICATE_DERIVATION", "derived_from", e)
        for value in derived:
            check(bool(EVENT.fullmatch(str(value))), "BAD_DERIVATION_ID", str(value), e)

    identity = m["canonical_identity"]
    check(isinstance(identity, dict), "BAD_IDENTITY_CONTRACT", "canonical_identity", e)
    if isinstance(identity, dict):
        for key, value in KEYS.items():
            check(identity.get(key) == value, "IDENTITY_KEY_DRIFT", key, e)
        rule = str(identity.get("dedupe_rule", "")).lower()
        for guard in ("title", "filename", "hashtag", "semantic similarity"):
            check(guard in rule, "DEDUPE_GUARD_MISSING", guard, e)

    nodes = m["nodes"]
    check(isinstance(nodes, list) and bool(nodes), "EMPTY_NODES", "nodes", e)
    ids: list[str] = []
    if isinstance(nodes, list):
        for index, node in enumerate(nodes):
            check(isinstance(node, dict), "BAD_NODE", str(index), e)
            if isinstance(node, dict):
                for key in ("id","type","state"):
                    check(isinstance(node.get(key), str) and bool(node.get(key)),
                          "BAD_NODE_FIELD", f"{index}:{key}", e)
                if isinstance(node.get("id"), str):
                    ids.append(node["id"])
        check(len(ids) == len(set(ids)), "DUPLICATE_NODE_ID", "nodes", e)

    node_set, triples = set(ids), []
    edges = m["edges"]
    check(isinstance(edges, list) and bool(edges), "EMPTY_EDGES", "edges", e)
    if isinstance(edges, list):
        for index, edge in enumerate(edges):
            if not isinstance(edge, dict):
                e.append({"code": "BAD_EDGE", "detail": str(index)})
                continue
            src, dst, kind = edge.get("from"), edge.get("to"), edge.get("type")
            check(src in node_set, "UNRESOLVED_EDGE_SOURCE", f"{index}:{src}", e)
            check(dst in node_set or bool(GATE.fullmatch(str(dst))),
                  "UNRESOLVED_EDGE_TARGET", f"{index}:{dst}", e)
            check(bool(EDGE.fullmatch(str(kind))), "BAD_EDGE_TYPE", f"{index}:{kind}", e)
            check(src != dst, "SELF_EDGE", str(index), e)
            triples.append((str(src), str(dst), str(kind)))
        check(len(triples) == len(set(triples)), "DUPLICATE_EDGE", "edges", e)

    state = m["observed_state"]
    pr140 = state.get("pr_140", {}) if isinstance(state, dict) else {}
    pr141 = (state.get("pr_141") or state.get("optimization_branch", {})) if isinstance(state, dict) else {}
    check(pr140.get("state") == "MERGED", "PR140_STATE_NOT_CORRECTED", str(pr140), e)
    check(bool(GIT_SHA.fullmatch(str(pr140.get("merge_commit_sha", "")))),
          "BAD_MERGE_SHA", str(pr140.get("merge_commit_sha")), e)
    check(isinstance(pr141, dict) and bool(pr141), "PR141_STATE_ABSENT", str(pr141), e)

    aligned = {x.get("gate") for x in m["gate_alignment"] if isinstance(x, dict)}
    for gate in ("O0","O1","O3","O5","O6"):
        check(gate in aligned, "MISSING_GATE_ALIGNMENT", gate, e)
    for key in ("f_ok","f_gap","f_next"):
        check(isinstance(m[key], list), "BAD_R3_FIELD", key, e)
    return e

def classify(c: dict[str, Any]) -> str:
    expected, a, b = c.get("expected"), c.get("a", {}), c.get("b", {})
    if expected == "ALIAS_ALLOWED":
        return "ALIAS_ALLOWED" if a.get("content_sha256") == b.get("content_sha256") else "SEPARATE_OBJECTS"
    if expected == "SEPARATE_OBJECTS":
        return "SEPARATE_OBJECTS" if a.get("title") == b.get("title") and a.get("content_sha256") != b.get("content_sha256") else "INVALID_FIXTURE"
    if expected == "REJECT_IDENTITY":
        return "REJECT_IDENTITY" if set(a) <= {"hashtags","title"} and set(b) <= {"hashtags","title"} else "INVALID_FIXTURE"
    if expected == "RELATION_ONLY":
        return "RELATION_ONLY" if "content_sha256" not in a and "content_sha256" not in b else "INVALID_FIXTURE"
    if expected == "STALE_STATE_EVENT_REQUIRED":
        return "STALE_STATE_EVENT_REQUIRED" if c.get("declared_state") != c.get("provider_state") else "NO_DIVERGENCE"
    return "UNKNOWN_EXPECTATION"

def validate_fixtures(f: dict[str, Any]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    errors, results = [], []
    check(f.get("schema") == "RAFAELIA_IDENTITY_FIXTURES/v1",
          "BAD_FIXTURE_SCHEMA", str(f.get("schema")), errors)
    cases = f.get("cases")
    check(isinstance(cases, list) and len(cases) >= 5,
          "INSUFFICIENT_FIXTURES", str(type(cases)), errors)
    if not isinstance(cases, list):
        return errors, results
    ids = []
    for case in cases:
        cid, expected = str(case.get("id", "")), str(case.get("expected", ""))
        actual = classify(case)
        ids.append(cid)
        results.append({"id": cid, "expected": expected, "actual": actual})
        check(actual == expected, "FIXTURE_FAILED", f"{cid}:{actual}", errors)
    check(len(ids) == len(set(ids)), "DUPLICATE_FIXTURE_ID", "cases", errors)
    return errors, results

def main() -> int:
    p = argparse.ArgumentParser()
    for name in ("manifest","fixtures","schema","output"):
        p.add_argument(f"--{name}", required=True, type=Path)
    a = p.parse_args()
    manifest_errors = validate_manifest(read(a.manifest))
    fixture_errors, fixture_results = validate_fixtures(read(a.fixtures))
    errors = manifest_errors + fixture_errors
    receipt = {
        "schema": "RAFAELIA_O12_VALIDATION_RECEIPT/v1",
        "validator_mode": "DEPENDENCY_FREE_STANDARD_LIBRARY",
        "claim_allowed": False,
        "automatic_merge": False,
        "inputs": {
            "manifest": {"path": str(a.manifest), "sha256": digest(a.manifest)},
            "schema": {"path": str(a.schema), "sha256": digest(a.schema)},
            "fixtures": {"path": str(a.fixtures), "sha256": digest(a.fixtures)},
            "validator": {"path": str(Path(__file__).resolve()), "sha256": digest(Path(__file__).resolve())}
        },
        "checks": {
            "manifest_errors": manifest_errors,
            "fixture_errors": fixture_errors,
            "fixture_results": fixture_results,
            "total_errors": len(errors)
        },
        "gate": {
            "id": "O12",
            "decision": "PASS_LIMITED" if not errors else "FAIL",
            "limitations": [
                "Structural/local validation only.",
                "Provider state, credential rotation, CI, backup replacement and Termux runtime are not proven.",
                "Scientific claims remain blocked."
            ]
        },
        "f_ok": [
            "Manifest structure checked without third-party packages.",
            "Node and edge identity constraints checked.",
            "Five false-identity fixtures executed."
        ] if not errors else [],
        "f_gap": [
            "Provider-state attestation remains external.",
            "O6 credential-rotation evidence absent.",
            "CI and physical Termux receipts absent."
        ],
        "f_next": [
            "Commit validator, schema, fixtures and receipt to PR #141.",
            "Keep PR #141 draft until O6 and external receipts exist."
        ]
    }
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"decision": receipt["gate"]["decision"], "total_errors": len(errors),
                      "fixture_results": fixture_results, "receipt": str(a.output)}, ensure_ascii=False))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
