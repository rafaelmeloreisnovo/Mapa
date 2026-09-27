#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re
from pathlib import Path
EXPECTED={"C01_SOURCE_ORIGIN","C02_DOCUMENT_STATE","C03_CODE_STATE","C04_EXECUTION","C05_EVIDENCE","C06_TRANSFER_HANDOFF","C07_CLAIM_PROMOTION","C08_CROSS_PROVIDER_BRIDGE","C09_CREDENTIAL_AUTHORITY"}
DIGEST={"content_digest","receipt_digest"}
PROVIDER={"git_commit_oid","git_blob_oid","drive_revision_id","provider_request_id"}
STATES={"PASS","FAIL","NOT_RUN","PENDING","AUDIT","TOKEN_VAZIO","IMPLEMENTED_UNTESTED","OBSERVED_UNPROMOTED","ROUTE_STATE_BLOCKED"}
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def validate_taxonomy(d):
 e=[]
 def req(c,m):
  if not c:e.append(m)
 req(d.get("schema")=="rafaelia.custody.types.v1","taxonomy schema mismatch")
 ids=[x.get("id") for x in d.get("classes",[]) if isinstance(x,dict)]
 req(set(ids)==EXPECTED,"custody class set mismatch"); req(len(ids)==len(set(ids)),"duplicate class ids")
 inv=set(d.get("invariants",[]))
 for x in ("SOURCE!=ARTIFACT!=EXECUTION!=EVIDENCE!=CLAIM","AUTHORIZATION!=EXECUTION!=CUSTODY!=OBSERVATION!=PROMOTION","PROVIDER_REVISION_ID!=CONTENT_DIGEST","GIT_OBJECT_ID!=RECEIPT_DIGEST","HASH_CHAIN!=MERKLE_TREE"):
  req(x in inv,"missing invariant "+x)
 req(d.get("chain_models",{}).get("linear_hash_chain",{}).get("merkle_claim_allowed") is False,"linear hash chain mislabeled merkle")
 return e
def validate_event(ev,tax):
 e=[]
 def req(c,m):
  if not c:e.append(m)
 req(ev.get("schema")=="rafaelia.custody.event.v1","event schema mismatch"); req(ev.get("custody_class") in EXPECTED,"unknown custody class")
 a=ev.get("actors",{})
 for r in ("authorized_by","executed_by","custodied_by"): req(isinstance(a.get(r),dict),"missing actor "+r)
 if isinstance(a.get("planned_by"),dict) and a["planned_by"].get("type")=="assistant_session":
  req(a.get("authorized_by",{}).get("type")!="assistant_session","assistant session must not self-authorize")
 i=ev.get("integrity",{}); k=i.get("identity_kind"); alg=i.get("algorithm"); canon=i.get("canonicalization")
 req(k in DIGEST|PROVIDER,"invalid integrity kind")
 if k in DIGEST:req(isinstance(alg,str) and bool(alg.strip()),"digest requires algorithm")
 if k=="receipt_digest":req(isinstance(canon,str) and bool(canon.strip()),"receipt_digest requires canonicalization")
 if k in PROVIDER:
  req(alg in (None,"TOKEN_VAZIO"),"provider identity must not be mislabeled as cryptographic digest algorithm")
  req(canon in (None,"TOKEN_VAZIO"),"provider identity must not carry digest canonicalization")
 if k in {"git_commit_oid","git_blob_oid"}:req(bool(re.fullmatch(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}",str(i.get("value","")))),"git oid must be 40 or 64 hex")
 req(ev.get("state") in STATES,"invalid state")
 if ev.get("gap") not in ("none","NONE","TOKEN_VAZIO",""):req(ev.get("claim_allowed") is False,"open gap must keep claim_allowed=false")
 return e
def main():
 p=argparse.ArgumentParser(); p.add_argument("--taxonomy",default="data/governance/custody/00_INDEX/custody_types_v1.json"); p.add_argument("--event"); a=p.parse_args()
 t=load(a.taxonomy); e=validate_taxonomy(t)
 if a.event:e+=validate_event(load(a.event),t)
 if e:
  print("FAIL"); [print(" -",x) for x in e]; return 1
 print("PASS: custody taxonomy")
 print("PASS: authorization/execution/custody separation")
 print("PASS: provider identity/digest separation")
 print("PASS: hash-chain/Merkle separation")
 return 0
if __name__=="__main__": raise SystemExit(main())
