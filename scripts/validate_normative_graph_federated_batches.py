#!/usr/bin/env python3
"""Fail-closed structural validator for federated normative-graph batches."""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

SCHEMA_VERSION = "NORMATIVE_GRAPH_FEDERATED_BATCH_V1"
DEFAULT_GLOB = "data/normative-graph/NORMATIVE_GRAPH_FEDERATED_BATCH_*.v1.json"


class ContractError(ValueError):
    pass


def _unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ContractError(f"duplicate JSON key: {key}")
        obj[key] = value
    return obj


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    except (OSError, json.JSONDecodeError, UnicodeError) as exc:
        raise ContractError(f"{path}: unreadable JSON: {exc}") from exc


def validate_batch(doc, expected_predecessor):
    required = ("schema_version", "batch_id", "generated_at", "claim_allowed",
                "invariants", "F_ok", "F_gap", "F_next")
    missing = [key for key in required if key not in doc]
    if missing:
        raise ContractError(f"missing top-level fields: {missing}")
    if doc["schema_version"] != SCHEMA_VERSION:
        raise ContractError(f"schema_version must be {SCHEMA_VERSION}")
    if doc["claim_allowed"] is not False:
        raise ContractError("claim_allowed must remain false")
    if not isinstance(doc["invariants"], list) or not doc["invariants"]:
        raise ContractError("invariants must be non-empty")
    if not isinstance(doc["F_ok"], list) or not isinstance(doc["F_gap"], list):
        raise ContractError("F_ok and F_gap must be lists")
    if not isinstance(doc["F_next"], str) or not doc["F_next"].strip():
        raise ContractError("F_next must be non-empty")

    collections = [name for name in ("repository_coverage", "repositories")
                   if isinstance(doc.get(name), list)]
    if len(collections) != 1:
        raise ContractError("exactly one repository collection is required")
    collection = collections[0]
    entries = doc[collection]
    if not entries:
        raise ContractError("repository collection must not be empty")

    seen = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ContractError("repository entry must be an object")
        repo = entry.get("repo") or entry.get("repository")
        if not isinstance(repo, str) or repo.count("/") != 1:
            raise ContractError(f"invalid repository identifier: {repo!r}")
        if repo in seen:
            raise ContractError(f"duplicate repository in batch: {repo}")
        seen.add(repo)
        if not isinstance(entry.get("ref"), str) or not entry["ref"]:
            raise ContractError(f"{repo}: ref is required")
        atoms = entry.get("normative_atoms")
        if not isinstance(atoms, list) or not atoms:
            raise ContractError(f"{repo}: normative_atoms must be non-empty")
        if collection == "repository_coverage" and not isinstance(entry.get("gaps"), list):
            raise ContractError(f"{repo}: gaps list is required")
        if collection == "repositories":
            if not isinstance(entry.get("evidence_gate"), str):
                raise ContractError(f"{repo}: evidence_gate is required")
            if not isinstance(entry.get("f_next"), str) or not entry["f_next"]:
                raise ContractError(f"{repo}: f_next is required")

    if expected_predecessor is None:
        if "predecessor_batch" in doc:
            raise ContractError("first batch must not declare predecessor_batch")
    elif doc.get("predecessor_batch") != expected_predecessor:
        raise ContractError(f"{doc['batch_id']}: predecessor must be {expected_predecessor}")

    return {"batch_id": doc["batch_id"], "repositories": sorted(seen)}


def validate_paths(paths):
    if not paths:
        raise ContractError("no batch files selected")
    reports, predecessor, global_repositories = [], None, set()
    for path in sorted(paths):
        report = validate_batch(load_json(path), predecessor)
        overlap = global_repositories.intersection(report["repositories"])
        if overlap:
            raise ContractError(f"cross-batch duplicate repositories: {sorted(overlap)}")
        global_repositories.update(report["repositories"])
        predecessor = report["batch_id"]
        reports.append(report)
    return reports


def self_test():
    base = {
        "schema_version": SCHEMA_VERSION,
        "batch_id": "TEST-001",
        "generated_at": "2026-08-12T00:00:00Z",
        "claim_allowed": False,
        "invariants": ["idea != evidence"],
        "repository_coverage": [{
            "repo": "owner/repo", "ref": "main",
            "normative_atoms": [{"domain": "license", "state": "TOKEN_VAZIO"}],
            "gaps": ["TOKEN_VAZIO_LICENSE"],
        }],
        "F_ok": [], "F_gap": ["TOKEN_VAZIO_LICENSE"],
        "F_next": "inspect LICENSE bytes",
    }
    validate_batch(base, None)
    mutations = [
        dict(base, claim_allowed=True),
        dict(base, repositories=[]),
        dict(base, schema_version="NORMATIVE_GRAPH_SCHEMA_V1"),
        json.loads(json.dumps(base)),
    ]
    mutations[-1]["repository_coverage"][0]["normative_atoms"] = []
    rejected = 0
    for mutation in mutations:
        try:
            validate_batch(mutation, None)
        except ContractError:
            rejected += 1
    if rejected != len(mutations):
        raise ContractError(f"self-test rejected {rejected}/{len(mutations)} falsifiers")
    return {"positive": 1, "negative_rejected": rejected}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            print(json.dumps({"self_test": self_test()}, sort_keys=True))
        paths = args.paths or sorted(Path(".").glob(DEFAULT_GLOB))
        reports = validate_paths(paths)
        print(json.dumps({
            "status": "PASS",
            "batch_count": len(reports),
            "repository_count": sum(len(x["repositories"]) for x in reports),
            "batches": [x["batch_id"] for x in reports],
            "claim_allowed": False,
        }, sort_keys=True))
        return 0
    except ContractError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc), "claim_allowed": False}, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
