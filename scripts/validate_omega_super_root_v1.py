#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def load(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def fail(reason):
    print(json.dumps({"status": "FAIL", "reason": reason}, ensure_ascii=False))
    raise SystemExit(1)


def main():
    root_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    root = load(root_dir / "data/knowledge/RAFAELIA_OMEGA_SUPER_ROOT.v1.json")
    registry = load(root_dir / "data/knowledge/RAFAELIA_OMEGA_UNIVERSAL_REGISTRY.v1.json")
    route_registry = load(root_dir / "data/knowledge/RAFAELIA_CONTEXT_ROUTES.v1.json")
    delta = load(root_dir / "data/governance/RAFAELIA_PR243_STATE_DELTA_20260814.v1.json")

    if root.get("claim_allowed") is not False:
        fail("super-root must remain claim_allowed=false")
    if registry.get("claim_allowed") is not False or route_registry.get("claim_allowed") is not False:
        fail("registries must remain claim_allowed=false")

    nodes = registry.get("nodes", [])
    node_ids = [n.get("omega_id") for n in nodes]
    if len(node_ids) != len(set(node_ids)):
        fail("duplicate omega_id")
    known_nodes = set(node_ids)
    if "OMEGA-NODE-SUPER-ROOT-V1" not in known_nodes:
        fail("super-root universal node missing")

    routes = route_registry.get("routes", [])
    route_ids = [r.get("route_id") for r in routes]
    if len(route_ids) != len(set(route_ids)):
        fail("duplicate route_id")
    known_routes = set(route_ids)
    if set(root.get("route_ids", [])) != known_routes:
        fail("root route_ids differ from route registry")

    for route in routes:
        rid = route["route_id"]
        policy = route.get("read_policy", {})
        if policy.get("default_mode") != "READ_ONLY":
            fail(f"{rid}: default mode must be READ_ONLY")
        if policy.get("open_minimum_subgraph") is not True:
            fail(f"{rid}: minimum-subgraph invariant disabled")
        if policy.get("historical_state_is_current") is not False:
            fail(f"{rid}: historical state cannot be current")
        if route.get("state", {}).get("claim_allowed") is not False:
            fail(f"{rid}: route claim gate must remain false")
        refs = set(route.get("entry_node_ids", []) + route.get("required_node_ids", []) + route.get("optional_node_ids", []))
        missing = sorted(refs - known_nodes)
        if missing:
            fail(f"{rid}: unknown node refs {missing}")

    for mount in root.get("mounts", []):
        if mount.get("node_id") not in known_nodes:
            fail(f"mount references unknown node {mount.get('node_id')}")
        if mount.get("mode") not in {"READ_ONLY", "REFERENCE_ONLY"}:
            fail(f"unsafe mount mode {mount.get('mode')}")

    for node in nodes:
        if node.get("state", {}).get("claim_allowed") is not False:
            fail(f"{node.get('omega_id')}: node claim gate must remain false")
        for route_id in node.get("recovery_routes", []):
            if route_id not in known_routes:
                fail(f"{node.get('omega_id')}: unknown recovery route {route_id}")
        for gap in node.get("gaps", []):
            if not str(gap.get("token", "")).startswith("TOKEN_VAZIO"):
                fail(f"{node.get('omega_id')}: gap is not TOKEN_VAZIO typed")
            if not gap.get("next_gate"):
                fail(f"{node.get('omega_id')}: gap lacks next_gate")

    if delta.get("current_provider", {}).get("merged") is not True:
        fail("PR243 current provider state must preserve merged=true")
    if delta.get("historical_snapshot", {}).get("state_class") != "HISTORICAL_SNAPSHOT":
        fail("PR243 old Drive state must stay historical")
    if "WITHOUT_ERASING" not in delta.get("relation", ""):
        fail("state reconciliation must preserve historical state")

    print(json.dumps({
        "status": "PASS_LIMITED",
        "claim_allowed": False,
        "nodes": len(nodes),
        "routes": len(routes),
        "mounts": len(root.get("mounts", [])),
        "checks": [
            "unique node IDs",
            "route references",
            "read-only/minimum-subgraph policy",
            "mount references",
            "typed TOKEN_VAZIO + next_gate",
            "claim gate",
            "PR243 current-vs-historical separation"
        ],
        "limitations": [
            "not a global coverage proof",
            "not a Termux/device/CI execution receipt",
            "does not validate external sources beyond recorded provider observations"
        ]
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
