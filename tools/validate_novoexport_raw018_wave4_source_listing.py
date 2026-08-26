#!/usr/bin/env python3

import json
from pathlib import Path

EVIDENCE = Path("data/evidence/novoexport_raw018_wave4_source_listing_reconciliation_20260825.v1.json")


def fail(msg: str) -> None:
    raise SystemExit(msg)


def main() -> None:
    d = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    if d.get("claim_allowed") is not False or d.get("release_allowed") is not False:
        fail("claim/release must remain false")
    if d.get("parent_record") != "NOVOEXPORT_RAW018_WAVE4_EVOLUTION_X_20260825_V1":
        fail("source-listing evidence must remain attached to Wave4")

    listing = d.get("source_listing", {})
    manifest = d.get("active_manifest", {})
    if listing.get("bytes") != 1396867:
        fail("temp.locate byte count mismatch")
    if listing.get("sha256") != "7e291744e7522eeb4a4ce4f843f55ef479205de8305ac126130ff6c5631682bf":
        fail("temp.locate SHA mismatch")
    if listing.get("file_entries_parsed") != 15437:
        fail("listing parsed-file count mismatch")
    if listing.get("raw018_historical_size_bytes") != 12115336:
        fail("raw018 historical listing size mismatch")
    if "conversations-018.json" not in listing.get("raw018_line", ""):
        fail("raw018 listing line missing")

    if manifest.get("bytes") != 3812404:
        fail("manifest byte count mismatch")
    if manifest.get("sha256") != "38bb97724a432420328a322eb27ff1af9de28201c2857448e62d2b2e3a36df4a":
        fail("manifest SHA mismatch")
    if manifest.get("export_file_entries") != 15439:
        fail("manifest entry count mismatch")

    full = d.get("full_path_size_reconciliation", {})
    if full.get("common_paths") != 15435 or full.get("common_path_size_mismatches") != 0:
        fail("full path/size reconciliation mismatch")
    if full.get("manifest_only_count") != 4 or len(full.get("manifest_only", [])) != 4:
        fail("manifest-only delta mismatch")
    if full.get("listing_only_count") != 2 or len(full.get("listing_only", [])) != 2:
        fail("listing-only delta mismatch")
    if full.get("result") != "NEAR_COMPLETE_PATH_SIZE_SNAPSHOT_COHERENCE_PASS":
        fail("near-complete snapshot result missing")

    family = d.get("conversation_family_reconciliation", {})
    for key in ("manifest_count", "listing_count", "common_count"):
        if family.get(key) != 51:
            fail(f"conversation family {key} must be 51")
    if family.get("path_size_mismatches") != 0:
        fail("conversation family path/size mismatch")
    if family.get("declared_bytes_manifest") != 1107289897 or family.get("declared_bytes_listing") != 1107289897:
        fail("conversation family aggregate mismatch")
    if family.get("result") != "CONVERSATION_FAMILY_51_OF_51_PATH_SIZE_COHERENCE_PASS":
        fail("conversation family reconciliation must pass")
    raw018 = family.get("raw018_member", {})
    if raw018 != {
        "manifest_size_bytes": 12115336,
        "listing_size_bytes": 12115336,
        "size_equal": True,
        "historical_source_listing_presence": True,
    }:
        fail("raw018 historical member evidence mismatch")

    promotions = d.get("promotions", {})
    if promotions.get("raw018_historical_local_source_listing_presence") != "EVIDENCED":
        fail("historical source presence must be evidenced")
    if promotions.get("conversation_family_path_size_snapshot_coherence") != "PASS":
        fail("conversation family coherence promotion missing")

    non = d.get("non_promotions", {})
    for key in (
        "raw018_current_provider_id",
        "raw018_current_or_immutable_content_bytes",
        "raw018_content_sha256",
        "raw018_current_json_parse",
        "raw018_current_cardinality",
        "raw018_raw_derived_pid_commitment_match",
    ):
        if non.get(key) != "TOKEN_VAZIO":
            fail(f"{key} must remain TOKEN_VAZIO")

    required = {
        "HISTORICAL_FILESYSTEM_LISTING != RAW_CONTENT_BYTES",
        "PATH_SIZE_COHERENCE != CONTENT_SHA256_EQUALITY",
        "51_OF_51_PATH_SIZE_MATCH != CURRENT_PROVIDER_CUSTODY",
        "LISTING_TIMESTAMP != CONTENT_VERSION_PROOF",
        "NEAR_COMPLETE_SNAPSHOT != TOTAL_SNAPSHOT_EQUALITY",
        "TOKEN_VAZIO != 0",
    }
    if not required.issubset(set(d.get("anti_regression", []))):
        fail("source-listing anti-regression rules incomplete")

    print(json.dumps({
        "status": "PASS",
        "record_id": d["record_id"],
        "common_paths": full["common_paths"],
        "conversation_paths": family["common_count"],
        "raw018_listing_presence": promotions["raw018_historical_local_source_listing_presence"],
        "raw018_bytes": non["raw018_current_or_immutable_content_bytes"],
        "claim_allowed": d["claim_allowed"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
