#!/usr/bin/env python3
import argparse, json

REQUIRED_INVARIANTS = {
    "TOKEN_VAZIO != 0",
    "filename/title != identity",
    "index != authority",
    "absence_of_evidence != evidence_of_absence",
    "VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM",
}
ALLOWED_POLICIES = {"NON_BLOCKING", "CLOSED", "BLOCKING_RUNTIME", "POST_RUN_BLOCKING_FOR_CLAIM"}

def load_json(path):
    with open(path, "r", encoding="utf-8") as f: return json.load(f)

def load_jsonl(path):
    out=[]
    with open(path, "r", encoding="utf-8") as f:
        for n,line in enumerate(f,1):
            line=line.strip()
            if not line: continue
            try: out.append(json.loads(line))
            except json.JSONDecodeError as e: raise ValueError(f"{path}:{n}: invalid JSONL: {e}") from e
    return out

def validate(registry, supersession, gaps, ci_policy=None):
    errors=[]
    if registry.get("schema") != "RAFAELIA_PROFILE_OS_REGISTRY_V1": errors.append("bad schema")
    if registry.get("mode") != "APPEND_ONLY": errors.append("mode must be APPEND_ONLY")
    if registry.get("delete_policy") != "NO_DELETE": errors.append("delete_policy must be NO_DELETE")
    if registry.get("claim_allowed") is not False: errors.append("claim_allowed must be false")
    if registry.get("identity_contract",{}).get("same_title_is_identity") is not False: errors.append("same title must never be identity")
    folder_ids=[x.get("provider_id") for x in registry.get("folders",[])]
    if len(folder_ids) != len(set(folder_ids)): errors.append("duplicate folder provider_id")
    if len(folder_ids) != 8: errors.append(f"expected exactly 8 level-1 folders, got {len(folder_ids)}")
    object_ids=[x.get("provider_id") for x in registry.get("objects",[])]
    if len(object_ids) != len(set(object_ids)): errors.append("duplicate object provider_id")
    for obj in registry.get("objects",[]):
        if obj.get("claim_allowed") is not False: errors.append(f"object {obj.get('provider_id')} claim_allowed must be false")
    missing=REQUIRED_INVARIANTS-set(registry.get("invariants",[]))
    if missing: errors.append("missing invariants: "+", ".join(sorted(missing)))
    for rel in supersession:
        src=rel.get("source",{}).get("provider_id"); dst=rel.get("target",{}).get("provider_id")
        if rel.get("type") != "SUPERSEDED_BY": errors.append("unsupported supersession relation type")
        if not src or not dst or src == dst: errors.append("invalid supersession endpoints")
        if rel.get("delete_candidate") is not False: errors.append("supersession delete_candidate must be false")
        if rel.get("claim_allowed") is not False: errors.append("supersession claim_allowed must be false")
    gap_ids=[]
    for gap in gaps:
        gid=gap.get("id"); gap_ids.append(gid)
        if gap.get("claim_allowed") is not False: errors.append(f"gap {gid} claim_allowed must be false")
        if not gid or not gap.get("state"): errors.append("gap missing id/state")
        if gap.get("state") == 0: errors.append(f"gap {gid} cannot encode TOKEN_VAZIO as zero")
        if gap.get("gate_policy") not in ALLOWED_POLICIES: errors.append(f"gap {gid} missing/invalid gate_policy")
        if gap.get("gate_policy") in {"BLOCKING_RUNTIME","POST_RUN_BLOCKING_FOR_CLAIM"} and not gap.get("resolution_path"):
            errors.append(f"gap {gid} blocking policy requires resolution_path")
    if len(gap_ids) != len(set(gap_ids)): errors.append("duplicate gap id")
    if ci_policy is not None:
        if ci_policy.get("schema") != "RAFAELIA_PROFILE_OS_CI_POLICY_V1": errors.append("bad CI policy schema")
        if ci_policy.get("mode") != "APPEND_ONLY" or ci_policy.get("delete_policy") != "NO_DELETE": errors.append("CI policy governance drift")
        if ci_policy.get("claim_allowed") is not False: errors.append("CI policy claim_allowed must be false")
        pids={x.get("id") for x in ci_policy.get("runtime_tokens",[])}
        gids=set(gap_ids)
        for pid in pids:
            if pid not in gids: errors.append(f"CI runtime token not declared in gap ledger: {pid}")
        comp=ci_policy.get("composition",[])
        if not comp or len(comp)!=len(set(comp)): errors.append("CI composition empty or duplicated")
    return errors

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--registry", required=True); ap.add_argument("--supersession", required=True); ap.add_argument("--gaps", required=True); ap.add_argument("--ci-policy"); args=ap.parse_args()
    registry=load_json(args.registry); supersession=load_jsonl(args.supersession); gaps=load_jsonl(args.gaps); policy=load_json(args.ci_policy) if args.ci_policy else None
    errors=validate(registry, supersession, gaps, policy)
    if errors:
        for e in errors: print("FAIL:",e)
        return 1
    print("PASS: PROFILE_OS registry invariants")
    print(f"folders={len(registry.get('folders', []))}")
    print(f"objects={len(registry.get('objects', []))}")
    print(f"supersession_relations={len(supersession)}")
    print(f"gaps={len(gaps)}")
    print("claim_allowed=false")
    return 0

if __name__ == "__main__": raise SystemExit(main())
