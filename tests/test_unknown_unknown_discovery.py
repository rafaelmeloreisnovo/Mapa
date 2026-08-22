#!/usr/bin/env python3
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tooling" / "unknown_unknown_discovery.py"
spec = importlib.util.spec_from_file_location("uud", MODULE_PATH)
uud = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(uud)


def test_not_found_is_candidate_not_fact():
    assets = [
        {"path": "codigo/a.c", "category": "codigo"},
        {"path": "docs/readme.md", "category": "docs"},
    ]
    atlas = {
        "records": [
            {
                "gap_id": "GAP-EXAMPLE-001",
                "falsifier": "counterexample",
                "next_gate": "run probe",
            }
        ]
    }
    out = uud.discover(assets, atlas)
    assert out
    assert all(x["state"] == "UNKNOWN_UNKNOWN_CANDIDATE" for x in out)
    assert all(x["claim_allowed"] is False for x in out)
    assert all("not proof of non-existence" in x["epistemic_boundary"] for x in out)


def test_gap_model_holes_are_detected():
    assets = [{"path": "receipts/r.json", "category": "receipts"}]
    atlas = {"records": [{"gap_id": "GAP-NO-GATE"}]}
    out = uud.discover(assets, atlas)
    classes = {(x["candidate_class"], x["key"]) for x in out}
    assert ("gap_without_falsifier", "GAP-NO-GATE") in classes
    assert ("gap_without_next_gate", "GAP-NO-GATE") in classes


def test_ids_and_order_are_deterministic():
    assets = [
        {"path": "z/x", "category": "z"},
        {"path": "a/x", "category": "a"},
    ]
    atlas = {"records": []}
    first = uud.discover(assets, atlas)
    second = uud.discover(list(reversed(assets)), atlas)
    assert first == second
    assert [x["candidate_id"] for x in first] == sorted(x["candidate_id"] for x in first)


if __name__ == "__main__":
    test_not_found_is_candidate_not_fact()
    test_gap_model_holes_are_detected()
    test_ids_and_order_are_deterministic()
    print(json.dumps({"tests": 3, "failures": 0, "status": "PASS"}))
