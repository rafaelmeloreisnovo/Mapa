import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "materialize_historical_metric_observations_v1.py"
spec = importlib.util.spec_from_file_location("histmat", SCRIPT)
histmat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(histmat)


def load_seed():
    return json.loads((ROOT / "data" / "benchmarks" / "historical-metric-seeds-046-047.v1.json").read_text(encoding="utf-8"))


def test_materializes_20_unique_records_fail_closed():
    records = histmat.materialize(load_seed())
    assert len(records) == 20
    ids = [r["observation_id"] for r in records]
    assert len(ids) == len(set(ids))
    assert all(r["schema"] == "RAFAELIA_METRIC_OBSERVATION_V1" for r in records)
    assert all(r["epistemic_class"] == "HISTORICAL_RUN_OUTPUT" for r in records)
    assert all(r["claim_allowed"] is False for r in records)


def test_negative_variants_and_supersession_preserved():
    records = {r["observation_id"]: r for r in histmat.materialize(load_seed())}
    assert records["METRIC-EDGEV7-047-001-UNROLL4_TIME"]["negative_evidence"] is True
    assert records["METRIC-EDGEV7-047-001-UNROLL8_BW"]["negative_evidence"] is True
    corrected = records["METRIC-ARM32-CPUMEM-046-001-CPU_MEAN_CORRECTED"]
    assert corrected["supersedes"] == ["METRIC-ARM32-CPUMEM-046-001-CPU_MEAN_SUPERSEDED"]


def test_source_shard_hashes_are_bound():
    records = histmat.materialize(load_seed())
    hashes = {r["evidence"]["artifact_sha256"] for r in records}
    assert "daef888aee856833c4f26c3c0af804826a2043c775f2d3c543d1135f27ee8e75" in hashes
    assert "dd133d11f02d757036eb3b9228a35e9734dc4b5984b1002f4f40c6b7260598d5" in hashes


def test_ns_access_is_preserved_not_guessed():
    records = {r["observation_id"]: r for r in histmat.materialize(load_seed())}
    lat = records["METRIC-ARM32-CPUMEM-046-001-LAT_16K"]
    assert lat["original_unit"] == "ns/access"
    assert lat["normalization"]["status"] == "PRESERVED_SEMANTIC"
    assert lat["normalization"]["canonical_unit"] == "ns/access"
