#!/usr/bin/env python3
"""Validate RAFAELIA authorship/provenance records using only the stdlib.

The validator distinguishes structural validity from epistemic promotion. A record may
be structurally valid while correctly remaining promotion_allowed=false because it
contains TOKEN_VAZIO blockers.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

REQUIRED_RECORD_KEYS = {
    "schema_version",
    "record_id",
    "recorded_at",
    "artifact",
    "roles",
    "origin_chain",
    "originality_state",
    "rights_state",
    "decision",
}

REQUIRED_ARTIFACT_KEYS = {
    "artifact_id",
    "locator",
    "revision",
    "media_type",
    "content_digest",
}

REQUIRED_DECISION_KEYS = {
    "authorship_complete",
    "attribution_complete",
    "plagiarism_risk",
    "promotion_allowed",
    "claim_allowed",
    "blocking_token_vazio",
}

VALID_ROLES = {
    "AUTHOR",
    "COAUTHOR",
    "SOURCE_AUTHOR",
    "CONTRIBUTOR",
    "SOFTWARE_DEVELOPER",
    "DATA_COLLECTOR",
    "EDITOR",
    "TRANSLATOR",
    "CURATOR",
    "REVIEWER",
    "PROJECT_CREATOR",
    "MAINTAINER",
    "INSTITUTION",
    "AI_ASSISTED_TOOL",
    "UNKNOWN",
}

VALID_RELATIONS = {
    "CREATED_BY",
    "DERIVED_FROM",
    "CITES",
    "ADAPTS",
    "TRANSLATES",
    "IMPLEMENTS",
    "REVIEWS",
    "CURATES",
    "REPRODUCES",
    "INSPIRED_BY",
    "GENERATED_WITH",
    "SUPERSEDES_WITHOUT_ERASURE",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: expected an object")
            records.append(value)
    return records


def _missing(container: dict[str, Any], required: Iterable[str]) -> list[str]:
    return sorted(key for key in required if key not in container)


def validate_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    record_id = str(record.get("record_id", "<unknown>"))

    missing = _missing(record, REQUIRED_RECORD_KEYS)
    if missing:
        return [f"{record_id}: missing record keys: {', '.join(missing)}"]

    if record.get("schema_version") != "rafaelia.authorship-provenance-record/v1":
        errors.append(f"{record_id}: unsupported schema_version")

    artifact = record.get("artifact")
    if not isinstance(artifact, dict):
        errors.append(f"{record_id}: artifact must be an object")
    else:
        missing_artifact = _missing(artifact, REQUIRED_ARTIFACT_KEYS)
        if missing_artifact:
            errors.append(
                f"{record_id}: missing artifact keys: {', '.join(missing_artifact)}"
            )
        digest = artifact.get("content_digest")
        if not isinstance(digest, dict) or not digest.get("algorithm") or not digest.get("value"):
            errors.append(f"{record_id}: content_digest requires algorithm and value")

    roles = record.get("roles")
    if not isinstance(roles, list) or not roles:
        errors.append(f"{record_id}: roles must contain at least one entry")
        roles = []

    has_unknown_role = False
    has_unresolved_identity = False
    for index, role in enumerate(roles):
        prefix = f"{record_id}: roles[{index}]"
        if not isinstance(role, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        role_name = role.get("role")
        if role_name not in VALID_ROLES:
            errors.append(f"{prefix}: invalid role {role_name!r}")
        if not str(role.get("contribution", "")).strip():
            errors.append(f"{prefix}: contribution is required")
        if role_name == "AI_ASSISTED_TOOL" and role.get("accountable") is not False:
            errors.append(f"{prefix}: AI_ASSISTED_TOOL must not be accountable author")
        if role_name == "UNKNOWN":
            has_unknown_role = True
        if role.get("identity_state") in {"TOKEN_VAZIO", "DISPUTED"}:
            has_unresolved_identity = True

    origin_chain = record.get("origin_chain")
    if not isinstance(origin_chain, list):
        errors.append(f"{record_id}: origin_chain must be an array")
        origin_chain = []
    for index, edge in enumerate(origin_chain):
        prefix = f"{record_id}: origin_chain[{index}]"
        if not isinstance(edge, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        if edge.get("relation") not in VALID_RELATIONS:
            errors.append(f"{prefix}: invalid relation")
        for key in ("source_locator", "source_revision", "source_author_state", "scope_used"):
            if not str(edge.get(key, "")).strip():
                errors.append(f"{prefix}: {key} is required")
        if edge.get("source_author_state") == "TOKEN_VAZIO" and edge.get("source_author"):
            errors.append(f"{prefix}: TOKEN_VAZIO source author cannot have asserted identity")

    rights = record.get("rights_state")
    if not isinstance(rights, dict):
        errors.append(f"{record_id}: rights_state must be an object")
        rights = {}
    if rights.get("moral_rights_preserved") is not True:
        errors.append(f"{record_id}: moral_rights_preserved must be true")

    decision = record.get("decision")
    if not isinstance(decision, dict):
        errors.append(f"{record_id}: decision must be an object")
        return errors
    missing_decision = _missing(decision, REQUIRED_DECISION_KEYS)
    if missing_decision:
        errors.append(f"{record_id}: missing decision keys: {', '.join(missing_decision)}")
        return errors

    blockers = decision.get("blocking_token_vazio")
    if not isinstance(blockers, list):
        errors.append(f"{record_id}: blocking_token_vazio must be an array")
        blockers = []
    for blocker in blockers:
        if not isinstance(blocker, str) or not blocker.startswith("TOKEN_VAZIO"):
            errors.append(f"{record_id}: invalid blocker {blocker!r}")

    permission_state = rights.get("permission_state")
    unresolved = bool(blockers) or permission_state in {"TOKEN_VAZIO", "DENIED", "DISPUTED"}
    unresolved = unresolved or has_unknown_role or has_unresolved_identity

    if unresolved and decision.get("promotion_allowed") is True:
        errors.append(f"{record_id}: unresolved authorship/rights cannot be promoted")
    if unresolved and decision.get("claim_allowed") is True:
        errors.append(f"{record_id}: unresolved authorship/rights cannot allow claims")

    if decision.get("authorship_complete") is True and (has_unknown_role or has_unresolved_identity):
        errors.append(f"{record_id}: authorship_complete conflicts with unresolved identity")

    if decision.get("promotion_allowed") is True:
        if decision.get("authorship_complete") is not True:
            errors.append(f"{record_id}: promotion requires authorship_complete")
        if decision.get("attribution_complete") is not True:
            errors.append(f"{record_id}: promotion requires attribution_complete")
        if decision.get("plagiarism_risk") not in {"NONE_OBSERVED", "LOW"}:
            errors.append(f"{record_id}: promotion requires bounded plagiarism risk")
        if blockers:
            errors.append(f"{record_id}: promotion requires no blocking TOKEN_VAZIO")
        if permission_state not in {"CONFIRMED", "NOT_REQUIRED"}:
            errors.append(f"{record_id}: promotion requires resolved permission_state")

    return errors


def validate_policy(policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if policy.get("principle") != "AUTHORSHIP_IS_INDISPENSABLE":
        errors.append("policy: AUTHORSHIP_IS_INDISPENSABLE is required")
    invariant = policy.get("authorship_invariant", {})
    required_invariants = {
        "origin is never silently replaced by the latest transmitter",
        "unknown or disputed authorship is TOKEN_VAZIO_AUTHORSHIP, never project ownership by default",
        "corrections supersede records but do not delete historical attribution",
    }
    actual = set(invariant.get("invariants", [])) if isinstance(invariant, dict) else set()
    missing = sorted(required_invariants - actual)
    if missing:
        errors.append("policy: missing invariants: " + "; ".join(missing))
    if policy.get("promotion_gate", {}).get("authorship_record_required") is not True:
        errors.append("policy: authorship_record_required must be true")
    if policy.get("perpetual_preservation", {}).get("deletion_of_authorship_history") is not False:
        errors.append("policy: deletion_of_authorship_history must be false")
    return errors


def validate_schema_contract(schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if schema.get("type") != "object":
        errors.append("schema: root type must be object")
    required = set(schema.get("required", []))
    missing = REQUIRED_RECORD_KEYS - required
    if missing:
        errors.append("schema: missing required keys: " + ", ".join(sorted(missing)))
    return errors


def build_report(policy_path: Path, schema_path: Path, registry_path: Path) -> dict[str, Any]:
    policy = load_json(policy_path)
    schema = load_json(schema_path)
    records = load_jsonl(registry_path)

    defects = validate_policy(policy) + validate_schema_contract(schema)
    for record in records:
        defects.extend(validate_record(record))

    blocker_count = sum(
        len(record.get("decision", {}).get("blocking_token_vazio", []))
        for record in records
    )
    promoted_count = sum(
        record.get("decision", {}).get("promotion_allowed") is True
        for record in records
    )

    return {
        "schema_version": "rafaelia.authorship-provenance-validation/v1",
        "status": "PASS" if not defects else "FAIL",
        "record_count": len(records),
        "promoted_count": promoted_count,
        "blocking_token_vazio_count": blocker_count,
        "defect_count": len(defects),
        "defects": defects,
        "boundary": (
            "PASS means the registry preserves authorship uncertainty consistently; "
            "it does not certify originality, ownership, legal compliance or absence of plagiarism."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    try:
        report = build_report(args.policy, args.schema, args.registry)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report = {
            "schema_version": "rafaelia.authorship-provenance-validation/v1",
            "status": "FAIL",
            "defect_count": 1,
            "defects": [str(exc)],
        }

    output = json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    print(output, end="")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output, encoding="utf-8")
    return 0 if report.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
