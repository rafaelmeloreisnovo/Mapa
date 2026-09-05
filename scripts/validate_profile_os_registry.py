#!/usr/bin/env python3
import argparse, json

REQUIRED_INVARIANTS = {
    "TOKEN_VAZIO != 0",
    "filename/title != identity",
    "index != authority",
    "absence_of_evidence != evidence_of_absence",
    "VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM",
}

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_jsonl(path):
    out=[]
    with open(path, "r", encoding="utf-8") as f:
        for n,line in enumerate(f,1):
            line=line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"{path}:{n}: invalid JSONL: {e}") from e
    return out

def validate(registry, supersession, gaps):
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
    for gap in gaps:
        if gap.get("claim_allowed") is not False: errors.append(f"gap {gap.get('id')} claim_allowed must be false")
        if not gap.get("id") or not gap.get("state"): errors.append("gap missing id/state")
        if gap.get("state") == 0: errors.append(f"gap {gap.get('id')} cannot encode TOKEN_VAZIO as zero")
    return errors

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--registry", required=True); ap.add_argument("--supersession", required=True); ap.add_argument("--gaps", required=True); args=ap.parse_args()
    registry=load_json(args.registry); supersession=load_jsonl(args.supersession); gaps=load_jsonl(args.gaps)
    errors=validate(registry, supersession, gaps)
    if errors:
        for e in errors: print("FAIL:",e)
        return 1
    print("PASS: PROFILE_OS registry invariants")
    print(f"folders={len(registry.get('folders', []))}")
    print(f"objects={len(registry.get('objects', []))}")
    print(f"supersession_relations={len(supersession)}")
    print("claim_allowed=false")
    return 0

if __name__ == "__main__": raise SystemExit(main())
