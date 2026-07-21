#!/usr/bin/env python3
"""
generate_asset_index.py — Automated index generator for Mapa repository.

Closes M2: Índices em biblioteconomia/ e indices/ eram manuais — sem geração automatizada.

Scans the repository tree and emits indices/ASSET_INDEX_AUTO.yaml with:
  - Every tracked file path, extension, directory category
  - Inferred content type (yaml/markdown/python/json/other)
  - Last-modified timestamp (git log, fallback to mtime)
  - Total counts per category

Run from repo root:
    python3 scripts/generate_asset_index.py [--out indices/ASSET_INDEX_AUTO.yaml]
"""

from __future__ import annotations

import argparse
import datetime
import os
import subprocess
import sys
from pathlib import Path


SKIP_DIRS = {".git", "node_modules", "__pycache__", ".mypy_cache"}

CATEGORY_MAP = {
    "biblioteconomia": "knowledge-classification",
    "indices": "index",
    "scripts": "tooling",
    "workflows": "workflow",
    "orquestrador": "orchestration",
    "visual": "visual-asset",
}

EXT_TYPE_MAP = {
    ".md": "markdown",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".py": "python",
    ".sh": "shell",
    ".txt": "text",
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".svg": "image",
}


def git_mtime(path: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(path)],
            capture_output=True, text=True, timeout=5
        )
        ts = result.stdout.strip()
        return ts if ts else None
    except Exception:
        return None


def scan_repo(root: Path) -> list[dict]:
    entries = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Prune skip dirs in-place so os.walk doesn't descend
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        rel_dir = Path(dirpath).relative_to(root)

        for fname in sorted(filenames):
            fpath = Path(dirpath) / fname
            rel = fpath.relative_to(root)
            parts = rel.parts
            # Determine category from top-level directory
            top = parts[0] if len(parts) > 1 else "root"
            category = CATEGORY_MAP.get(top, top)

            ext = fpath.suffix.lower()
            content_type = EXT_TYPE_MAP.get(ext, "other")

            mtime = git_mtime(rel) or datetime.datetime.fromtimestamp(
                fpath.stat().st_mtime, tz=datetime.timezone.utc
            ).isoformat()

            entries.append({
                "path": str(rel),
                "category": category,
                "content_type": content_type,
                "extension": ext or "(none)",
                "last_modified": mtime,
            })
    return entries


def build_yaml(entries: list[dict]) -> str:
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    counts: dict[str, int] = {}
    for e in entries:
        counts[e["category"]] = counts.get(e["category"], 0) + 1

    lines = [
        "# AUTO-GENERATED — do not edit by hand. Run scripts/generate_asset_index.py",
        f"schema: mapa_asset_index_auto_v1",
        f"generated: '{now}'",
        f"total_files: {len(entries)}",
        "counts_by_category:",
    ]
    for cat, cnt in sorted(counts.items()):
        lines.append(f"  {cat}: {cnt}")
    lines.append("items:")
    for e in entries:
        lines.append(f"  - path: {e['path']}")
        lines.append(f"    category: {e['category']}")
        lines.append(f"    content_type: {e['content_type']}")
        lines.append(f"    extension: '{e['extension']}'")
        lines.append(f"    last_modified: '{e['last_modified']}'")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate ASSET_INDEX_AUTO.yaml")
    parser.add_argument("--out", default="indices/ASSET_INDEX_AUTO.yaml",
                        help="Output file path (default: indices/ASSET_INDEX_AUTO.yaml)")
    parser.add_argument("--root", default=".", help="Repository root (default: .)")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    out_path = root / args.out

    print(f"Scanning {root} …", file=sys.stderr)
    entries = scan_repo(root)
    print(f"  Found {len(entries)} files", file=sys.stderr)

    yaml_out = build_yaml(entries)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(yaml_out, encoding="utf-8")
    print(f"Written: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
