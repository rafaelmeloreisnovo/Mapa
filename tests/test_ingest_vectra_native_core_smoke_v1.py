#!/usr/bin/env python3
import importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

ingest=load("native_smoke",ROOT/"tools"/"ingest_vectra_native_core_smoke_v1.py")
validator=load("validator",ROOT/"tools"/"validate_metric_observation_v1.py")
BINDING=json.loads((ROOT/"data"/"benchmarks"/"vectra-native-core-smoke-binding.v1.json").read_text(encoding="utf-8"))


def test_parse_exact_smoke_line():
    p=ingest.parse("benchmark_smoke: iters=100000 total_ns=59488100 avg_ns=594.88 hash64=123456\n")
    assert p=={"iters":100000,"total_ns":59488100,"avg_ns":594.88,"hash64":123456}


def test_iteration_mismatch_fails_closed():
    p=ingest.parse("benchmark_smoke: iters=99999 total_ns=1 avg_ns=1.0 hash64=1")
    try:
        ingest.observations(p,BINDING,"fixture.log")
        assert False,"expected iteration mismatch"
    except ValueError as e:
        assert "iteration mismatch" in str(e)


def test_without_receipt_remains_historical_and_validates():
    p=ingest.parse("benchmark_smoke: iters=100000 total_ns=59488100 avg_ns=594.88 hash64=123456")
    records=ingest.observations(p,BINDING,"fixture.log")
    assert len(records)==2
    assert all(r["epistemic_class"]=="HISTORICAL_RUN_OUTPUT" for r in records)
    assert all(r["claim_allowed"] is False for r in records)
    assert all(validator.validate(r)==[] for r in records)


def test_avg_metric_uses_ns_per_sector_semantics():
    p=ingest.parse("benchmark_smoke: iters=100000 total_ns=59488100 avg_ns=594.88 hash64=123456")
    avg=ingest.observations(p,BINDING,"fixture.log")[1]
    assert avg["original_unit"]=="ns/sector"
    assert avg["normalization"]["canonical_unit"]=="s/sector"
    assert abs(avg["normalization"]["canonical_value"]-5.9488e-7)<1e-15
