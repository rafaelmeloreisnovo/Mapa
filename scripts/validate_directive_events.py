#!/usr/bin/env python3
"""Validate append-only RAFAELIA DIRECTIVE_EVENT records with stdlib only."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any

SCHEMA = "rafaelia.directive-event/v1"
SCOPES = {"TURN","SESSION","PROJECT","REPOSITORY","CROSS_SOURCE"}
EFFECTS = {"INTERPRET","ROUTE","WRITE","BLOCK"}
SYSTEMS = {"GITHUB","GOOGLE_DRIVE"}
OPERATIONS = {"CREATE","UPDATE","APPEND"}
HEX = set("0123456789abcdef")

def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in HEX for c in value)

def validate_event(event: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(event, dict):
        return ["event must be an object"]
    required = {
        "schema_version","record_type","directive_id","declared_by","declared_at",
        "source","summary","scope","effects","authorization","target_surfaces",
        "effective_from","retroactive","supersedes","classification","invariants",
        "f_gap","f_next",
    }
    missing = sorted(required - set(event))
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))
    if event.get("schema_version") != SCHEMA:
        errors.append("schema_version mismatch")
    if event.get("record_type") != "DIRECTIVE_EVENT":
        errors.append("record_type must be DIRECTIVE_EVENT")
    directive_id = event.get("directive_id")
    if not isinstance(directive_id, str) or not directive_id.startswith("dir:"):
        errors.append("directive_id must start with dir:")
    if event.get("declared_by") != "USER":
        errors.append("declared_by must be USER")
    for field in ("declared_at","effective_from","summary"):
        if not isinstance(event.get(field), str) or not event[field].strip():
            errors.append(f"{field} must be non-empty")

    source = event.get("source")
    if not isinstance(source, dict):
        errors.append("source must be an object")
    else:
        if source.get("system") != "SESSION":
            errors.append("source.system must be SESSION")
        if not isinstance(source.get("locator"), str) or not source["locator"].strip():
            errors.append("source.locator must be non-empty")
        if not is_sha256(source.get("content_sha256")):
            errors.append("source.content_sha256 must be 64 lowercase hex chars")
        length = source.get("byte_length")
        if not isinstance(length, int) or isinstance(length, bool) or length < 1:
            errors.append("source.byte_length must be a positive integer")

    scope = event.get("scope")
    if not isinstance(scope, list) or not scope or len(scope) != len(set(scope)) or any(x not in SCOPES for x in scope):
        errors.append("scope must be a unique non-empty list of allowed values")
    effects = event.get("effects")
    if not isinstance(effects, list) or not effects or len(effects) != len(set(effects)) or any(x not in EFFECTS for x in effects):
        errors.append("effects must be a unique non-empty list; PROMOTE is forbidden")

    authorization = event.get("authorization")
    if not isinstance(authorization, dict):
        errors.append("authorization must be an object")
        authorization = {}
    for key in ("github_read","github_write","drive_read","drive_write"):
        if not isinstance(authorization.get(key), bool):
            errors.append(f"authorization.{key} must be boolean")
    for key in ("destructive_actions","automatic_merge","claim_promotion","external_messages"):
        if authorization.get(key) is not False:
            errors.append(f"authorization.{key} must remain false")
    if isinstance(effects, list) and "WRITE" in effects and not (
        authorization.get("github_write") is True or authorization.get("drive_write") is True
    ):
        errors.append("WRITE effect requires scoped GitHub or Drive write authorization")

    targets = event.get("target_surfaces")
    if not isinstance(targets, list) or not targets:
        errors.append("target_surfaces must be non-empty")
    else:
        for pos, target in enumerate(targets):
            label = f"target_surfaces[{pos}]"
            if not isinstance(target, dict):
                errors.append(f"{label} must be an object")
                continue
            system = target.get("system")
            operation = target.get("operation")
            if system not in SYSTEMS:
                errors.append(f"{label}.system is invalid")
            if operation not in OPERATIONS:
                errors.append(f"{label}.operation is invalid or destructive")
            if not isinstance(target.get("locator"), str) or not target["locator"].strip():
                errors.append(f"{label}.locator must be non-empty")
            if system == "GITHUB" and authorization.get("github_write") is not True:
                errors.append(f"{label} requires github_write=true")
            if system == "GOOGLE_DRIVE" and authorization.get("drive_write") is not True:
                errors.append(f"{label} requires drive_write=true")

    if event.get("retroactive") is not False:
        errors.append("retroactive must remain false")
    supersedes = event.get("supersedes")
    if supersedes != "TOKEN_VAZIO" and not (isinstance(supersedes, str) and supersedes.startswith("dir:")):
        errors.append("supersedes must be TOKEN_VAZIO or a directive id")

    classification = event.get("classification")
    if not isinstance(classification, dict):
        errors.append("classification must be an object")
    else:
        if classification.get("epistemic_state") != "DECLARED_BY_AUTHOR":
            errors.append("classification.epistemic_state must be DECLARED_BY_AUTHOR")
        if classification.get("claim_allowed") is not False:
            errors.append("classification.claim_allowed must remain false")
    invariants = event.get("invariants")
    if not isinstance(invariants, list) or not invariants or len(invariants) != len(set(invariants)):
        errors.append("invariants must be unique and non-empty")
    if not isinstance(event.get("f_gap"), list):
        errors.append("f_gap must be an array")
    if not isinstance(event.get("f_next"), list) or not event["f_next"]:
        errors.append("f_next must be a non-empty array")
    return errors

def load_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    events: list[dict[str, Any]] = []
    errors: list[str] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"line {number}: invalid JSON at column {exc.colno}")
            continue
        events.append(value)
    if not events:
        errors.append("directive event file must not be empty")
    return events, errors

def build_report(path: Path) -> dict[str, Any]:
    try:
        events, errors = load_jsonl(path)
    except Exception as exc:
        events, errors = [], [f"load failure: {exc}"]
    ids: set[str] = set()
    for pos, event in enumerate(events, 1):
        errors.extend(f"event {pos}: {x}" for x in validate_event(event))
        identifier = event.get("directive_id") if isinstance(event, dict) else None
        if isinstance(identifier, str):
            if identifier in ids:
                errors.append(f"event {pos}: duplicate directive_id {identifier}")
            ids.add(identifier)
    digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
    return {
        "schema_version":"rafaelia.directive-event-report/v1",
        "status":"PASS" if not errors else "FAIL",
        "claim_allowed":False,
        "event_count":len(events),
        "file_sha256":digest,
        "defects":errors,
        "boundary":"Directive validation proves explicit routing and authorization boundaries only; it does not prove execution, claim validity, or conformity.",
    }

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=root / "data/directives/directive_events.20260803.jsonl")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = build_report(args.events)
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    return 0 if report["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
