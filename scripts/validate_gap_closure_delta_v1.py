#!/usr/bin/env python3
import json
import pathlib
import sys

ALLOWED_TOP = {
    "schema", "delta_id", "generated_at", "mode", "claim_allowed",
    "automatic_promotion", "parent_refs", "invariants", "nodes"
}
REQ_NODE = {
    "id", "systems", "role", "state", "closed_now", "open_gaps",
    "next_gate", "promotion_gate", "evidence_refs"
}

def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)

def nonempty_str(v):
    return isinstance(v, str) and bool(v.strip())

def nonempty_str_list(v):
    return isinstance(v, list) and all(nonempty_str(x) for x in v)

def main(path):
    p = pathlib.Path(path)
    try:
        raw = p.read_text(encoding="utf-8")
        data = json.loads(raw)
    except Exception as exc:
        fail(f"load: {exc}")

    if data.get("schema") != "rafaelia.gap-closure-delta.v1":
        fail("schema")
    if data.get("mode") != "APPEND_ONLY_FEDERATED":
        fail("mode")
    if data.get("claim_allowed") is not False:
        fail("claim_allowed must remain false")
    if data.get("automatic_promotion") is not False:
        fail("automatic_promotion must remain false")
    if set(data) - ALLOWED_TOP:
        fail(f"unknown top-level keys: {sorted(set(data)-ALLOWED_TOP)}")
    if not nonempty_str_list(data.get("parent_refs")):
        fail("parent_refs")
    if not nonempty_str_list(data.get("invariants")):
        fail("invariants")

    nodes = data.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        fail("nodes")

    seen = set()
    for i, n in enumerate(nodes):
        if not isinstance(n, dict):
            fail(f"node[{i}] not object")
        missing = REQ_NODE - set(n)
        if missing:
            fail(f"node[{i}] missing {sorted(missing)}")
        unknown = set(n) - REQ_NODE
        if unknown:
            fail(f"node[{i}] unknown {sorted(unknown)}")

        nid = n["id"]
        if not nonempty_str(nid) or nid in seen:
            fail(f"node[{i}] duplicate/empty id")
        seen.add(nid)

        for key in ("systems", "closed_now", "open_gaps", "evidence_refs"):
            if not nonempty_str_list(n[key]):
                fail(f"{nid}.{key}")

        for key in ("role", "state", "next_gate", "promotion_gate"):
            if not nonempty_str(n[key]):
                fail(f"{nid}.{key}")

        if n["open_gaps"] and len(n["next_gate"].strip()) < 20:
            fail(f"{nid}.next_gate too weak")

        promoted_tokens = ("PROVEN", "CLOSED", "VERIFIED", "IMPLEMENTED", "CANONICAL")
        if any(tok in n["state"] for tok in promoted_tokens) and not n["evidence_refs"]:
            fail(f"{nid}.evidence_refs required for promoted state")

        physical_terms = " ".join(n["open_gaps"]).lower()
        if ("physical" in physical_terms or "device" in physical_terms) and "GATED" not in n["state"] and "PARTIAL" not in n["state"]:
            fail(f"{nid}.state must expose physical/device boundary")

    expected = {
        "NOVOEXPORT_RMRCTI_BRIDGE",
        "RAFAELIA_PRIVATE_BODY",
        "RAFGITTOOLS_CONTROL_PLANE",
        "RAFPOLIMATA_EVIDENCE_PRODUCER",
        "TERMUX_PACKAGES_RAFCODEPHI_FACTORY",
        "RAFCODEPHI_ANDROID_RUNTIME",
        "VECTRAS_VM_EXECUTION_SANDBOX",
        "GAIA_EVOLUTION_LAB",
        "MAPA_CANONICAL_INDEX",
        "FEDERATED_TOPOLOGY",
    }
    if seen != expected:
        fail(f"node set mismatch missing={sorted(expected-seen)} extra={sorted(seen-expected)}")

    print(f"PASS schema={data['schema']} nodes={len(nodes)} claim_allowed=false automatic_promotion=false")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <delta.json>", file=sys.stderr)
        raise SystemExit(2)
    main(sys.argv[1])
