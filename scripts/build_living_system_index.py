#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the RAFAELIA living-system mechanism index using Python stdlib only.

The builder never infers repository behavior from its name. Connector-backed identity
is preserved as FATO, while unread mechanism fields become first-class TOKEN_VAZIO
records with an explicit next action and exit criterion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable

SCHEMA = "mapa_living_system_index_v1"
SCHEMA_VERSION = "1.0.0"
PROFILE_SCHEMA = "repository_mechanism_profile_v1"
ALLOWED_STATES = {"FATO", "HIPOTESE", "PARABOLA", "TOKEN_VAZIO"}
MECHANISM_FIELDS = (
    "purpose",
    "inputs",
    "transformations",
    "outputs",
    "interfaces",
    "invariants",
    "quality_controls",
    "risks",
    "relations",
    "philosophical_context",
    "visual_model",
)


class LivingSystemError(ValueError):
    """Raised when source data would make the generated index untrustworthy."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise LivingSystemError(f"cannot read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise LivingSystemError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise LivingSystemError(f"root must be an object: {path}")
    return data


def safe_repo_path(root: Path, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise LivingSystemError(f"unsafe repository-relative path: {relative!r}")
    resolved = (root / path).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise LivingSystemError(f"path escapes repository root: {relative!r}") from exc
    return resolved


def token_vazio(field: str, repository_full_name: str) -> dict[str, Any]:
    return {
        "state": "TOKEN_VAZIO",
        "reason": f"{field} has not yet been established from repository content evidence",
        "next_action": (
            f"inspect {repository_full_name} files relevant to {field} and register only "
            "claims supported by stable paths or commit-pinned evidence"
        ),
        "exit_criteria": (
            "replace TOKEN_VAZIO with FATO, HIPOTESE, or PARABOLA; include value and at "
            "least one evidence record; pass deterministic validation"
        ),
    }


def canonical_digest(document: dict[str, Any]) -> str:
    clone = deepcopy(document)
    clone.setdefault("integrity", {})["digest"] = ""
    payload = json.dumps(
        clone,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.blake2b(payload, digest_size=32).hexdigest()


def validate_repository_record(record: dict[str, Any], source: str) -> None:
    required = {
        "repository_full_name": str,
        "repository_id": int,
        "owner": str,
        "repository_name": str,
        "default_branch": str,
        "visibility": str,
        "archived": bool,
        "metadata_status": str,
        "claim_scope": str,
        "observed_via": str,
    }
    for key, expected in required.items():
        value = record.get(key)
        if expected is int and isinstance(value, bool):
            value = None
        if not isinstance(value, expected):
            raise LivingSystemError(f"{source}: invalid or missing {key}")
    if record["metadata_status"] != "FATO":
        raise LivingSystemError(f"{source}: repository identity must remain FATO")


def merge_repository_records(records: Iterable[tuple[dict[str, Any], str]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for record, source in records:
        validate_repository_record(record, source)
        name = record["repository_full_name"]
        previous = merged.get(name)
        if previous and previous["repository_id"] != record["repository_id"]:
            raise LivingSystemError(
                f"repository identity collision for {name}: "
                f"{previous['repository_id']} != {record['repository_id']}"
            )
        merged[name] = deepcopy(record)
    return [merged[name] for name in sorted(merged)]


def load_inventory_records(repo_root: Path, head_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    head = load_json(head_path)
    if head.get("schema") != "repository_inventory_head_v1":
        raise LivingSystemError("inventory head schema must be repository_inventory_head_v1")

    checkpoint_rel = head.get("checkpoint", {}).get("path")
    if not isinstance(checkpoint_rel, str):
        raise LivingSystemError("inventory head checkpoint.path is required")
    checkpoint = load_json(safe_repo_path(repo_root, checkpoint_rel))
    if checkpoint.get("schema") != "repository_inventory_v2":
        raise LivingSystemError("checkpoint schema must be repository_inventory_v2")

    sourced: list[tuple[dict[str, Any], str]] = []
    checkpoint_records = checkpoint.get("repositories")
    if not isinstance(checkpoint_records, list):
        raise LivingSystemError("checkpoint repositories must be a list")
    for index, record in enumerate(checkpoint_records):
        if not isinstance(record, dict):
            raise LivingSystemError(f"checkpoint repositories[{index}] must be an object")
        sourced.append((record, f"{checkpoint_rel}#{index}"))

    delta_paths: list[str] = []
    deltas = head.get("delta_batches", [])
    if not isinstance(deltas, list):
        raise LivingSystemError("inventory head delta_batches must be a list")
    for delta_index, delta_ref in enumerate(deltas):
        if not isinstance(delta_ref, dict) or not isinstance(delta_ref.get("path"), str):
            raise LivingSystemError(f"delta_batches[{delta_index}].path is required")
        delta_rel = delta_ref["path"]
        delta_paths.append(delta_rel)
        delta = load_json(safe_repo_path(repo_root, delta_rel))
        if delta.get("schema") != "repository_inventory_batch_v1":
            raise LivingSystemError(f"delta schema mismatch: {delta_rel}")
        delta_records = delta.get("records")
        if not isinstance(delta_records, list):
            raise LivingSystemError(f"delta records must be a list: {delta_rel}")
        for record_index, record in enumerate(delta_records):
            if not isinstance(record, dict):
                raise LivingSystemError(f"{delta_rel} records[{record_index}] must be an object")
            sourced.append((record, f"{delta_rel}#{record_index}"))

    records = merge_repository_records(sourced)
    declared_count = head.get("derived", {}).get("materialized_count")
    if declared_count != len(records):
        raise LivingSystemError(
            f"inventory head materialized_count={declared_count!r} but merged records={len(records)}"
        )

    provenance = {
        "inventory_head": str(head_path.relative_to(repo_root)),
        "checkpoint": checkpoint_rel,
        "delta_batches": delta_paths,
        "inventory_generated_at": head.get("generated_at"),
        "inventory_state": head.get("derived", {}).get("inventory_state"),
        "inventory_claim_allowed": head.get("derived", {}).get("claim_allowed"),
        "accessible_total_observed": head.get("derived", {}).get("accessible_total_observed"),
        "materialized_count": len(records),
        "remaining_token_vazio": head.get("derived", {}).get("remaining_token_vazio"),
    }
    return records, provenance


def validate_evidence(evidence: Any, prefix: str) -> None:
    if not isinstance(evidence, list) or not evidence:
        raise LivingSystemError(f"{prefix}: non-empty evidence list required")
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            raise LivingSystemError(f"{prefix}.evidence[{index}] must be an object")
        for key in ("kind", "locator", "claim_scope"):
            if not isinstance(item.get(key), str) or not item[key]:
                raise LivingSystemError(f"{prefix}.evidence[{index}].{key} is required")


def validate_cell(cell: Any, prefix: str) -> dict[str, Any]:
    if not isinstance(cell, dict):
        raise LivingSystemError(f"{prefix}: mechanism field must be an object")
    state = cell.get("state")
    if state not in ALLOWED_STATES:
        raise LivingSystemError(f"{prefix}: unsupported state {state!r}")

    normalized = deepcopy(cell)
    if state == "TOKEN_VAZIO":
        for key in ("reason", "next_action", "exit_criteria"):
            if not isinstance(cell.get(key), str) or not cell[key].strip():
                raise LivingSystemError(f"{prefix}: TOKEN_VAZIO requires {key}")
        if "value" in cell or "evidence" in cell:
            raise LivingSystemError(f"{prefix}: TOKEN_VAZIO cannot claim value or evidence")
    else:
        if "value" not in cell:
            raise LivingSystemError(f"{prefix}: {state} requires value")
        validate_evidence(cell.get("evidence"), prefix)
        if state == "FATO" and cell.get("confidence") not in (None, 1, 1.0):
            raise LivingSystemError(f"{prefix}: FATO confidence, when present, must equal 1")
        if state == "HIPOTESE":
            confidence = cell.get("confidence")
            if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
                raise LivingSystemError(f"{prefix}: HIPOTESE requires numeric confidence")
            if not 0 <= confidence < 1:
                raise LivingSystemError(f"{prefix}: HIPOTESE confidence must be in [0, 1)")
    return normalized


def load_profiles(profile_dir: Path) -> dict[str, dict[str, Any]]:
    profiles: dict[str, dict[str, Any]] = {}
    if not profile_dir.exists():
        return profiles
    for path in sorted(profile_dir.glob("*.json")):
        profile = load_json(path)
        if profile.get("schema") != PROFILE_SCHEMA:
            raise LivingSystemError(f"{path}: schema must be {PROFILE_SCHEMA}")
        repository_full_name = profile.get("repository_full_name")
        if not isinstance(repository_full_name, str) or "/" not in repository_full_name:
            raise LivingSystemError(f"{path}: repository_full_name is invalid")
        if repository_full_name in profiles:
            raise LivingSystemError(f"duplicate profile for {repository_full_name}")
        mechanisms = profile.get("mechanisms")
        if not isinstance(mechanisms, dict):
            raise LivingSystemError(f"{path}: mechanisms must be an object")
        unknown = sorted(set(mechanisms) - set(MECHANISM_FIELDS))
        if unknown:
            raise LivingSystemError(f"{path}: unknown mechanism fields: {unknown}")
        normalized = deepcopy(profile)
        normalized["mechanisms"] = {
            key: validate_cell(value, f"{path.name}.{key}")
            for key, value in sorted(mechanisms.items())
        }
        profiles[repository_full_name] = normalized
    return profiles


def build_repository_entry(record: dict[str, Any], profile: dict[str, Any] | None) -> dict[str, Any]:
    repository_full_name = record["repository_full_name"]
    supplied = profile.get("mechanisms", {}) if profile else {}
    mechanisms = {
        field: deepcopy(supplied[field]) if field in supplied else token_vazio(field, repository_full_name)
        for field in MECHANISM_FIELDS
    }
    resolved_count = sum(cell["state"] != "TOKEN_VAZIO" for cell in mechanisms.values())
    hypothesis_count = sum(cell["state"] == "HIPOTESE" for cell in mechanisms.values())
    parable_count = sum(cell["state"] == "PARABOLA" for cell in mechanisms.values())
    empty_count = len(MECHANISM_FIELDS) - resolved_count

    return {
        "repository_full_name": repository_full_name,
        "repository_id": record["repository_id"],
        "identity": {
            "state": "FATO",
            "owner": record["owner"],
            "repository_name": record["repository_name"],
            "default_branch": record["default_branch"],
            "visibility": record["visibility"],
            "archived": record["archived"],
            "claim_scope": record["claim_scope"],
            "observed_via": record["observed_via"],
        },
        "profile_source": profile.get("profile_source") if profile else None,
        "mechanisms": mechanisms,
        "completeness": {
            "resolved_fields": resolved_count,
            "total_fields": len(MECHANISM_FIELDS),
            "ratio": round(resolved_count / len(MECHANISM_FIELDS), 12),
            "hypothesis_fields": hypothesis_count,
            "parable_fields": parable_count,
            "token_vazio_fields": empty_count,
        },
        "claim_allowed": bool(profile) and empty_count == 0 and hypothesis_count == 0 and parable_count == 0,
    }


def build_index(repo_root: Path, head_path: Path, profile_dir: Path) -> dict[str, Any]:
    records, provenance = load_inventory_records(repo_root, head_path)
    profiles = load_profiles(profile_dir)
    record_names = {record["repository_full_name"] for record in records}
    orphan_profiles = sorted(set(profiles) - record_names)
    if orphan_profiles:
        raise LivingSystemError(f"profiles without inventory identity: {orphan_profiles}")

    repositories = [
        build_repository_entry(record, profiles.get(record["repository_full_name"]))
        for record in records
    ]
    resolved = sum(item["completeness"]["resolved_fields"] for item in repositories)
    total = len(repositories) * len(MECHANISM_FIELDS)
    token_vazio_count = sum(item["completeness"]["token_vazio_fields"] for item in repositories)
    claim_allowed_count = sum(bool(item["claim_allowed"]) for item in repositories)

    document: dict[str, Any] = {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "generated_at": provenance["inventory_generated_at"],
        "epistemic_policy": {
            "allowed_states": sorted(ALLOWED_STATES),
            "rule": "repository names never imply behavior; unread mechanisms remain TOKEN_VAZIO",
            "promotion": "evidence is mandatory for FATO, HIPOTESE, and PARABOLA",
            "global_claim_allowed": False,
        },
        "source": provenance,
        "mechanism_fields": list(MECHANISM_FIELDS),
        "statistics": {
            "repository_count": len(repositories),
            "profile_count": len(profiles),
            "mechanism_cell_count": total,
            "resolved_cell_count": resolved,
            "token_vazio_cell_count": token_vazio_count,
            "knowledge_completeness_ratio": round(resolved / total, 12) if total else 0.0,
            "repository_claim_allowed_count": claim_allowed_count,
        },
        "repositories": repositories,
        "integrity": {
            "algorithm": "blake2b-256",
            "canonicalization": "json-sort-keys-utf8; integrity.digest blanked",
            "digest": "",
        },
    }
    document["integrity"]["digest"] = canonical_digest(document)
    return document


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build deterministic living-system mechanism index")
    parser.add_argument("--root", default=None, help="repository root; defaults to parent of scripts/")
    parser.add_argument("--head", default="indices/REPOSITORY_INVENTORY_HEAD.json")
    parser.add_argument("--profiles", default="data/mechanisms/profiles")
    parser.add_argument("--output", default="indices/LIVING_SYSTEM_INDEX.json")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="write canonical output")
    mode.add_argument("--check", action="store_true", help="fail if output differs")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    try:
        document = build_index(
            repo_root,
            safe_repo_path(repo_root, args.head),
            safe_repo_path(repo_root, args.profiles),
        )
        rendered = json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        output_path = safe_repo_path(repo_root, args.output)
        if args.write:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")
        elif args.check:
            if not output_path.is_file():
                raise LivingSystemError(f"generated index is missing: {args.output}")
            if output_path.read_text(encoding="utf-8") != rendered:
                raise LivingSystemError(
                    f"generated index is stale: run {Path(__file__).name} --write"
                )
        else:
            sys.stdout.write(rendered)
    except LivingSystemError as exc:
        sys.stderr.write(f"living-system build failed: {exc}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
