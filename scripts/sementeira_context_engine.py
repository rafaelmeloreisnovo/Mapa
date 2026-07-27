#!/usr/bin/env python3
"""Read-only context custody for GPT Project source snapshots (stdlib only)."""
from __future__ import annotations
import argparse, hashlib, json, math, re, sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Sequence

WORD_RE = re.compile(r"[\wÀ-ÿΩ∆ΦΘα-ω]+(?:[-'][\wÀ-ÿΩ∆ΦΘα-ω]+)*", re.UNICODE)
UNIT_RE = re.compile(r"(?:\b(?:s|ms|us|ns|Hz|kHz|MHz|GHz|B|KB|MB|GB|KiB|MiB|GiB|m|cm|mm|kg|g|K|°C|V|A|W|J|Pa|N|Mpc)\b|[%±])")
FORMULA_RE = re.compile(r"(?:=|→|<-|->|\^|\b(?:sin|cos|log|ln|sqrt|exp|DFT|FFT)\b)", re.I)
STOP = set("a à as o os um uma de da do das dos e ou que em no na nos nas para por com sem se como mais menos não sim ser estar é são foi fica ficou isso essa esse esta este ao aos pela pelo pelas pelos seu sua seus suas já também cada entre sobre quando onde qual quais porque".split())
CUES = {
 "GAP":("token_vazio","não sabemos","não sei","falta","ausente","pendente","lacuna"),
 "HYPOTHESIS_CANDIDATE":("hipótese","pode","poderia","possibilidade","talvez","propõe","candidato"),
 "PROTOCOL_CANDIDATE":("protocolo","gate","workflow","pipeline","deve","regra","invariante"),
 "METRIC_CANDIDATE":("métrica","índice","coeficiente","margem","acurácia","intervalo","estatística"),
 "PARABLE_SYMBOLIC":("parábola","mestre","yin","yang","tao","símbolo","cosmos","semente"),
 "IMPLEMENTATION_CANDIDATE":("implementado","código","script","teste","commit","branch","arquivo"),
 "EVIDENCE_CANDIDATE":("evidência","executado","pass","resultado","medido","hash","receipt"),
}
PRIORITY={"GAP":9,"HYPOTHESIS_CANDIDATE":8,"MODEL_CANDIDATE":7,"METRIC_CANDIDATE":6,"PROTOCOL_CANDIDATE":5,"EVIDENCE_CANDIDATE":4,"IMPLEMENTATION_CANDIDATE":3,"PARABLE_SYMBOLIC":2}
AFFIRM=("sustenta","confirma","pass","válido","verdadeiro","existe","evidência")
NEGATE=("refuta","falha","inválido","falso","não existe","contradiz","bloqueado")
FALS=("falsificador","refutar","rejeitar","contraexemplo","hipótese nula","teste de oposição")
INV={
 "ORIGIN":("origem","fonte","autoria","proveniência"),
 "CUSTODY":("hash","cadeia de custódia","append","previous_event"),
 "EVIDENCE":("evidência","teste","receipt","execução"),
 "BOUNDARY":("limite","fronteira","escala","unidade","condição de contorno"),
 "NON_COLLAPSE":("não confundir","não promover","não apagar","token_vazio"),
 "FEEDBACK":("retroalimentação","f_next","próximo gate","próxima porta"),
}

def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def canon(x:Any)->str:return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def tokens(text:str)->list[str]:return [x.casefold() for x in WORD_RE.findall(text)]
def terms(text:str)->list[str]:return [x for x in tokens(text) if len(x)>2 and x not in STOP]
def entropy(xs:Sequence[str])->float:
 if not xs:return 0.0
 c=Counter(xs);n=len(xs);return -sum((v/n)*math.log2(v/n) for v in c.values())
def jac(a:Iterable[str],b:Iterable[str])->float:
 a,b=set(a),set(b)
 return 1.0 if not a and not b else 0.0 if not a or not b else len(a&b)/len(a|b)
def thirds(xs:Sequence[str])->list[list[str]]:
 n=len(xs)
 if not n:return [[],[],[]]
 return [list(xs[:math.ceil(n/3)]),list(xs[math.ceil(n/3):math.ceil(2*n/3)]),list(xs[math.ceil(2*n/3):])]
