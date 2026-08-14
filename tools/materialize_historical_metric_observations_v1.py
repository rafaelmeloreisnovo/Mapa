#!/usr/bin/env python3
"""Materialize governed MetricObservationV1 records from historical shard seeds.

No benchmark is executed here. Historical values remain HISTORICAL_RUN_OUTPUT and
claim_allowed=false. The tool preserves supersession, negative results, shard
hashes and TOKEN_VAZIO fields.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

UNIT_RULES = {
    "ns": (1e-9, "s", "time", "UNIT_NS_TO_S_V1"),
    "ms": (1e-3, "s", "time", "UNIT_MS_TO_S_V1"),
    "MOPS": (1e6, "ops/s", "operation_rate", "UNIT_MOPS_TO_OPS_V1"),
    "MB/s": (1_000_000.0, "B/s", "byte_bandwidth", "UNIT_MBSI_TO_BPS_V1"),
    "GB/s": (1_000_000_000.0, "B/s", "byte_bandwidth", "UNIT_GBSI_TO_BPS_V1"),
    "ratio": (1.0, "ratio", "ratio", "UNIT_RATIO_IDENTITY_V1"),
}


def normalize(value, unit):
    if unit in UNIT_RULES:
        factor, canonical_unit, dimension, rule_id = UNIT_RULES[unit]
        return {
            "status": "NORMALIZED",
            "canonical_value": value * factor,
            "canonical_unit": canonical_unit,
            "dimension": dimension,
            "rule_id": rule_id,
        }
    return {
        "status": "PRESERVED_SEMANTIC",
        "canonical_value": value,
        "canonical_unit": unit,
        "dimension": "source_semantic",
        "rule_id": "PRESERVE_SOURCE_SEMANTIC_V1",
    }


def metric_id(run_id, symbol):
    return "METRIC-" + run_id.replace("HIST-", "") + "-" + symbol


def materialize(seed):
    out = []
    sources = seed["sources"]
    for run in seed["runs"]:
        src = sources[run["source"]]
        source_ref = {
            "provider_id": src["provider_id"],
            "file": f"conversations-{run['source']}.json",
            "conversation_id": run["conversation_id"],
        }
        if run.get("message_id"):
            source_ref["message_id"] = run["message_id"]
        supersession = run.get("supersession", {})
        run_open = list(run.get("open_tokens", []))
        for symbol, value, unit, category in run["metrics"]:
            oid = metric_id(run["run_id"], symbol)
            token_vazio = ["TOKEN_VAZIO_HISTORICAL_RAW_LOG_HASH_PER_MVP"] + run_open
            notes = run.get("notes", "")
            negative = symbol.startswith("UNROLL4") or symbol.startswith("UNROLL8")
            record = {
                "schema": "RAFAELIA_METRIC_OBSERVATION_V1",
                "observation_id": oid,
                "metric_name": f"{run['run_id']} {symbol}",
                "category": category,
                "value_state": "HISTORICAL",
                "epistemic_class": "HISTORICAL_RUN_OUTPUT",
                "observed_value": value,
                "original_unit": unit,
                "normalization": normalize(value, unit),
                "scope": f"historical shard {run['source']} / {run['run_id']}",
                "source_refs": [source_ref],
                "config": run.get("config", {}),
                "evidence": {
                    "artifact_sha256": src["sha256"],
                    "receipt_refs": [],
                    "raw_result_refs": [src["provider_id"], run["conversation_id"]] + ([run["message_id"]] if run.get("message_id") else []),
                    "digest_verified": True,
                },
                "negative_evidence": negative,
                "token_vazio": token_vazio,
                "promotion_gate": {"status": "BLOCKED", "reviewer": None, "receipt_ref": None},
                "claim_allowed": False,
                "notes": notes,
                "next_verifiable_step": "Bind exact historical raw-log/message bytes and replay this workload in a pinned current environment before promotion.",
            }
            if symbol in supersession:
                record["supersedes"] = [metric_id(run["run_id"], supersession[symbol])]
            out.append(record)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seed", nargs="?", default="data/benchmarks/historical-metric-seeds-046-047.v1.json")
    ap.add_argument("-o", "--output", default="data/benchmarks/metric-observation-v1.historical-046-047.json")
    args = ap.parse_args()
    seed = json.loads(Path(args.seed).read_text(encoding="utf-8"))
    records = materialize(seed)
    ids = [r["observation_id"] for r in records]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate observation_id")
    Path(args.output).write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS records={len(records)} output={args.output}")


if __name__ == "__main__":
    main()
