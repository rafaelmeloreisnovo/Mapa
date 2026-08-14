#!/usr/bin/env python3
import argparse, json
from jsonschema import Draft202012Validator, FormatChecker

def semantic_errors(x):
    e=[]
    if x['six_sigma']['rpn'] != x['six_sigma']['severity']*x['six_sigma']['occurrence']*x['six_sigma']['detectability']:
        e.append('RPN_MISMATCH')
    if x['epistemic']['state']=='VERIFIED' and not x['epistemic']['evidence_refs']:
        e.append('VERIFIED_WITHOUT_EVIDENCE')
    if x['execution']['state']=='VERIFIED' and not x['execution']['evidence_refs']:
        e.append('EXECUTION_VERIFIED_WITHOUT_EVIDENCE')
    if x['epistemic']['state']=='TOKEN_VAZIO' and (not x['f_gap'] or not x['f_next']):
        e.append('TOKEN_VAZIO_WITHOUT_GAP_NEXT')
    if x['attention']['state'] in ('ABORTED','BLOCKED_BY_CONTROL','SUPPRESSED_BY_POLICY') and not x['attention']['reason_code']:
        e.append('ATTENTION_STATE_WITHOUT_REASON')
    if x['attention']['state']=='SUPPRESSED_BY_POLICY' and not x['attention'].get('policy_ref'):
        e.append('POLICY_SUPPRESSION_WITHOUT_POLICY_REF')
    if x['contract']['status']=='SATISFIED' and any(r['state'] not in ('SATISFIED','NOT_APPLICABLE') for r in x['contract']['requirements']):
        e.append('CONTRACT_SATISFIED_WITH_OPEN_REQUIREMENT')
    if x['closure']['state']=='CLOSED' and any(g['state']!='PASS' for g in x['closure']['gates']):
        e.append('CLOSED_WITH_NONPASS_GATE')
    if x['provenance']['status']=='MISSING' and x['epistemic']['state'] in ('VERIFIED','EVIDENCED'):
        e.append('EVIDENCE_WITH_MISSING_PROVENANCE')
    return e

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('schema'); ap.add_argument('records'); a=ap.parse_args()
    schema=json.load(open(a.schema,encoding='utf-8')); data=json.load(open(a.records,encoding='utf-8')); items=data if isinstance(data,list) else [data]
    v=Draft202012Validator(schema,format_checker=FormatChecker()); errors=[]
    for i,x in enumerate(items):
        for z in v.iter_errors(x): errors.append(f'{i}:SCHEMA:{z.message}')
        for z in semantic_errors(x): errors.append(f'{i}:SEMANTIC:{z}')
    print(json.dumps({'result':'PASS' if not errors else 'FAIL','items':len(items),'errors':errors,'claim_allowed':False},sort_keys=True))
    return 0 if not errors else 1
if __name__=='__main__': raise SystemExit(main())
