#!/usr/bin/env python3

import json
from pathlib import Path

EVIDENCE = Path("data/evidence/novoexport_raw018_wave4_evolution_x_20260825.v1.json")
HEX = set("0123456789abcdef")
PID_COMMITMENT = "766644f8a199de4317500e6f40d44f9187f767e2ea453910ab4a4d0ec8cfc69e"


def fail(msg: str) -> None:
    raise SystemExit(msg)


def sha256_ok(value: str) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX


def main() -> None:
    data = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    if data.get("claim_allowed") is not False or data.get("release_allowed") is not False:
        fail("claim/release must remain false")
    if data.get("status") != "CANDIDATE_REJECTED_PID_COMMITMENT_PRESERVED_CURRENT_BYTE_CUSTODY_OPEN":
        fail("unexpected wave4 status")

    predecessor = data.get("predecessor", {})
    if predecessor.get("wave") != "NOVOEXPORT_RAW018_WAVE3_PID_RECONCILIATION_20260824_V1":
        fail("wave3 must be the direct append-only predecessor")
    if predecessor.get("merge_commit") != "3ab1eb3a596148e616f0e2d134f2cc8b71b0fafe":
        fail("wave3 merge commit mismatch")
    if predecessor.get("rule") != "APPEND_ONLY_REFINEMENT":
        fail("append-only predecessor rule missing")

    target = data.get("target", {})
    if target.get("path") != "conversations-018.json":
        fail("raw018 target path mismatch")
    if target.get("expected_size_bytes") != 12115336:
        fail("raw018 evidenced size changed")

    axes = data.get("x_evolution", {})
    for key in ("ATLAS", "NOVO", "L", "O", "T", "REL", "SCALE", "EVID", "GAP", "LEARN"):
        if key not in axes:
            fail(f"missing X evolution axis: {key}")

    wave3 = data.get("wave3_preserved_identity_evidence", {})
    if wave3.get("RAW018_PID_HASH_SET") != "EVIDENCED_RECONCILED_100_PRIVACY_PRESERVING":
        fail("merged Wave3 PID hash set was regressed")
    if wave3.get("candidate_count") != 100:
        fail("Wave3 candidate count changed")
    if wave3.get("candidate_set_sha256") != PID_COMMITMENT:
        fail("Wave3 candidate commitment changed")
    for key in ("candidate_chronological_sha256", "historical_object_witness_sha256"):
        if not sha256_ok(wave3.get(key, "")):
            fail(f"invalid preserved Wave3 digest: {key}")
    if wave3.get("current_raw_commitment_match") != "TOKEN_VAZIO_HARD_CUSTODY":
        fail("current-raw PID commitment match must remain open")

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
        fail("wave4 must narrow search without falsely promoting custody state")
    if transition.get("current_state") != "PARTIAL_EVIDENCED_PID_SET_CURRENT_BYTE_CUSTODY_OPEN":
        fail("Wave3-refined gap state must be preserved")
    if len(transition.get("open_dimensions", [])) < 5:
        fail("open current-byte dimensions must remain explicit")

    boundary = data.get("boundary", {})
    if boundary.get("raw018_pid_hash_set") != "EVIDENCED_RECONCILED_100_PRIVACY_PRESERVING_BY_WAVE3":
        fail("PID evidence must remain closed")
    for key in (
        "direct_provider_claim",
        "current_raw_bytes_claim",
        "raw_sha256_claim",
        "current_raw_json_parse_claim",
        "current_raw_cardinality_claim",
        "current_raw_pid_commitment_match",
    ):
        if boundary.get(key) != "TOKEN_VAZIO":
            fail(f"{key} must remain TOKEN_VAZIO")

    anti = data.get("anti_regression", {}).get("rules", [])
    required = {
        "PID_HASH_SET_EVIDENCE != CURRENT_RAW_BYTE_CUSTODY",
        "CANDIDATE_TEMPORAL_AFFINITY != PROVIDER_IDENTITY",
        "MONOLITH_OVERLAP != COMPLETE_SHARD_SOURCE",
        "NEIGHBOR_CARDINALITY != CURRENT_RAW018_CARDINALITY",
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
        "pid_commitment": wave3["RAW018_PID_HASH_SET"],
        "current_raw_provider": boundary["direct_provider_claim"],
        "claim_allowed": data["claim_allowed"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
