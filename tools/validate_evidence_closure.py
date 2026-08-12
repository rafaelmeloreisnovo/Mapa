#!/usr/bin/env python3
"""Fail-closed validator for RAFAELIA evidence-closure append-only JSONL."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "evidence-closure-record.v1"
STATES = {
    "TOKEN_VAZIO", "BLOCKED", "OBSERVED_LIMITED", "EVIDENCED",
    "CLOSED_PASS", "CLOSED_FAIL", "ARCHIVED",
}
AXES = {
    "CODE", "BUILD", "RUNTIME", "TEST", "CI", "DEVICE",
    "SECURITY", "PROVENANCE", "REPRODUCIBILITY",
}
EVIDENCE_STATES = {
    "PASS", "FAIL", "BLOCKED", "OBSERVED", "OBSERVED_LIMITED",
    "TOKEN_VAZIO", "NOT_APPLICABLE",
}
UNCERTAINTY_CLASSES = {"MEASURED", "BOUNDED", "TOKEN_VAZIO", "BLOCKED"}
PROVENANCE_AUTHORITIES = {
    "OBSERVED", "SOURCE_REPORTED", "PUBLIC_RECEIPT",
    "BYTE_HASHED", "BYTE_PARSED", "COMMIT_PINNED",
}
PROVENANCE_KINDS = {"github", "drive_private_sanitized", "receipt", "other"}
REQUIRED = {
    "schema_version", "closure_id", "revision", "status", "claim_allowed",
    "required_axes", "evidence_vector", "uncertainty", "problem", "risk",
    "next_probe", "closure_rule", "falsifier", "provenance", "receipts",
    "dependencies", "contradictions", "previous_record_sha256",
    "transition_reason", "observed_at",
}
OPTIONAL = {"tags", "owner", "scope"}
ALLOWED_KEYS = REQUIRED | OPTIONAL

ALLOWED_TRANSITIONS = {
    "TOKEN_VAZIO": {"TOKEN_VAZIO", "BLOCKED", "OBSERVED_LIMITED", "EVIDENCED", "CLOSED_FAIL"},
    "BLOCKED": {"BLOCKED", "TOKEN_VAZIO", "OBSERVED_LIMITED", "EVIDENCED", "CLOSED_FAIL"},
    "OBSERVED_LIMITED": {"OBSERVED_LIMITED", "BLOCKED", "EVIDENCED", "CLOSED_FAIL"},
    "EVIDENCED": {"EVIDENCED", "OBSERVED_LIMITED", "BLOCKED", "CLOSED_PASS", "CLOSED_FAIL"},
    "CLOSED_PASS": {"CLOSED_PASS", "BLOCKED", "CLOSED_FAIL", "ARCHIVED"},
    "CLOSED_FAIL": {"CLOSED_FAIL", "EVIDENCED", "ARCHIVED"},
    "ARCHIVED": {"ARCHIVED"},
}


class DuplicateKeyError(ValueError):
    pass


def _no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(f"duplicate key: {key}")
        out[key] = value
    return out


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def _parse_json(raw: str) -> dict[str, Any]:
    value = json.loads(raw, object_pairs_hook=_no_duplicates, parse_constant=_reject_constant)
    if not isinstance(value, dict):
        raise ValueError("record must be a JSON object")
    return value


def _canonical_sha256(record: dict[str, Any]) -> str:
    raw = json.dumps(
        record,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _is_hex(value: Any, length: int) -> bool:
    return isinstance(value, str) and len(value) == length and all(c in "0123456789abcdefABCDEF" for c in value)


def _is_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return "T" in value
    except ValueError:
        return False


def validate(path: Path) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    records: list[dict[str, Any]] = []

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            record = _parse_json(raw)
        except (json.JSONDecodeError, ValueError, DuplicateKeyError) as exc:
            errors.append(f"L{lineno}: invalid JSON: {exc}")
            continue
        record["__line"] = lineno
        records.append(record)

    by_closure: dict[str, list[dict[str, Any]]] = {}

    for record in records:
        line = int(record["__line"])
        public_record = {k: v for k, v in record.items() if k != "__line"}

        missing = REQUIRED - public_record.keys()
        unknown = public_record.keys() - ALLOWED_KEYS
        if missing:
            errors.append(f"L{line}: missing required keys: {sorted(missing)}")
            continue
        if unknown:
            errors.append(f"L{line}: unknown keys: {sorted(unknown)}")

        if record["schema_version"] != SCHEMA_VERSION:
            errors.append(f"L{line}: invalid schema_version")

        closure_id = record["closure_id"]
        if not isinstance(closure_id, str) or len(closure_id) < 6:
            errors.append(f"L{line}: invalid closure_id")
            continue
        by_closure.setdefault(closure_id, []).append(record)

        revision = record["revision"]
        if not isinstance(revision, int) or isinstance(revision, bool) or revision < 0:
            errors.append(f"L{line}: revision must be non-negative integer")

        status = record["status"]
        if status not in STATES:
            errors.append(f"L{line}: invalid status")

        if not isinstance(record["claim_allowed"], bool):
            errors.append(f"L{line}: claim_allowed must be boolean")

        required_axes = record["required_axes"]
        if not isinstance(required_axes, list) or not required_axes:
            errors.append(f"L{line}: required_axes must be non-empty list")
            required_axes_set: set[str] = set()
        else:
            required_axes_set = set()
            for axis in required_axes:
                if axis not in AXES:
                    errors.append(f"L{line}: invalid required axis {axis!r}")
                elif axis in required_axes_set:
                    errors.append(f"L{line}: duplicate required axis {axis}")
                required_axes_set.add(axis)
            if "PROVENANCE" not in required_axes_set:
                errors.append(f"L{line}: PROVENANCE must always be a required axis")

        vector = record["evidence_vector"]
        if not isinstance(vector, dict) or set(vector) != AXES:
            errors.append(f"L{line}: evidence_vector must contain exactly {sorted(AXES)}")
            vector = {}
        else:
            for axis, value in vector.items():
                if value not in EVIDENCE_STATES:
                    errors.append(f"L{line}: invalid evidence state {axis}={value!r}")

        uncertainty = record["uncertainty"]
        if not isinstance(uncertainty, dict):
            errors.append(f"L{line}: uncertainty must be object")
            uncertainty = {}
        else:
            if set(uncertainty) != {"class", "reasons"}:
                errors.append(f"L{line}: uncertainty requires exactly class,reasons")
            if uncertainty.get("class") not in UNCERTAINTY_CLASSES:
                errors.append(f"L{line}: invalid uncertainty.class")
            reasons = uncertainty.get("reasons")
            if not isinstance(reasons, list) or any(not isinstance(x, str) or not x.strip() for x in reasons):
                errors.append(f"L{line}: uncertainty.reasons must be a list of non-empty strings")

        for field in ("problem", "risk", "next_probe", "closure_rule", "falsifier", "transition_reason"):
            if not isinstance(record[field], str) or not record[field].strip():
                errors.append(f"L{line}: {field} must be non-empty string")

        if not _is_timestamp(record["observed_at"]):
            errors.append(f"L{line}: observed_at must be ISO-8601 date-time")

        provenance = record["provenance"]
        if not isinstance(provenance, list) or not provenance:
            errors.append(f"L{line}: provenance must be non-empty list")
        else:
            for i, ref in enumerate(provenance):
                if not isinstance(ref, dict):
                    errors.append(f"L{line}: provenance[{i}] must be object")
                    continue
                allowed = {"kind", "locator", "authority", "commit_sha", "sha256"}
                required_ref = {"kind", "locator", "authority"}
                if required_ref - ref.keys() or ref.keys() - allowed:
                    errors.append(f"L{line}: provenance[{i}] malformed keys")
                if ref.get("kind") not in PROVENANCE_KINDS:
                    errors.append(f"L{line}: provenance[{i}] invalid kind")
                if ref.get("authority") not in PROVENANCE_AUTHORITIES:
                    errors.append(f"L{line}: provenance[{i}] invalid authority")
                locator = ref.get("locator")
                if not isinstance(locator, str) or not locator:
                    errors.append(f"L{line}: provenance[{i}] locator required")
                if ref.get("kind") == "drive_private_sanitized" and isinstance(locator, str):
                    if "docs.google.com/" in locator or "drive.google.com/" in locator:
                        errors.append(f"L{line}: public projection cannot embed private Drive URL")
                if ref.get("commit_sha") is not None and not _is_hex(ref.get("commit_sha"), 40):
                    errors.append(f"L{line}: provenance[{i}] commit_sha must be 40 hex")
                if ref.get("sha256") is not None and not _is_hex(ref.get("sha256"), 64):
                    errors.append(f"L{line}: provenance[{i}] sha256 must be 64 hex")

        receipts = record["receipts"]
        if not isinstance(receipts, list):
            errors.append(f"L{line}: receipts must be list")
            receipts = []
        else:
            for i, receipt in enumerate(receipts):
                if not isinstance(receipt, dict):
                    errors.append(f"L{line}: receipts[{i}] must be object")
                    continue
                if set(receipt) != {"locator", "sha256", "producer", "observed_at"}:
                    errors.append(f"L{line}: receipts[{i}] requires locator,sha256,producer,observed_at")
                    continue
                if not isinstance(receipt["locator"], str) or not receipt["locator"]:
                    errors.append(f"L{line}: receipts[{i}] locator required")
                if not _is_hex(receipt["sha256"], 64):
                    errors.append(f"L{line}: receipts[{i}] sha256 must be 64 hex")
                if not isinstance(receipt["producer"], str) or not receipt["producer"]:
                    errors.append(f"L{line}: receipts[{i}] producer required")
                if not _is_timestamp(receipt["observed_at"]):
                    errors.append(f"L{line}: receipts[{i}] observed_at invalid")

        dependencies = record["dependencies"]
        if not isinstance(dependencies, list):
            errors.append(f"L{line}: dependencies must be list")
            dependencies = []
        else:
            for i, dep in enumerate(dependencies):
                if not isinstance(dep, dict) or set(dep) != {"closure_id", "state", "locator"}:
                    errors.append(f"L{line}: dependencies[{i}] malformed")
                    continue
                if dep["state"] not in STATES | {"NOT_APPLICABLE"}:
                    errors.append(f"L{line}: dependencies[{i}] invalid state")
                if not isinstance(dep["closure_id"], str) or not dep["closure_id"]:
                    errors.append(f"L{line}: dependencies[{i}] closure_id required")
                if not isinstance(dep["locator"], str) or not dep["locator"]:
                    errors.append(f"L{line}: dependencies[{i}] locator required")

        contradictions = record["contradictions"]
        if not isinstance(contradictions, list):
            errors.append(f"L{line}: contradictions must be list")
            contradictions = []
        else:
            ids: set[str] = set()
            for i, contradiction in enumerate(contradictions):
                if not isinstance(contradiction, dict):
                    errors.append(f"L{line}: contradictions[{i}] must be object")
                    continue
                required_c = {"id", "lhs", "rhs", "state", "resolution_evidence"}
                if set(contradiction) != required_c:
                    errors.append(f"L{line}: contradictions[{i}] malformed")
                    continue
                cid = contradiction["id"]
                if not isinstance(cid, str) or not cid:
                    errors.append(f"L{line}: contradictions[{i}] id required")
                elif cid in ids:
                    errors.append(f"L{line}: duplicate contradiction id {cid}")
                ids.add(cid)
                if contradiction["state"] not in {"OPEN", "RESOLVED"}:
                    errors.append(f"L{line}: contradictions[{i}] invalid state")
                if contradiction["state"] == "RESOLVED" and not contradiction["resolution_evidence"]:
                    errors.append(f"L{line}: resolved contradiction requires resolution_evidence")

        prev = record["previous_record_sha256"]
        if revision == 0:
            if prev is not None:
                errors.append(f"L{line}: revision 0 previous_record_sha256 must be null")
        else:
            if not _is_hex(prev, 64):
                errors.append(f"L{line}: revision >0 requires 64-hex previous_record_sha256")

        if record["status"] == "TOKEN_VAZIO":
            if "TOKEN_VAZIO" not in vector.values():
                errors.append(f"L{line}: TOKEN_VAZIO status requires TOKEN_VAZIO evidence axis")
            if uncertainty.get("class") not in {"TOKEN_VAZIO", "BLOCKED"}:
                errors.append(f"L{line}: TOKEN_VAZIO status requires uncertainty TOKEN_VAZIO/BLOCKED")

        if record["status"] == "BLOCKED" and uncertainty.get("class") != "BLOCKED":
            errors.append(f"L{line}: BLOCKED status requires uncertainty.class=BLOCKED")

        if record["status"] == "CLOSED_PASS":
            if not receipts:
                errors.append(f"L{line}: CLOSED_PASS requires at least one receipt")
            bad_axes = {
                axis for axis in required_axes_set
                if vector.get(axis) not in {"PASS", "NOT_APPLICABLE"}
            }
            if bad_axes:
                errors.append(f"L{line}: CLOSED_PASS has unresolved required axes {sorted(bad_axes)}")
            bad_deps = [d for d in dependencies if d.get("state") not in {"CLOSED_PASS", "NOT_APPLICABLE"}]
            if bad_deps:
                errors.append(f"L{line}: CLOSED_PASS has unresolved dependencies")
            if any(c.get("state") == "OPEN" for c in contradictions if isinstance(c, dict)):
                errors.append(f"L{line}: CLOSED_PASS has open contradictions")
            if uncertainty.get("class") not in {"MEASURED", "BOUNDED"}:
                errors.append(f"L{line}: CLOSED_PASS uncertainty must be MEASURED or BOUNDED")

        if record["claim_allowed"] is True:
            if record["status"] != "CLOSED_PASS":
                errors.append(f"L{line}: claim_allowed=true requires CLOSED_PASS")
            if uncertainty.get("class") not in {"MEASURED", "BOUNDED"}:
                errors.append(f"L{line}: claim_allowed=true requires bounded/measured uncertainty")
            for axis in required_axes_set:
                if vector.get(axis) not in {"PASS", "NOT_APPLICABLE"}:
                    errors.append(f"L{line}: claim_allowed=true with unresolved axis {axis}")

    for closure_id, chain in by_closure.items():
        chain_sorted = sorted(chain, key=lambda r: r.get("revision", -1) if isinstance(r.get("revision"), int) else -1)
        revisions = [r.get("revision") for r in chain_sorted]
        expected = list(range(len(chain_sorted)))
        if revisions != expected:
            errors.append(f"{closure_id}: revisions must be contiguous from 0, got {revisions}")

        for index in range(1, len(chain_sorted)):
            prev_record = {k: v for k, v in chain_sorted[index - 1].items() if k != "__line"}
            current = chain_sorted[index]
            line = int(current["__line"])
            digest = _canonical_sha256(prev_record)
            if current.get("previous_record_sha256") != digest:
                errors.append(f"L{line}: previous_record_sha256 mismatch for {closure_id}")
            previous_status = prev_record.get("status")
            current_status = current.get("status")
            if previous_status in ALLOWED_TRANSITIONS and current_status not in ALLOWED_TRANSITIONS[previous_status]:
                errors.append(f"L{line}: illegal transition {previous_status}->{current_status}")
            if previous_status == "CLOSED_PASS" and current_status in {"BLOCKED", "CLOSED_FAIL"}:
                reason = str(current.get("transition_reason", "")).lower()
                if not any(token in reason for token in ("reopen", "refut", "contrad", "new evidence", "nova evid")):
                    errors.append(f"L{line}: reopening CLOSED_PASS requires explicit new/refuting evidence reason")

    latest: dict[str, dict[str, Any]] = {}
    for closure_id, chain in by_closure.items():
        valid_revisions = [r for r in chain if isinstance(r.get("revision"), int)]
        if valid_revisions:
            latest[closure_id] = max(valid_revisions, key=lambda r: r["revision"])

    summary = {
        "file": str(path),
        "records": len(records),
        "closures": len(by_closure),
        "latest_by_status": {
            state: sum(1 for r in latest.values() if r.get("status") == state)
            for state in sorted(STATES)
        },
        "claim_allowed_true_latest": sum(1 for r in latest.values() if r.get("claim_allowed") is True),
        "errors": len(errors),
        "status": "PASS" if not errors else "FAIL",
    }
    return errors, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        default="data/governance/evidence-closure.public.v1.jsonl",
        type=Path,
    )
    args = parser.parse_args()
    errors, summary = validate(args.path)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    for error in errors:
        print(error, file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
