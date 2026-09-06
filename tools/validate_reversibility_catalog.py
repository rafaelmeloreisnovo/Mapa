#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'auditoria/reversibility/index.jsonl'
FED = ROOT / 'auditoria/reversibility/federation/registry.v1.json'

ALLOWED = {'PLANNED','EXECUTED_REVERSIBLE','ROLLBACK_AVAILABLE','ROLLED_BACK','SUPERSEDED','TOKEN_VAZIO'}
REQUIRED = {'event_id','timestamp','scope','operation','before_ref','after_ref','rollback_ref','evidence_ref','result','reversibility_state','risk_class','token_vazio','claim_allowed'}

def load_events():
    events=[]
    seen=set()
    for n,line in enumerate(INDEX.read_text(encoding='utf-8').splitlines(),1):
        if not line.strip():
            continue
        e=json.loads(line)
        missing=sorted(REQUIRED-set(e))
        if missing:
            raise SystemExit(f'line {n}: missing {missing}')
        if e['event_id'] in seen:
            raise SystemExit(f'line {n}: duplicate event_id {e["event_id"]}')
        if e['reversibility_state'] not in ALLOWED:
            raise SystemExit(f'line {n}: invalid reversibility_state')
        if e['claim_allowed'] is not False:
            raise SystemExit(f'line {n}: claim_allowed must remain false in this bounded catalog')
        if e['token_vazio'] and e['reversibility_state'] != 'TOKEN_VAZIO':
            raise SystemExit(f'line {n}: token_vazio=true requires TOKEN_VAZIO state')
        pred=e.get('predecessor_event_id')
        if pred is not None and pred not in seen:
            raise SystemExit(f'line {n}: predecessor {pred} must already exist')
        seen.add(e['event_id'])
        events.append(e)
    return events

def validate_federation():
    r=json.loads(FED.read_text(encoding='utf-8'))
    if r.get('claim_allowed') is not False:
        raise SystemExit('federation registry claim_allowed must be false')
    repos=r.get('repositories',[])
    names=[x.get('repository') for x in repos]
    if len(names) != len(set(names)):
        raise SystemExit('duplicate repository in reversibility federation registry')
    mapa=[x for x in repos if x.get('repository')=='rafaelmeloreisnovo/Mapa']
    if len(mapa)!=1 or mapa[0].get('local_reversibility_index')!='auditoria/reversibility/index.jsonl':
        raise SystemExit('Mapa local reversibility index binding invalid')
    for x in repos:
        if x.get('local_reversibility_index') is None and x.get('state')!='TOKEN_VAZIO':
            raise SystemExit(f"{x.get('repository')}: missing local index must be TOKEN_VAZIO")
    return r

def main():
    events=load_events()
    reg=validate_federation()
    print(json.dumps({
        'status':'VALIDATED_BOUNDED',
        'event_count':len(events),
        'repository_count':len(reg['repositories']),
        'claim_allowed':False,
        'limitations':['validation is repository-local','remote producer indexes are not fetched','workflow execution is separate evidence from validator presence']
    },indent=2,sort_keys=True))

if __name__=='__main__':
    main()
