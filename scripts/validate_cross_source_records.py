#!/usr/bin/env python3
"""Validate RAFAELIA cross-source records using only the Python standard library.

This validator enforces the operational invariants that must remain true even when
no third-party JSON Schema engine is installed. The JSON Schema remains the
canonical structural contract; this script is the deterministic repository gate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "rafaelia.cross-source-record/v1"
PROVIDERS = {"github", "google_drive", "termux", "session"}
NODE_TYPES = {
    "repository", "file", "document", "folder", "commit", "pr", "workflow",
    "dataset", "log", "claim", "action", "session", "directive",
}
EPISTEMIC_STATES = {
    "FATO", "VERIFIED_LIMITED", "CONVENCAO", "HIPOTESE", "SIMBOLICO",
    "TOKEN_VAZIO", "CONTRADICTION",
}
EVIDENCE_MODES = {"DEMONSTRACAO", "CONVENCAO", "HIPOTESE", "PARABOLA", "VAZIO"}
SENSITIVITIES = {"PUBLIC", "PRIVATE", "RESTRICTED", "EXCLUDED"}
RELATIONS = {
    "IMPLEMENTS", "EVIDENCES", "DERIVES_FROM", "INDEXES", "VALIDATES",
    "CONTRADICTS", "SUPERSEDES", "MIRRORS", "REQUIRES", "PRODUCES",
    "BLOCKS", "MENTIONS",
}
RELATION_STATES = {"OBSERVED", "DECLARED", "INFERRED", "TOKEN_VAZIO"}
EVIDENCE_KINDS = {
    "commit", "blob", "file", "document", "revision", "hash", "log",
    "measurement", "test", "review", "source",
}
ACTORS = {"human", "assistant", "workflow", "script"}
OPERATIONS = {"READ", "CREATE", "UPDATE", "VALIDATE", "TOKEN_VAZIO"}
HEX40 = set("0123456789abcdef")


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_lower_hex(value: Any, length: int) -> bool:
    return (
        isinstance(value, str)
        and len(value) == length
        and all(char in HEX40 for char in value)
    )


def _require_mapping(record: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = record.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be an object")
        return {}
    return value


def _require_list(record: dict[str, Any], key: str, errors: list[str]) -> list[Any]:
    value = record.get(key)
    if not isinstance(value, list):
        errors.append(f"{key} must be an array")
        return []
    return value


def validate_record(record: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["record must be an object"]

    required = {
        "schema_version", "record_id", "node_type", "canonical_owner", "source",
        "version", "classification", "evidence_refs", "relations", "custody",
        "next_verifiable_step",
    }
    missing = sorted(required - set(record))
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))

    if record.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must equal {SCHEMA_VERSION}")

    record_id = record.get("record_id")
    if not (_is_nonempty_string(record_id) and record_id.startswith("rec:")):
        errors.append("record_id must be a non-empty rec: identifier")

    if record.get("node_type") not in NODE_TYPES:
        errors.append("node_type is invalid")

    if not _is_nonempty_string(record.get("canonical_owner")):
        errors.append("canonical_owner must be non-empty")

    if not _is_nonempty_string(record.get("next_verifiable_step")):
        errors.append("next_verifiable_step must be non-empty")

    source = _require_mapping(record, "source", errors)
    provider = source.get("provider")
    if provider not in PROVIDERS:
        errors.append("source.provider is invalid")
    for field in ("account_scope", "locator", "observed_at"):
        if not _is_nonempty_string(source.get(field)):
            errors.append(f"source.{field} must be non-empty")

    provider_fields = {
        "github": "repository_full_name",
        "google_drive": "drive_file_id",
        "termux": "termux_path",
        "session": "session_id",
    }
    selected = provider_fields.get(provider)
    if selected and not _is_nonempty_string(source.get(selected)):
        errors.append(f"source.{selected} is required for provider {provider}")

    for candidate in provider_fields.values():
        if candidate == selected:
            continue
        if source.get(candidate) not in (None, ""):
            errors.append(f"source.{candidate} must be null outside its provider")

    if provider == "github":
        repository = source.get("repository_full_name")
        if _is_nonempty_string(repository) and repository.count("/") != 1:
            errors.append("source.repository_full_name must be owner/repository")
        if not _is_nonempty_string(source.get("path")):
            errors.append("source.path is required for provider github")
    elif source.get("path") not in (None, ""):
        errors.append("source.path must be null outside provider github")

    termux_path = source.get("termux_path")
    if isinstance(termux_path, str):
        parts = termux_path.replace("\\", "/").split("/")
        if ".." in parts:
            errors.append("source.termux_path must not contain parent traversal")

    version = _require_mapping(record, "version", errors)
    for field in ("git_ref", "drive_revision_id"):
        if not _is_nonempty_string(version.get(field)):
            errors.append(f"version.{field} must be non-empty")
    for field in ("commit_sha", "blob_sha"):
        value = version.get(field)
        if value != "TOKEN_VAZIO" and not _is_lower_hex(value, 40):
            errors.append(f"version.{field} must be TOKEN_VAZIO or 40 lowercase hex chars")

    content_hash = version.get("content_hash")
    if not isinstance(content_hash, dict):
        errors.append("version.content_hash must be an object")
    else:
        algorithm = content_hash.get("algorithm")
        value = content_hash.get("value")
        if algorithm == "TOKEN_VAZIO":
            if value != "TOKEN_VAZIO":
                errors.append("TOKEN_VAZIO hash algorithm requires TOKEN_VAZIO value")
        elif algorithm in {"sha256", "blake3"}:
            if not _is_lower_hex(value, 64):
                errors.append(f"{algorithm} content hash must be 64 lowercase hex chars")
        else:
            errors.append("version.content_hash.algorithm is invalid")

    classification = _require_mapping(record, "classification", errors)
    state = classification.get("epistemic_state")
    mode = classification.get("evidence_mode")
    claim_allowed = classification.get("claim_allowed")
    if not _is_nonempty_string(classification.get("domain")):
        errors.append("classification.domain must be non-empty")
    if state not in EPISTEMIC_STATES:
        errors.append("classification.epistemic_state is invalid")
    if mode not in EVIDENCE_MODES:
        errors.append("classification.evidence_mode is invalid")
    if not isinstance(claim_allowed, bool):
        errors.append("classification.claim_allowed must be boolean")
    if classification.get("sensitivity") not in SENSITIVITIES:
        errors.append("classification.sensitivity is invalid")

    evidence_refs = _require_list(record, "evidence_refs", errors)
    evidence_ids: set[str] = set()
    for index, evidence in enumerate(evidence_refs):
        prefix = f"evidence_refs[{index}]"
        if not isinstance(evidence, dict):
            errors.append(f"{prefix} must be an object")
            continue
        evidence_id = evidence.get("evidence_id")
        if not (_is_nonempty_string(evidence_id) and evidence_id.startswith("ev:")):
            errors.append(f"{prefix}.evidence_id must be an ev: identifier")
        elif evidence_id in evidence_ids:
            errors.append(f"{prefix}.evidence_id is duplicated")
        else:
            evidence_ids.add(evidence_id)
        if evidence.get("kind") not in EVIDENCE_KINDS:
            errors.append(f"{prefix}.kind is invalid")
        if not _is_nonempty_string(evidence.get("reference")):
            errors.append(f"{prefix}.reference must be non-empty")

    relations = _require_list(record, "relations", errors)
    for index, relation in enumerate(relations):
        prefix = f"relations[{index}]"
        if not isinstance(relation, dict):
            errors.append(f"{prefix} must be an object")
            continue
        if relation.get("predicate") not in RELATIONS:
            errors.append(f"{prefix}.predicate is invalid")
        target_id = relation.get("target_id")
        if not (_is_nonempty_string(target_id) and target_id.startswith("rec:")):
            errors.append(f"{prefix}.target_id must be a rec: identifier")
        evidence_id = relation.get("evidence_id")
        if evidence_id != "TOKEN_VAZIO" and evidence_id not in evidence_ids:
            errors.append(f"{prefix}.evidence_id must resolve locally or be TOKEN_VAZIO")
        weight = relation.get("weight_q16")
        if not isinstance(weight, int) or isinstance(weight, bool) or not 0 <= weight <= 65535:
            errors.append(f"{prefix}.weight_q16 must be an integer from 0 to 65535")
        if relation.get("state") not in RELATION_STATES:
            errors.append(f"{prefix}.state is invalid")

    custody = _require_mapping(record, "custody", errors)
    if custody.get("actor") not in ACTORS:
        errors.append("custody.actor is invalid")
    operation = custody.get("operation")
    if operation not in OPERATIONS:
        errors.append("custody.operation is invalid")
    for field in ("event_id", "previous_event_id"):
        value = custody.get(field)
        if value != "TOKEN_VAZIO" and not (
            _is_nonempty_string(value) and value.startswith("evt:")
        ):
            errors.append(f"custody.{field} must be an evt: identifier or TOKEN_VAZIO")

    if state == "TOKEN_VAZIO":
        if claim_allowed is not False:
            errors.append("TOKEN_VAZIO requires classification.claim_allowed=false")
        if mode != "VAZIO":
            errors.append("TOKEN_VAZIO requires classification.evidence_mode=VAZIO")

    if claim_allowed is True:
        if state not in {"FATO", "VERIFIED_LIMITED"}:
            errors.append("claim_allowed=true requires FATO or VERIFIED_LIMITED")
        if mode != "DEMONSTRACAO":
            errors.append("claim_allowed=true requires evidence_mode DEMONSTRACAO")
        if not evidence_refs:
            errors.append("claim_allowed=true requires at least one evidence_ref")

    if operation == "TOKEN_VAZIO" and custody.get("event_id") != "TOKEN_VAZIO":
        errors.append("custody operation TOKEN_VAZIO requires event_id TOKEN_VAZIO")

    return errors


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_fixture_sets(
    valid_paths: Iterable[Path],
    invalid_paths: Iterable[Path],
) -> dict[str, Any]:
    valid_results = []
    invalid_results = []
    unexpected_failures = 0
    unexpected_passes = 0

    for path in sorted(valid_paths):
        defects = validate_record(load_json(path))
        valid_results.append({"path": path.as_posix(), "defects": defects})
        if defects:
            unexpected_failures += 1

    for path in sorted(invalid_paths):
        defects = validate_record(load_json(path))
        invalid_results.append({"path": path.as_posix(), "defects": defects})
        if not defects:
            unexpected_passes += 1

    status = "PASS" if unexpected_failures == 0 and unexpected_passes == 0 else "FAIL"
    return {
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "valid_fixture_count": len(valid_results),
        "invalid_fixture_count": len(invalid_results),
        "unexpected_failures": unexpected_failures,
        "unexpected_passes": unexpected_passes,
        "claim_allowed": False,
        "valid_results": valid_results,
        "invalid_results": invalid_results,
        "next_verifiable_step": (
            "Integrate this gate into registry ingestion."
            if status == "PASS"
            else "Correct fixture or validator defects before registry ingestion."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--valid-dir",
        type=Path,
        default=Path("tests/fixtures/cross_source/valid"),
    )
    parser.add_argument(
        "--invalid-dir",
        type=Path,
        default=Path("tests/fixtures/cross_source/invalid"),
    )
    parser.add_argument("--write-report", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    valid_paths = list(args.valid_dir.glob("*.json"))
    invalid_paths = list(args.invalid_dir.glob("*.json"))
    report = validate_fixture_sets(valid_paths, invalid_paths)
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"

    if args.write_report:
        args.write_report.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
