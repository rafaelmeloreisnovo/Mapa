#!/usr/bin/env python3
"""Fail-closed, privacy-preserving indexer for OpenAI conversations.json."""
from __future__ import annotations

import argparse
import codecs
import hashlib
import json
from pathlib import Path
from typing import Any, BinaryIO, Iterator, Sequence

BUFFER = 1024 * 1024
VERSION = "1.0.0"


class CustodyError(ValueError):
    pass


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(BUFFER):
            h.update(chunk)
    return h.hexdigest()


def opaque(value: Any) -> str | None:
    return None if value is None else digest_bytes(str(value).encode("utf-8"))


def boundary(parts: Sequence[Path], reverse: bool = False) -> str | None:
    ordered = reversed(parts) if reverse else parts
    for path in ordered:
        size = path.stat().st_size
        with path.open("rb") as stream:
            if not reverse:
                while chunk := stream.read(BUFFER):
                    for byte in chunk:
                        if not chr(byte).isspace():
                            return chr(byte)
            else:
                pos = size
                while pos:
                    n = min(BUFFER, pos)
                    pos -= n
                    stream.seek(pos)
                    for byte in reversed(stream.read(n)):
                        if not chr(byte).isspace():
                            return chr(byte)
    return None


class PartsReader:
    def __init__(self, parts: Sequence[Path]) -> None:
        self.parts = list(parts)
        self.index = 0
        self.stream: BinaryIO | None = None

    def _next(self) -> bool:
        if self.stream:
            self.stream.close()
        self.stream = None
        if self.index == len(self.parts):
            return False
        self.stream = self.parts[self.index].open("rb")
        self.index += 1
        return True

    def read(self, size: int = -1) -> bytes:
        out: list[bytes] = []
        left = size
        while size < 0 or left > 0:
            if self.stream is None and not self._next():
                break
            assert self.stream
            chunk = self.stream.read(-1 if size < 0 else left)
            if chunk:
                out.append(chunk)
                if size >= 0:
                    left -= len(chunk)
            elif not self._next():
                break
        return b"".join(out)

    def __enter__(self) -> "PartsReader":
        return self

    def __exit__(self, *_: object) -> None:
        if self.stream:
            self.stream.close()


def source_manifest(parts: Sequence[Path]) -> tuple[list[dict[str, Any]], str, int]:
    combined = hashlib.sha256()
    records: list[dict[str, Any]] = []
    total = 0
    for order, path in enumerate(parts, 1):
        part_hash = hashlib.sha256()
        size = 0
        with path.open("rb") as stream:
            while chunk := stream.read(BUFFER):
                part_hash.update(chunk)
                combined.update(chunk)
                size += len(chunk)
        records.append({"order": order, "name": path.name,
                        "size_bytes": size, "sha256": part_hash.hexdigest()})
        total += size
    return records, combined.hexdigest(), total


def iter_array(parts: Sequence[Path], max_record_bytes: int) -> Iterator[Any]:
    """Incrementally parse a UTF-8 top-level array across arbitrary byte splits."""
    json_decoder = json.JSONDecoder()
    utf8 = codecs.getincrementaldecoder("utf-8")("strict")
    text, pos, eof = "", 0, False

    with PartsReader(parts) as reader:
        def compact() -> None:
            nonlocal text, pos
            if pos:
                text, pos = text[pos:], 0

        def more() -> bool:
            nonlocal text, eof
            if eof:
                return False
            compact()
            raw = reader.read(BUFFER)
            if raw:
                text += utf8.decode(raw, final=False)
                return True
            text += utf8.decode(b"", final=True)
            eof = True
            return False

        def ensure() -> bool:
            while pos >= len(text) and not eof:
                more()
            return pos < len(text)

        def spaces() -> None:
            nonlocal pos
            while True:
                while pos < len(text) and text[pos].isspace():
                    pos += 1
                if pos < len(text) or eof:
                    return
                more()

        if not ensure():
            raise CustodyError("empty source")
        spaces()
        if not ensure() or text[pos] != "[":
            raise CustodyError("root is not a JSON array")
        pos += 1
        first = True

        while True:
            spaces()
            if not ensure():
                raise CustodyError("missing closing bracket")
            if text[pos] == "]":
                pos += 1
                tail = text[pos:] + utf8.decode(reader.read(), final=True)
                if tail.strip():
                    raise CustodyError("bytes after JSON array")
                return
            if not first:
                if text[pos] != ",":
                    raise CustodyError("expected comma or closing bracket")
                pos += 1
                spaces()
                if not ensure() or text[pos] == "]":
                    raise CustodyError("incomplete array or trailing comma")

            start = pos
            while True:
                try:
                    value, end = json_decoder.raw_decode(text, pos)
                    break
                except json.JSONDecodeError as exc:
                    if len(text[start:].encode("utf-8")) > max_record_bytes:
                        raise CustodyError("record exceeds max_record_bytes") from exc
                    if eof:
                        raise CustodyError(f"malformed JSON: {exc.msg}") from exc
                    if start:
                        text, pos, start = text[start:], pos - start, 0
                    raw = reader.read(BUFFER)
                    if raw:
                        text += utf8.decode(raw, final=False)
                    else:
                        text += utf8.decode(b"", final=True)
                        eof = True
            yield value
            pos, first = end, False
            if pos > 2 * BUFFER:
                compact()


