#!/usr/bin/env python3
"""Validate the RAFAELIA numbered branch topology without external dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

LANE_PATTERN = re.compile(r"^main_(\d{2})_[a-z0-9_]+$")
REQUIRED_PROMOTION_FIELDS = (
    "source",
    "claim_state",
    "evidence",
    "falsifier",
    "rollback",
    "decision",
)


class TopologyError(ValueError):
    """Raised when the branch topology contract is violated."""


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise TopologyError(f"manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise TopologyError(f"invalid JSON manifest: {exc}") from exc
    if not isinstance(data, dict):
        raise TopologyError("manifest root must be an object")
    return data


def validate_manifest(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if data.get("default_branch") != "main":
        errors.append("default_branch must remain 'main'")
    if data.get("promotion_target") != "main":
        errors.append("promotion_target must be 'main'")
    if data.get("automatic_merge") is not False:
        errors.append("automatic_merge must be false")
    if data.get("automatic_default_branch_change") is not False:
        errors.append("automatic_default_branch_change must be false")

    lanes = data.get("lanes")
    if not isinstance(lanes, list):
        return errors + ["lanes must be a list"]
    if len(lanes) != 10:
        errors.append(f"expected 10 lanes, found {len(lanes)}")

    seen_orders: set[int] = set()
    seen_branches: set[str] = set()
    for lane in lanes:
        if not isinstance(lane, dict):
            errors.append("every lane must be an object")
            continue
        order = lane.get("order")
        branch = lane.get("branch")
        if not isinstance(order, int) or not 0 <= order <= 9:
            errors.append(f"invalid lane order: {order!r}")
            continue
        if order in seen_orders:
            errors.append(f"duplicate lane order: {order:02d}")
        seen_orders.add(order)

        if not isinstance(branch, str) or not LANE_PATTERN.fullmatch(branch):
            errors.append(f"invalid lane branch: {branch!r}")
            continue
        expected_prefix = f"main_{order:02d}_"
        if not branch.startswith(expected_prefix):
            errors.append(
                f"lane order {order:02d} must use prefix {expected_prefix!r}: {branch}"
            )
        if branch in seen_branches:
            errors.append(f"duplicate lane branch: {branch}")
        seen_branches.add(branch)

    expected_orders = set(range(10))
    if seen_orders != expected_orders:
        missing = sorted(expected_orders - seen_orders)
        extra = sorted(seen_orders - expected_orders)
        errors.append(f"lane order set mismatch; missing={missing}, extra={extra}")

    required = data.get("required_promotion_fields")
    if required != list(REQUIRED_PROMOTION_FIELDS):
        errors.append("required_promotion_fields differs from canonical order")

    return errors


def validate_event(
    data: dict[str, Any],
    *,
    repository_default_branch: str,
    base_ref: str,
    head_ref: str,
    pr_body: str,
) -> list[str]:
    errors: list[str] = []
    lane_names = {lane["branch"] for lane in data.get("lanes", []) if isinstance(lane, dict) and "branch" in lane}

    if repository_default_branch != "main":
        errors.append(
            f"repository default branch changed to {repository_default_branch!r}; expected 'main'"
        )

    if head_ref.startswith("main_") and head_ref not in lane_names:
        errors.append(f"unregistered numbered head branch: {head_ref}")
    if base_ref.startswith("main_") and base_ref not in lane_names:
        errors.append(f"unregistered numbered base branch: {base_ref}")

    if head_ref in lane_names:
        if base_ref != "main":
            errors.append(f"lane promotion must target main, not {base_ref!r}")
        body_lower = pr_body.lower()
        missing_fields = [
            field for field in REQUIRED_PROMOTION_FIELDS if f"{field}:" not in body_lower
        ]
        if missing_fields:
            errors.append(
                "lane promotion PR body is missing fields: " + ", ".join(missing_fields)
            )

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        default="data/governance/branch_topology_main_numbered_v1.json",
    )
    parser.add_argument("--default-branch", default="main")
    parser.add_argument("--base-ref", default="")
    parser.add_argument("--head-ref", default="")
    parser.add_argument("--pr-body-file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = load_manifest(Path(args.manifest))
    errors = validate_manifest(data)

    pr_body = ""
    if args.pr_body_file:
        pr_body = Path(args.pr_body_file).read_text(encoding="utf-8")

    errors.extend(
        validate_event(
            data,
            repository_default_branch=args.default_branch,
            base_ref=args.base_ref,
            head_ref=args.head_ref,
            pr_body=pr_body,
        )
    )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("PASS: numbered branch topology is coherent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
