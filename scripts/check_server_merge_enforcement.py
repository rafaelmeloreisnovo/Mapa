#!/usr/bin/env python3
"""Fail-closed detector for server-side merge enforcement.

This detector does not configure GitHub protection. It only classifies the
observable branch metadata returned by the GitHub branch endpoint.

VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM
TOKEN_VAZIO != 0
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path
from typing import Any

SCHEMA = "rafaelia.server-merge-enforcement-assurance/v1"


def classify_branch(branch: dict[str, Any]) -> dict[str, Any]:
    protection = branch.get("protection") or {}
    status_checks = protection.get("required_status_checks") or {}
    protected = branch.get("protected") is True
    protection_enabled = protection.get("enabled") is True
    enforcement = status_checks.get("enforcement_level")
    contexts = status_checks.get("contexts") or []
    checks = status_checks.get("checks") or []
    checks_present = bool(contexts or checks)

    failures: list[str] = []
    if not protected:
        failures.append("BRANCH_PROTECTION_DISABLED")
    if not protection_enabled:
        failures.append("PROTECTION_NOT_ENABLED")
    if enforcement in (None, "off"):
        failures.append("REQUIRED_STATUS_CHECKS_NOT_ENFORCED")
    if not checks_present:
        failures.append("NO_REQUIRED_STATUS_CHECKS_OBSERVED")

    passed = not failures
    return {
        "schema_version": SCHEMA,
        "branch": branch.get("name", "TOKEN_VAZIO_BRANCH_NAME"),
        "protected": protected,
        "protection_enabled": protection_enabled,
        "required_status_checks": {
            "enforcement_level": enforcement if enforcement is not None else "TOKEN_VAZIO",
            "contexts": contexts,
            "checks": checks,
        },
        "status": "PASS_SCOPED" if passed else "BLOCKED",
        "failure_modes": failures,
        "claim_allowed": False,
        "promotion_allowed": False,
        "server_side_merge_binding": (
            "EVIDENCED_SCOPED_BASELINE" if passed else "NOT_ENFORCED_OBSERVED"
        ),
        "promotion_control_exact_required_context": "TOKEN_VAZIO_NOT_OBSERVED_BY_THIS_ENDPOINT",
        "ruleset_or_bypass_path": "TOKEN_VAZIO_NOT_INSPECTED",
        "next_gate": (
            "PROVE_PROMOTION_CONTROL_CONTEXT_IS_SERVER_REQUIRED_AND_ZERO_APPROVAL_MERGE_IS_BLOCKED"
        ),
    }


def fetch_branch(repo: str, branch: str) -> dict[str, Any]:
    url = f"https://api.github.com/repos/{repo}/branches/{branch}"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "rafaelia-assurance"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def main() -> int:
    parser = argparse.ArgumentParser()
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--input-json")
    src.add_argument("--repo")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--write-report")
    args = parser.parse_args()

    if args.input_json:
        branch_data = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    else:
        branch_data = fetch_branch(args.repo, args.branch)

    report = classify_branch(branch_data)
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")

    return 0 if report["status"] == "PASS_SCOPED" else 2


if __name__ == "__main__":
    sys.exit(main())
