#!/usr/bin/env python3
"""Validate the five P0 internal gap-closure artifacts without external deps."""
from __future__ import annotations

import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
GEOM = ROOT / "data/geometry/piramide_triedrica_dupla_candidates.v1.json"
NUM = ROOT / "data/numerics/numeric_policy.v1.json"
PROV = ROOT / "data/provenance/poincare_formula_provenance.v1.json"
CORPUS = ROOT / "data/corpus/corpus_manifest_p0.v1.json"
XSR = ROOT / "data/reconciliation/cross_surface_reconciliation_p0.v1.jsonl"


class ValidationError(ValueError):
    pass


def load_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: pathlib.Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def edge_key(edge):
    if len(edge) != 2:
        raise ValidationError(f"invalid edge {edge}")
    return tuple(sorted(edge))


def face_edges(face):
    if len(face) != 3:
        raise ValidationError(f"non-triangular face {face}")
    return {edge_key((face[0], face[1])), edge_key((face[1], face[2])), edge_key((face[2], face[0]))}


def validate_geometry(doc):
    if doc.get("claim_allowed") is not False:
        raise ValidationError("geometry must remain claim_allowed=false")
    fixtures = {f["id"]: f for f in doc["fixtures"]}
    if set(fixtures) != {"G1", "G2", "G3"}:
        raise ValidationError("expected G1/G2/G3 fixtures")
    if doc.get("canonical_test_fixture_is_authorial_selection") is not False:
        raise ValidationError("test fixture must not be promoted to authorial selection")

    g1 = fixtures["G1"]
    v, e, f = len(g1["vertices"]), len(g1["edges"]), len(g1["oriented_faces"])
    if (v, e, f) != (5, 9, 6) or v - e + f != 2:
        raise ValidationError("G1 V/E/F or Euler invariant mismatch")
    edge_set = {edge_key(x) for x in g1["edges"]}
    used = set().union(*(face_edges(face) for face in g1["oriented_faces"]))
    if edge_set != used:
        raise ValidationError("G1 edge/face incidence mismatch")
    if set(g1["central_junction"]["vertices"]) != {"A", "B", "C"}:
        raise ValidationError("G1 central junction mismatch")

    g2 = fixtures["G2"]
    if (len(g2["vertices"]), len(g2["edges"]), len(g2["oriented_faces"])) != (7, 12, 8):
        raise ValidationError("G2 V/E/F mismatch")
    if g2["central_junction"] != {"type": "SHARED_VERTEX", "vertices": ["O"]}:
        raise ValidationError("G2 central point mismatch")

    g3 = fixtures["G3"]
    if not g3["state"].startswith("TOKEN_VAZIO_TYPED"):
        raise ValidationError("G3 uncertainty must remain typed")
    if any(k in g3 for k in ("vertices", "edges", "oriented_faces")):
        raise ValidationError("G3 must not invent V/E/F before source evidence")

    neg = doc["negative_fixture"]
    neg_edges = {edge_key(x) for x in neg["edges"]}
    neg_used = set().union(*(face_edges(face) for face in neg["oriented_faces"]))
    if not (neg_edges - neg_used):
        raise ValidationError("negative fixture must contain a dangling edge")


def validate_numeric(doc):
    if doc.get("claim_allowed") is not False:
        raise ValidationError("numeric policy cannot promote claims")
    policies = {p["policy_id"]: p for p in doc["policies"]}
    required = {"NUM-EXACT-COMBINATORIAL-V1", "NUM-FLOAT64-GEOMETRY-V1", "NUM-FLOAT32-ARM-V1", "NUM-FIXED-Q16-V1"}
    if set(policies) != required:
        raise ValidationError("numeric policy set mismatch")
    if policies["NUM-EXACT-COMBINATORIAL-V1"]["abs_epsilon"] != 0:
        raise ValidationError("exact combinatorics must use epsilon zero")
    for pid in ("NUM-FLOAT64-GEOMETRY-V1", "NUM-FLOAT32-ARM-V1"):
        p = policies[pid]
        if not (p["abs_epsilon"] > 0 and p["rel_epsilon"] > 0):
            raise ValidationError(f"{pid} tolerances must be positive")
        if "FAIL_CLOSED" not in p["overflow"]:
            raise ValidationError(f"{pid} overflow must fail closed")


