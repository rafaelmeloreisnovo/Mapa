#!/usr/bin/env python3
"""Extract append-only anteriority events from ChatGPT NOVOexport conversation shards.

Evidence boundary:
- first textual occurrence != first invention
- internal occurrence != public disclosure
- public disclosure != legal priority
- claim_allowed is always false in generated records

No third-party dependencies are required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Tuple


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def iter_conversations(payload: Any) -> Iterator[Dict[str, Any]]:
    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict):
                yield item
        return
    if isinstance(payload, dict):
        if isinstance(payload.get("conversations"), list):
            for item in payload["conversations"]:
                if isinstance(item, dict):
                    yield item
            return
        # Some exports/shards may contain a single conversation object.
        if "mapping" in payload:
            yield payload


def extract_message_text(message: Dict[str, Any]) -> str:
    content = message.get("content") or {}
    parts = content.get("parts") or []
    out: List[str] = []
    for part in parts:
        if isinstance(part, str):
            out.append(part)
        elif isinstance(part, dict):
            # Preserve structured textual values without inventing semantics.
            text = part.get("text")
            if isinstance(text, str):
                out.append(text)
    return "\n".join(out)


def iter_user_messages(conv: Dict[str, Any]) -> Iterator[Tuple[Dict[str, Any], Dict[str, Any]]]:
    mapping = conv.get("mapping") or {}
    if not isinstance(mapping, dict):
        return
    for node in mapping.values():
        if not isinstance(node, dict):
            continue
        message = node.get("message")
        if not isinstance(message, dict):
            continue
        author = message.get("author") or {}
        if author.get("role") != "user":
            continue
        yield node, message


def iso_utc(value: Any) -> str | None:
    try:
        ts = float(value)
    except (TypeError, ValueError):
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def compile_queries(config: Dict[str, Any]) -> List[Tuple[Dict[str, Any], List[Tuple[str, re.Pattern[str]]]]]:
    compiled = []
    for family in config.get("families", []):
        aliases = []
        for alias in family.get("aliases", []):
            aliases.append((alias, re.compile(re.escape(alias), re.IGNORECASE)))
        compiled.append((family, aliases))
    return compiled


def scan_shard(path: Path, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    payload = load_json(path)
    source_sha = sha256_file(path)
    queries = compile_queries(config)
    events: List[Dict[str, Any]] = []

    for conv in iter_conversations(payload):
        conversation_id = conv.get("id") or conv.get("conversation_id")
        title = conv.get("title")
        for _node, message in iter_user_messages(conv):
            text = extract_message_text(message)
            if not text:
                continue
            text_sha = sha256_bytes(text.encode("utf-8"))
            matched_families = []
            for family, aliases in queries:
                matched = [alias for alias, rx in aliases if rx.search(text)]
                if matched:
                    matched_families.append((family, matched))

            for family, matched in matched_families:
                events.append({
                    "schema": "rafaelia.novoexport.anteriority-event/v1",
                    "family_id": family["family_id"],
                    "canonical_name": family["canonical_name"],
                    "matched_aliases": sorted(set(matched), key=str.casefold),
                    "source_path": str(path),
                    "source_file_sha256": source_sha,
                    "conversation_id": conversation_id,
                    "conversation_title": title,
                    "message_id": message.get("id"),
                    "created_time": message.get("create_time"),
                    "created_at_utc": iso_utc(message.get("create_time")),
                    "text_sha256": text_sha,
                    "evidence_class": "E2_CONTENT_FINGERPRINTED",
                    "internal_documented": True,
                    "public_disclosure": "TOKEN_VAZIO",
                    "legal_priority": "TOKEN_VAZIO",
                    "scientific_novelty": "TOKEN_VAZIO",
                    "claim_allowed": False,
                })
    return events


def event_sort_key(event: Dict[str, Any]) -> Tuple[float, str, str]:
    try:
        t = float(event.get("created_time"))
    except (TypeError, ValueError):
        t = float("inf")
    return (t, str(event.get("source_path") or ""), str(event.get("message_id") or ""))


def build_summary(events: Iterable[Dict[str, Any]], config: Dict[str, Any]) -> Dict[str, Any]:
    event_list = sorted(events, key=event_sort_key)
    by_family: Dict[str, List[Dict[str, Any]]] = {}
    for event in event_list:
        by_family.setdefault(event["family_id"], []).append(event)

    families = []
    for family in config.get("families", []):
        rows = by_family.get(family["family_id"], [])
        first = rows[0] if rows else None
        families.append({
            "family_id": family["family_id"],
            "canonical_name": family["canonical_name"],
            "event_count": len(rows),
            "first_event": first,
            "state": "INTERNAL_DOCUMENTED" if first else "TOKEN_VAZIO_IN_SCANNED_INPUT",
            "claim_allowed": False,
        })

    return {
        "schema": "rafaelia.novoexport.anteriority-summary/v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "policy": {
            "append_only": True,
            "evidence_first": True,
            "first_mention_not_first_invention": True,
            "internal_anteriority_not_public_disclosure": True,
            "public_disclosure_not_legal_priority": True,
            "claim_allowed_default": False,
        },
        "events_total": len(event_list),
        "families": families,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("export_root", type=Path, help="Directory containing conversations-*.json shards")
    ap.add_argument("--config", type=Path, required=True, help="Family query config JSON")
    ap.add_argument("--events", type=Path, required=True, help="Output JSONL events path")
    ap.add_argument("--summary", type=Path, required=True, help="Output summary JSON path")
    args = ap.parse_args()

    config = load_json(args.config)
    shards = sorted(args.export_root.glob("conversations-*.json"))
    if not shards:
        raise SystemExit("no conversations-*.json shards found")

    events: List[Dict[str, Any]] = []
    for shard in shards:
        events.extend(scan_shard(shard, config))
    events.sort(key=event_sort_key)

    args.events.parent.mkdir(parents=True, exist_ok=True)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    with args.events.open("w", encoding="utf-8") as fh:
        for event in events:
            fh.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    summary = build_summary(events, config)
    with args.summary.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")

    print(f"PASS shards={len(shards)} events={len(events)} claim_allowed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
