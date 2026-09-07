#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POINTER = ROOT / "indices/ATLAS_X_MESSAGE_PROVENANCE_CURRENT_V1.json"
RECEIPT = ROOT / "receipts/2026-09-07_ATLAS_MESSAGE_PROVENANCE_CUSTODY_V1.json"

ROLE_MAP = {
    "user": "USER_SOURCE",
    "assistant": "MODEL_OUTPUT",
    "system": "SYSTEM_SOURCE",
    "tool": "TOOL_SOURCE",
}


def require(condition, reason):
    if not condition:
        raise SystemExit("FAIL_CLOSED:" + reason)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    pointer = load(POINTER)
    receipt = load(RECEIPT)

    require(pointer["schema"] == "rafaelia.atlas_message_provenance_pointer/v1", "pointer_schema")
    require(receipt["schema"] == "rafaelia.atlas_message_provenance_receipt/v1", "receipt_schema")
    require(pointer["route_id"] == receipt["route_id"] == "ATLAS:X-MESSAGE-PROVENANCE-CUSTODY-20260907", "route_id")
    require(pointer["state"] == "TERMUX_MERGED_LLAMA_SOURCE_READY_REMOTE_EXECUTION_GATED", "state")
    require(pointer["claim_allowed"] is False and receipt["claim_allowed"] is False, "claim_gate")
    require(pointer["weight_training_authorized"] is False and receipt["weight_training_authorized"] is False, "training_gate")
    require(receipt["weights_modified"] is False and receipt["raw_novoexport_mutated"] is False, "mutation_gate")

    contract = pointer["contract"]
    require(contract["id"] == receipt["contract"]["id"] == "MESSAGE_ROLE_BOUND_V1", "contract_id")
    require(contract["semantics"] == ROLE_MAP, "role_map")
    require(receipt["contract"]["message_role_mapping"] == ROLE_MAP, "receipt_role_map")
    require(contract["lexical_origin_inferred"] is False and receipt["contract"]["lexical_origin_inferred"] is False, "lexical_overclaim")
    for key in ("USER_RETRANSMISSION", "THIRD_PARTY_CODE", "MODEL_LABEL"):
        require(contract["unresolved_content_classes"].get(key) == "TOKEN_VAZIO_CONTENT_CLASSIFICATION", "content_gap:" + key)
        require(receipt["contract"]["content_level_classes"].get(key) == "TOKEN_VAZIO_CONTENT_CLASSIFICATION", "receipt_content_gap:" + key)

    termux = pointer["termux_evidence"]
    require(termux["merge_state"] == "MERGED", "termux_merge_state")
    require(termux["merge_commit"] == receipt["termux"]["merge_commit"] == "82e71419d606428e75279d6e6b545f4497de3de7", "termux_merge")
    require(all(v["conclusion"] == "SUCCESS" for v in termux["gates"].values()), "termux_relevant_gate")
    require(termux["orthogonal_external_gate"]["provider_protection_gate"]["conclusion"] == "FAILURE", "external_failure_erased")
    require(termux["orthogonal_external_gate"]["provider_protection_gate"]["promotion"] == "DENIED", "external_failure_promoted")

    llama = pointer["llama_evidence"]
    require(llama["merge_state"] == "OPEN_UNMERGED" and receipt["llama"]["merged"] is False, "llama_unproven_merge")
    require(llama["remote_execution_state"] == "TOKEN_VAZIO_REMOTE_EXECUTION", "llama_remote_state")
    require(llama["gap"] == receipt["llama"]["gap"] == "TV-LLAMA-ACTIONS-PRESTEP-REMOTE-EXECUTION", "llama_gap")
    require(llama["root_cause"] == receipt["llama"]["root_cause"] == "TOKEN_VAZIO", "llama_root_cause_overclaim")
    require(receipt["llama"]["initial_job_steps"] == 0 and receipt["llama"]["rerun_job_steps"] == 0, "llama_steps_fabricated")

    required_route = ["ATLAS:X", "NOVO:X", "L:X", "O:X", "T:X", "REL:X", "SCALE:X", "EVID:X", "GAP:X", "LEARN:X"]
    require(pointer["route"] == required_route, "route_order")
    require("DATASET_INFORMS != MISSION_AUTHORITY" in pointer["mission_invariants"], "dataset_authority")
    require("RETRIEVAL_CONTEXT != WEIGHT_UPDATE" in pointer["mission_invariants"], "retrieval_training")
    require("MESSAGE_ROLE_PROVENANCE != LEXICAL_AUTHORSHIP" in pointer["mission_invariants"], "message_lexical_boundary")

    print("message_provenance_custody_v1: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
