#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"data"/"governance"/"provider_governance_closure_v1.json"

def main():
    o=json.loads(P.read_text(encoding="utf-8"))
    assert o["schema"]=="rafaelia.provider-governance-closure.v1"
    assert o["claim_allowed"] is False
    assert o["separation"]["architecture_state"]=="STRUCTURAL_PASS_MERGED"
    assert o["separation"]["provider_state"]=="BLOCKED_EXTERNAL_CONFIGURATION"
    assert o["apply_contract"]["no_merge_endpoint"] is True
    assert o["apply_contract"]["expected_main_sha_required"] is True
    assert o["current_execution_surface"]["branch_protection_mutation_action"].startswith("TOKEN_VAZIO")
    ids={g["id"] for g in o["gaps"]}
    required={
      "GOV-MAPA-PROVIDER-RULESET",
      "GOV-MAPA-SERVER-MERGE-ENFORCEMENT",
      "GOV-MAPA-CODESCAN-CREDENTIALS",
      "GOV-MAPA-PROMOTION-CONTROL",
      "GOV-MAPA-ZERO-APPROVAL-REJECTION-RECEIPT"
    }
    assert required <= ids
    print("PASS provider_governance_closure_v1")
if __name__=="__main__":
    main()
