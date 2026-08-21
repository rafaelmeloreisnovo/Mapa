#!/usr/bin/env python3
import json, sys
from pathlib import Path
p=Path('governance/RAFAELIA_FEDERATED_OMEGA_CYCLE_20260821.v1.json')
d=json.loads(p.read_text())
err=[]
def req(c,m):
    if not c: err.append(m)
req(d.get('claim_allowed') is False,'cycle claim_allowed must remain false')
inv=set(d.get('invariants',[]))
for x in ['VISION != ARTIFACT != EXECUTION != EVIDENCE != CLAIM','TOKEN_VAZIO != 0','absence_of_evidence != evidence_of_absence','local_adapter_pass != producer_pass','policy_gate != provider_physical_barrier']:
    req(x in inv,f'missing invariant: {x}')
ledger=d.get('component_lifecycle_ledger',[])
req(len(ledger)>=5,'lifecycle ledger too small')
req(all('next_review_gate' in c and 'revalidation_rule' in c for c in ledger),'lifecycle review/revalidation missing')
gaps=d.get('operational_gaps',[])
required=['gap_id','source_pointer','owner_authority','affected_routes','observed_at','provenance','evidence_for','evidence_against','uncertainty_state','urgency','necessity','impact','detectability','recurrence_risk','failure_mode','falsifier','next_probe','mitigation','closure_gate','review_or_expiry','claim_allowed','actions']
for g in gaps:
    for k in required: req(k in g,f"{g.get('gap_id','?')} missing {k}")
    req(g.get('claim_allowed') is False,f"{g.get('gap_id','?')} claim must remain false")
provider=next((g for g in gaps if g.get('gap_id')=='PROVIDER_SERVER_BARRIER_FIELD_FAILURE_20260821'),None)
req(provider is not None,'provider P0 missing')
if provider:
    req(provider.get('urgency')=='P0','provider barrier must remain P0')
    req('rejected' in provider.get('closure_gate','').lower(),'provider closure must require rejection receipt')
req(len(d.get('F_next',[]))>=5,'F_next must remain executable and nonempty')
serialized=json.dumps(d)
req('"execution_hours_runtime_hours": 0' not in serialized,'unknown runtime coerced to zero')
req('"calendar_age": 0' not in serialized,'unknown age coerced to zero')
if err:
    print('FAIL federated omega cycle')
    for e in err: print('-',e)
    sys.exit(1)
print('PASS federated omega cycle fail-closed contract')
print('components=',len(ledger),'gaps=',len(gaps),'F_next=',len(d.get('F_next',[])))
