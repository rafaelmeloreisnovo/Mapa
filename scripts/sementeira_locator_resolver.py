#!/usr/bin/env python3
"""Resolve repository-local evidence locators and verify SHA-256 hashes.

Read-only, stdlib-only, deterministic and fail-closed. This resolver proves
only that observed bytes match declared hashes inside an authorized root. It
never promotes an epistemic claim by itself.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Any

PROTOCOL_VERSION = "SEMENTEIRA-LOCATOR-RESOLVER-V1"
HASH_RE = re.compile(r"^[0-9a-fA-F]{64}$")
MATCH = "HASH_MATCH"
MISMATCH = "HASH_MISMATCH"
UNRESOLVED = "TOKEN_VAZIO_UNRESOLVED"
BLOCKED = "BLOCKED_LOCATOR"


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    evidence_id: str
    locator: str
    message: str


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> tuple[str, int]:
    digest = hashlib.sha256()
    total = 0
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
            total += len(chunk)
    return digest.hexdigest(), total


def _relative_locator(locator: str) -> tuple[str | None, str | None]:
    if not isinstance(locator, str) or not locator.strip():
        return None, "LOCATOR_EMPTY"
    locator = locator.strip()
    if "\x00" in locator:
        return None, "LOCATOR_NUL"
    if locator.startswith("repo://"):
        locator = locator[len("repo://"):]
    elif "://" in locator:
        return None, "UNSUPPORTED_SCHEME"
    locator = locator.replace("\\", "/")
    pure = PurePosixPath(locator)
    if pure.is_absolute():
        return None, "ABSOLUTE_LOCATOR"
    if any(part in {"", "."} for part in pure.parts):
        pure = PurePosixPath(*[part for part in pure.parts if part not in {"", "."}])
    if any(part == ".." for part in pure.parts):
        return None, "PATH_TRAVERSAL"
    if not pure.parts:
        return None, "LOCATOR_EMPTY"
    return pure.as_posix(), None


def _is_within(candidate: Path, root: Path) -> bool:
    try:
        candidate.relative_to(root)
        return True
    except ValueError:
        return False


def resolve_locator(root: Path, locator: str) -> tuple[str, Path | None, str | None]:
    relative, error = _relative_locator(locator)
    if error:
        severity = BLOCKED if error != "UNSUPPORTED_SCHEME" else UNRESOLVED
        return severity, None, error

    root_resolved = root.resolve(strict=True)
    candidate_raw = root_resolved / relative

    # Reject symlinks anywhere in the declared path before following them.
    cursor = root_resolved
    for part in PurePosixPath(relative).parts:
        cursor = cursor / part
        if cursor.is_symlink():
            target = cursor.resolve(strict=False)
            if not _is_within(target, root_resolved):
                return BLOCKED, None, "SYMLINK_ESCAPE"

    candidate = candidate_raw.resolve(strict=False)
    if not _is_within(candidate, root_resolved):
        return BLOCKED, None, "ROOT_ESCAPE"
    if not candidate.exists():
        return UNRESOLVED, None, "FILE_NOT_FOUND"
    if not candidate.is_file():
        return BLOCKED, None, "NOT_A_REGULAR_FILE"
    if not os.access(candidate, os.R_OK):
        return UNRESOLVED, None, "FILE_NOT_READABLE"
    return "RESOLVED", candidate, None


def resolve_payload(payload: dict[str, Any], root: Path) -> dict[str, Any]:
    evidence = payload.get("evidence", [])
    findings: list[Finding] = []
    results: list[dict[str, Any]] = []

    if not isinstance(evidence, list):
        evidence = []
        findings.append(Finding(
            "EVIDENCE_LIST_REQUIRED", "BLOCK", "TOKEN_VAZIO_ID", "TOKEN_VAZIO_LOCATOR",
            "Top-level evidence must be a list."
        ))

    referenced_ids = {
        ref
        for claim in payload.get("claims", []) if isinstance(claim, dict)
        for ref in claim.get("evidence_refs", []) if isinstance(ref, str)
    }

    for index, item in enumerate(evidence):
        evidence_id = f"TOKEN_VAZIO_ID_{index}"
        locator = "TOKEN_VAZIO_LOCATOR"
        expected = None
        if not isinstance(item, dict):
            findings.append(Finding(
                "EVIDENCE_OBJECT_REQUIRED", "BLOCK", evidence_id, locator,
                "Evidence item must be an object."
            ))
            results.append({
                "evidence_id": evidence_id,
                "locator": locator,
                "status": BLOCKED,
                "reason": "EVIDENCE_OBJECT_REQUIRED",
                "referenced_by_claim": False,
            })
            continue

        evidence_id = str(item.get("id", evidence_id))
        locator = str(item.get("locator", locator))
        expected = item.get("sha256")
        referenced = evidence_id in referenced_ids

        if not isinstance(expected, str) or not HASH_RE.fullmatch(expected):
            findings.append(Finding(
                "INVALID_EXPECTED_SHA256", "BLOCK", evidence_id, locator,
                "Expected SHA-256 must contain exactly 64 hexadecimal characters."
            ))
            results.append({
                "evidence_id": evidence_id,
                "locator": locator,
                "expected_sha256": expected,
                "status": BLOCKED,
                "reason": "INVALID_EXPECTED_SHA256",
                "referenced_by_claim": referenced,
            })
            continue

        state, path, reason = resolve_locator(root, locator)
        if state != "RESOLVED" or path is None:
            severity = "BLOCK" if state == BLOCKED else "GAP"
            findings.append(Finding(
                reason or state, severity, evidence_id, locator,
                "Locator was not safely resolved inside the authorized root."
            ))
            results.append({
                "evidence_id": evidence_id,
                "locator": locator,
                "expected_sha256": expected.lower(),
                "status": state,
                "reason": reason,
                "referenced_by_claim": referenced,
            })
            continue

        actual, size = sha256_file(path)
        status = MATCH if actual == expected.lower() else MISMATCH
        if status == MISMATCH:
            findings.append(Finding(
                "SHA256_MISMATCH", "BLOCK" if referenced else "GAP", evidence_id, locator,
                "Observed bytes do not match the declared SHA-256."
            ))
        results.append({
            "evidence_id": evidence_id,
            "locator": locator,
            "resolved_relative_path": path.relative_to(root.resolve(strict=True)).as_posix(),
            "expected_sha256": expected.lower(),
            "actual_sha256": actual,
            "bytes": size,
            "status": status,
            "reason": None,
            "referenced_by_claim": referenced,
        })

    result_by_id = {item["evidence_id"]: item for item in results}
    missing_references = sorted(ref for ref in referenced_ids if ref not in result_by_id)
    for ref in missing_references:
        findings.append(Finding(
            "REFERENCED_EVIDENCE_MISSING", "BLOCK", ref, "TOKEN_VAZIO_LOCATOR",
            "A claim references evidence absent from the payload."
        ))

    referenced_results = [result_by_id[ref] for ref in sorted(referenced_ids) if ref in result_by_id]
    all_referenced_match = bool(referenced_results) and all(item["status"] == MATCH for item in referenced_results)
    blocking = [asdict(item) for item in findings if item.severity == "BLOCK"]
    gaps = [asdict(item) for item in findings if item.severity == "GAP"]
    strict_pass = all_referenced_match and not blocking and not missing_references

    core = {
        "protocol_version": PROTOCOL_VERSION,
        "input_sha256": sha256_json(payload),
        "root_policy": "AUTHORIZED_REPOSITORY_ROOT_READ_ONLY",
        "results": results,
        "referenced_evidence_ids": sorted(referenced_ids),
        "all_referenced_hashes_match": all_referenced_match,
        "artifact_identity_gate": "PASS" if strict_pass else "FAIL",
        "epistemic_promotion_allowed": False,
        "claim_allowed": False,
        "blocking_findings": blocking,
        "gaps": gaps,
        "r3": {
            "F_ok": "Referenced artifact bytes match declared hashes." if strict_pass else "All locators were preserved and evaluated fail-closed.",
            "F_gap": "Identity verified only at observed-byte layer; truth and replication remain outside this resolver." if strict_pass else "One or more locators or hashes remain unresolved, blocked or mismatched.",
            "F_next": "Pass this receipt to the cognitive/scientific gate; never promote a claim from hash identity alone.",
        },
    }
    core["receipt_sha256"] = sha256_json(core)
    return core


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Resolve Sementeira evidence locators and verify SHA-256 hashes.")
    parser.add_argument("input", type=Path, help="JSON payload containing evidence and claims.")
    parser.add_argument("--root", type=Path, required=True, help="Authorized repository root.")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)

    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Top-level JSON must be an object.")
        receipt = resolve_payload(payload, args.root)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)

    if args.strict and receipt["artifact_identity_gate"] != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
