#!/usr/bin/env python3
"""Fail-closed validator for the declared six-repository federation topology."""

import json
import sys
from pathlib import Path


def load_lineage_authority(repo_root="."):
    path = Path(repo_root) / "data" / "control-plane" / "lineage_authority_v1.json"
    if not path.exists():
        print(f"ERROR: lineage_authority_v1.json not found at {path}")
        return None
    with open(path) as f:
        return json.load(f)


def validate_repo_count(authority, expected_count):
    repos = authority.get("cross_repo_validation", {}).get("repos", [])
    if len(repos) != expected_count:
        print(f"ERROR: Expected {expected_count} repos, found {len(repos)}")
        return False
    print(f"✓ Repository count valid ({len(repos)} repos)")
    return True


def validate_role_non_overlap(authority):
    pyramid = authority.get("authority_pyramid", {})
    roles = {}
    for repo, spec in pyramid.items():
        role = spec.get("role")
        if not role:
            print(f"ERROR: {repo} has no role")
            return False
        if role in roles:
            print(f"ERROR: Role '{role}' assigned to both {repo} and {roles[role]}")
            return False
        roles[role] = repo
    print(f"✓ Role non-overlap validated ({len(roles)} distinct roles)")
    return True


def validate_responsibility_coverage(authority):
    pyramid = authority.get("authority_pyramid", {})
    required_domains = {
        "source": False,
        "build": False,
        "compiler": False,
        "version": False,
        "federation": False,
        "model": False,
    }
    for spec in pyramid.values():
        responsibilities = spec.get("responsibility", [])
        role = spec.get("role", "").lower()
        text = (" ".join(responsibilities) + " " + role).lower()
        if "source" in text or "verification" in text:
            required_domains["source"] = True
        if "build" in text or "compilation" in text:
            required_domains["build"] = True
        if "compiler" in text:
            required_domains["compiler"] = True
        if any(k in text for k in ("version", "commit", "versioning", "branch")):
            required_domains["version"] = True
        if any(k in text for k in ("federation", "validation", "routing")):
            required_domains["federation"] = True
        if any(k in text for k in ("model", "semantic", "inference", "authority")):
            required_domains["model"] = True
    missing = sorted(k for k, covered in required_domains.items() if not covered)
    if missing:
        print(f"ERROR: Responsibility coverage incomplete: {', '.join(missing)}")
        return False
    print("✓ Responsibility coverage validated (6 domains)")
    return True


def validate_immutable_id_schema(authority):
    for repo, spec in authority.get("authority_pyramid", {}).items():
        if spec.get("immutable_id_type") != "lineage_id":
            print(f"ERROR: {repo} does not use immutable_id_type='lineage_id'")
            return False
    print("✓ Immutable ID schema validated (all repos)")
    return True


def validate_independence_claims(authority):
    for repo, spec in authority.get("authority_pyramid", {}).items():
        claim = spec.get("independence_claim")
        if not isinstance(claim, str) or not claim.strip():
            print(f"ERROR: {repo} has empty independence_claim")
            return False
    print("✓ Independence claims validated (all repos)")
    return True


def validate_dedup_enforcement(authority):
    rules = authority.get("dedup_rules", [])
    by_class = {r.get("class"): r for r in rules}
    for klass in ("identical_artifact", "upstream_sync"):
        rule = by_class.get(klass)
        if not rule or rule.get("is_independent") is not False:
            print(f"ERROR: {klass} must be explicitly non-independent")
            return False
    print("✓ Dedup enforcement validated")
    return True


def validate_topology_cycle_safety(authority):
    """Validate declared dependency edges, weak connectivity, and acyclicity.

    This is deliberately fail-closed. Missing/malformed edges are not a PASS.
    A real cycle is a falsifier and must return False.
    """
    cfg = authority.get("cross_repo_validation", {})
    repos = cfg.get("repos", [])
    edges = cfg.get("dependency_edges")
    repo_set = set(repos)

    if not repos:
        print("ERROR: No repositories declared")
        return False
    if not isinstance(edges, list) or not edges:
        print("ERROR: dependency_edges missing or empty; acyclicity is TOKEN_VAZIO")
        return False

    adjacency = {repo: [] for repo in repos}
    undirected = {repo: set() for repo in repos}
    seen_edges = set()

    for raw in edges:
        if not isinstance(raw, list) or len(raw) != 2:
            print(f"ERROR: malformed dependency edge: {raw!r}")
            return False
        src, dst = raw
        if src not in repo_set or dst not in repo_set:
            print(f"ERROR: dependency edge references undeclared repo: {src!r}->{dst!r}")
            return False
        if src == dst:
            print(f"ERROR: self-cycle detected: {src}")
            return False
        edge = (src, dst)
        if edge in seen_edges:
            print(f"ERROR: duplicate dependency edge: {src}->{dst}")
            return False
        seen_edges.add(edge)
        adjacency[src].append(dst)
        undirected[src].add(dst)
        undirected[dst].add(src)

    # Weak connectivity: every declared repo must belong to the same authority graph.
    reached = set()
    stack = [repos[0]]
    while stack:
        node = stack.pop()
        if node in reached:
            continue
        reached.add(node)
        stack.extend(undirected[node] - reached)
    if reached != repo_set:
        missing = sorted(repo_set - reached)
        print(f"ERROR: disconnected repositories: {', '.join(missing)}")
        return False

    # DFS three-color cycle detector over the actual declared directed edges.
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {repo: WHITE for repo in repos}
    path = []

    def visit(node):
        color[node] = GRAY
        path.append(node)
        for nxt in adjacency[node]:
            if color[nxt] == GRAY:
                cycle_start = path.index(nxt)
                cycle = path[cycle_start:] + [nxt]
                print("ERROR: dependency cycle detected: " + " -> ".join(cycle))
                return False
            if color[nxt] == WHITE and not visit(nxt):
                return False
        path.pop()
        color[node] = BLACK
        return True

    for repo in repos:
        if color[repo] == WHITE and not visit(repo):
            return False

    print(f"✓ Topology cycle safety validated ({len(edges)} declared edges; connected DAG)")
    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Validate six-repo federation topology")
    parser.add_argument("--repos", type=int, default=6)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    if not args.check:
        print("Usage: python3 scripts/validate_federation_topology.py --repos 6 --check")
        return 0

    authority = load_lineage_authority(args.repo_root)
    if authority is None:
        return 1

    validators = [
        ("Repository count", lambda: validate_repo_count(authority, args.repos)),
        ("Role non-overlap", lambda: validate_role_non_overlap(authority)),
        ("Responsibility coverage", lambda: validate_responsibility_coverage(authority)),
        ("Immutable ID schema", lambda: validate_immutable_id_schema(authority)),
        ("Independence claims", lambda: validate_independence_claims(authority)),
        ("Dedup enforcement", lambda: validate_dedup_enforcement(authority)),
        ("Topology cycle safety", lambda: validate_topology_cycle_safety(authority)),
    ]

    all_pass = True
    for name, validator in validators:
        print(f"\n[{name}]")
        if not validator():
            all_pass = False

    print("\n" + "=" * 60)
    if all_pass:
        print("✓ FEDERATION TOPOLOGY VALIDATION PASSED")
        print("  Scope: declared schema/authority graph only; not device/runtime proof")
        return 0

    print("✗ FEDERATION TOPOLOGY VALIDATION FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
