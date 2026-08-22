#!/usr/bin/env python3
"""Fail-closed validator for MULTIMODAL_CAVE_SEED_V1.

The validator proves only structural coherence, bounded source metadata,
privacy/claim guards, exact rational anchors and the exhaustive scalar
10-bit -> (8-bit, 2-bit residual) roundtrip. It does not validate scientific,
identity, copyright, manifold, audio or video claims.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


SCHEMA = "rafaelia.multimodal_cave_seed.v1"
SEED_ID = "MULTIMODAL_CAVE_SEED_V1"
EXPECTED_SCHEMA_FILES = (
    "multimodal-cave-seed.v1.schema.json",
    "multimodal-object.v1.schema.json",
    "multimodal-representation.v1.schema.json",
    "multimodal-transform.v1.schema.json",
    "route-preface.v1.schema.json",
    "semantic-tile.v1.schema.json",
)
MIME_BY_EXTENSION = {
    ".gif": "image/gif",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".png": "image/png",
    ".raw": "application/octet-stream",
}


class ValidationError(ValueError):
    """Raised when an invariant fails closed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _strict_int(value: Any, name: str, minimum: int, maximum: int) -> int:
    require(type(value) is int, f"{name} must be an integer, not {type(value).__name__}")
    require(minimum <= value <= maximum, f"{name} outside {minimum}..{maximum}: {value}")
    return value


def encode_10_to_8_plus_residual(x10: int) -> tuple[int, int]:
    x10 = _strict_int(x10, "x10", 0, 1023)
    return x10 >> 2, x10 & 0b11


def decode_8_plus_residual(q8: int, r2: int) -> int:
    q8 = _strict_int(q8, "q8", 0, 255)
    r2 = _strict_int(r2, "r2", 0, 3)
    return (q8 << 2) | r2


def exhaustive_roundtrip() -> int:
    for x10 in range(1024):
        q8, r2 = encode_10_to_8_plus_residual(x10)
        require(decode_8_plus_residual(q8, r2) == x10, f"roundtrip failed at {x10}")
    return 1024