def derivative(xs:Sequence[str])->dict[str,Any]:
 ps=thirds(xs);tr=[]
 for a,b in zip(ps,ps[1:]):
  sa,sb=set(a),set(b);tr.append({"added":sorted(sb-sa)[:24],"removed":sorted(sa-sb)[:24],"jaccard":round(jac(sa,sb),6),"entropy_delta":round(entropy(b)-entropy(a),6)})
 return {"operator":"DERIVATIVE_LOCAL_DELTA","third_sizes":[len(x) for x in ps],"third_entropies":[round(entropy(x),6) for x in ps],"transitions":tr,"interpretation":"change signature only; not causal proof"}
derivative_signature=derivative

def blocks(text:str)->list[tuple[int,int,str]]:
 out=[];start=None;buf=[];ls=text.splitlines()
 for i,line in enumerate(ls,1):
  if line.strip():start=i if start is None else start;buf.append(line)
  elif buf:out.append((start or i,i-1,"\n".join(buf).strip()));start=None;buf=[]
 if buf:out.append((start or 1,len(ls),"\n".join(buf).strip()))
 return out
def plane(text:str)->tuple[str,list[str]]:
 low=text.casefold();scores={};found=[]
 for p,cs in CUES.items():
  hit=[c for c in cs if c in low]
  if hit:scores[p]=len(hit);found+=hit
 if FORMULA_RE.search(text):scores["MODEL_CANDIDATE"]=scores.get("MODEL_CANDIDATE",0)+1;found.append("formula-like-token")
 if not scores:return "BRAINSTORM_CANDIDATE",[]
 return max(scores,key=lambda p:(scores[p],PRIORITY.get(p,0))),sorted(set(found))
def invariants(text:str)->list[str]:
 low=text.casefold();return sorted(k for k,cs in INV.items() if any(c in low for c in cs))
def falsifier(text:str)->bool:
 low=text.casefold();return any(c in low for c in FALS)
def paradox(text:str)->bool:
 low=text.casefold();return any(c in low for c in AFFIRM) and any(c in low for c in NEGATE)

def load_manifest(path:Path,root:Path):
 m=json.loads(path.read_text(encoding="utf-8"));src=[];find=[]
 for item in m.get("sources",[]):
  p=root/item["path_hint"]
  if not p.is_file():find.append({"severity":"BLOCK","code":"SOURCE_MISSING","source_id":item.get("source_id"),"path":str(p)});continue
  raw=p.read_bytes();text=raw.decode("utf-8",errors="replace");actual=sha(raw);lines=len(text.splitlines())
  if actual!=item.get("sha256"):find.append({"severity":"BLOCK","code":"SOURCE_HASH_MISMATCH","source_id":item.get("source_id"),"expected":item.get("sha256"),"actual":actual})
  if len(raw)!=item.get("bytes"):find.append({"severity":"BLOCK","code":"SOURCE_SIZE_MISMATCH","source_id":item.get("source_id")})
  if lines!=item.get("lines"):find.append({"severity":"WARN","code":"SOURCE_LINE_COUNT_MISMATCH","source_id":item.get("source_id"),"expected":item.get("lines"),"actual":lines})
  src.append({"source_id":item["source_id"],"title":item["conversation_export_title"],"path":p,"path_hint":item["path_hint"],"sha256":actual,"bytes":len(raw),"lines":lines})
 return m,src,find

