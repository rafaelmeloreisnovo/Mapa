#!/usr/bin/env python3
"""Materialize recursive child clusters from evidence-backed G3 SPLIT_REQUIRED decisions.

Input:
  pragmatic_action_map.json
  systematic-pragmatic-g3-decisions.v1.jsonl

Output:
  deterministic child candidates. The tool never binds gap_ids and never promotes claims.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Sequence

SCHEMA = "rafaelia.systematic-pragmatic-child-clusters/v1"
DECISION_SCHEMA = "rafaelia.systematic-pragmatic-g3-decision/v1"


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected object")
    return value


def load_decisions(path: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        row = json.loads(raw)
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{lineno}: decision must be object")
        if row.get("schema") != DECISION_SCHEMA:
            raise ValueError(f"{path}:{lineno}: unsupported decision schema")
        cid = row.get("cluster_id")
        if not isinstance(cid, str) or not cid.startswith("CL-"):
            raise ValueError(f"{path}:{lineno}: invalid cluster_id")
        if cid in out:
            raise ValueError(f"{path}:{lineno}: duplicate decision for {cid}")
        if row.get("claim_allowed") is not False:
            raise ValueError(f"{path}:{lineno}: claim_allowed must remain false")
        out[cid] = row
    return out


def parts(path: str) -> list[str]:
    return [p for p in Path(path).parts if p not in {"", "."}]


def child_cluster_id(parent_cluster_id: str, segment: str) -> str:
    raw = f"{parent_cluster_id}\0{segment}".encode("utf-8")
    return "CL-" + hashlib.sha256(raw).hexdigest()[:16]


def rows_for_top_cluster(
    action_map: dict[str, Any],
    cluster: dict[str, Any],
) -> list[dict[str, Any]]:
    domain = str(cluster.get("domain", ""))
    return [
        row
        for row in action_map.get("actions", [])
        if row.get("root") == cluster.get("root")
        and row.get("service") == cluster.get("service")
        and row.get("nibiguiri_state") == cluster.get("nibiguiri_state")
        and list(row.get("markers") or []) == list(cluster.get("markers") or [])
        and parts(str(row.get("path", "")))
        and parts(str(row.get("path", "")))[0] == domain
    ]


def g4_state_for(decision_state: str, decision: dict[str, Any] | None) -> str:
    if decision_state == "SPLIT_REQUIRED":
        return "BLOCKED_BY_G3_SPLIT"
    if decision_state == "DISTINCT_GAP":
        return "REQUIRES_PER_ITEM_BINDING"
    if decision_state == "SAME_FAMILY":
        return "READY_FOR_AUTHORITY_BIND"
    if decision_state == "DUPLICATE":
        return "READY_FOR_EXISTING_BINDING"
    if decision_state == "FALSE_POSITIVE":
        return "NOT_APPLICABLE_FALSE_POSITIVE"
    if decision_state == "ACCEPTED_LIMITATION":
        return "NOT_APPLICABLE_ACCEPTED_LIMITATION"
    if decision:
        return "BLOCKED_PENDING_AUTHORITY_BIND"
    return "BLOCKED_BY_G3"


def split_rows(
    *,
    parent_cluster_id: str,
    parent_scope: Sequence[str],
    rows: Sequence[dict[str, Any]],
    decisions: dict[str, dict[str, Any]],
    level: int,
    ancestry: Sequence[str],
) -> list[dict[str, Any]]:
    next_index = len(parent_scope)
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        pp = parts(str(row.get("path", "")))
        segment = pp[next_index] if len(pp) > next_index else "__root__"
        grouped.setdefault(segment, []).append(row)

    children: list[dict[str, Any]] = []
    for segment, child_rows in sorted(grouped.items()):
        cid = child_cluster_id(parent_cluster_id, segment)
        scope = list(parent_scope) + [segment]
        next_counts: dict[str, int] = {}
        for row in child_rows:
            pp = parts(str(row.get("path", "")))
            nxt = pp[len(scope)] if len(pp) > len(scope) else "__leaf__"
            next_counts[nxt] = next_counts.get(nxt, 0) + 1

        priorities = sorted({str(row.get("priority", "")) for row in child_rows})
        authorities = sorted(
            {
                str(value)
                for row in child_rows
                for value in row.get("authority_required", [])
                if value
            }
        )
        evidence = sorted(
            {
                str(value)
                for row in child_rows
                for value in row.get("evidence_required", [])
                if value
            }
        )

        decision = decisions.get(cid)
        decision_state = decision.get("decision") if decision else "REVIEW_REQUIRED"
        split_strategy = (
            decision.get("split_strategy", "PATH_SEGMENT")
            if decision_state == "SPLIT_REQUIRED" and decision
            else None
        )
        g4_state = g4_state_for(decision_state, decision)

        child = {
            "cluster_id": cid,
            "parent_cluster_id": parent_cluster_id,
            "ancestry": list(ancestry) + [parent_cluster_id],
            "level": level,
            "root": child_rows[0].get("root") if child_rows else "TOKEN_VAZIO",
            "scope_prefix": "/".join(scope),
            "segment": segment,
            "action_count": len(child_rows),
            "priorities": priorities,
            "service": child_rows[0].get("service") if child_rows else "TOKEN_VAZIO",
            "markers": list(child_rows[0].get("markers") or []) if child_rows else [],
            "nibiguiri_state": (
                child_rows[0].get("nibiguiri_state") if child_rows else "TOKEN_VAZIO"
            ),
            "next_segment_counts": dict(sorted(next_counts.items())),
            "sample_paths": sorted(str(row.get("path", "")) for row in child_rows)[:10],
            "authority_required": authorities,
            "evidence_required": evidence,
            "g3": {
                "state": decision_state,
                "decision_id": decision.get("decision_id") if decision else None,
                "split_strategy": split_strategy,
                "binding_strategy": decision.get("binding_strategy") if decision else None,
                "automatic_decision": False,
            },
            "g4": {
                "state": g4_state,
                "binding": "TOKEN_VAZIO",
                "auto_create_gap_id": False,
            },
            "claim_allowed": False,
        }
        children.append(child)

        if decision_state == "SPLIT_REQUIRED" and split_strategy == "PATH_SEGMENT":
            children.extend(
                split_rows(
                    parent_cluster_id=cid,
                    parent_scope=scope,
                    rows=child_rows,
                    decisions=decisions,
                    level=level + 1,
                    ancestry=list(ancestry) + [parent_cluster_id],
                )
            )

    return children


def materialize(
    action_map: dict[str, Any],
    decisions: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    if action_map.get("schema") != "rafaelia.systematic-pragmatic-map/v1":
        raise ValueError("unsupported pragmatic action map schema")
    if action_map.get("claim_allowed") is not False:
        raise ValueError("action map claim_allowed must remain false")

    top_by_id = {
        str(cluster.get("cluster_id")): cluster
        for cluster in action_map.get("clusters", [])
        if isinstance(cluster, dict)
    }

    children: list[dict[str, Any]] = []
    consumed_decisions: set[str] = set()
    for cid, decision in sorted(decisions.items()):
        if cid not in top_by_id:
            continue
        if decision.get("decision") != "SPLIT_REQUIRED":
            continue
        parent = top_by_id[cid]
        rows = rows_for_top_cluster(action_map, parent)
        if not rows:
            raise ValueError(f"SPLIT_REQUIRED parent {cid} has no current actions")
        consumed_decisions.add(cid)
        children.extend(
            split_rows(
                parent_cluster_id=cid,
                parent_scope=[str(parent.get("domain", ""))],
                rows=rows,
                decisions=decisions,
                level=1,
                ancestry=[],
            )
        )

    generated_ids = {row["cluster_id"] for row in children}
    for cid, decision in decisions.items():
        if cid in generated_ids and decision.get("decision") == "SPLIT_REQUIRED":
            consumed_decisions.add(cid)

    unresolved_split_decisions = sorted(
        cid
        for cid, decision in decisions.items()
        if decision.get("decision") == "SPLIT_REQUIRED" and cid not in consumed_decisions
    )
    if unresolved_split_decisions:
        raise ValueError(
            "SPLIT_REQUIRED decisions do not resolve to current parent/child clusters: "
            + ", ".join(unresolved_split_decisions)
        )

    roots = [row for row in children if row["level"] == 1]
    review_required = sum(1 for row in children if row["g3"]["state"] == "REVIEW_REQUIRED")
    split_required = sum(1 for row in children if row["g3"]["state"] == "SPLIT_REQUIRED")
    deferred_semantic_splits = sum(
        1
        for row in children
        if row["g3"]["state"] == "SPLIT_REQUIRED"
        and row["g3"].get("split_strategy") == "SEMANTIC_SCHEMA"
    )
    distinct_gap = sum(1 for row in children if row["g3"]["state"] == "DISTINCT_GAP")

    payload = {
        "schema": SCHEMA,
        "claim_allowed": False,
        "source_action_map_sha256": canonical_sha256(action_map),
        "policy": {
            "recursive_split_requires_g3_decision": True,
            "child_is_not_equivalence": True,
            "auto_create_gap_id": False,
            "g4_requires_completed_g3": True,
        },
        "summary": {
            "child_candidates_total": len(children),
            "level1_children": len(roots),
            "review_required": review_required,
            "split_required": split_required,
            "deferred_semantic_splits": deferred_semantic_splits,
            "distinct_gap": distinct_gap,
            "max_level": max((row["level"] for row in children), default=0),
        },
        "children": sorted(
            children,
            key=lambda row: (
                row["level"],
                -row["action_count"],
                row["scope_prefix"],
                row["cluster_id"],
            ),
        ),
    }
    payload["children_digest_sha256"] = canonical_sha256(payload["children"])
    return payload


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--action-map", type=Path, required=True)
    ap.add_argument("--decisions", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    try:
        action_map = load_json(args.action_map)
        decisions = load_decisions(args.decisions)
        payload = materialize(action_map, decisions)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"child-materializer: {exc}")
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload["summary"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
