#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data/reconciliation/OMEGA_GAP_REDUCTION_RECEIPT_20260829.v1.json"
LEDGER = ROOT / "data/reconciliation/OMEGA_OPERATIONAL_WORK_LEDGER_20260829.v2.json"


def load(path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL: " + message)


def main():
    r = load(RECEIPT)
    l = load(LEDGER)

    require(r["claim_allowed"] is False, "receipt must remain claim-gated")
    require(r["release_allowed"] is False, "receipt must remain release-gated")
    require(r["promotion_allowed"] is False, "receipt must remain promotion-gated")
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
    require(p["mutation_completed"] is False, "binary relocation cannot be claimed before verified write")
    require(p["status"] == "PENDING_BINARY_PRESERVING_WRITE", "binary relocation state drift")

    raw = r["raw018"]
    require(raw["canonical_path"] == "conversations-018.json", "RAW018 path drift")
    require(raw["declared_size_bytes"] == 12115336, "RAW018 declared size drift")
    require(raw["pid_count"] == 100, "RAW018 PID commitment cardinality drift")
    require(raw["candidate_set_sha256"] == "766644f8a199de4317500e6f40d44f9187f767e2ea453910ab4a4d0ec8cfc69e", "RAW018 PID commitment drift")
    require("LISTING_MISS != GLOBAL_ABSENCE" in raw["anti_regression"], "RAW018 search-miss anti-regression missing")

    protected = set(r["protected_open_placeholders"])
    require("TOKEN_VAZIO_MATRIX_C_IDENTITY" in protected, "Matrix C identity must not be fabricated")
    require("TOKEN_VAZIO_MATRIX_C_FORMULA" in protected, "Matrix C formula must not be fabricated")

    require("VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM" in l["anti_regression"], "core epistemic invariant missing")
    print("PASS: omega gap reduction receipt v1 + operational ledger v2")


if __name__ == "__main__":
    main()
