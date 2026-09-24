#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SCHEMA = "rafaelia.byte-catalog.v1"

def ascii_class(value):
    if value <= 0x1F:
        return "CONTROL"
    if value <= 0x7E:
        return "PRINTABLE"
    if value == 0x7F:
        return "DEL"
    return "NON_ASCII"

def ascii_symbol(value):
    if 0x20 <= value <= 0x7E:
        return chr(value)
    return None

def utf8_role(value):
    if value <= 0x7F:
        return "SINGLE_BYTE_ASCII"
    if 0x80 <= value <= 0xBF:
        return "CONTINUATION"
    if 0xC2 <= value <= 0xDF:
        return "LEAD_2"
    if 0xE0 <= value <= 0xEF:
        return "LEAD_3"
    if 0xF0 <= value <= 0xF4:
        return "LEAD_4"
    return "INVALID_LEAD"

def make_row(value):
    return {
        "schema": SCHEMA,
        "byte_dec": value,
        "byte_hex": f"0x{value:02X}",
        "bits": f"{value:08b}",
        "popcount": value.bit_count(),
        "ascii_class": ascii_class(value),
        "ascii_symbol": ascii_symbol(value),
        "latin1_codepoint": f"U+{value:04X}",
        "utf8_role": utf8_role(value),
        "standalone_utf8": value <= 0x7F,
        "semantic_state": "TOKEN_VAZIO_UNBOUND",
        "claim_allowed": False,
    }

def generate():
    return [make_row(value) for value in range(256)]

def write_jsonl(path):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        for row in generate():
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="data/catalog/byte_catalog_v1.jsonl",
    )
    args = parser.parse_args()
    write_jsonl(args.output)

if __name__ == "__main__":
    main()
