#!/usr/bin/env python3
import argparse, hashlib, json, os, subprocess, sys, zipfile
from collections import Counter
from datetime import datetime, timezone

JQ_FILTER = r'''
def p: .[0];
select(
  (((p|length)==2) and (p[1]=="title" or p[1]=="create_time" or p[1]=="update_time" or p[1]=="id"))
  or (((p|length)==4) and p[1]=="mapping" and p[3]=="id")
  or (((p|length)==6) and p[1]=="mapping" and p[3]=="message" and p[4]=="author" and p[5]=="role")
  or (((p|length)==6) and p[1]=="mapping" and p[3]=="message" and p[4]=="content" and p[5]=="content_type")
)
'''

def sha256_file(path, chunk=8*1024*1024):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(chunk),b''):
            h.update(b)
    return h.hexdigest()

def member_sha256(zip_path, member, chunk=8*1024*1024):
    h=hashlib.sha256(); total=0
    with zipfile.ZipFile(zip_path) as z, z.open(member) as f:
        for b in iter(lambda:f.read(chunk),b''):
            h.update(b); total += len(b)
    return h.hexdigest(), total

def iso_utc(v):
    if v is None: return None
    try: return datetime.fromtimestamp(float(v), timezone.utc).isoformat().replace('+00:00','Z')
    except Exception: return None

def canonical_line(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',',':'))+'\n'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('zip_path')
    ap.add_argument('--out', required=True)
    ap.add_argument('--manifest', required=True)
    args=ap.parse_args()
    zip_sha=sha256_file(args.zip_path)
    member_sha, member_bytes=member_sha256(args.zip_path,'conversations.json')
    unzip=subprocess.Popen(['unzip','-p',args.zip_path,'conversations.json'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    jq=subprocess.Popen(['jq','--stream','-c',JQ_FILTER],stdin=unzip.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1)
    unzip.stdout.close()
    current_idx=None; cur=None; recs=0; total_msgs=0; total_nodes=0
    all_roles=Counter(); all_ct=Counter(); months=Counter(); min_ct=None; max_ct=None; max_ut=None
    pid_seen=set(); duplicate_pid=0
    def newrec(idx):
        return {'source_index':idx,'id':None,'title_sha256':None,'title_utf8_bytes':None,'create_time':None,'update_time':None,'mapping_nodes':0,'roles':Counter(),'content_types':Counter()}
    def flush(c,out):
        nonlocal recs,total_msgs,total_nodes,min_ct,max_ct,max_ut,duplicate_pid
        if c is None: return
        raw_id=c['id']
        pid=hashlib.sha256((raw_id or f'NO_ID:{c["source_index"]}').encode()).hexdigest()
        if pid in pid_seen: duplicate_pid += 1
        pid_seen.add(pid)
        ct=iso_utc(c['create_time']); ut=iso_utc(c['update_time'])
        if ct:
            months[ct[:7]] += 1; min_ct=ct if min_ct is None or ct<min_ct else min_ct; max_ct=ct if max_ct is None or ct>max_ct else max_ct
        if ut: max_ut=ut if max_ut is None or ut>max_ut else max_ut
        msg_count=sum(c['roles'].values()); total_msgs += msg_count; total_nodes += c['mapping_nodes']; all_roles.update(c['roles']); all_ct.update(c['content_types']); recs += 1
        out.write(canonical_line({'conversation_pid_sha256':pid,'source_index':c['source_index'],'create_time_utc':ct,'update_time_utc':ut,'month_utc':ct[:7] if ct else None,'mapping_nodes':c['mapping_nodes'],'message_count':msg_count,'role_counts':dict(sorted(c['roles'].items())),'content_type_counts':dict(sorted(c['content_types'].items())),'title_sha256':c['title_sha256'],'title_utf8_bytes':c['title_utf8_bytes'],'semantic_topic_state':'TOKEN_VAZIO_PRIVACY_REVIEW_PENDING','raw_id_present':raw_id is not None,'raw_title_stored':False,'raw_message_body_stored':False,'claim_allowed':False}))
    os.makedirs(os.path.dirname(args.out) or '.',exist_ok=True)
    with open(args.out,'w',encoding='utf-8',newline='\n') as out:
        for line in jq.stdout:
            ev=json.loads(line)
            if len(ev)<2: continue
            path,val=ev
            if not path or not isinstance(path[0],int): continue
            idx=path[0]
            if current_idx is None: current_idx=idx; cur=newrec(idx)
            elif idx != current_idx: flush(cur,out); current_idx=idx; cur=newrec(idx)
            if len(path)==2:
                key=path[1]
                if key=='id' and isinstance(val,str): cur['id']=val
                elif key=='title' and isinstance(val,str):
                    b=val.encode(); cur['title_sha256']=hashlib.sha256(b).hexdigest(); cur['title_utf8_bytes']=len(b)
                elif key=='create_time' and isinstance(val,(int,float)): cur['create_time']=val
                elif key=='update_time' and isinstance(val,(int,float)): cur['update_time']=val
            elif len(path)==4 and path[1]=='mapping' and path[3]=='id': cur['mapping_nodes'] += 1
            elif len(path)==6 and path[1]=='mapping' and path[3]=='message' and path[4]=='author' and path[5]=='role' and isinstance(val,str): cur['roles'][val] += 1
            elif len(path)==6 and path[1]=='mapping' and path[3]=='message' and path[4]=='content' and path[5]=='content_type' and isinstance(val,str): cur['content_types'][val] += 1
        flush(cur,out)
    jq_err=jq.stderr.read(); jq_rc=jq.wait(); unzip_err=unzip.stderr.read().decode('utf-8','replace'); unzip_rc=unzip.wait()
    if jq_rc or unzip_rc:
        print(jq_err,file=sys.stderr); print(unzip_err,file=sys.stderr); return 2
    manifest={'schema':'rafaelia.conversation-derived-index-manifest.v1','state':'VERIFIED_LOCAL_DETERMINISTIC_CANDIDATE','claim_allowed':False,'privacy':{'raw_titles':False,'raw_message_bodies':False,'raw_conversation_ids':False,'identifier_mode':'SHA256_PSEUDONYMIZED','semantic_topic_state':'TOKEN_VAZIO_PRIVACY_REVIEW_PENDING'},'source':{'zip_sha256':zip_sha,'conversations_member_sha256':member_sha,'conversations_member_bytes':member_bytes},'output':{'jsonl_sha256':sha256_file(args.out),'jsonl_bytes':os.path.getsize(args.out),'records':recs},'aggregates':{'mapping_nodes':total_nodes,'messages_with_payload':total_msgs,'role_counts':dict(sorted(all_roles.items())),'content_type_counts':dict(sorted(all_ct.items())),'conversation_month_counts':dict(sorted(months.items())),'create_time_min_utc':min_ct,'create_time_max_utc':max_ct,'update_time_max_utc':max_ut,'duplicate_pseudonym_count':duplicate_pid},'invariants':['source_read_only','full_source_sha256_required','raw_private_payload_not_materialized','append_only','TOKEN_VAZIO_topic_until_privacy_review'],'f_gap':['TOKEN_VAZIO_SEMANTIC_TOPIC_PRIVACY_REVIEW','TOKEN_VAZIO_CHUNK_GRAPH_MATERIALIZATION','TOKEN_VAZIO_CROSS_EXPORT_DEDUP']}
    with open(args.manifest,'w',encoding='utf-8',newline='\n') as f: f.write(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    return 0
if __name__=='__main__': raise SystemExit(main())
