#!/usr/bin/env python3
"""Fail-closed validator for RAFAELIA proof-custody receipts.

Uses only the Python standard library so it can run in Termux or a clean host.
A structurally valid receipt may report token_valid=false: preserved uncertainty
is an auditable result, not a validator failure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_TOP = {
    "schema",
    "receipt_id",
    "observed_at",
    "source",
    "artifacts",
    "verification",
    "governance",
    "decision",
}


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def valid_sha40(value: Any) -> bool:
    return isinstance(value, str) and SHA40.fullmatch(value) is not None


def valid_sha64(value: Any) -> bool:
    return isinstance(value, str) and SHA64.fullmatch(value) is not None


def nonempty_string_list(value: Any) -> bool:
    return (
        isinstance(value, list)
        and len(value) > 0
        and all(nonempty_string(item) for item in value)
    )


def gate_is_evidenced(gate: Any) -> bool:
    return (
        isinstance(gate, dict)
        and gate.get("executed_in_this_audit") is True
        and gate.get("pass") is True
        and nonempty_string(gate.get("toolchain"))
        and nonempty_string_list(gate.get("commands"))
        and nonempty_string(gate.get("receipt"))
    )


def validate_receipt(receipt: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    require(REQUIRED_TOP <= receipt.keys(), "missing required top-level fields", errors)
    require(
        receipt.get("schema") == "rafaelia.proof-custody-receipt.v1",
        "unexpected receipt schema",
        errors,
    )
    require(
        policy.get("schema") == "rafaelia.proof-custody-gate.v1",
        "unexpected policy schema",
        errors,
    )

    source = receipt.get("source", {})
    require(isinstance(source, dict), "source must be an object", errors)
    source_sha_valid = isinstance(source, dict) and valid_sha40(source.get("commit_sha"))
    require(source_sha_valid,
            "source.commit_sha must be a 40-character lowercase SHA", errors)

    artifacts = receipt.get("artifacts", [])
    require(isinstance(artifacts, list) and len(artifacts) > 0,
            "artifacts must be a non-empty array", errors)
    paths: set[str] = set()
    artifact_shas_valid = isinstance(artifacts, list) and len(artifacts) > 0
    if isinstance(artifacts, list):
        for index, artifact in enumerate(artifacts):
            require(isinstance(artifact, dict), f"artifact[{index}] must be an object", errors)
            if not isinstance(artifact, dict):
                artifact_shas_valid = False
                continue
            path = artifact.get("path")
            blob_sha = artifact.get("blob_sha")
            require(nonempty_string(path), f"artifact[{index}].path is required", errors)
            if nonempty_string(path):
                require(path not in paths, f"duplicate artifact path: {path}", errors)
                paths.add(path)
            sha_ok = valid_sha40(blob_sha)
            artifact_shas_valid = artifact_shas_valid and sha_ok
            require(sha_ok,
                    f"artifact[{index}].blob_sha must be a 40-character lowercase SHA", errors)

    verification = receipt.get("verification", {})
    governance = receipt.get("governance", {})
    decision = receipt.get("decision", {})
    require(isinstance(verification, dict), "verification must be an object", errors)
    require(isinstance(governance, dict), "governance must be an object", errors)
    require(isinstance(decision, dict), "decision must be an object", errors)

    build = verification.get("build", {}) if isinstance(verification, dict) else {}
    checker = verification.get("independent_checker", {}) if isinstance(verification, dict) else {}
    blocking = decision.get("blocking_token_vazio", []) if isinstance(decision, dict) else []

    build_evidenced = gate_is_evidenced(build)
    checker_evidenced = gate_is_evidenced(checker)
    if isinstance(build, dict) and build.get("pass") is True:
        require(build_evidenced,
                "build pass requires execution, toolchain, commands and receipt", errors)
    if isinstance(checker, dict) and checker.get("pass") is True:
        require(checker_evidenced,
                "checker pass requires execution, toolchain, commands and receipt", errors)

    review_approved = isinstance(governance, dict) and governance.get("independent_review_approved") is True
    review_evidenced = (
        review_approved
        and isinstance(governance.get("reviews_observed"), int)
        and governance.get("reviews_observed") > 0
        and nonempty_string(governance.get("reviewer_identity"))
        and valid_sha40(governance.get("reviewed_commit_sha"))
        and governance.get("reviewed_commit_sha") == source.get("commit_sha")
        and nonempty_string(governance.get("approval_receipt"))
    )
    if review_approved:
        require(review_evidenced,
                "independent review requires reviewer, exact reviewed SHA and approval receipt", errors)

    merged_flag = isinstance(governance, dict) and governance.get("merged_on_protected_edge") is True
    merged_evidenced = merged_flag and valid_sha40(governance.get("merge_commit_sha"))
    if merged_flag:
        require(merged_evidenced,
                "protected merge requires a valid merge_commit_sha", errors)

    checks_flag = isinstance(governance, dict) and governance.get("required_checks_pass") is True
    checks_evidenced = checks_flag and nonempty_string_list(governance.get("combined_status_checks"))
    if checks_flag:
        require(checks_evidenced,
                "required checks pass requires at least one named status check", errors)

    digest_flag = isinstance(decision, dict) and decision.get("receipt_digest_present") is True
    digest_evidenced = digest_flag and valid_sha64(decision.get("receipt_payload_sha256"))
    if digest_flag:
        require(digest_evidenced,
                "receipt digest present requires a 64-character lowercase SHA-256", errors)

    blocking_valid = isinstance(blocking, list) and all(nonempty_string(item) for item in blocking)
    require(blocking_valid, "blocking_token_vazio must be an array of non-empty strings", errors)

    predicate = {
        "hash_bound": (
            isinstance(verification, dict)
            and verification.get("hash_bound") is True
            and source_sha_valid
            and artifact_shas_valid
        ),
        "build_pass": build_evidenced,
        "checker_pass": checker_evidenced,
        "independent_review_approved": review_evidenced,
        "merged_on_protected_edge": merged_evidenced,
        "required_checks_pass": checks_evidenced,
        "receipt_digest_present": digest_evidenced,
        "no_blocking_token_vazio": blocking_valid and len(blocking) == 0,
    }

    required_predicates = policy.get("token_valid_predicate", {}).get("all_required", [])
    require(isinstance(required_predicates, list) and len(required_predicates) > 0,
            "policy token_valid_predicate.all_required must be non-empty", errors)
    unknown = [name for name in required_predicates if name not in predicate]
    require(not unknown, f"policy references unknown predicates: {unknown}", errors)

    computed_token_valid = not unknown and all(predicate[name] for name in required_predicates)
    declared_token_valid = isinstance(decision, dict) and decision.get("token_valid") is True
    require(declared_token_valid == computed_token_valid,
            "decision.token_valid does not match the fail-closed predicate", errors)
    require(not (isinstance(decision, dict)
                 and decision.get("claim_allowed") is True
                 and not computed_token_valid),
            "claim_allowed=true is forbidden while token_valid=false", errors)

    return {
        "receipt_valid": not errors,
        "token_valid": computed_token_valid,
        "predicate": predicate,
        "blocking_token_vazio": blocking if blocking_valid else ["INVALID_BLOCKING_FIELD"],
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument(
        "--policy",
        type=Path,
        default=Path("data/control-plane/proof-custody-gate.v1.json"),
    )
    args = parser.parse_args()

    try:
        receipt_bytes = args.receipt.read_bytes()
        receipt = load_json(args.receipt)
        policy = load_json(args.policy)
        result = validate_receipt(receipt, policy)
        result["receipt_file_sha256"] = hashlib.sha256(receipt_bytes).hexdigest()
    except (OSError, ValueError) as exc:
        print(json.dumps({"receipt_valid": False, "errors": [str(exc)]}, indent=2))
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["receipt_valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
