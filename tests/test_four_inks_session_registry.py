from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_four_inks_session_registry.py"
SPEC = importlib.util.spec_from_file_location("four_inks_registry", MODULE_PATH)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def records():
    return MOD.load_records(ROOT / "indices/SESSION_VECTOR_FOUR_INKS_REGISTRY.v1.jsonl")


def test_registry_passes():
    report = MOD.validate(records())
    assert report["status"] == "PASS", report["errors"]
    assert report["claim_allowed"] is False
    assert report["pointer_count"] == 5
    assert report["selected_vector_count"] == 22


def test_pointer_claim_cannot_be_elevated():
    data = records()
    data[0]["claim_allowed"] = True
    report = MOD.validate(data)
    assert report["status"] == "FAIL"
    assert any("claim_allowed" in e for e in report["errors"])


def test_source_ref_drift_fails():
    data = records()
    data[0]["source_ref"] = "0" * 40
    report = MOD.validate(data)
    assert report["status"] == "FAIL"
    assert any("one producer ref" in e for e in report["errors"])


def test_source_blob_drift_fails():
    data = records()
    data[-1]["source_blob_sha"] = "1" * 40
    report = MOD.validate(data)
    assert report["status"] == "FAIL"
    assert any("one producer blob" in e for e in report["errors"])


def test_authority_split_brain_fails():
    data = records()
    data[1]["authority"]["control_plane"] = "rafaelmeloreisnovo/papers"
    report = MOD.validate(data)
    assert report["status"] == "FAIL"
    assert any("authority split" in e for e in report["errors"])


def test_selector_count_mismatch_fails():
    data = records()
    data[2]["selector"]["expected_count"] = 4
    report = MOD.validate(data)
    assert report["status"] == "FAIL"
    assert any("expected_count" in e or "total 22" in e for e in report["errors"])


def test_missing_regime_fails():
    data = records()[:-1]
    report = MOD.validate(data)
    assert report["status"] == "FAIL"
    assert any("all five regimes" in e for e in report["errors"])


def test_token_vazio_digest_does_not_allow_claim():
    data = records()
    assert all(r["source_digest"] == "TOKEN_VAZIO" for r in data)
    assert all(r["claim_allowed"] is False for r in data)
