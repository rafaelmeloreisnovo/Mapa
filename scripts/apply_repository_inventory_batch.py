#!/usr/bin/env python3
"""Deterministically apply a connector-backed repository inventory batch."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from validate_repository_inventory import (
    ALLOWED_OWNERS,
    REQUIRED_REPO_FIELDS,
    canonical_digest,
    validate_inventory,
)

HEX64 = set("0123456789abcdef")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be an object")
    return data


def canonical_batch_digest(batch: dict[str, Any]) -> str:
    clone = copy.deepcopy(batch)
    clone.setdefault("integrity", {})["digest"] = ""
    raw = json.dumps(
        clone, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.blake2b(raw, digest_size=32).hexdigest()


def validate_batch(batch: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "schema", "schema_version", "batch_id", "observed_at", "source",
        "record_count", "owner_counts", "records", "integrity",
    }
    missing = sorted(required - set(batch))
    if missing:
        return [f"batch missing top-level fields: {missing}"]
    if batch["schema"] != "repository_inventory_batch_v1":
        errors.append("batch schema must be repository_inventory_batch_v1")
    if batch["schema_version"] != "1.0.0":
        errors.append("batch schema_version must be 1.0.0")
    if batch["source"] != "github_connector.get_repo":
        errors.append("batch source must be github_connector.get_repo")
    if not isinstance(batch["batch_id"], str) or not batch["batch_id"].strip():
        errors.append("batch_id must be a non-empty string")
    if not isinstance(batch["observed_at"], str) or not batch["observed_at"].endswith("Z"):
        errors.append("observed_at must be an explicit UTC timestamp ending in Z")

    records = batch["records"]
    if not isinstance(records, list):
        return errors + ["batch records must be a list"]
    if batch["record_count"] != len(records):
        errors.append("batch record_count mismatch")

    ids: set[int] = set()
    names: set[str] = set()
    derived_owner_counts = {owner: 0 for owner in sorted(ALLOWED_OWNERS)}
    for index, record in enumerate(records):
        prefix = f"records[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing_fields = sorted(REQUIRED_REPO_FIELDS - set(record))
        if missing_fields:
            errors.append(f"{prefix} missing fields: {missing_fields}")
            continue
        full_name = record["repository_full_name"]
        repository_id = record["repository_id"]
        owner = record["owner"]
        name = record["repository_name"]
        if owner not in ALLOWED_OWNERS:
            errors.append(f"{prefix}.owner not allowed")
        else:
            derived_owner_counts[owner] += 1
        if full_name != f"{owner}/{name}":
            errors.append(f"{prefix}.repository_full_name does not match owner/name")
        if record["clone_url"] != f"https://github.com/{full_name}.git":
            errors.append(f"{prefix}.clone_url is not canonical")
        if not isinstance(repository_id, int) or isinstance(repository_id, bool) or repository_id <= 0:
            errors.append(f"{prefix}.repository_id must be a positive integer")
        elif repository_id in ids:
            errors.append(f"duplicate batch repository_id: {repository_id}")
        ids.add(repository_id)
        if full_name in names:
            errors.append(f"duplicate batch repository_full_name: {full_name}")
        names.add(full_name)
        if record["visibility"] not in {"public", "private"}:
            errors.append(f"{prefix}.visibility invalid")
        if not isinstance(record["archived"], bool):
            errors.append(f"{prefix}.archived must be boolean")
        if not isinstance(record["size_kib"], int) or isinstance(record["size_kib"], bool) or record["size_kib"] < 0:
            errors.append(f"{prefix}.size_kib must be a non-negative integer")
        if record["metadata_status"] != "FATO":
            errors.append(f"{prefix}.metadata_status must be FATO")
        if record["claim_scope"] != "repository_identity_and_connector_metadata_only":
            errors.append(f"{prefix}.claim_scope invalid")
        if record["observed_via"] != "github_connector.get_repo":
            errors.append(f"{prefix}.observed_via invalid")

    if batch["owner_counts"] != derived_owner_counts:
        errors.append(
            f"batch owner_counts mismatch: declared={batch['owner_counts']!r} "
            f"derived={derived_owner_counts!r}"
        )
    integrity = batch["integrity"]
    digest = integrity.get("digest", "") if isinstance(integrity, dict) else ""
    if not isinstance(integrity, dict) or integrity.get("algorithm") != "blake2b-256":
        errors.append("batch integrity.algorithm must be blake2b-256")
    if not isinstance(digest, str) or len(digest) != 64 or any(ch not in HEX64 for ch in digest):
        errors.append("batch integrity.digest must be 64 lowercase hex chars")
    elif digest != canonical_batch_digest(batch):
        errors.append("batch integrity.digest mismatch")
    return errors


def recalculate_inventory(data: dict[str, Any], observed_at: str) -> dict[str, Any]:
    result = copy.deepcopy(data)
    repos = sorted(
        result["repositories"],
        key=lambda item: item["repository_full_name"].casefold(),
    )
    result["repositories"] = repos
    total = result["scope"]["accessible_total_observed"]
    materialized = len(repos)
    result["generated_at"] = observed_at
    result["scope"]["materialized_count"] = materialized
    result["scope"]["completeness_ratio"] = round(materialized / total, 12) if total else 0.0
    result["scope"]["state"] = "PARTIAL"
    result["scope"]["claim_allowed"] = False
    result["statistics"] = {
        "materialized_count": materialized,
        "public_count": sum(repo["visibility"] == "public" for repo in repos),
        "private_count": sum(repo["visibility"] == "private" for repo in repos),
        "archived_count": sum(repo["archived"] is True for repo in repos),
        "owner_counts": {
            owner: sum(repo["owner"] == owner for repo in repos)
            for owner in sorted(ALLOWED_OWNERS)
        },
    }
    missing = total - materialized
    result["absence_ledger"]["state"] = "TOKEN_VAZIO"
    result["absence_ledger"]["missing_materialized_records"] = missing
    result["absence_ledger"]["reason"] = (
        "Connector-backed materialization is incremental. "
        "Unmaterialized records are not promoted without direct evidence."
    )
    result["absence_ledger"]["next_action"] = (
        "Apply the next connector-backed batch through "
        "scripts/apply_repository_inventory_batch.py."
    )
    result["integrity"]["digest"] = ""
    result["integrity"]["digest"] = canonical_digest(result)
    return result


def apply_batch(
    inventory: dict[str, Any], batch: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    inventory_errors = validate_inventory(inventory)
    batch_errors = validate_batch(batch)
    if inventory_errors or batch_errors:
        raise ValueError(
            json.dumps(
                {"inventory_errors": inventory_errors, "batch_errors": batch_errors},
                ensure_ascii=False,
                sort_keys=True,
            )
        )

    by_name = {repo["repository_full_name"]: repo for repo in inventory["repositories"]}
    by_id = {repo["repository_id"]: repo for repo in inventory["repositories"]}
    added: list[str] = []
    skipped: list[str] = []

    output = copy.deepcopy(inventory)
    for record in batch["records"]:
        full_name = record["repository_full_name"]
        repository_id = record["repository_id"]
        existing_by_name = by_name.get(full_name)
        existing_by_id = by_id.get(repository_id)
        if existing_by_name is not None:
            if existing_by_name != record:
                raise ValueError(f"name collision with divergent evidence: {full_name}")
            skipped.append(full_name)
            continue
        if existing_by_id is not None:
            raise ValueError(
                "repository_id collision: "
                f"{repository_id} maps to {existing_by_id['repository_full_name']} "
                f"and {full_name}"
            )
        output["repositories"].append(copy.deepcopy(record))
        by_name[full_name] = record
        by_id[repository_id] = record
        added.append(full_name)

    output = recalculate_inventory(output, batch["observed_at"])
    output_errors = validate_inventory(output)
    if output_errors:
        raise ValueError(json.dumps({"output_errors": output_errors}, ensure_ascii=False))

    audit = {
        "schema": "repository_inventory_batch_application_v1",
        "batch_id": batch["batch_id"],
        "batch_digest_blake2b_256": batch["integrity"]["digest"],
        "before_materialized_count": len(inventory["repositories"]),
        "after_materialized_count": len(output["repositories"]),
        "accessible_total_observed": output["scope"]["accessible_total_observed"],
        "remaining_token_vazio": output["absence_ledger"]["missing_materialized_records"],
        "added_count": len(added),
        "skipped_idempotent_count": len(skipped),
        "added": sorted(added, key=str.casefold),
        "skipped_idempotent": sorted(skipped, key=str.casefold),
        "inventory_state": output["scope"]["state"],
        "claim_allowed": output["scope"]["claim_allowed"],
        "output_digest_blake2b_256": output["integrity"]["digest"],
        "status": "PASS",
    }
    return output, audit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", default="indices/REPOSITORY_INVENTORY.json")
    parser.add_argument("--batch", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--write-audit", required=True)
    args = parser.parse_args(argv)
    try:
        inventory = load_json(Path(args.inventory))
        batch = load_json(Path(args.batch))
        output, audit = apply_batch(inventory, batch)
        Path(args.output).write_text(
            json.dumps(output, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        Path(args.write_audit).write_text(
            json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
