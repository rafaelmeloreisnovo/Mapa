#!/usr/bin/env python3
"""Strict, read-only Phase 0 foundation validator.

This validator checks the versioned Phase 0 manifest against files that are
actually present in the checkout. It deliberately scopes TOKEN_VAZIO checks to
the four Phase 0 entries instead of silently treating every historical record
as if it used the same schema.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable


STATE_TOKENS = (
    "VERIFIED",
    "DECLARED",
    "TESTED_LOCAL",
    "TESTED_DEVICE",
    "PARTIAL",
    "IMPLEMENTED",
    "AUDIT",
    "TOKEN_VAZIO",
)

FOUNDATION_GATES = (
    "claim_allowed",
    "falsifiers",
    "evidence_uniqueness",
    "lane_dag",
    "observation_coverage",
)


def check_manifest_contract(root: Path, manifest: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    del root
    errors: list[str] = []
    if manifest.get("schema") != "rafaelia.phase-0-foundation-manifest/v1":
        errors.append("unexpected manifest schema")
    if not isinstance(manifest.get("manifest_id"), str) or not manifest["manifest_id"].strip():
        errors.append("manifest_id must be non-empty")
    if manifest.get("repository") != "rafaelmeloreisnovo/Mapa":
        errors.append("repository authority mismatch")
    required_docs = manifest.get("required_documentation")
    if not isinstance(required_docs, list) or len(required_docs) != 4:
        errors.append("required_documentation must contain exactly 4 entries")
    token_entries = manifest.get("token_vazio_entries")
    if not isinstance(token_entries, list) or len(token_entries) != 4:
        errors.append("token_vazio_entries must contain exactly 4 entries")
    else:
        token_ids = [item.get("id") for item in token_entries if isinstance(item, dict)]
        if len(token_ids) != len(set(token_ids)):
            errors.append("TOKEN_VAZIO entry IDs must be unique")
    audit_logs = manifest.get("audit_logs")
    if not isinstance(audit_logs, list) or len(audit_logs) != 5:
        errors.append("audit_logs must contain exactly 5 entries")
    else:
        audit_paths = [item.get("path") for item in audit_logs if isinstance(item, dict)]
        if len(audit_paths) != len(set(audit_paths)):
            errors.append("audit log paths must be unique")
    security_audits = manifest.get("security_audits")
    if not isinstance(security_audits, list) or len(security_audits) != 4:
        errors.append("security_audits must contain exactly 4 entries")
    if set(manifest.get("gates", {})) != {
        "evidence_uniqueness",
        "lane_dag",
        "observation_coverage",
    }:
        errors.append("gate contract keys are incomplete or unexpected")
    append_only = manifest.get("append_only", {})
    if append_only.get("deletions_allowed") is not False:
        errors.append("append_only.deletions_allowed must be false")
    if append_only.get("historical_artifacts_rewritten") is not False:
        errors.append("append_only.historical_artifacts_rewritten must be false")
    details = {
        "required_documentation": len(required_docs) if isinstance(required_docs, list) else None,
        "token_vazio_entries": len(token_entries) if isinstance(token_entries, list) else None,
        "audit_logs": len(audit_logs) if isinstance(audit_logs, list) else None,
        "security_audits": len(security_audits) if isinstance(security_audits, list) else None,
        "errors": errors,
    }
    return not errors, (
        "manifest schema, cardinalities, IDs, and append-only flags are coherent"
        if not errors
        else "; ".join(errors)
    ), details


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_under_root(root: Path, relative: str) -> Path:
    root = root.resolve()
    path = (root / relative).resolve()
    if path != root and root not in path.parents:
        raise ValueError(f"path escapes repository root: {relative}")
    return path


def check_claim_allowed(root: Path, manifest: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    errors: list[str] = []
    checked = [("manifest", manifest.get("claim_allowed"))]
    if manifest.get("claim_allowed") is not False:
        errors.append("manifest.claim_allowed must be false")
    claim_state = manifest.get("claim_state", {})
    if claim_state.get("expected") is not False:
        errors.append("claim_state.expected must be false")
    for relative in claim_state.get("files", []):
        path = resolve_under_root(root, relative)
        if not path.is_file():
            errors.append(f"missing claim-state file: {relative}")
            continue
        try:
            data = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{relative}: invalid JSON ({exc})")
            continue
        value = data.get("claim_allowed") if isinstance(data, dict) else None
        checked.append((relative, value))
        if value is not False:
            errors.append(f"{relative}.claim_allowed={value!r}, expected false")
    details = {"checked": checked, "errors": errors}
    return not errors, (
        "claim_allowed=false enforced in manifest and state files"
        if not errors
        else "; ".join(errors)
    ), details


def check_documentation(root: Path, manifest: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    errors: list[str] = []
    checked = 0
    for item in manifest.get("required_documentation", []):
        checked += 1
        relative = item.get("path", "")
        path = resolve_under_root(root, relative)
        if not path.is_file():
            errors.append(f"{item.get('id')}: missing {relative}")
            continue
        content = path.read_text(encoding="utf-8")
        for marker in item.get("markers", []):
            if marker not in content:
                errors.append(f"{item.get('id')}: marker missing: {marker}")
    details = {"checked": checked, "errors": errors}
    return not errors, (
        f"{checked} required documentation artifacts present and marker-bound"
        if not errors
        else "; ".join(errors)
    ), details


def check_falsifiers(root: Path, manifest: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    del root
    errors: list[str] = []
    checked = 0
    for item in manifest.get("token_vazio_entries", []):
        checked += 1
        if item.get("status") != "TOKEN_VAZIO":
            errors.append(f"{item.get('id')}: status is not TOKEN_VAZIO")
        if item.get("claim_allowed") is not False:
            errors.append(f"{item.get('id')}: claim_allowed must be false")
        if not isinstance(item.get("falsifier"), str) or not item["falsifier"].strip():
            errors.append(f"{item.get('id')}: missing falsifier")
        if not isinstance(item.get("next_verifiable_step"), str) or not item["next_verifiable_step"].strip():
            errors.append(f"{item.get('id')}: missing next_verifiable_step")
    details = {"checked": checked, "errors": errors}
    return not errors, (
        f"{checked} TOKEN_VAZIO entries have falsifier, next_verifiable_step, and claim boundary"
        if not errors
        else "; ".join(errors)
    ), details


def check_token_locations(root: Path, manifest: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    errors: list[str] = []
    checked = 0
    for item in manifest.get("token_vazio_entries", []):
        checked += 1
        for field in ("source", "approval_location"):
            location = item.get(field, {})
            relative = location.get("path", "")
            marker = location.get("marker", "")
            path = resolve_under_root(root, relative)
            if not path.is_file():
                errors.append(f"{item.get('id')}.{field}: missing {relative}")
                continue
            content = path.read_text(encoding="utf-8")
            if marker not in content:
                errors.append(f"{item.get('id')}.{field}: marker missing: {marker}")
    details = {"checked": checked, "errors": errors}
    return not errors, (
        f"{checked} TOKEN_VAZIO source and approval locations resolve"
        if not errors
        else "; ".join(errors)
    ), details


def _walk_evidence_ids(value: Any, path: str = "$"):
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key == "evidence_id" and isinstance(child, str) and child:
                yield child, child_path
            yield from _walk_evidence_ids(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_evidence_ids(child, f"{path}[{index}]")


def check_evidence_uniqueness(root: Path, config: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    seen: dict[str, str] = {}
    duplicates: list[str] = []
    errors: list[str] = []
    files_checked = 0
    for relative in config.get("files", []):
        files_checked += 1
        path = resolve_under_root(root, relative)
        if not path.is_file():
            errors.append(f"missing evidence file: {relative}")
            continue
        try:
            payload = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{relative}: invalid JSON ({exc})")
            continue
        for evidence_id, location in _walk_evidence_ids(payload):
            if evidence_id in seen:
                duplicates.append(f"{evidence_id}: {seen[evidence_id]} and {relative}{location}")
            else:
                seen[evidence_id] = f"{relative}{location}"
    errors.extend(duplicates)
    details = {
        "files_checked": files_checked,
        "unique_evidence_ids": len(seen),
        "duplicates": duplicates,
        "errors": errors,
    }
    return not errors, (
        f"{len(seen)} unique evidence_id values across {files_checked} files"
        if not errors
        else "; ".join(errors)
    ), details


def check_lane_dag(config: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    nodes = set(config.get("nodes", []))
    dependencies = config.get("dependencies", {})
    errors: list[str] = []
    if nodes != set(dependencies):
        errors.append("lane nodes and dependency keys differ")
    for node, deps in dependencies.items():
        unknown = set(deps) - nodes
        if unknown:
            errors.append(f"{node}: unknown dependency {sorted(unknown)}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            raise ValueError(f"cycle detected at {node}")
        if node in visited:
            return
        visiting.add(node)
        for dependency in dependencies.get(node, []):
            visit(dependency)
        visiting.remove(node)
        visited.add(node)

    if not errors:
        try:
            for node in nodes:
                visit(node)
        except ValueError as exc:
            errors.append(str(exc))
    details = {
        "nodes": sorted(nodes),
        "visited": sorted(visited),
        "errors": errors,
    }
    return not errors, (
        f"lane DAG is acyclic ({len(nodes)} nodes)"
        if not errors
        else "; ".join(errors)
    ), details


def check_observation_coverage(root: Path, config: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    relative = config.get("path", "")
    path = resolve_under_root(root, relative)
    errors: list[str] = []
    rows: dict[str, str] = {}
    if not path.is_file():
        errors.append(f"missing observation matrix: {relative}")
    else:
        content = path.read_text(encoding="utf-8")
        for line in content.splitlines():
            match = re.match(r"^\|\s*(O[0-9]+)\s*\|", line)
            if match:
                rows[match.group(1)] = line
        for observation in config.get("observations", []):
            row = rows.get(observation)
            if row is None:
                errors.append(f"{observation}: row missing")
                continue
            if not any(token in row for token in STATE_TOKENS):
                errors.append(f"{observation}: no evidence state or TOKEN_VAZIO in row")
    details = {
        "required": list(config.get("observations", [])),
        "rows_found": sorted(rows),
        "errors": errors,
    }
    return not errors, (
        f"{len(config.get('observations', []))} observations have explicit state rows"
        if not errors
        else "; ".join(errors)
    ), details


def check_audit_logs(root: Path, entries: list[dict[str, Any]]) -> tuple[bool, str, dict[str, Any]]:
    errors: list[str] = []
    checked: list[dict[str, Any]] = []
    for item in entries:
        relative = item.get("path", "")
        path = resolve_under_root(root, relative)
        record_count = 0
        if not path.is_file():
            errors.append(f"{item.get('id')}: missing {relative}")
        else:
            try:
                if item.get("format") == "jsonl":
                    records = [
                        json.loads(line)
                        for line in path.read_text(encoding="utf-8").splitlines()
                        if line.strip()
                    ]
                    record_count = len(records)
                elif item.get("format") == "json":
                    json.loads(path.read_text(encoding="utf-8"))
                    record_count = 1
                else:
                    errors.append(f"{item.get('id')}: unsupported format")
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"{item.get('id')}: invalid {item.get('format')} ({exc})")
        if record_count < int(item.get("minimum_records", 1)):
            errors.append(f"{item.get('id')}: {record_count} records below minimum")
        checked.append({"id": item.get("id"), "path": relative, "records": record_count})
    details = {"checked": checked, "errors": errors}
    return not errors, (
        f"{len(checked)} append-only audit logs are readable"
        if not errors
        else "; ".join(errors)
    ), details


def run_checks(root: Path, manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    checks: dict[str, dict[str, Any]] = {}

    def add(name: str, function: Callable[[], tuple[bool, str, dict[str, Any]]]) -> None:
        try:
            ok, message, details = function()
        except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            ok, message, details = False, f"validator exception: {exc}", {"errors": [str(exc)]}
        checks[name] = {
            "status": "PASS" if ok else "FAIL",
            "message": message,
            "details": details,
        }

    add("manifest_contract", lambda: check_manifest_contract(root, manifest))
    add("claim_allowed", lambda: check_claim_allowed(root, manifest))
    add("documentation", lambda: check_documentation(root, manifest))
    add("falsifiers", lambda: check_falsifiers(root, manifest))
    add("token_locations", lambda: check_token_locations(root, manifest))
    add(
        "evidence_uniqueness",
        lambda: check_evidence_uniqueness(root, manifest["gates"]["evidence_uniqueness"]),
    )
    add("lane_dag", lambda: check_lane_dag(manifest["gates"]["lane_dag"]))
    add(
        "observation_coverage",
        lambda: check_observation_coverage(root, manifest["gates"]["observation_coverage"]),
    )
    add("audit_logs", lambda: check_audit_logs(root, manifest["audit_logs"]))
    return checks


def build_receipt(root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    checks = run_checks(root, manifest)
    failed = [name for name, result in checks.items() if result["status"] != "PASS"]
    foundation_failed = [
        name for name in FOUNDATION_GATES
        if checks.get(name, {}).get("status") != "PASS"
    ]
    observed_head = manifest.get("baseline", {}).get("provider_reference_head")
    try:
        observed_head = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip() or observed_head
    except (OSError, subprocess.CalledProcessError):
        pass
    return {
        "schema": "rafaelia.phase-0-foundation-validation-receipt/v2",
        "manifest_id": manifest.get("manifest_id"),
        "repository": manifest.get("repository"),
        "observed_head": observed_head,
        "provider_reference_head": manifest.get("baseline", {}).get("provider_reference_head"),
        "claim_allowed": False,
        "status": "PASS" if not failed else "FAIL",
        "checks": checks,
        "summary": {
            "checks_total": len(checks),
            "checks_passed": len(checks) - len(failed),
            "checks_failed": len(failed),
            "failed_checks": failed,
            "foundation_gates_total": len(FOUNDATION_GATES),
            "foundation_gates_failed": foundation_failed,
        },
        "boundary": "documentation, manifest, custody, and validation structure only; no physical runtime or scientific promotion",
        "f_ok": "strict Phase 0 foundation checks executed against current checkout",
        "f_gap": failed or [
            "historical 106-test count is not a reproducible current-suite claim",
            "physical runtime and global exhaustivity remain outside this gate",
        ],
        "f_next": "append a new receipt when an open falsifier or the requested non-regression scope is reproduced",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("data/control-plane/phase_0_foundation_manifest.v1.json"),
    )
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    manifest_path = args.manifest if args.manifest.is_absolute() else root / args.manifest
    try:
        manifest = load_json(manifest_path)
        receipt = build_receipt(root, manifest)
    except (OSError, json.JSONDecodeError, TypeError) as exc:
        print(f"PHASE_0_V2_FAIL: {exc}", file=sys.stderr)
        return 2
    if args.receipt:
        output = args.receipt if args.receipt.is_absolute() else root / args.receipt
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
