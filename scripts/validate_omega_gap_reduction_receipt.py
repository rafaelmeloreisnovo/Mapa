#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data/reconciliation/OMEGA_GAP_REDUCTION_RECEIPT_20260829.v1.json"
CI_RECEIPT = ROOT / "data/reconciliation/OMEGA_GAP_REDUCTION_CI_RECEIPT_20260829.v1.json"
SEAL_RECEIPT = ROOT / "data/reconciliation/GENESIS_SEAL_ROOT_CUSTODY_EXCEPTION_20260829.v1.json"
LEDGER = ROOT / "data/reconciliation/OMEGA_OPERATIONAL_WORK_LEDGER_20260829.v2.json"


def load(path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL: " + message)


def main():
    r = load(RECEIPT)
    c = load(CI_RECEIPT)
    s = load(SEAL_RECEIPT)
    l = load(LEDGER)

    for name, obj in (("receipt", r), ("CI receipt", c), ("Seal receipt", s)):
        require(obj["claim_allowed"] is False, f"{name} must remain claim-gated")
        require(obj["release_allowed"] is False, f"{name} must remain release-gated")
        require(obj["promotion_allowed"] is False, f"{name} must remain promotion-gated")
    require(l["claim_allowed"] is False, "ledger must remain claim-gated")

    m = r["messages_19shard"]
    require(m["provider_scope_reproduction"] == "EVIDENCE_PASS", "provider-scope evidence state drift")
    require(m["files"] == "19/19", "19-shard cardinality drift")
    require(m["input_scope_complete"] is True, "provider scope must be complete")
    require(m["parse_error_count"] == 0, "provider-scope parse errors observed")
    require(m["remaining_gap"] == "TOKEN_VAZIO_EXACT_CANONICAL_EXECUTABLE_FULL_SCOPE_BINDING", "exact executable gap must remain explicit")

    stale = {
        "TOKEN_VAZIO_19_SHARD_TERMINAL_EXECUTION",
        "TOKEN_VAZIO_4_OUTPUT_HASHES",
        "TOKEN_VAZIO_INPUT_SCOPE_COMPLETE_TRUE",
    }
    front = next(x for x in l["fronts"] if x["id"] == "MAPA-MESSAGES-19SHARD")
    require(not stale.intersection(front["open_gates"]), "superseded MESSAGES placeholders re-opened")
    require(front["open_gates"] == ["TOKEN_VAZIO_EXACT_CANONICAL_EXECUTABLE_FULL_SCOPE_BINDING"], "unexpected MESSAGES open-gate set")

    p = r["root_png"]
    require(p["git_blob_id"] == "b9d3af394b3f32601c51debf285ee1f627343f14", "Genesis Seal blob drift")
    require(p["byte_size"] == 3160622, "Genesis Seal size drift")
    require(p["mutation_completed"] is False, "historical receipt must not claim binary relocation")

    sc = s["custody"]
    gp = s["guard_policy"]
    require(s["path"] == p["path"], "Seal successor path drift")
    require(sc["git_blob_id"] == p["git_blob_id"], "Seal successor blob drift")
    require(sc["size_bytes"] == p["byte_size"], "Seal successor size drift")
    require(sc["content_mutated"] is False and sc["path_mutated"] is False, "Seal successor must preserve content and path")
    require(gp["root_hash_named_png_default"] == "DENY", "root PNG guard must remain default-deny")
    require(gp["allowed_paths"] == [p["path"]], "root PNG exception set drift")
    require(gp["allowed_only_if"]["git_hash_object_equals"] == p["git_blob_id"], "guard blob identity drift")
    require(gp["allowed_only_if"]["byte_size_equals"] == p["byte_size"], "guard byte-size identity drift")
    require(gp["additional_file_png"] == "FAIL", "additional root PNGs must fail")
    require(gp["blob_drift"] == "FAIL" and gp["size_drift"] == "FAIL", "Seal drift must fail closed")
    require(s["new_treatment"] == "PRESERVE_PUBLIC_ROOT_ANCHOR_WITH_EXACT_CONTENT_ADDRESS_AND_SIZE_GUARD", "Seal treatment drift")

    raw = r["raw018"]
    require(raw["canonical_path"] == "conversations-018.json", "RAW018 path drift")
    require(raw["declared_size_bytes"] == 12115336, "RAW018 declared size drift")
    require(raw["pid_count"] == 100, "RAW018 PID commitment cardinality drift")
    require(raw["candidate_set_sha256"] == "766644f8a199de4317500e6f40d44f9187f767e2ea453910ab4a4d0ec8cfc69e", "RAW018 PID commitment drift")
    require("LISTING_MISS != GLOBAL_ABSENCE" in raw["anti_regression"], "RAW018 search-miss anti-regression missing")

    protected = set(r["protected_open_placeholders"])
    require("TOKEN_VAZIO_MATRIX_C_IDENTITY" in protected, "Matrix C identity must not be fabricated")
    require("TOKEN_VAZIO_MATRIX_C_FORMULA" in protected, "Matrix C formula must not be fabricated")

    checks = c["checks"]
    require(checks["omega_gap_reduction_receipt"]["conclusion"] == "success", "receipt integrity gate must be PASS")
    require(checks["branch_topology_gate"]["conclusion"] == "success", "branch topology gate must be PASS")
    require(checks["general_ci"]["causal_object"] == p["path"], "historical CI causal object must match Genesis Seal path")

    promo = checks["promotion_control"]
    require(promo["result"] == "DENIED", "promotion must remain denied")
    require(promo["blocking_reasons"] == ["INDEPENDENT_APPROVAL_MISSING"], "promotion blocking reason drift")
    require(promo["observed_independent_approvals"] == 0, "independent approval count drift")
    require(promo["required_independent_approvals"] == 1, "required independent approval count drift")

    server = checks["server_merge_enforcement"]
    require(server["server_side_merge_binding"] == "NOT_ENFORCED_OBSERVED", "server enforcement state drift")
    require(server["protected"] is False, "main protection state drift")
    require(server["protection_enabled"] is False, "main protection enabled state drift")
    require(server["required_status_checks"]["enforcement_level"] == "off", "required checks enforcement drift")
    require(set(server["failure_modes"]) == {
        "BRANCH_PROTECTION_DISABLED",
        "PROTECTION_NOT_ENABLED",
        "REQUIRED_STATUS_CHECKS_NOT_ENFORCED",
        "NO_REQUIRED_STATUS_CHECKS_OBSERVED",
    }, "server enforcement failure-mode set drift")

    require(c["aggregate"]["merge_recommendation"] == "DO_NOT_PROMOTE", "CI successor must remain fail-closed")
    require("VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM" in l["anti_regression"], "core epistemic invariant missing")
    print("PASS: gap reduction + CI causality + Genesis Seal custody successor + ledger v2")


if __name__ == "__main__":
    main()
