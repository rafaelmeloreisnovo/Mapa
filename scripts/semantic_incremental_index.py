#!/usr/bin/env python3
"""Deterministic RAFAELIA INC node indexer.

No network access. Reads versioned INC-*.yaml node headers, validates the
monotonic namespace, and emits a compact JSON discovery index. It does not
promote claims and does not allocate an ID when the existing sequence is
ambiguous.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

INC_RE = re.compile(r"^INC-(\d{6})$")
FIELD_RE = {
    "id": re.compile(r"^id:\s*(INC-\d{6})\s*$", re.M),
    "subject": re.compile(r'^subject:\s*["\']?(.*?)["\']?\s*$', re.M),
    "semantic_type": re.compile(r"^semantic_type:\s*(\S+)\s*$", re.M),
    "state": re.compile(r"^state:\s*(\S+)\s*$", re.M),
    "created_at": re.compile(r'^created_at:\s*["\']?(.*?)["\']?\s*$', re.M),
}


def field(text: str, name: str) -> str | None:
    match = FIELD_RE[name].search(text)
    return match.group(1).strip() if match else None


def load_nodes(root: Path) -> list[dict[str, str]]:
    nodes: list[dict[str, str]] = []
    seen: set[str] = set()
    for path in sorted(root.glob("INC-*.yaml")):
        text = path.read_text(encoding="utf-8")
        inc_id = field(text, "id")
        if not inc_id or not INC_RE.fullmatch(inc_id):
            raise ValueError(f"invalid or missing INC id: {path}")
        if path.stem != inc_id:
            raise ValueError(f"filename/id mismatch: {path.stem} != {inc_id}")
        if inc_id in seen:
            raise ValueError(f"duplicate INC id: {inc_id}")
        seen.add(inc_id)
        nodes.append({
            "id": inc_id,
            "subject": field(text, "subject") or "TOKEN_VAZIO_SUBJECT",
            "semantic_type": field(text, "semantic_type") or "TOKEN_VAZIO_SEMANTIC_TYPE",
            "state": field(text, "state") or "TOKEN_VAZIO_STATE",
            "created_at": field(text, "created_at") or "TOKEN_VAZIO_CREATED_AT",
            "path": path.as_posix(),
        })
    return nodes


def validate_sequence(nodes: list[dict[str, str]]) -> dict[str, object]:
    if not nodes:
        return {
            "sequence_state": "TOKEN_VAZIO_INCREMENTAL_SEQUENCE",
            "first": None,
            "last": None,
            "next_candidate": None,
        }
    nums = sorted(int(INC_RE.fullmatch(n["id"]).group(1)) for n in nodes)
    if len(nums) != len(set(nums)):
        raise ValueError("duplicate numeric INC id")
    missing = [n for n in range(nums[0], nums[-1] + 1) if n not in set(nums)]
    if missing:
        return {
            "sequence_state": "TOKEN_VAZIO_INCREMENTAL_SEQUENCE",
            "first": f"INC-{nums[0]:06d}",
            "last": f"INC-{nums[-1]:06d}",
            "next_candidate": None,
            "missing": [f"INC-{n:06d}" for n in missing],
        }
    return {
        "sequence_state": "PASS",
        "first": f"INC-{nums[0]:06d}",
        "last": f"INC-{nums[-1]:06d}",
        "next_candidate": f"INC-{nums[-1] + 1:06d}",
        "missing": [],
    }


def build_index(root: Path) -> dict[str, object]:
    nodes = load_nodes(root)
    return {
        "schema": "rafaelia_incremental_semantic_index_auto_v1",
        "claim_allowed": False,
        "source_root": root.as_posix(),
        "count": len(nodes),
        "sequence": validate_sequence(nodes),
        "nodes": nodes,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("data/memory/incremental"))
    parser.add_argument("--output", type=Path, default=Path("indices/semantic/INCREMENTAL_SEMANTIC_GRAPH_INDEX_AUTO.json"))
    parser.add_argument("--check", action="store_true", help="validate only; do not write")
    args = parser.parse_args()
    index = build_index(args.root)
    if index["sequence"]["sequence_state"] != "PASS":
        print(json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True))
        return 2
    if not args.check:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
