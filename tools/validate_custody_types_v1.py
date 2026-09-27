#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

EXPECTED = {
    "C01_SOURCE_ORIGIN","C02_DOCUMENT_STATE","C03_CODE_STATE",
    "C04_EXECUTION","C05_EVIDENCE","C06_TRANSFER_HANDOFF",
    "C07_CLAIM_PROMOTION","C08_CROSS_PROVIDER_BRIDGE","C09_CREDENTIAL_AUTHORITY",
}
DIGEST = {"content_digest","receipt_digest"}
PROVIDER = {"git_commit_oid","git_blob_oid","drive_revision_id","provider_request_id"}
STATES = {
    "PASS","FAIL","NOT_RUN","PENDING","AUDIT","TOKEN_VAZIO",
    "IMPLEMENTED_UNTESTED","OBSERVED_UNPROMOTED","ROUTE_STATE_BLOCKED",
}
CANONICAL_REGISTRY = "data/control-plane/CUSTODY_CHAIN_TYPE_REGISTRY.v1.json"
MAPPING = "data/governance/custody/01_ATLAS/CUSTODY_TYPES_V1_CANONICAL_MAPPING.json"

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def validate_taxonomy(data):
    errors=[]
    def req(cond,msg):
        if not cond: errors.append(msg)
    req(data.get("schema")=="rafaelia.custody.types.v1","taxonomy schema mismatch")
    ids=[x.get("id") for x in data.get("classes",[]) if isinstance(x,dict)]
    req(set(ids)==EXPECTED,"custody class set mismatch")
    req(len(ids)==len(set(ids)),"duplicate class ids")
    inv=set(data.get("invariants",[]))
    for item in (
        "SOURCE!=ARTIFACT!=EXECUTION!=EVIDENCE!=CLAIM",
        "AUTHORIZATION!=EXECUTION!=CUSTODY!=OBSERVATION!=PROMOTION",
        "PROVIDER_REVISION_ID!=CONTENT_DIGEST",
        "GIT_OBJECT_ID!=RECEIPT_DIGEST",
        "HASH_CHAIN!=MERKLE_TREE",
    ):
        req(item in inv,"missing invariant "+item)
    req(data.get("chain_models",{}).get("linear_hash_chain",{}).get("merkle_claim_allowed") is False,
        "linear hash chain mislabeled merkle")
    req(data.get("authority_status")=="LOCAL_TYPED_PROJECTION",
        "local taxonomy must declare LOCAL_TYPED_PROJECTION authority status")
    req(data.get("canonical_registry_ref")==CANONICAL_REGISTRY,
        "canonical registry pointer mismatch")
    req(data.get("canonical_mapping_ref")==MAPPING,
        "canonical mapping pointer mismatch")
    req(data.get("claim_allowed") is False,"projection must remain claim_allowed=false")
    return errors

def validate_projection(taxonomy, canonical, mapping):
    errors=[]
    def req(cond,msg):
        if not cond: errors.append(msg)

    req(canonical.get("schema_version")=="rafaelia.custody-chain-type-registry.v1",
        "canonical registry schema mismatch")
    canonical_profiles={x.get("profile_id") for x in canonical.get("custody_profiles",[]) if isinstance(x,dict)}
    canonical_actors={x.get("actor_class") for x in canonical.get("actor_classes",[]) if isinstance(x,dict)}

    req(mapping.get("schema")=="rafaelia.custody.projection-map.v1","projection map schema mismatch")
    req(mapping.get("authority_status")=="CANONICAL_REGISTRY_PRECEDENCE",
        "projection must declare canonical registry precedence")
    req(mapping.get("canonical_registry_ref")==CANONICAL_REGISTRY,
        "projection canonical registry pointer mismatch")
    req(mapping.get("projection_ref")=="data/governance/custody/00_INDEX/custody_types_v1.json",
        "projection taxonomy pointer mismatch")
    req(mapping.get("claim_allowed") is False,"projection map must remain claim_allowed=false")

    rows=[x for x in mapping.get("class_mapping",[]) if isinstance(x,dict)]
    local_ids=[x.get("local_class") for x in rows]
    req(set(local_ids)==EXPECTED,"projection must cover every C01..C09 local class exactly")
    req(len(local_ids)==len(set(local_ids)),"projection contains duplicate local classes")

    for row in rows:
        cid=row.get("local_class")
        targets=row.get("canonical_profiles",[])
        req(isinstance(targets,list),f"{cid}: canonical_profiles must be a list")
        unknown=set(targets)-canonical_profiles if isinstance(targets,list) else set()
        req(not unknown,f"{cid}: unknown canonical profiles: {sorted(unknown)}")
        if not targets:
            req(str(row.get("mapping_state","")).startswith("TOKEN_VAZIO"),
                f"{cid}: unmapped class must remain TOKEN_VAZIO")
            req(bool(row.get("gap")),f"{cid}: unmapped class requires explicit gap")
        else:
            req(row.get("mapping_state") in {"DIRECT","CONDITIONAL"},
                f"{cid}: mapped class requires DIRECT or CONDITIONAL state")

    c09=next((x for x in rows if x.get("local_class")=="C09_CREDENTIAL_AUTHORITY"),{})
    req(c09.get("canonical_profiles")==[],"C09 must not invent a direct canonical credential profile")
    req(str(c09.get("mapping_state","")).startswith("TOKEN_VAZIO"),
        "C09 must remain explicit TOKEN_VAZIO without direct canonical profile")

    actor_map=mapping.get("actor_mapping",{})
    for key in ("authorized_by","planned_by","executed_by_connector","executed_by_runtime","independent_review","unknown_actor"):
        target=actor_map.get(key)
        req(target in canonical_actors,f"actor mapping {key} -> {target!r} is not canonical")
    req(actor_map.get("custodied_by")=="SURFACE_AUTHORITY_NOT_ACTOR_CLASS",
        "custodied_by must remain a surface authority, not be forced into an actor class")

    req(taxonomy.get("canonical_registry_ref")==mapping.get("canonical_registry_ref"),
        "taxonomy and mapping disagree on canonical registry")
    return errors

