#!/usr/bin/env python3
"""Fail-closed validator for RAFAELIA proof-custody receipts.

Uses only the Python standard library so it can run in Termux or a clean host.
A valid receipt may still report token_valid=false; that is an auditable result,
not a validator failure.
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
    require(SHA40.fullmatch(str(source.get("commit_sha", ""))) is not None,
            "source.commit_sha must be a 40-character lowercase SHA", errors)

    artifacts = receipt.get("artifacts", [])
    require(isinstance(artifacts, list) and len(artifacts) > 0,
            "artifacts must be a non-empty array", errors)
    paths: set[str] = set()
    if isinstance(artifacts, list):
        for index, artifact in enumerate(artifacts):
            require(isinstance(artifact, dict), f"artifact[{index}] must be an object", errors)
            if not isinstance(artifact, dict):
                continue
            path = str(artifact.get("path", ""))
            blob_sha = str(artifact.get("blob_sha", ""))
            require(bool(path), f"artifact[{index}].path is required", errors)
            require(path not in paths, f"duplicate artifact path: {path}", errors)
            paths.add(path)
            require(SHA40.fullmatch(blob_sha) is not None,
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

    predicate = {
        "hash_bound": verification.get("hash_bound") is True,
        "build_pass": isinstance(build, dict) and build.get("pass") is True,
        "checker_pass": isinstance(checker, dict) and checker.get("pass") is True,
        "independent_review_approved": governance.get("independent_review_approved") is True,
        "merged_on_protected_edge": governance.get("merged_on_protected_edge") is True,
        "required_checks_pass": governance.get("required_checks_pass") is True,
        "receipt_digest_present": decision.get("receipt_digest_present") is True,
        "no_blocking_token_vazio": isinstance(blocking, list) and len(blocking) == 0,
    }

    required_predicates = policy.get("token_valid_predicate", {}).get("all_required", [])
    require(isinstance(required_predicates, list) and len(required_predicates) > 0,
            "policy token_valid_predicate.all_required must be non-empty", errors)
    unknown = [name for name in required_predicates if name not in predicate]
    require(not unknown, f"policy references unknown predicates: {unknown}", errors)

    computed_token_valid = not unknown and all(predicate[name] for name in required_predicates)
    declared_token_valid = decision.get("token_valid") is True
    require(declared_token_valid == computed_token_valid,
            "decision.token_valid does not match the fail-closed predicate", errors)
    require(not (decision.get("claim_allowed") is True and not computed_token_valid),
            "claim_allowed=true is forbidden while token_valid=false", errors)

    return {
        "receipt_valid": not errors,
        "token_valid": computed_token_valid,
        "predicate": predicate,
        "blocking_token_vazio": blocking if isinstance(blocking, list) else ["INVALID_BLOCKING_FIELD"],
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
        result["receipt_sha256"] = hashlib.sha256(receipt_bytes).hexdigest()
    except (OSError, ValueError) as exc:
        print(json.dumps({"receipt_valid": False, "errors": [str(exc)]}, indent=2))
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["receipt_valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
