#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REQUIRED = {
    "repo", "visibility", "role", "classification", "license_state",
    "provenance_state", "gate_state", "urgency", "risk", "closure",
    "next_verifiable_step"
}
VALID_URGENCY = {"P0", "P1", "P2", "P3"}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "data/control-plane/PUBLIC_REPOSITORY_ASSURANCE_MATRIX_V1.json")
    data = json.loads(path.read_text(encoding="utf-8"))

    if data.get("schema") != "rafaelia.public-repository-assurance.v1":
        fail("unexpected schema")
    if data.get("claim_allowed") is not False:
        fail("matrix must remain claim_allowed=false")

    repos = data.get("repositories")
    if not isinstance(repos, list) or not repos:
        fail("repositories must be a non-empty list")

    seen = set()
    token_vazio_count = 0
    p0_open = 0

    for i, rec in enumerate(repos):
        missing = sorted(REQUIRED - set(rec))
        if missing:
            fail(f"record {i} missing fields: {missing}")
        repo = rec["repo"]
        if repo in seen:
            fail(f"duplicate repository: {repo}")
        seen.add(repo)
        if rec["visibility"] != "public":
            fail(f"non-public repository leaked into public matrix: {repo}")
        if rec["urgency"] not in VALID_URGENCY:
            fail(f"invalid urgency for {repo}: {rec['urgency']}")
        if not rec["closure"].strip() or not rec["next_verifiable_step"].strip():
            fail(f"open record without closure route: {repo}")

        serialized = json.dumps(rec, sort_keys=True)
        has_gap = "TOKEN_VAZIO" in serialized
        if has_gap:
            token_vazio_count += 1
            if rec["urgency"] == "P0":
                p0_open += 1
            if rec.get("license_state") == "PASS" or rec.get("provenance_state") == "PASS" or rec.get("gate_state") == "PASS":
                fail(f"ambiguous PASS mixed with TOKEN_VAZIO in {repo}")

    promotion = data.get("promotion_rule", {})
    if promotion.get("otherwise") != "TOKEN_VAZIO":
        fail("promotion rule must fail closed to TOKEN_VAZIO")

    print(f"PASS repositories={len(repos)} token_vazio_records={token_vazio_count} p0_open={p0_open}")


if __name__ == "__main__":
    main()
