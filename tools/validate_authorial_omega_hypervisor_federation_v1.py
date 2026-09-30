#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data" / "manifold" / "authorial_omega_hypervisor_federation_v1.json"

class ValidationError(ValueError):
    pass

def req(cond, msg):
    if not cond:
        raise ValidationError(msg)

def load(path=DEFAULT):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def validate(obj):
    req(obj.get("schema") == "rafaelia.authorial-omega-hypervisor-federation.v1", "schema")
    req(obj.get("claim_allowed") is False, "claim_allowed must remain false")
    inv=set(obj.get("invariants",[]))
    for x in (
        "SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM",
        "TOKEN_VAZIO != 0",
        "IMPLEMENTED_UNTESTED != PASS",
        "REPOSITORY_OWNERSHIP != WHOLE_REPOSITORY_AUTHORSHIP",
        "STRUCTURAL_MODEL_REFERENCE != CODE_INHERITANCE",
    ):
        req(x in inv, f"missing invariant: {x}")

    expected_states=["C01_INTENT","C02_AUTHORSHIP","C03_GAPS","C04_MOUNT","C05_EXECUTE","C06_VERIFY","C07_CUSTODY","C08_OMEGA"]
    states=obj["cycle"]["states"]
    req([x["id"] for x in states] == expected_states, "cycle order")
    req(states[-1].get("next") == "C01_INTENT", "C08 reentry")
    req("unresolved_gap_register" in states[-1].get("requires",[]), "C08 gap register")

    mounts={m["id"]:m for m in obj.get("mounts",[])}
    req(len(mounts)==len(obj.get("mounts",[])), "duplicate mount")
    for m in mounts.values():
        for k in ("kind","authority","ref","authorship_state","mode","raw_payload_publication"):
            req(k in m, f"{m['id']} missing {k}")
        req(m["raw_payload_publication"] is False, f"{m['id']} public raw payload forbidden")
        if m["kind"]=="EXTERNAL_PROVIDER_SURFACE":
            req("READ_ONLY" in m["mode"] or "PROVIDER_ACTIONS" in m["mode"], f"{m['id']} provider default boundary")

    models={m["id"]:m for m in obj.get("model_references",[])}
    req(models["VECTRA_STRUCTURAL_MODEL"]["code_import"] is False, "Vectra inherited code import forbidden")
    req(models["VECTRA_STRUCTURAL_MODEL"]["whole_repo_authorial"] is False, "Vectra whole repo authorial forbidden")
    req(models["PCR_CUSTODY_CYCLE_MODEL"]["code_import"] is False, "PCR code import forbidden")
    req(models["PCR_CUSTODY_CYCLE_MODEL"]["whole_repo_authorial"] is False, "PCR whole repo authorial forbidden")

    assets={a["artifact_id"]:a for a in obj.get("proven_authorial_assets",[])}
    bl0=assets.get("RAF_BL0_V0")
    req(bl0 is not None, "RAF_BL0_V0")
    req(bl0["classification"]=="AUTHORIAL_PROVEN", "RAF_BL0 classification")
    blobs={x["blob"] for x in bl0["proof"]["byte_identical_mirrors"]}
    req(blobs=={"132f948d199f6679fcae4f33912e0a3ad69691a3"}, "RAF_BL0 mirror identity")
    req(bl0["proof"]["vectra_introduction"]["change"]=="ADD_87_LINES_FROM_ZERO", "Vectra introduction")
    req(bl0["proof"]["termux_introduction"]["change"]=="ADD_87_LINES_FROM_ZERO", "Termux introduction")

    gap_ids=[g["id"] for g in obj.get("gaps",[])]
    req(len(gap_ids)==len(set(gap_ids)), "duplicate gaps")
    req(set(obj.get("F_gap",[]))==set(gap_ids), "F_gap must index all current gaps")
    req(bool(obj.get("F_next")), "F_next")
    return True

def main():
    obj=load()
    validate(obj)
    print("PASS authorial_omega_hypervisor_federation_v1")
    print(f"mounts={len(obj['mounts'])} relations={len(obj['relations'])} gaps={len(obj['gaps'])} authorial_assets={len(obj['proven_authorial_assets'])}")

if __name__ == "__main__":
    main()