def _ids(items: Iterable[dict[str, Any]], key: str, namespace: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for item in items:
        ident = item.get(key)
        require(isinstance(ident, str) and ident, f"missing {namespace} identifier {key}")
        require(ident not in out, f"duplicate {namespace} id: {ident}")
        out[ident] = item
    return out


def _walk_claim_guards(value: Any, path: str = "$") -> int:
    count = 0
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key == "claim_allowed":
                require(child is False, f"claim promotion blocked at {child_path}")
                count += 1
            count += _walk_claim_guards(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            count += _walk_claim_guards(child, f"{path}[{index}]")
    return count


def _contains_bounds(parent: dict[str, float], child: dict[str, float]) -> bool:
    epsilon = 1e-12
    return (
        child["x"] + epsilon >= parent["x"]
        and child["y"] + epsilon >= parent["y"]
        and child["x"] + child["width"] <= parent["x"] + parent["width"] + epsilon
        and child["y"] + child["height"] <= parent["y"] + parent["height"] + epsilon
    )


def _assert_acyclic(nodes: Iterable[str], edges: Iterable[tuple[str, str]], label: str) -> None:
    graph: dict[str, list[str]] = {node: [] for node in nodes}
    for source, target in edges:
        if source in graph and target in graph:
            graph[source].append(target)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        require(node not in visiting, f"cycle detected in {label} at {node}")
        if node in visited:
            return
        visiting.add(node)
        for target in graph[node]:
            visit(target)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)


def _matrix_product(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    return [
        [sum(left[row][k] * right[k][col] for k in range(3)) for col in range(3)]
        for row in range(3)
    ]


def _validate_schemas(repo_root: Path) -> int:
    schema_dir = repo_root / "schemas"
    ids: set[str] = set()
    for filename in EXPECTED_SCHEMA_FILES:
        path = schema_dir / filename
        require(path.is_file(), f"missing schema file: {path}")
        payload = load_json(path)
        require(payload.get("$schema") == "https://json-schema.org/draft/2020-12/schema", f"wrong draft: {filename}")
        schema_id = payload.get("$id")
        require(isinstance(schema_id, str) and schema_id, f"missing $id: {filename}")
        require(schema_id not in ids, f"duplicate schema $id: {schema_id}")
        ids.add(schema_id)
    root = load_json(schema_dir / EXPECTED_SCHEMA_FILES[0])
    refs = {
        item["items"]["$ref"]
        for item in root.get("properties", {}).values()
        if isinstance(item, dict) and isinstance(item.get("items"), dict) and "$ref" in item["items"]
    }
    for ref in refs:
        require((schema_dir / ref).is_file(), f"dangling local schema ref: {ref}")
    return len(EXPECTED_SCHEMA_FILES)


def _validate_sources(
    objects: dict[str, dict[str, Any]], representations: dict[str, dict[str, Any]]
) -> tuple[int, int]:
    require(len(objects) == 10, f"expected ten source objects, got {len(objects)}")
    sha_seen: set[str] = set()
    provider_seen: set[str] = set()
    roles: set[str] = set()
    mismatch_count = 0
    alias_objects: set[str] = set()
    for object_id, obj in objects.items():
        source = obj["source"]
        sha = source["sha256"]
        provider_id = source["provider_id"]
        require(len(sha) == 64 and all(ch in "0123456789abcdef" for ch in sha), f"bad SHA-256: {object_id}")
        require(sha not in sha_seen, f"duplicate source bytes inside seed: {sha}")
        require(provider_id not in provider_seen, f"duplicate provider id: {provider_id}")
        require(obj["role"] not in roles, f"duplicate role: {obj['role']}")
        sha_seen.add(sha)
        provider_seen.add(provider_id)
        roles.add(obj["role"])
        require(source["bytes_in_repository"] is False, f"source bytes copied into repository: {object_id}")
        require(source["detected_mime"] == "image/jpeg", f"unexpected detected media: {object_id}")
        suffix = Path(source["observed_filename"]).suffix.lower()
        require(suffix == source["declared_extension"].lower(), f"extension record mismatch: {object_id}")
        expected_match = MIME_BY_EXTENSION.get(suffix) == source["detected_mime"]
        require(source["extension_mime_match"] is expected_match, f"extension/MIME truth mismatch: {object_id}")
        mismatch_count += int(not expected_match)
        require(len(obj["representation_ids"]) == 1, f"seed v1 requires one source representation: {object_id}")
        rep_id = obj["representation_ids"][0]
        require(rep_id in representations, f"dangling representation: {object_id} -> {rep_id}")
        rep = representations[rep_id]
        require(rep["object_id"] == object_id, f"representation owner mismatch: {rep_id}")
        require(rep["source_locator"]["sha256"] == sha, f"representation SHA mismatch: {rep_id}")
        require(rep["source_locator"]["provider_id"] == provider_id, f"representation provider mismatch: {rep_id}")
        for source_key, media_key in (("pixel_width", "width"), ("pixel_height", "height"), ("bit_depth", "bit_depth"), ("color_space", "color_space")):
            require(source[source_key] == rep["media"][media_key], f"media metadata mismatch: {rep_id}:{media_key}")
        if source["existing_aliases"]:
            alias_objects.add(object_id)
            for alias in source["existing_aliases"]:
                require(alias["match_basis"] == "EXACT_SHA256_AND_BYTE_COUNT", f"weak alias basis: {object_id}")
    require(mismatch_count == 9, f"expected nine extension/MIME mismatches, got {mismatch_count}")
    require(alias_objects == {"MMO-08", "MMO-09"}, f"unexpected exact aliases: {sorted(alias_objects)}")
    return len(objects), mismatch_count


def _validate_tiles(
    objects: dict[str, dict[str, Any]], tiles: dict[str, dict[str, Any]]
) -> tuple[int, int]:
    actual_children: dict[str, set[str]] = defaultdict(set)
    roots = 0
    for tile_id, tile in tiles.items():
        object_id = tile["object_id"]
        require(object_id in objects, f"tile has unknown object: {tile_id}")
        bounds = tile["bounds_normalized"]
        require(bounds["x"] + bounds["width"] <= 1 + 1e-12, f"tile exceeds frame x: {tile_id}")
        require(bounds["y"] + bounds["height"] <= 1 + 1e-12, f"tile exceeds frame y: {tile_id}")
        parent_id = tile["parent_tile_id"]
        if parent_id is None:
            roots += 1
            require(tile["depth"] == 0, f"root tile depth must be zero: {tile_id}")
            require(bounds == {"x": 0, "y": 0, "width": 1, "height": 1}, f"root must cover frame: {tile_id}")
            require(objects[object_id]["root_tile_id"] == tile_id, f"object root mismatch: {object_id}")
        else:
            require(parent_id in tiles, f"dangling tile parent: {tile_id} -> {parent_id}")
            parent = tiles[parent_id]
            require(parent["object_id"] == object_id, f"cross-object containment: {tile_id}")
            require(tile["depth"] == parent["depth"] + 1, f"bad tile depth: {tile_id}")
            require(_contains_bounds(parent["bounds_normalized"], bounds), f"child outside parent: {tile_id}")
            actual_children[parent_id].add(tile_id)
        expected_privacy = objects[object_id]["privacy"]["classification"]
        require(tile["privacy"] == expected_privacy, f"tile privacy drift: {tile_id}")
        for interpretation in tile["interpretations"]:
            if interpretation["layer"] == "SCIENTIFIC":
                require(interpretation["state"] == "TOKEN_VAZIO", f"scientific interpretation promoted: {tile_id}")
    for tile_id, tile in tiles.items():
        require(set(tile["child_tile_ids"]) == actual_children[tile_id], f"child index mismatch: {tile_id}")
    containment_edges = [(tile["parent_tile_id"], tile_id) for tile_id, tile in tiles.items() if tile["parent_tile_id"]]
    _assert_acyclic(tiles, containment_edges, "tile containment")
    require(roots == len(objects), f"expected one root per object, got {roots}")
    return len(tiles), roots


def _validate_prefaces(prefaces: dict[str, dict[str, Any]], resolvable: set[str]) -> int:
    roots = []
    edges: list[tuple[str, str]] = []
    for preface_id, preface in prefaces.items():
        parent_id = preface["parent_preface_id"]
        if parent_id is None:
            roots.append(preface_id)
            require(preface["depth"] == 0, f"preface root depth: {preface_id}")
        else:
            require(parent_id in prefaces, f"dangling preface parent: {preface_id} -> {parent_id}")
            require(preface["depth"] == prefaces[parent_id]["depth"] + 1, f"preface depth mismatch: {preface_id}")
            edges.append((parent_id, preface_id))
        require(preface["depth"] <= 2, f"seed v1 preface depth exceeded: {preface_id}")
        for field in ("target_ids", "route", "source_ids"):
            for target in preface[field]:
                require(target in resolvable, f"dangling preface {field}: {preface_id} -> {target}")
    require(roots == ["PREFACE-ROOT"], f"unexpected preface roots: {roots}")
    _assert_acyclic(prefaces, edges, "route prefaces")
    return len(prefaces)


def _validate_math(anchors: dict[str, dict[str, Any]]) -> None:
    radical = anchors["ANCHOR-SQRT-3-OVER-2-IN-RADICAL"]
    quotient = anchors["ANCHOR-SQRT3-OVER-2"]
    require(radical["normalized_ast"] != quotient["normalized_ast"], "distinct square-root ASTs collapsed")
    require(math.isclose(radical["approximate_value"], math.sqrt(3 / 2), rel_tol=0, abs_tol=1e-15), "radical value mismatch")
    require(math.isclose(quotient["approximate_value"], math.sqrt(3) / 2, rel_tol=0, abs_tol=1e-15), "quotient value mismatch")
    require(not math.isclose(radical["approximate_value"], quotient["approximate_value"], rel_tol=0, abs_tol=1e-12), "distinct formula values collapsed")
    matrix = anchors["ANCHOR-MATRIX-M"]["matrix_A"]
    require(_matrix_product(matrix, matrix) == [[9, 0, 0], [0, 9, 0], [0, 0, 9]], "A^2 != 9I")


def validate_seed(seed: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    require(seed.get("schema") == SCHEMA, "wrong seed schema")
    require(seed.get("seed_id") == SEED_ID, "wrong seed id")
    require(seed.get("state") == "VERIFIED_LIMITED", "seed state must remain bounded")
    require(seed.get("claim_allowed") is False, "global claim promotion blocked")
    datetime.fromisoformat(seed["generated_at"])
    claim_guards = _walk_claim_guards(seed)
    require(claim_guards >= 80, f"unexpectedly sparse claim guards: {claim_guards}")

    concepts = _ids(seed["concepts"], "concept_id", "concept")
    objects = _ids(seed["objects"], "object_id", "object")
    representations = _ids(seed["representations"], "representation_id", "representation")
    transforms = _ids(seed["transforms"], "transform_id", "transform")
    tiles = _ids(seed["tiles"], "tile_id", "tile")
    prefaces = _ids(seed["route_prefaces"], "preface_id", "preface")
    anchors = _ids(seed["mathematical_anchors"], "anchor_id", "anchor")
    gaps = _ids(seed["gaps"], "gap_id", "gap")
    relations = _ids(seed["relations"], "relation_id", "relation")

    all_ids = [
        seed["seed_id"],
        seed["bit_codec_contract"]["contract_id"],
        *concepts,
        *objects,
        *representations,
        *transforms,
        *tiles,
        *prefaces,
        *anchors,
        *gaps,
    ]
    require(len(all_ids) == len(set(all_ids)), "identifier collision across namespaces")
    resolvable = set(all_ids)

    object_count, mismatch_count = _validate_sources(objects, representations)
    tile_count, root_count = _validate_tiles(objects, tiles)
    for transform_id, transform in transforms.items():
        for rep_id in [*transform["input_representation_ids"], *transform["output_representation_ids"]]:
            require(rep_id in representations, f"dangling transform representation: {transform_id} -> {rep_id}")
        if transform["state"] == "VERIFIED_LIMITED":
            require(transform["evidence"]["result"] == "PASS", f"verified transform lacks PASS: {transform_id}")
        if transform["state"] == "TOKEN_VAZIO_EXECUTION":
            require(transform["evidence"]["result"] != "PASS", f"unexecuted transform promoted: {transform_id}")

    dependency_edges: list[tuple[str, str]] = []
    for relation_id, relation in relations.items():
        require(relation["source_id"] in resolvable, f"dangling relation source: {relation_id}")
        require(relation["target_id"] in resolvable, f"dangling relation target: {relation_id}")
        require(0 <= relation["confidence"] <= 1, f"relation confidence outside range: {relation_id}")
        if relation["graph_class"] in {"DEPENDENCY", "PROVENANCE"}:
            dependency_edges.append((relation["source_id"], relation["target_id"]))
    _assert_acyclic(resolvable, dependency_edges, "dependency/provenance graph")

    preface_count = _validate_prefaces(prefaces, resolvable)
    _validate_math(anchors)
    for gap_id, gap in gaps.items():
        require(gap["state"] == "TOKEN_VAZIO", f"gap promoted without closure: {gap_id}")
        require(gap["falsifier"] and gap["next_gate"], f"gap lacks falsifier/next gate: {gap_id}")

    portrait = objects["MMO-10"]
    require(portrait["privacy"]["classification"] == "SENSITIVE_PERSONAL_IMAGE", "portrait sensitivity missing")
    require(portrait["privacy"]["identity_inference_allowed"] is False, "identity inference enabled")
    require(portrait["privacy"]["segmentation_export_allowed"] is False, "portrait crop export enabled")
    require(seed["bit_codec_contract"]["parity_only_reversible"] is False, "parity-only overclaim")
    codec_vectors = exhaustive_roundtrip()
    schema_count = _validate_schemas(repo_root)

    return {
        "status": "PASS",
        "schema": SCHEMA,
        "objects": object_count,
        "representations": len(representations),
        "tiles": tile_count,
        "root_tiles": root_count,
        "relations": len(relations),
        "prefaces": preface_count,
        "transforms": len(transforms),
        "gaps": len(gaps),
        "schemas": schema_count,
        "claim_guards": claim_guards,
        "extension_mime_mismatches": mismatch_count,
        "codec_vectors": codec_vectors,
        "claim_allowed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--seed",
        default="data/multimodal/MULTIMODAL_CAVE_SEED_20260822.v1.json",
    )
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    seed_path = (repo_root / args.seed).resolve()
    try:
        seed = load_json(seed_path)
        result = validate_seed(seed, repo_root)
        result["seed_sha256"] = sha256_file(seed_path)
        result["seed_path"] = str(seed_path.relative_to(repo_root))
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
