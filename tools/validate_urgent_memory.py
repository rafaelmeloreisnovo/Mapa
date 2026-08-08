#!/usr/bin/env python3
"""Deterministic stdlib validator for RAFAELIA urgent-memory JSONL."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PRIORITIES = {"P0", "P1", "P2", "P3", "P4"}
PRIORITY_BASIS = {"SOURCE_DECLARED", "COMPUTED", "GOVERNANCE_OVERRIDE"}
STATES = {"OPEN", "TESTABLE", "RUNNING", "BLOCKED_EXTERNAL", "CLOSED_PASS", "CLOSED_FAIL", "ARCHIVED"}
CATEGORIES = {
    "SECURITY", "MEASUREMENT", "INTEGRITY", "TOKEN_ACCOUNTING", "RECEIPT",
    "MULTIMODAL_JOIN", "PROVENANCE", "EXECUTION_EVIDENCE",
    "REPRODUCIBILITY", "OTHER",
}
AUTHORITIES = {"OBSERVED", "SOURCE_REPORTED", "PUBLIC_RECEIPT", "BYTE_HASHED", "BYTE_PARSED"}
KINDS = {"github", "drive_private_sanitized", "receipt", "other"}
REQUIRED = {
    "schema_version", "urgent_id", "priority", "priority_basis", "state",
    "source_state", "category", "problem", "risk", "next_gate",
    "claim_allowed", "provenance", "source_memory_ids",
    "source_ordinal_paths", "longitudinal_refs", "closure_contract",
    "created_at", "last_checked_at", "revision",
}
CLOSURE_REQUIRED = {"expected_evidence", "closure_test", "receipt_required"}


def validate(path: Path) -> tuple[list[str], dict[str, object]]:
    errors: list[str] = []
    nodes: list[dict[str, object]] = []

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            node = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"L{lineno}: invalid JSON: {exc}")
            continue
        node["__line"] = lineno
        nodes.append(node)

    seen_ids: set[str] = set()
    for node in nodes:
        line = int(node["__line"])
        missing = REQUIRED - node.keys()
        if missing:
            errors.append(f"L{line}: missing required keys: {sorted(missing)}")
            continue

        if node["schema_version"] != "urgent-memory-node.v1":
            errors.append(f"L{line}: invalid schema_version")

        urgent_id = node["urgent_id"]
        if not isinstance(urgent_id, str) or len(urgent_id) < 3:
            errors.append(f"L{line}: invalid urgent_id")
        elif urgent_id in seen_ids:
            errors.append(f"L{line}: duplicate urgent_id {urgent_id}")
        else:
            seen_ids.add(urgent_id)

        if node["priority"] not in PRIORITIES:
            errors.append(f"L{line}: invalid priority")
        if node["priority_basis"] not in PRIORITY_BASIS:
            errors.append(f"L{line}: invalid priority_basis")
        if node["state"] not in STATES:
            errors.append(f"L{line}: invalid state")
        if node["category"] not in CATEGORIES:
            errors.append(f"L{line}: invalid category")
        if node["claim_allowed"] is not False and node["state"] not in {"CLOSED_PASS", "ARCHIVED"}:
            errors.append(f"L{line}: unresolved urgent node cannot have claim_allowed=true")

        score = node.get("urgency_score")
        if score is not None and (
            not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 100
        ):
            errors.append(f"L{line}: urgency_score outside 0..100")
        if score is None:
            basis = node.get("measurement_basis")
            if not isinstance(basis, dict) or "urgency_score" not in basis:
                errors.append(f"L{line}: null urgency_score requires measurement_basis.urgency_score")
        elif node["priority_basis"] == "COMPUTED":
            expected_priority = (
                "P0" if score >= 80 else
                "P1" if score >= 60 else
                "P2" if score >= 40 else
                "P3" if score >= 20 else
                "P4"
            )
            if node["priority"] != expected_priority:
                errors.append(
                    f"L{line}: computed urgency_score={score} requires priority={expected_priority}"
                )

        refs = node["provenance"]
        if not isinstance(refs, list) or not refs:
            errors.append(f"L{line}: provenance must be non-empty list")
        else:
            for ref in refs:
                if not isinstance(ref, dict):
                    errors.append(f"L{line}: provenance entry must be object")
                    continue
                if ref.get("kind") not in KINDS:
                    errors.append(f"L{line}: invalid provenance kind")
                if ref.get("authority") not in AUTHORITIES:
                    errors.append(f"L{line}: invalid provenance authority")
                if not isinstance(ref.get("locator"), str) or not ref["locator"]:
                    errors.append(f"L{line}: provenance locator required")
                if ref.get("kind") == "drive_private_sanitized":
                    locator = str(ref.get("locator", ""))
                    if "docs.google.com/" in locator or "drive.google.com/" in locator:
                        errors.append(f"L{line}: public urgent projection must not embed private Drive URLs")

        ordinals = node["source_ordinal_paths"]
        if not isinstance(ordinals, list):
            errors.append(f"L{line}: source_ordinal_paths must be list")
        else:
            for op in ordinals:
                if not (
                    isinstance(op, list) and len(op) == 6
                    and all(isinstance(x, int) and not isinstance(x, bool) and x >= 0 for x in op)
                ):
                    errors.append(f"L{line}: invalid source ordinal path")

        closure = node["closure_contract"]
        if not isinstance(closure, dict):
            errors.append(f"L{line}: closure_contract must be object")
        else:
            missing_closure = CLOSURE_REQUIRED - closure.keys()
            if missing_closure:
                errors.append(f"L{line}: closure_contract missing {sorted(missing_closure)}")
            if closure.get("receipt_required") is not True:
                errors.append(f"L{line}: urgent closure must require a receipt")

    by_priority = {p: sum(1 for n in nodes if n.get("priority") == p) for p in sorted(PRIORITIES)}
    summary = {
        "file": str(path),
        "nodes": len(nodes),
        "unique_ids": len(seen_ids),
        "by_priority": by_priority,
        "open_like": sum(1 for n in nodes if n.get("state") in {"OPEN", "TESTABLE", "RUNNING", "BLOCKED_EXTERNAL"}),
        "claim_allowed_true": sum(1 for n in nodes if n.get("claim_allowed") is True),
        "errors": len(errors),
        "status": "PASS" if not errors else "FAIL",
    }
    return errors, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        default="data/memory/urgent-memory.public.v1.jsonl",
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
