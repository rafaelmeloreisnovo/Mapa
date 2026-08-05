#!/usr/bin/env python3
"""Fail-closed pull-request promotion control for RAFAELIA.

The control evaluates GitHub pull-request event metadata plus review records.
It does not infer intent from missing evidence: an unreadable event, missing
policy, ambiguous review state, draft PR, enabled auto-merge, or an explicit
do-not-merge declaration results in DENIED.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

EXIT_ALLOWED = 0
EXIT_DENIED = 3
EXIT_INVALID = 4


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load {path}: {exc}") from exc


def normalize_text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def compile_patterns(values: Any, field: str) -> list[re.Pattern[str]]:
    if not isinstance(values, list) or not all(isinstance(item, str) and item for item in values):
        raise ValueError(f"{field} must be a non-empty string array")
    return [re.compile(item, re.IGNORECASE | re.MULTILINE) for item in values]


def pull_request_from_event(event: Any) -> dict[str, Any]:
    if not isinstance(event, dict):
        raise ValueError("event must be a JSON object")
    pr = event.get("pull_request")
    if not isinstance(pr, dict):
        raise ValueError("event.pull_request must be a JSON object")
    return pr


def latest_reviews_by_actor(reviews: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(reviews, list):
        raise ValueError("reviews must be a JSON array")
    latest: dict[str, dict[str, Any]] = {}
    for index, review in enumerate(reviews):
        if not isinstance(review, dict):
            raise ValueError(f"reviews[{index}] must be a JSON object")
        user = review.get("user")
        login = user.get("login") if isinstance(user, dict) else None
        if not isinstance(login, str) or not login:
            raise ValueError(f"reviews[{index}].user.login is required")
        latest[login.casefold()] = review
    return latest


def count_independent_approvals(
    reviews: Any,
    author_login: str,
    ignore_bot_suffix: str,
) -> tuple[int, list[str]]:
    latest = latest_reviews_by_actor(reviews)
    approved: list[str] = []
    for folded_login, review in latest.items():
        user = review["user"]
        login = user["login"]
        state = normalize_text(review.get("state")).upper()
        if folded_login == author_login.casefold():
            continue
        if ignore_bot_suffix and folded_login.endswith(ignore_bot_suffix.casefold()):
            continue
        if state == "APPROVED":
            approved.append(login)
    approved.sort(key=str.casefold)
    return len(approved), approved


def evaluate(event: Any, reviews: Any, policy: Any) -> dict[str, Any]:
    if not isinstance(policy, dict):
        raise ValueError("policy must be a JSON object")
    if policy.get("schema") != "rafaelia.promotion-control/v1":
        raise ValueError("unexpected policy schema")

    required_approvals = policy.get("required_independent_approvals")
    if not isinstance(required_approvals, int) or required_approvals < 1:
        raise ValueError("required_independent_approvals must be an integer >= 1")

    deny_patterns = compile_patterns(policy.get("deny_body_patterns"), "deny_body_patterns")
    review_patterns = compile_patterns(
        policy.get("human_review_required_patterns"),
        "human_review_required_patterns",
    )
    ignore_bot_suffix = policy.get("ignore_bot_login_suffix", "[bot]")
    if not isinstance(ignore_bot_suffix, str):
        raise ValueError("ignore_bot_login_suffix must be a string")

    pr = pull_request_from_event(event)
    author = pr.get("user")
    author_login = author.get("login") if isinstance(author, dict) else None
    if not isinstance(author_login, str) or not author_login:
        raise ValueError("pull_request.user.login is required")

    body = normalize_text(pr.get("body"))
    blockers: list[str] = []
    evidence: list[str] = []

    if pr.get("state") != "open":
        blockers.append("PULL_REQUEST_NOT_OPEN")
    if pr.get("draft") is not False:
        blockers.append("PULL_REQUEST_DRAFT_OR_UNKNOWN")
    if pr.get("merged") is True:
        blockers.append("PULL_REQUEST_ALREADY_MERGED")
    if pr.get("auto_merge") is not None:
        blockers.append("AUTO_MERGE_ENABLED")

    matched_deny_patterns = [pattern.pattern for pattern in deny_patterns if pattern.search(body)]
    if matched_deny_patterns:
        blockers.append("EXPLICIT_BODY_DENIAL")
        evidence.extend(f"body_pattern:{pattern}" for pattern in matched_deny_patterns)

    human_review_required = any(pattern.search(body) for pattern in review_patterns)
    approval_count, approved_by = count_independent_approvals(
        reviews,
        author_login=author_login,
        ignore_bot_suffix=ignore_bot_suffix,
    )
    if human_review_required and approval_count < required_approvals:
        blockers.append("HUMAN_REVIEW_MISSING")

    result = "ALLOWED_FOR_MANUAL_MERGE" if not blockers else "DENIED"
    return {
        "schema": "rafaelia.promotion-control-result/v1",
        "result": result,
        "claim_allowed": False,
        "automatic_merge": False,
        "manual_merge_only": True,
        "human_review_required": human_review_required,
        "required_independent_approvals": required_approvals,
        "observed_independent_approvals": approval_count,
        "approved_by": approved_by,
        "blocking_reasons": blockers,
        "evidence": evidence,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", type=Path, required=True)
    parser.add_argument("--reviews", type=Path, required=True)
    parser.add_argument(
        "--policy",
        type=Path,
        default=Path("data/control-plane/promotion-control.v1.json"),
    )
    args = parser.parse_args(argv)

    try:
        result = evaluate(
            load_json(args.event),
            load_json(args.reviews),
            load_json(args.policy),
        )
    except ValueError as exc:
        invalid = {
            "schema": "rafaelia.promotion-control-result/v1",
            "result": "DENIED_INVALID_INPUT",
            "claim_allowed": False,
            "automatic_merge": False,
            "blocking_reasons": ["INVALID_OR_MISSING_EVIDENCE"],
            "error": str(exc),
        }
        json.dump(invalid, sys.stdout, ensure_ascii=False, sort_keys=True)
        sys.stdout.write("\n")
        return EXIT_INVALID

    json.dump(result, sys.stdout, ensure_ascii=False, sort_keys=True)
    sys.stdout.write("\n")
    return EXIT_ALLOWED if result["result"] == "ALLOWED_FOR_MANUAL_MERGE" else EXIT_DENIED


if __name__ == "__main__":
    raise SystemExit(main())
