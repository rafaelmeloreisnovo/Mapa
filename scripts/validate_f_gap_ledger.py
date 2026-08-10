#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ALLOWED_STATES = {
    "CONFIRMED_SOURCE", "IMPLEMENTED_UNVERIFIED", "UNCERTAINTY",
    "TOKEN_VAZIO", "BLOCKED_SAFETY", "CLOSED"
}
ALLOWED_PRIORITIES = {"P0", "P1", "P2"}
ID_RE = re.compile(r"^FG-\d{3}$")


def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    return 1


def main(path):
    p = Path(path)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"cannot parse {p}: {exc}")

    gaps = data.get("gaps")
    if not isinstance(gaps, list) or not gaps:
        return fail("gaps must be a non-empty list")

    seen = set()
    counts = {"P0": 0, "P1": 0, "P2": 0}
    for i, gap in enumerate(gaps):
        if not isinstance(gap, dict):
            return fail(f"gaps[{i}] is not an object")
        gid = gap.get("id", "")
        if not ID_RE.fullmatch(gid):
            return fail(f"invalid id at index {i}: {gid!r}")
        if gid in seen:
            return fail(f"duplicate id: {gid}")
        seen.add(gid)

        priority = gap.get("priority")
        state = gap.get("state")
        if priority not in ALLOWED_PRIORITIES:
            return fail(f"{gid}: invalid priority {priority!r}")
        if state not in ALLOWED_STATES:
            return fail(f"{gid}: invalid state {state!r}")
        counts[priority] += 1

        for field in ("domain", "gap", "next"):
            if not isinstance(gap.get(field), str) or not gap[field].strip():
                return fail(f"{gid}: missing/non-empty {field}")

        if state == "CLOSED":
            for field in ("evidence", "provenance", "acceptance_test", "receipt"):
                value = gap.get(field)
                if field in ("evidence", "provenance"):
                    if not isinstance(value, list) or not value or not all(isinstance(x, str) and x.strip() for x in value):
                        return fail(f"{gid}: CLOSED requires non-empty {field} list")
                elif not isinstance(value, str) or not value.strip():
                    return fail(f"{gid}: CLOSED requires {field}")

    summary = data.get("summary", {})
    expected = {"total": len(gaps), "p0": counts["P0"], "p1": counts["P1"], "p2": counts["P2"]}
    if summary != expected:
        return fail(f"summary mismatch: got={summary} expected={expected}")

    if data.get("claim_allowed") is not False:
        return fail("claim_allowed must remain false in GOVERNED_PARTIAL ledger")

    print(f"PASS: {p} gaps={len(gaps)} P0={counts['P0']} P1={counts['P1']} P2={counts['P2']} claim_allowed=false")
    return 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "data/governance/f_gap_ledger.v1.json"
    raise SystemExit(main(target))
