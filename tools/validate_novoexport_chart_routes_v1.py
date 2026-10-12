#!/usr/bin/env python3
"""Validate sanitized NOVOexport chart/route intake without pretending to verify Drive bytes.
No third-party packages; hosted factory validator, never an L0 runtime dependency.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/assurance/novoexport-chart-route-audit.v1.json"
EXPECTED_IDS={
"NOVO_RAW_SHARD_BASELINE","OFFICE_CHART1_6","GRAPHVIZ_CAMADA_SEM_NOME",
"TOROID_PSY_CYCLE","Z42_CIRCULANT","ICOSPHERE_F2","RLL_FIGURE_PIPELINE",
"RLL_QUANTITATIVE_F2_F10","ACTIVE_BOOTSTRAP_ROUTE","SOURCE_ARTIFACT_RECON"
}
EXPECTED_ROLES={
"Mapa":"INDEX_ROUTE_GAP_AUTHORITY",
"RafPolimata":"FREESTANDING_MATH_KERNEL_AUTHORITY",
"RafGitTools":"CONSENTED_PRIVATE_INGEST_AND_RECEIPTS",
}
EXPECTED_INVARIANTS={
"source_not_artifact_not_execution_not_evidence_not_claim",
"novoshard_count_not_full_semantic_scan","role_input_not_assistant_output",
"cooccurrence_not_causality","same_node_count_not_isomorphism",
"rapport_evidence_weight_zero","chart_cache_not_observation",
"opt_in_llama_not_lama_plugin","scientific_smoke_not_posterior",
"no_external_code_transplant",
}
ENTRY_FIELDS={"id","kind","source_alias","owner","state","chart_role",
"target","gap","claim_allowed"}
ALLOWED_KIND={"CORPUS_INDEX","OFFICE_XML_CHART_CACHE","GRAPHVIZ_SCHEMATIC",
"SYMBOLIC_DIAGRAM","FORMAL_GRAPH","SCIENCE_CLAIM_CHART","GOVERNANCE_ROUTE"}
ALLOWED_TARGET={"Mapa","RafPolimata","RafGitTools"}
def validate(v):
    issues=[]
    if not isinstance(v,dict):
        return ["ROOT_NOT_OBJECT"]
    if v.get("schema")!="rafaelia.novoexport.chart-route-reconstruction/v1":
        issues.append("SCHEMA")
    if v.get("scope")!="SYNTHETIC_AND_SANITIZED_INDEX_ONLY":
        issues.append("SCOPE")
    for k,expected in (("live_provider_provenance_verified",False),
                       ("all_chart_data_ingested",False),
                       ("raw_private_payload_included",False),
                       ("all_claims_blocked",True),("claim_allowed",False)):
        if v.get(k) is not expected:
            issues.append("PROMOTION_OR_PRIVACY:"+k)
    if v.get("roles")!=EXPECTED_ROLES:
        issues.append("PRODUCER_AUTHORITY_DRIFT")
    inv=v.get("boundaries")
    if not isinstance(inv,dict) or set(inv)!=EXPECTED_INVARIANTS or any(x is not True for x in inv.values()):
        issues.append("INVARIANT_DOWNGRADE")
    formal=v.get("formal_fixtures",{})
    a=formal.get("C42pm6pm7",{}) if isinstance(formal,dict) else {}
    b=formal.get("icosphere_f2",{}) if isinstance(formal,dict) else {}
    if a!={"vertices":42,"edges":84,"degree":4} or b!={"vertices":42,"edges":120,"faces":80,"euler":2}:
        issues.append("Z42_ICOSPHERE_COLLISION")
    cached=v.get("observed_chart_cache",{})
    if not isinstance(cached,dict) or cached!={"count":6,
       "generic_series_chart_ids":[1,2,3,5,6], "sales_like_chart_ids":[4],
       "source_workbook":"TOKEN_VAZIO_UNBOUND",
       "specific_dataset":"TOKEN_VAZIO_UNBOUND",
       "physical_measurement":False}:
        issues.append("OFFICE_TEMPLATE_MISPROMOTION")
    baseline=v.get("observed_novo_baseline",{})
    if not isinstance(baseline,dict) or baseline!={"shards":51,
        "root_items":5054, "nonempty_conversations":5052,
        "user_messages":111367, "assistant_messages":185427,
        "state":"DERIVED_HISTORICAL_NOT_RECOUNTED"}:
        issues.append("BASELINE_AS_LIVE_SCAN")
    items=v.get("entries")
    if not isinstance(items,list) or len(items)!=len(EXPECTED_IDS):
        return issues+["ENTRY_COUNT"]
    seen=set()
    for i,r in enumerate(items):
        pre="ENTRY_"+str(i)+":"
        if not isinstance(r,dict) or set(r)!=ENTRY_FIELDS:
            issues.append(pre+"SCHEMA")
            continue
        n=r["id"]
        if n not in EXPECTED_IDS or n in seen:
            issues.append(pre+"IDENTITY")
        seen.add(n)
        if r["kind"] not in ALLOWED_KIND or r["target"] not in ALLOWED_TARGET:
            issues.append(pre+"KIND_AUTHORITY")
        if r["claim_allowed"] is not False:
            issues.append(pre+"CLAIM_NOT_BLOCKED")
        for field in ["source_alias","owner","state","chart_role","gap"]:
            s=r.get(field)
            if not isinstance(s,str) or not s.strip() or len(s)>512:
                issues.append(pre+"MISSING_"+field)
            elif "https://" in s or "drive.google.com" in s or "docs.google.com" in s:
                issues.append(pre+"PRIVATE_LINK_IN_PUBLIC_CATALOG")
    if seen!=EXPECTED_IDS:
        issues.append("MISSING_OR_DUPLICATED")
    byid={r.get("id"):r for r in items if isinstance(r,dict)}
    for key,kind,role in [
        ("OFFICE_CHART1_6","OFFICE_XML_CHART_CACHE","RENDERED_EXAMPLE_NOT_DATA"),
        ("Z42_CIRCULANT","FORMAL_GRAPH","MATH_SPEC_NOT_KERNEL"),
        ("ICOSPHERE_F2","FORMAL_GRAPH","MATH_SPEC_NOT_KERNEL"),
        ("RLL_QUANTITATIVE_F2_F10","SCIENCE_CLAIM_CHART","UNVERIFIED_QUANTITATIVE"),
        ("ACTIVE_BOOTSTRAP_ROUTE","GOVERNANCE_ROUTE","OPERATIONAL_CONTROL_PLANE")]:
        r=byid.get(key,{})
        if r.get("kind")!=kind or r.get("chart_role")!=role:
            issues.append("MATERIAL_DOMAIN_DRIFT:"+key)
    if byid.get("RLL_QUANTITATIVE_F2_F10",{}).get("state")!="HISTORICAL_PLANNED_OUTPUTS":
        issues.append("RLL_QUANTITATIVE_UNVERIFIED")
    if byid.get("NOVO_RAW_SHARD_BASELINE",{}).get("state")!="DERIVED_BASELINE_NOT_RECOUNTED":
        issues.append("CORPUS_COVERAGE_FRAUD")
    return issues

if __name__=="__main__":
    try:
        data=json.loads(SOURCE.read_text("utf-8"))
        problems=validate(data)
    except (OSError,ValueError,UnicodeError) as error:
        problems=["READ_OR_PARSE_ERROR:"+type(error).__name__]
    print(json.dumps({"state":"PASS_SCOPED" if not problems else "FAIL",
                      "scope":"SANITIZED_METADATA_ONLY",
                      "claim_allowed":False,"issues":problems},sort_keys=True))
    raise SystemExit(bool(problems))
