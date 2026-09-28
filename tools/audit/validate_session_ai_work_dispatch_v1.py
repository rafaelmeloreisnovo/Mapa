#!/usr/bin/env python3
import json, sys
from pathlib import Path
REQUIRED_PACKET={'id','alpha_summary','delta','layer_class','agents','workstreams','authority','source_min','execution_target','evidence_rule','status','omega_exit'}
REQUIRED_ROUTE={'route_id','source_ref','target_ref','relation_type','owner','authority','predecessor','successor','dependency_edges','evidence_ref','receipt_ref','rollback_ref','replay_recipe','reproduction_state','privacy_class','retention_class','claim_allowed','hash_ref'}
ALLOWED_LAYERS={'BODY','SOUL','SPIRIT'}
def die(msg): raise SystemExit('FAIL: '+msg)
def validate(data):
    if data.get('schema')!='RAFAELIA_SESSION_AI_WORK_DISPATCH_V1': die('unexpected schema')
    if data.get('claim_allowed') is not False: die('claim_allowed must be false')
    inv=set(data.get('invariants',[]))
    for x in ('SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM','TOKEN_VAZIO != 0','IMPLEMENTED_UNTESTED != PASS','AGENT_ASSIGNMENT != AGENT_EXECUTION'):
        if x not in inv: die('missing invariant: '+x)
    roles=data.get('agent_roles',[]); ids=[r.get('id') for r in roles]
    if not ids or len(ids)!=len(set(ids)): die('agent role IDs must be unique/non-empty')
    role_set=set(ids); packets=data.get('session_packets',[])
    if not packets: die('session_packets empty')
    pids=[]
    for p in packets:
        miss=REQUIRED_PACKET-set(p)
        if miss: die(f"{p.get('id')}: missing {sorted(miss)}")
        if len(p['source_min'])>3: die(f"{p['id']}: source_min > 3")
        if not set(p['layer_class']).issubset(ALLOWED_LAYERS): die(f"{p['id']}: invalid layer_class")
        if not set(p['agents']).issubset(role_set): die(f"{p['id']}: unknown agent")
        if p.get('claim_allowed') is not False: die(f"{p['id']}: claim_allowed must be false")
        for k in ('authority','execution_target','evidence_rule'):
            if not str(p[k]).strip(): die(f"{p['id']}: blank {k}")
        pids.append(p['id'])
    if len(pids)!=len(set(pids)): die('duplicate packet IDs')
    if set(data.get('route_pin_required',[]))!=REQUIRED_ROUTE: die('route_pin_required contract drift')
    drive=data.get('drive_localities',{})
    for k in ('atlas','routes','edges','evidence','receipts'):
        if not drive.get(k,{}).get('id'): die('missing drive locality '+k)
    return {'status':'PASS','roles':len(roles),'packets':len(packets),'claim_allowed':False}
def main():
    if len(sys.argv)!=2: die('usage: validator <registry.json>')
    data=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    print(json.dumps(validate(data),sort_keys=True))
if __name__=='__main__': main()
