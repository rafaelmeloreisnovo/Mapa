#!/usr/bin/env python3
"""Validate the atomic repository inventory head over an immutable checkpoint."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from apply_repository_inventory_batch import (
    apply_batch,
    canonical_batch_digest,
    load_json,
)
from validate_repository_inventory import canonical_digest, validate_inventory


def canonical_head_digest(head: dict[str, Any]) -> str:
    clone = copy.deepcopy(head)
    clone.setdefault("integrity", {})["digest"] = ""
    raw = json.dumps(
        clone, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.blake2b(raw, digest_size=32).hexdigest()


def validate_head(root: Path, head: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    required = {
        "schema", "schema_version", "generated_at", "checkpoint",
        "delta_batches", "derived", "integrity",
    }
    missing = sorted(required - set(head))
    if missing:
        return [f"head missing fields: {missing}"], {}

    if head["schema"] != "repository_inventory_head_v1":
        errors.append("head schema must be repository_inventory_head_v1")
    if head["schema_version"] != "1.0.0":
        errors.append("head schema_version must be 1.0.0")

    integrity = head.get("integrity", {})
    if integrity.get("algorithm") != "blake2b-256":
        errors.append("head integrity.algorithm must be blake2b-256")
    if integrity.get("digest") != canonical_head_digest(head):
        errors.append("head integrity.digest mismatch")

    checkpoint_ref = head.get("checkpoint", {})
    checkpoint_path = root / str(checkpoint_ref.get("path", ""))
    try:
        current = load_json(checkpoint_path)
    except Exception as exc:
        return errors + [f"checkpoint load failed: {exc}"], {}

    inventory_errors = validate_inventory(current)
    errors.extend(f"checkpoint: {item}" for item in inventory_errors)
    if len(current.get("repositories", [])) != checkpoint_ref.get("materialized_count"):
        errors.append("checkpoint materialized_count mismatch")
    if canonical_digest(current) != checkpoint_ref.get("digest_blake2b_256"):
        errors.append("checkpoint digest mismatch")

    seen_batch_ids: set[str] = set()
    applications: list[dict[str, Any]] = []
    for index, ref in enumerate(head.get("delta_batches", [])):
        prefix = f"delta_batches[{index}]"
        if not isinstance(ref, dict):
            errors.append(f"{prefix} must be an object")
            continue
        path = root / str(ref.get("path", ""))
        try:
            batch = load_json(path)
        except Exception as exc:
            errors.append(f"{prefix} load failed: {exc}")
            continue
        batch_id = batch.get("batch_id")
        if batch_id in seen_batch_ids:
            errors.append(f"duplicate batch_id in head: {batch_id}")
        seen_batch_ids.add(str(batch_id))
        if batch_id != ref.get("batch_id"):
            errors.append(f"{prefix} batch_id mismatch")
        if canonical_batch_digest(batch) != ref.get("digest_blake2b_256"):
            errors.append(f"{prefix} digest mismatch")
        try:
            current, audit = apply_batch(current, batch)
            applications.append(audit)
        except Exception as exc:
            errors.append(f"{prefix} application failed: {exc}")

    repos = current.get("repositories", [])
    scope = current.get("scope", {})
    stats = current.get("statistics", {})
    ledger = current.get("absence_ledger", {})
    derived_actual = {
        "accessible_total_observed": scope.get("accessible_total_observed"),
        "materialized_count": len(repos),
        "completeness_ratio": scope.get("completeness_ratio"),
        "public_count": stats.get("public_count"),
        "private_count": stats.get("private_count"),
        "archived_count": stats.get("archived_count"),
        "owner_counts": stats.get("owner_counts"),
        "remaining_token_vazio": ledger.get("missing_materialized_records"),
        "inventory_state": scope.get("state"),
        "claim_allowed": scope.get("claim_allowed"),
        "inventory_digest_blake2b_256": current.get("integrity", {}).get("digest"),
    }
    if head.get("derived") != derived_actual:
        errors.append("head derived state mismatch")

    replay_fixed = True
    for ref in head.get("delta_batches", []):
        try:
            batch = load_json(root / ref["path"])
            replayed, audit = apply_batch(current, batch)
            if replayed != current or audit["added_count"] != 0:
                replay_fixed = False
                errors.append(f"{ref['batch_id']}: replay is not a fixed point")
        except Exception as exc:
            replay_fixed = False
            errors.append(f"{ref.get('batch_id')}: replay failed: {exc}")

    report = {
        "schema": "repository_inventory_head_validation_v1",
        "status": "PASS" if not errors else "FAIL",
        "head_digest_blake2b_256": canonical_head_digest(head),
        "checkpoint_materialized_count": checkpoint_ref.get("materialized_count"),
        "delta_batch_count": len(head.get("delta_batches", [])),
        "materialized_count": len(repos),
        "remaining_token_vazio": ledger.get("missing_materialized_records"),
        "inventory_state": scope.get("state", "TOKEN_VAZIO"),
        "claim_allowed": False,
        "all_delta_batches_fixed_points": replay_fixed and not errors,
        "inventory_digest_blake2b_256": current.get("integrity", {}).get(
            "digest", "TOKEN_VAZIO"
        ),
        "applications": applications,
        "errors": errors,
    }
    return errors, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--head", default="indices/REPOSITORY_INVENTORY_HEAD.json"
    )
    parser.add_argument("--write-report", default=None)
    args = parser.parse_args(argv)
    root = Path.cwd()
    try:
        head = load_json(root / args.head)
        errors, report = validate_head(root, head)
    except Exception as exc:
        errors = [f"load_error: {exc}"]
        report = {
            "schema": "repository_inventory_head_validation_v1",
            "status": "FAIL",
            "errors": errors,
        }
    rendered = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.write_report:
        Path(args.write_report).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
