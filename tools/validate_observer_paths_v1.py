#!/usr/bin/env python3
"""Fail-closed synthetic observer/uncertainty graph routing validator.

This does NOT certify real observers, cause, provider enforcement or review.
Real observations must use the existing RAFAELIA provenance/receipt gates.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

FIXTURES = Path(__file__).resolve().parents[1] / "data/observations/observer-paths-synthetic.v1.json"
SCHEMA = "rafaelia.observer-paths-synthetic/v1"
KINDS = {
    "OBSERVATION_CANDIDATE", "HYPOTHESIS", "CONTRADICTION",
    "CORRECTION_CANDIDATE", "GRAPH_FORK", "TEMPORAL_GAP",
    "REFUSAL", "LATE_SIGNAL",
}
STATES = {"UNVERIFIED", "TOKEN_VAZIO", "CONTRADICTION", "HOLD"}
LINKS = {"BRANCHES_FROM", "CONTRADICTS", "SUPERSEDES", "PARALLEL_WITH", "FOLLOWS", "BLOCKED_BY", "CAUSE_CANDIDATE"}
MODALITIES = {"VERBAL", "NONVERBAL", "UNDETERMINED"}


def iso_time(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != SCHEMA or data.get("state") != "SYNTHETIC_ROUTING_FIXTURES_ONLY":
        errors.append("INVALID_SYNTHETIC_SCHEMA")
    if data.get("claim_allowed") is not False:
        errors.append("GLOBAL_CLAIM_MUST_REMAIN_FALSE")
    if data.get("gates", {}).get("promotion") != "HOLD":
        errors.append("PROMOTION_MUST_REMAIN_HOLD")

    areas = data.get("approved_conduct_areas")
    markers = data.get("approved_uncertainty_markers")
    if not isinstance(areas, list) or len(areas) != 12 or len(set(areas)) != len(areas):
        errors.append("AREA_VOCABULARY_INVALID")
        areas = []
    if not isinstance(markers, list) or len(markers) < 10 or len(set(markers)) != len(markers):
        errors.append("UNCERTAINTY_MARKER_VOCABULARY_INVALID")
        markers = []
    events = data.get("events")
    if not isinstance(events, list) or len(events) != 8:
        errors.append("EIGHT_SYNTHETIC_EVENTS_REQUIRED")
        events = []

    seen: set[str] = set()
    used_areas: set[str] = set()
    used_markers: set[str] = set()
    for index, item in enumerate(events, 1):
        prefix = f"event[{index}]"
        if not isinstance(item, dict):
            errors.append(prefix + ":NOT_OBJECT")
            continue
        ident = item.get("event_id")
        if not isinstance(ident, str) or not ident or ident in seen:
            errors.append(prefix + ":DUPLICATE_OR_INVALID_ID")
        if item.get("sequence") != index:
            errors.append(prefix + ":SEQUENCE_DRIFT")
        if not iso_time(item.get("observed_at")):
            errors.append(prefix + ":OBSERVATION_TIME_MISSING")
        tags = item.get("uncertainty_markers")
        if not isinstance(tags, list) or not tags or any(t not in markers for t in tags):
            errors.append(prefix + ":MARKERS_INVALID")
            tags = []
        if len(tags) != len(set(tags)):
            errors.append(prefix + ":DUPLICATE_MARKER")
        used_markers.update(tags)
        if item.get("effective_at") is None:
            if "ATEMPORAL" not in tags:
                errors.append(prefix + ":UNKNOWN_EFFECTIVE_TIME_UNTYPED")
        elif not iso_time(item.get("effective_at")):
            errors.append(prefix + ":EFFECTIVE_TIME_INVALID")
        conduct = item.get("conduct_areas")
        if not isinstance(conduct, list) or not conduct or any(a not in areas for a in conduct):
            errors.append(prefix + ":CONDUCT_INVALID")
            conduct = []
        used_areas.update(conduct)
        obs = item.get("observer")
        if not isinstance(obs, dict) or obs.get("mode") != "SYNTHETIC" or obs.get("authority_state") != "NOT_A_REAL_REVIEWER" or not str(obs.get("id", "")).startswith("SYNTH-"):
            errors.append(prefix + ":SYNTHETIC_OBSERVER_AUTHORITY_INVALID")
        source = item.get("source")
        if not isinstance(source, dict) or source.get("system") != "SYNTHETIC_FIXTURE" or not str(source.get("locator", "")).startswith("fixture://") or source.get("content_sha256_state") != "TOKEN_VAZIO_NO_EXTERNAL_SOURCE_BYTES":
            errors.append(prefix + ":REAL_PROVENANCE_FABRICATION_OR_MISSING_FIXTURE")
        if item.get("evidence_refs") != [] or item.get("receipt_state") != "NOT_RUN_REAL_WORLD":
            errors.append(prefix + ":REAL_EVIDENCE_MUST_NOT_BE_CLAIMED")
        if item.get("claim_allowed") is not False:
            errors.append(prefix + ":EVENT_CLAIM_MUST_REMAIN_FALSE")
        if item.get("epistemic_state") not in STATES or item.get("event_kind") not in KINDS:
            errors.append(prefix + ":INVALID_EPISTEMIC_STATE_OR_KIND")
        if item.get("modality") not in MODALITIES:
            errors.append(prefix + ":INVALID_MODALITY")
        if "VERBAL" in tags and item.get("modality") != "VERBAL":
            errors.append(prefix + ":VERBAL_MODALITY_LOSS")
        if "NONVERBAL" in tags and item.get("modality") != "NONVERBAL":
            errors.append(prefix + ":NONVERBAL_MODALITY_LOSS")
        if item.get("epistemic_state") == "TOKEN_VAZIO" and "TOKEN_VAZIO" not in tags:
            errors.append(prefix + ":UNTYPED_EPISTEMIC_VOID")
        if not isinstance(item.get("gap_reason"), str) or len(item["gap_reason"].strip()) < 8:
            errors.append(prefix + ":GAP_REASON_MISSING")
        if not isinstance(item.get("falsifier"), str) or len(item["falsifier"].strip()) < 12 or not isinstance(item.get("next_gate"), str) or not item["next_gate"]:
            errors.append(prefix + ":FALSIFIER_OR_GATE_MISSING")
        if item.get("event_kind") == "REFUSAL" and item.get("epistemic_state") != "HOLD":
            errors.append(prefix + ":REFUSAL_CANNOT_AUTO_APPROVE")
        edges = item.get("links")
        if not isinstance(edges, list):
            errors.append(prefix + ":EDGES_INVALID")
            edges = []
        edge_keys: set[tuple[str, str]] = set()
        for edge in edges:
            if not isinstance(edge, dict):
                errors.append(prefix + ":EDGE_NOT_OBJECT")
                continue
            target, kind = edge.get("to"), edge.get("type")
            if target not in seen or target == ident or kind not in LINKS:
                errors.append(prefix + ":DANGLING_FORWARD_OR_INVALID_EDGE")
            if (target, kind) in edge_keys:
                errors.append(prefix + ":DUPLICATE_EDGE")
            edge_keys.add((target, kind))
            if kind == "SUPERSEDES" and item.get("event_kind") != "CORRECTION_CANDIDATE":
                errors.append(prefix + ":SILENT_OR_UNJUSTIFIED_SUPERSESSION")
            if kind == "CONTRADICTS" and item.get("epistemic_state") != "CONTRADICTION":
                errors.append(prefix + ":CONTRADICTION_NOT_PRESERVED")
            if kind == "CAUSE_CANDIDATE" and item.get("claim_allowed") is not False:
                errors.append(prefix + ":CAUSAL_PROMOTION_FORBIDDEN")
        if isinstance(ident, str):
            seen.add(ident)
    if set(areas) - used_areas:
        errors.append("UNTESTED_CONDUCT_AREAS:" + ",".join(sorted(set(areas) - used_areas)))
    if set(markers) - used_markers:
        errors.append("UNTESTED_UNCERTAINTY_MARKERS:" + ",".join(sorted(set(markers) - used_markers)))
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", type=Path, default=FIXTURES)
    args = ap.parse_args()
    try:
        data = json.loads(args.fixtures.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("nonobject fixture root")
        errors = validate(data)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = ["FIXTURE_READ_OR_PARSE_ERROR:" + str(exc)]
    report = {"schema": "rafaelia.observer-path-fixtures-validation/v1",
              "state": "FAIL" if errors else "PASS",
              "scope": "SYNTHETIC_ONLY_NO_PROMOTION",
              "claim_allowed": False, "errors": errors}
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
