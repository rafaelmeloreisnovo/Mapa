#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

def load_gaps(path):
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows

def resolve(gap_id, rows):
    by_id = {row["gap_id"]: row for row in rows}
    gap = by_id.get(gap_id)
    if gap is None:
        return {
            "status": "TOKEN_VAZIO_GAP_NOT_FOUND",
            "gap_id": gap_id,
            "catalog_reduction": {
                "before": "NP_CATALOG",
                "after": "NP_CATALOG",
                "method": "no stable gap_id matched",
                "complexity_claim": False,
            },
            "claim_allowed": False,
        }

    ancestry = []
    cur = gap
    seen = set()
    while cur["parent_gap_id"] is not None:
        parent_id = cur["parent_gap_id"]
        if parent_id in seen or parent_id not in by_id:
            return {
                "status": "TOKEN_VAZIO_GAP_GRAPH_INVALID",
                "gap_id": gap_id,
                "claim_allowed": False,
            }
        seen.add(parent_id)
        ancestry.append(parent_id)
        cur = by_id[parent_id]

    return {
        "status": "GAP_NAVIGABLE",
        "gap_id": gap_id,
        "state": gap["state"],
        "kind": gap["kind"],
        "summary": gap["summary"],
        "origin_ref": gap["origin_ref"],
        "parent_gap_id": gap["parent_gap_id"],
        "child_gap_refs": gap["child_gap_refs"],
        "depth": len(ancestry),
        "path_to_root": list(reversed(ancestry)),
        "expected_type": gap["expected_type"],
        "evidence_needed": gap["evidence_needed"],
        "closure_criterion": gap["closure_criterion"],
        "catalog_reduction": gap["catalog_reduction"],
        "noise": gap["noise"],
        "markers": gap["markers"],
        "claim_allowed": False,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("gap_id")
    parser.add_argument("--gaps", default="data/manifold/gaps_omega_v1.jsonl")
    args = parser.parse_args()
    print(json.dumps(resolve(args.gap_id, load_gaps(args.gaps)), ensure_ascii=False, sort_keys=True))

if __name__ == "__main__":
    main()
