#!/usr/bin/env python3
import json
import sys
from pathlib import Path

EXPECTED_GATES = {
    "source_resolved",
    "authority_resolved",
    "state_resolved",
    "evidence_resolved",
}
EXPECTED_FAIL_CLOSED_FIELDS = {
    "SOURCE",
    "AUTHORITY",
    "EXECUTION_TARGET",
    "EVIDENCE_RULE",
}
ALLOWED_EXPAND = {
    "missing_source",
    "contradiction",
    "unresolved_authority",
    "missing_evidence",
    "explicit_request",
}

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def read_jsonl(path):
    return [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

def fail(message):
    raise SystemExit(message)

def validate_dispatch(manifest_path, routes_path):
    obj = load_json(manifest_path)
    required = {
        "schema_version", "dispatch_version", "canonical_boot", "roots",
        "mu_read", "gates", "fail_closed", "hotstate_policy", "superseded",
        "route_registry", "claim_allowed",
    }
    missing = sorted(required - set(obj))
    if missing:
        fail(f"dispatch: missing {missing}")

    if obj["schema_version"] != "1.0" or obj["dispatch_version"] != "V2.1":
        fail("dispatch: unsupported version")
    if obj["canonical_boot"] != {
        "id": "1T4OIN2RC1I-KFsdaQTCqieeZUGYBXissWrdrZMG0DN8",
        "state": "ACTIVE",
    }:
        fail("dispatch: canonical boot mismatch")
    if obj["claim_allowed"] is not False:
        fail("dispatch: claim_allowed must remain false")

    roots = obj["roots"]
    for name in ("canonical_index", "routes", "ledger", "current_state"):
        if name not in roots or not roots[name].get("id") or roots[name].get("required") is not True:
            fail(f"dispatch: required root invalid: {name}")

    mu = obj["mu_read"]
    if not 1 <= mu.get("default_roots", 0) <= 3:
        fail("dispatch: mu_read default_roots out of budget")
    if mu.get("default_depth") != 1:
        fail("dispatch: mu_read default_depth must be 1")
    expand = set(mu.get("expand_if", []))
    if not expand or not expand <= ALLOWED_EXPAND:
        fail("dispatch: invalid mu_read expansion condition")

    if set(obj["gates"]) != EXPECTED_GATES:
        fail("dispatch: gate set mismatch")

    fc = obj["fail_closed"]
    if set(fc.get("required_fields", [])) != EXPECTED_FAIL_CLOSED_FIELDS:
        fail("dispatch: fail-closed required fields mismatch")
    if fc.get("blocked_state") != "ROUTE_STATE_BLOCKED":
        fail("dispatch: blocked state mismatch")
    if fc.get("token_empty") != "TOKEN_VAZIO":
        fail("dispatch: empty token mismatch")

    hot = obj["hotstate_policy"]
    if hot.get("mode") != "HOTSTATE_O1":
        fail("dispatch: hotstate mode mismatch")
    if not 1 <= hot.get("max_lines", 0) <= 80:
        fail("dispatch: hotstate max_lines out of budget")
    if not 1 <= hot.get("max_active_nodes", 0) <= 3:
        fail("dispatch: hotstate max_active_nodes out of budget")
    if hot.get("history_sink") != "LEDGER_OR_SNAPSHOT":
        fail("dispatch: hotstate history sink mismatch")
    if hot.get("mutation_rule") != "REPLACE_ACTIVE_SNAPSHOT_NOT_APPEND_HISTORY":
        fail("dispatch: hotstate mutation rule mismatch")
    if hot.get("predecessor_required") is not True:
        fail("dispatch: hotstate predecessor must be preserved")

    current_state_id = roots["current_state"]["id"]

    superseded = obj["superseded"]
    old_id = "1l2hhCHYFBouU4qNU-WFY3kqI1wEzfJ64EDvi2iH1mbI"
    if not any(row.get("id") == old_id and row.get("by") == obj["canonical_boot"]["id"] for row in superseded):
        fail("dispatch: START_LITE supersession missing")

    # CURRENT_STATE is an append-only successor chain. Do not require a
    # historical V1 node to point directly at the newest HOTSTATE: V1→V2→V3
    # is valid, while a missing edge or cycle must still fail closed.
    lineage_anchor = "1KHzF3yA8B5RSLiTAGnbJ9lVmEc5rn-l6gOcsdmT5YwQ"
    successor_of = {
        row.get("id"): row.get("by")
        for row in superseded
        if row.get("id") and row.get("by")
    }
    cursor = lineage_anchor
    seen = set()
    while cursor != current_state_id:
        if cursor in seen:
            fail("dispatch: CURRENT_STATE supersession cycle")
        seen.add(cursor)
        nxt = successor_of.get(cursor)
        if not nxt:
            fail("dispatch: CURRENT_STATE predecessor supersession missing")
        cursor = nxt

    routes = read_jsonl(routes_path)
    active = [row for row in routes if row.get("state") != "SUPERSEDED"]
    legacy = [
        row["route_id"]
        for row in active
        if "START_LITE" in row.get("path", [])
    ]
    if legacy:
        fail(f"dispatch: active legacy START_LITE routes: {legacy}")

    default = next((row for row in active if row.get("route_id") == "R0001"), None)
    if default is None:
        fail("dispatch: R0001 missing")
    prefix = default.get("path", [])[:3]
    if prefix != ["CANONICAL_BOOT_V2", "CURRENT_STATE", "INTENT_ACTIVE_NODE"]:
        fail(f"dispatch: R0001 prefix mismatch: {prefix}")

    return {
        "status": "PASS",
        "dispatch_version": obj["dispatch_version"],
        "active_routes": len(active),
        "legacy_active_routes": 0,
        "mu_read_roots": mu["default_roots"],
        "mu_read_depth": mu["default_depth"],
        "hotstate_max_lines": hot["max_lines"],
        "hotstate_max_active_nodes": hot["max_active_nodes"],
        "claim_allowed": False,
    }

def main(argv):
    if len(argv) != 3:
        fail("usage: validate_manifold_dispatch.py DISPATCH.json ROUTES.jsonl")
    print(json.dumps(validate_dispatch(argv[1], argv[2]), sort_keys=True))

if __name__ == "__main__":
    main(sys.argv)
