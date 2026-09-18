#!/usr/bin/env python3
"""Validate evidence-backed G3 decisions for systematic pragmatic clusters."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SCHEMA = "rafaelia.systematic-pragmatic-g3-decision/v1"
ALLOWED = {
    "DUPLICATE",
    "SAME_FAMILY",
    "DISTINCT_GAP",
    "SPLIT_REQUIRED",
    "FALSE_POSITIVE",
    "ACCEPTED_LIMITATION",
}
SPLIT_STRATEGIES = {"PATH_SEGMENT", "SEMANTIC_SCHEMA"}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {lineno}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"line {lineno}: record must be object")
        rows.append(row)
    return rows


def _partition_view(observed: dict[str, Any]) -> tuple[Any, Any]:
    counts = observed.get("partition_counts")
    distinct = observed.get("distinct_partitions")
    if counts is None:
        counts = observed.get("subdomain_counts")
    if distinct is None:
        distinct = observed.get("distinct_subdomains")
    return counts, distinct


def _valid_counts(
    *,
    where: str,
    action_count: Any,
    counts: Any,
    distinct: Any,
    errors: list[str],
) -> None:
    if not isinstance(counts, dict) or not counts:
        errors.append(f"{where}: partition/subdomain counts missing")
        return
    bad = [
        key
        for key, value in counts.items()
        if not isinstance(key, str)
        or not isinstance(value, int)
        or isinstance(value, bool)
        or value <= 0
    ]
    if bad:
        errors.append(f"{where}: invalid partition count entries: {bad}")
        return
    if isinstance(action_count, int) and sum(counts.values()) != action_count:
        errors.append(
            f"{where}: partition count sum={sum(counts.values())} "
            f"!= action_count={action_count}"
        )
    if distinct != len(counts):
        errors.append(f"{where}: distinct partition count mismatch")


def validate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    seen: set[str] = set()
    by_decision: dict[str, int] = {}

    for idx, row in enumerate(rows):
        where = f"record[{idx}]"
        if row.get("schema") != SCHEMA:
            errors.append(f"{where}: invalid schema")

        decision_id = row.get("decision_id")
        if not isinstance(decision_id, str) or not decision_id:
            errors.append(f"{where}: decision_id missing")
        elif decision_id in seen:
            errors.append(f"{where}: duplicate decision_id {decision_id}")
        else:
            seen.add(decision_id)

        cluster_id = row.get("cluster_id")
        if not isinstance(cluster_id, str) or not cluster_id.startswith("CL-"):
            errors.append(f"{where}: invalid cluster_id")

        if row.get("claim_allowed") is not False:
            errors.append(f"{where}: claim_allowed must remain false")

        decision = row.get("decision")
        if decision not in ALLOWED:
            errors.append(f"{where}: invalid decision {decision!r}")
        else:
            by_decision[decision] = by_decision.get(decision, 0) + 1

        source = row.get("source")
        if not isinstance(source, dict):
            errors.append(f"{where}: source missing")
        else:
            digest = source.get("artifact_digest")
            if (
                not isinstance(digest, str)
                or not digest.startswith("sha256:")
                or len(digest) != 71
            ):
                errors.append(f"{where}: artifact_digest must be sha256:<64 hex>")
            if not isinstance(source.get("workflow_run_id"), int):
                errors.append(f"{where}: workflow_run_id missing")
            if (
                not isinstance(source.get("tested_head"), str)
                or len(source.get("tested_head", "")) != 40
            ):
                errors.append(f"{where}: tested_head must be 40-char SHA")

        observed = row.get("observed")
        if not isinstance(observed, dict):
            errors.append(f"{where}: observed missing")
            continue

        action_count = observed.get("action_count")
        if not isinstance(action_count, int) or isinstance(action_count, bool) or action_count <= 0:
            errors.append(f"{where}: action_count must be > 0")

        g4 = row.get("g4_authority_bind_gate")
        if not isinstance(g4, dict):
            errors.append(f"{where}: g4_authority_bind_gate missing")
            g4 = {}
        if g4.get("auto_create_gap_id") is not False:
            errors.append(f"{where}: auto_create_gap_id must remain false")

        evidence = row.get("evidence_refs", [])
        if decision in {"SAME_FAMILY", "DUPLICATE", "DISTINCT_GAP"}:
            if not isinstance(evidence, list) or not evidence:
                errors.append(f"{where}: {decision} requires evidence_refs")

        if decision == "SPLIT_REQUIRED":
            strategy = row.get("split_strategy", "PATH_SEGMENT")
            if strategy not in SPLIT_STRATEGIES:
                errors.append(f"{where}: invalid split_strategy {strategy!r}")
            counts, distinct = _partition_view(observed)
            _valid_counts(
                where=where,
                action_count=action_count,
                counts=counts,
                distinct=distinct,
                errors=errors,
            )
            if not isinstance(distinct, int) or distinct < 2:
                errors.append(f"{where}: SPLIT_REQUIRED needs >=2 observed partitions")
            if g4.get("state") != "BLOCKED_BY_G3_SPLIT":
                errors.append(f"{where}: SPLIT_REQUIRED must block G4")
            if g4.get("binding") != "TOKEN_VAZIO":
                errors.append(f"{where}: SPLIT_REQUIRED binding must remain TOKEN_VAZIO")
            if not row.get("reason"):
                errors.append(f"{where}: SPLIT_REQUIRED requires reason")

        elif decision == "DISTINCT_GAP":
            if row.get("binding_strategy") != "PER_EXISTING_GAP_ID":
                errors.append(
                    f"{where}: DISTINCT_GAP requires binding_strategy=PER_EXISTING_GAP_ID"
                )
            if g4.get("state") != "REQUIRES_PER_ITEM_BINDING":
                errors.append(f"{where}: DISTINCT_GAP must require per-item G4 binding")
            if g4.get("binding") != "TOKEN_VAZIO":
                errors.append(f"{where}: DISTINCT_GAP Atlas binding must remain TOKEN_VAZIO")
            with_gap_id = observed.get("with_gap_id")
            if with_gap_id != action_count:
                errors.append(
                    f"{where}: DISTINCT_GAP requires with_gap_id == action_count"
                )
            unique_gap_ids = observed.get("unique_gap_ids")
            if not isinstance(unique_gap_ids, int) or unique_gap_ids <= 0:
                errors.append(f"{where}: DISTINCT_GAP unique_gap_ids missing")

        elif decision == "FALSE_POSITIVE":
            if g4.get("state") != "NOT_APPLICABLE_FALSE_POSITIVE":
                errors.append(f"{where}: FALSE_POSITIVE must make G4 not applicable")
            if g4.get("binding") != "TOKEN_VAZIO":
                errors.append(f"{where}: FALSE_POSITIVE binding must remain TOKEN_VAZIO")

        elif decision == "ACCEPTED_LIMITATION":
            if g4.get("state") != "NOT_APPLICABLE_ACCEPTED_LIMITATION":
                errors.append(
                    f"{where}: ACCEPTED_LIMITATION must make G4 not applicable"
                )
            if g4.get("binding") != "TOKEN_VAZIO":
                errors.append(
                    f"{where}: ACCEPTED_LIMITATION binding must remain TOKEN_VAZIO"
                )

    return {
        "schema": "rafaelia.systematic-pragmatic-g3-validation/v1",
        "status": "PASS" if not errors else "FAIL",
        "claim_allowed": False,
        "records": len(rows),
        "by_decision": dict(sorted(by_decision.items())),
        "errors": errors,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("decisions", type=Path)
    ap.add_argument("--write-report", type=Path)
    args = ap.parse_args()

    try:
        rows = load_jsonl(args.decisions)
        report = validate(rows)
    except (OSError, ValueError) as exc:
        report = {
            "schema": "rafaelia.systematic-pragmatic-g3-validation/v1",
            "status": "FAIL",
            "claim_allowed": False,
            "records": 0,
            "by_decision": {},
            "errors": [str(exc)],
        }

    out = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(out, encoding="utf-8")
    else:
        print(out, end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
