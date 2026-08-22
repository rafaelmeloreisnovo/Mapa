#!/usr/bin/env python3
"""RAFAELIA UNKNOWN_UNKNOWN_DISCOVERY_V1.

Discovers *candidates* for unformulated gaps without pretending they are facts.
The engine is deliberately conservative: it emits UNKNOWN_UNKNOWN_CANDIDATE,
never PASS/FAIL, and requires later human/evidence promotion to TOKEN_VAZIO.

Inputs are bounded, versioned repository artifacts. No network access is used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

STATE = "UNKNOWN_UNKNOWN_CANDIDATE"
SCHEMA = "rafaelia.unknown_unknown_discovery.v1"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_asset_index(path: Path) -> list[dict[str, Any]]:
    """Parse the generated YAML asset index without requiring PyYAML.

    Only the stable `items` subset (path/category/content_type/extension) is needed.
    """
    items: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    in_items = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip() == "items:":
            in_items = True
            continue
        if not in_items:
            continue
        line = raw.strip()
        if line.startswith("- path:"):
            if current:
                items.append(current)
            current = {"path": line.split(":", 1)[1].strip().strip("'\"")}
        elif current and ":" in line:
            k, v = line.split(":", 1)
            if k in {"category", "content_type", "extension"}:
                current[k] = v.strip().strip("'\"")
    if current:
        items.append(current)
    return items


def stable_id(kind: str, key: str) -> str:
    digest = hashlib.sha256(f"{kind}\0{key}".encode()).hexdigest()[:12]
    return f"UUC-{kind.upper()}-{digest}"


def candidate(kind: str, key: str, observation: str, probe: str, evidence: list[str]) -> dict[str, Any]:
    return {
        "candidate_id": stable_id(kind, key),
        "state": STATE,
        "candidate_class": kind,
        "key": key,
        "observation": observation,
        "search_scope": evidence,
        "epistemic_boundary": "Absence in the bounded inputs is not proof of non-existence.",
        "promotion_rule": "Promote only after the missing question/object is formulated and a bounded search is evidenced; then create/link a TOKEN_VAZIO gap.",
        "next_probe": probe,
        "claim_allowed": False,
    }


def discover(asset_items: list[dict[str, Any]], gap_atlas: dict[str, Any]) -> list[dict[str, Any]]:
    paths = {x.get("path", "") for x in asset_items}
    categories = {x.get("category", "") for x in asset_items}
    gaps = gap_atlas.get("records", [])
    gap_text = json.dumps(gaps, sort_keys=True).lower()
    out: list[dict[str, Any]] = []

    # 1) Critical epistemic surfaces that should exist somewhere in a mature evidence system.
    expected_surfaces = {
        "falsifiers": ("falsifier", "Search for claims without explicit falsifiers and formalize the missing falsification question."),
        "provenance": ("provenance", "Search for artifacts/claims without source identity, custody, ref/hash or timestamp."),
        "receipts": ("receipt", "Search for executions or promotions lacking checksum-bound receipts."),
        "security": ("security", "Search for secret exposure, unsafe provenance and missing remediation receipts."),
        "replication": ("replication", "Search for important claims without independent reproduction authority."),
    }
    for surface, (needle, probe) in expected_surfaces.items():
        in_assets = surface in categories or any(surface in p.lower() for p in paths)
        in_gaps = needle in gap_text
        if not in_assets and not in_gaps:
            out.append(candidate(
                "missing_surface",
                surface,
                f"No explicit {surface!r} surface was found in the bounded asset index or Gap Atlas text.",
                probe,
                ["ASSET_INDEX_AUTO.yaml", "RAFAELIA_GAP_ATLAS_V1.json"],
            ))

    # 2) Repository categories with assets but no visible corresponding gap language.
    # This does not assert that a gap must exist; it asks whether the surface has been interrogated.
    for category in sorted(c for c in categories if c and c not in {"root", ".github"}):
        if category.lower() not in gap_text:
            out.append(candidate(
                "unquestioned_category",
                category,
                f"Category {category!r} exists in the asset inventory but is not named in the bounded Gap Atlas text.",
                f"Ask what can fail, drift, contradict, become orphaned, or lack evidence in category {category!r}; suppress candidate if an equivalent gap is found under another name.",
                ["ASSET_INDEX_AUTO.yaml", "RAFAELIA_GAP_ATLAS_V1.json"],
            ))

    # 3) Gap records without an explicit falsifier or next gate are epistemic holes in the gap model itself.
    for idx, rec in enumerate(gaps):
        gid = str(rec.get("gap_id", f"record-{idx}"))
        if not rec.get("falsifier"):
            out.append(candidate(
                "gap_without_falsifier",
                gid,
                f"Gap {gid} has no explicit falsifier in the bounded Gap Atlas record.",
                "Define what observation would show the current gap framing is wrong or already resolved.",
                ["RAFAELIA_GAP_ATLAS_V1.json"],
            ))
        if not rec.get("next_gate"):
            out.append(candidate(
                "gap_without_next_gate",
                gid,
                f"Gap {gid} has no explicit next_gate in the bounded Gap Atlas record.",
                "Define the smallest verifiable action that reduces uncertainty without promoting the claim.",
                ["RAFAELIA_GAP_ATLAS_V1.json"],
            ))

    # Stable deterministic ordering.
    return sorted(out, key=lambda x: x["candidate_id"])


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--asset-index", default="indices/ASSET_INDEX_AUTO.yaml")
    p.add_argument("--gap-atlas", default="data/gap-atlas/RAFAELIA_GAP_ATLAS_V1.json")
    p.add_argument("--output", default="data/gap-atlas/UNKNOWN_UNKNOWN_DISCOVERY_V1.generated.json")
    args = p.parse_args()

    asset_path = Path(args.asset_index)
    gap_path = Path(args.gap_atlas)
    asset_items = load_asset_index(asset_path)
    gap_atlas = load_json(gap_path)
    candidates = discover(asset_items, gap_atlas)

    payload = {
        "schema": SCHEMA,
        "state_model": [
            "KNOWN_KNOWN",
            "KNOWN_UNKNOWN",
            "UNKNOWN_UNKNOWN_CANDIDATE",
            "UNOBSERVABLE_CURRENTLY",
            "CONTRADICTION",
            "FALSIFIED",
            "VERIFIED_LIMITED",
        ],
        "inputs": {
            "asset_index": str(asset_path),
            "gap_atlas": str(gap_path),
        },
        "invariant": "NOT_FOUND_IN_BOUNDED_SEARCH != DOES_NOT_EXIST",
        "candidate_count": len(candidates),
        "candidates": candidates,
        "r3": {
            "f_ok": "Bounded deterministic discovery completed over declared inputs.",
            "f_gap": "Candidates are questions to investigate, not established missing facts.",
            "f_next": "Review candidates; for each confirmed formulated gap, append/link a TOKEN_VAZIO record with evidence of the bounded search.",
        },
        "claim_allowed": False,
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"schema": SCHEMA, "candidate_count": len(candidates), "output": args.output}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
