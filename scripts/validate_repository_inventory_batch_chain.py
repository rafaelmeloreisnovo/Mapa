#!/usr/bin/env python3
"""Validate committed inventory batches as immutable fixed-point evidence."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from apply_repository_inventory_batch import apply_batch, load_json, validate_batch
from validate_repository_inventory import validate_inventory


def validate_batch_chain(
    inventory: dict[str, Any],
    batches: list[tuple[Path, dict[str, Any]]],
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    inventory_errors = validate_inventory(inventory)
    errors.extend(f"inventory: {error}" for error in inventory_errors)

    inventory_by_name = {
        record["repository_full_name"]: record
        for record in inventory.get("repositories", [])
        if isinstance(record, dict) and "repository_full_name" in record
    }
    inventory_by_id = {
        record["repository_id"]: record
        for record in inventory.get("repositories", [])
        if isinstance(record, dict) and "repository_id" in record
    }

    seen_batch_ids: set[str] = set()
    seen_names: dict[str, str] = {}
    seen_ids: dict[int, str] = {}
    batch_ids: list[str] = []
    observed_times: list[str] = []
    total_batch_records = 0
    fixed_points = True

    if not batches:
        errors.append("no inventory batches found")

    for path, batch in batches:
        prefix = str(path)
        batch_errors = validate_batch(batch)
        errors.extend(f"{prefix}: {error}" for error in batch_errors)
        batch_id = batch.get("batch_id", "TOKEN_VAZIO")
        if batch_id in seen_batch_ids:
            errors.append(f"duplicate batch_id: {batch_id}")
        seen_batch_ids.add(batch_id)
        batch_ids.append(batch_id)
        observed_times.append(str(batch.get("observed_at", "TOKEN_VAZIO")))

        records = batch.get("records", [])
        if not isinstance(records, list):
            continue
        total_batch_records += len(records)
        for record in records:
            if not isinstance(record, dict):
                continue
            full_name = record.get("repository_full_name")
            repository_id = record.get("repository_id")
            if full_name in seen_names:
                errors.append(
                    f"repository repeated across batches: {full_name} "
                    f"({seen_names[full_name]} and {batch_id})"
                )
            else:
                seen_names[full_name] = batch_id
            if repository_id in seen_ids:
                errors.append(
                    f"repository_id repeated across batches: {repository_id} "
                    f"({seen_ids[repository_id]} and {batch_id})"
                )
            else:
                seen_ids[repository_id] = batch_id

            current_by_name = inventory_by_name.get(full_name)
            current_by_id = inventory_by_id.get(repository_id)
            if current_by_name is None:
                errors.append(f"{batch_id}: inventory missing {full_name}")
            elif current_by_name != record:
                errors.append(f"{batch_id}: divergent inventory evidence for {full_name}")
            if current_by_id is None:
                errors.append(f"{batch_id}: inventory missing repository_id {repository_id}")
            elif current_by_id.get("repository_full_name") != full_name:
                errors.append(
                    f"{batch_id}: repository_id {repository_id} maps to "
                    f"{current_by_id.get('repository_full_name')} instead of {full_name}"
                )

        if not batch_errors and not inventory_errors:
            try:
                replayed, audit = apply_batch(inventory, batch)
                if replayed != inventory:
                    fixed_points = False
                    errors.append(f"{batch_id}: replay changed canonical inventory")
                if audit["added_count"] != 0:
                    fixed_points = False
                    errors.append(f"{batch_id}: replay unexpectedly added records")
                if audit["skipped_idempotent_count"] != len(records):
                    fixed_points = False
                    errors.append(f"{batch_id}: idempotent skip count mismatch")
            except Exception as exc:
                fixed_points = False
                errors.append(f"{batch_id}: replay failure: {exc}")

    if observed_times != sorted(observed_times):
        errors.append("batch observed_at timestamps are not monotonic in filename order")

    materialized = len(inventory.get("repositories", []))
    baseline_unbatched = materialized - total_batch_records
    if baseline_unbatched < 0:
        errors.append("batch records exceed materialized inventory count")

    report = {
        "schema": "repository_inventory_batch_chain_report_v1",
        "status": "PASS" if not errors else "FAIL",
        "inventory_state": inventory.get("scope", {}).get("state", "TOKEN_VAZIO"),
        "claim_allowed": False,
        "materialized_count": materialized,
        "batch_count": len(batches),
        "batch_ids": batch_ids,
        "total_batch_records": total_batch_records,
        "baseline_unbatched_records": baseline_unbatched,
        "all_batches_fixed_points": fixed_points and not errors,
        "inventory_digest_blake2b_256": inventory.get("integrity", {}).get(
            "digest", "TOKEN_VAZIO"
        ),
        "errors": errors,
    }
    return errors, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", default="indices/REPOSITORY_INVENTORY.json")
    parser.add_argument("--batches-dir", default="indices/inventory_batches")
    parser.add_argument("--write-report", default=None)
    args = parser.parse_args(argv)

    try:
        inventory = load_json(Path(args.inventory))
        batch_paths = sorted(Path(args.batches_dir).glob("*.json"))
        batches = [(path, load_json(path)) for path in batch_paths]
        errors, report = validate_batch_chain(inventory, batches)
    except Exception as exc:
        errors = [f"load_error: {exc}"]
        report = {
            "schema": "repository_inventory_batch_chain_report_v1",
            "status": "FAIL",
            "inventory_state": "TOKEN_VAZIO",
            "claim_allowed": False,
            "materialized_count": "TOKEN_VAZIO",
            "batch_count": "TOKEN_VAZIO",
            "batch_ids": [],
            "total_batch_records": "TOKEN_VAZIO",
            "baseline_unbatched_records": "TOKEN_VAZIO",
            "all_batches_fixed_points": False,
            "inventory_digest_blake2b_256": "TOKEN_VAZIO",
            "errors": errors,
        }

    rendered = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.write_report:
        Path(args.write_report).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
