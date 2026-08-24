#!/usr/bin/env python3

import json
from pathlib import Path

EVIDENCE = Path("data/evidence/novoexport_raw018_wave2_20260824.v1.json")


def fail(msg: str) -> None:
    raise SystemExit(msg)


def main() -> None:
    data = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    if data.get("claim_allowed") is not False:
        fail("claim_allowed must remain false")

    if data.get("status") != "PARTIAL_EVIDENCED_PHYSICAL_INVENTORY_PROVIDER_UNBOUND":
        fail("unexpected status")

    target = data.get("target", {})
    if target.get("path") != "conversations-018.json":
        fail("raw target path mismatch")
    if target.get("size_bytes") != 12115336:
        fail("raw target byte size mismatch")

    planes = data.get("evidence_planes", [])
    if len(planes) != 2:
        fail("exactly two evidence planes required")

    names = {p.get("source") for p in planes}
    if names != {"export_manifest.json", "temp.locate.txt"}:
        fail("unexpected evidence-plane set")

    for plane in planes:
        obs = plane.get("observation", {})
        if obs.get("path") != target["path"] or obs.get("size_bytes") != target["size_bytes"]:
            fail(f"evidence disagreement: {plane.get('source')}")
        sha = plane.get("sha256", "")
        if len(sha) != 64:
            fail(f"invalid evidence SHA-256: {plane.get('source')}")

    agreement = data.get("agreement", {})
    if agreement.get("path_matches") is not True or agreement.get("size_matches") is not True:
        fail("agreement must be exact")
    if agreement.get("independent_planes") != 2:
        fail("independent plane count mismatch")

    transition = data.get("gap_transition", {})
    if transition.get("gap_id") != "TV-RAW-018-CURRENT-ID":
        fail("gap id mismatch")
    if transition.get("current_state") != "PARTIAL_EVIDENCED_PHYSICAL_INVENTORY_PROVIDER_UNBOUND":
        fail("gap transition state mismatch")
    if not transition.get("open_dimensions"):
        fail("open dimensions must remain explicit")

    boundary = data.get("boundary", {})
    if boundary.get("direct_provider_claim") != "TOKEN_VAZIO":
        fail("provider must remain TOKEN_VAZIO")
    if boundary.get("current_raw_bytes_claim") != "TOKEN_VAZIO":
        fail("raw bytes must remain TOKEN_VAZIO")
    if boundary.get("sha_pid_claim") != "TOKEN_VAZIO":
        fail("SHA/PID must remain TOKEN_VAZIO")

    if data.get("anti_substitution", {}).get("rule") != "DERIVED_ORDINAL != RAW_SOURCE_ORDINAL":
        fail("anti-substitution invariant missing")

    print(json.dumps({
        "status": "PASS",
        "gap_id": transition["gap_id"],
        "state": transition["current_state"],
        "path": target["path"],
        "size_bytes": target["size_bytes"],
        "evidence_planes": len(planes),
        "claim_allowed": data["claim_allowed"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
