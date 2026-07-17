#!/usr/bin/env python3
"""Validate the Ω³ federated repository authority registry.

Standard-library only. The validator is intentionally fail-closed: malformed or
ambiguous authority data blocks promotion but does not claim integration exists.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "indices" / "repository_authority_registry.json"

ALLOWED_STATES = {
    "VERIFIED",
    "VERIFIED_LIMITED",
    "DECLARED_BY_AUTHOR",
    "HYPOTHESIS",
    "TOKEN_VAZIO",
    "CONTRADICTION",
}
REQUIRED_REPO_FIELDS = {
    "repository",
    "role",
    "canonical_for",
    "consumes",
    "produces",
    "evidence_state",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if not REGISTRY.is_file():
        fail(f"registry not found: {REGISTRY}")

    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse registry: {exc}")

    if data.get("claim_allowed") is not False:
        fail("top-level claim_allowed must remain false until independent review")

    repos = data.get("repositories")
    if not isinstance(repos, list) or not repos:
        fail("repositories must be a non-empty list")

    names: list[str] = []
    authorities: defaultdict[str, list[str]] = defaultdict(list)

    for index, item in enumerate(repos):
        if not isinstance(item, dict):
            fail(f"repositories[{index}] must be an object")

        missing = REQUIRED_REPO_FIELDS - item.keys()
        if missing:
            fail(f"repositories[{index}] missing fields: {sorted(missing)}")

        name = item["repository"]
        if not isinstance(name, str) or name.count("/") != 1:
            fail(f"invalid repository name at index {index}: {name!r}")
        names.append(name)

        state = item["evidence_state"]
        if state not in ALLOWED_STATES:
            fail(f"invalid evidence_state for {name}: {state!r}")

        for field in ("canonical_for", "consumes", "produces"):
            value = item[field]
            if not isinstance(value, list) or any(not isinstance(v, str) or not v for v in value):
                fail(f"{name}.{field} must be a list of non-empty strings")

        for domain in item["canonical_for"]:
            authorities[domain].append(name)

    duplicates = [name for name, count in Counter(names).items() if count > 1]
    if duplicates:
        fail(f"duplicate repositories: {duplicates}")

    ambiguous = {domain: owners for domain, owners in authorities.items() if len(owners) != 1}
    if ambiguous:
        fail(f"canonical domains must have exactly one owner: {ambiguous}")

    control_plane = data.get("control_plane")
    if control_plane not in names:
        fail("control_plane must reference a registered repository")

    invariants = data.get("global_invariants")
    if not isinstance(invariants, list) or len(set(invariants)) != len(invariants):
        fail("global_invariants must be a unique list")

    print(
        json.dumps(
            {
                "status": "PASS",
                "claim_allowed": False,
                "repositories": len(repos),
                "canonical_domains": len(authorities),
                "registry": str(REGISTRY.relative_to(ROOT)),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
