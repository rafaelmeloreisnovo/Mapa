#!/usr/bin/env python3
"""Validate an append-only RAFAELIA chain-of-custody JSONL ledger.

The validator intentionally uses only the Python standard library so it can run
in Termux, local CI, and constrained audit environments without dependency drift.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

SCHEMA_VERSION = "mapa.custody-event.v1"
EVENT_ID_RE = re.compile(r"^COC-([0-9]{8}T[0-9]{6}Z)-[A-Z0-9_-]{4,64}$")
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
UTC_TIMESTAMP_RE = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
    r"(?:\.[0-9]+)?Z$"
)
HEX64_RE = re.compile(r"^[a-f0-9]{64}$")

REQUIRED_FIELDS = {
    "schema_version",
    "event_id",
    "timestamp_utc",
    "repository",
    "branch",
    "actor",
    "operation",
    "object",
    "epistemic_state",
    "claim_allowed",
    "evidence",
    "controls",
    "sigma",
    "next_verifiable_step",
}
ALLOWED_FIELDS = REQUIRED_FIELDS | {
    "source_ref",
    "previous_event_id",
    "supersedes_event_id",
    "event_hash_sha256",
}
ACTOR_FIELDS = {"type", "id"}
OBJECT_FIELDS = {"path", "media_type", "size_bytes", "sha256", "blake3"}
EVIDENCE_FIELDS = {"kind", "reference"}
CONTROL_FIELDS = {
    "integrity",
    "traceability",
    "reproducibility",
    "confidentiality",
}
SIGMA_FIELDS = {"phase", "defect_definition", "metric", "baseline", "target"}

OPERATIONS = {
    "INGEST",
    "CLASSIFY",
    "TRANSFORM",
    "VALIDATE",
    "TRANSFER",
    "PUBLISH",
    "CORRECT",
    "RETIRE",
    "TOKEN_VAZIO",
}
EPISTEMIC_STATES = {"FATO", "HIPOTESE", "SIMBOLICO", "TOKEN_VAZIO"}
EVIDENCE_KINDS = {
    "commit",
    "file",
    "hash",
    "log",
    "measurement",
    "source",
    "review",
    "test",
}
SIGMA_PHASES = {"DEFINE", "MEASURE", "ANALYZE", "IMPROVE", "CONTROL"}
CONTROL_STATES = {"verified", "partial", "TOKEN_VAZIO"}
CONFIDENTIALITY_STATES = {"public", "internal", "restricted"}


def canonical_event_hash(event: dict[str, Any]) -> str:
    payload = dict(event)
    payload.pop("event_hash_sha256", None)
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def is_safe_relative_path(value: str) -> bool:
    path = PurePosixPath(value)
    return (
        bool(value)
        and not path.is_absolute()
        and ".." not in path.parts
        and "\\" not in value
    )


def parse_utc_timestamp(value: str) -> datetime | None:
    if not UTC_TIMESTAMP_RE.fullmatch(value):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        return None
    return parsed


def event_id_timestamp(event_id: str) -> str | None:
    match = EVENT_ID_RE.fullmatch(event_id)
    return match.group(1) if match else None


def validate_no_extra_fields(
    value: dict[str, Any],
    allowed: set[str],
    prefix: str,
) -> list[str]:
    extras = sorted(set(value) - allowed)
    if not extras:
        return []
    return [f"{prefix}: unexpected fields: {', '.join(extras)}"]


def validate_event(event: Any, line_no: int, known_ids: set[str]) -> list[str]:
    prefix = f"line {line_no}"
    errors: list[str] = []

    if not isinstance(event, dict):
        return [f"{prefix}: event must be a JSON object"]

    errors.extend(validate_no_extra_fields(event, ALLOWED_FIELDS, prefix))

    missing = sorted(REQUIRED_FIELDS - set(event))
    if missing:
        errors.append(f"{prefix}: missing required fields: {', '.join(missing)}")

    if event.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"{prefix}: unsupported schema_version")

    event_id = event.get("event_id")
    id_timestamp = None
    if not isinstance(event_id, str) or not EVENT_ID_RE.fullmatch(event_id):
        errors.append(f"{prefix}: invalid event_id")
    else:
        id_timestamp = event_id_timestamp(event_id)
        if event_id in known_ids:
            errors.append(f"{prefix}: duplicate event_id {event_id}")

    timestamp = event.get("timestamp_utc")
    parsed_timestamp = (
        parse_utc_timestamp(timestamp) if isinstance(timestamp, str) else None
    )
    if parsed_timestamp is None:
        errors.append(f"{prefix}: timestamp_utc must be ISO-8601 UTC ending in Z")
    elif id_timestamp is not None:
        normalized = parsed_timestamp.strftime("%Y%m%dT%H%M%SZ")
        if normalized != id_timestamp:
            errors.append(f"{prefix}: event_id timestamp must match timestamp_utc")

    repository = event.get("repository")
    if not isinstance(repository, str) or not REPOSITORY_RE.fullmatch(repository):
        errors.append(f"{prefix}: repository must use owner/name")

    branch = event.get("branch")
    if not isinstance(branch, str) or not branch.strip():
        errors.append(f"{prefix}: branch must be non-empty")

    operation = event.get("operation")
    if operation not in OPERATIONS:
        errors.append(f"{prefix}: invalid operation")

    state = event.get("epistemic_state")
    if state not in EPISTEMIC_STATES:
        errors.append(f"{prefix}: invalid epistemic_state")

    claim_allowed = event.get("claim_allowed")
    if not isinstance(claim_allowed, bool):
        errors.append(f"{prefix}: claim_allowed must be boolean")

    evidence = event.get("evidence")
    if not isinstance(evidence, list):
        errors.append(f"{prefix}: evidence must be an array")
    else:
        if claim_allowed and not evidence:
            errors.append(f"{prefix}: claim_allowed=true requires evidence")
        for index, item in enumerate(evidence):
            item_prefix = f"{prefix}: evidence[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{item_prefix} must be an object")
                continue
            errors.extend(
                validate_no_extra_fields(item, EVIDENCE_FIELDS, item_prefix)
            )
            if item.get("kind") not in EVIDENCE_KINDS:
                errors.append(f"{item_prefix}.kind is invalid")
            reference = item.get("reference")
            if not isinstance(reference, str) or not reference.strip():
                errors.append(f"{item_prefix}.reference must be non-empty")

    if state == "TOKEN_VAZIO":
        if claim_allowed is not False:
            errors.append(f"{prefix}: TOKEN_VAZIO requires claim_allowed=false")
        if operation != "TOKEN_VAZIO":
            errors.append(
                f"{prefix}: epistemic_state TOKEN_VAZIO requires operation TOKEN_VAZIO"
            )
    elif operation == "TOKEN_VAZIO":
        errors.append(
            f"{prefix}: operation TOKEN_VAZIO requires epistemic_state TOKEN_VAZIO"
        )

    next_step = event.get("next_verifiable_step")
    if not isinstance(next_step, str) or not next_step.strip():
        errors.append(f"{prefix}: next_verifiable_step must be explicit")

    actor = event.get("actor")
    if not isinstance(actor, dict):
        errors.append(f"{prefix}: actor must be an object")
    else:
        errors.extend(validate_no_extra_fields(actor, ACTOR_FIELDS, f"{prefix}: actor"))
        if actor.get("type") not in {"human", "automation", "service"}:
            errors.append(f"{prefix}: invalid actor.type")
        actor_id = actor.get("id")
        if not isinstance(actor_id, str) or not actor_id.strip():
            errors.append(f"{prefix}: actor.id must be non-empty")

    obj = event.get("object")
    if not isinstance(obj, dict):
        errors.append(f"{prefix}: object must be an object")
    else:
        errors.extend(validate_no_extra_fields(obj, OBJECT_FIELDS, f"{prefix}: object"))
        object_path = obj.get("path")
        if not isinstance(object_path, str) or not is_safe_relative_path(object_path):
            errors.append(
                f"{prefix}: object.path must be safe and repository-relative"
            )
        media_type = obj.get("media_type")
        if not isinstance(media_type, str) or not media_type.strip():
            errors.append(f"{prefix}: object.media_type must be non-empty")
        for hash_name in ("sha256", "blake3"):
            value = obj.get(hash_name)
            if value is not None and (
                not isinstance(value, str) or not HEX64_RE.fullmatch(value)
            ):
                errors.append(
                    f"{prefix}: object.{hash_name} must be 64 lowercase hex chars or null"
                )
        size = obj.get("size_bytes")
        if size is not None and (
            not isinstance(size, int) or isinstance(size, bool) or size < 0
        ):
            errors.append(
                f"{prefix}: object.size_bytes must be a non-negative integer or null"
            )

    controls = event.get("controls")
    if not isinstance(controls, dict):
        errors.append(f"{prefix}: controls must be an object")
    else:
        errors.extend(
            validate_no_extra_fields(controls, CONTROL_FIELDS, f"{prefix}: controls")
        )
        for key in ("integrity", "traceability", "reproducibility"):
            if controls.get(key) not in CONTROL_STATES:
                errors.append(f"{prefix}: invalid controls.{key}")
        confidentiality = controls.get("confidentiality")
        if confidentiality is not None and confidentiality not in CONFIDENTIALITY_STATES:
            errors.append(f"{prefix}: invalid controls.confidentiality")

    sigma = event.get("sigma")
    if not isinstance(sigma, dict):
        errors.append(f"{prefix}: sigma must be an object")
    else:
        errors.extend(validate_no_extra_fields(sigma, SIGMA_FIELDS, f"{prefix}: sigma"))
        if sigma.get("phase") not in SIGMA_PHASES:
            errors.append(f"{prefix}: invalid sigma.phase")
        for key in ("defect_definition", "metric"):
            value = sigma.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}: sigma.{key} must be non-empty")
        if "baseline" not in sigma or "target" not in sigma:
            errors.append(f"{prefix}: sigma requires baseline and target")

    previous = event.get("previous_event_id")
    if previous is not None:
        if not isinstance(previous, str):
            errors.append(f"{prefix}: previous_event_id must be string or null")
        elif previous == event_id:
            errors.append(f"{prefix}: event cannot reference itself")
        elif previous not in known_ids:
            errors.append(f"{prefix}: previous_event_id must reference an earlier event")

    supersedes = event.get("supersedes_event_id")
    if operation == "CORRECT":
        if not isinstance(supersedes, str) or supersedes not in known_ids:
            errors.append(
                f"{prefix}: CORRECT requires supersedes_event_id referencing an earlier valid event"
            )
    elif supersedes is not None:
        errors.append(
            f"{prefix}: supersedes_event_id is only allowed for operation CORRECT"
        )

    declared_hash = event.get("event_hash_sha256")
    if declared_hash is not None:
        if not isinstance(declared_hash, str) or not HEX64_RE.fullmatch(declared_hash):
            errors.append(
                f"{prefix}: event_hash_sha256 must be 64 lowercase hex chars or null"
            )
        else:
            calculated = canonical_event_hash(event)
            if declared_hash != calculated:
                errors.append(
                    f"{prefix}: event_hash_sha256 mismatch; expected {calculated}"
                )

    return errors


def validate_object_evidence(
    event: dict[str, Any],
    line_no: int,
    repo_root: Path,
) -> list[str]:
    prefix = f"line {line_no}"
    obj = event.get("object")
    if not isinstance(obj, dict):
        return []

    object_path = obj.get("path")
    if not isinstance(object_path, str) or not is_safe_relative_path(object_path):
        return []

    candidate = (repo_root / object_path).resolve()
    try:
        candidate.relative_to(repo_root.resolve())
    except ValueError:
        return [f"{prefix}: resolved object.path escapes repo_root"]

    if not candidate.is_file():
        if event.get("operation") == "RETIRE":
            return []
        return [f"{prefix}: referenced object does not exist: {object_path}"]

    errors: list[str] = []
    data = candidate.read_bytes()
    declared_size = obj.get("size_bytes")
    if declared_size is not None and declared_size != len(data):
        errors.append(
            f"{prefix}: object.size_bytes mismatch; expected {len(data)}"
        )

    declared_sha256 = obj.get("sha256")
    if declared_sha256 is not None:
        calculated = hashlib.sha256(data).hexdigest()
        if declared_sha256 != calculated:
            errors.append(
                f"{prefix}: object.sha256 mismatch; expected {calculated}"
            )

    return errors


def validate_ledger(
    path: Path,
    repo_root: Path | None = None,
) -> tuple[int, list[str]]:
    known_ids: set[str] = set()
    errors: list[str] = []
    count = 0
    last_valid_event_id: str | None = None
    last_valid_timestamp: datetime | None = None

    with path.open("r", encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, start=1):
            stripped = raw.strip()
            if not stripped:
                continue
            count += 1
            try:
                event = json.loads(stripped)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_no}: invalid JSON: {exc.msg}")
                continue

            event_errors = validate_event(event, line_no, known_ids)

            if isinstance(event, dict):
                previous = event.get("previous_event_id")
                if previous != last_valid_event_id:
                    event_errors.append(
                        f"line {line_no}: previous_event_id must equal the immediately preceding valid event"
                    )

                timestamp = event.get("timestamp_utc")
                parsed = (
                    parse_utc_timestamp(timestamp)
                    if isinstance(timestamp, str)
                    else None
                )
                if (
                    parsed is not None
                    and last_valid_timestamp is not None
                    and parsed < last_valid_timestamp
                ):
                    event_errors.append(
                        f"line {line_no}: timestamp_utc must be monotonic"
                    )

                if repo_root is not None:
                    event_errors.extend(
                        validate_object_evidence(event, line_no, repo_root)
                    )

            errors.extend(event_errors)

            if not event_errors and isinstance(event, dict):
                event_id = event.get("event_id")
                if isinstance(event_id, str):
                    known_ids.add(event_id)
                    last_valid_event_id = event_id
                    timestamp = event.get("timestamp_utc")
                    if isinstance(timestamp, str):
                        last_valid_timestamp = parse_utc_timestamp(timestamp)

    if count == 0:
        errors.append(
            "ledger is empty: register a bootstrap event or explicit TOKEN_VAZIO"
        )

    return count, errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a RAFAELIA chain-of-custody JSONL ledger"
    )
    parser.add_argument(
        "ledger",
        type=Path,
        help="path to the append-only JSONL ledger",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="optional repository root for object existence, size, and SHA-256 checks",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.ledger.is_file():
        print(f"ERROR: ledger not found: {args.ledger}", file=sys.stderr)
        return 2
    if args.repo_root is not None and not args.repo_root.is_dir():
        print(f"ERROR: repo root not found: {args.repo_root}", file=sys.stderr)
        return 2

    count, errors = validate_ledger(args.ledger, args.repo_root)
    if errors:
        print(
            f"FAIL: {len(errors)} defect(s) across {count} event(s)",
            file=sys.stderr,
        )
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"OK: {count} custody event(s) validated; chain semantics preserved"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
