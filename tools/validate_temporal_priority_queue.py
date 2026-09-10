#!/usr/bin/env python3
"""Fail-closed validator for the current RAFAELIA uncertainty/gap routing layer."""
from __future__ import annotations
import argparse,json,re,sys
from datetime import datetime,timezone
from pathlib import Path
from typing import Any
HEX40=re.compile(r"^[0-9a-f]{40}$")
PRIORITIES={"P0","P1","P2","P3"}
REQUIRED_OPEN_FIELDS={"priority","id","state","scope","authority","evidence","uncertainty","falsifier","closure_gate","next_action"}
FORBIDDEN_ACTIVE_IDS={"TV-ROOT-PNG-STRUCTURAL-CI-BLOCKER","TV-GENESIS-SEAL-EXACT-SHA256","TV-RAW018-CURRENT-BYTE-CUSTODY","TV-RAW018-PID-COMMITMENT-ALGORITHM-PROVENANCE","TV-RAW018-CHRONOLOGICAL-COMMITMENT-CURRENT-REPRODUCTION","TOKEN_VAZIO_RUNNER"}
MANDATORY_ACTIVE_IDS={"P0-MAIN-SERVER-ENFORCEMENT","P0-INDEPENDENT-APPROVAL"}
def fail(errors:list[str],message:str)->None: errors.append(message)
def nonempty_list(value:Any)->bool: return isinstance(value,list) and bool(value) and all(isinstance(item,str) and item.strip() for item in value)
def parse_iso(value:Any):
    if not isinstance(value,str) or not value.strip(): return None
    try: dt=datetime.fromisoformat(value.replace("Z","+00:00"))
    except ValueError: return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