def validate_provenance(doc):
    if doc.get("claim_allowed") is not False:
        raise ValidationError("provenance cannot promote claim")
    raw = doc["raw_blocks"]
    expected = [f"RAW-LIVRO-VIVO-20260716-{i:03d}" for i in range(1, 65)]
    if raw != expected:
        raise ValidationError("raw block IDs are not a complete stable 001..064 sequence")
    if doc["raw_source"]["raw_math_block_count"] != 64:
        raise ValidationError("raw block count mismatch")
    manifest = doc["formula_artifact_manifest"]
    if manifest["formulas_json_materialized_in_repo_or_release"] is not False:
        raise ValidationError("do not claim formulas.json materialized")
    mapping = doc["mapping_state"]
    if not mapping["FORM_id"].startswith("TOKEN_VAZIO_TYPED"):
        raise ValidationError("FORM join must remain typed until exact bytes exist")
    if doc["semantic_boundary"]["rule"] != "embedding != return_map != conjecture":
        raise ValidationError("Poincare semantic separation lost")


def validate_corpus(doc):
    if doc.get("claim_allowed") is not False or doc.get("global_drive_complete_claim") is not False:
        raise ValidationError("corpus scope must not become a global Drive completeness claim")
    audit = doc["omega7_audit"]
    if audit["files_observed"] != 62822 or audit["files_with_hash"] != 62821:
        raise ValidationError("Omega7 audit counts changed unexpectedly")
    expected_ratio = audit["files_with_hash"] / audit["files_observed"]
    if not math.isclose(audit["hash_coverage_ratio"], expected_ratio, rel_tol=0, abs_tol=1e-15):
        raise ValidationError("hash coverage ratio mismatch")
    if doc["residual_classification"]["missing_hash_count_in_omega7_audit"] != 1:
        raise ValidationError("single hash residual must be explicit")
    for src in doc["canonical_p0_sources"]:
        if not (src.get("provider_id") or (src.get("repository") and src.get("path"))):
            raise ValidationError(f"anonymous P0 source {src.get('id')}")
        if not src.get("privacy") or not src.get("license") or not src.get("derived_from"):
            raise ValidationError(f"incomplete authority fields for {src.get('id')}")


def validate_reconciliation(records):
    if len(records) != 5:
        raise ValidationError("expected five reconciliation anchors")
    ids = set()
    for r in records:
        if r.get("schema") != "rafaelia.cross-surface-reconciliation.v1":
            raise ValidationError("bad reconciliation schema")
        if r["record_id"] in ids:
            raise ValidationError("duplicate reconciliation record")
        ids.add(r["record_id"])
        if r.get("claim_allowed") is not False:
            raise ValidationError("reconciliation cannot promote scientific claim")
        drive = r.get("drive", {})
        github = r.get("github", {})
        if not drive.get("id"):
            raise ValidationError(f"missing Drive provider id in {r['record_id']}")
        if not github.get("repository") or not github.get("path"):
            raise ValidationError(f"missing GitHub locator in {r['record_id']}")
        for key in ("state", "F_next"):
            if not r.get(key):
                raise ValidationError(f"missing {key} in {r['record_id']}")


def main() -> int:
    try:
        validate_geometry(load_json(GEOM))
        validate_numeric(load_json(NUM))
        validate_provenance(load_json(PROV))
        validate_corpus(load_json(CORPUS))
        validate_reconciliation(load_jsonl(XSR))
    except (OSError, KeyError, TypeError, ValueError, ValidationError) as exc:
        print(f"P0_INTERNAL_GAP_CLOSURE_FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({
        "schema": "rafaelia.p0-internal-gap-closure-validation.v1",
        "state": "PASS",
        "validated_gaps": ["cross_surface_reconciliation", "poincare_provenance", "geometry_VEF", "numeric_policy", "corpus_scope"],
        "claim_allowed": False,
        "external_residuals_preserved": True
    }, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
