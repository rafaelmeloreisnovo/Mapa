#!/usr/bin/env python3
"""Plan or apply GitHub main-branch protection for RAFAELIA Promotion Control.

Default mode is non-mutating.  --apply requires RAFAELIA_ADMIN_TOKEN and
re-observes the provider state after the PUT.  The script never attempts a
merge and never upgrades claim_allowed from false.

VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM
TOKEN_VAZIO != 0
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

API_VERSION = "2026-03-10"
SCHEMA = "rafaelia.provider-merge-protection-bootstrap/v1"
DEFAULT_CONTEXT = "promotion-control / enforce"


def protection_payload(required_context: str) -> dict[str, Any]:
    return {
        "required_status_checks": {
            "strict": True,
            "contexts": [required_context],
        },
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": False,
            "required_approving_review_count": 1,
            "require_last_push_approval": True,
        },
        "restrictions": None,
    }


def _request(url: str, *, token: str | None = None, method: str = "GET", payload: dict[str, Any] | None = None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": "rafaelia-provider-merge-protection-bootstrap",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = None
    if payload is not None:
        data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, headers=headers, data=data, method=method)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def fetch_branch(repo: str, branch: str, token: str | None = None) -> dict[str, Any]:
    return _request(f"https://api.github.com/repos/{repo}/branches/{branch}", token=token)


def fetch_protection(repo: str, branch: str, token: str) -> dict[str, Any]:
    return _request(f"https://api.github.com/repos/{repo}/branches/{branch}/protection", token=token)


def apply_protection(repo: str, branch: str, token: str, required_context: str) -> dict[str, Any]:
    return _request(
        f"https://api.github.com/repos/{repo}/branches/{branch}/protection",
        token=token,
        method="PUT",
        payload=protection_payload(required_context),
    )


def verify_observed(branch_data: dict[str, Any], protection: dict[str, Any], required_context: str) -> list[str]:
    failures: list[str] = []
    if branch_data.get("protected") is not True:
        failures.append("BRANCH_NOT_PROTECTED")

    status_checks = protection.get("required_status_checks") or {}
    observed_contexts = set(status_checks.get("contexts") or [])
    for check in status_checks.get("checks") or []:
        if isinstance(check, dict) and check.get("context"):
            observed_contexts.add(check["context"])
    if required_context not in observed_contexts:
        failures.append("PROMOTION_CONTROL_CONTEXT_NOT_REQUIRED")

    enforce_admins = protection.get("enforce_admins") or {}
    if enforce_admins.get("enabled") is not True:
        failures.append("ADMINS_NOT_ENFORCED")

    reviews = protection.get("required_pull_request_reviews") or {}
    if int(reviews.get("required_approving_review_count") or 0) < 1:
        failures.append("ZERO_APPROVAL_NOT_PROVIDER_BLOCKED_BY_REVIEW_RULE")

    return failures


def render_receipt(*, repo: str, branch: str, required_context: str, before_sha: str, after_sha: str | None,
                   mode: str, status: str, failures: list[str], provider_response: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA,
        "repo": repo,
        "branch": branch,
        "required_context": required_context,
        "mode": mode,
        "status": status,
        "before_main_sha": before_sha,
        "after_main_sha": after_sha if after_sha is not None else "TOKEN_VAZIO_NOT_APPLIED",
        "failure_modes": failures,
        "provider_response_observed": provider_response is not None,
        "claim_allowed": False,
        "promotion_allowed": False,
        "epistemic_boundary": [
            "Configuration evidence is not zero-approval merge rejection evidence.",
            "No merge endpoint is called by this script.",
            "claim_allowed remains false until the dedicated server-side rejection receipt exists.",
        ],
        "next_gate": "SERVER_SIDE_ZERO_APPROVAL_REJECTED_MERGE_RECEIPT",
    }


def write_receipt(path: str | None, receipt: dict[str, Any]) -> None:
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", "rafaelmeloreisnovo/Mapa"))
    parser.add_argument("--branch", default="main")
    parser.add_argument("--required-context", default=DEFAULT_CONTEXT)
    parser.add_argument("--expected-main-sha")
    parser.add_argument("--write-receipt")
    parser.add_argument("--apply", action="store_true", help="Mutate provider protection; requires RAFAELIA_ADMIN_TOKEN")
    args = parser.parse_args()

    token = os.environ.get("RAFAELIA_ADMIN_TOKEN") if args.apply else None
    if args.apply and not token:
        print("TOKEN_VAZIO_RAFAELIA_ADMIN_TOKEN: --apply refused", file=sys.stderr)
        return 20

    try:
        before = fetch_branch(args.repo, args.branch, token)
    except urllib.error.HTTPError as exc:
        print(f"provider branch read failed: HTTP {exc.code}", file=sys.stderr)
        return 21

    before_sha = ((before.get("commit") or {}).get("sha") or "TOKEN_VAZIO_MAIN_SHA")
    if args.expected_main_sha and before_sha != args.expected_main_sha:
        print(
            f"MAIN_SHA_PRECONDITION_FAILED expected={args.expected_main_sha} observed={before_sha}",
            file=sys.stderr,
        )
        return 22

    if not args.apply:
        receipt = render_receipt(
            repo=args.repo,
            branch=args.branch,
            required_context=args.required_context,
            before_sha=before_sha,
            after_sha=None,
            mode="PLAN_ONLY",
            status="TOKEN_VAZIO_ADMIN_CREDENTIAL_NOT_USED",
            failures=["PROVIDER_MUTATION_NOT_EXECUTED"],
        )
        write_receipt(args.write_receipt, receipt)
        return 0

    try:
        provider_response = apply_protection(args.repo, args.branch, token, args.required_context)
        after = fetch_branch(args.repo, args.branch, token)
        protection = fetch_protection(args.repo, args.branch, token)
    except urllib.error.HTTPError as exc:
        print(f"provider protection mutation/readback failed: HTTP {exc.code}", file=sys.stderr)
        return 23

    after_sha = ((after.get("commit") or {}).get("sha") or "TOKEN_VAZIO_MAIN_SHA")
    failures = verify_observed(after, protection, args.required_context)
    if after_sha != before_sha:
        failures.append("MAIN_SHA_CHANGED_DURING_PROTECTION_CONFIGURATION")

    status = "APPLIED_AND_REOBSERVED" if not failures else "BLOCKED_AFTER_APPLY"
    receipt = render_receipt(
        repo=args.repo,
        branch=args.branch,
        required_context=args.required_context,
        before_sha=before_sha,
        after_sha=after_sha,
        mode="APPLY",
        status=status,
        failures=failures,
        provider_response=provider_response,
    )
    write_receipt(args.write_receipt, receipt)
    return 0 if not failures else 24


if __name__ == "__main__":
    sys.exit(main())
