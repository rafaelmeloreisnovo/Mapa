#!/usr/bin/env python3
"""Compose Sementeira cognitive and locator receipts into a fail-closed gate.

This module never promotes a claim. It verifies that every evidence reference used
by a cognitive claim maps to a locator result whose observed bytes match the
SHA-256 declared in the original cognitive payload.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

PROTOCOL_VERSION = "SEMENTEIRA-COGNITIVE-LOCATOR-GATE-V1"
MATCH = "HASH_MATCH"
BLOCKING_LOCATOR_STATES = {
    "HASH_MISMATCH",
    "TOKEN_VAZIO_UNRESOLVED",
    "BLOCKED_LOCATOR",
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


def receipt_hash_is_valid(receipt: dict[str, Any]) -> bool:
    supplied = receipt.get("receipt_sha256")
    if not isinstance(supplied, str) or len(supplied) != 64:
        return False
    core = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    return sha256_json(core) == supplied


def _is_nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_bundle(bundle: dict[str, Any]) -> tuple[list[Finding], list[dict[str, Any]]]:
    findings: list[Finding] = []
    claim_results: list[dict[str, Any]] = []

    if bundle.get("protocol_version") != PROTOCOL_VERSION:
        findings.append(Finding("PROTOCOL_VERSION_MISMATCH", "BLOCK", "$.protocol_version", f"Expected {PROTOCOL_VERSION}."))

    if bundle.get("claim_allowed") is not False:
        findings.append(Finding("CLAIM_ALLOWED_MUST_BE_FALSE", "BLOCK", "$.claim_allowed", "Composite gate must remain fail-closed."))

    cognitive_payload = bundle.get("cognitive_payload")
    cognitive_receipt = bundle.get("cognitive_receipt")
    locator_receipt = bundle.get("locator_receipt")
    if not isinstance(cognitive_payload, dict):
        findings.append(Finding("COGNITIVE_PAYLOAD_REQUIRED", "BLOCK", "$.cognitive_payload", "Original cognitive payload is required."))
        cognitive_payload = {}
    if not isinstance(cognitive_receipt, dict):
        findings.append(Finding("COGNITIVE_RECEIPT_REQUIRED", "BLOCK", "$.cognitive_receipt", "Cognitive receipt is required."))
        cognitive_receipt = {}
    if not isinstance(locator_receipt, dict):
        findings.append(Finding("LOCATOR_RECEIPT_REQUIRED", "BLOCK", "$.locator_receipt", "Locator receipt is required."))
        locator_receipt = {}

    if cognitive_receipt:
        if not receipt_hash_is_valid(cognitive_receipt):
            findings.append(Finding("COGNITIVE_RECEIPT_HASH_INVALID", "BLOCK", "$.cognitive_receipt.receipt_sha256", "Cognitive receipt self-hash does not match its content."))
        expected_input = sha256_json(cognitive_payload)
        if cognitive_receipt.get("input_sha256") != expected_input:
            findings.append(Finding("COGNITIVE_INPUT_HASH_MISMATCH", "BLOCK", "$.cognitive_receipt.input_sha256", "Cognitive receipt does not belong to the supplied cognitive payload."))
        if cognitive_receipt.get("structural_pass") is not True:
            findings.append(Finding("COGNITIVE_GATE_NOT_PASSED", "BLOCK", "$.cognitive_receipt.structural_pass", "Cognitive structural gate must pass before identity linkage."))
        if cognitive_receipt.get("claim_allowed") is not False:
            findings.append(Finding("COGNITIVE_RECEIPT_PROMOTION_FORBIDDEN", "BLOCK", "$.cognitive_receipt.claim_allowed", "Upstream cognitive receipt must remain fail-closed."))

    if locator_receipt:
        if not receipt_hash_is_valid(locator_receipt):
            findings.append(Finding("LOCATOR_RECEIPT_HASH_INVALID", "BLOCK", "$.locator_receipt.receipt_sha256", "Locator receipt self-hash does not match its content."))
        if locator_receipt.get("claim_allowed") is not False or locator_receipt.get("epistemic_promotion_allowed") is not False:
            findings.append(Finding("LOCATOR_RECEIPT_PROMOTION_FORBIDDEN", "BLOCK", "$.locator_receipt", "Locator receipt cannot authorize epistemic promotion."))
        if locator_receipt.get("artifact_identity_gate") != "PASS":
            findings.append(Finding("ARTIFACT_IDENTITY_GATE_NOT_PASSED", "BLOCK", "$.locator_receipt.artifact_identity_gate", "Locator identity gate did not pass."))
        if locator_receipt.get("all_referenced_hashes_match") is not True:
            findings.append(Finding("REFERENCED_HASHES_NOT_ALL_MATCH", "BLOCK", "$.locator_receipt.all_referenced_hashes_match", "All referenced evidence must be HASH_MATCH."))

    evidence_by_id: dict[str, dict[str, Any]] = {}
    evidence = cognitive_payload.get("evidence", [])
    if not isinstance(evidence, list):
        findings.append(Finding("COGNITIVE_EVIDENCE_LIST_REQUIRED", "BLOCK", "$.cognitive_payload.evidence", "Evidence must be a list."))
        evidence = []
    for index, item in enumerate(evidence):
        if isinstance(item, dict) and _is_nonempty_text(item.get("id")):
            evidence_by_id[item["id"]] = item
        else:
            findings.append(Finding("COGNITIVE_EVIDENCE_INVALID", "BLOCK", f"$.cognitive_payload.evidence[{index}]", "Evidence item requires an id."))

    locator_by_id: dict[str, dict[str, Any]] = {}
    locator_results = locator_receipt.get("results", []) if isinstance(locator_receipt, dict) else []
    if not isinstance(locator_results, list):
        findings.append(Finding("LOCATOR_RESULTS_LIST_REQUIRED", "BLOCK", "$.locator_receipt.results", "Locator results must be a list."))
        locator_results = []
    for index, result in enumerate(locator_results):
        if isinstance(result, dict) and _is_nonempty_text(result.get("evidence_id")):
            locator_by_id[result["evidence_id"]] = result
        else:
            findings.append(Finding("LOCATOR_RESULT_INVALID", "BLOCK", f"$.locator_receipt.results[{index}]", "Locator result requires evidence_id."))

    cognitive_claim_receipts = {
        item.get("id"): item
        for item in cognitive_receipt.get("claims", [])
        if isinstance(item, dict) and _is_nonempty_text(item.get("id"))
    }

    claims = cognitive_payload.get("claims", [])
    if not isinstance(claims, list):
        findings.append(Finding("COGNITIVE_CLAIMS_LIST_REQUIRED", "BLOCK", "$.cognitive_payload.claims", "Claims must be a list."))
        claims = []

    for index, claim in enumerate(claims):
        path = f"$.cognitive_payload.claims[{index}]"
        if not isinstance(claim, dict) or not _is_nonempty_text(claim.get("id")):
            findings.append(Finding("COGNITIVE_CLAIM_INVALID", "BLOCK", path, "Claim requires an id."))
            continue
        claim_id = claim["id"]
        refs = claim.get("evidence_refs", [])
        if not isinstance(refs, list) or not refs:
            findings.append(Finding("CLAIM_EVIDENCE_REFS_REQUIRED", "BLOCK", f"{path}.evidence_refs", "At least one evidence reference is required."))
            refs = []

        ref_results: list[dict[str, Any]] = []
        claim_blocked = False
        for ref in refs:
            evidence_item = evidence_by_id.get(ref)
            locator_result = locator_by_id.get(ref)
            if evidence_item is None:
                findings.append(Finding("CLAIM_EVIDENCE_REF_UNKNOWN", "BLOCK", f"{path}.evidence_refs", f"Unknown cognitive evidence ref: {ref}"))
                claim_blocked = True
                continue
            if locator_result is None:
                findings.append(Finding("CLAIM_EVIDENCE_NOT_RESOLVED", "BLOCK", f"{path}.evidence_refs", f"No locator result for evidence ref: {ref}"))
                claim_blocked = True
                continue

            status = locator_result.get("status")
            linked = {
                "evidence_id": ref,
                "status": status,
                "locator": locator_result.get("locator"),
                "expected_sha256": locator_result.get("expected_sha256"),
                "actual_sha256": locator_result.get("actual_sha256"),
            }
            ref_results.append(linked)

            if status != MATCH:
                code = "CLAIM_EVIDENCE_IDENTITY_BLOCKED" if status in BLOCKING_LOCATOR_STATES else "CLAIM_EVIDENCE_STATUS_INVALID"
                findings.append(Finding(code, "BLOCK", f"{path}.evidence_refs", f"Evidence {ref} has locator status {status!r}."))
                claim_blocked = True

            if locator_result.get("locator") != evidence_item.get("locator"):
                findings.append(Finding("EVIDENCE_LOCATOR_LINK_MISMATCH", "BLOCK", f"{path}.evidence_refs", f"Locator differs for evidence {ref}."))
                claim_blocked = True

            declared_sha = evidence_item.get("sha256")
            expected_sha = locator_result.get("expected_sha256")
            actual_sha = locator_result.get("actual_sha256")
            if not (declared_sha == expected_sha == actual_sha):
                findings.append(Finding("EVIDENCE_SHA_LINK_MISMATCH", "BLOCK", f"{path}.evidence_refs", f"Declared, expected and observed SHA-256 differ for evidence {ref}."))
                claim_blocked = True

        cognitive_claim = cognitive_claim_receipts.get(claim_id)
        if cognitive_claim is None:
            findings.append(Finding("COGNITIVE_CLAIM_RECEIPT_MISSING", "BLOCK", path, f"Cognitive receipt has no result for claim {claim_id}."))
            claim_blocked = True

        claim_results.append({
            "id": claim_id,
            "identity_supported": not claim_blocked and bool(refs),
            "promotion_readiness": "READY_FOR_DOMAIN_SPECIFIC_REVIEW" if not claim_blocked and bool(refs) else "BLOCKED_BY_ARTIFACT_IDENTITY",
            "claim_allowed": False,
            "evidence_identity": ref_results,
            "cognitive_state": cognitive_claim.get("inferred_state") if isinstance(cognitive_claim, dict) else None,
        })

    return findings, claim_results


def build_receipt(bundle: dict[str, Any]) -> dict[str, Any]:
    findings, claim_results = validate_bundle(bundle)
    blocking = [asdict(item) for item in findings if item.severity == "BLOCK"]
    structural_pass = not blocking
    ready_claims = sum(1 for item in claim_results if item["promotion_readiness"] == "READY_FOR_DOMAIN_SPECIFIC_REVIEW")
    core = {
        "protocol_version": PROTOCOL_VERSION,
        "input_sha256": sha256_json(bundle),
        "structural_pass": structural_pass,
        "artifact_identity_link_gate": "PASS" if structural_pass else "BLOCKED",
        "claim_allowed": False,
        "epistemic_promotion_allowed": False,
        "blocking_findings": blocking,
        "claims": claim_results,
        "ready_for_domain_specific_review_count": ready_claims,
        "r3": {
            "F_ok": "Every claim evidence ref is linked to matching observed bytes." if structural_pass else "Bundle preserved and audited fail-closed.",
            "F_gap": "Domain truth, causal validity and independent replication remain outside this gate." if structural_pass else f"{len(blocking)} blocking finding(s).",
            "F_next": "Route ready claims to the domain-specific scientific/computational gate; never promote from byte identity alone.",
        },
    }
    core["receipt_sha256"] = sha256_json(core)
    return core


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Link cognitive claims to locator-resolved artifact identities.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    try:
        bundle = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(bundle, dict):
            raise ContractError("Top-level JSON must be an object.")
        receipt = build_receipt(bundle)
    except (OSError, json.JSONDecodeError, ContractError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    rendered = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 1 if args.strict and not receipt["structural_pass"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
