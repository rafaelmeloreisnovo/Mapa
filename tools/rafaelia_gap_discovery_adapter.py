#!/usr/bin/env python3
"""Bridge Repository Gap Mapper output into non-destructive Gap Atlas candidates.

This adapter never auto-closes or auto-promotes an atlas record. It converts each
observed repository gap instance into either:
  * mapped: at least one atlas record references the artifact/path; or
  * unmapped: a candidate that must receive/link a gap_id.

The output is a discovery receipt, not evidence that the underlying gap is fixed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def candidate_id(root: str, path: str, gap: str) -> str:
    raw = f"{root}\0{path}\0{gap}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:24]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gap-map", type=Path, required=True)
    ap.add_argument("--atlas", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--fail-on-unmapped", action="store_true")
    args = ap.parse_args()

    gap_map = load(args.gap_map)
    atlas = load(args.atlas)
    if gap_map.get("schema") != "rafaelia.repository-gap-map/v1":
        raise SystemExit("ERROR: unsupported repository gap map schema")
    if atlas.get("schema") != "RAFAELIA_GAP_ATLAS_V1":
        raise SystemExit("ERROR: unsupported gap atlas schema")

    records = atlas.get("records", [])
    candidates: list[dict] = []
    mapped = 0
    unmapped = 0

    for artifact in gap_map.get("artifacts", []):
        gaps = artifact.get("gaps") or []
        if not gaps:
            continue
        path = artifact.get("path", "")
        root = artifact.get("root", "")
        map_artifact_id = artifact.get("artifact_id", "")
        refs = []
        for rec in records:
            source_text = "\n".join(rec.get("source_refs", []))
            if rec.get("artifact_id") == map_artifact_id or (path and path in source_text):
                refs.append(rec["gap_id"])
        for gap in gaps:
            is_mapped = bool(refs)
            mapped += int(is_mapped)
            unmapped += int(not is_mapped)
            candidates.append(
                {
                    "candidate_id": candidate_id(root, path, gap),
                    "map_artifact_id": map_artifact_id,
                    "root": root,
                    "path": path,
                    "kind": artifact.get("kind"),
                    "gap": gap,
                    "unresolved_markers": artifact.get("unresolved_markers", []),
                    "sha256": artifact.get("sha256"),
                    "hash_status": artifact.get("hash_status"),
                    "mapped_gap_ids": sorted(refs),
                    "state": "MAPPED" if is_mapped else "UNMAPPED_REQUIRES_GAP_ID",
                }
            )

    output = {
        "schema": "RAFAELIA_GAP_DISCOVERY_RECEIPT_V1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "claim_allowed": False,
        "source_gap_map": str(args.gap_map),
        "source_atlas": str(args.atlas),
        "summary": {
            "gap_instances": len(candidates),
            "mapped": mapped,
            "unmapped": unmapped,
        },
        "candidates": candidates,
        "next_gate": "Every UNMAPPED_REQUIRES_GAP_ID candidate must be triaged into an existing gap_id, a new typed gap record, or an explicit false-positive/accepted-limitation event.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output["summary"], sort_keys=True))
    return 1 if args.fail_on_unmapped and unmapped else 0


if __name__ == "__main__":
    raise SystemExit(main())