def validate(data:dict[str,Any],now:datetime|None=None)->list[str]:
    errors=[]
    if data.get("schema")!="rafaelia.token-vazio-priority-queue.v4": fail(errors,"SCHEMA_MISMATCH")
    if data.get("claim_allowed") is not False: fail(errors,"CLAIM_ALLOWED_MUST_BE_FALSE")
    if data.get("release_allowed") is not False: fail(errors,"RELEASE_ALLOWED_MUST_BE_FALSE")
    if data.get("promotion_allowed") is not False: fail(errors,"PROMOTION_ALLOWED_MUST_BE_FALSE")
    if data.get("history_policy")!="APPEND_ONLY_PRESERVE_PREDECESSOR": fail(errors,"APPEND_ONLY_HISTORY_POLICY_REQUIRED")
    if data.get("latest_evidence_wins_for_routing") is not True: fail(errors,"LATEST_EVIDENCE_ROUTING_REQUIRED")
    if data.get("unresolved_untyped_gaps")!=0: fail(errors,"UNTYPED_GAPS_MUST_BE_ZERO")
    source_sha=data.get("source_main_sha")
    if not isinstance(source_sha,str) or not HEX40.fullmatch(source_sha): fail(errors,"SOURCE_MAIN_SHA_INVALID")
    snapshot=data.get("provider_snapshot")
    if not isinstance(snapshot,dict): fail(errors,"PROVIDER_SNAPSHOT_REQUIRED")
    else:
        if snapshot.get("main_sha")!=source_sha: fail(errors,"PROVIDER_MAIN_SHA_BINDING_MISMATCH")
        observed_at=parse_iso(snapshot.get("observed_at")); evidence_at=parse_iso(data.get("evidence_updated_at")); max_hours=snapshot.get("freshness_max_hours")
        if observed_at is None: fail(errors,"PROVIDER_OBSERVED_AT_INVALID")
        if evidence_at is None: fail(errors,"EVIDENCE_UPDATED_AT_INVALID")
        if not isinstance(max_hours,(int,float)) or max_hours<=0 or max_hours>168: fail(errors,"FRESHNESS_MAX_HOURS_INVALID")
        if observed_at and evidence_at and observed_at!=evidence_at: fail(errors,"PROVIDER_EVIDENCE_TIMESTAMP_MISMATCH")
        rulesets=snapshot.get("repository_rulesets")
        if not isinstance(rulesets,list): fail(errors,"PROVIDER_RULESETS_NOT_LIST")
        else:
            seen=set()
            for i,row in enumerate(rulesets):
                if not isinstance(row,dict): fail(errors,f"PROVIDER_RULESET[{i}]:NOT_OBJECT"); continue
                rid=row.get("id")
                if not isinstance(rid,int): fail(errors,f"PROVIDER_RULESET[{i}]:INVALID_ID")
                elif rid in seen: fail(errors,f"DUPLICATE_PROVIDER_RULESET:{rid}")
                else: seen.add(rid)
                if row.get("enforcement") not in {"disabled","active","evaluate"}: fail(errors,f"PROVIDER_RULESET[{i}]:INVALID_ENFORCEMENT")
        if observed_at and isinstance(max_hours,(int,float)) and max_hours>0:
            current=now or datetime.now(timezone.utc); age=(current.astimezone(timezone.utc)-observed_at.astimezone(timezone.utc)).total_seconds()/3600
            if age < -1: fail(errors,"PROVIDER_SNAPSHOT_FROM_FUTURE")
            elif age > max_hours: fail(errors,f"PROVIDER_SNAPSHOT_STALE:{age:.2f}h>{max_hours}h")
    active=data.get("active_items"); resolved=data.get("resolved_or_superseded")
    if not isinstance(active,list): fail(errors,"ACTIVE_ITEMS_NOT_LIST"); active=[]
    if not isinstance(resolved,list): fail(errors,"RESOLVED_ITEMS_NOT_LIST"); resolved=[]
    ids=set(); active_ids=set()
    for index,item in enumerate(active):
        prefix=f"active_items[{index}]"
        if not isinstance(item,dict): fail(errors,f"{prefix}:NOT_OBJECT"); continue
        missing=REQUIRED_OPEN_FIELDS-item.keys()
        if missing: fail(errors,f"{prefix}:MISSING_FIELDS:{','.join(sorted(missing))}")
        gap_id=item.get("id")
        if not isinstance(gap_id,str) or not gap_id.strip(): fail(errors,f"{prefix}:INVALID_ID"); continue
        if gap_id in ids: fail(errors,f"DUPLICATE_ID:{gap_id}")
        ids.add(gap_id); active_ids.add(gap_id)
        if item.get("priority") not in PRIORITIES: fail(errors,f"{gap_id}:INVALID_PRIORITY")
        state=item.get("state")
        if not isinstance(state,str) or not state.strip(): fail(errors,f"{gap_id}:INVALID_STATE")
        for field in ("scope","evidence","closure_gate"):
            if not nonempty_list(item.get(field)): fail(errors,f"{gap_id}:{field.upper()}_EMPTY")
        for field in ("authority","uncertainty","falsifier","next_action"):
            value=item.get(field)
            if not isinstance(value,str) or not value.strip(): fail(errors,f"{gap_id}:{field.upper()}_EMPTY")
    for gap_id in sorted(active_ids&FORBIDDEN_ACTIVE_IDS): fail(errors,f"STALE_RESOLVED_GAP_REACTIVATED:{gap_id}")
    for gap_id in sorted(MANDATORY_ACTIVE_IDS-active_ids): fail(errors,f"MANDATORY_P0_MISSING:{gap_id}")
    resolved_ids=set()
    for index,item in enumerate(resolved):
        prefix=f"resolved_or_superseded[{index}]"
        if not isinstance(item,dict): fail(errors,f"{prefix}:NOT_OBJECT"); continue
        gap_id=item.get("id"); state=item.get("state"); evidence=item.get("evidence")
        if not isinstance(gap_id,str) or not gap_id.strip(): fail(errors,f"{prefix}:INVALID_ID"); continue
        if gap_id in ids: fail(errors,f"ID_ACTIVE_AND_RESOLVED:{gap_id}")
        if gap_id in resolved_ids: fail(errors,f"DUPLICATE_RESOLVED_ID:{gap_id}")
        resolved_ids.add(gap_id); ids.add(gap_id)
        if not isinstance(state,str) or not state.strip(): fail(errors,f"{gap_id}:INVALID_RESOLVED_STATE")
        if not nonempty_list(evidence): fail(errors,f"{gap_id}:RESOLUTION_EVIDENCE_EMPTY")
    for gap_id in sorted(FORBIDDEN_ACTIVE_IDS-resolved_ids): fail(errors,f"EXPECTED_RESOLUTION_ROW_MISSING:{gap_id}")
    invariants=data.get("invariants")
    if not nonempty_list(invariants): fail(errors,"INVARIANTS_EMPTY")
    else:
        required={"TOKEN_VAZIO != 0","resolved != deleted_history","latest_evidence_wins_for_current_routing","provider_snapshot.main_sha == source_main_sha"}
        for invariant in sorted(required-set(invariants)): fail(errors,f"REQUIRED_INVARIANT_MISSING:{invariant}")
    return errors
def main()->int:
    parser=argparse.ArgumentParser(); parser.add_argument("path",nargs="?",default="data/control-plane/TOKEN_VAZIO_PRIORITY_QUEUE.v4.json"); args=parser.parse_args(); path=Path(args.path)
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc: print(f"FAIL: unable to read/parse {path}: {exc}",file=sys.stderr); return 2
    if not isinstance(data,dict): print("FAIL: queue root must be an object",file=sys.stderr); return 2
    errors=validate(data)
    if errors:
        for error in errors: print(f"FAIL: {error}",file=sys.stderr)
        print(f"RESULT: FAIL ({len(errors)} finding(s))",file=sys.stderr); return 1
    print(f"PASS: {path}"); print(f"active_items={len(data['active_items'])}"); print(f"resolved_or_superseded={len(data['resolved_or_superseded'])}"); print(f"provider_main_sha={data['provider_snapshot']['main_sha']}"); print(f"provider_rulesets={len(data['provider_snapshot']['repository_rulesets'])}"); print("claim_allowed=false"); return 0
if __name__=="__main__": raise SystemExit(main())
