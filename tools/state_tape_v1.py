#!/usr/bin/env python3
import argparse
import binascii
import json
from pathlib import Path

SCHEMA = "rafaelia.state-tape.v1"

def _crc32(data):
    return f"{binascii.crc32(data) & 0xFFFFFFFF:08x}"

def pair16(data, endian="big"):
    if endian not in {"big", "little"}:
        raise ValueError("endian must be big or little")
    out = []
    usable = len(data) - (len(data) % 2)
    for offset in range(0, usable, 2):
        a = data[offset]
        b = data[offset + 1]
        if endian == "big":
            word = (a << 8) | b
        else:
            word = a | (b << 8)
        out.append({
            "offset": offset,
            "byte_a": a,
            "byte_b": b,
            "word16": word,
            "word16_hex": f"0x{word:04X}",
            "endian": endian,
        })
    return out

def combine_byte_pair(a, b):
    if not 0 <= a <= 255 or not 0 <= b <= 255:
        raise ValueError("bytes must be in 0..255")
    total = a + b
    return {
        "a": a,
        "b": b,
        "or8": a | b,
        "and8": a & b,
        "xor8": a ^ b,
        "add8_mod256": total & 0xFF,
        "carry": 1 if total > 0xFF else 0,
        "concat16_be": (a << 8) | b,
        "concat16_le": a | (b << 8),
        "same_bit_mask": (~(a ^ b)) & 0xFF,
        "different_bit_mask": a ^ b,
        "semantic_operator": "TOKEN_VAZIO_UNBOUND",
    }

def compose_streams(left, right):
    width = min(len(left), len(right))
    return {
        "length_compared": width,
        "left_extra_bytes": max(0, len(left) - width),
        "right_extra_bytes": max(0, len(right) - width),
        "pairs": [
            {
                "offset": i,
                **combine_byte_pair(left[i], right[i]),
            }
            for i in range(width)
        ],
        "operator_choice": "TOKEN_VAZIO_UNBOUND",
        "claim_allowed": False,
    }

def snapshot_delta(before, after, block_size=64, page_size=256):
    if block_size <= 0 or page_size <= 0:
        raise ValueError("block_size and page_size must be positive")

    max_len = max(len(before), len(after))
    activity = []
    total_changed_bytes = 0
    total_changed_bits = 0
    total_unchanged_bytes = 0

    for block_index, start in enumerate(range(0, max_len, block_size)):
        left = before[start:start + block_size]
        right = after[start:start + block_size]
        width = max(len(left), len(right))
        left_pad = left + b"\x00" * (width - len(left))
        right_pad = right + b"\x00" * (width - len(right))
        xor_mask = bytes(a ^ b for a, b in zip(left_pad, right_pad))
        changed_bytes = sum(1 for value in xor_mask if value)
        changed_bits = sum(value.bit_count() for value in xor_mask)
        unchanged_bytes = width - changed_bytes

        total_changed_bytes += changed_bytes
        total_changed_bits += changed_bits
        total_unchanged_bytes += unchanged_bytes

        activity.append({
            "block_index": block_index,
            "offset": start,
            "length": width,
            "changed_bytes": changed_bytes,
            "changed_bits": changed_bits,
            "changed": changed_bytes > 0,
            "xor_mask_hex": xor_mask.hex(),
            "before_crc32": _crc32(left_pad),
            "after_crc32": _crc32(right_pad),
        })

    if len(before) != len(after):
        state = "SIZE_CHANGED"
    elif total_changed_bytes == 0:
        state = "NO_DELTA"
    else:
        state = "SPARSE_DELTA_OBSERVED"

    page_activity = []
    for page_index, start in enumerate(range(0, max_len, page_size)):
        left = before[start:start + page_size]
        right = after[start:start + page_size]
        width = max(len(left), len(right))
        left_pad = left + b"\x00" * (width - len(left))
        right_pad = right + b"\x00" * (width - len(right))
        xor_mask = bytes(a ^ b for a, b in zip(left_pad, right_pad))
        page_activity.append({
            "page_index": page_index,
            "offset": start,
            "length": width,
            "changed": any(xor_mask),
            "changed_bytes": sum(1 for value in xor_mask if value),
            "changed_bits": sum(value.bit_count() for value in xor_mask),
        })

    return {
        "schema": SCHEMA,
        "before_size": len(before),
        "after_size": len(after),
        "changed_bytes": total_changed_bytes,
        "changed_bits": total_changed_bits,
        "unchanged_bytes": total_unchanged_bytes,
        "block_size": block_size,
        "page_size": page_size,
        "activity": activity,
        "page_activity": page_activity,
        "state": state,
        "interpretation": "TOKEN_VAZIO_UNBOUND",
        "claim_allowed": False,
    }

def punched_tape(delta):
    return "".join("●" if block["changed"] else "·" for block in delta["activity"])

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    pair = sub.add_parser("pair16")
    pair.add_argument("input")
    pair.add_argument("--endian", choices=["big", "little"], default="big")

    delta = sub.add_parser("delta")
    delta.add_argument("before")
    delta.add_argument("after")
    delta.add_argument("--block-size", type=int, default=64)
    delta.add_argument("--page-size", type=int, default=256)

    args = parser.parse_args()
    if args.command == "pair16":
        data = Path(args.input).read_bytes()
        out = {
            "schema": "rafaelia.pair16.v1",
            "source": Path(args.input).name,
            "pairs": pair16(data, args.endian),
            "claim_allowed": False,
        }
    else:
        out = snapshot_delta(
            Path(args.before).read_bytes(),
            Path(args.after).read_bytes(),
            block_size=args.block_size,
            page_size=args.page_size,
        )
        out["punched_tape"] = punched_tape(out)

    print(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
