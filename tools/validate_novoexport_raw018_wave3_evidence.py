#!/usr/bin/env python3
import json
from pathlib import Path

EVIDENCE = Path("data/evidence/novoexport_raw018_wave3_pid_reconciliation_20260824.v1.json")

EXPECTED_SET = "766644f8a199de4317500e6f40d44f9187f767e2ea453910ab4a4d0ec8cfc69e"
EXPECTED_CHRONO = "c29cbc493b2401d0d875a49a71999f4b32f8b3faab8a86cd2c1d9a4e4ca83706"
EXPECTED_OBJECT_WITNESS = "f14cd8767241255d64dba51b818e1bf3d5eefb6af157f1b321199cb102223156"


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    data = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    if data.get("claim_allowed") is not False:
        fail("claim_allowed must remain false")
    if data.get("status") != "PARTIAL_EVIDENCED_PID_SET_CURRENT_BYTE_CUSTODY_OPEN":
        fail("unexpected Wave 3 status")

    target = data.get("target", {})
    if target.get("path") != "conversations-018.json":
        fail("target path mismatch")
    if target.get("expected_size_bytes") != 12115336:
        fail("target size mismatch")

    refinement = data.get("gap_refinement", {}).get("new_dimensions", {})
    if refinement.get("RAW018_PID_HASH_SET") != "EVIDENCED_RECONCILED_100_PRIVACY_PRESERVING":
        fail("PID hash set must be explicitly evidenced")
    for key in (
        "RAW018_CURRENT_PROVIDER",
        "RAW018_CURRENT_BYTES",
        "RAW018_CURRENT_SHA256",
        "RAW018_CURRENT_JSON_PARSE",
    ):
        if refinement.get(key) != "TOKEN_VAZIO_HARD_CUSTODY":
            fail(f"{key} must remain TOKEN_VAZIO_HARD_CUSTODY")

    rec = data.get("identity_reconciliation", {})
    expected_counts = {
        "historical_locator_unique_pids": 2573,
        "current_index_unique_pids": 4698,
        "historical_current_intersection": 2473,
        "historical_minus_current": 100,
        "candidate_pids_outside_live_sibling_boundary": 0,
    }
    for key, value in expected_counts.items():
        if rec.get(key) != value:
            fail(f"identity reconciliation mismatch: {key}")
    if rec.get("candidate_set_sha256") != EXPECTED_SET:
        fail("candidate set commitment mismatch")
    if rec.get("candidate_chronological_sha256") != EXPECTED_CHRONO:
        fail("candidate chronological commitment mismatch")
    if rec.get("raw_ids_persisted_publicly") is not False:
        fail("raw ids must not be persisted publicly")
    if rec.get("candidate_hash_list_persisted_publicly") is not False:
        fail("candidate hash list must not be persisted publicly")

    siblings = data.get("live_sibling_boundary", {})
    raw17 = siblings.get("raw017", {})
    raw19 = siblings.get("raw019", {})
    if raw17.get("root_objects") != 100 or raw19.get("root_objects") != 100:
        fail("sibling root count mismatch")
    if raw17.get("create_time_monotonic_ascending") is not True:
        fail("RAW017 monotonic evidence missing")
    if raw19.get("create_time_monotonic_ascending") is not True:
        fail("RAW019 monotonic evidence missing")

    witness = data.get("independent_historical_archive_witness", {})
    if witness.get("candidate_pids_found") != 100:
        fail("archive witness must find all 100 candidates")
    if witness.get("candidate_pids_missing") != 0:
        fail("archive witness has missing candidates")
    if witness.get("timestamp_agreement_count") != 100:
        fail("timestamp agreement must cover all candidates")
    if witness.get("timestamp_max_abs_delta_seconds", 1) > 0.0011:
        fail("timestamp precision tolerance exceeded")
    if witness.get("object_witness_sha256") != EXPECTED_OBJECT_WITNESS:
        fail("object witness commitment mismatch")

    falsifiers = data.get("falsifiers_preserved", [])
    if len(falsifiers) < 3 or any(item.get("result") != "FALSE" for item in falsifiers):
        fail("falsifiers must remain explicitly preserved")

    boundary = data.get("current_custody_boundary", {})
    if boundary.get("direct_current_provider_search") != "BOUNDED_NO_RESULT":
        fail("direct provider search boundary mismatch")
    if boundary.get("absence_global") is not False:
        fail("bounded search miss must not become global absence")
    for key in ("current_raw_bytes", "current_raw_sha256", "current_raw_json_parse", "current_raw_provider"):
        if boundary.get(key) != "TOKEN_VAZIO":
            fail(f"{key} must remain TOKEN_VAZIO")

    anti = set(data.get("anti_regression", []))
    required = {
        "PID_HASH_SET_EVIDENCE != CURRENT_RAW_BYTE_CUSTODY",
        "HISTORICAL_OBJECT_WITNESS != CURRENT_RAW018_SHA256",
        "CARDINALITY_MATCH_ALONE != IDENTITY_PROOF",
        "TIMESTAMP_WINDOW_ALONE != IDENTITY_PROOF",
        "DERIVED_ORDINAL != RAW_SOURCE_ORDINAL",
        "SEARCH_MISS != GLOBAL_ABSENCE",
    }
    if not required.issubset(anti):
        fail("anti-regression boundary incomplete")

    print(json.dumps({
        "status": "PASS",
        "wave": data["evidence_id"],
        "pid_hash_set": refinement["RAW018_PID_HASH_SET"],
        "candidate_count": rec["historical_minus_current"],
        "candidate_set_sha256": rec["candidate_set_sha256"],
        "current_byte_custody": "OPEN_TOKEN_VAZIO",
        "claim_allowed": data["claim_allowed"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
