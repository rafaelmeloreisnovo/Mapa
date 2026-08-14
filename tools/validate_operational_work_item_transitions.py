#!/usr/bin/env python3
import argparse, json
from datetime import datetime
from jsonschema import Draft202012Validator, FormatChecker

def parse_time(s):
    return datetime.fromisoformat(s.replace('Z','+00:00'))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('schema'); ap.add_argument('events'); a=ap.parse_args()
    schema=json.load(open(a.schema,encoding='utf-8')); data=json.load(open(a.events,encoding='utf-8')); events=data if isinstance(data,list) else [data]
    v=Draft202012Validator(schema,format_checker=FormatChecker()); errors=[]; ids=set(); seen_by_work={}; last_time={}
    for i,e in enumerate(events):
        for z in v.iter_errors(e): errors.append(f'{i}:SCHEMA:{z.message}')
        eid=e.get('event_id'); wid=e.get('work_item_id'); typ=e.get('event_type'); prior=e.get('prior_event_id'); fs=e.get('from_state'); ts=e.get('to_state'); ev=e.get('evidence_refs',[])
        if eid in ids: errors.append(f'{i}:DUPLICATE_EVENT_ID')
        ids.add(eid)
        if typ=='CREATE':
            if prior!='TOKEN_VAZIO': errors.append(f'{i}:CREATE_PRIOR_NOT_TOKEN_VAZIO')
            if fs is not None: errors.append(f'{i}:CREATE_FROM_STATE_NOT_NULL')
        else:
            if prior=='TOKEN_VAZIO': errors.append(f'{i}:NONCREATE_PRIOR_TOKEN_VAZIO')
            if fs is None: errors.append(f'{i}:NONCREATE_FROM_STATE_NULL')
            if fs==ts: errors.append(f'{i}:NONCREATE_NO_STATE_CHANGE')
            if prior not in seen_by_work.get(wid,set()): errors.append(f'{i}:PRIOR_EVENT_NOT_PREVIOUSLY_OBSERVED_FOR_WORK_ITEM')
        if typ=='SUPERSEDE' and ts and not (ts.get('attention')=='SUPERSEDED' or ts.get('epistemic')=='SUPERSEDED'):
            errors.append(f'{i}:SUPERSEDE_WITHOUT_SUPERSEDED_STATE')
        if ts and (ts.get('epistemic') in ('VERIFIED','EVIDENCED') or ts.get('execution')=='VERIFIED' or ts.get('closure')=='CLOSED') and not ev:
            errors.append(f'{i}:EVIDENCE_REQUIRED_FOR_PROMOTED_STATE')
        try:
            t=parse_time(e['observed_at'])
            if wid in last_time and t < last_time[wid]: errors.append(f'{i}:NONMONOTONIC_TIME')
            last_time[wid]=t
        except Exception: pass
        seen_by_work.setdefault(wid,set()).add(eid)
    print(json.dumps({'result':'PASS' if not errors else 'FAIL','events':len(events),'unique_event_ids':len(ids),'errors':errors,'claim_allowed':False},sort_keys=True))
    return 0 if not errors else 1
if __name__=='__main__': raise SystemExit(main())
