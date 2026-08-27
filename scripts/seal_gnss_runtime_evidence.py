#!/usr/bin/env python3
"""Seal one GNSS_RUNTIME_RECEIPT_V1 into an append-only evidence-closure record.

This tool is intentionally narrower than a claim promoter. It validates the raw
GNSS receipt, hashes its exact bytes, pins the producer commit, and emits an
`evidence-closure-record.v1` JSONL record with `status=EVIDENCED` and
`claim_allowed=false`.

It does NOT infer network transfer, model-context access, legal compliance,
reproducibility, or a general device capability from one physical observation.
Stdlib only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

from validate_gnss_runtime_receipt import ContractError, load_json, validate as validate_gnss

HEX40 = re.compile(r"^[0-9a-fA-F]{40}$")


def sha256_bytes(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def build_record(receipt_path: Path, producer_repo: str, producer_commit: str) -> dict:
    if not HEX40.fullmatch(producer_commit):
        raise ContractError("producer_commit must be exactly 40 hexadecimal characters")
    if not producer_repo.strip():
        raise ContractError("producer_repo must be non-empty")

    receipt = load_json(receipt_path)
    summary = validate_gnss(receipt)
    digest = sha256_bytes(receipt_path)
    receipt_id = str(summary["receipt_id"])
    observed_at = str(receipt["recorded_at"])

    # One successful physical receipt is evidence, not closure of the full chain.
    # BUILD/CI remain OBSERVED_LIMITED here because this local sealer cannot
    # independently query GitHub Actions. REPRODUCIBILITY remains TOKEN_VAZIO
    # until a second compatible execution exists.
    return {
        "schema_version": "evidence-closure-record.v1",
        "closure_id": f"GNSS-RUNTIME-{receipt_id}",
        "revision": 0,
        "status": "EVIDENCED",
        "claim_allowed": False,
        "scope": "authorized minimized Android GNSS runtime observation",
        "owner": "RAFAELIA legal-gnss control-plane",
        "tags": ["GNSS", "ANDROID", "PRIVACY", "PROVENANCE", "F_NEXT"],
        "required_axes": ["RUNTIME", "DEVICE", "PROVENANCE"],
        "evidence_vector": {
            "CODE": "OBSERVED_LIMITED",
            "BUILD": "OBSERVED_LIMITED",
            "RUNTIME": "OBSERVED",
            "TEST": "PASS",
            "CI": "OBSERVED_LIMITED",
            "DEVICE": "OBSERVED",
            "SECURITY": "OBSERVED_LIMITED",
            "PROVENANCE": "PASS",
            "REPRODUCIBILITY": "TOKEN_VAZIO",
        },
        "uncertainty": {
            "class": "BOUNDED",
            "reasons": [
                "one physical runtime observation does not prove reproducibility",
                "network and assistant/model context boundaries remain outside this receipt",
                "build/CI identity requires independent build receipt binding",
            ],
        },
        "problem": "physical GNSS observation requires byte-level provenance without over-promoting downstream claims",
        "risk": "a local observation could be mistaken for general GNSS capability, network transfer, model-context access, or legal compliance",
        "next_probe": "bind this byte-hashed receipt to the exact verified APK/build artifact, then test each remaining service/tool/assistant/model boundary independently",
        "closure_rule": "full closure requires independently evidenced required boundaries plus reproducibility; this seal alone remains EVIDENCED",
        "falsifier": "receipt bytes fail GNSS_RUNTIME_RECEIPT_V1 validation, producer commit is unpinned, digest changes, or downstream claims exceed observed boundaries",
        "provenance": [
            {
                "kind": "receipt",
                "locator": receipt_path.name,
                "authority": "BYTE_HASHED",
                "sha256": digest,
            },
            {
                "kind": "github",
                "locator": producer_repo,
                "authority": "COMMIT_PINNED",
                "commit_sha": producer_commit.lower(),
            },
        ],
        "receipts": [
            {
                "locator": receipt_path.name,
                "sha256": digest,
                "producer": producer_repo,
                "observed_at": observed_at,
            }
        ],
        "dependencies": [
            {
                "closure_id": "FN-GNSS-001",
                "state": "CLOSED_PASS",
                "locator": "data/control-plane/legal-gnss/F_NEXT_CONTINUOUS_EVOLUTION_20260826.v1.json",
            }
        ],
        "contradictions": [],
        "previous_record_sha256": None,
        "transition_reason": "physical receipt validated and exact receipt bytes hash-sealed; claim promotion remains blocked pending downstream evidence",
        "observed_at": observed_at,
    }


def _fixture() -> dict:
    gates = [
        "HARDWARE_TO_ANDROID",
        "ANDROID_TO_APP",
        "APP_TO_SERVICE",
        "SERVICE_TO_TOOL",
        "TOOL_TO_ASSISTANT_CONTEXT",
        "ASSISTANT_CONTEXT_TO_MODEL",
        "APP_TO_THIRD_PARTY",
    ]
    return {
        "schema_version": "GNSS_RUNTIME_RECEIPT_V1",
        "receipt_id": "SELFTEST-GNSS-001",
        "recorded_at": "2026-08-26T21:00:00-03:00",
        "scope": {
            "purpose": "self-test only",
            "product_or_app": "fixture",
            "jurisdiction": "Brazil",
            "authorized_test": True,
        },
        "device_context": {
            "android_version": "fixture",
            "hardware_model_state": "REDACTED",
            "location_services_enabled": True,
        },
        "permission_state": {
            "coarse_location": "GRANTED",
            "fine_location": "GRANTED",
            "precise_location_toggle": "ENABLED",
        },
        "path_gates": [
            {"gate": g, "state": "TOKEN_VAZIO", "evidence_ref": "self-test"}
            for g in gates
        ],
        "field_observations": [
            {
                "field": "latitude",
                "state": "REDACTED",
                "source_boundary": "ANDROID_TO_APP",
                "value_retained": False,
            }
        ],
        "privacy_controls": {
            "minimized_scope": True,
            "unrelated_personal_data_excluded": True,
            "precise_coordinates_retention": "REDACTED",
            "redaction_applied": True,
        },
        "evidence": {
            "runtime_receipt_ref": "self-test",
            "hash_state": "TOKEN_VAZIO",
            "provenance_state": "TOKEN_VAZIO",
        },
        "claim_allowed": False,
        "F_ok": [],
        "F_gap": ["fixture"],
        "F_next": "seal fixture",
    }


def self_test() -> dict:
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "fixture.json"
        path.write_text(json.dumps(_fixture(), sort_keys=True), encoding="utf-8")
        rec = build_record(path, "rafaelmeloreisnovo/termux-api_rafcodephi", "0" * 40)
        if rec["status"] != "EVIDENCED" or rec["claim_allowed"] is not False:
            raise ContractError("self-test promotion boundary failed")
        if rec["evidence_vector"]["REPRODUCIBILITY"] != "TOKEN_VAZIO":
            raise ContractError("self-test must preserve reproducibility TOKEN_VAZIO")
        if rec["provenance"][0]["sha256"] != sha256_bytes(path):
            raise ContractError("self-test digest mismatch")

        rejected = 0
        for bad_commit in ("", "abc", "g" * 40, "0" * 39):
            try:
                build_record(path, "rafaelmeloreisnovo/termux-api_rafcodephi", bad_commit)
            except ContractError:
                rejected += 1
        if rejected != 4:
            raise ContractError(f"self-test rejected {rejected}/4 malformed producer commits")
        return {"positive": 1, "negative_rejected": rejected}


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("receipt", nargs="?", type=Path)
    p.add_argument("--producer-repo", default="rafaelmeloreisnovo/termux-api_rafcodephi")
    p.add_argument("--producer-commit")
    p.add_argument("--output", type=Path)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    try:
        result = {}
        if args.self_test:
            result["self_test"] = self_test()
        if args.receipt:
            if not args.producer_commit:
                raise ContractError("--producer-commit is required with a receipt")
            record = build_record(args.receipt, args.producer_repo, args.producer_commit)
            line = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(line, encoding="utf-8")
                result["output"] = str(args.output)
            else:
                sys.stdout.write(line)
                return 0
        if result:
            print(json.dumps({"status": "PASS", **result}, sort_keys=True))
            return 0
        raise ContractError("provide a receipt and/or --self-test")
    except ContractError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc), "claim_allowed": False}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
