#!/usr/bin/env python3
"""Enrich four canonical Gap Atlas fields from explicit structured source evidence.

Target fields:
- artifact_id
- provider
- scope
- evidence_required

This tool is evidence-only. It never mutates the Atlas, never allocates gap IDs,
and never treats an alias or a structured derivation as canonical equivalence.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

SCHEMA = "rafaelia.systematic-pragmatic-identity-semantics-enrichment/v1"
TARGET_FIELDS = ("artifact_id", "provider", "scope", "evidence_required")
STATES = {
    "EXACT_STRUCTURED",
    "NORMALIZED_ENUM_CANDIDATE",
    "ALIAS_CANDIDATE",
    "STRUCTURED_DERIVATION_CANDIDATE",
    "CONFLICT",
    "TOKEN_VAZIO",
}
PROVIDERS = {
    "GitHub",
    "Google Drive",
    "Android/Termux",
    "External Scientific Source",
    "Human Review",
    "Cross-Provider",
}
PROVIDER_NORMALIZATION = {
    "github": "GitHub",
    "github.com": "GitHub",
    "google drive": "Google Drive",
    "gdrive": "Google Drive",
    "drive": "Google Drive",
    "android": "Android/Termux",
    "termux": "Android/Termux",
    "android/termux": "Android/Termux",
    "external scientific source": "External Scientific Source",
    "human review": "Human Review",
    "cross-provider": "Cross-Provider",
    "cross_provider": "Cross-Provider",
}
ALIASES = {
    "artifact_id": (
        "artifact",
        "artifact_name",
        "artifact_path",
        "artifact_digest",
        "archive_digest",
        "receipt_id",
        "receipt",
        "target_path",
        "source_artifact",
        "output_artifact",
    ),
    "provider": (
        "source_provider",
        "provider_name",
    ),
    "scope": (
        "audit_scope",
        "review_scope",
        "source_scope",
        "bounded_scope",
    ),
    "evidence_required": (
        "evidence_needed",
        "required_evidence",
        "proof_required",
        "evidence_gate",
    ),
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected object")
    return value


def walk(value: Any, prefix: str = "") -> Iterable[tuple[str, str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            key_s = str(key)
            path = f"{prefix}.{key_s}" if prefix else key_s
            yield path, key_s, child
            yield from walk(child, path)
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            path = f"{prefix}[{idx}]"
            yield from walk(child, path)


def nonempty(value: Any) -> bool:
    return value not in (None, "", [], {})


def normalize_string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            if isinstance(item, str) and item.strip():
                out.append(item.strip())
            elif isinstance(item, dict):
                for key in ("criterion", "evidence_needed", "value", "description"):
                    child = item.get(key)
                    if isinstance(child, str) and child.strip():
                        out.append(child.strip())
        return out
    if isinstance(value, dict):
        out: list[str] = []
        for child in value.values():
            out.extend(normalize_string_list(child))
        return out
    return []


def normalize_provider(value: Any) -> tuple[str | None, str]:
    if not isinstance(value, str) or not value.strip():
        return None, "INVALID"
    raw = value.strip()
    if raw in PROVIDERS:
        return raw, "EXACT"
    mapped = PROVIDER_NORMALIZATION.get(raw.lower())
    if mapped:
        return mapped, "NORMALIZED"
    return None, "UNMAPPED"


def canonical_key(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def looks_like_repository(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    text = value.strip()
    if not text or " " in text or text.startswith(("http://", "https://")):
        return False
    parts = text.split("/")
    return len(parts) == 2 and all(parts)


def flatten_strings(value: Any) -> list[str]:
    out: list[str] = []
    if isinstance(value, str) and value.strip():
        out.append(value.strip())
    elif isinstance(value, list):
        for child in value:
            out.extend(flatten_strings(child))
    elif isinstance(value, dict):
        for key, child in value.items():
            vals = flatten_strings(child)
            if vals:
                out.extend(f"{key}:{v}" for v in vals)
            elif child not in (None, "", [], {}):
                out.append(f"{key}:{child}")
    return out


def collect_field(
    field: str,
    records: list[tuple[str, dict[str, Any]]],
) -> dict[str, Any]:
    exact: list[dict[str, Any]] = []
    normalized: list[dict[str, Any]] = []
    aliases: list[dict[str, Any]] = []
    derived: list[dict[str, Any]] = []

    for source_path, obj in records:
        for object_path, key, value in walk(obj):
            if not nonempty(value):
                continue

            if key == field:
                if field == "provider":
                    provider, mode = normalize_provider(value)
                    if provider is not None:
                        item = {
                            "source_path": source_path,
                            "object_path": object_path,
                            "source_key": key,
                            "raw_value": value,
                            "value": provider,
                        }
                        if mode == "EXACT":
                            item["relation"] = "EXACT_PROVIDER_ENUM"
                            exact.append(item)
                        else:
                            item["relation"] = "NORMALIZED_PROVIDER_ENUM"
                            normalized.append(item)
                    else:
                        aliases.append(
                            {
                                "source_path": source_path,
                                "object_path": object_path,
                                "source_key": key,
                                "raw_value": value,
                                "value": value,
                                "relation": "PROVIDER_VALUE_NOT_IN_CANONICAL_ENUM",
                            }
                        )
                elif field == "evidence_required":
                    vals = normalize_string_list(value)
                    if vals:
                        exact.append(
                            {
                                "source_path": source_path,
                                "object_path": object_path,
                                "source_key": key,
                                "raw_value": value,
                                "value": vals,
                                "relation": "EXACT_FIELD_NAME_STRUCTURED",
                            }
                        )
                elif isinstance(value, str) and value.strip():
                    exact.append(
                        {
                            "source_path": source_path,
                            "object_path": object_path,
                            "source_key": key,
                            "raw_value": value,
                            "value": value.strip(),
                            "relation": "EXACT_FIELD_NAME_STRUCTURED",
                        }
                    )

            if key in ALIASES.get(field, ()):
                if field == "provider":
                    provider, mode = normalize_provider(value)
                    if provider is not None:
                        normalized.append(
                            {
                                "source_path": source_path,
                                "object_path": object_path,
                                "source_key": key,
                                "raw_value": value,
                                "value": provider,
                                "relation": (
                                    "ALIAS_NORMALIZED_PROVIDER_ENUM"
                                    if mode == "NORMALIZED"
                                    else "ALIAS_PROVIDER_ENUM"
                                ),
                            }
                        )
                elif field == "evidence_required":
                    vals = normalize_string_list(value)
                    if vals:
                        aliases.append(
                            {
                                "source_path": source_path,
                                "object_path": object_path,
                                "source_key": key,
                                "raw_value": value,
                                "value": vals,
                                "relation": "EVIDENCE_ALIAS_NOT_EQUIVALENCE",
                            }
                        )
                else:
                    vals = normalize_string_list(value)
                    if vals:
                        aliases.append(
                            {
                                "source_path": source_path,
                                "object_path": object_path,
                                "source_key": key,
                                "raw_value": value,
                                "value": vals[0] if len(vals) == 1 else vals,
                                "relation": "ALIAS_NOT_EQUIVALENCE",
                            }
                        )

            if (
                field == "provider"
                and key in {"owner", "repository", "repository_full_name", "repo"}
                and looks_like_repository(value)
            ):
                derived.append(
                    {
                        "source_path": source_path,
                        "object_path": object_path,
                        "source_key": key,
                        "raw_value": value,
                        "value": "GitHub",
                        "relation": "REPOSITORY_IDENTITY_IMPLIES_GITHUB_PROVIDER_CANDIDATE",
                    }
                )

            if field == "scope" and key in {
                "affected_routes",
                "affected_components",
                "impact_radius",
                "affected_scope",
                "components",
                "targets",
            }:
                vals = flatten_strings(value)
                if vals:
                    derived.append(
                        {
                            "source_path": source_path,
                            "object_path": object_path,
                            "source_key": key,
                            "raw_value": value,
                            "value": vals,
                            "relation": "STRUCTURED_AFFECTED_SURFACE_CANDIDATE",
                        }
                    )

    def reduce_items(
        items: list[dict[str, Any]],
        state: str,
    ) -> dict[str, Any] | None:
        if not items:
            return None

        if field == "evidence_required":
            combined: list[str] = []
            seen: set[str] = set()
            for item in items:
                for value in normalize_string_list(item["value"]):
                    if value not in seen:
                        seen.add(value)
                        combined.append(value)
            if combined:
                return {
                    "state": state,
                    "value": combined,
                    "evidence": items,
                    "combination": "UNION_OF_COMPLEMENTARY_REQUIREMENTS",
                    "governed_review_required": True,
                }

        if field == "scope" and state == "STRUCTURED_DERIVATION_CANDIDATE":
            combined: list[str] = []
            seen: set[str] = set()
            for item in items:
                for value in flatten_strings(item["value"]):
                    if value not in seen:
                        seen.add(value)
                        combined.append(value)
            if combined:
                return {
                    "state": state,
                    "value": combined,
                    "evidence": items,
                    "combination": "BOUNDED_AFFECTED_SURFACE",
                    "governed_review_required": True,
                }

        unique: dict[str, Any] = {}
        for item in items:
            unique[canonical_key(item["value"])] = item["value"]
        if len(unique) == 1:
            return {
                "state": state,
                "value": next(iter(unique.values())),
                "evidence": items,
                "governed_review_required": True,
            }
        return {
            "state": "CONFLICT",
            "value": "TOKEN_VAZIO",
            "candidate_values": list(unique.values()),
            "evidence": items,
            "governed_review_required": True,
        }

    for items, state in (
        (exact, "EXACT_STRUCTURED"),
        (normalized, "NORMALIZED_ENUM_CANDIDATE"),
        (aliases, "ALIAS_CANDIDATE"),
        (derived, "STRUCTURED_DERIVATION_CANDIDATE"),
    ):
        reduced = reduce_items(items, state)
        if reduced is not None:
            return reduced

    return {
        "state": "TOKEN_VAZIO",
        "value": "TOKEN_VAZIO",
        "evidence": [],
        "governed_review_required": True,
    }


def load_records(repo_root: Path, paths: list[str]) -> list[tuple[str, dict[str, Any]]]:
    out: list[tuple[str, dict[str, Any]]] = []
    for rel in paths:
        obj = json.loads((repo_root / rel).read_text(encoding="utf-8"))
        if not isinstance(obj, dict):
            raise ValueError(f"{rel}: expected source object")
        out.append((rel, obj))
    return out


def build(
    completion: dict[str, Any],
    repo_root: Path,
) -> dict[str, Any]:
    if completion.get("schema") != "rafaelia.systematic-pragmatic-canonical-completion/v1":
        raise ValueError("unsupported canonical completion schema")
    if completion.get("claim_allowed") is not False:
        raise ValueError("canonical completion claim boundary is open")
    if completion.get("atlas_mutation_allowed") is not False:
        raise ValueError("canonical completion permits Atlas mutation")

    rows: list[dict[str, Any]] = []
    counts = {
        field: {state: 0 for state in sorted(STATES)}
        for field in TARGET_FIELDS
    }

    for row in completion.get("completions", []):
        if not isinstance(row, dict):
            raise ValueError("completion row must be object")
        source_gap_id = row.get("source_gap_id")
        source_paths = [
            str(value)
            for value in row.get("source_paths", [])
            if isinstance(value, str) and value
        ]
        if not isinstance(source_gap_id, str) or not source_gap_id or not source_paths:
            raise ValueError("completion row missing source identity/path")
        records = load_records(repo_root, source_paths)
        fields = {field: collect_field(field, records) for field in TARGET_FIELDS}
        for field, item in fields.items():
            counts[field][item["state"]] += 1

        rows.append(
            {
                "enrichment_id": "G4E-" + source_gap_id,
                "completion_id": row.get("completion_id"),
                "source_gap_id": source_gap_id,
                "source_paths": source_paths,
                "target_fields": fields,
                "proposed_atlas_gap_id": "TOKEN_VAZIO",
                "g4": {
                    "state": "IDENTITY_SEMANTICS_REVIEW_REQUIRED",
                    "atlas_mutation_allowed": False,
                    "auto_create_gap_id": False,
                    "governed_review_required": True,
                },
                "claim_allowed": False,
            }
        )

    return {
        "schema": SCHEMA,
        "claim_allowed": False,
        "atlas_mutation_allowed": False,
        "policy": {
            "same_key_structured_evidence_is_not_auto_promotion": True,
            "provider_normalization_is_candidate_not_binding": True,
            "structured_derivation_is_candidate_not_binding": True,
            "alias_is_not_equivalence": True,
            "artifact_identity_requires_explicit_source_evidence": True,
            "auto_create_gap_id": False,
        },
        "summary": {
            "records": len(rows),
            "field_state_counts": counts,
        },
        "enrichments": sorted(rows, key=lambda row: row["source_gap_id"]),
    }


def validate(payload: dict[str, Any]) -> None:
    if payload.get("claim_allowed") is not False:
        raise ValueError("claim boundary opened")
    if payload.get("atlas_mutation_allowed") is not False:
        raise ValueError("Atlas mutation enabled")
    rows = payload.get("enrichments", [])
    if payload.get("summary", {}).get("records") != len(rows):
        raise ValueError("row count mismatch")
    for row in rows:
        if row.get("proposed_atlas_gap_id") != "TOKEN_VAZIO":
            raise ValueError(f"{row.get('source_gap_id')}: premature Atlas id")
        if row.get("claim_allowed") is not False:
            raise ValueError(f"{row.get('source_gap_id')}: claim boundary opened")
        g4 = row.get("g4", {})
        if g4.get("atlas_mutation_allowed") is not False:
            raise ValueError(f"{row.get('source_gap_id')}: Atlas mutation enabled")
        if g4.get("auto_create_gap_id") is not False:
            raise ValueError(f"{row.get('source_gap_id')}: automatic gap id enabled")
        fields = row.get("target_fields", {})
        if set(fields) != set(TARGET_FIELDS):
            raise ValueError(f"{row.get('source_gap_id')}: target field set mismatch")
        for field, item in fields.items():
            if item.get("state") not in STATES:
                raise ValueError(f"{row.get('source_gap_id')}:{field}: invalid state")
            if (
                item.get("state") in {"TOKEN_VAZIO", "CONFLICT"}
                and item.get("value") != "TOKEN_VAZIO"
            ):
                raise ValueError(
                    f"{row.get('source_gap_id')}:{field}: unsupported value promoted"
                )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--completion", type=Path, required=True)
    ap.add_argument("--repo-root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    try:
        payload = build(load_json(args.completion), args.repo_root)
        validate(payload)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"identity-semantics-enrichment: {exc}")
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload["summary"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
