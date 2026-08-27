#!/usr/bin/env python3
"""Fail-closed semantic validator for RAFAELIA F_next Continuous Evolution V1.

Stdlib only. This validator does not attest legal compliance or runtime truth; it checks
that the control-plane chain preserves urgency/evidence separation, risk-vector integrity,
provenance, falsifiers, dependency references and bounded claim promotion.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data/control-plane/legal-gnss/F_NEXT_CONTINUOUS_EVOLUTION_20260826.v1.json"

RISK_KEYS = {"A", "S", "P", "G", "I", "V", "C", "U"}
RISK_STATES = {"CONTROLLED", "WATCH", "P1", "P0", "NOT_APPLICABLE_WITH_EVIDENCE", "TOKEN_VAZIO"}
STATES = {"READY", "ACTIVE", "WAITING_EXTERNAL_RUNTIME", "BLOCKED", "TOKEN_VAZIO", "CLOSED_PASS", "CLOSED_FAIL", "SUPERSEDED"}
PRIORITIES = {"P0", "P1", "P2", "P3"}
URGENCIES = {"NOW", "NEXT", "SCHEDULED", "DEFERRED"}
CLAIMS = ["OBSERVATION", "EVIDENCED_OBSERVATION", "BOUNDED_CLAIM", "PRECISE_CLAIM", "GENERAL_CLAIM"]
CLAIM_TARGETS = set(CLAIMS) | {"NONE"}


def fail(msg: str) -> None:
    raise ValueError(msg)


def validate(doc: dict) -> None:
    if doc.get("schema_version") != "rafaelia.f-next-continuous-evolution/v1":
        fail("bad schema_version")
    if doc.get("append_only") is not True:
        fail("append_only must be true")
    if doc.get("claim_allowed") is not False:
        fail("chain-level claim_allowed must remain false")
    if doc.get("claim_ladder") != CLAIMS:
        fail("claim_ladder must preserve canonical order")
    inv = set(doc.get("mother_invariants", []))
    required_inv = {
        "urgency != permission_to_promote_evidence",
        "TOKEN_VAZIO != zero != false",
        "claim_precision cannot exceed evidence precision",
    }
    if not required_inv.issubset(inv):
        fail("missing mother invariant")

    stages = doc.get("stages")
    if not isinstance(stages, list) or not stages:
        fail("stages missing")
    ids = [s.get("id") for s in stages]
    if any(not isinstance(x, str) or not x.startswith("FN-") for x in ids):
        fail("invalid stage id")
    if len(ids) != len(set(ids)):
        fail("duplicate stage id")
    orders = [s.get("order") for s in stages]
    if orders != sorted(orders) or len(orders) != len(set(orders)):
        fail("stage order must be unique and monotonic")
    known_ids = set(ids)

    for s in stages:
        sid = s["id"]
        if s.get("state") not in STATES:
            fail(f"{sid}: invalid state")
        if s.get("priority") not in PRIORITIES:
            fail(f"{sid}: invalid priority")
        if s.get("urgency") not in URGENCIES:
            fail(f"{sid}: invalid urgency")
        rv = s.get("risk_vector")
        if not isinstance(rv, dict) or set(rv) != RISK_KEYS:
            fail(f"{sid}: risk vector must be R=(A,S,P,G,I,V,C,U)")
        if any(v not in RISK_STATES for v in rv.values()):
            fail(f"{sid}: invalid risk state")
        if "P0" in rv.values() and s.get("state") == "CLOSED_PASS":
            fail(f"{sid}: non-compensatory P0 cannot be CLOSED_PASS")
        for field in ("provenance", "required_evidence", "mitigations", "forbidden_promotions"):
            value = s.get(field)
            if not isinstance(value, list) or not value or any(not str(x).strip() for x in value):
                fail(f"{sid}: {field} must be non-empty")
        if not str(s.get("falsifier", "")).strip():
            fail(f"{sid}: falsifier missing")
        if not str(s.get("closure_condition", "")).strip():
            fail(f"{sid}: closure condition missing")
        deps = s.get("dependencies")
        if not isinstance(deps, list) or any(d not in known_ids for d in deps):
            fail(f"{sid}: unknown dependency")
        if sid in deps:
            fail(f"{sid}: self dependency")
        if s.get("claim_target") not in CLAIM_TARGETS:
            fail(f"{sid}: invalid claim target")
        if s.get("claim_target") == "GENERAL_CLAIM":
            fail(f"{sid}: GENERAL_CLAIM forbidden in this chain")
        for edge in ("next_on_pass", "next_on_fail"):
            target = s.get(edge)
            if target is not None and target not in known_ids:
                fail(f"{sid}: {edge} points outside chain")
        if s.get("state") == "WAITING_EXTERNAL_RUNTIME" and "RUNTIME" not in (s.get("scope", "") + " " + s.get("problem", "")).upper():
            fail(f"{sid}: external runtime state must name runtime boundary")

    loop = doc.get("continuous_loop") or {}
    every = loop.get("on_every_transition")
    if not isinstance(every, list) or len(every) < 4:
        fail("continuous loop transition checks missing")
    selection = str(loop.get("selection_rule", ""))
    promotion = str(loop.get("promotion_rule", ""))
    regression = str(loop.get("regression_rule", ""))
    if "urgency" not in selection.lower() or "never" not in selection.lower():
        fail("selection rule must prevent urgency from changing evidence state")
    if "GENERAL_CLAIM" not in promotion:
        fail("promotion rule must explicitly bound GENERAL_CLAIM")
    if "append-only" not in regression.lower() and "append_only" not in regression.lower():
        fail("regression rule must be append-only")


def self_test(doc: dict) -> None:
    validate(doc)
    cases = []

    x = copy.deepcopy(doc); x["claim_allowed"] = True
    cases.append(("claim promotion at chain level", x))

    x = copy.deepcopy(doc); x["stages"][1]["risk_vector"]["P"] = "P0"; x["stages"][1]["state"] = "CLOSED_PASS"
    cases.append(("P0 closed pass", x))

    x = copy.deepcopy(doc); x["stages"][2]["provenance"] = []
    cases.append(("missing provenance", x))

    x = copy.deepcopy(doc); x["stages"][6]["claim_target"] = "GENERAL_CLAIM"
    cases.append(("unsupported general claim", x))

    x = copy.deepcopy(doc); x["continuous_loop"]["selection_rule"] = "urgency decides everything"
    cases.append(("urgency overrides evidence", x))

    x = copy.deepcopy(doc); x["stages"][3]["dependencies"] = ["FN-DOES-NOT-EXIST"]
    cases.append(("unknown dependency", x))

    for name, bad in cases:
        try:
            validate(bad)
        except ValueError:
            continue
        fail(f"negative self-test unexpectedly passed: {name}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default=str(DEFAULT))
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    with open(args.path, encoding="utf-8") as fh:
        doc = json.load(fh)
    validate(doc)
    if args.self_test:
        self_test(doc)
    print("PASS: F_next continuous evolution chain is structurally fail-closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
