#!/usr/bin/env python3
import argparse
import binascii
import hashlib
import json
import struct
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath

SCHEMA = "rafaelia.zip-byte-catalog.v1"
TILE_BYTES = 64
PAGE_BYTES = 256

def _crc32(data):
    return f"{binascii.crc32(data) & 0xFFFFFFFF:08x}"

def _sha256(data):
    return hashlib.sha256(data).hexdigest()

def _unsafe_member_name(name):
    normalized = name.replace("\\", "/")
    path = PurePosixPath(normalized)
    return (
        normalized.startswith("/")
        or any(part == ".." for part in path.parts)
        or "\x00" in name
    )

def _tile_rows(data):
    return [
        " ".join(f"{byte:02X}" for byte in data[i:i + 8])
        for i in range(0, len(data), 8)
    ]

def _word_view(data, width, endian):
    usable = len(data) - (len(data) % width)
    code = {4: "I", 8: "Q"}[width]
    prefix = {"little": "<", "big": ">"}[endian]
    return [
        struct.unpack(prefix + code, data[i:i + width])[0]
        for i in range(0, usable, width)
    ]

def _text_state(data):
    try:
        data.decode("ascii")
        return "ASCII_VALID"
    except UnicodeDecodeError:
        pass
    try:
        data.decode("utf-8")
        return "UTF8_VALID"
    except UnicodeDecodeError:
        return "BINARY_OR_OTHER_ENCODING"

