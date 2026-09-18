#!/usr/bin/env python3
import json,sys
from pathlib import Path

p=Path(sys.argv[1] if len(sys.argv)>1 else "data/governance/SYSTEMATIC_PRAGMATIC_TERMINAL_ASSURANCE_V1.json")
d=json.loads(p.read_text(encoding="utf-8"))
assert d["schema"]=="rafaelia.systematic-pragmatic-terminal-assurance/v1"
assert d["claim_allowed"] is False
assert d["publication_ready"] is False
assert d["autonomous_objective_creation"] is False
s=d["structural_routing"]
assert s["state"]=="COMPLETE_STRUCTURAL_ROUTING"
assert s["source_gap_bindings"]==35
assert s["schema_families_structurally_resolved"]==25
assert s["remaining_internal_review_required"]==0
assert s["remaining_internal_binding_token_vazio_count"]==0
assert len(d["internal_regressions"])==2
assert all(x["local_code_change_authorized"] is True for x in d["internal_regressions"])
assert len(d["external_gates"])==4
assert all(x["local_code_change_authorized"] is False for x in d["external_gates"])
t=d["terminal_semantics"]
assert t["structural_routing_complete"] is True
assert t["repository_operational_readiness"]=="BLOCKED_BY_EXTERNAL_GATES"
assert t["external_gate_failure_does_not_reopen_structural_routing"] is True
assert t["external_gate_failure_remains_explicit"] is True
assert t["source_record_binding_is_subject_closure"] is False
print(json.dumps({"status":"PASS","structural_routing":"COMPLETE","external_gates":4,"claim_allowed":False},sort_keys=True))
