#!/usr/bin/env python3
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
CONTRACT = ROOT / "data" / "control-plane" / "PAGES_PUBLICATION_AUTHORITY.v1.json"
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
USES = re.compile(r"^\s*-?\s*uses:\s*[^@\s]+@([^\s#]+)")


def trigger_block(text: str) -> str:
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip() == "on:"), None)
    if start is None:
        return ""
    out = []
    for line in lines[start + 1 :]:
        if line and not line.startswith((" ", "\t")):
            break
        out.append(line)
    return "\n".join(out)


def is_pages_producer(text: str) -> bool:
    return "pages: write" in text and "actions/deploy-pages@" in text


def auto_push_main(text: str) -> bool:
    block = trigger_block(text)
    return "push:" in block and ("main" in block or "branches:" not in block)


def action_refs(text: str):
    for line in text.splitlines():
        match = USES.match(line)
        if match:
            yield match.group(1)


def main() -> int:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    authoritative = contract["automatic_producer"]

    producers = {}
    for path in sorted(WORKFLOWS.glob("*.y*ml")):
        text = path.read_text(encoding="utf-8")
        if is_pages_producer(text):
            rel = path.relative_to(ROOT).as_posix()
            producers[rel] = {
                "auto": auto_push_main(text),
                "refs": list(action_refs(text)),
            }

    automatic = sorted(path for path, meta in producers.items() if meta["auto"])
    assert automatic == [authoritative], (
        f"expected exactly one automatic Pages producer {authoritative!r}; got {automatic!r}"
    )

    authority_meta = producers.get(authoritative)
    assert authority_meta is not None, f"authority {authoritative!r} is not a Pages producer"
    bad_refs = [ref for ref in authority_meta["refs"] if not FULL_SHA.fullmatch(ref)]
    assert not bad_refs, (
        f"authoritative Pages producer must use full 40-hex Action pins; got {bad_refs!r}"
    )

    declared_alternatives = set(contract["alternatives"])
    observed_alternatives = set(producers) - {authoritative}
    assert declared_alternatives == observed_alternatives, (
        "contract/workflow producer set mismatch: "
        f"declared={sorted(declared_alternatives)!r}, observed={sorted(observed_alternatives)!r}"
    )

    for path in observed_alternatives:
        assert not producers[path]["auto"], f"alternative producer {path} must remain manual-only"

    print(
        "PASS pages publication authority: "
        f"authority={authoritative}; producers={len(producers)}; automatic=1"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL pages publication authority: {exc}", file=sys.stderr)
        raise SystemExit(1)
