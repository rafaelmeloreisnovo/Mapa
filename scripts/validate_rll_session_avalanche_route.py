"""Validate the pointer-only RLL session Avalanche route."""
from __future__ import annotations
import json
import re
from pathlib import Path

SHA40 = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_ROLES = {
    "SOURCE_AUTHORITY", "ORCHESTRATION_AUTHORITY",
    "GOVERNANCE_AUTHORITY", "POINTER_ONLY"
}


def validate(route: dict) -> list[str]:
    errors: list[str] = []
    if route.get("state") != "ACTIVE_POINTER_ROUTE":
        errors.append("bad state")
    nodes = route.get("nodes", [])
    node_ids = [node.get("id") for node in nodes]
    if len(node_ids) != len(set(node_ids)):
        errors.append("duplicate node ids")
    if {node.get("role") for node in nodes} != REQUIRED_ROLES:
        errors.append("roles incomplete")
    known = set(node_ids)
    for node in nodes:
        if not node.get("repository") or not node.get("artifacts"):
            errors.append(f"{node.get('id')}: incomplete")
        if node.get("role") == "POINTER_ONLY":
            if node.get("commit") != "SELF_AFTER_MERGE":
                errors.append("map self ref must be deferred")
        elif not SHA40.fullmatch(str(node.get("commit", ""))):
            errors.append(f"{node.get('id')}: unpinned commit")
    for edge in route.get("edges", []):
        if edge.get("from") not in known or edge.get("to") not in known:
            errors.append("dangling edge")
        if edge.get("from") == edge.get("to"):
            errors.append("self edge")
    invariants = route.get("invariants", {})
    for key in (
        "map_is_source_authority", "private_payload_copied",
        "automatic_cross_repo_write", "automatic_merge", "claim_allowed"
    ):
        if invariants.get(key) is not False:
            errors.append(f"{key} must be false")
    if invariants.get("pinned_external_commits_required") is not True:
        errors.append("pins required")
    if any(
        node.get("role") == "POINTER_ONLY"
        and node.get("repository") != "rafaelmeloreisnovo/Mapa"
        for node in nodes
    ):
        errors.append("pointer owner")
    return errors


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", nargs="?",
        default="data/federation/rll-session-avalanche-route-v1.json"
    )
    args = parser.parse_args()
    errors = validate(load(args.path))
    if errors:
        raise SystemExit("INVALID: " + "; ".join(errors))
    print("PASS: pointer-only route valid")
