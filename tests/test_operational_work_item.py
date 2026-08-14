#!/usr/bin/env python3
import copy, json, subprocess, sys, tempfile, pathlib
SCHEMA=sys.argv[1] if len(sys.argv)>1 else 'schemas/operational-work-item.v1.schema.json'
VALIDATOR=sys.argv[2] if len(sys.argv)>2 else 'tools/validate_operational_work_item.py'
BASE=sys.argv[3] if len(sys.argv)>3 else 'data/governance/operational-work-items.c80.v1.json'
items=json.load(open(BASE,encoding='utf-8')); base=items[0]

def run(obj):
    with tempfile.NamedTemporaryFile('w',suffix='.json',delete=False,encoding='utf-8') as f:
        json.dump(obj,f); p=f.name
    cp=subprocess.run([sys.executable,VALIDATOR,SCHEMA,p],capture_output=True,text=True)
    pathlib.Path(p).unlink(missing_ok=True)
    return cp.returncode,cp.stdout.strip()

tests=[('positive_baseline',base,0)]
x=copy.deepcopy(base); x['six_sigma']['rpn']=31; tests.append(('rpn_mismatch',x,1))
x=copy.deepcopy(base); x['epistemic']={'state':'VERIFIED','evidence_refs':[]}; tests.append(('verified_no_evidence',x,1))
x=copy.deepcopy(base); x['f_gap']=[]; tests.append(('token_vazio_no_gap',x,1))
x=copy.deepcopy(base); x['attention']={'state':'SUPPRESSED_BY_POLICY','reason_code':'POLICY','policy_ref':None}; tests.append(('suppressed_no_policy_ref',x,1))
x=copy.deepcopy(base); x['contract']['status']='SATISFIED'; tests.append(('contract_false_closure',x,1))
x=copy.deepcopy(base); x['closure']['state']='CLOSED'; tests.append(('closed_nonpass_gate',x,1))
x=copy.deepcopy(base); x['epistemic']={'state':'EVIDENCED','evidence_refs':['R']}; x['provenance']['status']='MISSING'; tests.append(('evidence_missing_provenance',x,1))
x=copy.deepcopy(base); x['claim_allowed']=True; tests.append(('claim_promotion',x,1))
x=copy.deepcopy(base); x['unexpected']='x'; tests.append(('extra_property',x,1))
passn=0
for name,obj,expect_nonzero in tests:
    rc,out=run(obj); ok=(rc!=0) if expect_nonzero else (rc==0); passn+=int(ok)
    print(('PASS' if ok else 'FAIL'),name,'rc='+str(rc),out[:180])
print(f'RESULT pass={passn} total={len(tests)} claim_allowed=false')
raise SystemExit(0 if passn==len(tests) else 1)
