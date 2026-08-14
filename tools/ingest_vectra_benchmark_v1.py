#!/usr/bin/env python3
"""Convert VectraBenchmark audit JSONL/CSV output to RAFAELIA MetricObservationV1.

Fail-closed rules:
- metric_id must exist in binding;
- run context must precede metric lines for JSONL;
- formatted unit and declared unit are both preserved;
- IOPS semantics are restored from binding even when formatter emits generic ops/s;
- proxies/simulations remain notes and claim_allowed=false;
- no record is promoted automatically.
"""
from __future__ import annotations
import argparse, csv, json, math, re
from pathlib import Path

SCHEMA="RAFAELIA_METRIC_OBSERVATION_V1"
RATE={"ops/s":1.0,"Kops/s":1e3,"Mops/s":1e6,"Gops/s":1e9}
TIME={"ns":1e-9,"μs":1e-6,"µs":1e-6,"us":1e-6,"ms":1e-3,"s":1.0}
TIME_PER={"ns/op":(1e-9,"s/op"),"μs/op":(1e-6,"s/op"),"µs/op":(1e-6,"s/op"),
          "ms/op":(1e-3,"s/op"),"ns/access":(1e-9,"s/access"),
          "μs/sync":(1e-6,"s/sync"),"µs/sync":(1e-6,"s/sync"),
          "μs/switch":(1e-6,"s/switch"),"µs/switch":(1e-6,"s/switch"),
          "ns/call":(1e-9,"s/call")}
BW={"MB/s":(1_000_000.0,"B/s"),"MiB/s":(1_048_576.0,"B/s"),"GB/s":(1_000_000_000.0,"B/s")}
SEM_RATE={"allocs/s","maps/s","events/s","states/s","IOPS"}

def load_binding(path):
    obj=json.loads(Path(path).read_text(encoding="utf-8"))
    if obj.get("schema")!="RAFAELIA_VECTRA_79_METRIC_BINDING_V2":
        raise ValueError("unexpected binding schema")
    fields=obj["fields"]
    out={}
    for row in obj["metrics"]:
        rec=dict(zip(fields,row))
        mid=rec["metric_id"]
        if mid in out: raise ValueError(f"duplicate metric_id {mid}")
        out[mid]=rec
    if sorted(out)!=list(range(79)):
        raise ValueError("binding must contain exactly metric_id 0..78")
    return out,obj["producer"]

def parse_formatted(text):
    if not isinstance(text,str): raise ValueError("formatted value must be string")
    m=re.match(r"^\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s+(.+?)\s*$",text)
    if not m: raise ValueError(f"unparseable formatted value: {text!r}")
    v=float(m.group(1)); u=m.group(2)
    if not math.isfinite(v): raise ValueError("non-finite formatted value")
    return v,u

def normalize(value, unit, semantic_kind):
    if semantic_kind=="io_operations_per_second" and unit in RATE:
        return value*RATE[unit],"IOPS","io_operation_rate","VECTRA_FORMATTED_RATE_TO_IOPS_V1"
    if unit=="IOPS":
        return value,"IOPS","io_operation_rate","UNIT_IOPS_SEMANTIC_V1"
    if unit in RATE:
        return value*RATE[unit],"ops/s","operation_rate","VECTRA_OP_RATE_PREFIX_V1"
    if unit in BW:
        f,cu=BW[unit]; return value*f,cu,"byte_bandwidth","VECTRA_BW_SI_V1"
    if unit in TIME_PER:
        f,cu=TIME_PER[unit]; return value*f,cu,"time_per_event","VECTRA_TIME_PER_EVENT_V1"
    if unit in TIME:
        return value*TIME[unit],"s","time","VECTRA_TIME_SI_V1"
    if unit in SEM_RATE:
        return value,unit,"semantic_rate","VECTRA_SEMANTIC_RATE_IDENTITY_V1"
    if unit=="MFLOPS":
        return value*1e6,"FLOP/s","floating_point_rate","UNIT_MFLOPS_TO_FLOPS_V1"
    if unit=="GFLOPS":
        return value*1e9,"FLOP/s","floating_point_rate","UNIT_GFLOPS_TO_FLOPS_V1"
    return None,unit,"unknown","TOKEN_VAZIO_UNIT_RULE"

