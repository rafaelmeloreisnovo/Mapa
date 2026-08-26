#!/usr/bin/env python3

import json
from pathlib import Path

EVIDENCE = Path("data/evidence/novoexport_raw018_wave4_evolution_x_20260825.v1.json")
HEX = set("0123456789abcdef")


def fail(msg: str) -> None:
    raise SystemExit(msg)


def sha256_ok(value: str) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX


def main() -> None:
    data = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    if data.get("claim_allowed") is not False or data.get("release_allowed") is not False:
        fail("claim/release must remain false")
    if data.get("status") != "CANDIDATE_REJECTED_RAW018_PROVIDER_STILL_UNBOUND":
        fail("unexpected wave4 status")
    if data.get("predecessor") != "NOVOEXPORT_RAW018_WAVE2_20260824_V1":
        fail("append-only predecessor missing")

    target = data.get("target", {})
    if target.get("path") != "conversations-018.json":
        fail("raw018 target path mismatch")
    if target.get("expected_size_bytes_from_predecessor") != 12115336:
        fail("raw018 predecessor size changed")

    axes = data.get("x_evolution", {})
    for key in ("ATLAS", "NOVO", "L", "O", "T", "REL", "SCALE", "EVID", "GAP", "LEARN"):
        if key not in axes:
            fail(f"missing X evolution axis: {key}")

    candidate = data.get("candidate_archive", {})
    if candidate.get("size_bytes") != 187756731:
        fail("candidate archive size mismatch")
    if not sha256_ok(candidate.get("sha256", "")):
        fail("candidate archive SHA-256 invalid")
    if candidate.get("member_count") != 5 or len(candidate.get("members", [])) != 5:
        fail("candidate archive member count mismatch")
    member_names = {m.get("name") for m in candidate.get("members", [])}
    if member_names != {"user.json", "conversations.json", "message_feedback.json", "shared_conversations.json", "chat.html"}:
        fail("candidate archive member set mismatch")
    if candidate.get("exact_raw018_member_present") is not False:
        fail("raw018 must not be claimed as direct archive member")
    if candidate.get("direct_container_result") != "REJECTED_FOR_DIRECT_RAW018_CONTAINER":
        fail("candidate must stay rejected as direct container")

    neighbors = data.get("current_neighbor_evidence", {})
    s17 = neighbors.get("shard017", {})
    s19 = neighbors.get("shard019", {})
    if s17.get("json_array_cardinality") != 100 or s19.get("json_array_cardinality") != 100:
        fail("observed neighbor cardinality changed")
    if not sha256_ok(s17.get("sha256", "")) or not sha256_ok(s19.get("sha256", "")):
        fail("neighbor SHA-256 invalid")

    probe = data.get("candidate_monolith_boundary_probe", {})
    observations = {x.get("role"): x.get("present") for x in probe.get("observations", [])}
    expected = {
        "current_shard017_first": True,
        "current_shard017_last": False,
        "current_shard019_first": False,
    }
    if observations != expected:
        fail("boundary probe does not match observed evidence")
    if probe.get("result") != "REJECTED_AS_COMPLETE_SOURCE_FOR_CURRENT_SHARD_RANGE_017_019":
        fail("monolith must remain rejected as complete current shard source")

    transition = data.get("gap_transition", {})
    if transition.get("gap_id") != "TV-RAW-018-CURRENT-ID":
        fail("gap id mismatch")
    if transition.get("previous_state") != transition.get("current_state"):
        fail("wave4 must narrow search without falsely promoting gap state")
    if transition.get("current_state") != "PARTIAL_EVIDENCED_PHYSICAL_INVENTORY_PROVIDER_UNBOUND":
        fail("raw018 provider gap state changed unexpectedly")
    if len(transition.get("open_dimensions", [])) < 5:
        fail("open raw018 dimensions must remain explicit")

    boundary = data.get("boundary", {})
    for key in ("direct_provider_claim", "current_raw_bytes_claim", "raw_sha256_claim", "raw_cardinality_claim", "raw_pid_set_claim"):
        if boundary.get(key) != "TOKEN_VAZIO":
            fail(f"{key} must remain TOKEN_VAZIO")

    anti = data.get("anti_regression", {}).get("rules", [])
    required = {
        "CANDIDATE_TEMPORAL_AFFINITY != PROVIDER_IDENTITY",
        "MONOLITH_OVERLAP != COMPLETE_SHARD_SOURCE",
        "NEIGHBOR_CARDINALITY != RAW018_CARDINALITY",
        "RECONSTRUCTION != OBSERVED_RAW_SOURCE",
        "TOKEN_VAZIO != 0",
    }
    if not required.issubset(set(anti)):
        fail("anti-regression rule set incomplete")

    print(json.dumps({
        "status": "PASS",
        "record_id": data["record_id"],
        "gap_id": transition["gap_id"],
        "candidate": candidate["direct_container_result"],
        "monolith": probe["result"],
        "raw018_provider": boundary["direct_provider_claim"],
        "claim_allowed": data["claim_allowed"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