def build_event(s:dict[str,Any],start:int,end:int,fragment:str)->dict[str,Any]:
 ts=terms(fragment);p,c=plane(fragment);fh=sha(fragment.encode());g=[]
 if p=="HYPOTHESIS_CANDIDATE" and not falsifier(fragment):g.append({"class":"TV-TEST","reason":"hypothesis candidate has no explicit falsifier","required_test":"define a rejection condition or counterexample"})
 if p=="METRIC_CANDIDATE" and not UNIT_RE.search(fragment):g.append({"class":"TV-BOUNDARY","reason":"metric candidate has no explicit unit or dimension","required_test":"declare unit, domain and valid range"})
 if p=="GAP":g.append({"class":"TOKEN_VAZIO","reason":"gap explicitly observed","required_test":"preserve and type the missing information"})
 return {"schema":"sementeira.context-event/v1","event_id":"sem-"+sha(f"{s['sha256']}:{start}:{end}:{fh}".encode())[:20],"project":"Sementeira","source":{"source_id":s["source_id"],"title":s["title"],"path_hint":s["path_hint"],"source_sha256":s["sha256"],"line_start":start,"line_end":end,"fragment_sha256":fh},"state":"BRAINSTORM_CANDIDATE","plane":p,"literal_preserved_by_pointer":True,"token_count":len(ts),"unique_token_count":len(set(ts)),"top_terms":[x for x,_ in Counter(ts).most_common(16)],"classification_cues":c,"invariants":invariants(fragment),"derivative":derivative(ts),"antiderivative":{"operator":"ANTIDERIVATIVE_PROVENANCE_RETURN","reconstructs":["source_id","source_sha256","line_start","line_end","fragment_sha256"],"content_reconstruction_claimed":False,"roundtrip_state":"PENDING_VALIDATION"},"paradox_candidate":paradox(fragment),"falsifier_present":falsifier(fragment),"token_vazio":g,"forbidden_promotions":["CORRELATION_TO_CAUSATION","SYMBOL_TO_PHYSICAL_PROOF","BRAINSTORM_TO_VALIDATED_MEMORY","SOURCE_SNAPSHOT_TO_TRUTH"],"claim_allowed":False}

def validate_event(e:dict[str,Any],text:str)->list[str]:
 er=[]
 if e.get("claim_allowed") is not False:er.append("claim_allowed must remain false")
 if e.get("state")!="BRAINSTORM_CANDIDATE":er.append("initial source event must be BRAINSTORM_CANDIDATE")
 s=e.get("source")
 if not isinstance(s,dict):return er+["source must be an object"]
 a,b=s.get("line_start"),s.get("line_end")
 if not isinstance(a,int) or not isinstance(b,int) or a<1 or b<a:er.append("invalid source coordinates")
 else:
  frag="\n".join(text.splitlines()[a-1:b]).strip()
  if sha(frag.encode())!=s.get("fragment_sha256"):er.append("antiderivative provenance roundtrip failed")
  else:e["antiderivative"]["roundtrip_state"]="PASS_SOURCE_COORDINATE_HASH"
 if e.get("plane")=="HYPOTHESIS_CANDIDATE" and not e.get("falsifier_present") and not any(x.get("class")=="TV-TEST" for x in e.get("token_vazio",[])):er.append("hypothesis without falsifier must emit TV-TEST")
 return er

def relations(ev:list[dict[str,Any]],min_jaccard=.22,limit=500)->list[dict[str,Any]]:
 sets={e["event_id"]:set(e["top_terms"]) for e in ev};by=defaultdict(list)
 for eid,ss in sets.items():
  for t in ss:by[t].append(eid)
 rare={t for t,ids in by.items() if 2<=len(ids)<=4};cand=[]
 for i,l in enumerate(ev):
  for r in ev[i+1:]:
   a,b=l["event_id"],r["event_id"];over=sets[a]&sets[b];score=jac(sets[a],sets[b]);bridge=sorted(over&rare)
   if score>=min_jaccard or bridge:cand.append((score+min(len(bridge)*.03,.15),a,b,bridge))
 cand.sort(reverse=True)
 return [{"relation_id":"rel-"+sha(f"{a}:{b}".encode())[:18],"from":a,"to":b,"type":"HEURISTIC_SEMANTIC_CORRELATION","score":round(score,6),"rare_bridge_terms":bridge,"causality_claimed":False,"state":"FELTS","claim_allowed":False} for score,a,b,bridge in cand[:limit]]

