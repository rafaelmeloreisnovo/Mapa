#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path
from typing import Any

SCHEMA='mapa.platform-assurance-pointer.v1'
SHA40=re.compile(r'^[0-9a-f]{40}$')
SHA64=re.compile(r'^[0-9a-f]{64}$')
P0_IDS={
 'WI-TERMUX-CI-289','WI-TERMUX-LOADER-290','WI-RLL-FASE29-582',
 'WI-TERMUX-DEVICE-RECEIPT','WI-PLATFORM-CI-EXECUTION'
}
STATES={'MERGED_LIMITED','BLOCKED','TOKEN_VAZIO'}

class ValidationError(ValueError): pass

def require(c: bool, m: str)->None:
    if not c: raise ValidationError(m)

def load(path: Path)->dict[str,Any]:
    try: d=json.loads(path.read_text(encoding='utf-8'))
    except (OSError,json.JSONDecodeError) as e: raise ValidationError(str(e)) from e
    require(isinstance(d,dict),'root must be object'); return d

def digest(data:dict[str,Any])->str:
    clone=json.loads(json.dumps(data)); clone.setdefault('integrity',{})['digest']=''
    raw=json.dumps(clone,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    return hashlib.blake2b(raw,digest_size=32).hexdigest()

def validate(data:dict[str,Any], observed_producer_head:str|None=None)->dict[str,Any]:
    require(data.get('schema')==SCHEMA,'invalid schema')
    require(data.get('authority_repository')=='rafaelmeloreisnovo/Mapa','Mapa authority required')
    require(data.get('claim_allowed') is False,'claim_allowed must remain false')
    require(data.get('state') in {'ACTIVE_CONTROL_PLANE_WITH_OPEN_BLOCKERS','STALE_POINTER'},'invalid state')
    producer=data.get('producer'); require(isinstance(producer,dict),'producer object required')
    require(producer.get('repository')=='rafaelmeloreisnovo/RafGitTools','producer authority mismatch')
    require(isinstance(producer.get('pull_request'),int) and producer['pull_request']>0,'producer PR required')
    require(bool(SHA40.fullmatch(str(producer.get('merge_commit','')))),'producer merge SHA invalid')
    require(bool(SHA64.fullmatch(str(producer.get('index_digest','')))),'producer index digest invalid')
    for k in ('index_path','control_path','validator_path'):
        require(isinstance(producer.get(k),str) and producer[k],'producer path missing')
    scope=data.get('scope'); require(isinstance(scope,dict),'scope object required')
    require(scope.get('repository_count')==6,'repository_count must be 6')
    require(scope.get('work_item_count')==12,'work_item_count must be 12')
    require(scope.get('priority_counts')=={'P0':5,'P1':5,'P2':2},'priority_counts mismatch')
    require(scope.get('state_counts')=={'BLOCKED':5,'MERGED_LIMITED':1,'PARTIAL':2,'TOKEN_VAZIO':4},'state_counts mismatch')
    require(scope.get('open_blocking_count')==9,'open_blocking_count mismatch')
    require(scope.get('promotion_ready_count')==0,'promotion_ready_count must be zero')
    require(scope.get('claim_allowed') is False,'scope claim_allowed must be false')
    routes=data.get('p0_routes'); require(isinstance(routes,list) and len(routes)==5,'five P0 routes required')
    ids=set(); merged=0
    for i,r in enumerate(routes):
        require(isinstance(r,dict),f'p0_routes[{i}] object required')
        rid=r.get('id'); require(rid in P0_IDS,f'unknown P0 id: {rid}')
        require(rid not in ids,f'duplicate P0 id: {rid}'); ids.add(rid)
        require(r.get('state') in STATES,f'{rid}: invalid state')
        require(isinstance(r.get('repository'),str) and '/' in r['repository'],f'{rid}: repository invalid')
        require(isinstance(r.get('source'),str) and r['source'],f'{rid}: source required')
        if r['state']=='MERGED_LIMITED': merged+=1
    require(ids==P0_IDS,'P0 route coverage mismatch')
    require(merged==1,'exactly one MERGED_LIMITED P0 route required')
    boundaries=data.get('boundaries'); require(isinstance(boundaries,dict),'boundaries object required')
    for key in ('automatic_cross_repository_write','automatic_merge','claim_allowed','map_copies_control_plane_logic','map_elevates_work_item_state','public_file_is_public_domain','security_blocker_is_compensable','zero_step_is_pass'):
        require(boundaries.get(key) is False,f'boundary {key} must be false')
    drift=data.get('drift_policy'); require(isinstance(drift,dict),'drift_policy object required')
    observed=drift.get('observed_producer_ref'); require(bool(SHA40.fullmatch(str(observed or ''))),'observed producer ref invalid')
    require(observed==producer['merge_commit'],'observed producer ref must equal pinned merge')
    require(drift.get('stale_if_producer_head_differs') is True,'drift must fail stale')
    require(drift.get('stale_state')=='STALE_POINTER','stale state invalid')
    req=drift.get('refresh_requires'); require(isinstance(req,list) and len(req)>=4,'refresh requirements incomplete')
    expected=digest(data); require(data.get('integrity',{}).get('algorithm')=='blake2b-256','integrity algorithm invalid')
    require(data.get('integrity',{}).get('digest')==expected,'integrity digest mismatch')
    observed_state=data['state']; reasons=[]
    if observed_producer_head is not None:
        require(bool(SHA40.fullmatch(observed_producer_head)),'observed producer head invalid')
        if observed_producer_head!=producer['merge_commit']:
            observed_state='STALE_POINTER'; reasons.append('producer head differs from pinned merge')
    return {'status':'PASS','pointer_state':observed_state,'reasons':reasons,'producer_merge_commit':producer['merge_commit'],'index_digest':producer['index_digest'],'p0_routes':len(routes),'open_blocking_count':scope['open_blocking_count'],'promotion_ready_count':0,'claim_allowed':False,'integrity_digest':expected}

def main(argv=None)->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--path',type=Path,default=Path('indices/PLATFORM_ASSURANCE_CONTROL_PLANE.json')); ap.add_argument('--observed-producer-head'); ap.add_argument('--write-report',type=Path)
    a=ap.parse_args(argv)
    try: out=validate(load(a.path),a.observed_producer_head)
    except ValidationError as e: print(json.dumps({'status':'FAIL','error':str(e)},ensure_ascii=False),file=sys.stderr); return 1
    text=json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    if a.write_report: a.write_report.parent.mkdir(parents=True,exist_ok=True); a.write_report.write_text(text,encoding='utf-8')
    print(text,end=''); return 0
if __name__=='__main__': raise SystemExit(main())