def time_value(value: Any) -> float | int | None:
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def depth(mapping: dict[str, Any], node_id: str) -> int | None:
    count, seen, current = 0, set(), node_id
    while True:
        if current in seen:
            return None
        seen.add(current)
        node = mapping.get(current)
        if not isinstance(node, dict) or node.get("parent") is None:
            return count
        current, count = str(node["parent"]), count + 1


def index_one(value: Any, ordinal: int, include_ids: bool) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if not isinstance(value, dict):
        raise CustodyError(f"conversation {ordinal} is not an object")
    conv_id = value.get("id") or f"ordinal:{ordinal}"
    mapping = value.get("mapping") if isinstance(value.get("mapping"), dict) else {}
    rows: list[dict[str, Any]] = []
    for node_id, node in sorted(mapping.items(), key=lambda item: str(item[0])):
        if not isinstance(node, dict) or not isinstance(node.get("message"), dict):
            continue
        message = node["message"]
        author = message.get("author") if isinstance(message.get("author"), dict) else {}
        content = message.get("content")
        content_type = content.get("content_type") if isinstance(content, dict) else None
        payload = canonical(content)
        row = {
            "schema": "rafaelia.conversation-message-index.v1",
            "conversation_id_sha256": opaque(conv_id),
            "message_id_sha256": opaque(message.get("id") or node_id),
            "node_id_sha256": opaque(node_id),
            "parent_node_id_sha256": opaque(node.get("parent")),
            "ordinal": len(rows) + 1,
            "depth": depth(mapping, str(node_id)),
            "role": author.get("role") if isinstance(author.get("role"), str) else "TOKEN_VAZIO_ROLE",
            "content_type": content_type if isinstance(content_type, str) else "TOKEN_VAZIO_CONTENT_TYPE",
            "create_time": time_value(message.get("create_time")),
            "content_sha256": digest_bytes(payload),
            "content_canonical_bytes": len(payload),
            "raw_content_included": False,
            "claim_allowed": False,
        }
        if include_ids:
            row.update({"conversation_id": str(conv_id), "message_id": str(message.get("id") or node_id),
                        "node_id": str(node_id), "parent_node_id": node.get("parent")})
        rows.append(row)

    title = str(value.get("title") or "").encode("utf-8")
    structure = [{key: row[key] for key in ("message_id_sha256", "parent_node_id_sha256",
                                             "role", "content_type", "content_sha256")} for row in rows]
    conv = {
        "schema": "rafaelia.conversation-index.v1",
        "ordinal": ordinal,
        "conversation_id_sha256": opaque(conv_id),
        "title_sha256": digest_bytes(title),
        "title_utf8_bytes": len(title),
        "create_time": time_value(value.get("create_time")),
        "update_time": time_value(value.get("update_time")),
        "message_count": len(rows),
        "mapping_node_count": len(mapping),
        "structural_sha256": digest_bytes(canonical(structure)),
        "raw_title_included": False,
        "raw_content_included": False,
        "claim_allowed": False,
    }
    if include_ids:
        conv["conversation_id"] = str(conv_id)
    return conv, rows


def write_json(path: Path, value: Any) -> None:
    path.write_bytes(canonical(value))


def write_jsonl(path: Path, rows: Sequence[dict[str, Any]]) -> None:
    path.write_bytes(b"".join(canonical(row) for row in rows))