def run_engine(manifest_path:Path,root:Path)->dict[str,Any]:
 m,src,find=load_manifest(manifest_path,root);ev=[];pc=Counter();gc=Counter();px=0
 for s in src:
  text=s["path"].read_text(encoding="utf-8",errors="replace")
  for a,b,frag in blocks(text):
   e=build_event(s,a,b,frag)
   for msg in validate_event(e,text):find.append({"severity":"BLOCK","code":"EVENT_INVALID","event_id":e["event_id"],"message":msg})
   ev.append(e);pc[e["plane"]]+=1;px+=int(e["paradox_candidate"])
   for gap in e["token_vazio"]:gc[gap["class"]]+=1
 rel=relations(ev);dupes=[];byh=defaultdict(list)
 for s in src:byh[s["sha256"]].append(s["source_id"])
 dupes=[ids for ids in byh.values() if len(ids)>1]
 for ids in dupes:find.append({"severity":"INFO","code":"DUPLICATE_SOURCE_CONTENT","source_ids":ids})
 block=sum(x["severity"]=="BLOCK" for x in find)
 out={"schema":"sementeira.context-baseline/v1","project":"Sementeira","method_status":"BRAINSTORM_THEN_FALSIFY","source_manifest_sha256":sha(manifest_path.read_bytes()),"source_count_declared":m.get("source_count"),"source_count_verified":len(src),"source_bytes_verified":sum(s["bytes"] for s in src),"source_lines_verified":sum(s["lines"] for s in src),"events":ev,"relations":rel,"statistics":{"event_count":len(ev),"relation_count":len(rel),"plane_counts":dict(sorted(pc.items())),"gap_counts":dict(sorted(gc.items())),"paradox_candidates":px,"duplicate_source_groups":len(dupes),"sampling_frame":"complete census of supplied local source snapshots","confidence_interval":None,"margin_of_error":None,"reason_no_margin":"deterministic census; semantic accuracy lacks independent ground truth"},"findings":find,"blocking_findings":block,"invariants":["source snapshot != validated memory","brainstorm != claim","derivative != causality","antiderivative returns provenance, not lost content","correlation != mechanism","symbolic != physical proof","TOKEN_VAZIO != zero"],"F_ok":["sources verified by SHA-256 and size","literal blocks preserved by source coordinates and fragment hashes","derivative signatures computed","antiderivative provenance roundtrips checked","correlations emitted only as FELTS","hypotheses without falsifiers emit TV-TEST"],"F_gap":["independent semantic ground truth","human review of candidate planes and paradoxes","calibrated similarity thresholds","cross-project source API for native GPT Project memory","longitudinal delta across future source snapshots"],"F_next":"Review false positives, freeze a labeled calibration set, then compare the next Project snapshot as an append-only delta.","claim_allowed":False}
 out["baseline_sha256"]=sha(canon(out).encode());return out

def markdown(r:dict[str,Any])->str:
 s=r["statistics"];lines=["# Sementeira — baseline de custódia contextual V1","",f"- Fontes: **{r['source_count_verified']}**",f"- Linhas: **{r['source_lines_verified']}**",f"- Eventos: **{s['event_count']}**",f"- Relações FELTS: **{s['relation_count']}**",f"- Bloqueios: **{r['blocking_findings']}**",f"- SHA-256: `{r['baseline_sha256']}`","","## Planos","","| Plano | Blocos |","|---|---:|"]
 lines += [f"| `{k}` | {v} |" for k,v in s["plane_counts"].items()]
 lines += ["","## Limite estatístico","","Censo determinístico das fontes fornecidas; acurácia semântica = `TOKEN_VAZIO_GROUND_TRUTH` até rotulagem independente.","","`claim_allowed=false`",""]
 return "\n".join(lines)
def main()->int:
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--manifest",required=True,type=Path);p.add_argument("--source-root",required=True,type=Path);p.add_argument("--output-json",required=True,type=Path);p.add_argument("--output-md",required=True,type=Path);p.add_argument("--strict",action="store_true");a=p.parse_args()
 try:r=run_engine(a.manifest,a.source_root)
 except (OSError,ValueError,json.JSONDecodeError,KeyError) as e:print(f"FAIL: {e}",file=sys.stderr);return 2
 a.output_json.parent.mkdir(parents=True,exist_ok=True);a.output_md.parent.mkdir(parents=True,exist_ok=True);a.output_json.write_text(json.dumps(r,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");a.output_md.write_text(markdown(r),encoding="utf-8");print(f"PASS: {r['source_count_verified']} sources, {r['statistics']['event_count']} events, {r['blocking_findings']} blocking findings");return 1 if a.strict and r["blocking_findings"] else 0
if __name__=="__main__":raise SystemExit(main())
