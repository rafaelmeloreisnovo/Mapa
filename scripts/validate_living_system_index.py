#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail-closed validator for indices/LIVING_SYSTEM_INDEX.json."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from build_living_system_index import (
    ALLOWED_STATES,
    MECHANISM_FIELDS,
    SCHEMA,
    SCHEMA_VERSION,
    LivingSystemError,
    canonical_digest,
    load_json,
    safe_repo_path,
    validate_cell,
)


def validate_index(document: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    if document.get("schema") != SCHEMA:
        errors.append(f"schema must be {SCHEMA}")
    if document.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if document.get("mechanism_fields") != list(MECHANISM_FIELDS):
        errors.append("mechanism_fields differ from the executable contract")

    policy = document.get("epistemic_policy")
    if not isinstance(policy, dict):
        errors.append("epistemic_policy must be an object")
    else:
        if policy.get("allowed_states") != sorted(ALLOWED_STATES):
            errors.append("allowed_states differ from executable contract")
        if policy.get("global_claim_allowed") is not False:
            errors.append("global_claim_allowed must remain false for partial inventory")

    repositories = document.get("repositories")
    if not isinstance(repositories, list):
        errors.append("repositories must be a list")
        repositories = []

    names: set[str] = set()
    ids: set[int] = set()
    resolved_total = 0
    token_total = 0
    claim_allowed_total = 0

    for index, repository in enumerate(repositories):
        prefix = f"repositories[{index}]"
        if not isinstance(repository, dict):
            errors.append(f"{prefix} must be an object")
            continue
        name = repository.get("repository_full_name")
        repo_id = repository.get("repository_id")
        if not isinstance(name, str) or "/" not in name:
            errors.append(f"{prefix}.repository_full_name is invalid")
        elif name in names:
            errors.append(f"duplicate repository_full_name: {name}")
        else:
            names.add(name)
        if not isinstance(repo_id, int) or isinstance(repo_id, bool):
            errors.append(f"{prefix}.repository_id is invalid")
        elif repo_id in ids:
            errors.append(f"duplicate repository_id: {repo_id}")
        else:
            ids.add(repo_id)

        identity = repository.get("identity")
        if not isinstance(identity, dict) or identity.get("state") != "FATO":
            errors.append(f"{prefix}.identity must remain FATO")

        mechanisms = repository.get("mechanisms")
        if not isinstance(mechanisms, dict):
            errors.append(f"{prefix}.mechanisms must be an object")
            continue
        if set(mechanisms) != set(MECHANISM_FIELDS):
            errors.append(f"{prefix}.mechanisms must contain exactly the contracted fields")
            continue

        token_count = 0
        hypothesis_count = 0
        parable_count = 0
        for field in MECHANISM_FIELDS:
            try:
                cell = validate_cell(mechanisms[field], f"{prefix}.{field}")
            except LivingSystemError as exc:
                errors.append(str(exc))
                continue
            token_count += cell["state"] == "TOKEN_VAZIO"
            hypothesis_count += cell["state"] == "HIPOTESE"
            parable_count += cell["state"] == "PARABOLA"

        resolved_count = len(MECHANISM_FIELDS) - token_count
        expected_completeness = {
            "resolved_fields": resolved_count,
            "total_fields": len(MECHANISM_FIELDS),
            "ratio": round(resolved_count / len(MECHANISM_FIELDS), 12),
            "hypothesis_fields": hypothesis_count,
            "parable_fields": parable_count,
            "token_vazio_fields": token_count,
        }
        if repository.get("completeness") != expected_completeness:
            errors.append(f"{prefix}.completeness differs from derived values")

        expected_claim = (
            token_count == 0
            and hypothesis_count == 0
            and parable_count == 0
            and bool(repository.get("profile_source"))
        )
        if repository.get("claim_allowed") != expected_claim:
            errors.append(f"{prefix}.claim_allowed differs from fail-closed rule")
        if repository.get("claim_allowed"):
            claim_allowed_total += 1
        resolved_total += resolved_count
        token_total += token_count

    stats = document.get("statistics")
    total_cells = len(repositories) * len(MECHANISM_FIELDS)
    expected_stats = {
        "repository_count": len(repositories),
        "profile_count": sum(
            bool(repo.get("profile_source")) for repo in repositories if isinstance(repo, dict)
        ),
        "mechanism_cell_count": total_cells,
        "resolved_cell_count": resolved_total,
        "token_vazio_cell_count": token_total,
        "knowledge_completeness_ratio": (
            round(resolved_total / total_cells, 12) if total_cells else 0.0
        ),
        "repository_claim_allowed_count": claim_allowed_total,
    }
    if stats != expected_stats:
        errors.append("statistics differ from derived values")

    declared_digest = document.get("integrity", {}).get("digest")
    calculated_digest = canonical_digest(document)
    if declared_digest != calculated_digest:
        errors.append("integrity digest mismatch")

    if token_total == 0:
        warnings.append(
            "no TOKEN_VAZIO remains; require independent review before enabling global claims"
        )

    return {
        "schema": "mapa_living_system_validation_v1",
        "ok": not errors,
        "errors": sorted(errors),
        "warnings": sorted(warnings),
        "derived": expected_stats,
        "integrity": {
            "algorithm": "blake2b-256",
            "declared": declared_digest,
            "calculated": calculated_digest,
            "match": declared_digest == calculated_digest,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the living-system mechanism index")
    parser.add_argument("--root", default=None)
    parser.add_argument("--index", default="indices/LIVING_SYSTEM_INDEX.json")
    parser.add_argument("--write-report", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    try:
        document = load_json(safe_repo_path(repo_root, args.index))
        report = validate_index(document)
    except LivingSystemError as exc:
        report = {
            "schema": "mapa_living_system_validation_v1",
            "ok": False,
            "errors": [str(exc)],
            "warnings": [],
        }
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    sys.stdout.write(rendered)
    if args.write_report:
        target = safe_repo_path(repo_root, args.write_report)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
