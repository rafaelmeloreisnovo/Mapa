#!/usr/bin/env python3
"""Validate provider-scope continuity for the JSON totality invariant.

This validates the manifest itself, not the bytes of the Drive objects.
Stdlib only; fail closed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def canonical_sha256(obj):
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def validate_series(name, items, expected_start=1):
    require(isinstance(items, list) and items, f"{name}: empty")
    ords = [x.get("ordinal") for x in items]
    ids = [x.get("drive_id") for x in items]
    require(all(isinstance(o, int) for o in ords), f"{name}: ordinal missing")
    require(len(ords) == len(set(ords)), f"{name}: duplicate ordinal")
    require(len(ids) == len(set(ids)), f"{name}: duplicate provider id")
    require(all(isinstance(i, str) and i for i in ids), f"{name}: provider id missing")
    ordered = sorted(ords)
    require(ordered == list(range(expected_start, max(ordered) + 1)), f"{name}: ordinal gap")
    return {"count": len(items), "first": min(ords), "last": max(ords), "contiguous": True, "unique_provider_ids": True}


def validate(payload):
    require(payload.get("schema") == "rafaelia.json-totality-invariant-scope/v1", "invalid schema")
    require(payload.get("claim_allowed") is False, "claim_allowed must remain false")
    require(payload.get("identity_rule") == "provider_id_plus_parent_id_plus_title; filename_alone_is_not_identity", "identity rule missing")
    scope = payload.get("scope")
    require(isinstance(scope, dict), "scope missing")
    parent = scope.get("primary_derived_parent_id")
    require(isinstance(parent, str) and parent, "primary parent id missing")
    messages = validate_series("MESSAGES", scope.get("observed_primary_message_series"))
    nodes = validate_series("NODES", scope.get("observed_primary_node_series"))
    assets = validate_series("ASSETS", scope.get("observed_primary_asset_series"))
    secondary = scope.get("observed_secondary_duplicate_parent_id")
    require(isinstance(secondary, str) and secondary and secondary != parent, "secondary duplicate parent must be distinct")
    require(scope.get("duplicate_family_state") == "OBSERVED_PARTIAL_DO_NOT_COLLAPSE_BY_FILENAME", "duplicate-family boundary missing")
    return {
        "schema": "rafaelia.json-totality-scope-validation/v1",
        "state": "PASS_SCOPE_STRUCTURE_ONLY",
        "claim_allowed": False,
        "primary_parent_id": parent,
        "secondary_duplicate_parent_id": secondary,
        "series": {"messages": messages, "nodes": nodes, "assets": assets},
        "input_scope_sha256": canonical_sha256(payload),
        "boundary": "provider manifest structure passed; Drive object bytes and complete corpus closure remain outside this receipt"
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scope", type=Path)
    ap.add_argument("--receipt", type=Path)
    ns = ap.parse_args()
    try:
        payload = json.loads(ns.scope.read_text(encoding="utf-8"))
        receipt = validate(payload)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"state": "FAIL", "claim_allowed": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    text = json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if ns.receipt:
        ns.receipt.parent.mkdir(parents=True, exist_ok=True)
        ns.receipt.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
