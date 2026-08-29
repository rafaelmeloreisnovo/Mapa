#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

DEFAULT_PATH = Path("data/reconciliation/OMEGA_OPERATIONAL_WORK_LEDGER_20260829.v1.json")
SHA40 = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_FRONT = {
    "id",
    "repository",
    "authority",
    "status",
    "evidence",
    "open_gates",
    "falsifier",
    "next_verifiable_step",
}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def nonempty_text(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH
    data = json.loads(path.read_text(encoding="utf-8"))

    if data.get("schema") != "rafaelia.omega-operational-work-ledger.v1":
        fail("unexpected schema")
    if data.get("claim_allowed") is not False:
        fail("claim_allowed must remain false")
    if data.get("release_allowed") is not False:
        fail("release_allowed must remain false while runtime gates are open")
    if data.get("promotion_allowed") is not False:
        fail("promotion_allowed must remain false while TOKEN_VAZIO remains")
    if data.get("state") != "DELIVERED_WITH_OPEN_RUNTIME_GATES":
        fail("unexpected top-level state")

    invariants = data.get("invariants")
    required_invariants = {
        "VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM",
        "TOKEN_VAZIO != PASS",
        "CI_BUILD != PHYSICAL_ANDROID_RUNTIME",
        "DRIVE_NEWER != OVERWRITE",
        "IMPLEMENTATION != SCIENTIFIC_VALIDATION",
    }
    if not isinstance(invariants, list) or not required_invariants.issubset(set(invariants)):
        fail("required anti-promotion invariants missing")

    fronts = data.get("observed_fronts")
    if not isinstance(fronts, list) or not fronts:
        fail("observed_fronts must be a non-empty list")

    seen = set()
    token_vazio_fronts = 0
    for i, front in enumerate(fronts):
        if not isinstance(front, dict):
            fail(f"front {i} must be an object")
        missing = sorted(REQUIRED_FRONT - set(front))
        if missing:
            fail(f"front {i} missing fields: {missing}")

        ident = front["id"]
        if not nonempty_text(ident):
            fail(f"front {i} has empty id")
        if ident in seen:
            fail(f"duplicate front id: {ident}")
        seen.add(ident)

        for field in ("repository", "authority", "status", "falsifier", "next_verifiable_step"):
            if not nonempty_text(front[field]):
                fail(f"{ident}: empty {field}")

        evidence = front["evidence"]
        if not isinstance(evidence, list) or not evidence or not all(nonempty_text(x) for x in evidence):
            fail(f"{ident}: evidence must be a non-empty string list")

        gates = front["open_gates"]
        if not isinstance(gates, list) or not gates or not all(nonempty_text(x) for x in gates):
            fail(f"{ident}: open_gates must be a non-empty string list")
        serialized_gates = " ".join(gates)
        has_typed_gap = "TOKEN_VAZIO" in serialized_gates or "TV-" in serialized_gates
        if not has_typed_gap:
            fail(f"{ident}: open gates are not typed as TOKEN_VAZIO/TV")
        token_vazio_fronts += 1

        observed_head = front.get("observed_head")
        if observed_head is not None and not SHA40.fullmatch(observed_head):
            fail(f"{ident}: observed_head must be an exact 40-hex commit SHA")

        if front.get("claim_allowed") is True:
            fail(f"{ident}: front-level claim_allowed=true is forbidden")

        forbidden_statuses = {"PASS", "CLOSED", "RELEASED", "PROVEN_COMPLETE"}
        if front["status"] in forbidden_statuses:
            fail(f"{ident}: open gates cannot coexist with status={front['status']}")

    priorities = data.get("priority_order")
    if not isinstance(priorities, list) or len(priorities) != len(fronts):
        fail("priority_order must have one entry per observed front")
    if not all(nonempty_text(x) for x in priorities):
        fail("priority_order contains empty entries")

    anti = data.get("anti_regression")
    required_true = {
        "do_not_close_from_inference",
        "append_only_successors",
        "require_exact_source_pointer",
        "require_falsifier_or_failure_condition",
        "require_next_verifiable_step",
    }
    if not isinstance(anti, dict):
        fail("anti_regression must be an object")
    for key in required_true:
        if anti.get(key) is not True:
            fail(f"anti_regression.{key} must be true")

    print(
        "PASS "
        f"fronts={len(fronts)} "
        f"typed_gap_fronts={token_vazio_fronts} "
        "claim_allowed=false release_allowed=false promotion_allowed=false"
    )


if __name__ == "__main__":
    main()
