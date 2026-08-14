#!/usr/bin/env python3
import copy, json, pathlib, subprocess, sys, tempfile
SCHEMA=sys.argv[1] if len(sys.argv)>1 else 'schemas/operational-work-item-transition.v1.schema.json'
VALIDATOR=sys.argv[2] if len(sys.argv)>2 else 'tools/validate_operational_work_item_transitions.py'
BASE=sys.argv[3] if len(sys.argv)>3 else 'data/governance/operational-work-item-transitions.c80.v1.json'
base=json.load(open(BASE,encoding='utf-8'))

def run(events):
    with tempfile.NamedTemporaryFile('w',suffix='.json',delete=False,encoding='utf-8') as f:
        json.dump(events,f); p=f.name
    cp=subprocess.run([sys.executable,VALIDATOR,SCHEMA,p],capture_output=True,text=True)
    pathlib.Path(p).unlink(missing_ok=True)
    return cp.returncode,cp.stdout.strip()

def transition_from(e, event_id, observed_at='2026-08-14T01:46:00Z'):
    n=copy.deepcopy(e); n['event_id']=event_id; n['event_type']='TRANSITION'; n['prior_event_id']=e['event_id']; n['from_state']=copy.deepcopy(e['to_state']); n['to_state']=copy.deepcopy(e['to_state']); n['to_state']['attention']='ACTIVE' if e['to_state']['attention']!='ACTIVE' else 'DEFERRED'; n['observed_at']=observed_at; n['reason_code']='TEST_TRANSITION'; return n

tests=[]
tests.append(('positive_baseline',base,0))
x=copy.deepcopy(base); x[1]['event_id']=x[0]['event_id']; tests.append(('duplicate_event_id',x,1))
x=copy.deepcopy(base); x[0]['prior_event_id']='WIE-FAKE-PRIOR'; tests.append(('create_prior_not_token_vazio',x,1))
x=copy.deepcopy(base); x[0]['from_state']=copy.deepcopy(x[0]['to_state']); tests.append(('create_from_not_null',x,1))
n=transition_from(base[1],'WIE-C80-CHUNK-GRAPH-T1'); n['prior_event_id']='TOKEN_VAZIO'; tests.append(('transition_prior_token_vazio',[base[1],n],1))
n=transition_from(base[1],'WIE-C80-CHUNK-GRAPH-T2'); n['to_state']=copy.deepcopy(n['from_state']); tests.append(('transition_no_state_change',[base[1],n],1))
n=transition_from(base[1],'WIE-C80-CHUNK-GRAPH-T3'); n['prior_event_id']='WIE-UNKNOWN-PRIOR'; tests.append(('transition_unknown_prior',[base[1],n],1))
n=transition_from(base[1],'WIE-C80-CHUNK-GRAPH-T4'); n['to_state']['epistemic']='EVIDENCED'; n['evidence_refs']=[]; tests.append(('promotion_without_evidence',[base[1],n],1))
n=transition_from(base[1],'WIE-C80-CHUNK-GRAPH-T5'); n['event_type']='SUPERSEDE'; tests.append(('supersede_without_superseded_state',[base[1],n],1))
n=transition_from(base[1],'WIE-C80-CHUNK-GRAPH-T6','2026-08-14T01:44:00Z'); tests.append(('nonmonotonic_time',[base[1],n],1))
x=copy.deepcopy(base); x[0]['claim_allowed']=True; tests.append(('claim_promotion',x,1))
passed=0
for name,obj,expect_fail in tests:
    rc,out=run(obj); ok=(rc!=0) if expect_fail else (rc==0); passed += int(ok); print(('PASS' if ok else 'FAIL'),name,'rc='+str(rc),out[:200])
print(f'RESULT pass={passed} total={len(tests)} claim_allowed=false')
raise SystemExit(0 if passed==len(tests) else 1)
