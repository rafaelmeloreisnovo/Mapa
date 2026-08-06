#!/usr/bin/env python3
"""Validate RAFAELIA cognitive operators 15-70 (stdlib only)."""
from __future__ import annotations
import argparse, hashlib, json, sys
from collections import Counter
from pathlib import Path

MANIFEST_SCHEMA = "rafaelia.cognitive-operator-registry/v1"
SEGMENT_SCHEMA = "rafaelia.cognitive-operator-segment/v1"
FORMAL = {
    "VALID","VALID_WITH_ASSUMPTIONS","VALID_WITH_CONVENTION","MISNAMED",
    "MISCLASSIFIED","INCOMPLETE","CONVENTION_DEPENDENT",
    "INVALID_AS_GENERAL_DEFINITION","INVALID_AS_STATED","FORMAL_HEURISTIC",
    "DIMENSIONALLY_INCOMPLETE",
}
UNSAFE = {
    "INCOMPLETE","CONVENTION_DEPENDENT","INVALID_AS_GENERAL_DEFINITION",
    "INVALID_AS_STATED","FORMAL_HEURISTIC","DIMENSIONALLY_INCOMPLETE",
}
REQUIRED = {
    "id","n","name","kind","formal","execution","claim_allowed","formula",
    "boundary","falsifier","physical_bridge","route",
}
INVARIANTS = {
    "operator_name != mathematical_definition",
    "analogy != mechanism",
    "formal_expression != executable_model",
    "TOKEN_VAZIO != 0",
    "IMPLEMENTABLE != PASS",
    "physical_label != physical_evidence",
}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_registry(manifest_path: Path):
    manifest = read_json(manifest_path)
    repo_root = manifest_path.resolve().parents[2]
    operators, segment_errors = [], []
    for item in manifest.get("segments", []):
        path = repo_root / item.get("path", "")
        try:
            segment = read_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            segment_errors.append(f"cannot read segment {path}: {exc}")
            continue
        if segment.get("schema") != SEGMENT_SCHEMA:
            segment_errors.append(f"{path}: invalid segment schema")
        if segment.get("range") != item.get("range"):
            segment_errors.append(f"{path}: range differs from manifest")
        if segment.get("count") != item.get("count"):
            segment_errors.append(f"{path}: count differs from manifest")
        entries = segment.get("operators", [])
        if not isinstance(entries, list) or len(entries) != item.get("count"):
            segment_errors.append(f"{path}: operator count mismatch")
            continue
        operators.extend(entries)
    return manifest, operators, segment_errors


def validate(manifest, operators, segment_errors=None):
    errors = list(segment_errors or [])
    if manifest.get("schema") != MANIFEST_SCHEMA:
        errors.append("invalid manifest schema")
    meta = manifest.get("metadata", {})
    if meta.get("claim_allowed") is not False:
        errors.append("metadata.claim_allowed must be false")
    if meta.get("source_range") != [15, 70]:
        errors.append("metadata.source_range must be [15,70]")
    if meta.get("operator_count") != 56:
        errors.append("metadata.operator_count must be 56")
    if not INVARIANTS.issubset(set(meta.get("invariants", []))):
        errors.append("mandatory invariants are missing")
    if sum(x.get("count", 0) for x in manifest.get("segments", [])) != 56:
        errors.append("manifest segment counts must sum to 56")
    if len(operators) != 56:
        errors.append(f"registry must contain 56 operators, got {len(operators)}")

    ids, numbers, kinds = [], [], []
    for i, op in enumerate(operators):
        prefix = f"operator[{i}]"
        if not isinstance(op, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = REQUIRED - set(op)
        if missing:
            errors.append(f"{prefix} missing {sorted(missing)}")
            continue
        n, oid = op["n"], op["id"]
        ids.append(oid); numbers.append(n); kinds.append(op["kind"])
        if oid != f"COG-{n:03d}":
            errors.append(f"{oid}: id does not match ordinal")
        if op["formal"] not in FORMAL:
            errors.append(f"{oid}: unknown formal state")
        if op["execution"] not in {"IMPLEMENTABLE","TOKEN_VAZIO"}:
            errors.append(f"{oid}: unknown execution state")
        if op["claim_allowed"] is not False:
            errors.append(f"{oid}: claim_allowed must be false")
        for key in ("name","kind","formula","boundary","falsifier"):
            if not isinstance(op[key], str) or not op[key].strip():
                errors.append(f"{oid}: {key} must be non-empty")
        if op["formal"] in UNSAFE and op["execution"] != "TOKEN_VAZIO":
            errors.append(f"{oid}: {op['formal']} cannot be IMPLEMENTABLE")
        if op["execution"] == "IMPLEMENTABLE":
            if op["route"] != "RafPolimata":
                errors.append(f"{oid}: IMPLEMENTABLE must route to RafPolimata")
        else:
            if op["route"] != "Mapa":
                errors.append(f"{oid}: TOKEN_VAZIO must route to Mapa")
            if not str(op.get("gap", "")).strip():
                errors.append(f"{oid}: TOKEN_VAZIO requires gap")
            if not str(op.get("next_gate", "")).strip():
                errors.append(f"{oid}: TOKEN_VAZIO requires next_gate")
        if op["physical_bridge"] and op["execution"] != "TOKEN_VAZIO":
            errors.append(f"{oid}: physical bridge cannot be IMPLEMENTABLE")

    if numbers != list(range(15, 71)):
        errors.append("ordinals must be contiguous and ordered from 15 to 70")
    if len(ids) != len(set(ids)):
        errors.append("operator ids must be unique")
    if len(kinds) != len(set(kinds)):
        errors.append("normalized kinds must be unique")
    return sorted(set(errors))


def build_report(manifest, operators, segment_errors=None):
    errors = validate(manifest, operators, segment_errors)
    execution = Counter(x.get("execution") for x in operators)
    formal = Counter(x.get("formal") for x in operators)
    return {
        "schema":"rafaelia.cognitive-operator-audit/v1",
        "valid":not errors,
        "errors":errors,
        "registry_sha256":hashlib.sha256(canonical({"manifest":manifest,"operators":operators}).encode()).hexdigest(),
        "summary":{
            "operators":len(operators),
            "implementable":execution.get("IMPLEMENTABLE",0),
            "token_vazio":execution.get("TOKEN_VAZIO",0),
            "physical_bridges":sum(bool(x.get("physical_bridge")) for x in operators),
            "formal":dict(sorted(formal.items())),
            "claim_allowed":False,
        },
        "routing":{
            "Mapa":"canonical classification, boundaries and TOKEN_VAZIO",
            "RafPolimata":"bounded implementations and reproducible tests",
            "papers":"reviewed synthesis after evidence gates",
        },
    }


def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--manifest",default="data/ontology/cognitive-operators.v1.json")
    parser.add_argument("--output")
    args=parser.parse_args(argv)
    try:
        manifest, operators, segment_errors = load_registry(Path(args.manifest))
    except (OSError,json.JSONDecodeError) as exc:
        print(exc,file=sys.stderr); return 2
    report=build_report(manifest,operators,segment_errors)
    if args.output:
        out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(report["summary"],ensure_ascii=False,sort_keys=True))
    for error in report["errors"]: print(error,file=sys.stderr)
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
