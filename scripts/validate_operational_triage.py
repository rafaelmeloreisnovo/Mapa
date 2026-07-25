#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

SCHEMA_VERSION='rafaelia.operational-triage/v1'
PRIORITIES=['P0_CRITICAL','P1_URGENT','P2_NECESSARY','P3_IMPORTANT','P4_BACKLOG']
RELATION_TYPES={'SAME_SITUATION','STRUCTURAL_ANALOG','DEPENDENT','PART_OF','CONFLICTS_WITH','SUPERSEDES','DISTINCT','TOKEN_VAZIO'}
WEIGHTS={'human_safety':6,'privacy_integrity':5,'operational_impact':3,'dependency_blocking':3,'risk_of_delay':2,'evidence_deficit':1,'reversibility':-1}

def score(v): return max(0,min(100,sum(WEIGHTS[k]*int(v[k]) for k in WEIGHTS)))
def priority(item):
    v=item['score_vector']
    if v['human_safety']>=5 or (v['privacy_integrity']>=5 and v['risk_of_delay']>=4): return 'P0_CRITICAL'
    s=score(v)
    if s>=55:return 'P1_URGENT'
    if s>=35:return 'P2_NECESSARY'
    if s>=18:return 'P3_IMPORTANT'
    return 'P4_BACKLOG'

def invmap(item): return {x['id']:x for x in item.get('invariants',[]) if isinstance(x,dict) and 'id' in x}
def same_eligible(a,b):
    mismatch=[]
    for f in ('domain','object_type','target','privacy_class','data_class','epistemic_state'):
        if a.get(f)!=b.get(f): mismatch.append(f)
    ia,ib=invmap(a),invmap(b)
    if set(ia)!=set(ib): mismatch.append('invariant_ids')
    else:
        for k in ia:
            if ia[k].get('state')!=ib[k].get('state'): mismatch.append('invariant_state:'+k)
    return not mismatch,mismatch

