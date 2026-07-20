#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
from typing import Any

SCHEMA = "mapa.iso-operational-readiness.v1"
PRIORITIES = {"P0", "P1", "P2", "P3"}
LEVELS = {0, 1, 2, 3, 4, 5}

class ValidationError(ValueError): pass

def require(condition: bool, message: str) -> None:
    if not condition: raise ValidationError(message)

def load(path: Path) -> dict[str, Any]:
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc: raise ValidationError(str(exc)) from exc
    require(isinstance(data,dict),"root must be an object"); return data

def canonical_digest(data: dict[str, Any]) -> str:
    clone=json.loads(json.dumps(data)); clone.setdefault("integrity",{})["digest"]=""
    payload=json.dumps(clone,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    return hashlib.blake2b(payload,digest_size=32).hexdigest()

def validate(data: dict[str, Any]) -> dict[str, Any]:
    require(data.get("schema")==SCHEMA,"invalid schema")
    require(data.get("authority_repository")=="rafaelmeloreisnovo/Mapa","Mapa authority required")
    require(data.get("assessment_type")=="CONSERVATIVE_OPERATIONAL_READINESS_NOT_CERTIFICATION","assessment type must remain conservative")
    require(data.get("claim_allowed") is False,"claim_allowed must remain false")
    require(data.get("certification_claim") is False,"certification claim is forbidden")
    require(data.get("conformity_claim") is False,"conformity claim is forbidden")
    boundaries=data.get("boundaries"); require(isinstance(boundaries,dict) and boundaries,"boundaries required")
    for key,value in boundaries.items(): require(value is False,f"boundary {key} must be false")

    observed=data.get("observed_state"); require(isinstance(observed,dict),"observed_state required")
    total,materialized,vazio=(observed.get("repositories_observed"),observed.get("repositories_materialized"),observed.get("repositories_token_vazio"))
    require((total,materialized,vazio)==(126,51,75),"inventory observation mismatch")
    require(materialized+vazio==total,"inventory arithmetic mismatch")
    require(abs(observed.get("inventory_completeness_ratio",-1)-materialized/total)<1e-12,"inventory completeness mismatch")
    require(observed.get("inventory_state")=="PARTIAL","inventory must remain PARTIAL")
    require(observed.get("assurance_work_items")==12,"assurance work item count mismatch")
    require(observed.get("assurance_open_blockers")==9,"assurance blocker count mismatch")
    require(observed.get("assurance_promotion_ready")==0,"promotion_ready must be zero")
    require(observed.get("estimate_uncertainty_percent")>=30,"uncertainty must not be understated")

    standards=data.get("standards_references"); require(isinstance(standards,list) and len(standards)>=8,"standards reference set incomplete")
    for row in standards: require(isinstance(row,list) and len(row)==5,"standard row must have five fields")
    standard_ids=[row[0] for row in standards]; require(len(standard_ids)==len(set(standard_ids)),"duplicate standard reference")
    required={"ISO-9000-2026","ISO-9001-2015","ISO-8000-8-2015","ISO-8000-51-2023","ISO-8000-63-2019","ISO-IEC-27000-2026","ISO-IEC-27001-2022","ISO-IEC-27002-2022"}
    require(required.issubset(set(standard_ids)),"missing standard reference")

    scope=data.get("core_scope_repositories"); require(isinstance(scope,list) and len(scope)==8,"eight core repositories required")
    require(len(scope)==len(set(scope)),"duplicate core repository")

    efforts=data.get("effort_scenarios"); require(isinstance(efforts,list) and len(efforts)==5,"five effort scenarios required")
    ids=set()
    for row in efforts:
        require(isinstance(row,list) and len(row)==10,"effort row must have ten fields")
        eid,_,pmin,pmax,hmin,hmax,cmin,cmax,unit,_=row
        require(eid not in ids,"duplicate effort id"); ids.add(eid)
        require(all(isinstance(v,int) for v in (pmin,pmax,hmin,hmax,cmin,cmax)),f"{eid}: integer ranges required")
        require(0<pmin<=pmax and 0<hmin<=hmax and 0<cmin<=cmax,f"{eid}: invalid range")
        require(unit in {"weeks","months"},f"{eid}: invalid calendar unit")
    core=next(row for row in efforts if row[0]=="E03")
    require((core[2],core[3],core[4],core[5])==(14,16,10300,15800),"core estimate changed without review")

    roles=data.get("recommended_roles"); require(isinstance(roles,list) and len(roles)==14,"fourteen baseline roles required")
    for row in roles: require(isinstance(row,list) and len(row)==5,"role row must have five fields")
    role_ids=[row[0] for row in roles]; require(len(role_ids)==len(set(role_ids)),"duplicate role id")
    require(sum(row[2] for row in roles)==14,"baseline role count must be 14")

    areas=data.get("maturity_areas"); require(isinstance(areas,list) and len(areas)>=13,"maturity area coverage incomplete")
    area_ids=set()
    for row in areas:
        require(isinstance(row,list) and len(row)==6,"maturity row must have six fields")
        aid,_,low,high,evidence,gap=row
        require(aid not in area_ids,"duplicate maturity area"); area_ids.add(aid)
        require(low in LEVELS and high in LEVELS and low<=high,f"{aid}: invalid maturity range")
        require(bool(evidence) and bool(gap),f"{aid}: evidence and gap required")

    heuristics=data.get("heuristics"); require(isinstance(heuristics,list) and len(heuristics)==30,"exactly thirty heuristics required")
    for row in heuristics: require(isinstance(row,list) and len(row)==4,"heuristic row must have four fields")
    heuristic_ids=[row[0] for row in heuristics]; require(len(heuristic_ids)==len(set(heuristic_ids)),"duplicate heuristic id")
    require(set(heuristic_ids)=={f"H{i:02d}" for i in range(1,31)},"heuristic ID coverage mismatch")
    categories={row[1] for row in heuristics}; require(len(categories)>=12,"heuristics are not sufficiently diverse")
    for row in heuristics: require(all(isinstance(v,str) and v for v in row),f"{row[0]}: incomplete heuristic")

    gaps=data.get("gap_ledger"); require(isinstance(gaps,list) and len(gaps)>=25,"gap ledger incomplete")
    for row in gaps: require(isinstance(row,list) and len(row)==9,"gap row must have nine fields")
    gap_ids=[row[0] for row in gaps]; require(len(gap_ids)==len(set(gap_ids)),"duplicate gap id")
    priorities={p:0 for p in PRIORITIES}
    for row in gaps:
        gid,priority,_,finding,next_action,exit_criteria,owners,hmin,hmax=row
        require(priority in PRIORITIES,f"{gid}: invalid priority"); priorities[priority]+=1
        require(bool(finding) and bool(next_action) and bool(exit_criteria),f"{gid}: finding/action/exit criteria required")
        require(isinstance(owners,list) and owners,f"{gid}: owner role required")
        require(set(owners).issubset(set(role_ids)),f"{gid}: unknown owner role")
        require(isinstance(hmin,int) and isinstance(hmax,int) and 0<hmin<=hmax,f"{gid}: invalid hours")

    derived=data.get("derived"); require(isinstance(derived,dict),"derived required")
    require(derived.get("role_count")==14,"derived role count mismatch")
    require(derived.get("heuristic_count")==30,"derived heuristic count mismatch")
    require(derived.get("heuristic_category_count")==len(categories),"derived category count mismatch")
    require(derived.get("gap_count")==len(gaps),"derived gap count mismatch")
    require(derived.get("gap_priority_counts")==priorities,"derived priority counts mismatch")
    require(derived.get("p0_p1_gap_count")==priorities["P0"]+priorities["P1"],"derived P0/P1 count mismatch")
    require(derived.get("recommended_strategy")=="DELTA_FIRST_RISK_BASED_WAVES","strategy mismatch")
    require(derived.get("claim_allowed") is False,"derived claim boundary mismatch")

    integrity=data.get("integrity"); require(isinstance(integrity,dict),"integrity required")
    require(integrity.get("algorithm")=="blake2b-256","integrity algorithm mismatch")
    expected=canonical_digest(data); require(integrity.get("digest")==expected,"integrity digest mismatch")
    return {"status":"PASS","assessment_type":data["assessment_type"],"repositories_materialized":materialized,"repositories_token_vazio":vazio,"heuristic_count":len(heuristics),"heuristic_category_count":len(categories),"gap_count":len(gaps),"gap_priority_counts":priorities,"baseline_roles":14,"core_hours_min":core[4],"core_hours_max":core[5],"claim_allowed":False,"certification_claim":False,"integrity_digest":expected}

def main(argv=None)->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--path",type=Path,default=Path("indices/ISO_OPERATIONAL_READINESS_BASELINE.json")); ap.add_argument("--write-report",type=Path); a=ap.parse_args(argv)
    try: result=validate(load(a.path))
    except ValidationError as exc: print(json.dumps({"status":"FAIL","error":str(exc)},ensure_ascii=False),file=sys.stderr); return 1
    text=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if a.write_report: a.write_report.parent.mkdir(parents=True,exist_ok=True); a.write_report.write_text(text,encoding="utf-8")
    print(text,end=""); return 0
if __name__=="__main__": raise SystemExit(main())
