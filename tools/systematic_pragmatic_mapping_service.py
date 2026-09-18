#!/usr/bin/env python3
"""Systematic + pragmatic mapping service for the RAFAELIA Gap Atlas.

This is an orchestration layer over repository_gap_mapper.py. It does not
auto-close gaps and does not promote claims. It turns bounded repository
observations into a deterministic action queue with:

SOURCE -> OBSERVATION -> ATLAS BINDING -> NIBIGUIRI -> SERVICE -> GATE -> RECEIPT

Python stdlib only; suitable for Termux, CI and offline/local execution.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterable, Sequence

import repository_gap_mapper as rgm

SCHEMA = "rafaelia.systematic-pragmatic-map/v1"
RECEIPT_SCHEMA = "rafaelia.systematic-pragmatic-map-receipt/v1"

PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "TOKEN_VAZIO": 9}
DEFAULT_GAP_PRIORITY = {
    "BINARY_PROVENANCE_MISSING": "P1",
    "ASM_NOT_REFERENCED_BY_BUILD": "P1",
    "HASH_INCOMPLETE": "P1",
    "UNRESOLVED_MARKERS": "P2",
    "DOCUMENT_INCOMPLETE": "P2",
}
SERVICE_BY_GAP = {
    "BINARY_PROVENANCE_MISSING": "PROVENANCE_REPAIR",
    "ASM_NOT_REFERENCED_BY_BUILD": "BUILD_INTEGRATION_AUDIT",
    "HASH_INCOMPLETE": "CUSTODY_HASH",
    "UNRESOLVED_MARKERS": "SEMANTIC_TRIAGE",
    "DOCUMENT_INCOMPLETE": "DOCUMENT_COMPLETION",
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def unique(values: Iterable[str]) -> list[str]:
    return sorted({value for value in values if value})


def match_atlas_records(
    atlas_records: Sequence[dict[str, Any]],
    artifact_id: str,
    path: str,
) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for record in atlas_records:
        refs = "\n".join(str(x) for x in record.get("source_refs", []))
        if record.get("artifact_id") == artifact_id or (path and path in refs):
            matches.append(record)
    return matches


def record_priority(records: Sequence[dict[str, Any]], gap: str) -> str:
    observed = [
        str(record.get("priority", "TOKEN_VAZIO"))
        for record in records
        if str(record.get("priority", "TOKEN_VAZIO")) in PRIORITY_ORDER
    ]
    if observed:
        return min(observed, key=lambda value: PRIORITY_ORDER[value])
    return DEFAULT_GAP_PRIORITY.get(gap, "P2")


def next_gate_for(
    records: Sequence[dict[str, Any]],
    nibiguiri_state: str,
) -> list[str]:
    if records:
        gates = unique(str(record.get("next_gate", "")) for record in records)
        return gates or ["Review mapped Atlas record and execute its evidence gate."]
    if nibiguiri_state == "NIBIGUIRI:CAUSA_DESCONHECIDA":
        return [
            "Determine whether this observation is a real gap, accepted limitation, "
            "false positive, duplicate, or formally demonstrable unindexed relation; "
            "only then bind/promote its Nibiguiri subtype."
        ]
    return ["Preserve TOKEN_VAZIO and obtain source/evidence before promotion."]


def action_id(root: str, path: str, gap: str) -> str:
    return hashlib.sha256(f"{root}\0{path}\0{gap}".encode("utf-8")).hexdigest()[:24]


def path_domain(path: str) -> str:
    parts = [part for part in Path(path).parts if part not in {".", ""}]
    return parts[0] if parts else "__root__"


def cluster_id(
    root: str,
    domain: str,
    service: str,
    markers: Sequence[str],
    nibiguiri_state: str,
) -> str:
    raw = "\0".join(
        [root, domain, service, ",".join(sorted(markers)), nibiguiri_state]
    ).encode("utf-8")
    return "CL-" + hashlib.sha256(raw).hexdigest()[:16]


def build_clusters(actions: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str, tuple[str, ...], str], list[dict[str, Any]]] = {}
    for action in actions:
        key = (
            str(action.get("root", "")),
            path_domain(str(action.get("path", ""))),
            str(action.get("service", "GAP_TRIAGE")),
            tuple(sorted(str(x) for x in action.get("markers", []))),
            str(action.get("nibiguiri_state", "TOKEN_VAZIO")),
        )
        grouped.setdefault(key, []).append(action)

    clusters: list[dict[str, Any]] = []
    for (root, domain, service, markers, state), rows in sorted(grouped.items()):
        priorities = sorted(
            {str(row.get("priority", "TOKEN_VAZIO")) for row in rows},
            key=lambda value: PRIORITY_ORDER.get(value, 9),
        )
        cid = cluster_id(root, domain, service, markers, state)
        authority_required = unique(
            str(value)
            for row in rows
            for value in row.get("authority_required", [])
        )
        evidence_required = unique(
            str(value)
            for row in rows
            for value in row.get("evidence_required", [])
        )
        clusters.append(
            {
                "cluster_id": cid,
                "root": root,
                "domain": domain,
                "service": service,
                "markers": list(markers),
                "nibiguiri_state": state,
                "action_count": len(rows),
                "priorities": priorities,
                "sample_paths": sorted(str(row.get("path", "")) for row in rows)[:10],
                "authority_required": authority_required,
                "evidence_required": evidence_required,
                "g3_semantic_split_gate": {
                    "state": "REVIEW_REQUIRED",
                    "allowed_decisions": [
                        "DUPLICATE",
                        "SAME_FAMILY",
                        "DISTINCT_GAP",
                        "FALSE_POSITIVE",
                        "ACCEPTED_LIMITATION",
                    ],
                    "automatic_decision": False,
                    "evidence_required": [
                        "Representative source sample",
                        "Invariant comparison",
                        "Reason for merge/split/closure classification",
                    ],
                },
                "g4_authority_bind_gate": {
                    "state": "BLOCKED_BY_G3",
                    "binding": "TOKEN_VAZIO",
                    "auto_create_gap_id": False,
                    "authority_required": authority_required,
                    "evidence_required": evidence_required,
                },
                "next_gate": (
                    "G3: review representative samples and decide DUPLICATE, SAME_FAMILY, "
                    "DISTINCT_GAP, FALSE_POSITIVE or ACCEPTED_LIMITATION. G4 remains "
                    "blocked until that decision has evidence."
                ),
                "claim_allowed": False,
            }
        )
    return clusters


def build_cluster_review_queue(
    clusters: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema": "rafaelia.systematic-pragmatic-cluster-review/v1",
        "claim_allowed": False,
        "policy": {
            "cluster_is_not_equivalence": True,
            "unknown_cause_is_default": True,
            "obvious_unindexed_requires_formal_demonstration": True,
            "authority_binding_requires_g3_evidence": True,
            "auto_create_gap_id": False,
        },
        "gates": {
            "G3_SEMANTIC_SPLIT": {
                "pass_requires": [
                    "explicit decision",
                    "representative source evidence",
                    "invariant comparison",
                    "reason",
                ]
            },
            "G4_AUTHORITY_BIND": {
                "blocked_until": "G3_SEMANTIC_SPLIT=PASS",
                "pass_requires": [
                    "existing gap_id or governed new gap proposal",
                    "authority_required",
                    "evidence_required",
                ],
            },
        },
        "clusters": [
            {
                "cluster_id": cluster["cluster_id"],
                "root": cluster["root"],
                "domain": cluster["domain"],
                "service": cluster["service"],
                "action_count": cluster["action_count"],
                "markers": cluster["markers"],
                "nibiguiri_state": cluster["nibiguiri_state"],
                "sample_paths": cluster["sample_paths"],
                "g3_semantic_split_gate": cluster["g3_semantic_split_gate"],
                "g4_authority_bind_gate": cluster["g4_authority_bind_gate"],
                "claim_allowed": False,
            }
            for cluster in clusters
        ],
    }


def pragmatic_filter_stats(gap_map: dict[str, Any]) -> dict[str, int]:
    preserved = 0
    coalesced = 0
    for artifact in gap_map.get("artifacts", []):
        gaps = set(artifact.get("gaps") or [])
        markers = set(artifact.get("unresolved_markers") or [])
        if (
            artifact.get("kind") == "DOCUMENT"
            and markers
            and markers.issubset({"TOKEN_VAZIO"})
        ):
            preserved += 1
        elif "UNRESOLVED_MARKERS" in gaps and "DOCUMENT_INCOMPLETE" in gaps:
            coalesced += 1
    return {
        "preserved_token_vazio_observations": preserved,
        "coalesced_document_duplicate_actions": coalesced,
    }


def build_actions(gap_map: dict[str, Any], atlas: dict[str, Any]) -> list[dict[str, Any]]:
    if gap_map.get("schema") != rgm.SCHEMA:
        raise ValueError(f"unsupported gap map schema: {gap_map.get('schema')}")
    if atlas.get("schema") != "RAFAELIA_GAP_ATLAS_V1":
        raise ValueError(f"unsupported atlas schema: {atlas.get('schema')}")

    records = list(atlas.get("records", []))
    actions: list[dict[str, Any]] = []

    for artifact in gap_map.get("artifacts", []):
        root = str(artifact.get("root", ""))
        path = str(artifact.get("path", ""))
        artifact_id = str(artifact.get("artifact_id", ""))
        gaps = sorted(set(artifact.get("gaps") or []))
        markers = set(artifact.get("unresolved_markers") or [])

        # TOKEN_VAZIO is a valid epistemic state. A document containing only
        # TOKEN_VAZIO markers is preserved as an observation in the source gap
        # map and must not become artificial work in the pragmatic queue.
        if (
            artifact.get("kind") == "DOCUMENT"
            and markers
            and markers.issubset({"TOKEN_VAZIO"})
        ):
            continue

        # repository_gap_mapper emits DOCUMENT_INCOMPLETE in addition to
        # UNRESOLVED_MARKERS for the same document. One root cause should create
        # one pragmatic action, not two.
        if "UNRESOLVED_MARKERS" in gaps and "DOCUMENT_INCOMPLETE" in gaps:
            gaps = [gap for gap in gaps if gap != "DOCUMENT_INCOMPLETE"]

        for gap in gaps:
            matched = match_atlas_records(records, artifact_id, path)
            gap_ids = unique(str(record.get("gap_id", "")) for record in matched)
            priority = record_priority(matched, gap)
            if matched:
                nibiguiri_state = "INDEXED"
                atlas_state = unique(str(record.get("state", "")) for record in matched)
            else:
                # Absence of an Atlas binding proves only that the cause/class is
                # unresolved. OBVIO_NAO_INDEXADO is reserved for a separately
                # demonstrated formal relation, never inferred from scanner absence.
                nibiguiri_state = "NIBIGUIRI:CAUSA_DESCONHECIDA"
                atlas_state = ["TOKEN_VAZIO_NOT_INDEXED"]

            authority = unique(
                str(value)
                for record in matched
                for value in record.get("authority_required", [])
            )
            evidence = unique(
                str(value)
                for record in matched
                for value in record.get("evidence_required", [])
            )
            if not authority:
                authority = ["Repository owner/producer", "Gap Atlas governance"]
            if not evidence:
                evidence = [
                    "Stable source/path/hash binding",
                    "Triage receipt",
                    "Gap-ID binding or explicit false-positive/accepted-limitation event",
                ]

            actions.append(
                {
                    "action_id": action_id(root, path, gap),
                    "root": root,
                    "path": path,
                    "artifact_id": artifact_id,
                    "artifact_kind": artifact.get("kind"),
                    "gap": gap,
                    "priority": priority,
                    "blocking": priority == "P0",
                    "service": SERVICE_BY_GAP.get(gap, "GAP_TRIAGE"),
                    "markers": sorted(markers),
                    "nibiguiri_state": nibiguiri_state,
                    "mapped_gap_ids": gap_ids,
                    "atlas_state": atlas_state,
                    "authority_required": authority,
                    "evidence_required": evidence,
                    "next_gate": next_gate_for(matched, nibiguiri_state),
                    "source_sha256": artifact.get("sha256"),
                    "hash_status": artifact.get("hash_status"),
                    "effort": "TOKEN_VAZIO_UNMEASURED",
                    "claim_allowed": False,
                }
            )

    actions.sort(
        key=lambda row: (
            PRIORITY_ORDER.get(str(row["priority"]), 9),
            0 if row["nibiguiri_state"] != "INDEXED" else 1,
            str(row["service"]),
            str(row["root"]),
            str(row["path"]),
            str(row["gap"]),
        )
    )
    return actions


def summarize(actions: Sequence[dict[str, Any]]) -> dict[str, Any]:
    priorities = {key: 0 for key in ("P0", "P1", "P2", "P3", "TOKEN_VAZIO")}
    services: dict[str, int] = {}
    nibiguiri: dict[str, int] = {}
    for action in actions:
        priority = str(action.get("priority", "TOKEN_VAZIO"))
        priorities[priority] = priorities.get(priority, 0) + 1
        service = str(action.get("service", "GAP_TRIAGE"))
        services[service] = services.get(service, 0) + 1
        state = str(action.get("nibiguiri_state", "TOKEN_VAZIO"))
        nibiguiri[state] = nibiguiri.get(state, 0) + 1

    return {
        "actions": len(actions),
        "blocking_p0": priorities.get("P0", 0),
        "unmapped": sum(
            1 for row in actions if row.get("nibiguiri_state") != "INDEXED"
        ),
        "priorities": priorities,
        "services": dict(sorted(services.items())),
        "nibiguiri": dict(sorted(nibiguiri.items())),
    }


def render_markdown(payload: dict[str, Any], top: int) -> str:
    summary = payload["summary"]
    actions = payload["actions"]
    shown = actions if top <= 0 else actions[:top]
    lines = [
        "# RAFAELIA — Systematic Pragmatic Map",
        "",
        f"- Schema: `{payload['schema']}`",
        f"- Generated at: `{payload['generated_at']}`",
        f"- Actions: **{summary['actions']}**",
        f"- P0 blockers: **{summary['blocking_p0']}**",
        f"- Nibiguiri/unmapped: **{summary['unmapped']}**",
        f"- Deterministic clusters: **{summary.get('clusters', 0)}**",
        f"- Largest cluster: **{summary.get('largest_cluster_actions', 0)}** actions",
        f"- TOKEN_VAZIO preserved as observation: **{summary.get('preserved_token_vazio_observations', 0)}**",
        f"- Duplicate document actions coalesced: **{summary.get('coalesced_document_duplicate_actions', 0)}**",
        "- Claim boundary: `claim_allowed=false`",
        "",
        "## Operational flow",
        "",
        "`SCAN → BIND → NIBIGUIRI → PRIORIZE → SERVICE → GATE → RECEIPT`",
        "",
        "## Action queue",
        "",
        "| Pri | Root | Path | Gap | Service | Nibiguiri | Next gate |",
        "|---|---|---|---|---|---|---|",
    ]
    if not shown:
        lines.append("| — | — | — | — | — | — | No detected action |")
    for row in shown:
        gate = "<br>".join(str(x) for x in row["next_gate"])
        path = str(row["path"]).replace("|", "\\|")
        lines.append(
            f"| **{row['priority']}** | `{row['root']}` | `{path}` | "
            f"`{row['gap']}` | `{row['service']}` | "
            f"`{row['nibiguiri_state']}` | {gate} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `INDEXED` means the observation is already bound to at least one Atlas gap.",
            "- `NIBIGUIRI:CAUSA_DESCONHECIDA` is the automatic state for an unbound scanner observation.",
            "- `NIBIGUIRI:OBVIO_NAO_INDEXADO` requires a separate formal demonstration and is never inferred from missing binding.",
            "- Priority is an operational triage heuristic, not scientific truth or business value.",
            "- `effort=TOKEN_VAZIO_UNMEASURED` until measured execution data exist.",
            "- No action auto-closes a gap or promotes a claim.",
            "",
            "## R3",
            "",
            f"`F_ok=systematic map produced; actions={summary['actions']}`  ",
            f"`F_gap=unmapped={summary['unmapped']}; p0={summary['blocking_p0']}`  ",
            "`F_next=execute the highest-priority evidence gate under the named authority`",
            "",
        ]
    )
    return "\n".join(lines)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Scan repositories and produce a systematic pragmatic action map."
    )
    parser.add_argument(
        "--root",
        action="append",
        required=True,
        metavar="[NAME=]PATH",
        help="Repository/root to scan. Repeat for multiple roots.",
    )
    parser.add_argument(
        "--atlas",
        type=Path,
        default=repo_root / "data/gap-atlas/RAFAELIA_GAP_ATLAS_V1.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=repo_root / "artifacts/systematic-pragmatic-map",
    )
    parser.add_argument("--exclude", action="append", default=[])
    parser.add_argument("--content-limit", type=int, default=1024 * 1024)
    parser.add_argument("--max-hash-bytes", type=int, default=256 * 1024 * 1024)
    parser.add_argument("--top", type=int, default=50)
    parser.add_argument(
        "--fail-on",
        choices=["none", "p0", "unmapped", "any"],
        default="none",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    excludes = rgm.DEFAULT_EXCLUDES | set(args.exclude)
    roots = [rgm.parse_root(value) for value in args.root]
    all_artifacts: list[rgm.Artifact] = []
    root_stats: dict[str, dict[str, int]] = {}

    try:
        atlas = load_json(args.atlas)
        for spec in roots:
            artifacts, stats = rgm.scan_root(
                spec,
                excludes,
                args.content_limit,
                args.max_hash_bytes,
            )
            all_artifacts.extend(artifacts)
            root_stats[spec.name] = stats
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"systematic-pragmatic-mapper: {exc}", file=sys.stderr)
        return 2

    all_artifacts.sort(key=lambda item: (item.root, item.path))
    gap_map = {
        "schema": rgm.SCHEMA,
        "generated_at": utc_now(),
        "roots": [{"name": root.name, "path": root.path} for root in roots],
        "configuration": {
            "excludes": sorted(excludes),
            "content_limit": args.content_limit,
            "max_hash_bytes": args.max_hash_bytes,
        },
        "root_stats": root_stats,
        "summary": rgm.summarize(all_artifacts),
        "artifacts": [
            {
                "artifact_id": item.artifact_id,
                "root": item.root,
                "path": item.path,
                "size_bytes": item.size_bytes,
                "kind": item.kind,
                "language": item.language,
                "magic": item.magic,
                "sha256": item.sha256,
                "hash_status": item.hash_status,
                "unresolved_markers": item.unresolved_markers,
                "spdx_present": item.spdx_present,
                "build_referenced": item.build_referenced,
                "referenced_by": item.referenced_by,
                "provenance_sidecars": item.provenance_sidecars,
                "gaps": item.gaps,
            }
            for item in all_artifacts
        ],
    }

    actions = build_actions(gap_map, atlas)
    clusters = build_clusters(actions)
    cluster_review = build_cluster_review_queue(clusters)
    generated_at = utc_now()
    action_summary = summarize(actions)
    action_summary.update(pragmatic_filter_stats(gap_map))
    action_summary["clusters"] = len(clusters)
    action_summary["largest_cluster_actions"] = max(
        (cluster["action_count"] for cluster in clusters), default=0
    )
    action_map = {
        "schema": SCHEMA,
        "generated_at": generated_at,
        "claim_allowed": False,
        "source_atlas": str(args.atlas),
        "source_atlas_sha256": canonical_sha256(atlas),
        "source_gap_map_sha256": canonical_sha256(gap_map),
        "flow": [
            "SCAN",
            "BIND",
            "NIBIGUIRI",
            "PRIORIZE",
            "SERVICE",
            "GATE",
            "RECEIPT",
        ],
        "summary": action_summary,
        "clusters": clusters,
        "actions": actions,
    }

    output_dir = args.output_dir
    gap_json = output_dir / "repository_gap_map.json"
    gap_md = output_dir / "repository_gap_map.md"
    map_json = output_dir / "pragmatic_action_map.json"
    map_md = output_dir / "pragmatic_action_map.md"
    review_json = output_dir / "cluster_review_queue.json"
    receipt_json = output_dir / "receipt.json"

    write_json(gap_json, gap_map)
    gap_md.parent.mkdir(parents=True, exist_ok=True)
    gap_md.write_text(rgm.render_markdown(gap_map), encoding="utf-8")
    write_json(map_json, action_map)
    map_md.write_text(render_markdown(action_map, args.top), encoding="utf-8")
    write_json(review_json, cluster_review)

    receipt = {
        "schema": RECEIPT_SCHEMA,
        "generated_at": generated_at,
        "claim_allowed": False,
        "roots": [root.name for root in roots],
        "source_atlas_sha256": action_map["source_atlas_sha256"],
        "source_gap_map_sha256": action_map["source_gap_map_sha256"],
        "pragmatic_action_map_sha256": canonical_sha256(action_map),
        "summary": action_map["summary"],
        "cluster_digest_sha256": canonical_sha256(action_map["clusters"]),
        "cluster_review_digest_sha256": canonical_sha256(cluster_review),
        "g3_state": "REVIEW_REQUIRED" if clusters else "NOT_APPLICABLE",
        "g4_state": "BLOCKED_BY_G3" if clusters else "NOT_APPLICABLE",
        "f_ok": [
            "bounded scan",
            "atlas binding",
            "Nibiguiri classification",
            "deterministic clusters",
            "G3 review queue",
        ],
        "f_gap": [
            "unmapped observations require human/governed binding",
            "effort remains TOKEN_VAZIO until measured",
            "physical/external evidence remains authority-specific",
        ],
        "f_next": "Execute the first applicable highest-priority next_gate and append evidence.",
    }
    write_json(receipt_json, receipt)

    print(json.dumps(action_map["summary"], ensure_ascii=False, sort_keys=True))

    if args.fail_on == "p0" and action_map["summary"]["blocking_p0"]:
        return 1
    if args.fail_on == "unmapped" and action_map["summary"]["unmapped"]:
        return 1
    if args.fail_on == "any" and action_map["summary"]["actions"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