def make_obs(metric, binding, producer, run, raw_ref, artifact_sha256=None, receipt_ref=None):
    formatted=metric.get("formatted") or metric.get("formatted_value")
    value,formatted_unit=parse_formatted(formatted)
    cv,cu,dim,rule=normalize(value,formatted_unit,binding["semantic_kind"])
    declared=metric.get("unit") or binding["declared_unit_label"]
    conflicts=[]
    if declared != formatted_unit:
        conflicts.append(f"declared_unit={declared};formatted_unit={formatted_unit}")
    conflicts.extend(binding.get("flags") or [])
    epi="MEASURED_WITH_RECEIPT" if (artifact_sha256 or receipt_ref) and run else "HISTORICAL_RUN_OUTPUT"
    state="MEASURED" if epi=="MEASURED_WITH_RECEIPT" else "HISTORICAL"
    evidence={"artifact_sha256":artifact_sha256,"receipt_refs":[receipt_ref] if receipt_ref else [],
              "raw_result_refs":[raw_ref],"digest_verified":None}
    norm={"status":"NORMALIZED" if cv is not None else "PRESERVED_SEMANTIC",
          "canonical_value":cv,"canonical_unit":cu,"dimension":dim,"rule_id":rule}
    notes=("; ".join(conflicts)) if conflicts else "method/unit binding consistent at static inspection level"
    return {
      "schema":SCHEMA,
      "observation_id":f"METRIC-VECTRA-{int(binding['metric_id']):02d}-{run.get('timestamp_ms','UNKNOWN')}",
      "observed_at":str(run.get("timestamp_ms")) if run.get("timestamp_ms") is not None else None,
      "metric_name":binding["symbol"],
      "category":{"CPU_SINGLE":"CPU","CPU_MULTI":"CPU","MEMORY":"MEMORY","STORAGE":"STORAGE",
                  "INTEGRITY":"INTEGRITY","EMULATION":"EMULATION"}[binding["category"]],
      "value_state":state,"epistemic_class":epi,
      "observed_value":value,"original_unit":formatted_unit,"normalization":norm,
      "statistic":{"kind":"RAW","sample_count":None,"repeats":None,"confidence":None},
      "direction":"CONTEXT_DEPENDENT",
      "scope":"VECTRA_BENCHMARK_RUN_BOUND_TO_STATIC_METHOD_MAP",
      "source_refs":[producer,{"metric_id":binding["metric_id"],"producer_method":binding["producer_method"],
                              "declared_unit_label":binding["declared_unit_label"],"formatter":binding["formatter"]}],
      "environment":{"cpu_model":run.get("cpu_model"),"cpu_arch":run.get("cpu_arch"),
                     "cpu_cores":run.get("cpu_cores"),"ram_bytes":run.get("ram_bytes")},
      "workload":{"seed":run.get("seed"),"warmup":run.get("warmup"),"samples":run.get("samples"),
                  "min_test_duration_ns":run.get("min_test_duration_ns")},
      "config":{"raw_ns":metric.get("raw_ns"),"formatted_value":formatted,"declared_unit":declared,
                "semantic_kind":binding["semantic_kind"],"binding_flags":binding.get("flags") or []},
      "evidence":evidence,"negative_evidence":False,
      "token_vazio":["TOKEN_VAZIO_UNIT_CONFLICT_REVIEW"] if declared != formatted_unit else [],
      "promotion_gate":{"status":"NOT_REQUESTED","reviewer":None,"receipt_ref":None},
      "claim_allowed":False,"notes":notes,
      "next_verifiable_step":"Validate observation; bind build/workload/receipt; review unit/proxy flags before any promotion."
    }

def read_jsonl(path):
    run={}
    metrics=[]
    for n,line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        obj=json.loads(line)
        if obj.get("type")=="run": run=obj
        elif obj.get("type")=="metric": metrics.append(obj)
    if not run: raise ValueError("JSONL missing type=run record")
    return run,metrics

def read_csv(path):
    rows=list(csv.DictReader(Path(path).open(encoding="utf-8",newline="")))
    metrics=[]
    for r in rows:
        metrics.append({"metric_id":int(r["metric_id"]),"name":r.get("name"),"category":r.get("category"),
                        "raw_ns":int(r["raw_ns"]),"formatted":r["formatted_value"],"unit":r["unit"]})
    return {},metrics

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument("--binding",required=True)
    ap.add_argument("--input",required=True)
    ap.add_argument("--format",choices=["jsonl","csv"],required=True)
    ap.add_argument("--output",required=True)
    ap.add_argument("--artifact-sha256")
    ap.add_argument("--receipt-ref")
    a=ap.parse_args(argv)
    bindings,producer=load_binding(a.binding)
    run,rows=read_jsonl(a.input) if a.format=="jsonl" else read_csv(a.input)
    out=[]
    for row in rows:
        mid=int(row["metric_id"])
        if mid not in bindings: raise SystemExit(f"unknown metric_id {mid}")
        out.append(make_obs(row,bindings[mid],producer,run,a.input,a.artifact_sha256,a.receipt_ref))
    Path(a.output).write_text("\n".join(json.dumps(x,ensure_ascii=False,separators=(",",":")) for x in out)+"\n",encoding="utf-8")
    print(f"PASS records={len(out)} output={a.output}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
