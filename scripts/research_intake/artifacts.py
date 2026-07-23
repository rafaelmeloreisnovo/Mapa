from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from .core import PUBLIC_STATES, allocate_record_ids, canonical_json, load_id_registry


def synthesis(records: list[dict[str, Any]], config: dict[str, Any], generated_at: str) -> dict[str, Any]:
    states = Counter(record["state"] for record in records)
    domains = Counter(record["domain"] for record in records if record["domain"] != "TOKEN_VAZIO")
    reviewed = sum(1 for record in records if record.get("review"))
    milestone = (len(records) // config["volume_step"]) * config["volume_step"]
    return {
        "schema": "mapa.research-intake-synthesis/v1", "generated_at": generated_at,
        "record_count": len(records), "volume_milestone": milestone,
        "next_volume_milestone": milestone + config["volume_step"], "reviewed_count": reviewed,
        "domain_count": len(domains), "state_counts": dict(sorted(states.items())),
        "domain_counts": dict(sorted(domains.items())),
        "structure_trigger_met": reviewed >= config["minimum_reviewed"] and len(domains) >= config["minimum_domains"],
        "trigger_policy": "HEURISTIC_TRIGGER_NOT_PROMOTION", "claim_allowed": False,
        "warning": "volume and structure generate a synthesis artifact; they do not prove any scientific claim",
    }


def public_export(records: list[dict[str, Any]], generated_at: str) -> dict[str, Any]:
    exported = []
    for record in records:
        review = record.get("review") or {}
        if record["state"] not in PUBLIC_STATES or not review.get("public_export_allowed"):
            continue
        exported.append({
            "record_id": record["record_id"], "canonical_key": record["canonical_key"],
            "title": record["title"], "year": record["year"], "authors": record["authors"],
            "domain": record["domain"],
            "persistent_ids": {key: record[key] for key in ("doi", "arxiv_id", "pmid") if record.get(key)},
            "source_count": record["metadata_source_count"], "state": record["state"],
            "reviewed_at": review["reviewed_at"], "scope": review["scope"],
            "falsifier": review["falsifier"], "evidence_basis": review["evidence_basis"],
            "claim_allowed": False,
        })
    return {
        "schema": "rll.public-literature-navigation/v1", "generated_at": generated_at,
        "source_authority": "rafaelmeloreisnovo/Mapa (private)", "automatic_push": False,
        "records": exported, "claim_allowed": False,
        "boundary": "navigation metadata only; no private notes, raw queries, abstracts, credentials or unreviewed records",
    }


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.write_text("".join(canonical_json(record) + "\n" for record in records), encoding="utf-8")


def emit_artifacts(records: list[dict[str, Any]], config: dict[str, Any], outdir: Path,
                   generated_at: str, id_registry: dict[str, Any] | None = None) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    buckets = {
        "02_UNREVIEWED.jsonl": "UNREVIEWED", "04_HYPOTHESIS_CANDIDATES.jsonl": "HYPOTHESIS_CANDIDATE",
        "05_UNLIKELY_CURRENT_EVIDENCE.jsonl": "UNLIKELY_UNDER_CURRENT_EVIDENCE",
        "06_CONFLICTED.jsonl": "CONFLICTED", "07_REVIEWED_EVIDENCE.jsonl": "REVIEWED_EVIDENCE",
        "08_TOKEN_VAZIO.jsonl": "TOKEN_VAZIO",
    }
    write_jsonl(outdir / "01_RAW_NORMALIZED.jsonl", records)
    for filename, state in buckets.items():
        write_jsonl(outdir / filename, (record for record in records if record["state"] == state))
    (outdir / "03_EVOLVING_SYNTHESIS.json").write_text(
        json.dumps(synthesis(records, config, generated_at), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (outdir / "09_RLL_PUBLIC_EXPORT.json").write_text(
        json.dumps(public_export(records, generated_at), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    registry = id_registry or load_id_registry(None, config["prefix"], config["width"])
    proposal = allocate_record_ids(records, registry, config["prefix"], config["width"])
    proposal.update(generated_at=generated_at, status="PROPOSAL_REQUIRES_REVIEW_BEFORE_CANONICAL_UPDATE")
    (outdir / "10_ID_REGISTRY_PROPOSAL.json").write_text(
        json.dumps(proposal, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = {
        "schema": "mapa.research-intake-manifest/v1", "generated_at": generated_at,
        "config_schema": config["schema"], "source_count": len(config["sources"]),
        "record_count": len(records), "claim_allowed": False,
        "files": sorted(path.name for path in outdir.iterdir() if path.is_file()),
    }
    (outdir / "00_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    checksums = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}"
                 for path in sorted(outdir.iterdir()) if path.is_file() and path.name != "CHECKSUMS.sha256"]
    (outdir / "CHECKSUMS.sha256").write_text("\n".join(checksums) + "\n", encoding="utf-8")
