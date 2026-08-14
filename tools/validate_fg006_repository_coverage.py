#!/usr/bin/env python3
import json,sys
from pathlib import Path
REQ={"provider","path_or_id","hash","timestamp","generator","parent","execution","receipt"}
BUCKETS=("present","partial","absent","not_applicable")
def validate(d):
 e=[]
 if d.get("schema")!="RAFAELIA_FG006_REPOSITORY_COVERAGE_LEDGER_V1":e+=["schema"]
 if d.get("claim_allowed") is not False:e+=["claim_allowed"]
 if d.get("repository_wide_closed") is not False:e+=["premature_close"]
 r=d.get("records")
 if not isinstance(r,list) or not r:return e+["records"]
 seen=set()
 for i,x in enumerate(r):
  p=x.get("path")
  if not p or p in seen:e+=[f"record[{i}].path"]
  seen.add(p)
  used=set()
  for b in BUCKETS:
   vals=x.get(b,[])
   if not isinstance(vals,list):e+=[f"record[{i}].{b}"];continue
   if used&set(vals):e+=[f"record[{i}].overlap"]
   used|=set(vals)
  if not used<=REQ:e+=[f"record[{i}].unknown_field"]
 s=d.get("summary",{})
 if s.get("candidate_count")!=len(r):e+=["count"]
 if s.get("content_inspected_count")+s.get("metadata_or_applicability_tv_count")!=len(r):e+=["inspection_count"]
 if s.get("full_fg006_original_contract_count")!=0:e+=["unexpected_full"]
 if not s.get("blocking_token_vazio"):e+=["blocking_tv"]
 return e
def main():
 d=json.loads(Path(sys.argv[1]).read_text())
 e=validate(d)
 if e:
  [print("REJECT",x) for x in e];return 1
 print(f"PASS fg006-coverage-c81 candidates={len(d['records'])} inspected={d['summary']['content_inspected_count']} closed=false");return 0
if __name__=="__main__":raise SystemExit(main())
