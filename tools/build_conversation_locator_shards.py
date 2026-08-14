#!/usr/bin/env python3
import argparse, json, hashlib, os, re
from collections import defaultdict

def line(obj): return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',',':'))+'\n'
def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('index'); ap.add_argument('--outdir',required=True); ap.add_argument('--manifest',required=True); a=ap.parse_args()
    os.makedirs(a.outdir,exist_ok=True); buckets=defaultdict(list)
    with open(a.index,encoding='utf-8') as f:
        for raw in f:
            r=json.loads(raw); month=r.get('month_utc') or 'TOKEN_VAZIO_TIME'
            buckets[month].append({'pid':r['conversation_pid_sha256'],'source_index':r['source_index'],'create_time_utc':r['create_time_utc'],'update_time_utc':r['update_time_utc'],'month_utc':r['month_utc'],'mapping_nodes':r['mapping_nodes'],'message_count':r['message_count'],'title_sha256':r['title_sha256'],'semantic_topic_state':'TOKEN_VAZIO_PRIVACY_REVIEW_PENDING','claim_allowed':False})
    shards=[]
    for month in sorted(buckets):
        safe=re.sub(r'[^0-9A-Za-z_-]','_',month); p=os.path.join(a.outdir,f'conversation-locator-{safe}.v1.jsonl')
        with open(p,'w',encoding='utf-8',newline='\n') as f:
            for o in buckets[month]: f.write(line(o))
        shards.append({'month':month,'path':os.path.basename(p),'records':len(buckets[month]),'bytes':os.path.getsize(p),'sha256':sha(p)})
    manifest={'schema':'rafaelia.conversation-locator-shards.v1','claim_allowed':False,'privacy':{'raw_ids':False,'raw_titles':False,'raw_messages':False,'topic':'TOKEN_VAZIO_PRIVACY_REVIEW_PENDING'},'source_index_sha256':sha(a.index),'records':sum(x['records'] for x in shards),'shards':shards,'invariants':['pseudonymized_id_only','temporal_locator_only','no_raw_payload','append_only'],'f_gap':['TOKEN_VAZIO_SEMANTIC_TOPIC_PRIVACY_REVIEW','TOKEN_VAZIO_CHUNK_GRAPH_MATERIALIZATION','TOKEN_VAZIO_CROSS_EXPORT_DEDUP']}
    with open(a.manifest,'w',encoding='utf-8',newline='\n') as f: f.write(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
if __name__=='__main__': main()
