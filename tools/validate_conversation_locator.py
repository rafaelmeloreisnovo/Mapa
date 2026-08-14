#!/usr/bin/env python3
import argparse, json, re, os, hashlib
HEX64=re.compile(r'^[0-9a-f]{64}$')
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('manifest'); ap.add_argument('shard_dir'); a=ap.parse_args()
    m=json.load(open(a.manifest,encoding='utf-8')); errs=[]; pids=set(); idxs=set(); n=0
    if m.get('claim_allowed') is not False: errs.append('manifest claim gate')
    forbidden={'title','message','messages','conversation_id','raw_id','raw_title','raw_message_body'}
    for s in m['shards']:
        p=os.path.join(a.shard_dir,s['path'])
        if not os.path.exists(p): errs.append('missing '+s['path']); continue
        if sha(p)!=s['sha256']: errs.append('sha '+s['path'])
        c=0
        for raw in open(p,encoding='utf-8'):
            c+=1; n+=1; r=json.loads(raw)
            if set(r)&forbidden: errs.append('forbidden field')
            if not HEX64.fullmatch(r.get('pid','')): errs.append('pid format')
            if r.get('pid') in pids: errs.append('duplicate pid')
            pids.add(r.get('pid'))
            i=r.get('source_index')
            if not isinstance(i,int) or i<0 or i in idxs: errs.append('source index')
            idxs.add(i)
            if r.get('claim_allowed') is not False: errs.append('record claim gate')
            if r.get('semantic_topic_state')!='TOKEN_VAZIO_PRIVACY_REVIEW_PENDING': errs.append('topic state')
            ct=r.get('create_time_utc'); mo=r.get('month_utc')
            if ct and mo and not ct.startswith(mo+'-'): errs.append('month mismatch')
            for k in ('mapping_nodes','message_count'):
                if not isinstance(r.get(k),int) or r[k]<0: errs.append('count')
        if c!=s['records']: errs.append('record count '+s['path'])
    if n!=m['records']: errs.append('total count')
    if idxs and idxs != set(range(min(idxs),max(idxs)+1)): errs.append('noncontiguous source indexes')
    print(json.dumps({'result':'PASS' if not errs else 'FAIL','records':n,'unique_pids':len(pids),'source_index_min':min(idxs) if idxs else None,'source_index_max':max(idxs) if idxs else None,'errors':errs[:20],'claim_allowed':False},sort_keys=True))
    return 0 if not errs else 1
if __name__=='__main__': raise SystemExit(main())
