#!/usr/bin/env python3
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

ingest=load("ingest",ROOT/"tools"/"ingest_vectra_benchmark_v1.py")
validator=load("validator",ROOT/"tools"/"validate_metric_observation_v1.py")
BINDING=ROOT/"data"/"benchmarks"/"vectra-79-metric-binding.v2.json"


def run_context(ts=123):
    return {"timestamp_ms":ts,"cpu_model":"fixture","cpu_arch":"armv7l","cpu_cores":8,"ram_bytes":1024,
            "seed":1,"warmup":7,"samples":21,"min_test_duration_ns":500000000}


def test_iops_generic_mops_formatter_validates_semantically():
    bindings,producer=ingest.load_binding(BINDING)
    metric={"metric_id":47,"raw_ns":1000,"formatted":"1.50 Mops/s","unit":"IOPS"}
    obs=ingest.make_obs(metric,bindings[47],producer,run_context(),"fixture.jsonl")
    assert obs["normalization"]["canonical_unit"]=="IOPS"
    assert obs["normalization"]["canonical_value"]==1_500_000.0
    assert validator.validate(obs)==[]


def test_float_slot_generic_mops_formatter_becomes_flops_not_generic_ops():
    bindings,producer=ingest.load_binding(BINDING)
    metric={"metric_id":8,"raw_ns":1000,"formatted":"2.00 Mops/s","unit":"MFLOPS"}
    obs=ingest.make_obs(metric,bindings[8],producer,run_context(124),"fixture.jsonl")
    assert obs["normalization"]["canonical_unit"]=="FLOP/s"
    assert obs["normalization"]["canonical_value"]==2_000_000.0
    assert validator.validate(obs)==[]


def test_mapping_rate_generic_kops_formatter_retains_maps_semantics():
    bindings,producer=ingest.load_binding(BINDING)
    metric={"metric_id":72,"raw_ns":1000,"formatted":"5.00 Kops/s","unit":"maps/s"}
    obs=ingest.make_obs(metric,bindings[72],producer,run_context(125),"fixture.jsonl")
    assert obs["normalization"]["canonical_unit"]=="maps/s"
    assert obs["normalization"]["canonical_value"]==5000.0
    assert validator.validate(obs)==[]


def test_ns_access_is_normalized_consistently():
    norm=validator.expected_normalization(7.01,"ns/access")
    assert norm["canonical_unit"]=="s/access"
    assert abs(norm["canonical_value"]-7.01e-9)<1e-20
