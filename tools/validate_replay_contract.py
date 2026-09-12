#!/usr/bin/env python3
import json, sys
from pathlib import Path

REQUIRED_COERCIONS = {"0","false","null","empty_string","missing","default"}

def fail(errors, msg):
    errors.append(msg)

def validate(doc):
    errors = []
    if doc.get("schema_version") != "rafaelia.replay-contract/v1":
        fail(errors, "schema_version")
    if doc.get("claim_allowed") is not False:
        fail(errors, "claim_allowed must be false")

    b = doc.get("boundary", {})
    if not b.get("base_state_ref"):
        fail(errors, "boundary.base_state_ref")
    if not isinstance(b.get("unresolved"), list):
        fail(errors, "boundary.unresolved")

    r = doc.get("reconstruction", {})
    if r.get("result") == "PASS_EXACT":
        if not r.get("expected_hash") or r.get("expected_hash") != r.get("observed_hash"):
            fail(errors, "PASS_EXACT requires equal non-empty hashes")
    if r.get("result") == "TOKEN_VAZIO" and not r.get("missing"):
        fail(errors, "TOKEN_VAZIO reconstruction must enumerate missing")

    ops = doc.get("operator_versions", [])
    if not ops:
        fail(errors, "operator_versions empty")
    seen_ops = set()
    for op in ops:
        oid = op.get("operator_id")
        if not oid or oid in seen_ops:
            fail(errors, f"operator_id duplicate/empty: {oid}")
        seen_ops.add(oid)
        if op.get("formal_binding") is True:
            if op.get("binding_state") != "BOUND":
                fail(errors, f"{oid}: formal binding must be BOUND")
        if oid == "PLECT" and op.get("formal_binding") is True and not op.get("test_refs"):
            fail(errors, "PLECT cannot become formal without test_refs")

    eo = doc.get("event_order", {})
    events = eo.get("events", [])
    ids = [e.get("event_id") for e in events]
    if len(ids) != len(set(ids)):
        fail(errors, "duplicate event ids")
    known = set(ids)
    for e in events:
        if e.get("event_id") in set(e.get("parents", [])):
            fail(errors, f"self parent: {e.get('event_id')}")
        for p in e.get("parents", []):
            if p not in known and eo.get("orphan_policy") == "REJECT":
                fail(errors, f"orphan parent: {p}")

    up = doc.get("unicode_policy", {})
    if up.get("preserve_raw") is not True or up.get("codepoints_required") is not True:
        fail(errors, "unicode raw/codepoint preservation required")
    if up.get("confusable_policy") != "DISTINCT_UNLESS_ALIAS_PROVEN":
        fail(errors, "unicode confusable policy")

    tv = doc.get("token_vazio_policy", {})
    got = set(tv.get("forbidden_coercions", []))
    if REQUIRED_COERCIONS - got:
        fail(errors, "TOKEN_VAZIO coercion set incomplete")
    if tv.get("search_miss_is_absence") is not False:
        fail(errors, "SEARCH_MISS != ABSENCE")

    sl = doc.get("source_lineage", {})
    if sl.get("lineage_id_required") is not True or sl.get("dedupe_required") is not True:
        fail(errors, "source lineage/dedupe required")

    dp = doc.get("dictionary_policy", {})
    if dp.get("append_only") is not True or dp.get("correction_policy") != "APPEND_PLUS_SUPERSEDES":
        fail(errors, "dictionary append-only correction policy")
    if dp.get("conflict_policy") != "FORK_UNTIL_RESOLVED":
        fail(errors, "dictionary conflict policy")

    sp = doc.get("snapshot_policy", {})
    if sp.get("snapshot_hash_required") is not True:
        fail(errors, "snapshot hash required")
    if sp.get("stale_behavior") != "MARK_STALE_DO_NOT_PROMOTE":
        fail(errors, "snapshot stale behavior")

    ex = doc.get("exit_criteria", {})
    if int(ex.get("max_active_gap_families", 0)) < 1 or not ex.get("stop_conditions"):
        fail(errors, "exit criteria")

    if doc.get("falsification", {}).get("negative_controls_required") is not True:
        fail(errors, "negative controls required")

    pr = doc.get("privacy", {})
    if pr.get("raw_content_default") is not False or pr.get("reconstructibility_does_not_imply_raw_retention") is not True:
        fail(errors, "privacy/reconstructibility boundary")

    cp = doc.get("cultural_provenance", {})
    if cp.get("official_tradition_claim") is not False:
        fail(errors, "cultural authority must remain false")

    uq = doc.get("uncertainty", {})
    if uq.get("weighted_paths_state") != "CALIBRATED" and uq.get("calibration_required_before_weights") is not True:
        fail(errors, "uncalibrated weights")

    hv = doc.get("human_validation", {})
    if hv.get("state") != "ABORTED_UNTIL_ETHICS":
        fail(errors, "human validation must remain aborted until ethics")
    if hv.get("ethics_review_required") is not True or hv.get("consent_required") is not True:
        fail(errors, "human validation ethics/consent")

    for ob in doc.get("operator_observations", []):
        if ob.get("operator_id") == "PLECT" and ob.get("source_bound") is True and ob.get("formal_binding") is True:
            fail(errors, "historical PLECT observation cannot self-promote to formal binding")

    return errors

def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "data/contracts/replay-contract.v1.json")
    doc = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(doc)
    if errors:
        print(json.dumps({"status":"FAIL","errors":errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"status":"PASS_LIMITED_STRUCTURE","contract_id":doc["contract_id"],"claim_allowed":False}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
