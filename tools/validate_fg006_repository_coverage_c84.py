#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
REQ={"provider","path_or_id","hash","timestamp","generator","parent","execution","receipt"}
BUCKETS=("present","partial","absent","not_applicable")
H40=re.compile(r"^[0-9a-f]{40}$")
UID=re.compile(r"^FG006-C84-\d{8}T\d{4}Z-[0-9a-f]{8}$")
def partition(x,p,e):
 u=set()
 for b in BUCKETS:
  v=x.get(b)
  if not isinstance(v,list): e.append(f"{p}.{b}"); continue
  s=set(v)
  if len(s)!=len(v): e.append(f"{p}.{b}_duplicate")
  if u&s:e.append(f"{p}.overlap")
  u|=s
 if u!=REQ:e.append(f"{p}.partition")
def validate(d):
 e=[]
 if d.get("schema")!="RAFAELIA_FG006_C84_RECONCILIATION_V1":e.append("schema")
 if d.get("cycle_id")!="OMEGA-ANTI-REGRESSION-C84":e.append("cycle_id")
 if d.get("trail_id")!="FG006_REPOSITORY_COVERAGE":e.append("trail_id")
 if not UID.fullmatch(str(d.get("cycle_uid",""))):e.append("cycle_uid")
 if d.get("claim_allowed") is not False:e.append("claim")
 if d.get("repository_wide_closed") is not False:e.append("close")
 ci=d.get("cycle_identity",{})
 if ci.get("collided_label")!="C83" or ci.get("collision_state")!="CONTAINED_APPEND_ONLY":e.append("collision")
 if ci.get("preexisting_c83_drive_id")!="1uC3c--OxCGiUAYJ3XxVfiqLzdWL7hMRTEvawD115T1U":e.append("prior_c83_drive")
 if ci.get("preexisting_c83_pr")!=223 or ci.get("superseded_local_c83_pr")!=226:e.append("prior_c83_pr")
 ap=ci.get("allocation_probe",{})
 if ap.get("drive_results")!=0 or ap.get("github_results")!=0 or ap.get("observed_before_materialization") is not True:e.append("allocation_probe")
 p=d.get("parent_c82",{})
 if p.get("head")!="20f88932062d651c37ed92c964a66efe5ae108c8":e.append("parent_head")
 if p.get("minimum_candidate_count")!=30:e.append("parent_count")
 if p.get("tree_truncated") is not False or p.get("machine_extracted_full_pathset") is not False:e.append("tree_boundary")
 cc=d.get("concurrency_containment",{})
 if cc.get("superseded_concurrent_pr")!=225 or cc.get("superseded_c83_pr")!=226 or cc.get("preexisting_c83_pr")!=223:e.append("concurrency_refs")
 if cc.get("merge_authorized") is not False:e.append("merge_authorized")
 rr=d.get("c81_unfetched_resolution",{})
 rec=rr.get("records",[])
 if rr.get("count_before")!=11 or rr.get("content_fetched_count")!=11 or rr.get("remaining")!=0 or len(rec)!=11:e.append("resolution_count")
 seen=set()
 for i,x in enumerate(rec):
  q=f"record[{i}]";p=x.get("path")
  if not p or p in seen:e.append(f"{q}.path")
  seen.add(p)
  if not H40.fullmatch(str(x.get("source_git_blob_sha1",""))):e.append(f"{q}.blob")
  if not str(x.get("inspection","")).startswith("CONTENT_FETCHED_C83"):e.append(f"{q}.inspection")
  partition(x,q,e)
 up=d.get("inspection_upgrades",[])
 if len(up)!=2:e.append("upgrades")
 else:
  a,b=up
  if a.get("observed_event_count")!=15 or a.get("windows")!=[[1,5],[6,10],[11,20]]:e.append("custody_windows")
  if b.get("observed_record_count")!=23 or b.get("windows")!=[[1,8],[9,20],[21,40]]:e.append("source_windows")
 ca=d.get("candidate_accounting",{})
 if ca.get("parent_lower_bound")!=30 or ca.get("c83_new_candidates")!=0 or ca.get("current_lower_bound")!=30:e.append("candidate_accounting")
 if not str(ca.get("exhaustive_candidate_count","")).startswith("TOKEN_VAZIO"):e.append("exhaustive_overclaim")
 tv=d.get("token_vazio",{})
 if "TOKEN_VAZIO_FG006_UNFETCHED_CANDIDATE_CONTENT_C81" not in tv.get("resolved",[]):e.append("content_tv")
 if "TOKEN_VAZIO_CYCLE_ID_COLLISION_C83_C84" not in tv.get("resolved",[]):e.append("collision_tv")
 if "TOKEN_VAZIO_FG006_TREE_PAYLOAD_MACHINE_EXTRACTION_C82" not in tv.get("open",[]):e.append("tree_tv")
 if "TOKEN_VAZIO_GLOBAL_CYCLE_ID_ATOMIC_ALLOCATION" not in tv.get("open",[]):e.append("allocator_tv")
 return e
def main():
 d=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"));e=validate(d)
 if e:
  [print("REJECT",x) for x in e];return 1
 print("PASS fg006-c84 lower_bound=30 content_resolved=11 cycle_collision=contained closed=false");return 0
if __name__=="__main__":raise SystemExit(main())
