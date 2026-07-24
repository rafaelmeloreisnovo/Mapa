#!/usr/bin/env python3
"""Evaluate cross-source gate reports against a versioned growth-safe floor."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")
    return value


def add_check(
    checks: list[dict[str, Any]],
    name: str,
    observed: Any,
    operator: str,
    required: Any,
) -> None:
    if operator == "eq":
        passed = observed == required
    elif operator == "ge":
        passed = (
            isinstance(observed, int)
            and not isinstance(observed, bool)
            and isinstance(required, int)
            and not isinstance(required, bool)
            and observed >= required
        )
    else:
        raise ValueError(f"unsupported operator: {operator}")
    checks.append(
        {
            "name": name,
            "observed": observed,
            "operator": operator,
            "required": required,
            "passed": passed,
        }
    )


def evaluate(
    floor: dict[str, Any],
    records: dict[str, Any],
    registry: dict[str, Any],
    custody: dict[str, Any],
    tests: dict[str, Any],
) -> dict[str, Any]:
    minimums = floor.get("minimums")
    invariants = floor.get("invariants")
    if not isinstance(minimums, dict) or not isinstance(invariants, dict):
        raise ValueError("quality floor requires object fields: minimums and invariants")

    checks: list[dict[str, Any]] = []

    for report_name, report in (
        ("records", records),
        ("registry", registry),
        ("custody", custody),
        ("tests", tests),
    ):
        add_check(checks, f"{report_name}.status", report.get("status"), "eq", "PASS")
        add_check(
            checks,
            f"{report_name}.claim_allowed",
            report.get("claim_allowed"),
            "eq",
            invariants.get("claim_allowed"),
        )

    add_check(
        checks,
        "tests.remote_ci_substituted",
        tests.get("remote_ci_substituted"),
        "eq",
        invariants.get("remote_ci_substituted"),
    )
    add_check(
        checks,
        "tests.complete_execution",
        tests.get("complete_execution"),
        "eq",
        invariants.get("complete_execution"),
    )
    add_check(
        checks,
        "tests.test_file_count",
        tests.get("test_file_count"),
        "ge",
        minimums.get("test_files"),
    )
    add_check(
        checks,
        "tests.tests_discovered",
        tests.get("tests_discovered"),
        "ge",
        minimums.get("tests_discovered"),
    )
    add_check(
        checks,
        "tests.tests_run",
        tests.get("tests_run"),
        "ge",
        minimums.get("tests_run"),
    )
    add_check(
        checks,
        "tests.run_matches_discovery",
        tests.get("tests_run"),
        "eq",
        tests.get("tests_discovered"),
    )
    add_check(checks, "tests.failures", tests.get("failures"), "eq", 0)
    add_check(checks, "tests.errors", tests.get("errors"), "eq", 0)

    add_check(
        checks,
        "records.valid_fixture_count",
        records.get("valid_fixture_count"),
        "ge",
        minimums.get("valid_fixtures"),
    )
    add_check(
        checks,
        "records.invalid_fixture_count",
        records.get("invalid_fixture_count"),
        "ge",
        minimums.get("invalid_fixtures"),
    )
    add_check(
        checks,
        "records.unexpected_failures",
        records.get("unexpected_failures"),
        "eq",
        invariants.get("unexpected_failures"),
    )
    add_check(
        checks,
        "records.unexpected_passes",
        records.get("unexpected_passes"),
        "eq",
        invariants.get("unexpected_passes"),
    )

    add_check(
        checks,
        "registry.record_count",
        registry.get("record_count"),
        "ge",
        minimums.get("registry_records"),
    )
    provider_counts = registry.get("provider_counts")
    provider_counts = provider_counts if isinstance(provider_counts, dict) else {}
    required_provider_counts = minimums.get("provider_counts")
    if not isinstance(required_provider_counts, dict):
        raise ValueError("quality floor minimums.provider_counts must be an object")
    for provider, minimum in sorted(required_provider_counts.items()):
        add_check(
            checks,
            f"registry.provider_counts.{provider}",
            provider_counts.get(provider, 0),
            "ge",
            minimum,
        )
    add_check(
        checks,
        "registry.defect_count",
        registry.get("defect_count"),
        "eq",
        invariants.get("defect_count"),
    )

    add_check(
        checks,
        "custody.event_count",
        custody.get("event_count"),
        "ge",
        minimums.get("custody_events"),
    )
    add_check(
        checks,
        "custody.defect_count",
        custody.get("defect_count"),
        "eq",
        invariants.get("defect_count"),
    )

    failed = [check for check in checks if not check["passed"]]
    status = "PASS" if not failed else "FAIL"
    return {
        "schema_version": "rafaelia.cross-source-gate-evaluation/v2",
        "status": status,
        "floor_schema_version": floor.get("schema_version"),
        "comparison": "observed_greater_than_or_equal_to_minimum",
        "check_count": len(checks),
        "failed_check_count": len(failed),
        "checks": checks,
        "claim_allowed": False,
        "remote_ci_substituted": False,
        "promotion_state": (
            "LOCAL_PASS_REMOTE_TOKEN_VAZIO" if status == "PASS" else "BLOCKED"
        ),
        "next_verifiable_step": (
            "Obtain an independently started remote runner and compare sealed artifacts."
            if status == "PASS"
            else "Correct failed floor checks without lowering the floor in the same change."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--floor", type=Path, required=True)
    parser.add_argument("--records-report", type=Path, required=True)
    parser.add_argument("--registry-report", type=Path, required=True)
    parser.add_argument("--custody-report", type=Path, required=True)
    parser.add_argument("--test-report", type=Path, required=True)
    parser.add_argument("--write-report", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = evaluate(
        load_object(args.floor),
        load_object(args.records_report),
        load_object(args.registry_report),
        load_object(args.custody_report),
        load_object(args.test_report),
    )
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
