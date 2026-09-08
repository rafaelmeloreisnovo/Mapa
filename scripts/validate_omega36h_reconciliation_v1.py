#!/usr/bin/env python3
import json
from pathlib import Path

P = Path("indices/ATLAS_X_OMEGA36H_RECONCILIATION_CURRENT_V1.json")
d = json.loads(P.read_text(encoding="utf-8"))

errors = []

def require(cond, msg):
    if not cond:
        errors.append(msg)

require(d.get("claim_allowed") is False, "claim_allowed must remain false")
require(d.get("global_finished") is False, "global_finished must remain false")
require(d.get("weight_training_authorized") is False, "weight training must remain unauthorized")
require(d.get("autonomous_goal_creation") is False, "autonomous goal creation must remain false")
require(d.get("scientific_claim_promotion") is False, "scientific claim promotion must remain false")

m = d.get("mission_boundary", {})
require(m.get("dataset_informs_context") is True, "dataset must inform context")
require(m.get("dataset_creates_mission_authority") is False, "dataset must not create mission authority")
require(m.get("model_output_grants_execution") is False, "model output must not grant execution")
require(m.get("model_can_create_independent_goal") is False, "model must not create an independent goal")
require(m.get("learn_updates_model_weights") is False, "LEARN must not update model weights")

obs = d.get("observed", {})
gh = obs.get("github", {})
pr557 = gh.get("pr_557", {})
require(pr557.get("merged") is True, "PR #557 merge observation missing")
require(pr557.get("submitted_reviews") == 0, "PR #557 review observation must preserve zero submitted reviews")
require(gh.get("main_protected") is False, "observed main protection state must remain false until provider evidence changes")
require(gh.get("required_status_check_enforcement") == "off", "server enforcement observation drifted")

master = obs.get("master_index", {})
require(master.get("conversation_shards") == 51, "canonical conversation shard count must be 51")
require(master.get("range") == "000..050", "canonical conversation range must be 000..050")
require(master.get("raw_conversation_bytes") == 1107289897, "canonical raw byte count drifted")
require(master.get("full_universe_claim") is False, "full universe claim must remain false")

drive = obs.get("drive", {})
require(drive.get("direct_folder_count_before_reconciliation") == 22, "pre-reconciliation live folder count must remain observed value 22")
require(drive.get("direct_folder_count_after_reconciliation_root") == 23, "post-reconciliation root folder count must remain observed value 23")

zipraf = obs.get("zipraf", {})
for gate in ("g14", "g15a", "g15b"):
    require(str(zipraf.get(gate, "")).startswith("PASS_RECORDED_SCOPE_ARMV7"), f"{gate} must stay scope-qualified")
require(str(zipraf.get("second_physical_architecture", "")).startswith("TOKEN_VAZIO"), "second physical architecture cannot be promoted without evidence")
require(str(zipraf.get("independent_external_security_audit", "")).startswith("TOKEN_VAZIO"), "external security audit cannot be promoted without evidence")

needed = {
    "SOURCE!=ARTEFATO!=EXECUCAO!=EVIDENCIA!=CLAIM",
    "TOKEN_VAZIO!=0",
    "DATASET_CONTEXT!=PROGRAM_MISSION_AUTHORITY",
    "MODEL_PROPOSAL!=EXECUTION_PERMISSION",
    "MERGED!=REVIEWED",
    "LOCAL_POLICY!=SERVER_ENFORCEMENT",
    "PLAN_COUNT!=LIVE_INVENTORY",
    "TEMPLATE!=EVIDENCE",
    "7_SEMANTIC!=7_GEOMETRIC",
}
inv = set(d.get("invariants", []))
require(needed <= inv, f"missing invariants: {sorted(needed - inv)}")

gaps = d.get("gaps", {})
require(gaps.get("github_server_enforcement") == "FAIL_PROVIDER_OBSERVED_UNENFORCED", "provider enforcement must remain observed FAIL")
for k, v in gaps.items():
    if k == "github_server_enforcement":
        continue
    require(str(v).startswith("TOKEN_VAZIO"), f"gap {k} must remain typed TOKEN_VAZIO until evidence closes it")

term = d.get("terminal", {})
require(term.get("source_side_reconciliation_closed") is True, "source-side reconciliation must be closed")
require(term.get("external_execution_closure") is False, "external execution closure must remain false")
require(term.get("terminal_allowed_now") is False, "terminal state cannot be allowed now")
require(term.get("terminal_state_promotes_scientific_claim") is False, "terminal state cannot promote scientific claim")
require(term.get("terminal_state_authorizes_weight_training") is False, "terminal state cannot authorize weight training")

if errors:
    print("OMEGA36H_RECONCILIATION=FAIL")
    for e in errors:
        print("-", e)
    raise SystemExit(1)

print("OMEGA36H_RECONCILIATION=PASS")
print("source_side_reconciliation_closed=true")
print("external_execution_closure=false")
print("claim_allowed=false")
