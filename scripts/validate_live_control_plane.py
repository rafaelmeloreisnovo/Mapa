#!/usr/bin/env python3
"""Validate the RAFAELIA live control-plane snapshot using Python stdlib only."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

SHA40 = re.compile(r"^[0-9a-f]{40}$")
REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
ID = re.compile(r"^[A-Z][A-Z0-9_.:-]{2,127}$")
ALLOWED_EVIDENCE_STATES = {"VERIFIED", "VERIFIED_LIMITED", "TOKEN_VAZIO", "CONTRADICTION"}
ALLOWED_MODULE_STATES = {"VERIFIED", "VERIFIED_LIMITED", "PARTIAL", "PARTIAL_DRAFT", "TOKEN_VAZIO", "BLOCKED"}
ALLOWED_PRODUCT_STATES = {"VERIFIED", "VERIFIED_LIMITED", "VERIFIED_LIMITED_DRAFT", "PARTIAL", "TOKEN_VAZIO", "BLOCKED"}
EXPECTED_FILES = {
    "evidence": "data/control-plane/evidence_pointer_registry.v1.json",
    "modules": "data/control-plane/module_registry.v1.json",
    "products": "data/control-plane/product_graph.v1.json",
    "merge_decisions": "data/control-plane/merge_decisions.v1.json",
    "procedure_state": "data/control-plane/procedure_state.v1.json",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def unique(items: list[dict[str, Any]], key: str, errors: list[str], label: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{label}[{index}] must be object")
            continue
        value = item.get(key)
        if not nonempty(value):
            errors.append(f"{label}[{index}].{key} missing")
            continue
        if value in out:
            errors.append(f"duplicate {label} id: {value}")
        out[value] = item
    return out


def require_claim_blocked(document: dict[str, Any], name: str, errors: list[str]) -> None:
    if document.get("claim_allowed") is not False:
        errors.append(f"{name}.claim_allowed must be false")


def validate(repo_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    cp = repo_root / "data/control-plane"
    snapshot_path = cp / "current_state_snapshot.v1.json"
    if not snapshot_path.exists():
        return {"status": "FAIL", "errors": ["current snapshot missing"], "warnings": [], "claim_allowed": False}

    snapshot = load_json(snapshot_path)
    require_claim_blocked(snapshot, "snapshot", errors)
    if snapshot.get("schema_version") != "rafaelia.live-control-plane-snapshot/v1":
        errors.append("invalid snapshot schema_version")
    registries = snapshot.get("registries")
    if not isinstance(registries, dict):
        errors.append("snapshot.registries must be object")
        registries = {}
    for key, expected in EXPECTED_FILES.items():
        actual = registries.get(key)
        if actual != expected:
            errors.append(f"snapshot.registries.{key} must equal {expected}")
        if isinstance(actual, str) and "fixtures" in Path(actual).parts:
            errors.append(f"live registry {key} must not point into fixtures")
        if isinstance(actual, str) and not (repo_root / actual).exists():
            errors.append(f"registry file missing: {actual}")

    docs = {key: load_json(repo_root / path) for key, path in EXPECTED_FILES.items() if (repo_root / path).exists()}
    for key, doc in docs.items():
        if not isinstance(doc, dict):
            errors.append(f"{key} registry must be object")
        else:
            require_claim_blocked(doc, key, errors)

    ev_doc = docs.get("evidence", {})
    if ev_doc.get("schema_version") != "rafaelia.evidence-pointer-registry/v1":
        errors.append("invalid evidence registry schema_version")
    evidence = unique(ev_doc.get("pointers", []) if isinstance(ev_doc.get("pointers"), list) else [], "evidence_id", errors, "evidence")
    for eid, item in evidence.items():
        if item.get("claim_allowed") is not False:
            errors.append(f"{eid}.claim_allowed must be false")
        provider, kind, state = item.get("provider"), item.get("kind"), item.get("state")
        if provider not in {"github", "local_repository"}:
            errors.append(f"{eid}.provider invalid")
        if kind not in {"commit", "file", "pull_request", "issue_comment", "run", "test", "report"}:
            errors.append(f"{eid}.kind invalid")
        if state not in ALLOWED_EVIDENCE_STATES:
            errors.append(f"{eid}.state invalid")
        repository = item.get("repository")
        if not (nonempty(repository) and REPO.fullmatch(repository)):
            errors.append(f"{eid}.repository invalid")
        ref = item.get("ref")
        if kind in {"commit", "file", "pull_request"} and not (nonempty(ref) and SHA40.fullmatch(ref)):
            errors.append(f"{eid}.ref must be immutable 40-hex SHA for {kind}")
        if kind == "pull_request":
            if not isinstance(item.get("pr_number"), int) or item["pr_number"] <= 0:
                errors.append(f"{eid}.pr_number invalid")
            if item.get("pr_state") not in {"OPEN_DRAFT", "OPEN_READY", "MERGED", "CLOSED"}:
                errors.append(f"{eid}.pr_state invalid")
        path = item.get("path")
        if provider == "local_repository":
            if not nonempty(path):
                errors.append(f"{eid}.path required for local_repository")
            elif Path(path).is_absolute() or ".." in Path(path).parts:
                errors.append(f"{eid}.path unsafe")
            elif not (repo_root / path).exists():
                errors.append(f"{eid}.local evidence path missing: {path}")
        if provider == "github" and kind == "file" and not nonempty(path):
            errors.append(f"{eid}.path required for cross-repository file")
        if not isinstance(item.get("supports"), list) or not item["supports"]:
            errors.append(f"{eid}.supports must be non-empty")
        if not isinstance(item.get("limitations"), list) or not item["limitations"]:
            errors.append(f"{eid}.limitations must be non-empty")

    mod_doc = docs.get("modules", {})
    if mod_doc.get("schema_version") != "rafaelia.live-module-registry/v1":
        errors.append("invalid module registry schema_version")
    modules = unique(mod_doc.get("modules", []) if isinstance(mod_doc.get("modules"), list) else [], "module_id", errors, "module")
    for mid, item in modules.items():
        if item.get("state") not in ALLOWED_MODULE_STATES:
            errors.append(f"{mid}.state invalid")
        if not (nonempty(item.get("repository")) and REPO.fullmatch(item["repository"])):
            errors.append(f"{mid}.repository invalid")
        if item.get("state") != "TOKEN_VAZIO" and not (nonempty(item.get("observed_ref")) and SHA40.fullmatch(item["observed_ref"])):
            errors.append(f"{mid}.observed_ref must be immutable SHA")
        evs = item.get("evidence_ids")
        if not isinstance(evs, list):
            errors.append(f"{mid}.evidence_ids must be array")
            evs = []
        for eid in evs:
            if eid not in evidence:
                errors.append(f"{mid} references unknown evidence {eid}")
        if item.get("state") in {"VERIFIED", "VERIFIED_LIMITED", "PARTIAL_DRAFT"} and not evs:
            errors.append(f"{mid} state requires evidence")
        if not isinstance(item.get("gaps"), list) or not item["gaps"]:
            errors.append(f"{mid}.gaps must be non-empty")
        if not nonempty(item.get("next_action")):
            errors.append(f"{mid}.next_action missing")

    prod_doc = docs.get("products", {})
    if prod_doc.get("schema_version") != "rafaelia.live-product-graph/v1":
        errors.append("invalid product graph schema_version")
    products = unique(prod_doc.get("products", []) if isinstance(prod_doc.get("products"), list) else [], "product_id", errors, "product")
    for pid, item in products.items():
        state = item.get("state")
        if state not in ALLOWED_PRODUCT_STATES:
            errors.append(f"{pid}.state invalid")
        producers = item.get("producer_modules")
        if not isinstance(producers, list) or not producers:
            errors.append(f"{pid}.producer_modules must be non-empty")
            producers = []
        for mid in producers:
            if mid not in modules:
                errors.append(f"{pid} references unknown module {mid}")
        evs = item.get("evidence_ids")
        if not isinstance(evs, list):
            errors.append(f"{pid}.evidence_ids must be array")
            evs = []
        for eid in evs:
            if eid not in evidence:
                errors.append(f"{pid} references unknown evidence {eid}")
        if state in {"VERIFIED", "VERIFIED_LIMITED", "VERIFIED_LIMITED_DRAFT"} and not evs:
            errors.append(f"{pid} verified state requires evidence")
        if state == "TOKEN_VAZIO" and evs:
            warnings.append(f"{pid} TOKEN_VAZIO carries evidence pointers; review whether state should be PARTIAL")
        if state == "VERIFIED_LIMITED_DRAFT":
            if not all(modules.get(mid, {}).get("state") == "PARTIAL_DRAFT" for mid in producers):
                errors.append(f"{pid} draft product requires PARTIAL_DRAFT producers")
            if not any(evidence.get(eid, {}).get("kind") == "pull_request" and evidence[eid].get("pr_state") == "OPEN_DRAFT" for eid in evs):
                errors.append(f"{pid} draft product requires OPEN_DRAFT PR evidence")
        if not isinstance(item.get("gaps"), list) or not item["gaps"]:
            errors.append(f"{pid}.gaps must be non-empty")
        if not nonempty(item.get("next_action")):
            errors.append(f"{pid}.next_action missing")

    relations = unique(prod_doc.get("relations", []) if isinstance(prod_doc.get("relations"), list) else [], "relation_id", errors, "relation")
    for rid, rel in relations.items():
        if rel.get("from") not in products or rel.get("to") not in products:
            errors.append(f"{rid} endpoints must reference products")
        if rel.get("from") == rel.get("to"):
            errors.append(f"{rid} cannot self-relate")

    dec_doc = docs.get("merge_decisions", {})
    if dec_doc.get("schema_version") != "rafaelia.merge-decision-ledger/v1":
        errors.append("invalid merge decision schema_version")
    if dec_doc.get("append_only") is not True:
        errors.append("merge decision ledger must be append_only")
    decisions = unique(dec_doc.get("decisions", []) if isinstance(dec_doc.get("decisions"), list) else [], "decision_id", errors, "decision")
    pr_numbers: set[int] = set()
    for did, item in decisions.items():
        pr = item.get("pr_number")
        if not isinstance(pr, int) or pr <= 0:
            errors.append(f"{did}.pr_number invalid")
        elif pr in pr_numbers:
            errors.append(f"duplicate merge decision PR: {pr}")
        else:
            pr_numbers.add(pr)
        if not (nonempty(item.get("merge_commit")) and SHA40.fullmatch(item["merge_commit"])):
            errors.append(f"{did}.merge_commit invalid")
        if item.get("observed_state") != "MERGED_WITH_LIMITED_EVIDENCE":
            errors.append(f"{did}.observed_state must preserve limited evidence")
        if item.get("remote_validation") != "TOKEN_VAZIO_RUNNER":
            errors.append(f"{did}.remote_validation must remain TOKEN_VAZIO_RUNNER")
        if item.get("human_override") is not True or item.get("decision_type") != "HUMAN_OVERRIDE_LIMITED":
            errors.append(f"{did} must record limited human override")
        if item.get("claim_promotion") is not False:
            errors.append(f"{did}.claim_promotion must be false")
        for eid in item.get("evidence_ids", []):
            if eid not in evidence:
                errors.append(f"{did} references unknown evidence {eid}")
    if pr_numbers != {51, 52, 54}:
        errors.append("merge decisions must reconcile PRs 51, 52 and 54")

    proc_doc = docs.get("procedure_state", {})
    if proc_doc.get("schema_version") != "rafaelia.procedure-state/v1":
        errors.append("invalid procedure state schema_version")
    source_ledger = proc_doc.get("source_ledger")
    if not nonempty(source_ledger) or not (repo_root / source_ledger).exists():
        errors.append("procedure_state.source_ledger missing")
    procedures = unique(proc_doc.get("procedures", []) if isinstance(proc_doc.get("procedures"), list) else [], "proc_id", errors, "procedure")
    for proc_id, item in procedures.items():
        if item.get("claim_allowed") is not False:
            errors.append(f"{proc_id}.claim_allowed must be false")
        decision_id = item.get("decision_id")
        if decision_id is not None and decision_id not in decisions:
            errors.append(f"{proc_id} references unknown decision {decision_id}")
        for eid in item.get("evidence_ids", []):
            if eid not in evidence:
                errors.append(f"{proc_id} references unknown evidence {eid}")
        if not nonempty(item.get("next_verifiable_step")):
            errors.append(f"{proc_id}.next_verifiable_step missing")

    derived = snapshot.get("derived", {})
    expected_counts = {
        "module_count": len(modules),
        "product_count": len(products),
        "merge_decision_count": len(decisions),
        "evidence_pointer_count": len(evidence),
        "procedure_state_count": len(procedures),
    }
    for key, value in expected_counts.items():
        if derived.get(key) != value:
            errors.append(f"snapshot.derived.{key}={derived.get(key)} but actual={value}")
    if derived.get("remote_runner_state") != "TOKEN_VAZIO_RUNNER":
        errors.append("remote runner state must remain TOKEN_VAZIO_RUNNER")
    if derived.get("semantic_interpretation_state") != "TOKEN_VAZIO":
        errors.append("semantic interpretation must remain TOKEN_VAZIO")
    invariants = snapshot.get("invariants")
    required_invariants = {
        "fixture_is_not_live_state", "merge_does_not_imply_remote_gate_pass",
        "cross_repository_evidence_is_typed", "private_raw_source_does_not_cross_to_model",
        "token_vazio_is_valid_and_non_promotable", "claim_allowed_remains_false",
    }
    if not isinstance(invariants, list) or not required_invariants.issubset(set(invariants)):
        errors.append("snapshot invariants incomplete")

    return {
        "schema_version": "rafaelia.live-control-plane-validation/v1",
        "status": "PASS" if not errors else "FAIL",
        "claim_allowed": False,
        "errors": errors,
        "warnings": warnings,
        "metrics": {
            "evidence_pointers": len(evidence), "modules": len(modules), "products": len(products),
            "relations": len(relations), "merge_decisions": len(decisions), "procedure_states": len(procedures),
        },
        "states": {
            "remote_runner": derived.get("remote_runner_state", "TOKEN_VAZIO"),
            "semantic_interpretation": derived.get("semantic_interpretation_state", "TOKEN_VAZIO"),
            "termux_health_bridge": derived.get("termux_health_bridge_state", "TOKEN_VAZIO"),
        },
        "next_verifiable_step": snapshot.get("next_verifiable_step", "TOKEN_VAZIO"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--write-report", type=Path)
    args = parser.parse_args()
    report = validate(args.repo_root.resolve())
    text = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
