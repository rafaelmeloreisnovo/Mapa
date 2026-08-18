#!/usr/bin/env python3
"""Deterministic semantic gate for WILDCHAR / Delta-Manifold routing.

The JSON Schema is structural. This stdlib-only validator enforces the
epistemic invariants that matter operationally: WILDCHAR creates candidates,
not truth; analogy/parabola never becomes literal mechanism implicitly;
TOKEN_VAZIO blocks claim promotion; numeric priority stays uncalibrated;
provenance and falsifiers are mandatory for promotable scientific routes;
and anti-regression events are append-only ordered records.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "rafaelia.wildchar-delta-manifold/v1"
KINDS = {"claim","hypothesis","question","analogy","parabola","counterexample","boundary_case"}
EPISTEMIC = {"FATO","VERIFIED_LIMITED","HIPOTESE","TOKEN_VAZIO","REFUTED","SUPERSEDED"}
PRIORITY = {"P0_CRITICAL","P1_URGENT","P2_NECESSARY","P3_IMPORTANT","P4_BACKLOG"}
ROUTE_ID = re.compile(r"^route:[a-z0-9][a-z0-9._:-]{3,127}$")
REQUIRED_AXES = {
    "concept","evidence","provenance","falsifier_status","gap_unknown",
    "urgency_necessity","next_providence_action",
}
REQUIRED_LENSES = {
    "direct","inverse","boundary","counterexample","analogy_parabola",
    "adjacent_domain_transfer","unknown_unknown",
}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(document: Any) -> tuple[list[str], dict[str, Any]]:
    defects: list[str] = []
    if not isinstance(document, dict):
        return ["document must be an object"], {}

    if document.get("schema_version") != SCHEMA_VERSION:
        defects.append(f"schema_version must equal {SCHEMA_VERSION}")
    if document.get("claim_allowed") is not False:
        defects.append("manifold-level claim_allowed must remain false")

    wild = document.get("wildchar")
    if not isinstance(wild, dict):
        defects.append("wildchar must be an object")
        wild = {}
    if wild.get("N") != "*" or wild.get("cardinality") != "open":
        defects.append("WILDCHAR cardinality must be represented as N='*', cardinality='open'")
    if wild.get("role") != "candidate_space_expansion":
        defects.append("WILDCHAR role must be candidate_space_expansion")
    if wild.get("numeric_weights_state") != "TOKEN_VAZIO_CALIBRATION":
        defects.append("numeric weights must remain TOKEN_VAZIO_CALIBRATION")
    if set(wild.get("lenses", [])) != REQUIRED_LENSES:
        defects.append("wildchar.lenses must contain exactly the seven canonical lenses")

    if set(document.get("axes", [])) != REQUIRED_AXES:
        defects.append("axes must contain exactly the seven canonical manifold axes")
    questions = document.get("route_questions")
    if not isinstance(questions, list) or len(questions) != 7 or not all(_nonempty(q) for q in questions):
        defects.append("route_questions must contain exactly seven non-empty questions")

    routes = document.get("routes")
    if not isinstance(routes, list):
        defects.append("routes must be an array")
        routes = []

    ids: set[str] = set()
    route_by_id: dict[str, dict[str, Any]] = {}
    for index, route in enumerate(routes):
        p = f"routes[{index}]"
        if not isinstance(route, dict):
            defects.append(f"{p} must be an object")
            continue
        rid = route.get("id")
        if not (_nonempty(rid) and ROUTE_ID.fullmatch(rid)):
            defects.append(f"{p}.id is invalid")
            continue
        if rid in ids:
            defects.append(f"duplicate route id: {rid}")
        ids.add(rid)
        route_by_id[rid] = route

        kind = route.get("kind")
        epistemic = route.get("epistemic_state")
        if kind not in KINDS:
            defects.append(f"{p}.kind is invalid")
        if epistemic not in EPISTEMIC:
            defects.append(f"{p}.epistemic_state is invalid")
        if route.get("priority") not in PRIORITY:
            defects.append(f"{p}.priority is invalid")
        if not isinstance(route.get("claim_allowed"), bool):
            defects.append(f"{p}.claim_allowed must be boolean")

        if route.get("origin") == "WILDCHAR" and route.get("claim_allowed") is not False:
            defects.append(f"{p}: WILDCHAR candidates cannot be promoted directly")
        if kind in {"analogy","parabola"}:
            if route.get("literal_claim") is not False:
                defects.append(f"{p}: analogy/parabola requires literal_claim=false")
            if route.get("claim_allowed") is not False:
                defects.append(f"{p}: analogy/parabola cannot carry claim_allowed=true")
        if epistemic in {"TOKEN_VAZIO","HIPOTESE","REFUTED","SUPERSEDED"} and route.get("claim_allowed") is not False:
            defects.append(f"{p}: epistemic state {epistemic} requires claim_allowed=false")

        provenance = route.get("provenance")
        if kind in {"claim","hypothesis","counterexample","boundary_case"}:
            if not isinstance(provenance, list) or not provenance:
                defects.append(f"{p}: scientific route requires provenance")
            if not _nonempty(route.get("falsifier")):
                defects.append(f"{p}: scientific route requires a falsifier")

        token_vazio = route.get("token_vazio")
        if epistemic == "TOKEN_VAZIO":
            if not isinstance(token_vazio, list) or not token_vazio:
                defects.append(f"{p}: TOKEN_VAZIO state requires an explicit token_vazio record")
        if isinstance(token_vazio, list):
            for j, tv in enumerate(token_vazio):
                if not isinstance(tv, dict) or not all(_nonempty(tv.get(k)) for k in ("field","reason","next_test")):
                    defects.append(f"{p}.token_vazio[{j}] requires field, reason and next_test")

        if route.get("claim_allowed") is True:
            if epistemic not in {"FATO","VERIFIED_LIMITED"}:
                defects.append(f"{p}: claim promotion requires FATO or VERIFIED_LIMITED")
            if not route.get("evidence_for"):
                defects.append(f"{p}: claim promotion requires evidence_for")
            if not provenance:
                defects.append(f"{p}: claim promotion requires provenance")
            if not _nonempty(route.get("falsifier")):
                defects.append(f"{p}: claim promotion requires falsifier")

        providence = route.get("F_providencia_operacional", [])
        if not isinstance(providence, list):
            defects.append(f"{p}.F_providencia_operacional must be an array")
        else:
            for j, action in enumerate(providence):
                if not isinstance(action, dict):
                    defects.append(f"{p}.F_providencia_operacional[{j}] must be an object")
                    continue
                if not _nonempty(action.get("action")) or not _nonempty(action.get("verification")):
                    defects.append(f"{p}.F_providencia_operacional[{j}] requires action and verification")

    events = document.get("anti_regression")
    if not isinstance(events, list):
        defects.append("anti_regression must be an array")
        events = []
    seqs: list[int] = []
    for index, event in enumerate(events):
        p = f"anti_regression[{index}]"
        if not isinstance(event, dict):
            defects.append(f"{p} must be an object")
            continue
        seq = event.get("seq")
        if not isinstance(seq, int) or isinstance(seq, bool) or seq < 1:
            defects.append(f"{p}.seq must be a positive integer")
        else:
            seqs.append(seq)
        rid = event.get("route_id")
        if rid not in route_by_id:
            defects.append(f"{p}.route_id references unknown route {rid!r}")
        if not _nonempty(event.get("reason")):
            defects.append(f"{p}.reason must be non-empty")
    if seqs != sorted(seqs) or len(seqs) != len(set(seqs)):
        defects.append("anti_regression seq values must be strictly increasing and unique")

    real_routes = [
        r for r in route_by_id.values()
        if r.get("origin") in {"DIRECT", "IMPORTED"}
        and isinstance(r.get("provenance"), list)
        and r.get("provenance")
    ]
    if defects:
        next_step = "Correct every defect before ingesting or promoting any real route."
    elif real_routes:
        next_step = (
            "Execute the highest-priority open F_next/falsifier on a provenance-bearing real route; "
            "append the result without promoting WILDCHAR-generated candidates."
        )
    else:
        next_step = (
            "Ingest one real route with immutable provenance; keep WILDCHAR-generated candidates "
            "claim_allowed=false until its producer evidence and falsifier close."
        )

    report = {
        "schema_version": SCHEMA_VERSION,
        "manifold_id": document.get("manifold_id"),
        "status": "PASS" if not defects else "FAIL",
        "route_count": len(route_by_id),
        "real_route_count": len(real_routes),
        "wildchar_candidate_count": sum(r.get("origin") == "WILDCHAR" for r in route_by_id.values()),
        "token_vazio_count": sum(r.get("epistemic_state") == "TOKEN_VAZIO" for r in route_by_id.values()),
        "claim_allowed_count": sum(r.get("claim_allowed") is True for r in route_by_id.values()),
        "anti_regression_event_count": len(events),
        "defects": defects,
        "claim_allowed": False,
        "next_verifiable_step": next_step,
    }
    return defects, report


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("manifest", nargs="?", type=Path,
                   default=Path("data/routing/wildchar-delta-manifold.synthetic.v1.json"))
    p.add_argument("--write-report", type=Path)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    document = json.loads(args.manifest.read_text(encoding="utf-8"))
    defects, report = validate(document)
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 1 if defects else 0


if __name__ == "__main__":
    raise SystemExit(main())
