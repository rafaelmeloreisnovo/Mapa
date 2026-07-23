from __future__ import annotations

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

VALID_STATES = {
    "UNREVIEWED", "HYPOTHESIS_CANDIDATE", "UNLIKELY_UNDER_CURRENT_EVIDENCE",
    "CONFLICTED", "REVIEWED_EVIDENCE", "TOKEN_VAZIO",
}
PUBLIC_STATES = {"REVIEWED_EVIDENCE"}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_text(text: str) -> str:
    return " ".join(str(text or "").split())


def title_fingerprint(title: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", " ", normalize_text(title).casefold()).strip()
    return sha256_text(normalized)[:24]


def canonical_key(record: dict[str, Any]) -> str:
    doi = normalize_text(record.get("doi", "")).lower()
    if doi:
        return f"doi:{doi}"
    arxiv_id = normalize_text(record.get("arxiv_id", "")).lower()
    if arxiv_id:
        return f"arxiv:{arxiv_id}"
    pmid = normalize_text(record.get("pmid", ""))
    if pmid:
        return f"pmid:{pmid}"
    source_id = normalize_text(record.get("source_record_id", ""))
    title = normalize_text(record.get("title", ""))
    if title:
        return f"title:{title_fingerprint(title)}"
    if source_id:
        return f"source:{normalize_text(record.get('source', 'unknown'))}:{source_id}"
    return f"token-vazio:{sha256_text(canonical_json(record))[:24]}"


def load_config(path: Path) -> dict[str, Any]:
    root = ET.parse(path).getroot()
    if root.attrib.get("schema") != "mapa.research-intake/v1":
        raise ValueError("unexpected config schema")
    if root.attrib.get("claimAllowed", "true").lower() != "false":
        raise ValueError("claimAllowed must be false")
    boundary = root.find("boundary")
    if boundary is None:
        raise ValueError("boundary missing")

    def bool_text(name: str) -> bool:
        node = boundary.find(name)
        if node is None:
            raise ValueError(f"boundary.{name} missing")
        return (node.text or "").strip().lower() == "true"

    if not bool_text("rawMetadataPrivate"):
        raise ValueError("raw metadata must remain private")
    if bool_text("automaticPublicPush") or bool_text("automaticClaimPromotion") or bool_text("unknownIsZero"):
        raise ValueError("unsafe boundary configuration")
    seq, trigger, sources = root.find("sequence"), root.find("synthesisTrigger"), root.find("sources")
    if seq is None or trigger is None or sources is None:
        raise ValueError("sequence, synthesisTrigger and sources are required")
    return {
        "schema": root.attrib["schema"], "version": root.attrib["version"],
        "prefix": seq.attrib["prefix"], "width": int(seq.attrib["width"]),
        "volume_step": int(trigger.attrib["volumeStep"]),
        "minimum_reviewed": int(trigger.attrib["minimumReviewed"]),
        "minimum_domains": int(trigger.attrib["minimumDomains"]),
        "sources": [dict(source.attrib) for source in sources.findall("source")],
        "claim_allowed": False,
    }


def load_json_records(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("fixture root must be a list")
    return [dict(item) for item in data]


def load_review_ledger(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None or not path.exists():
        return {}
    reviews: dict[str, dict[str, Any]] = {}
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        item = json.loads(line)
        key, state = normalize_text(item.get("canonical_key", "")), item.get("state")
        if not key or state not in VALID_STATES - {"UNREVIEWED", "TOKEN_VAZIO"}:
            raise ValueError(f"invalid review ledger line {line_no}")
        required = ("reviewed_by", "reviewed_at", "reason", "scope", "falsifier", "evidence_basis")
        missing = [field for field in required if not normalize_text(item.get(field, ""))]
        if missing:
            raise ValueError(f"review provenance missing at line {line_no}: {missing}")
        if item.get("public_export_allowed") not in {True, False}:
            raise ValueError(f"public_export_allowed must be boolean at line {line_no}")
        reviews[key] = item
    return reviews


def load_id_registry(path: Path | None, prefix: str, width: int) -> dict[str, Any]:
    if path is None or not path.exists():
        return {"schema": "mapa.research-intake-id-registry/v1", "prefix": prefix,
                "width": width, "next_sequence": 1, "assignments": {}, "claim_allowed": False}
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "mapa.research-intake-id-registry/v1":
        raise ValueError("unexpected id registry schema")
    if data.get("prefix") != prefix or data.get("width") != width:
        raise ValueError("id registry prefix/width mismatch")
    if data.get("claim_allowed") is not False or not isinstance(data.get("assignments"), dict):
        raise ValueError("invalid id registry boundary")
    ids = list(data["assignments"].values())
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate record id in registry")
    pattern = re.compile(rf"^{re.escape(prefix)}-[0-9]{{{width}}}$")
    if any(not pattern.fullmatch(str(value)) for value in ids):
        raise ValueError("invalid record id format")
    expected_next = max((int(value.rsplit("-", 1)[1]) for value in ids), default=0) + 1
    if data.get("next_sequence") != expected_next:
        raise ValueError("id registry next_sequence mismatch")
    return data


def allocate_record_ids(records: list[dict[str, Any]], registry: dict[str, Any], prefix: str, width: int) -> dict[str, Any]:
    assignments, next_sequence = dict(registry.get("assignments", {})), int(registry.get("next_sequence", 1))
    for key in sorted(record["canonical_key"] for record in records):
        if key not in assignments:
            assignments[key] = f"{prefix}-{next_sequence:0{width}d}"
            next_sequence += 1
    return {"schema": "mapa.research-intake-id-registry/v1", "prefix": prefix, "width": width,
            "next_sequence": next_sequence, "assignments": dict(sorted(assignments.items())), "claim_allowed": False}


def normalize_record(raw: dict[str, Any]) -> dict[str, Any]:
    record = {
        "source": normalize_text(raw.get("source", "unknown")),
        "source_record_id": normalize_text(raw.get("source_record_id", "")),
        "title": normalize_text(raw.get("title", "")), "year": raw.get("year"),
        "authors": [normalize_text(v) for v in raw.get("authors", []) if normalize_text(v)],
        "doi": normalize_text(raw.get("doi", "")).lower(),
        "arxiv_id": normalize_text(raw.get("arxiv_id", "")).lower(),
        "pmid": normalize_text(raw.get("pmid", "")),
        "domain": normalize_text(raw.get("domain", "TOKEN_VAZIO")) or "TOKEN_VAZIO",
        "url": normalize_text(raw.get("url", "")),
    }
    record["canonical_key"] = canonical_key(record)
    fields = [record["title"], record["authors"], record["year"], record["url"],
              record["doi"] or record["arxiv_id"] or record["pmid"] or record["source_record_id"]]
    record["metadata_completeness"] = sum(bool(value) for value in fields) / len(fields)
    record["payload_sha256"] = sha256_text(canonical_json(record))
    return record


def deduplicate(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for raw in records:
        normalized = normalize_record(raw)
        groups[normalized["canonical_key"]].append(normalized)
    output = []
    for key in sorted(groups):
        versions = sorted(groups[key], key=lambda item: (item["source"], item["source_record_id"]))
        best = max(versions, key=lambda item: (item["metadata_completeness"], len(item["title"])))
        sources = sorted({item["source"] for item in versions})
        merged = dict(best)
        merged.update({
            "metadata_sources": sources, "metadata_source_count": len(sources),
            "source_records": [{"source": item["source"], "source_record_id": item["source_record_id"],
                                "payload_sha256": item["payload_sha256"]} for item in versions],
            "metadata_corroboration_only": len(sources) > 1,
        })
        output.append(merged)
    return output


def assign_states(records: list[dict[str, Any]], reviews: dict[str, dict[str, Any]], prefix: str,
                  width: int, id_registry: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    proposal = allocate_record_ids(records, id_registry or load_id_registry(None, prefix, width), prefix, width)
    assigned = []
    for record in sorted(records, key=lambda item: item["canonical_key"]):
        item = dict(record)
        item["record_id"] = proposal["assignments"][item["canonical_key"]]
        if not item["title"] or item["metadata_completeness"] < 0.4:
            item.update(state="TOKEN_VAZIO", state_reason="metadata insufficient; absence was not converted to zero", review=None)
        elif item["canonical_key"] in reviews:
            review = reviews[item["canonical_key"]]
            item.update(state=review["state"], state_reason=normalize_text(review["reason"]), review={
                "reviewed_by": review["reviewed_by"], "reviewed_at": review["reviewed_at"],
                "scope": normalize_text(review["scope"]), "falsifier": normalize_text(review["falsifier"]),
                "evidence_basis": normalize_text(review["evidence_basis"]),
                "public_export_allowed": review["public_export_allowed"],
            })
        else:
            item.update(state="UNREVIEWED", state_reason="normalized metadata awaiting explicit human review", review=None)
        item["claim_allowed"] = False
        assigned.append(item)
    return assigned
