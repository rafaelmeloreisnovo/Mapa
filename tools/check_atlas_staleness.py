#!/usr/bin/env python3
"""Compare semantic object snapshots across providers; never fetches providers itself."""
import json
import sys
from pathlib import Path


def main(path):
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    groups = {}
    for row in doc.get("observations", []):
        groups.setdefault(row["object_id"], []).append(row)

    stale = []
    unresolved = []
    for object_id, rows in sorted(groups.items()):
        hashes = {
            row.get("semantic_hash")
            for row in rows
            if row.get("semantic_hash") not in (None, "TOKEN_VAZIO")
        }
        versions = {
            row.get("state_version")
            for row in rows
            if row.get("state_version") not in (None, "TOKEN_VAZIO")
        }
        if any(row.get("semantic_hash") == "TOKEN_VAZIO" for row in rows):
            unresolved.append(object_id)
        if len(hashes) > 1 or len(versions) > 1:
            stale.append(
                {
                    "object_id": object_id,
                    "providers": [row.get("provider") for row in rows],
                    "hashes": sorted(hashes),
                    "versions": sorted(versions),
                }
            )

    result = {
        "status": "PASS" if not stale else "STALE_DETECTED",
        "stale": stale,
        "unresolved": unresolved,
        "claim_allowed": False,
    }
    print(json.dumps(result, sort_keys=True))
    return 2 if stale else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