def validate(registry:Any,repo_root:Path|None=None):
    errors=[]; warnings=[]
    if not isinstance(registry,dict): return {'status':'FAIL','errors':['registry must be object'],'warnings':[],'claim_allowed':False}
    if registry.get('schema_version')!=SCHEMA_VERSION: errors.append('invalid schema_version')
    if registry.get('claim_allowed') is not False: errors.append('registry claim_allowed must remain false')
    p=registry.get('policy',{})
    for k in ('token_vazio_is_valid','exact_equivalence_requires_evidence','human_safety_precedes_performance','privacy_precedes_interpretation'):
        if p.get(k) is not True: errors.append('policy.'+k+' must be true')
    items=registry.get('items',[])
    if not isinstance(items,list) or not items: errors.append('items must be non-empty'); items=[]
    by={}; counts={x:0 for x in PRIORITIES}
    for n,item in enumerate(items):
        if not isinstance(item,dict): errors.append(f'items[{n}] must be object'); continue
        iid=item.get('item_id')
        if not isinstance(iid,str) or not iid: errors.append(f'items[{n}].item_id missing'); continue
        if iid in by: errors.append('duplicate item_id '+iid)
        by[iid]=item
        v=item.get('score_vector')
        if not isinstance(v,dict): errors.append(iid+'.score_vector must be object'); continue
        good=True
        for k in WEIGHTS:
            x=v.get(k)
            if not isinstance(x,int) or isinstance(x,bool) or not 0<=x<=5: errors.append(f'{iid}.score_vector.{k} must be 0..5'); good=False
        if good:
            exp=priority(item); counts[exp]+=1
            if item.get('declared_priority')!=exp: errors.append(f'{iid}.declared_priority={item.get("declared_priority")} but derived={exp}')
        invs=item.get('invariants',[])
        if not isinstance(invs,list) or not invs: errors.append(iid+'.invariants must be non-empty'); invs=[]
        seen=set()
        for inv in invs:
            if not isinstance(inv,dict): errors.append(iid+' invariant must be object'); continue
            k=inv.get('id')
            if k in seen: errors.append(iid+' duplicate invariant '+str(k))
            seen.add(k)
            if inv.get('state')=='SATISFIED' and not inv.get('evidence_refs'): errors.append(f'{iid}.{k} SATISFIED requires evidence_refs')
        if item.get('epistemic_state')=='TOKEN_VAZIO' and item.get('status') in {'VERIFIED','CLOSED'}: errors.append(iid+' TOKEN_VAZIO cannot be VERIFIED or CLOSED')
        if item.get('privacy_class') in {'RESTRICTED','EXCLUDED'} and v.get('privacy_integrity',0)<4: errors.append(iid+' restricted/excluded data requires privacy_integrity >= 4')
        if repo_root:
            for ref in item.get('evidence_refs',[]):
                if ref.startswith(('http://','https://','PR-','RUN-')): continue
                if not (repo_root/ref).exists(): warnings.append(iid+' evidence ref not found in checkout: '+ref)
    for iid,item in by.items():
        for dep in item.get('dependencies',[]):
            if dep==iid: errors.append(iid+' cannot depend on itself')
            elif dep not in by: errors.append(f'{iid} dependency {dep} does not exist')
    groups=registry.get('groups',[]); covered=set(); gids=set()
    if not isinstance(groups,list): errors.append('groups must be array'); groups=[]
    for g in groups:
        if not isinstance(g,dict): errors.append('group must be object'); continue
        gid=g.get('group_id')
        if gid in gids: errors.append('duplicate group_id '+str(gid))
        gids.add(gid)
        if g.get('claim_allowed') is not False: errors.append(str(gid)+'.claim_allowed must be false')
        for m in g.get('members',[]):
            if m not in by: errors.append(f'{gid} member {m} does not exist')
            covered.add(m)
    rels=registry.get('relations',[]); rids=set(); same=set(); distinct=set()
    if not isinstance(rels,list): errors.append('relations must be array'); rels=[]
    for r in rels:
        if not isinstance(r,dict): errors.append('relation must be object'); continue
        rid=r.get('relation_id')
        if rid in rids: errors.append('duplicate relation_id '+str(rid))
        rids.add(rid)
        l,rr=r.get('left'),r.get('right')
        if l==rr: errors.append(str(rid)+' cannot self-relate')
        if l not in by or rr not in by: errors.append(str(rid)+' endpoints must exist'); continue
        typ=r.get('relation_type')
        if typ not in RELATION_TYPES: errors.append(str(rid)+' invalid relation_type'); continue
        pair=tuple(sorted((l,rr)))
        if typ=='SAME_SITUATION':
            same.add(pair); ok,mm=same_eligible(by[l],by[rr])
            if not ok: errors.append(str(rid)+' SAME_SITUATION mismatch: '+', '.join(mm))
            if not r.get('evidence_refs'): errors.append(str(rid)+' SAME_SITUATION requires evidence_refs')
        if typ=='DISTINCT': distinct.add(pair)
        if r.get('claim_allowed') is not False: errors.append(str(rid)+'.claim_allowed must be false')
    for pair in same & distinct: errors.append(f'pair {pair} cannot be SAME_SITUATION and DISTINCT')
    ungrouped=sorted(set(by)-covered)
    if ungrouped: warnings.append('ungrouped items: '+', '.join(ungrouped))
    visiting=set(); visited=set()
    def walk(node,trail):
        if node in visiting: errors.append('dependency cycle: '+' -> '.join(trail+[node])); return
        if node in visited:return
        visiting.add(node)
        for dep in by.get(node,{}).get('dependencies',[]):
            if dep in by: walk(dep,trail+[node])
        visiting.remove(node); visited.add(node)
    for iid in by: walk(iid,[])
    ordered=sorted(by.values(),key=lambda x:(PRIORITIES.index(x['declared_priority']),-score(x['score_vector']),x['item_id']))
    return {'schema_version':SCHEMA_VERSION,'status':'PASS' if not errors else 'FAIL','errors':errors,'warnings':warnings,'claim_allowed':False,'metrics':{'items':len(by),'groups':len(groups),'relations':len(rels),'priority_counts':counts,'ungrouped_items':len(ungrouped)},'execution_queue':[{'item_id':x['item_id'],'priority':x['declared_priority'],'score':score(x['score_vector']),'status':x['status'],'next_action':x['next_action']} for x in ordered],'next_verifiable_step':registry.get('next_verifiable_step','TOKEN_VAZIO')}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('registry',type=Path); ap.add_argument('--repo-root',type=Path); ap.add_argument('--write-report',type=Path); a=ap.parse_args()
    report=validate(json.loads(a.registry.read_text(encoding='utf-8')),a.repo_root)
    out=json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    if a.write_report: a.write_report.parent.mkdir(parents=True,exist_ok=True); a.write_report.write_text(out,encoding='utf-8')
    else: print(out,end='')
    raise SystemExit(0 if report['status']=='PASS' else 1)
if __name__=='__main__': main()
