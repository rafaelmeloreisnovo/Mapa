#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

SCHEMA='mapa.toroidal-research-federation.v1'
STATES={'ACTIVE','ADAPTER_PLANNED','TOKEN_VAZIO'}
ROLES={'GOVERNANCE','MAP','SCIENCE','ORCHESTRATION','RUNTIME','MEMORY'}

class ValidationError(ValueError): pass

def load(path:Path):
    try: data=json.loads(path.read_text(encoding='utf-8'))
    except (OSError,json.JSONDecodeError) as e: raise ValidationError(str(e)) from e
    if not isinstance(data,dict): raise ValidationError('root must be object')
    return data

def digest(data):
    clone=json.loads(json.dumps(data)); clone.setdefault('integrity',{})['digest']=''
    raw=json.dumps(clone,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    return hashlib.blake2b(raw,digest_size=32).hexdigest()

def validate(data):
    errors=[]
    if data.get('schema')!=SCHEMA: errors.append(f'schema must be {SCHEMA}')
    c=data.get('canonical_contract',{})
    if c.get('repository')!='rafaelmeloreisnovo/RafGitTools': errors.append('canonical contract authority mismatch')
    if c.get('schema')!='rafaelia.toroidal-research-cycle-contract.v1': errors.append('canonical contract schema mismatch')
    gov=data.get('governance',{})
    if gov.get('authority_repository')!='rafaelmeloreisnovo/Mapa': errors.append('Mapa must own the registry')
    if gov.get('claim_allowed') is not False: errors.append('registry must remain claim_allowed=false')
    repos=data.get('repositories')
    if not isinstance(repos,list): errors.append('repositories must be array'); repos=[]
    by_id={}; by_name={}; by_role={}
    for i,r in enumerate(repos):
        if not isinstance(r,dict): errors.append(f'repositories[{i}] must be object'); continue
        rid=r.get('id'); name=r.get('full_name'); role=r.get('role'); state=r.get('state')
        if not isinstance(rid,str) or not rid: errors.append(f'repositories[{i}].id invalid'); continue
        if rid in by_id: errors.append(f'duplicate repository id: {rid}')
        by_id[rid]=r
        if not isinstance(name,str) or '/' not in name: errors.append(f'{rid}.full_name invalid')
        elif name in by_name: errors.append(f'duplicate full_name: {name}')
        else: by_name[name]=rid
        if role not in ROLES: errors.append(f'{rid}.role invalid')
        elif role in by_role: errors.append(f'duplicate role: {role}')
        else: by_role[role]=rid
        if state not in STATES: errors.append(f'{rid}.state invalid')
        deps=r.get('depends_on')
        if not isinstance(deps,list): errors.append(f'{rid}.depends_on must be array')
        if state=='ACTIVE':
            for field in ('artifact_path','evidence_locator'):
                if not isinstance(r.get(field),str) or not r[field] or r[field]=='TOKEN_VAZIO': errors.append(f'{rid}.{field} required for ACTIVE')
        else:
            criteria=r.get('exit_criteria')
            if not isinstance(criteria,list) or not criteria: errors.append(f'{rid}.exit_criteria required for {state}')
    if set(by_role)!=ROLES: errors.append('roles must contain exactly one of each canonical role')
    for rid,r in by_id.items():
        for dep in r.get('depends_on',[]):
            if dep not in by_id: errors.append(f'{rid} depends on unknown id: {dep}')
            if dep==rid: errors.append(f'{rid} self dependency')
    edges=data.get('edges')
    if not isinstance(edges,list): errors.append('edges must be array'); edges=[]
    seen=set(); adjacency={rid:[] for rid in by_id}
    for i,e in enumerate(edges):
        if not isinstance(e,dict): errors.append(f'edges[{i}] must be object'); continue
        a,b=e.get('from'),e.get('to'); key=(a,b,e.get('relation'))
        if key in seen: errors.append(f'duplicate edge: {key}')
        seen.add(key)
        if a not in by_id or b not in by_id: errors.append(f'edge references unknown node: {a}->{b}')
        elif a==b: errors.append(f'self edge: {a}')
        else: adjacency[a].append(b)
        if not isinstance(e.get('relation'),str) or not e['relation']: errors.append(f'edges[{i}].relation invalid')
    visiting=set(); visited=set(); cycle=False
    def dfs(node):
        nonlocal cycle
        if node in visiting: cycle=True; return
        if node in visited: return
        visiting.add(node)
        for nxt in adjacency.get(node,[]): dfs(nxt)
        visiting.remove(node); visited.add(node)
    for node in adjacency: dfs(node)
    if cycle: errors.append('federation graph must be acyclic')
    derived=data.get('derived',{})
    actual={'repository_count':len(by_id),'active_count':sum(r.get('state')=='ACTIVE' for r in by_id.values()),'adapter_planned_count':sum(r.get('state')=='ADAPTER_PLANNED' for r in by_id.values()),'token_vazio_count':sum(r.get('state')=='TOKEN_VAZIO' for r in by_id.values()),'edge_count':len(edges),'cycle_count':int(cycle),'claim_allowed':False}
    for k,v in actual.items():
        if derived.get(k)!=v: errors.append(f'derived.{k} must be {v!r}')
    expected=digest(data); observed=data.get('integrity',{}).get('digest')
    if observed!=expected: errors.append('integrity digest mismatch')
    if errors: raise ValidationError('\n'.join(f'- {x}' for x in errors))
    return {'status':'PASS',**actual,'integrity_digest':expected,'inventory_state':gov.get('inventory_state')}

def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument('--path',type=Path,default=Path('indices/TOROIDAL_RESEARCH_FEDERATION.json')); ap.add_argument('--write-report',type=Path)
    args=ap.parse_args(argv)
    try: out=validate(load(args.path))
    except ValidationError as e: print(e,file=sys.stderr); return 1
    text=json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if args.write_report: args.write_report.write_text(text,encoding='utf-8')
    print(text,end=''); return 0
if __name__=='__main__': raise SystemExit(main())
