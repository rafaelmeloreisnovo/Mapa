#!/usr/bin/env python3
"""Fail-closed audit for workflow dependency, license and runtime boundaries.

The parser is intentionally small and linear-time. It inspects only structural
invariants needed by this gate and never promotes unverified legal, scientific,
or runtime-compatibility claims. Unknown compatibility remains TOKEN_VAZIO.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

SHA40 = re.compile(r"^[0-9a-fA-F]{40}$")
USES_LINE = re.compile(r"^uses:\s*([^@\s]+)@([^\s#]+)\s*$")


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _permissions_contents(lines: list[str]) -> list[str]:
    """Return top-level permissions.contents values using one forward scan."""
    values: list[str] = []
    in_permissions = False
    permissions_indent = 0

    for raw in lines:
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = _indent(raw)

        if not in_permissions:
            if indent == 0 and stripped == "permissions:":
                in_permissions = True
                permissions_indent = indent
            continue

        if indent <= permissions_indent:
            in_permissions = False
            if indent == 0 and stripped == "permissions:":
                in_permissions = True
                permissions_indent = indent
            continue

        if stripped.startswith("contents:"):
            _, value = stripped.split(":", 1)
            values.append(value.strip())

    return values


def audit(root: Path, workflow_rel: str, license_rel: str) -> dict[str, Any]:
    workflow_path = root / workflow_rel
    license_path = root / license_rel

    workflow = workflow_path.read_text(encoding="utf-8")
    license_text = license_path.read_text(encoding="utf-8")
    lines = workflow.splitlines()

    actions: list[dict[str, Any]] = []
    unpinned: list[dict[str, Any]] = []
    persist_values: list[str] = []
    claim_true_literal = False

    for raw in lines:
        stripped = raw.strip()

        match = USES_LINE.fullmatch(stripped)
        if match:
            action, ref = match.groups()
            item = {
                "action": action,
                "ref": ref,
                "sha_pinned": bool(SHA40.fullmatch(ref)),
            }
            actions.append(item)
            if not item["sha_pinned"]:
                unpinned.append(item)

        if stripped.startswith("persist-credentials:"):
            _, value = stripped.split(":", 1)
            persist_values.append(value.strip().lower())

        normalized = stripped.replace(" ", "").lower()
        if normalized == "claim_allowed:true":
            claim_true_literal = True

    contents_values = _permissions_contents(lines)

    checks = {
        "external_actions_found": bool(actions),
        "all_external_actions_sha_pinned": bool(actions) and not unpinned,
        "contents_permission_read": contents_values == ["read"],
        "contents_permission_write_absent": "write" not in contents_values,
        "checkout_persist_credentials_false": bool(persist_values)
        and all(value == "false" for value in persist_values),
        "claim_promotion_literal_absent": not claim_true_literal,
        "repository_gpl3_text_present": (
            "GNU GENERAL PUBLIC LICENSE" in license_text and "Version 3" in license_text
        ),
    }

    blocking = [name for name, ok in checks.items() if not ok]
    decision = "VERIFIED_BOUNDARY_READ_ONLY" if not blocking else "BLOCKED_POLICY_REGRESSION"

    return {
        "schema": "rafaelia.workflow-dependency-boundary-audit.v1",
        "decision": decision,
        "workflow": workflow_rel,
        "repository_license": license_rel,
        "checks": checks,
        "blocking_regressions": blocking,
        "observed": {
            "permissions_contents_values": contents_values,
            "persist_credentials_values": persist_values,
            "external_action_count": len(actions),
        },
        "actions": actions,
        "token_vazio": {
            "dependency_license_compatibility": "TOKEN_VAZIO_REQUIRES_SEPARATE_LICENSE_REVIEW",
            "pinned_action_node24_native_compatibility": "TOKEN_VAZIO_REQUIRES_EXACT_RELEASE_VERIFICATION",
        },
        "runtime_observation": {
            "known_warning_class": "NODE20_ACTION_RUNTIME_DEPRECATION_RUNNER_FORCED_NODE24",
            "warning_is_compatibility_proof": False,
        },
        "boundaries": {
            "repository_license_does_not_override_dependency_licenses": True,
            "sha_pin_is_provenance_not_license_compatibility": True,
            "runner_success_is_not_native_runtime_compatibility_proof": True,
            "ci_is_not_physical_runtime": True,
            "hash_is_not_truth": True,
        },
        "complexity_contract": {
            "workflow_scan": "O(lines)",
            "catastrophic_regex_backtracking": False,
        },
        "automatic_mutation": False,
        "automatic_merge": False,
        "claim_allowed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--workflow", default=".github/workflows/rafaelia-adaptive-cycle.yml")
    parser.add_argument("--license", dest="license_rel", default="LICENSE")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    result = audit(Path(args.root), args.workflow, args.license_rel)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["decision"] == "VERIFIED_BOUNDARY_READ_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
