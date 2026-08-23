#!/usr/bin/env python3
"""Dependency-free bootstrap audit for RAFAELIA Relationship House V1."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOUSE = ROOT / "RAFAELIA_RELATIONSHIP_HOUSE_V1"


def load_json(rel: str):
    with (HOUSE / rel).open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    contract = load_json("00_AUTHORITY/CONTRACT_V1.json")
    assert contract["dimensions_total"] == 17
    dims = contract["dimensions"]
    assert len(dims) == 17
    assert [d["id"] for d in dims] == [f"D{i}" for i in range(1, 18)]
    assert contract["txt_projection"]["max_chunk_bytes"] == 2_000_000
    assert contract["txt_projection"]["encoding"] == "UTF-8"
    assert contract["semantic_model"]["tensor_view"] == "DERIVED_ONLY"
    assert contract["semantic_model"]["geojson"] == "VISUALIZATION_ONLY"
    assert contract["token_vazio"]["mode"] == "FEDERATED_BRIDGE"

    tv = ROOT / contract["token_vazio"]["authority"]
    assert tv.is_file(), f"TOKEN_VAZIO authority missing: {tv}"

    ns = load_json("03_TAXONOMY/areas_namespace.bootstrap.json")
    assert ns["namespace_start"] == 1
    assert ns["namespace_end"] == 136
    assert ns["namespace_capacity"] == 136
    assert ns["completeness_claim"] is False
    assert ns["default_for_unlisted_slots"]["status"] == "TOKEN_VAZIO"
    conflicts = set(ns["conflict_slots"])
    provisional = set(ns["provisional_labels"])
    assert conflicts.isdisjoint(provisional), "conflicted taxonomy slot promoted as provisional"

    json_files = sorted(HOUSE.rglob("*.json"))
    for path in json_files:
        with path.open("r", encoding="utf-8") as f:
            json.load(f)

    for path in sorted(HOUSE.rglob("*.jsonl")):
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                if line.strip():
                    try:
                        json.loads(line)
                    except json.JSONDecodeError as exc:
                        raise AssertionError(f"invalid JSONL {path}:{line_no}: {exc}") from exc

    # This tree is public; explicit private Drive locators must never be committed.
    forbidden = ("drive.google.com", "document_id\":", "private_locator\":")
    for path in sorted(p for p in HOUSE.rglob("*") if p.is_file()):
        if path.suffix in {".md", ".json", ".jsonl", ".py", ".sh"}:
            text = path.read_text(encoding="utf-8")
            for needle in forbidden:
                assert needle not in text, f"public/private boundary violation in {path}: {needle}"

    print("RELATIONSHIP_HOUSE_V1_AUDIT=PASS")
    print(f"dimensions={len(dims)} namespace_capacity={ns['namespace_capacity']} json_files={len(json_files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
