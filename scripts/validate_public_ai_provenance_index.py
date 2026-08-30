#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

REGISTRY = Path("data/control-plane/PUBLIC_AI_PROVENANCE_INDEX_V1_20260829.json")
MANIFEST = Path("fixtures/private_chunk_hash_index_manifest.sample.v1.json")
INDICES = [
    "IDX-IDENTITY", "IDX-CONTENT-COMMITMENT", "IDX-TEMPORAL",
    "IDX-PROVIDER-PROVENANCE", "IDX-MODALITY-SIGNATURE", "IDX-RELATION",
    "IDX-EVIDENCE-WEIGHT", "IDX-PRIVACY-BOUNDARY", "IDX-SUPERSESSION",
    "IDX-CLAIM-GATE",
]
GUARDS = {
    "TEXT_STYLE_TO_PROVIDER_PROOF", "IMAGE_RESOLUTION_TO_PROVIDER_PROOF",
    "NO_SIGNAL_TO_NON_ORIGIN_PROOF", "HASH_TO_AUTHORSHIP_PROOF",
    "HASH_TO_SEMANTIC_EQUIVALENCE", "SEMANTIC_SIMILARITY_TO_IDENTITY",
}
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def load(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def check_registry(d):
    e = []
    req = lambda ok, msg: None if ok else e.append(msg)
    req(d.get("schema") == "rafaelia.public_ai_provenance_index.v1", "registry schema")
    req(d.get("claim_allowed") is False, "registry claim must be false")
    req(d.get("public_ci_only") is True, "CI must be public-only")
    req(d.get("private_content_access") == "FORBIDDEN", "private content forbidden")
    req(d.get("index_invariant") == "INDICES_ARE_MULTIPLE_ORTHOGONAL_VIEWS_NOT_ONE_SCORE", "plural index invariant")
    bridge = d.get("private_bridge", {})
    req(bridge.get("mode") == "HASH_COMMITMENTS_ONLY", "hash-only bridge")
    req(bridge.get("raw_private_forbidden_in_public_ci") is True, "raw private CI boundary")
    ids = [x.get("id") for x in d.get("invariant_indices", [])]
    req(ids == INDICES, "10 canonical indices")
    req(GUARDS <= set(d.get("forbidden_promotions", [])), "attribution guards")
    obs = {x.get("id") for x in d.get("public_observations", [])}
    for needed in (
        "OBS-OPENAI-IMAGE-PROVENANCE-2026", "OBS-OPENAI-VERIFY-2026",
        "OBS-OPENAI-TEXT-BOUNDARY-2026", "OBS-PROVENANCE-LOSS-BOUNDARY-2026",
    ):
        req(needed in obs, f"missing {needed}")
    req(d.get("cross_ai_extension", {}).get("unknown_provider_state") == "TOKEN_VAZIO_PUBLIC_PROVENANCE_ADAPTER", "unknown provider fail-closed")
    req(d.get("dynamic_weighting", {}).get("gate") == "ATTRIBUTION_STRENGTH_LE_EVIDENCE_CLASS_CEILING", "weights cannot upgrade evidence")
    return e


def check_manifest(d):
    e = []
    req = lambda ok, msg: None if ok else e.append(msg)
    req(d.get("schema") == "rafaelia.private_chunk_hash_index_manifest.v1", "manifest schema")
    req(d.get("public_safe") is True, "manifest public_safe")
    req(d.get("raw_content_included") is False, "raw content prohibited")
    req(d.get("claim_allowed") is False, "manifest claim must be false")
    req(d.get("index_invariants") == INDICES, "manifest index invariant order")
    chunks = d.get("chunks", [])
    req(d.get("leaf_count") == len(chunks), "leaf_count")
    commitments = []
    ids = []
    for i, c in enumerate(chunks):
        req(c.get("ordinal") == i, f"ordinal {i}")
        req(str(c.get("opaque_id", "")).startswith("CHUNK-"), f"opaque id {i}")
        h = c.get("commitment", "")
        req(bool(HEX64.fullmatch(h)), f"commitment {i}")
        commitments.append(h)
        ids.append(c.get("opaque_id"))
    req(len(set(ids)) == len(ids), "opaque IDs unique")
    req(len(set(commitments)) == len(commitments), "commitments unique")
    if commitments and all(HEX64.fullmatch(x) for x in commitments):
        root = hashlib.sha256("\n".join(commitments).encode("ascii")).hexdigest()
        req(d.get("public_navigation_root_sha256") == root, "navigation root")
    return e


def main():
    try:
        errors = check_registry(load(REGISTRY)) + check_manifest(load(MANIFEST))
    except Exception as exc:
        print(f"FAIL load: {exc}", file=sys.stderr)
        return 2
    if errors:
        print("FAIL public AI provenance invariant")
        for item in errors:
            print(" -", item)
        return 1
    print("PASS public AI provenance invariant")
    print(" - public CI reads no private content")
    print(" - 10 orthogonal indices preserved")
    print(" - heuristic signatures cannot become provider proof")
    print(" - hash-only navigation root verified")
    print(" - claim_allowed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