def _nested_archive_state(data):
    zip_signatures = (b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")
    if data.startswith(zip_signatures):
        return "TOKEN_VAZIO_NOT_EXPANDED"
    return "NOT_ZIP_SIGNATURE"

def _compression_ratio(info):
    if info.compress_size == 0:
        return None
    return info.file_size / info.compress_size

def scan_zip(
    archive_path,
    *,
    max_members=1024,
    max_member_bytes=4 * 1024 * 1024,
    max_total_bytes=16 * 1024 * 1024,
    include_word_views=False,
):
    path = Path(archive_path)
    result = {
        "schema": SCHEMA,
        "archive_name": path.name,
        "archive_size": path.stat().st_size,
        "tile_bytes": TILE_BYTES,
        "tile_shape": [8, 8],
        "page_bytes": PAGE_BYTES,
        "limits": {
            "max_members": max_members,
            "max_member_bytes": max_member_bytes,
            "max_total_bytes": max_total_bytes,
        },
        "members": [],
        "redundancy_groups": [],
        "semantic_state": "TOKEN_VAZIO_UNBOUND",
        "claim_allowed": False,
    }

    block_refs = []
    total_read = 0

    with zipfile.ZipFile(path, "r") as archive:
        infos = archive.infolist()
        result["member_count_declared"] = len(infos)
        if len(infos) > max_members:
            result["archive_state"] = "TOKEN_VAZIO_MEMBER_LIMIT"
            infos = infos[:max_members]
        else:
            result["archive_state"] = "CATALOGUED_BOUNDED"

        for member_index, info in enumerate(infos):
            record = {
                "member_index": member_index,
                "name": info.filename,
                "unsafe_path_flag": _unsafe_member_name(info.filename),
                "is_directory": info.is_dir(),
                "encrypted": bool(info.flag_bits & 0x1),
                "compression_type": info.compress_type,
                "compressed_size": info.compress_size,
                "file_size": info.file_size,
                "header_crc32": f"{info.CRC:08x}",
                "compression_ratio": _compression_ratio(info),
                "blocks": [],
                "pages": [],
                "semantic_state": "TOKEN_VAZIO_UNBOUND",
            }

            if info.is_dir():
                record["state"] = "DIRECTORY"
                result["members"].append(record)
                continue

            if record["encrypted"]:
                record["state"] = "TOKEN_VAZIO_ENCRYPTED"
                result["members"].append(record)
                continue

            if info.file_size > max_member_bytes:
                record["state"] = "TOKEN_VAZIO_MEMBER_SIZE_LIMIT"
                result["members"].append(record)
                continue

            if total_read + info.file_size > max_total_bytes:
                record["state"] = "TOKEN_VAZIO_TOTAL_SIZE_LIMIT"
                result["members"].append(record)
                continue

            try:
                data = archive.read(info)
            except (RuntimeError, NotImplementedError, zipfile.BadZipFile) as exc:
                record["state"] = "TOKEN_VAZIO_READ_ERROR"
                record["error_type"] = type(exc).__name__
                result["members"].append(record)
                continue

            total_read += len(data)
            computed_crc = _crc32(data)
            record.update({
                "state": "CATALOGUED",
                "bytes_read": len(data),
                "computed_crc32": computed_crc,
                "crc_match": computed_crc == record["header_crc32"],
                "sha256": _sha256(data),
                "text_state": _text_state(data),
                "nested_archive_state": _nested_archive_state(data),
            })

            for block_index, start in enumerate(range(0, len(data), TILE_BYTES)):
                chunk = data[start:start + TILE_BYTES]
                digest = _sha256(chunk)
                hist = Counter(chunk)
                block = {
                    "block_index": block_index,
                    "offset": start,
                    "length": len(chunk),
                    "full_tile_8x8": len(chunk) == TILE_BYTES,
                    "tile_hex_rows": _tile_rows(chunk),
                    "crc32": _crc32(chunk),
                    "sha256": digest,
                    "redundancy_group_id": None,
                    "redundancy_count": None,
                    "byte_hist_nonzero": {
                        f"0x{value:02X}": hist[value]
                        for value in sorted(hist)
                    },
                    "read32_count": len(chunk) // 4,
                    "read64_count": len(chunk) // 8,
                    "semantic_state": "TOKEN_VAZIO_UNBOUND",
                }
                if include_word_views:
                    block["word_views"] = {
                        "u32_le": _word_view(chunk, 4, "little"),
                        "u32_be": _word_view(chunk, 4, "big"),
                        "u64_le": _word_view(chunk, 8, "little"),
                        "u64_be": _word_view(chunk, 8, "big"),
                    }
                record["blocks"].append(block)
                block_refs.append((digest, block))

            for page_index, start in enumerate(range(0, len(data), PAGE_BYTES)):
                page = data[start:start + PAGE_BYTES]
                record["pages"].append({
                    "page_index": page_index,
                    "offset": start,
                    "length": len(page),
                    "full_page_256": len(page) == PAGE_BYTES,
                    "crc32": _crc32(page),
                    "sha256": _sha256(page),
                    "read32_count": len(page) // 4,
                    "read64_count": len(page) // 8,
                    "semantic_state": "TOKEN_VAZIO_UNBOUND",
                })

            result["members"].append(record)

    counts = Counter(digest for digest, _ in block_refs)
    group_by_digest = {}
    for digest, _ in block_refs:
        if digest not in group_by_digest:
            group_by_digest[digest] = f"R{len(group_by_digest) + 1:06d}"

    for digest, block in block_refs:
        block["redundancy_group_id"] = group_by_digest[digest]
        block["redundancy_count"] = counts[digest]

    result["redundancy_groups"] = [
        {
            "redundancy_group_id": group_by_digest[digest],
            "sha256": digest,
            "occurrences": counts[digest],
            "is_redundant": counts[digest] > 1,
        }
        for digest in group_by_digest
    ]
    result["bytes_read_total"] = total_read
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive")
    parser.add_argument("--max-members", type=int, default=1024)
    parser.add_argument("--max-member-bytes", type=int, default=4 * 1024 * 1024)
    parser.add_argument("--max-total-bytes", type=int, default=16 * 1024 * 1024)
    parser.add_argument("--include-word-views", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()

    result = scan_zip(
        args.archive,
        max_members=args.max_members,
        max_member_bytes=args.max_member_bytes,
        max_total_bytes=args.max_total_bytes,
        include_word_views=args.include_word_views,
    )
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")

if __name__ == "__main__":
    main()
