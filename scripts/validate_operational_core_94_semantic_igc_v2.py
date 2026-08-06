#!/usr/bin/env python3
"""Fail-closed semantic/IGC validator for the sharded Operational Core 94 V2."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
NODE_RE=re.compile(r"^OC94-(\d{3})$"); PATH_RE=re.compile(r"^SP-(\d{3})$"); SHA256_RE=re.compile(r"^[0-9a-f]{64}$")
GATES=("G_S","G_D","G_T","G_I","G_E","G_F","G_C")
PATH_TYPES={"GOVERNANCE","PROVENANCE","SEMANTIC_DEPENDENCY","GENERATOR_LINEAGE","CUSTODY","NAVIGATION","SEMANTIC_ARTICULATION","REDUNDANCY"}
def fail(m): raise SystemExit(f"FAIL: {m}")
def root_for(reg:Path)->Path:
    if reg.parent.name=="core" and reg.parent.parent.name=="data": return reg.parents[2]
    return reg.parent
def load_shards(root:Path, rels:list[str], schema:str)->list[dict]:
    out=[]
    for rel in rels:
        p=root/rel
        if not p.is_file(): fail(f"missing shard {rel}")
        obj=json.loads(p.read_text(encoding="utf-8"))
        if obj.get("schema")!=schema or not isinstance(obj.get("items"),list): fail(f"invalid shard {rel}")
        out.extend(obj["items"])
    return out
def main()->int:
    reg=Path(sys.argv[1]) if len(sys.argv)>1 else Path("data/core/operational-core-94.semantic-igc.v2.json")
    d=json.loads(reg.read_text(encoding="utf-8")); root=root_for(reg)
    if d.get("schema")!="rafaelia.operational-core-94.semantic-igc.v2": fail("unexpected schema")
    if d.get("claim_allowed") is not False: fail("global claim_allowed must remain false")
    for x in ("append-only","non-destructive","fail-closed","evidence-first"):
        if x not in set(d.get("mode",[])): fail(f"missing mode {x}")
    nodes=load_shards(root,d.get("node_shards",[]),"rafaelia.operational-core-94.nodes-shard.v2")
    paths=load_shards(root,d.get("path_shards",[]),"rafaelia.operational-core-94.paths-shard.v2")
    b=d.get("boundary",{})
    if b.get("expected_total")!=94: fail("expected_total must remain 94")
    if b.get("identified_count")!=len(nodes): fail("identified_count mismatch")
    if b.get("unitemized_count")!=94-len(nodes): fail("boundary does not close to 94")
    if b.get("original_itemizing_artifact")!="TOKEN_VAZIO_NOT_LOCATED_AFTER_DRIVE_AND_GITHUB_SEARCH": fail("itemization source must remain explicit TOKEN_VAZIO")
    gap=b.get("unitemized_range",{})
    if gap.get("count")!=94-len(nodes) or gap.get("first_id")!=f"OC94-{len(nodes)+1:03d}" or gap.get("last_id")!="OC94-094": fail("unitemized range mismatch")
    ext={x.get("id"):x for x in d.get("external_references",[])}; ids=[]; titles=set(); providers={}
    for i,n in enumerate(nodes,1):
        nid=n.get("id"); m=NODE_RE.fullmatch(nid or "")
        if not m or int(m.group(1))!=i: fail(f"node IDs must be contiguous: {nid}")
        if nid in ids: fail(f"duplicate node {nid}")
        ids.append(nid); title=n.get("title")
        if not isinstance(title,str) or not title.strip() or title in titles: fail(f"invalid/duplicate title {title!r}")
        titles.add(title)
        if n.get("claim_allowed") is not False: fail(f"node {nid} promoted claim")
        if n.get("read_state")!="READ_COMPLETE": fail(f"node {nid} not read completely")
        for k in ("source","semantic","execution_state","scientific_validation_state","F_ok","F_gap","F_next"):
            if k not in n: fail(f"node {nid} missing {k}")
        src=n["source"]; provider=src.get("provider_id")
        if provider: providers[nid]=provider
        if 10<=i<=16:
            if not provider: fail(f"output {nid} missing provider_id")
            if not SHA256_RE.fullmatch(src.get("sha256",'')): fail(f"output {nid} missing SHA-256")
            if not isinstance(src.get("bytes"),int) or src["bytes"]<0: fail(f"output {nid} missing bytes")
            if src.get("identity_rule")!="provider_id+parent_id+bytes+sha256": fail(f"output {nid} weak identity rule")
        if 10<=i<=15:
            g=n.get("generator",{}); er=g.get("external_ref")
            if er not in ext: fail(f"output {nid} generator ref missing")
            if g.get("revision")!=ext[er].get("revision") or g.get("blob_sha")!=ext[er].get("blob_sha"): fail(f"output {nid} generator lineage mismatch")
        if i==16 and n.get("generator",{}).get("lineage_state")!="TOKEN_VAZIO_GENERATOR_NOT_LOCATED": fail("zone53 generator must remain TOKEN_VAZIO")
    sem=d.get("semantic_method",{}); gp=sem.get("graph_projection",{})
    if gp.get("transformation_family")!="DISCRETE_TYPED_GRAPH_PROJECTION" or gp.get("epsilon")!=0: fail("wrong graph projection")
    if gp.get("claim_scope")!="OPERATIONAL_MODEL_NOT_UNIVERSAL_GEOMETRIC_THEOREM": fail("scope overclaim")
    if sem.get("identity_invariant")!="source_locator + source_revision + content_sha256": fail("identity invariant weakened")
    endpoints=set(ids)|set(ext); pids=[]
    for i,p in enumerate(paths,1):
        pid=p.get("path_id"); m=PATH_RE.fullmatch(pid or "")
        if not m or int(m.group(1))!=i: fail(f"path IDs must be contiguous: {pid}")
        if pid in pids: fail(f"duplicate path {pid}")
        pids.append(pid)
        if p.get("source") not in endpoints or p.get("target") not in endpoints: fail(f"unknown endpoint in {pid}")
        if p.get("path_type") not in PATH_TYPES: fail(f"invalid path type in {pid}")
        profile=sem.get("gate_profiles",{}).get(p.get("gate_profile"),{})
        if profile.get("transformation_family")!="DISCRETE_TYPED_GRAPH_PROJECTION": fail(f"wrong transformation in {pid}")
        if profile.get("state")!="VERIFIED_LIMITED_STATIC" or p.get("state")!="VERIFIED_LIMITED_STATIC": fail(f"path {pid} over/under classified")
        if profile.get("claim_allowed") is not False or p.get("claim_allowed") is not False: fail(f"path {pid} promoted claim")
        for g in GATES:
            if profile.get("cohesion_gates",{}).get(g)!="PASS": fail(f"path {pid} missing gate {g}")
        for k in ("scope","evidence","negative_rule"):
            if not p.get(k): fail(f"path {pid} missing {k}")
        inv=set(profile.get("preserved_invariants",[]))
        for x in ("source_identity","target_identity","typed_incidence","epistemic_state","claim_gate_false"):
            if x not in inv: fail(f"path {pid} missing invariant {x}")
    metrics=d.get("path_metrics",{})
    if metrics.get("declared_paths")!=len(paths) or metrics.get("verified_limited_static")!=len(paths): fail("path metrics mismatch")
    if metrics.get("physical_execution_verified")!=0: fail("physical execution cannot be promoted")
    if metrics.get("independent_scientific_validation_verified")!=0: fail("independent validation cannot be promoted")
    groups=metrics.get("content_duplicate_groups",[])
    if len(groups)!=1 or groups[0].get("members")!=["OC94-014","OC94-015"]: fail("duplicate group contract missing")
    if providers.get("OC94-014")==providers.get("OC94-015"): fail("distinct provider identities collapsed")
    if nodes[13]["source"].get("sha256")!=nodes[14]["source"].get("sha256"): fail("declared byte-identical pair hash mismatch")
    expected={"anchors_read_complete":6,"p2_outputs_provider_ids_resolved":7,"p2_outputs_sha256_resolved":7,"p2_generator_lineage_resolved":6,"termux_physical_execution_verified":0,"independent_review_verified":0,"original_94_itemization_source_located":0}
    for k,v in expected.items():
        if d.get("resolved_deltas",{}).get(k)!=v: fail(f"resolved delta mismatch: {k}")
    print(json.dumps({"status":"PASS","event_id":d["event_id"],"nodes":len(nodes),"paths":len(paths),"identified":len(nodes),"unitemized":94-len(nodes),"anchors_read":6,"p2_provider_sha_resolved":7,"generator_lineage_resolved":6,"physical_execution_verified":0,"independent_validation_verified":0,"claim_allowed":False},ensure_ascii=False,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
