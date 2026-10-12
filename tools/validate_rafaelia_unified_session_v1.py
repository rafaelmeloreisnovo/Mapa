#!/usr/bin/env python3
"""Validate ONE logical RAFAELIA session view, not ChatGPT/Drive runtime facts.

Deterministic, standard-library only, pure source-side metadata gate.
A PASS here is not proof of author rights, private bytes, reviewer, runtime or science.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/assurance/rafaelia-unified-session-audit.v1.json"
PRED = ROOT / "data/assurance/novoexport-chart-route-audit.v1.json"
FAMILIES = {"F%02d" % n for n in range(1,27)}
GAPS = {"G%03d" % n for n in range(1,26)}
OWNERS = {"Mapa","RafPolimata","RafGitTools"}
STATES = {"OPEN","PARTIAL","NOT_RUN","FAIL_OBSERVED"}
RELATIONS = {"HAS_VECTOR","ROUTES_TO","BLOCKED_BY"}
NULL_KINDS = {"NUMERIC_ZERO","RESIDUE_ZERO","EMPTY_SET","NULL_VALUE",
              "TOKEN_VAZIO","UNDEFINED","NO_REAL_SOLUTION",
              "MISSING_OBSERVATION","NOT_APPLICABLE","APPROX_ZERO"}
L9 = ["LONGITUDINAL","ORTHOGONAL","TRANSVERSAL","PROVENANCE",
      "CONTEXTUAL","RELATIONAL","INDEXICAL","EVIDENTIAL","ADAPTIVE"]
S7 = ["TOKEN","BLOCK","FILE","PROJECT","ECOSYSTEM","CORPUS","MANIFOLD"]
PLANE5 = ["SOURCE","ARTIFACT","EXECUTION","EVIDENCE","CLAIM"]
ESSENTIAL = {
    "TOKEN_VAZIO_NE_ZERO_NE_NULL_NE_EMPTY_SET",
    "SOURCE_NE_ARTIFACT_NE_EXECUTION_NE_EVIDENCE_NE_CLAIM",
    "IMPLEMENTED_UNTESTED_NE_PASS",
    "USER_INPUT_NE_ASSISTANT_OUTPUT",
    "SAME_CARDINALITY_NE_GRAPH_ISOMORPHISM",
    "CHART_CACHE_NE_OBSERVATION",
    "CO_OCCURRENCE_NE_CAUSALITY",
    "RAPPORT_EVIDENCE_WEIGHT_ZERO",
    "NO_GAP_AUTO_CLOSURE",
    "CI_PASS_NE_PROVIDER_ENFORCEMENT",
    "PRIVATE_SOURCE_NE_PUBLIC_PROJECTION"
}

def _not_blank(x):
    return isinstance(x,str) and bool(x.strip()) and len(x)<768

def validate(v):
    issues=[]
    if not isinstance(v,dict):
        return ["ROOT_NOT_OBJECT"]
    if v.get("schema")!="rafaelia.unified-session-audit/v1":
        issues.append("SCHEMA_VERSION")
    if v.get("version")!="S1":
        issues.append("IMMUTABLE_SNAPSHOT_VERSION")
    session=v.get("logical_interaction",{})
    if not isinstance(session,dict) or session.get("id")!="SESSION_COMPOSITE_OMEGA" or session.get("type")!="COMPOSITE_VIEW_NOT_SOURCE_EVENT" or session.get("not_single_temporal_event") is not True or session.get("original_messages_mutated") is not False or session.get("claim_allowed") is not False or not str(session.get("raw_chat_session_id","")).startswith("TOKEN_VAZIO"):
        issues.append("PHANTOM_SINGLE_SOURCE_SESSION")
    if not isinstance(session,dict) or session.get("historical_exact_message_boundaries")!="TOKEN_VAZIO_SOURCE_GENEALOGY":
        issues.append("PHANTOM_MESSAGE_GENEALOGY")
    read=v.get("read_model",{})
    if not isinstance(read,dict) or read.get("start")!="START_HERE_CANONICAL_V2_2" or read.get("min_roots")!=3 or read.get("no_raw_corpus_replication") is not True:
        issues.append("SOURCE_FIRST_AND_PRIVATE_ROUTING")
    axis=v.get("axes",{})
    if not isinstance(axis,dict) or axis.get("L9")!=L9 or axis.get("S7")!=S7 or axis.get("plane5")!=PLANE5:
        issues.append("L9_S7_SOURCE_PLANES")
    null=v.get("typed_null_discriminants")
    if not isinstance(null,list) or len(null)!=10 or set(null)!=NULL_KINDS:
        issues.append("TYPED_EMPTY_NOT_ZERO")
    ins=v.get("critical_invariants")
    if not isinstance(ins,list) or len(set(ins))!=len(ins) or not ESSENTIAL.issubset(set(ins)):
        issues.append("BOUNDARIES_REMOVED")
    producers=v.get("producers",{})
    if not isinstance(producers,dict) or set(producers)!=OWNERS:
        issues.append("FEDERATED_PRODUCER_AUTHORITY")
    vectors=v.get("vectors")
    gaps=v.get("gaps")
    if not isinstance(vectors,list) or {x.get("id") for x in vectors if isinstance(x,dict)}!=FAMILIES or len(vectors)!=26:
        return issues+["VECTOR_COVERAGE_MISSING"]
    if not isinstance(gaps,list) or {x.get("id") for x in gaps if isinstance(x,dict)}!=GAPS or len(gaps)!=25:
        return issues+["GAP_COVERAGE_MISSING"]
    gap_map={x["id"]:x for x in gaps}
    for g in gaps:
        i=g["id"]
        if g.get("token_type")!="TOKEN_VAZIO" or not str(g.get("missing_reason","")).startswith("TOKEN_VAZIO_"):
            issues.append("GAP_TYPE_LOSS:"+i)
        if g.get("authority") not in OWNERS or g.get("state") not in STATES:
            issues.append("GAP_STATE_OR_AUTHORITY:"+i)
        if g.get("priority") not in {"P0","P1","P2"}:
            issues.append("GAP_PRIORITY:"+i)
        for k in ["evidence_required","falsifier","next_action","rollback"]:
            if not _not_blank(g.get(k)):
                issues.append("GAP_NO_"+k+":"+i)
        if g.get("receipt_state")!="REQUIRED_NOT_OBSERVED" or g.get("claim_allowed") is not False:
            issues.append("GAP_FAKE_CLOSURE:"+i)
        if g.get("rollback")!="KEEP_PREDECESSOR_NO_PROMOTION":
            issues.append("GAP_ROLLBACK_MUTATION:"+i)
    indexed=set()
    for f in vectors:
        i=f["id"]
        indexed.add(i)
        if f.get("producer") not in OWNERS or not _not_blank(f.get("family")) or not _not_blank(f.get("subtypes")) or not _not_blank(f.get("boundary")):
            issues.append("VECTOR_INCOMPLETE:"+i)
        if not isinstance(f.get("gaps"),list) or not f["gaps"] or len(f["gaps"])!=len(set(f["gaps"])) or any(g not in gap_map for g in f["gaps"]):
            issues.append("VECTOR_GAP_EDGE_MISSING:"+i)
        if f.get("claim_allowed") is not False or f.get("runtime_evidence_state")!="NOT_ESTABLISHED_FOR_THIS_VECTOR":
            issues.append("VECTOR_OVERCLAIM:"+i)
        if f.get("source_evidence_state")!="SCOPED_ROUTED_DOCUMENT_OR_SESSION_INTENT":
            issues.append("VECTOR_SOURCE_OVERCLAIM:"+i)
    covered={g for f in vectors for g in f.get("gaps",[]) if isinstance(f.get("gaps"),list)}
    if covered!=GAPS:
        issues.append("ORPHANED_GAP")
    kinds={f["id"]:f["family"] for f in vectors}
    for i,category in {
        "F03":"GRAFO_TOPOLOGICO_GEOMETRICO",
        "F04":"GRAFO_ZONAS_FISICAS",
        "F07":"CHART_OFFICE_XML",
        "F10":"CHART_CIENTIFICO_RLL",
        "F11":"CONJUNTOS_VAZIOS_E_DISCRIMINANTES",
        "F16":"CI_PROVIDER_GOVERNANCA",
        "F20":"LAMA_BARRO_PLUGIN",
        "F24":"NAVEGACAO_HUMANO_IA"}.items():
        if kinds.get(i)!=category:
            issues.append("SEMANTIC_NAMESPACE_COLLAPSE:"+i)
    topo=v.get("formal_falsification_fixtures",{})
    if not isinstance(topo,dict):
        topo={}
    c=topo.get("circulant_C42_pm6_pm7",{})
    ico=topo.get("icosphere_f2",{})
    if not isinstance(c,dict) or not isinstance(ico,dict) or any((c.get("v")!=42,c.get("e")!=84,c.get("degree")!=4,ico.get("v")!=42,ico.get("e")!=120,ico.get("f")!=80,ico.get("euler")!=2,c.get("namespace")==ico.get("namespace")):
        issues.append("GRAPH42_FALSE_ISOMORPHISM")
    z=topo.get("physical_zones",{})
    m=topo.get("historical_zone_metric_rows",{})
    if not isinstance(z,dict) or not isinstance(m,dict) or z.get("count")!=137 or z.get("partial_last_zone") is not True or m.get("count")!=136 or m.get("coverage_not_equal") is not True:
        issues.append("ZONE136_VS137_FALSE_COVERAGE")
    chart=topo.get("office_chart_xml",{})
    if not isinstance(chart,dict) or chart.get("count")!=6 or chart.get("source_workbook")!="TOKEN_VAZIO_UNBOUND" or chart.get("chart_cache_not_observational_data") is not True:
        issues.append("UNSOURCED_OFFICE_CHART_PROMOTION")
    graph=v.get("semantic_graph",{})
    nodes=graph.get("nodes") if isinstance(graph,dict) else None
    edges=graph.get("edges") if isinstance(graph,dict) else None
    if not isinstance(nodes,list) or not isinstance(edges,list):
        return issues+["GRAPH_NOT_TYPED"]
    by_id={x.get("id"):x for x in nodes if isinstance(x,dict)}
    expected_nodes={"SESSION_COMPOSITE_OMEGA"} | {"P_"+o for o in OWNERS} | FAMILIES | GAPS
    if set(by_id)!=expected_nodes or len(nodes)!=len(expected_nodes):
        issues.append("NODE_MISSING_OR_DUPLICATE")
    if by_id.get("SESSION_COMPOSITE_OMEGA",{}).get("type")!="COMPOSITE_VIEW":
        issues.append("GRAPH_FALSE_SESSION_EVENT")
    for f in vectors:
        if by_id.get(f["id"],{}).get("type")!="VECTOR" or by_id.get(f["id"],{}).get("owner")!=f["producer"]:
            issues.append("VECTOR_NODE_INCONSISTENCY:"+f["id"])
    for g in gaps:
        if by_id.get(g["id"],{}).get("type")!="TYPED_GAP" or by_id.get(g["id"],{}).get("owner")!=g["authority"]:
            issues.append("GAP_NODE_INCONSISTENCY:"+g["id"])
    expected_edges=set()
    for f in vectors:
        expected_edges.add(("SESSION_COMPOSITE_OMEGA","HAS_VECTOR",f["id"]))
        expected_edges.add((f["id"],"ROUTES_TO","P_"+f["producer"]))
        for g in f["gaps"]:
            expected_edges.add((f["id"],"BLOCKED_BY",g))
    actual_edges=set()
    for e in edges:
        if not isinstance(e,dict):
            issues.append("INVALID_EDGE")
            continue
        t=(e.get("from"),e.get("relation"),e.get("to"))
        if e.get("relation") not in RELATIONS or t[0] not in by_id or t[2] not in by_id:
            issues.append("DANGLING_OR_UNTYPED_EDGE")
        if not _not_blank(e.get("provenance")) or not _not_blank(e.get("epistemic")):
            issues.append("EDGE_WITHOUT_SOURCE_OR_STATE")
        actual_edges.add(t)
    if len(actual_edges)!=len(edges) or actual_edges!=expected_edges:
        issues.append("GRAPH_EDGE_BIJECTION_MISSING")
    evid=v.get("evidence_register")
    if not isinstance(evid,list) or len(evid)!=3 or any(r.get("state")!="PRIOR_OBSERVATION_NEEDS_CURRENT_HEAD_RECHECK" or r.get("claim_allowed") is not False or not _not_blank(r.get("provenance")) for r in evid):
        issues.append("PRIOR_CI_FALSE_PROMOTION")
    receipts=v.get("receipts")
    if not isinstance(receipts,list) or len(receipts)!=2 or any(r.get("state") not in {"TEMPLATE_NOT_EXECUTION","REVERT_PLAN_AVAILABLE_NOT_EXERCISED"} for r in receipts):
        issues.append("RECEIPT_FAKE_EXECUTION")
    gate=v.get("promotion",{})
    if not isinstance(gate,dict) or any(gate.get(k) is not False for k in ["claim_allowed","repo_merge_allowed","source_code_promotion_allowed"]):
        issues.append("PROMOTION_UNAUTHORIZED")
    pred=v.get("predecessor",{})
    if not isinstance(pred,dict) or pred.get("path")!="data/assurance/novoexport-chart-route-audit.v1.json" or pred.get("relation")!="EXTENDS_NOT_REPLACES":
        issues.append("LOSS_OF_PREDECESSOR")
    if not PRED.is_file():
        issues.append("PREDECESSOR_FILE_MISSING")
    # A public control-plane catalog must never carry private Drive URLs.
    # The ban applies to all string fields, not just known source fields.
    raw=json.dumps(v,ensure_ascii=False)
    if re.search(r"https?://|drive\.google\.com|docs\.google\.com|(?:sk-[A-Za-z0-9_-]{12,})",raw,re.I):
        issues.append("PRIVATE_LINK_OR_SECRET_IN_PUBLIC_MANIFEST")
    return sorted(set(issues))

if __name__=="__main__":
    try:
        obj=json.loads(SOURCE.read_text(encoding="utf-8"))
        problems=validate(obj)
    except (OSError,ValueError,UnicodeError) as error:
        problems=["READ_ERROR_"+type(error).__name__]
    print(json.dumps({"gate":"UNIFIED_SESSION_SOURCE_METADATA_V1",
                      "result":"PASS_SCOPED" if not problems else "FAIL",
                      "scope":"PUBLIC_SANITIZED_PROJECTION_ONLY",
                      "claim_allowed":False,"problems":problems},sort_keys=True))
    raise SystemExit(bool(problems))
