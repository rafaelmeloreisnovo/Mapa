#!/usr/bin/env python3
"""Sementeira 5x7 cognitive gate.

Stdlib-only, deterministic and fail-closed. It validates the human-facing
five-variable contract, the seven epistemic directions, TOKEN_VAZIO semantics,
and claim-promotion gates without inventing weights.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable

PROTOCOL_VERSION = "SEMENTEIRA-5X7-V1"
REQUIRED_VARIABLES = (
    "intention",
    "evidence",
    "human_state",
    "execution_capacity",
    "next_falsifiable_gate",
)
REQUIRED_DIRECTIONS = (
    "fact",
    "gap",
    "invariant",
    "variant",
    "proof_or_falsifier",
    "parable",
    "feedback",
)
EVIDENCE_KINDS = {"SOURCE", "METHOD", "TEST_RECEIPT", "REPLICATION"}
TOKEN_VAZIO_STATES = {
    "TOKEN_VAZIO",
    "TOKEN_VAZIO_UNKNOWN",
    "TOKEN_VAZIO_UNMEASURED",
    "TOKEN_VAZIO_UNIDENTIFIABLE",
    "TOKEN_VAZIO_CONTRADICTORY",
    "TOKEN_VAZIO_OUT_OF_DOMAIN",
    "TOKEN_VAZIO_WITHHELD",
    "TOKEN_VAZIO_CALIBRATION",
}


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    path: str
    message: str


class ContractError(ValueError):
    pass


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _is_nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _walk(value: Any, path: str = "$") -> Iterable[tuple[str, Any]]:
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, f"{path}[{index}]")


def validate_contract(payload: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []

    if payload.get("protocol_version") != PROTOCOL_VERSION:
        findings.append(Finding(
            "PROTOCOL_VERSION_MISMATCH", "BLOCK", "$.protocol_version",
            f"Expected {PROTOCOL_VERSION}."
        ))

    variables = payload.get("variables")
    if not isinstance(variables, dict):
        findings.append(Finding("VARIABLES_REQUIRED", "BLOCK", "$.variables", "variables must be an object."))
    else:
        keys = tuple(variables.keys())
        missing = [name for name in REQUIRED_VARIABLES if name not in variables]
        extra = [name for name in keys if name not in REQUIRED_VARIABLES]
        if missing:
            findings.append(Finding("FIVE_VARIABLES_MISSING", "BLOCK", "$.variables", f"Missing: {', '.join(missing)}"))
        if extra:
            findings.append(Finding("FIVE_VARIABLES_EXCEEDED", "BLOCK", "$.variables", f"Unexpected human-facing variables: {', '.join(extra)}"))
        if len(keys) != 5:
            findings.append(Finding("FIVE_VARIABLES_CARDINALITY", "BLOCK", "$.variables", "Exactly five human-facing variables are required."))
        for name in REQUIRED_VARIABLES:
            if name in variables and not _is_nonempty_text(variables[name]):
                findings.append(Finding("VARIABLE_EMPTY", "BLOCK", f"$.variables.{name}", "Variable must be non-empty text."))

    directions = payload.get("directions")
    if not isinstance(directions, dict):
        findings.append(Finding("DIRECTIONS_REQUIRED", "BLOCK", "$.directions", "directions must be an object."))
    else:
        missing = [name for name in REQUIRED_DIRECTIONS if name not in directions]
        extra = [name for name in directions if name not in REQUIRED_DIRECTIONS]
        if missing:
            findings.append(Finding("SEVEN_DIRECTIONS_MISSING", "BLOCK", "$.directions", f"Missing: {', '.join(missing)}"))
        if extra:
            findings.append(Finding("SEVEN_DIRECTIONS_EXTRA", "BLOCK", "$.directions", f"Unexpected directions: {', '.join(extra)}"))
        for name in REQUIRED_DIRECTIONS:
            if name in directions and not _is_nonempty_text(directions[name]):
                findings.append(Finding("DIRECTION_EMPTY", "BLOCK", f"$.directions.{name}", "Direction must be non-empty text."))

    for path, value in _walk(payload):
        if isinstance(value, dict) and value.get("state") in TOKEN_VAZIO_STATES:
            if value.get("value", None) == 0 or value.get("weight", None) == 0:
                findings.append(Finding(
                    "TOKEN_VAZIO_NOT_ZERO", "BLOCK", path,
                    "TOKEN_VAZIO is unknown/withheld state, not observed numeric zero."
                ))
            if "weight" in value and value.get("weight") is not None:
                findings.append(Finding(
                    "TOKEN_VAZIO_WEIGHT_MUST_BE_NULL", "BLOCK", f"{path}.weight",
                    "Unknown evidence weight must remain null until calibration."
                ))

    evidence = payload.get("evidence", [])
    if not isinstance(evidence, list):
        findings.append(Finding("EVIDENCE_LIST_REQUIRED", "BLOCK", "$.evidence", "evidence must be a list."))
        evidence = []

    evidence_by_id: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(evidence):
        path = f"$.evidence[{index}]"
        if not isinstance(item, dict):
            findings.append(Finding("EVIDENCE_OBJECT_REQUIRED", "BLOCK", path, "Evidence item must be an object."))
            continue
        evidence_id = item.get("id")
        kind = item.get("kind")
        if not _is_nonempty_text(evidence_id):
            findings.append(Finding("EVIDENCE_ID_REQUIRED", "BLOCK", f"{path}.id", "Evidence id is required."))
        elif evidence_id in evidence_by_id:
            findings.append(Finding("EVIDENCE_ID_DUPLICATE", "BLOCK", f"{path}.id", "Evidence id must be unique."))
        else:
            evidence_by_id[evidence_id] = item
        if kind not in EVIDENCE_KINDS:
            findings.append(Finding("EVIDENCE_KIND_INVALID", "BLOCK", f"{path}.kind", f"Allowed: {sorted(EVIDENCE_KINDS)}"))
        if not _is_nonempty_text(item.get("locator")):
            findings.append(Finding("EVIDENCE_LOCATOR_REQUIRED", "BLOCK", f"{path}.locator", "A source/commit/run locator is required."))
        if not _is_nonempty_text(item.get("sha256")) or len(item.get("sha256", "")) != 64:
            findings.append(Finding("EVIDENCE_HASH_REQUIRED", "BLOCK", f"{path}.sha256", "A 64-hex SHA-256 is required."))

    claims = payload.get("claims", [])
    if not isinstance(claims, list):
        findings.append(Finding("CLAIMS_LIST_REQUIRED", "BLOCK", "$.claims", "claims must be a list."))
        claims = []

    for index, claim in enumerate(claims):
        path = f"$.claims[{index}]"
        if not isinstance(claim, dict):
            findings.append(Finding("CLAIM_OBJECT_REQUIRED", "BLOCK", path, "Claim must be an object."))
            continue
        if not _is_nonempty_text(claim.get("id")):
            findings.append(Finding("CLAIM_ID_REQUIRED", "BLOCK", f"{path}.id", "Claim id is required."))
        if not _is_nonempty_text(claim.get("statement")):
            findings.append(Finding("CLAIM_STATEMENT_REQUIRED", "BLOCK", f"{path}.statement", "Claim statement is required."))

        refs = claim.get("evidence_refs", [])
        if not isinstance(refs, list):
            findings.append(Finding("CLAIM_EVIDENCE_REFS_INVALID", "BLOCK", f"{path}.evidence_refs", "Must be a list."))
            refs = []
        linked = [evidence_by_id[ref] for ref in refs if ref in evidence_by_id]
        missing_refs = [ref for ref in refs if ref not in evidence_by_id]
        if missing_refs:
            findings.append(Finding("CLAIM_EVIDENCE_REF_MISSING", "BLOCK", f"{path}.evidence_refs", f"Unknown refs: {missing_refs}"))

        kinds = {item.get("kind") for item in linked}
        if not _is_nonempty_text(claim.get("falsifier")):
            findings.append(Finding("CLAIM_FALSIFIER_MISSING", "GAP", f"{path}.falsifier", "Claim remains hypothesis without a falsifier."))
        required_for_local_evidence = {"SOURCE", "METHOD", "TEST_RECEIPT"}
        if not required_for_local_evidence.issubset(kinds):
            findings.append(Finding(
                "CLAIM_LOCAL_EVIDENCE_INCOMPLETE", "GAP", path,
                "SOURCE + METHOD + TEST_RECEIPT are required before local-evidence promotion."
            ))
        if claim.get("requested_state") in {"EVIDENCED", "PROVED", "REPLICATED"}:
            if not required_for_local_evidence.issubset(kinds):
                findings.append(Finding(
                    "CLAIM_PROMOTION_BLOCKED", "BLOCK", f"{path}.requested_state",
                    "Requested state exceeds available evidence."
                ))
            if claim.get("requested_state") == "REPLICATED" and "REPLICATION" not in kinds:
                findings.append(Finding(
                    "REPLICATION_REQUIRED", "BLOCK", f"{path}.requested_state",
                    "Independent replication receipt is required."
                ))

        if isinstance(claim.get("weight"), (int, float)):
            calibration_ref = claim.get("calibration_receipt_ref")
            if not _is_nonempty_text(calibration_ref) or calibration_ref not in evidence_by_id:
                findings.append(Finding(
                    "UNSUPPORTED_NUMERIC_WEIGHT", "BLOCK", f"{path}.weight",
                    "Numeric weight requires a referenced calibration receipt."
                ))

    human_state_evidence = [
        item for item in evidence
        if isinstance(item, dict) and item.get("kind") == "HUMAN_STATE"
    ]
    if human_state_evidence:
        findings.append(Finding(
            "HUMAN_STATE_IS_NOT_EVIDENCE", "BLOCK", "$.evidence",
            "Emotion/fatigue/context may affect routing, but cannot support a factual claim."
        ))

    if payload.get("claim_allowed") is not False:
        findings.append(Finding(
            "CLAIM_ALLOWED_MUST_BE_FALSE", "BLOCK", "$.claim_allowed",
            "This gate is pre-promotion and must remain fail-closed."
        ))

    return findings


def infer_claim_states(payload: dict[str, Any], findings: list[Finding]) -> list[dict[str, Any]]:
    evidence_by_id = {
        item["id"]: item
        for item in payload.get("evidence", [])
        if isinstance(item, dict) and _is_nonempty_text(item.get("id"))
    }
    output: list[dict[str, Any]] = []
    for claim in payload.get("claims", []):
        if not isinstance(claim, dict):
            continue
        refs = claim.get("evidence_refs", []) if isinstance(claim.get("evidence_refs", []), list) else []
        kinds = {evidence_by_id[ref].get("kind") for ref in refs if ref in evidence_by_id}
        has_falsifier = _is_nonempty_text(claim.get("falsifier"))
        if {"SOURCE", "METHOD", "TEST_RECEIPT", "REPLICATION"}.issubset(kinds) and has_falsifier:
            state = "REPLICATION_CANDIDATE"
        elif {"SOURCE", "METHOD", "TEST_RECEIPT"}.issubset(kinds) and has_falsifier:
            state = "LOCAL_EVIDENCE_CANDIDATE"
        elif has_falsifier:
            state = "TESTABLE_HYPOTHESIS"
        else:
            state = "TOKEN_VAZIO_TEST_DEFINITION"
        output.append({
            "id": claim.get("id", "TOKEN_VAZIO_ID"),
            "inferred_state": state,
            "claim_allowed": False,
            "evidence_kinds": sorted(kind for kind in kinds if isinstance(kind, str)),
        })
    return output


def build_receipt(payload: dict[str, Any]) -> dict[str, Any]:
    findings = validate_contract(payload)
    blocking = [asdict(item) for item in findings if item.severity == "BLOCK"]
    gaps = [asdict(item) for item in findings if item.severity == "GAP"]
    structural_pass = not blocking
    inferred_claims = infer_claim_states(payload, findings)
    receipt_core = {
        "protocol_version": PROTOCOL_VERSION,
        "input_sha256": sha256_json(payload),
        "structural_pass": structural_pass,
        "claim_allowed": False,
        "blocking_findings": blocking,
        "gaps": gaps,
        "claims": inferred_claims,
        "r3": {
            "F_ok": "Five variables and seven directions validated." if structural_pass else "Input preserved and audited fail-closed.",
            "F_gap": "No blocking findings." if structural_pass else f"{len(blocking)} blocking finding(s).",
            "F_next": "Attach missing receipts or define falsifiers; do not promote claims automatically.",
        },
    }
    receipt_core["receipt_sha256"] = sha256_json(receipt_core)
    return receipt_core


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a Sementeira 5x7 cognitive gate event.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--strict", action="store_true", help="Return non-zero on blocking findings.")
    args = parser.parse_args(argv)

    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ContractError("Top-level JSON must be an object.")
        receipt = build_receipt(payload)
    except (OSError, json.JSONDecodeError, ContractError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)

    if args.strict and not receipt["structural_pass"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
