#!/usr/bin/env python3
"""Parse one Vectra native core smoke line into fail-closed MetricObservationV1.

This is a HOST smoke pathway. It must never be promoted as an Android/device
benchmark without a separate device-specific execution receipt.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

PATTERN=re.compile(r"benchmark_smoke:\s+iters=(\d+)\s+total_ns=(\d+)\s+avg_ns=([0-9]+(?:\.[0-9]+)?)\s+hash64=(\d+)")


def parse(text):
    matches=list(PATTERN.finditer(text))
    if len(matches)!=1:
        raise ValueError(f"expected exactly one benchmark_smoke line, found {len(matches)}")
    m=matches[0]
    return {"iters":int(m.group(1)),"total_ns":int(m.group(2)),"avg_ns":float(m.group(3)),"hash64":int(m.group(4))}


def observations(parsed, binding, raw_ref, artifact_sha256=None, receipt_ref=None, environment=None):
    workload=binding["workload"]
    if parsed["iters"]!=workload["iterations"]:
        raise ValueError(f"iteration mismatch: log={parsed['iters']} binding={workload['iterations']}")
    evidence={"artifact_sha256":artifact_sha256,"receipt_refs":[receipt_ref] if receipt_ref else [],
              "raw_result_refs":[raw_ref],"digest_verified":None}
    measured=bool((artifact_sha256 or receipt_ref) and environment)
    epi="MEASURED_WITH_RECEIPT" if measured else "HISTORICAL_RUN_OUTPUT"
    state="MEASURED" if measured else "HISTORICAL"
    base={
      "schema":"RAFAELIA_METRIC_OBSERVATION_V1","observed_at":None,"value_state":state,
      "epistemic_class":epi,"statistic":{"kind":"RAW","sample_count":1,"repeats":1,"confidence":None},
      "direction":"LOWER_IS_BETTER","scope":"VECTRA_NATIVE_HOST_CORE_SMOKE_256B",
      "source_refs":[binding["producer"]],"environment":environment or {},"workload":workload,
      "config":{"iterations":parsed["iters"],"payload_bytes":workload["payload_bytes"],"final_hash64":parsed["hash64"]},
      "evidence":evidence,"negative_evidence":False,
      "token_vazio":[] if measured else ["TOKEN_VAZIO_NATIVE_SMOKE_EXECUTION_RECEIPT"],
      "promotion_gate":{"status":"NOT_REQUESTED","reviewer":None,"receipt_ref":None},
      "claim_allowed":False,"notes":"HOST smoke only; not Android/device benchmark.",
      "next_verifiable_step":"Bind binary/source/environment/raw-log hashes and compare repeated runs before any performance claim."
    }
    total=dict(base); total.update({
      "observation_id":"METRIC-VECTRA-HOST-SMOKE-TOTAL-001","metric_name":"HOST_CORE_SMOKE_TOTAL_TIME",
      "category":"TIME","observed_value":parsed["total_ns"],"original_unit":"ns",
      "normalization":{"status":"NORMALIZED","canonical_value":parsed["total_ns"]*1e-9,"canonical_unit":"s","dimension":"time","rule_id":"UNIT_NS_TO_S_V1"}
    })
    avg=dict(base); avg.update({
      "observation_id":"METRIC-VECTRA-HOST-SMOKE-AVG-001","metric_name":"HOST_CORE_SMOKE_AVG_SECTOR_TIME",
      "category":"TIME","observed_value":parsed["avg_ns"],"original_unit":"ns/sector",
      "normalization":{"status":"NORMALIZED","canonical_value":parsed["avg_ns"]*1e-9,"canonical_unit":"s/sector","dimension":"time_per_sector","rule_id":"UNIT_NSSECTOR_TO_SSECTOR_V1"}
    })
    return [total,avg]


def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument("--binding",required=True); ap.add_argument("--input",required=True); ap.add_argument("--output",required=True)
    ap.add_argument("--artifact-sha256"); ap.add_argument("--receipt-ref"); ap.add_argument("--environment-json")
    a=ap.parse_args(argv)
    binding=json.loads(Path(a.binding).read_text(encoding="utf-8"))
    if binding.get("schema")!="RAFAELIA_VECTRA_NATIVE_CORE_SMOKE_BINDING_V1": raise SystemExit("unexpected binding schema")
    parsed=parse(Path(a.input).read_text(encoding="utf-8"))
    env=json.loads(a.environment_json) if a.environment_json else None
    records=observations(parsed,binding,a.input,a.artifact_sha256,a.receipt_ref,env)
    Path(a.output).write_text("\n".join(json.dumps(r,ensure_ascii=False,separators=(",",":")) for r in records)+"\n",encoding="utf-8")
    print(f"PASS records={len(records)} iters={parsed['iters']} output={a.output}")
    return 0

if __name__=="__main__": raise SystemExit(main())
