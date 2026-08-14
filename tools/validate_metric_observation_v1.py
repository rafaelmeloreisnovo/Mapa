#!/usr/bin/env python3
"""Validate and normalize RAFAELIA MetricObservationV1 without external deps.

Exit 0 only when every observation passes fail-closed checks.
This validator deliberately keeps semantic units such as IOPS distinct from generic ops/s.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

SCHEMA = "RAFAELIA_METRIC_OBSERVATION_V1"

UNIT_RULES = {
    "ns": (1e-9, "s", "time", "UNIT_NS_TO_S_V1"),
    "us": (1e-6, "s", "time", "UNIT_US_TO_S_V1"),
    "µs": (1e-6, "s", "time", "UNIT_US_TO_S_V1"),
    "ms": (1e-3, "s", "time", "UNIT_MS_TO_S_V1"),
    "s": (1.0, "s", "time", "UNIT_S_IDENTITY_V1"),
    "ns/op": (1e-9, "s/op", "time_per_operation", "UNIT_NSOP_TO_SOP_V1"),
    "ns/sector": (1e-9, "s/sector", "time_per_sector", "UNIT_NSSECTOR_TO_SSECTOR_V1"),
    "ops/s": (1.0, "ops/s", "operation_rate", "UNIT_OPS_IDENTITY_V1"),
    "MOPS": (1e6, "ops/s", "operation_rate", "UNIT_MOPS_TO_OPS_V1"),
    "GOPS": (1e9, "ops/s", "operation_rate", "UNIT_GOPS_TO_OPS_V1"),
    "sectors/s": (1.0, "sectors/s", "sector_rate", "UNIT_SECTORS_IDENTITY_V1"),
    "chunks/s": (1.0, "chunks/s", "chunk_rate", "UNIT_CHUNKS_IDENTITY_V1"),
    "files/s": (1.0, "files/s", "file_rate", "UNIT_FILES_IDENTITY_V1"),
    "audits/s": (1.0, "audits/s", "audit_rate", "UNIT_AUDITS_IDENTITY_V1"),
    "IOPS": (1.0, "IOPS", "io_operation_rate", "UNIT_IOPS_SEMANTIC_V1"),
    "MB/s": (1_000_000.0, "B/s", "byte_bandwidth", "UNIT_MBSI_TO_BPS_V1"),
    "MiB/s": (1_048_576.0, "B/s", "byte_bandwidth", "UNIT_MIBS_TO_BPS_V1"),
    "GB/s": (1_000_000_000.0, "B/s", "byte_bandwidth", "UNIT_GBSI_TO_BPS_V1"),
    "Mbps": (1_000_000.0, "bit/s", "bit_rate", "UNIT_MBPS_TO_BITPS_V1"),
    "Gbps": (1_000_000_000.0, "bit/s", "bit_rate", "UNIT_GBPS_TO_BITPS_V1"),
    "GFLOPS": (1e9, "FLOP/s", "floating_point_rate", "UNIT_GFLOPS_TO_FLOPS_V1"),
    "cycles": (1.0, "cycles", "cycle_count", "UNIT_CYCLES_IDENTITY_V1"),
    "cycles/op": (1.0, "cycles/op", "cycles_per_operation", "UNIT_CYCLESOP_IDENTITY_V1"),
    "bytes": (1.0, "B", "size", "UNIT_BYTES_IDENTITY_V1"),
    "KiB": (1024.0, "B", "size", "UNIT_KIB_TO_B_V1"),
    "MiB": (1048576.0, "B", "size", "UNIT_MIB_TO_B_V1"),
    "GiB": (1073741824.0, "B", "size", "UNIT_GIB_TO_B_V1"),
    "percent": (0.01, "ratio", "ratio", "UNIT_PERCENT_TO_RATIO_V1"),
    "ratio": (1.0, "ratio", "ratio", "UNIT_RATIO_IDENTITY_V1"),
}

NON_PROMOTABLE = {
    "HISTORICAL_RUN_OUTPUT",
    "MEASUREMENT_PATH_IMPLEMENTED",
    "DOCUMENTED_BENCHMARK_UNBOUND",
    "ESTIMATE_CODE_ANALYSIS",
    "EXPECTED_REFERENCE_RANGE",
    "OPERATIONAL_THRESHOLD",
    "TOKEN_VAZIO",
}

REQUIRED = {
    "schema", "observation_id", "metric_name", "category", "value_state",
    "epistemic_class", "observed_value", "original_unit", "normalization",
    "scope", "source_refs", "evidence", "claim_allowed", "next_verifiable_step",
}


def expected_normalization(value, unit):
    if value is None:
        return None
    if unit not in UNIT_RULES:
        return None
    factor, canonical_unit, dimension, rule_id = UNIT_RULES[unit]
    return {
        "status": "PRESERVED_SEMANTIC" if unit == "IOPS" else "NORMALIZED",
        "canonical_value": value * factor,
        "canonical_unit": canonical_unit,
        "dimension": dimension,
        "rule_id": rule_id,
    }


def close_enough(a, b):
    if a is None or b is None:
        return a is b
    return math.isclose(float(a), float(b), rel_tol=1e-12, abs_tol=1e-15)


def has_measurement_evidence(evidence):
    if not isinstance(evidence, dict):
        return False
    if evidence.get("artifact_sha256"):
        return True
    if evidence.get("receipt_refs"):
        return True
    if evidence.get("raw_result_refs"):
        return True
    return False


def validate(obj):
    errors = []
    if not isinstance(obj, dict):
        return ["observation must be an object"]

    missing = sorted(REQUIRED - set(obj))
    if missing:
        errors.append("missing required: " + ", ".join(missing))
        return errors

    if obj["schema"] != SCHEMA:
        errors.append(f"schema must be {SCHEMA}")

    if not isinstance(obj["source_refs"], list) or not obj["source_refs"]:
        errors.append("source_refs must contain at least one source")

    if not isinstance(obj["claim_allowed"], bool):
        errors.append("claim_allowed must be boolean")

    value = obj["observed_value"]
    unit = obj["original_unit"]
    epi = obj["epistemic_class"]
    state = obj["value_state"]
    norm = obj["normalization"]

    if state == "TOKEN_VAZIO":
        if value is not None:
            errors.append("TOKEN_VAZIO requires observed_value=null")
        if obj["claim_allowed"]:
            errors.append("TOKEN_VAZIO requires claim_allowed=false")
        if norm.get("status") != "TOKEN_VAZIO" or norm.get("canonical_value") is not None:
            errors.append("TOKEN_VAZIO requires empty normalization")
        return errors

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        errors.append("observed_value must be numeric outside TOKEN_VAZIO")
    elif not math.isfinite(float(value)):
        errors.append("observed_value must be finite")

    expected = expected_normalization(value, unit)
    if expected is None:
        if norm.get("status") not in {"PRESERVED_SEMANTIC", "TOKEN_VAZIO"}:
            errors.append(f"unknown unit {unit!r} must be explicitly preserved or TOKEN_VAZIO")
    else:
        for key in ("status", "canonical_unit", "dimension", "rule_id"):
            if norm.get(key) != expected[key]:
                errors.append(f"normalization.{key}: expected {expected[key]!r}, got {norm.get(key)!r}")
        if not close_enough(norm.get("canonical_value"), expected["canonical_value"]):
            errors.append(
                f"normalization.canonical_value: expected {expected['canonical_value']!r}, got {norm.get('canonical_value')!r}"
            )

    if epi in NON_PROMOTABLE and obj["claim_allowed"]:
        errors.append(f"{epi} is fail-closed: claim_allowed must be false")

    if epi == "MEASURED_WITH_RECEIPT":
        if not has_measurement_evidence(obj["evidence"]):
            errors.append("MEASURED_WITH_RECEIPT requires artifact hash, receipt ref, or raw result ref")
        if not obj.get("environment"):
            errors.append("MEASURED_WITH_RECEIPT requires non-empty environment")
        if not obj.get("workload"):
            errors.append("MEASURED_WITH_RECEIPT requires non-empty workload")

    if obj["claim_allowed"]:
        gate = obj.get("promotion_gate") or {}
        if epi != "MEASURED_WITH_RECEIPT":
            errors.append("claim promotion only permitted from MEASURED_WITH_RECEIPT")
        if gate.get("status") != "APPROVED" or not gate.get("receipt_ref"):
            errors.append("claim_allowed=true requires APPROVED promotion_gate with receipt_ref")

    return errors


def load_records(path):
    text = Path(path).read_text(encoding="utf-8")
    stripped = text.lstrip()
    if stripped.startswith("["):
        data = json.loads(text)
        if not isinstance(data, list):
            raise ValueError("JSON root must be array or object")
        return data
    if stripped.startswith("{"):
        try:
            data = json.loads(text)
            return [data]
        except json.JSONDecodeError:
            pass
    records = []
    for line_no, line in enumerate(text.splitlines(), 1):
        if line.strip():
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"JSONL line {line_no}: {exc}") from exc
    return records


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    args = ap.parse_args(argv)
    failures = 0
    total = 0
    for path in args.paths:
        try:
            records = load_records(path)
        except Exception as exc:
            print(f"FAIL {path}: {exc}")
            failures += 1
            continue
        for idx, obj in enumerate(records):
            total += 1
            errs = validate(obj)
            oid = obj.get("observation_id", f"index={idx}") if isinstance(obj, dict) else f"index={idx}"
            if errs:
                failures += 1
                print(f"FAIL {path}::{oid}")
                for err in errs:
                    print(f"  - {err}")
            else:
                print(f"PASS {path}::{oid}")
    print(f"SUMMARY total={total} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
