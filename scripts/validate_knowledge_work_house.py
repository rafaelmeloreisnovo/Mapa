#!/usr/bin/env python3
import json
import sys
from pathlib import Path

VALID_STATES = {
    "DRAFT","TOKEN_VAZIO","BLOCKED","CONTRADICTION",
    "VERIFIED_LIMITED","REPRODUCED","ROLLBACK_READY","CLOSED"
}

def validate_unit(u):
    errors = []
    required = [
        "id","intent","authority","sources","context","evidence",
        "contradictions","uncertainty","reproduction","rollback",
        "reconstructibility","state","claim_allowed","next"
    ]
    for key in required:
        if key not in u:
            errors.append(f"missing:{key}")

    if errors:
        return errors

    if not u["sources"]:
        errors.append("provenance:sources_empty")

    ctx = u["context"]
    for key in ("scope","boundary","observed_at"):
        if not ctx.get(key):
            errors.append(f"context:missing_{key}")

    if u["state"] not in VALID_STATES:
        errors.append("state:invalid")

    open_contradictions = [
        c for c in u["contradictions"] if c.get("state") == "OPEN"
    ]

    rep = u["reproduction"]
    rb = u["rollback"]
    rec = u["reconstructibility"]

    reconstructible = (
        rec.get("status") == "PASS"
        and rec.get("inputs_pinned") is True
        and rec.get("versions_pinned") is True
        and rec.get("outputs_identified") is True
    )

    promotable = (
        bool(u["sources"])
        and bool(u["evidence"])
        and not open_contradictions
        and rep.get("status") == "PASS"
        and bool(rep.get("procedure"))
        and rb.get("ready") is True
        and bool(rb.get("predecessor"))
        and reconstructible
    )

    if u["claim_allowed"] and not promotable:
        errors.append("claim_gate:promotion_without_all_guards")

    if u["state"] in {"REPRODUCED","CLOSED"} and rep.get("status") != "PASS":
        errors.append("reproduction:state_requires_pass")

    if u["state"] == "CLOSED" and not reconstructible:
        errors.append("reconstructibility:closed_requires_pass")

    if any(x.get("state") in {"TOKEN_VAZIO","BLOCKED","PARTIAL"} for x in u["uncertainty"]) and u["claim_allowed"]:
        errors.append("uncertainty:unresolved_but_claim_allowed")

    return errors

def main():
    if len(sys.argv) != 2:
        print("usage: validate_knowledge_work_house.py UNIT.json", file=sys.stderr)
        return 2
    p = Path(sys.argv[1])
    data = json.loads(p.read_text(encoding="utf-8"))
    units = data if isinstance(data, list) else [data]
    all_errors = []
    for i, unit in enumerate(units):
        errs = validate_unit(unit)
        all_errors.extend([f"{i}:{e}" for e in errs])
    if all_errors:
        print(json.dumps({"status":"FAIL","errors":all_errors}, indent=2))
        return 1
    print(json.dumps({"status":"PASS","units":len(units)}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
