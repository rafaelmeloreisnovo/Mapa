#!/usr/bin/env python3
"""RAFAELIA authorial/upstream intake: fail-closed *metadata* validation only.
This program cannot authenticate legal ownership, Git blobs or live provider state.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data/assurance/federated-authorship-intake-20261011.v1.json"
CATEGORIES = {
    "UPSTREAM_DERIVED", "UPSTREAM_MODIFIED", "PROJECT_LOCAL_TRACEABLE_AI_ASSISTED",
    "PROJECT_DECLARED_AUTHORIAL", "RESEARCH_REFERENCE", "MIXED_UNVERIFIED",
    "RESTRICTED_PRIVATE", "PRODUCER_BOUNDARY", "CONSUMER_BOUNDARY",
}
REQUIRED = {
    "id", "producer_repo", "source_path", "observed_git_blob",
    "origin_class", "license_state", "source_layer", "blocker", "reason",
    "copy_policy", "claim_allowed", "independent_rights_review",
    "physical_runtime_proof", "personal_data_included",
}
BLOCKED_LICENSE_TOKENS = ("TOKEN_VAZIO", "CONFLICT", "PATH_SPECIFIC", "CUSTOM_PROPOSED")
EXPECTED_IDS = {
    "VECTRAS_UPSTREAM", "VECTRAS_FORK_ABOUT", "VECTRAS_RMR_VECTOR",
    "TERMUX_APP", "TERMUX_PACKAGES", "LLAMA_UPSTREAM", "LLAMA_BITSTACK",
    "GAIA_PHI_BL0", "GAIA_PHI_NET", "GAIA_PDS_MANIFESTO",
    "GAIA_COLLECTION", "RAFAELIA_PRIVATE", "RLL_COSMOLOGY",
    "RAFPOLIMATA_L0", "RAFGITTOOLS_LICENSE",
}

def verify(doc: Any) -> list[str]:
    if not isinstance(doc, dict):
        return ["INVALID_ROOT"]
    issues = []
    if (doc.get("schema") != "rafaelia.federated-authorship-intake/v1" or
            doc.get("scope") != "SOURCE_POINTERS_ONLY_NO_CODE_CLONING" or
            doc.get("decision") != "HOLD_NO_PROMOTION" or
            doc.get("claim_allowed") is not False or
            doc.get("scientific_novelty_proven") is not False or
            doc.get("all_entries_copy_blocked") is not True):
        issues.append("GLOBAL_PROMOTION_OR_SCHEMA_DRIFT")
    if set(doc) != {"schema","as_of_date","scope","source_authority","decision",
                    "claim_allowed","scientific_novelty_proven",
                    "all_entries_copy_blocked","policy","entries"}:
        issues.append("UNKNOWN_OR_MISSING_ROOT_FIELDS")
    policy=doc.get("policy")
    if not isinstance(policy,dict) or set(policy)!={
        "upstream_copyright_retained","project_local_is_not_global_priority",
        "license_compatibility_requires_per_file_evidence","pure_L0_requires_zero_OS_runtime",
        "source_not_artifact_not_execution_not_evidence_not_claim",
        "no_private_payload","skipped_is_not_pass"
    } or any(v is not True for v in policy.values()):
        issues.append("POLICY_INVARIANT_DISABLED")
    if doc.get("source_authority")!="INDIVIDUAL_PRODUCER_REPOSITORY":
        issues.append("AUTHORITY_LAUNDERING")
    entries=doc.get("entries")
    if not isinstance(entries,list) or len(entries)!=15:
        return issues+["SOURCE_CARDINALITY_DRIFT"]
    ids=set()
    for pos,item in enumerate(entries):
        prefix=f"entry[{pos}]"
        if not isinstance(item,dict):
            issues.append(prefix+":NOT_OBJECT")
            continue
        if set(item)!=REQUIRED:
            issues.append(prefix+":SCHEMA_DRIFT")
        id_=item.get("id")
        if not isinstance(id_,str) or id_ not in EXPECTED_IDS or id_ in ids:
            issues.append(prefix+":IDENTITY_INVALID")
        else:
            ids.add(id_)
        origin=item.get("origin_class")
        if not isinstance(origin,str) or origin not in CATEGORIES:
            issues.append(prefix+":ORIGIN_UNTYPED")
        for name in ("producer_repo","source_path","license_state","source_layer","blocker","reason"):
            v=item.get(name)
            if not isinstance(v,str) or not v.strip() or len(v)>1024:
                issues.append(prefix+":MISSING_"+name.upper())
        sha=item.get("observed_git_blob")
        if (not isinstance(sha,str) or len(sha)!=40 or
                any(c not in "0123456789abcdef" for c in sha)):
            issues.append(prefix+":BLOB_UNVERIFIED_FORMAT")
        if (item.get("copy_policy")!="NO_SOURCE_TRANSPLANT_METADATA_POINTER_ONLY" or
                item.get("claim_allowed") is not False or
                item.get("independent_rights_review")!="TOKEN_VAZIO" or
                item.get("physical_runtime_proof")!="NOT_RUN" or
                item.get("personal_data_included") is not False):
            issues.append(prefix+":SOURCE_PROMOTION_OR_PRIVACY_BYPASS")
        license_=item.get("license_state")
        if id_=="VECTRAS_RMR_VECTOR" and license_!="GPL-2.0-only":
            issues.append(prefix+":VECTRAS_LICENSE_DOWNGRADE")
        if id_=="RAFGITTOOLS_LICENSE" and license_!="GPL-3.0-OR-LATER":
            issues.append(prefix+":RAFGITTOOLS_LICENSE_DOWNGRADE")
        if id_=="LLAMA_BITSTACK" and item.get("source_layer")!="C_HOSTED_NOT_L0":
            issues.append(prefix+":HOSTED_BITSTACK_MISLABELED_AS_L0")
        if id_=="GAIA_PHI_NET" and item.get("source_layer")!="OS_SERVICE_BOUNDARY":
            issues.append(prefix+":NETWORK_SYSCALLS_MISLABELED_AS_L0")
        if id_=="RAFAELIA_PRIVATE" and origin!="RESTRICTED_PRIVATE":
            issues.append(prefix+":PRIVATE_SCOPE_DECLASSIFIED")
        if id_=="RLL_COSMOLOGY" and origin!="RESEARCH_REFERENCE":
            issues.append(prefix+":SCIENTIFIC_CLAIM_PROMOTION")
    if ids!=EXPECTED_IDS:
        issues.append("SOURCES_MISSING_OR_DUPLICATED")
    return issues

def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--file",type=Path,default=DEFAULT)
    args=parser.parse_args()
    try:
        doc=json.loads(args.file.read_text(encoding="utf-8"))
        issues=verify(doc)
    except (OSError,UnicodeError,ValueError) as exc:
        issues=["READ_PARSE_ERROR:"+type(exc).__name__]
    print(json.dumps({"schema":"rafaelia.authorship-intake-receipt/v1",
                      "scope":"METADATA_ONLY","claim_allowed":False,
                      "state":"FAIL" if issues else "PASS_SCOPED",
                      "issues":issues},indent=2,ensure_ascii=False))
    return int(bool(issues))

if __name__=="__main__":
    raise SystemExit(main())