def sums(out: Path) -> None:
    lines = [f"{digest_file(path)}  {path.name}" for path in sorted(out.iterdir())
             if path.is_file() and path.name != "SHA256SUMS"]
    (out / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(parts: Sequence[Path], out: Path, *, source_id: str,
        include_opaque_ids: bool = False,
        max_record_bytes: int = 128 * 1024 * 1024) -> dict[str, Any]:
    sources = [Path(path) for path in parts]
    if not sources or any(not path.is_file() for path in sources):
        raise CustodyError("ordered existing source parts are required")
    out.mkdir(parents=True, exist_ok=True)
    records, logical_hash, total = source_manifest(sources)
    first, last = boundary(sources), boundary(sources, reverse=True)
    complete = first == "[" and last == "]"
    manifest = {
        "schema": "rafaelia.conversation-custody-manifest.v1", "schema_version": VERSION,
        "source_id": source_id, "source_parts": records, "logical_source_bytes": total,
        "logical_source_sha256": logical_hash, "ordered_concatenation": True,
        "source_modified": False,
        "boundary": {"first_non_whitespace": first, "last_non_whitespace": last,
                     "starts_with_json_array": first == "[", "ends_with_json_array": last == "]"},
        "privacy": {"raw_titles_in_index": False, "raw_message_bodies_in_index": False,
                    "opaque_ids_included": include_opaque_ids},
        "claim_allowed": False,
    }
    write_json(out / "source.manifest.json", manifest)
    conversations: list[dict[str, Any]] = []
    messages: list[dict[str, Any]] = []
    state, error = "TOKEN_VAZIO_REASSEMBLY_REQUIRED", None
    if complete:
        try:
            for ordinal, value in enumerate(iter_array(sources, max_record_bytes), 1):
                conv, rows = index_one(value, ordinal, include_opaque_ids)
                conversations.append(conv)
                messages.extend(rows)
            state = "INDEXED_PRIVACY_PRESERVING"
        except (CustodyError, UnicodeDecodeError) as exc:
            state, error = "TOKEN_VAZIO_SOURCE_PARSE_FAILED", f"{type(exc).__name__}: {exc}"
    else:
        error = "complete ordered top-level JSON array not observed"

    if state == "INDEXED_PRIVACY_PRESERVING":
        write_jsonl(out / "conversations.index.jsonl", conversations)
        write_jsonl(out / "messages.index.jsonl", messages)
    else:
        for name in ("conversations.index.jsonl", "messages.index.jsonl"):
            (out / name).unlink(missing_ok=True)

    audit = [{"schema": "rafaelia.conversation-custody-audit.v1",
              "event": "INDEX_MATERIALIZED" if state == "INDEXED_PRIVACY_PRESERVING" else "INDEX_BLOCKED_FAIL_CLOSED",
              "state": state, "source_id": source_id, "logical_source_sha256": logical_hash,
              "raw_private_text_copied": False, "claim_allowed": False}]
    write_jsonl(out / "audit.jsonl", audit)
    receipt = {
        "schema": "rafaelia.conversation-custody-receipt.v1", "source_id": source_id,
        "state": state, "logical_source_sha256": logical_hash, "logical_source_bytes": total,
        "conversation_count": len(conversations), "message_count": len(messages), "error": error,
        "falsifier": "hash/order/UTF-8/JSON/boundary mismatch or raw-text leakage",
        "next_verifiable_step": "verify ordered full reassembly and rerun" if state != "INDEXED_PRIVACY_PRESERVING" else "reconcile counts and review privacy",
        "claim_allowed": False,
    }
    write_json(out / "receipt.json", receipt)
    (out / "coverage_report.md").write_text(
        f"# Conversation custody coverage V1\n\n- State: `{state}`\n- Bytes: `{total}`\n"
        f"- SHA-256: `{logical_hash}`\n- Conversations: `{len(conversations)}`\n"
        f"- Messages: `{len(messages)}`\n- Raw private text copied: `false`\n"
        f"- Claim allowed: `false`\n\n## F_gap\n\n- {error or 'independent reconciliation pending'}\n",
        encoding="utf-8")
    sums(out)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("parts", nargs="+", type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--source-id", default="CONVERSATIONS-EXPORT")
    parser.add_argument("--include-opaque-ids", action="store_true")
    parser.add_argument("--max-record-bytes", type=int, default=128 * 1024 * 1024)
    args = parser.parse_args()
    try:
        receipt = run(args.parts, args.out_dir, source_id=args.source_id,
                      include_opaque_ids=args.include_opaque_ids,
                      max_record_bytes=args.max_record_bytes)
    except (OSError, CustodyError) as exc:
        print(f"FAIL_CLOSED: {type(exc).__name__}: {exc}")
        return 2
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0 if receipt["state"] == "INDEXED_PRIVACY_PRESERVING" else 3


if __name__ == "__main__":
    raise SystemExit(main())
