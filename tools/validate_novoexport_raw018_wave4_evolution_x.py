#!/usr/bin/env python3

import json
from pathlib import Path

EVIDENCE = Path("data/evidence/novoexport_raw018_wave4_evolution_x_20260825.v1.json")
HEX = set("0123456789abcdef")
PID_COMMITMENT = "766644f8a199de4317500e6f40d44f9187f767e2ea453910ab4a4d0ec8cfc69e"
MANIFEST_SHA = "38bb97724a432420328a322eb27ff1af9de28201c2857448e62d2b2e3a36df4a"


def fail(msg: str) -> None:
    raise SystemExit(msg)


def sha256_ok(value: str) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX


def main() -> None:
    data = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    if data.get("claim_allowed") is not False or data.get("release_allowed") is not False:
        fail("claim/release must remain false")
    if data.get("status") != "ACTIVE_G2_MEMBERSHIP_AND_BATCH_COHERENCE_EVIDENCED_CURRENT_BYTE_CUSTODY_OPEN":
        fail("unexpected wave4 status")

    predecessor = data.get("predecessor", {})
    if predecessor.get("wave") != "NOVOEXPORT_RAW018_WAVE3_PID_RECONCILIATION_20260824_V1":
        fail("wave3 must remain the direct append-only predecessor")
    if predecessor.get("merge_commit") != "3ab1eb3a596148e616f0e2d134f2cc8b71b0fafe":
        fail("wave3 merge commit mismatch")
    if predecessor.get("rule") != "APPEND_ONLY_REFINEMENT":
        fail("append-only predecessor rule missing")

    target = data.get("target", {})
    if target.get("path") != "conversations-018.json" or target.get("expected_size_bytes") != 12115336:
        fail("raw018 target identity/size changed")

    axes = data.get("x_evolution", {})
    for key in ("ATLAS", "NOVO", "L", "O", "T", "REL", "SCALE", "EVID", "GAP", "LEARN"):
        if key not in axes:
            fail(f"missing X evolution axis: {key}")

    wave3 = data.get("wave3_preserved_identity_evidence", {})
    if wave3.get("RAW018_PID_HASH_SET") != "EVIDENCED_RECONCILED_100_PRIVACY_PRESERVING":
        fail("merged Wave3 PID hash set regressed")
    if wave3.get("candidate_count") != 100 or wave3.get("candidate_set_sha256") != PID_COMMITMENT:
        fail("Wave3 PID commitment changed")
    for key in ("candidate_chronological_sha256", "historical_object_witness_sha256"):
        if not sha256_ok(wave3.get(key, "")):
            fail(f"invalid preserved Wave3 digest: {key}")
    if wave3.get("current_raw_commitment_match") != "TOKEN_VAZIO_HARD_CUSTODY":
        fail("current-raw PID commitment match must remain open")

    g2 = data.get("active_generation_bridge", {})
    if g2.get("state") != "ACTIVE_SOURCE_BOUND_TO_NOVOEXPORT_JSON_GENERATION":
        fail("active G2 source state missing")
    if g2.get("manifest_sha256") != MANIFEST_SHA or g2.get("manifest_bytes") != 3812404:
        fail("exact active manifest identity mismatch")
    if g2.get("generation_id") != "novoexport_g2_38bb97724a432420":
        fail("active generation id mismatch")
    if g2.get("conversation_shard_count") != 51 or g2.get("conversation_family_declared_bytes") != 1107289897:
        fail("active conversation family declaration mismatch")
    if g2.get("legacy_chunks_active_authority") is not False:
        fail("legacy chunks must not become active authority")

    manifest_probe = g2.get("manifest_entry_probe", {}).get("conversations-018.json", {})
    if manifest_probe.get("size_bytes") != 12115336:
        fail("raw018 exact manifest size mismatch")
    if manifest_probe.get("fields") != ["path", "size_bytes"]:
        fail("raw018 manifest entry field boundary changed")
    if manifest_probe.get("provider_id_present") is not False or manifest_probe.get("content_sha256_present") is not False:
        fail("manifest must not be upgraded into provider/hash evidence")

    exact = g2.get("exact_source_receipts", {})
    if exact.get("receipt_count_at_generation_snapshot") != 11:
        fail("G2 exact-source receipt count mismatch")
    if exact.get("raw018_exact_receipt_present") is not False:
        fail("raw018 exact source receipt must remain absent")
    if exact.get("raw019_exact_receipt_present") is not True or exact.get("raw020_exact_receipt_present") is not True:
        fail("known exact neighboring receipts missing")

    batch = g2.get("batch_00014", {})
    if (batch.get("first_path"), batch.get("last_path"), batch.get("record_count")) != (
        "conversations-017.json", "conversations-020.json", 4
    ):
        fail("batch-00014 path boundary mismatch")
    if batch.get("declared_source_bytes") != 64541017:
        fail("batch-00014 declared bytes changed")
    for key in ("record_sha256", "records_payload_sha256"):
        if not sha256_ok(batch.get(key, "")):
            fail(f"invalid batch commitment: {key}")

    equation = g2.get("batch_byte_equation", {})
    components = [
        equation.get("raw017_observed_bytes"),
        equation.get("raw018_manifest_declared_bytes"),
        equation.get("raw019_observed_bytes"),
        equation.get("raw020_observed_bytes"),
    ]
    if components != [22560934, 12115336, 16440670, 13424077]:
        fail("batch equation components changed")
    if sum(components) != 64541017 or equation.get("sum") != 64541017:
        fail("batch byte equation does not close")
    if equation.get("equals_batch_declared_source_bytes") is not True:
        fail("batch byte coherence must be explicit")
    if equation.get("result") != "TRANSVERSAL_DECLARED_BYTE_COHERENCE_PASS":
        fail("unexpected batch coherence result")
    if equation.get("boundary") != "BATCH_SUM_AGREEMENT != RAW018_BYTE_CUSTODY":
        fail("batch/custody epistemic boundary missing")

    candidate = data.get("candidate_archive", {})
    if candidate.get("size_bytes") != 187756731 or not sha256_ok(candidate.get("sha256", "")):
        fail("candidate archive identity invalid")
    if candidate.get("member_count") != 5 or candidate.get("exact_raw018_member_present") is not False:
        fail("candidate archive member evidence mismatch")
    if candidate.get("direct_container_result") != "REJECTED_FOR_DIRECT_RAW018_CONTAINER":
        fail("candidate must remain rejected")

    neighbors = data.get("current_neighbor_evidence", {})
    for name, size, digest in (
        ("shard017", 22560934, "b4b6a6080b89102699e6dbd9958c715264464d74f9782126af3085296eb3ce4f"),
        ("shard019", 16440670, "f90bfc11a9088772570c1f81503c1bedcc9bd475c5435ce809d62812ff351436"),
        ("shard020", 13424077, "32ad3e5f02f06353280fb41fbb6a320b3cb9e42c841105b95674a6a386d8b6c3"),
    ):
        item = neighbors.get(name, {})
        if item.get("size_bytes") != size or item.get("sha256") != digest:
            fail(f"neighbor evidence mismatch: {name}")
        if item.get("json_array_cardinality") != 100:
            fail(f"neighbor cardinality mismatch: {name}")

    probe = data.get("candidate_monolith_boundary_probe", {})
    observations = {x.get("role"): x.get("present") for x in probe.get("observations", [])}
    if observations != {
        "current_shard017_first": True,
        "current_shard017_last": False,
        "current_shard019_first": False,
    }:
        fail("historical candidate boundary probe changed")
    if probe.get("result") != "REJECTED_AS_COMPLETE_SOURCE_FOR_CURRENT_SHARD_RANGE_017_019":
        fail("candidate monolith must remain rejected")

    transition = data.get("gap_transition", {})
    if transition.get("gap_id") != "TV-RAW-018-CURRENT-ID":
        fail("gap id mismatch")
    if transition.get("previous_state") != "PARTIAL_EVIDENCED_PID_SET_CURRENT_BYTE_CUSTODY_OPEN":
        fail("Wave3 predecessor state changed")
    if transition.get("current_state") != "PARTIAL_EVIDENCED_ACTIVE_MEMBERSHIP_PID_SET_CURRENT_BYTE_CUSTODY_OPEN":
        fail("Wave4 state must only promote active membership/batch coherence")
    if len(transition.get("open_dimensions", [])) != 5:
        fail("current raw custody dimensions must remain explicit")

    boundary = data.get("boundary", {})
    if boundary.get("raw018_active_logical_membership") != "EVIDENCED_BY_EXACT_ACTIVE_MANIFEST_AND_G2":
        fail("active logical membership not promoted correctly")
    if boundary.get("raw018_pid_hash_set") != "EVIDENCED_RECONCILED_100_PRIVACY_PRESERVING_BY_WAVE3":
        fail("PID commitment evidence regressed")
    if boundary.get("batch_declared_byte_coherence") != "PASS":
        fail("batch coherence not recorded")
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

    required = {
        "PID_HASH_SET_EVIDENCE != CURRENT_RAW_BYTE_CUSTODY",
        "ACTIVE_GENERATION_MEMBERSHIP != PROVIDER_IDENTITY",
        "BATCH_SUM_AGREEMENT != RAW018_BYTE_CUSTODY",
        "MANIFEST_DECLARED_SIZE != OBSERVED_CURRENT_BYTES",
        "CANDIDATE_TEMPORAL_AFFINITY != PROVIDER_IDENTITY",
        "MONOLITH_OVERLAP != COMPLETE_SHARD_SOURCE",
        "NEIGHBOR_CARDINALITY != CURRENT_RAW018_CARDINALITY",
        "RECONSTRUCTION != OBSERVED_RAW_SOURCE",
        "TOKEN_VAZIO != 0",
    }
    if not required.issubset(set(data.get("anti_regression", {}).get("rules", []))):
        fail("anti-regression rule set incomplete")

    print(json.dumps({
        "status": "PASS",
        "record_id": data["record_id"],
        "gap_id": transition["gap_id"],
        "generation": g2["generation_id"],
        "batch_00014_bytes": batch["declared_source_bytes"],
        "batch_equation": equation["result"],
        "pid_commitment": wave3["RAW018_PID_HASH_SET"],
        "current_raw_provider": boundary["direct_provider_claim"],
        "claim_allowed": data["claim_allowed"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
