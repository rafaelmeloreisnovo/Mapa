#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"data"/"governance"/"gap_of_gaps_current_v1.json"

def main():
    o=json.loads(P.read_text(encoding="utf-8"))
    assert o["schema"]=="rafaelia.gap-of-gaps-current.v1"
    assert o["claim_allowed"] is False
    assert o["architecture_state"]["state"]=="STRUCTURAL_PASS_MERGED"
    assert o["architecture_state"]["provider_governance_is_separate"] is True
    uids=set()
    for e in o["entries"]:
        assert e["uid"] not in uids, e["uid"]
        uids.add(e["uid"])
        for k in ("state","authority","summary","provenance","next_action","closure_criterion","falsifier"):
            assert isinstance(e[k],str) and e[k], (e["uid"],k)
        assert e["claim_allowed"] is False
    assert any("TOKEN_VAZIO" in e["state"] for e in o["entries"])
    assert any(e["source_id"]=="GOV-MAPA-PROVIDER-RULESET" for e in o["entries"])
    assert any(e["source_id"]=="STATE-HOTSTATE-SUCCESSOR" for e in o["entries"])
    print("PASS gap_of_gaps_current_v1")
    print(json.dumps(o["counts"],sort_keys=True))
if __name__=="__main__":
    main()
