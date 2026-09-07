#!/usr/bin/env python3
"""Fail-closed validator for NOVOexport ACTIVE_V2 source-universe binding."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data/evidence/novoexport_active_v2_source_universe_20260907.v1.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")

REQUIRED_INVARIANTS = {
    "DATASET_INFORMS != MISSION_AUTHORITY",
    "RETRIEVAL_CONTEXT != WEIGHT_UPDATE",
    "LEARN_APPEND_ONLY != ONLINE_SELF_TRAINING",
    "SOURCE != DERIVED_INDEX != EXECUTION != EVIDENCE != CLAIM",
    "RAPPORT != PROOF",
    "TOKEN_VAZIO != 0",
    "PHYSICAL_UNIVERSE_BOUND != SEMANTIC_EXHAUSTIVITY",
    "DEFAULT_BRANCH_PROVIDER > BRANCH_NAME_ASSUMPTION",
    "NOT_FOUND_ROUTE != DATA_LOSS",
}

def validate(d: dict) -> list[str]:
    e: list[str] = []
    if d.get("schema") != "rafaelia.novoexport-active-v2-source-universe.v1":
        e.append("schema")
    if d.get("claim_allowed") is not False:
        e.append("claim_allowed_must_be_false")

    p = d.get("physical_universe", {})
    cats = p.get("category_counts", {})
    if p.get("export_files") != 15439:
        e.append("export_files")
    if p.get("logical_files") != 15369:
        e.append("logical_files")
    if sum(cats.values()) != p.get("export_files"):
        e.append("category_sum")
    if cats != {
        "dat": 15358,
        "conversations_json": 51,
        "codex_json": 21,
        "core_json": 8,
        "chat_html": 1,
    }:
        e.append("category_counts")

    conv = p.get("conversations_shards", {})
    if conv != {"first": 0, "last": 50, "count": 51, "missing": []}:
        e.append("conversations_range")
    codex = p.get("codex_shards", {})
    if codex != {"first": 0, "last": 20, "count": 21, "missing": []}:
        e.append("codex_range")

    src = d.get("source", {})
    if not HEX64.fullmatch(str(src.get("export_manifest_sha256", ""))):
        e.append("export_manifest_sha256")
    for k in ("canonical_path_size_lines_sha256", "merkle_sha256_path_nul_size"):
        if not HEX64.fullmatch(str(p.get(k, ""))):
            e.append(k)
    if p.get("merkle_leaf_count") != p.get("export_files"):
        e.append("merkle_leaf_count")

    sem = d.get("semantic_ingest", {})
    if sem.get("physical_manifest_complete") is not True:
        e.append("physical_manifest_complete")
    if sem.get("semantic_exhaustivity_proven") is not False:
        e.append("semantic_exhaustivity_proven_must_be_false")
    if not str(sem.get("state", "")).startswith("TOKEN_VAZIO"):
        e.append("semantic_state")

    drift = d.get("route_drift", [])
    if not drift:
        e.append("route_drift")
    else:
        for item in drift:
            if item.get("readback") == "NOT_FOUND" and item.get("replacement") != "TOKEN_VAZIO":
                e.append("not_found_replacement_inferred")

    missing_inv = REQUIRED_INVARIANTS - set(d.get("invariants", []))
    if missing_inv:
        e.append("missing_invariants:" + ",".join(sorted(missing_inv)))

    gaps = set(d.get("planes", {}).get("GAP:X", []))
    if not {"TV-INDEX-INGEST-000-050", "TV-MESSAGES-FULL-COVERAGE"} <= gaps:
        e.append("open_semantic_gaps_not_preserved")

    return e

def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else DEFAULT
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: cannot read {path}: {exc}", file=sys.stderr)
        return 2
    errors = validate(d)
    if errors:
        print("FAIL: " + "; ".join(errors), file=sys.stderr)
        return 1
    print(
        "PASS "
        f"physical={d['physical_universe']['export_files']} "
        f"logical={d['physical_universe']['logical_files']} "
        "semantic=OPEN claim_allowed=false"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
