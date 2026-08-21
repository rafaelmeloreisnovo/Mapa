#!/usr/bin/env python3
import json, sys
from pathlib import Path
p=Path('governance/RAFAELIA_ADAPTIVE_RESILIENCE_WATCHDOG_V1.json')
d=json.loads(p.read_text())
errors=[]
def req(cond,msg):
    if not cond: errors.append(msg)
req(d.get('claim_allowed') is False,'claim_allowed must remain false')
inv=set(d.get('invariants',[]))
for x in ['prediction != evidence','sandbox_pass != production_pass','TOKEN_VAZIO != PASS','P0_non_compensatory = true']:
    req(x in inv,f'missing invariant: {x}')
req(d.get('triggers',{}).get('P0','').startswith('immediate HOLD'),'P0 must HOLD')
req(d.get('watchdog',{}).get('stale_state_action')=='FAIL_CLOSED_HOLD','watchdog stale state must fail closed')
req('attacking third-party systems' in d.get('sandbox_self_test',{}).get('forbidden',[]),'sandbox must forbid third-party attack')
req(d.get('rollback',{}).get('otherwise')=='HOLD_FOR_AUTHORITY','ambiguous rollback must hold for authority')
req('it never changes claim_allowed' in d.get('predictive_layer',{}).get('rule',''),'prediction must not promote claim')
req(d.get('closure',{}).get('append_only') is True,'closure must be append-only')
if errors:
    print('FAIL')
    for e in errors: print('-',e)
    sys.exit(1)
print('PASS adaptive resilience watchdog fail-closed contract')
