#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

SCHEMA = "mapa.claim-vocabulary-policy.v1"
CLAIM_MARKERS = (
    "claim_state",
    "claim-status",
    "claim_status",
    "conformity_state",
    "certification_state",
)
INLINE_RECORD_RE = re.compile(r"<!--\s*CLAIM_RECORD\s*(\{.*?\})\s*-->", re.DOTALL)


class ClaimValidationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ClaimValidationError(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ClaimValidationError(f"{path}: {exc}") from exc
    require(isinstance(data, dict), f"{path}: root must be an object")
    return data


def canonical_digest(data: dict[str, Any]) -> str:
    clone = json.loads(json.dumps(data))
    clone.setdefault("integrity", {})["digest"] = ""
    payload = json.dumps(
        clone,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.blake2b(payload, digest_size=32).hexdigest()


def validate_policy(policy: dict[str, Any]) -> dict[str, Any]:
    require(policy.get("schema") == SCHEMA, "invalid claim vocabulary schema")
    require(
        policy.get("authority_repository") == "rafaelmeloreisnovo/Mapa",
        "Mapa authority required",
    )
    require(policy.get("gap_id") == "G006", "G006 scope required")
    require(
        policy.get("rollout_mode") == "REPORT_PROSE_FAIL_EXPLICIT",
        "rollout mode must preserve staged fail-closed adoption",
    )
    require(policy.get("claim_allowed") is False, "global claim promotion is forbidden")
    require(policy.get("certification_claim") is False, "certification claim is forbidden")

    descriptive = policy.get("descriptive_states")
    strong = policy.get("strong_states")
    forbidden = policy.get("forbidden_states")
    requirements = policy.get("terminal_requirements")
    invalid_pointers = policy.get("invalid_pointer_values")
    contradiction_tokens = policy.get("contradiction_tokens")
    scan_extensions = policy.get("scan_extensions")
    excluded_paths = policy.get("excluded_paths")

    require(isinstance(descriptive, list) and descriptive, "descriptive states required")
    require(isinstance(strong, list) and strong, "strong states required")
    require(isinstance(forbidden, list) and forbidden, "forbidden states required")
    require(isinstance(requirements, dict) and requirements, "terminal requirements required")
    require(isinstance(invalid_pointers, list) and invalid_pointers, "invalid pointer values required")
    require(isinstance(contradiction_tokens, list) and contradiction_tokens, "contradiction tokens required")
    require(isinstance(scan_extensions, list) and scan_extensions, "scan extensions required")
    require(isinstance(excluded_paths, list), "excluded paths must be a list")

    all_states = [str(value).upper() for value in descriptive + strong]
    require(len(all_states) == len(set(all_states)), "duplicate claim state")
    require(set(forbidden).issubset(set(strong)), "forbidden states must be strong states")
    require(set(requirements).issubset(set(strong)), "requirements reference unknown state")
    require("CERTIFIED" in forbidden, "CERTIFIED must remain forbidden")
    require("COMPLETE" in requirements, "COMPLETE requirements missing")
    require("COMPLIANT" in requirements, "COMPLIANT requirements missing")
    require("ALIGNED" in requirements, "ALIGNED requirements missing")

    for state, fields in requirements.items():
        require(isinstance(fields, list) and fields, f"{state}: requirement fields missing")
        require(len(fields) == len(set(fields)), f"{state}: duplicate requirement field")
        require(all(isinstance(field, str) and field for field in fields), f"{state}: invalid requirement field")

    integrity = policy.get("integrity")
    require(isinstance(integrity, dict), "integrity object required")
    require(integrity.get("algorithm") == "blake2b-256", "integrity algorithm mismatch")
    expected = canonical_digest(policy)
    require(integrity.get("digest") == expected, "claim vocabulary integrity mismatch")

    return {
        "status": "PASS",
        "schema": SCHEMA,
        "state_count": len(all_states),
        "strong_state_count": len(strong),
        "forbidden_state_count": len(forbidden),
        "claim_allowed": False,
        "certification_claim": False,
        "integrity_digest": expected,
    }


def _state_from_record(record: dict[str, Any]) -> str:
    found: list[tuple[str, str]] = []
    for marker in CLAIM_MARKERS:
        if marker in record:
            value = record[marker]
            require(isinstance(value, str) and value.strip(), f"{marker}: state must be a non-empty string")
            found.append((marker, value.strip().upper()))
    require(found, "explicit claim record has no claim-state marker")
    values = {value for _, value in found}
    require(len(values) == 1, "conflicting claim-state markers")
    return found[0][1]


def _pointer_valid(value: Any, invalid_values: set[str]) -> bool:
    if isinstance(value, str):
        normalized = value.strip().upper()
        return bool(normalized) and normalized not in invalid_values
    if isinstance(value, list):
        return bool(value) and all(_pointer_valid(item, invalid_values) for item in value)
    return False


def validate_claim_record(
    record: dict[str, Any],
    policy: dict[str, Any],
    source: str = "<memory>",
) -> dict[str, Any]:
    validate_policy(policy)
    state = _state_from_record(record)
    allowed = {str(value).upper() for value in policy["descriptive_states"] + policy["strong_states"]}
    forbidden = {str(value).upper() for value in policy["forbidden_states"]}
    invalid_values = {str(value).upper() for value in policy["invalid_pointer_values"]}

    require(state in allowed, f"{source}: unknown claim state {state}")
    require(state not in forbidden, f"{source}: forbidden claim state {state}")
    require(record.get("claim_allowed") is False, f"{source}: claim_allowed must be false")
    require(record.get("certification_claim", False) is False, f"{source}: certification_claim must be false")

    requirements = policy["terminal_requirements"].get(state, [])
    for field in requirements:
        require(field in record, f"{source}: {state} requires {field}")
        require(
            _pointer_valid(record[field], invalid_values),
            f"{source}: {state} has invalid {field}",
        )

    if state in {"COMPLETE", "COMPLIANT"}:
        expected_states = {
            "implementation_state": {"IMPLEMENTED"},
            "execution_state": {"EXECUTED"},
            "evidence_state": {"EVIDENCED", "INDEPENDENTLY_ASSURED"},
        }
        for field, accepted in expected_states.items():
            value = record.get(field)
            require(isinstance(value, str), f"{source}: {state} requires {field}")
            require(value.strip().upper() in accepted, f"{source}: invalid {field} for {state}")

        blocker = record.get("blocking_state")
        if blocker is not None:
            require(
                isinstance(blocker, str) and blocker.strip().upper() not in invalid_values,
                f"{source}: {state} contradicts blocking_state",
            )

    if state == "ALIGNED":
        require(record.get("conformity_claim") is False, f"{source}: ALIGNED must not imply conformity")
        require(
            _pointer_valid(record.get("alignment_scope"), invalid_values),
            f"{source}: ALIGNED requires alignment_scope",
        )

    return {
        "source": source,
        "state": state,
        "status": "PASS",
        "claim_allowed": False,
        "certification_claim": False,
    }


def _iter_explicit_json_records(value: Any, path: str = "$") -> Iterable[tuple[str, dict[str, Any]]]:
    if isinstance(value, dict):
        if any(marker in value for marker in CLAIM_MARKERS):
            yield path, value
        for key, child in value.items():
            yield from _iter_explicit_json_records(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _iter_explicit_json_records(child, f"{path}[{index}]")


def _is_excluded(relative: Path, excluded_paths: list[str]) -> bool:
    posix = relative.as_posix()
    return any(posix == prefix or posix.startswith(prefix.rstrip("/") + "/") for prefix in excluded_paths)


def _token_present(text: str, token: str) -> bool:
    return re.search(rf"(?<![A-Z0-9_]){re.escape(token)}(?![A-Z0-9_])", text.upper()) is not None


def scan_repository(
    root: Path,
    policy: dict[str, Any],
    *,
    max_bytes: int = 2_000_000,
) -> dict[str, Any]:
    policy_result = validate_policy(policy)
    extensions = {str(value).lower() for value in policy["scan_extensions"]}
    excluded_paths = [str(value) for value in policy["excluded_paths"]]
    strong_states = {str(value).upper() for value in policy["strong_states"]}
    contradiction_tokens = {str(value).upper() for value in policy["contradiction_tokens"]}

    files_scanned = 0
    files_skipped = 0
    explicit_records = 0
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    warning_count = 0

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if _is_excluded(relative, excluded_paths) or path.suffix.lower() not in extensions:
            continue
        try:
            size = path.stat().st_size
        except OSError as exc:
            errors.append({"path": relative.as_posix(), "error": str(exc)})
            continue
        if size > max_bytes:
            files_skipped += 1
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append({"path": relative.as_posix(), "error": str(exc)})
            continue

        files_scanned += 1
        records: list[tuple[str, dict[str, Any]]] = []
        if path.suffix.lower() == ".json":
            try:
                value = json.loads(text)
            except json.JSONDecodeError as exc:
                errors.append({"path": relative.as_posix(), "error": f"invalid JSON: {exc}"})
                continue
            records.extend(_iter_explicit_json_records(value))
        else:
            for index, match in enumerate(INLINE_RECORD_RE.finditer(text), start=1):
                try:
                    record = json.loads(match.group(1))
                except json.JSONDecodeError as exc:
                    errors.append(
                        {
                            "path": relative.as_posix(),
                            "location": f"inline[{index}]",
                            "error": f"invalid CLAIM_RECORD JSON: {exc}",
                        }
                    )
                    continue
                if not isinstance(record, dict):
                    errors.append(
                        {
                            "path": relative.as_posix(),
                            "location": f"inline[{index}]",
                            "error": "CLAIM_RECORD must be an object",
                        }
                    )
                    continue
                records.append((f"inline[{index}]", record))

        for location, record in records:
            explicit_records += 1
            source = f"{relative.as_posix()}:{location}"
            try:
                validate_claim_record(record, policy, source)
            except ClaimValidationError as exc:
                errors.append({"path": relative.as_posix(), "location": location, "error": str(exc)})

        strong_present = sorted(state for state in strong_states if _token_present(text, state))
        pending_present = sorted(token for token in contradiction_tokens if _token_present(text, token))
        if strong_present and pending_present:
            warning_count += 1
            if len(warnings) < 100:
                warnings.append(
                    {
                        "path": relative.as_posix(),
                        "class": "POTENTIAL_PROSE_CONTRADICTION",
                        "strong_tokens": strong_present,
                        "pending_tokens": pending_present,
                    }
                )

    return {
        "status": "PASS" if not errors else "FAIL",
        "schema": "mapa.claim-vocabulary-scan.v1",
        "gap_id": policy["gap_id"],
        "scope_repository": policy["authority_repository"],
        "rollout_mode": policy["rollout_mode"],
        "control_state": "IMPLEMENTED_LOCAL_SCOPE",
        "portfolio_exit_criteria_met": False,
        "policy_status": policy_result["status"],
        "files_scanned": files_scanned,
        "files_skipped_by_size": files_skipped,
        "explicit_claim_records": explicit_records,
        "explicit_claim_error_count": len(errors),
        "prose_contradiction_candidate_count": warning_count,
        "errors": errors[:100],
        "warnings": warnings,
        "warnings_truncated": warning_count > len(warnings),
        "claim_allowed": False,
        "certification_claim": False,
        "policy_integrity_digest": policy_result["integrity_digest"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", type=Path, default=Path("indices/CLAIM_VOCABULARY_POLICY.json"))
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--max-bytes", type=int, default=2_000_000)
    parser.add_argument("--write-report", type=Path)
    args = parser.parse_args(argv)

    try:
        policy = load_json(args.policy)
        result = scan_repository(args.root, policy, max_bytes=args.max_bytes)
    except ClaimValidationError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1

    text = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
