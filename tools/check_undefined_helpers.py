#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

FORBIDDEN = [
    r"^__aeabi_",
    r"^__gnu_",
    r"^__stack_chk_",
    r"^(memcpy|memmove|memset|memcmp)$",
    r"^(malloc|free|calloc|realloc)$",
]
allowed = set(sys.argv[2].split(",")) if len(sys.argv) > 2 and sys.argv[2] else set()
symbols = []
for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
    symbol = line.strip().split()[-1] if line.strip() else ""
    if symbol:
        symbols.append(symbol)
bad = sorted({symbol for symbol in symbols if symbol not in allowed and any(re.search(pattern, symbol) for pattern in FORBIDDEN)})
out = {"status": "PASS" if not bad else "FAIL", "undefined_symbols": sorted(set(symbols)), "forbidden": bad, "claim_allowed": False}
print(json.dumps(out, sort_keys=True))
raise SystemExit(0 if not bad else 1)