def validate_event(event, taxonomy):
    errors=[]
    def req(cond,msg):
        if not cond: errors.append(msg)
    req(event.get("schema")=="rafaelia.custody.event.v1","event schema mismatch")
    req(event.get("custody_class") in EXPECTED,"unknown custody class")
    actors=event.get("actors",{})
    for role in ("authorized_by","executed_by","custodied_by"):
        req(isinstance(actors.get(role),dict),"missing actor "+role)
    if isinstance(actors.get("planned_by"),dict) and actors["planned_by"].get("type")=="assistant_session":
        req(actors.get("authorized_by",{}).get("type")!="assistant_session",
            "assistant session must not self-authorize")
    integrity=event.get("integrity",{})
    kind=integrity.get("identity_kind")
    algorithm=integrity.get("algorithm")
    canonicalization=integrity.get("canonicalization")
    req(kind in DIGEST|PROVIDER,"invalid integrity kind")
    if kind in DIGEST:
        req(isinstance(algorithm,str) and bool(algorithm.strip()),"digest requires algorithm")
    if kind=="receipt_digest":
        req(isinstance(canonicalization,str) and bool(canonicalization.strip()),
            "receipt_digest requires canonicalization")
    if kind in PROVIDER:
        req(algorithm in (None,"TOKEN_VAZIO"),
            "provider identity must not be mislabeled as cryptographic digest algorithm")
        req(canonicalization in (None,"TOKEN_VAZIO"),
            "provider identity must not carry digest canonicalization")
    if kind in {"git_commit_oid","git_blob_oid"}:
        req(bool(re.fullmatch(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}",str(integrity.get("value","")))),
            "git oid must be 40 or 64 hex")
    req(event.get("state") in STATES,"invalid state")
    if event.get("gap") not in ("none","NONE","TOKEN_VAZIO",""):
        req(event.get("claim_allowed") is False,"open gap must keep claim_allowed=false")
    return errors

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--taxonomy",default="data/governance/custody/00_INDEX/custody_types_v1.json")
    parser.add_argument("--canonical",default=CANONICAL_REGISTRY)
    parser.add_argument("--mapping",default=MAPPING)
    parser.add_argument("--event")
    args=parser.parse_args()

    taxonomy=load(args.taxonomy)
    canonical=load(args.canonical)
    mapping=load(args.mapping)

    errors=validate_taxonomy(taxonomy)
    errors+=validate_projection(taxonomy,canonical,mapping)
    if args.event:
        errors+=validate_event(load(args.event),taxonomy)

    if errors:
        print("FAIL")
        for error in errors:
            print(" -",error)
        return 1

    print("PASS: local custody taxonomy")
    print("PASS: canonical federation registry precedence")
    print("PASS: C01..C09 crosswalk uses only evidenced canonical profiles")
    print("PASS: C09 remains TOKEN_VAZIO where no direct canonical profile exists")
    print("PASS: authorization/execution/custody separation")
    print("PASS: provider identity/digest separation")
    print("PASS: hash-chain/Merkle separation")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
