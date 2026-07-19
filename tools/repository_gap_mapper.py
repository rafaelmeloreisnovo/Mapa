#!/usr/bin/env python3
"""Deterministic multi-repository gap mapper for the RAFAELIA ecosystem.

The scanner is intentionally Python-stdlib-only so it can run in Termux, CI,
and restricted/offline environments. It inventories loose files, classifies
ASM/ELF/DEX/APK/Gradle artifacts, detects unresolved markers, checks whether
source artifacts are referenced by build descriptors, and emits JSON + Markdown.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

SCHEMA = "rafaelia.repository-gap-map/v1"
DEFAULT_EXCLUDES = {
    ".git", ".gradle", ".idea", ".repo", ".venv", "build", "dist",
    "node_modules", "__pycache__", "target", "vendor",
}
BUILD_FILENAMES = {
    "android.bp", "android.mk", "cmakelists.txt", "makefile", "meson.build",
    "settings.gradle", "settings.gradle.kts", "build.gradle", "build.gradle.kts",
    "gradle.properties", "pom.xml",
}
BUILD_SUFFIXES = {".mk", ".bp", ".gradle", ".kts", ".cmake", ".meson"}
ASM_SUFFIXES = {".s", ".asm", ".inc"}
C_SUFFIXES = {".c", ".h", ".cc", ".cpp", ".cxx", ".hpp"}
JVM_SUFFIXES = {".java", ".kt", ".kts"}
DOC_SUFFIXES = {".md", ".rst", ".txt", ".adoc"}
TEXT_SUFFIXES = (
    ASM_SUFFIXES | C_SUFFIXES | JVM_SUFFIXES | DOC_SUFFIXES |
    {".py", ".sh", ".bash", ".zsh", ".json", ".jsonl", ".yaml", ".yml",
     ".toml", ".xml", ".properties", ".cfg", ".ini", ".csv", ".tsv"}
)
MARKER_RE = re.compile(
    r"\b(TODO|FIXME|TBD|TOKEN_VAZIO|PLACEHOLDER|STUB|NOASSERTION)\b",
    re.IGNORECASE,
)
DEX_RE = re.compile(br"^dex\n0(?:35|37|38|39|40|41)\x00$")
SPDX_RE = re.compile(r"SPDX-License-Identifier\s*:", re.IGNORECASE)


@dataclass(frozen=True)
class RootSpec:
    name: str
    path: str


@dataclass
class Artifact:
    artifact_id: str
    root: str
    path: str
    size_bytes: int
    kind: str
    language: str | None
    magic: str | None
    sha256: str | None
    hash_status: str
    unresolved_markers: list[str]
    spdx_present: bool | None
    build_referenced: bool | None
    referenced_by: list[str]
    provenance_sidecars: list[str]
    gaps: list[str]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def parse_root(value: str) -> RootSpec:
    if "=" in value:
        name, raw_path = value.split("=", 1)
        if name.strip() and raw_path.strip():
            return RootSpec(name.strip(), str(Path(raw_path).expanduser().resolve()))
    path = Path(value).expanduser().resolve()
    return RootSpec(path.name or "root", str(path))


def is_excluded(path: Path, root: Path, excludes: set[str]) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return True
    return any(part in excludes for part in parts)


def iter_files(root: Path, excludes: set[str]) -> Iterable[Path]:
    for current, dirnames, filenames in os.walk(root):
        current_path = Path(current)
        dirnames[:] = sorted(
            d for d in dirnames
            if d not in excludes and not is_excluded(current_path / d, root, excludes)
        )
        for filename in sorted(filenames):
            path = current_path / filename
            if not is_excluded(path, root, excludes) and path.is_file():
                yield path


def read_prefix(path: Path, limit: int) -> bytes:
    try:
        with path.open("rb") as handle:
            return handle.read(limit)
    except OSError:
        return b""


def sha256_file(path: Path, max_hash_bytes: int) -> tuple[str | None, str]:
    try:
        size = path.stat().st_size
        if max_hash_bytes > 0 and size > max_hash_bytes:
            return None, "skipped_large_file"
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            while True:
                chunk = handle.read(1024 * 1024)
                if not chunk:
                    break
                digest.update(chunk)
        return digest.hexdigest(), "complete"
    except OSError as exc:
        return None, f"error:{exc.__class__.__name__}"


def classify(path: Path, prefix: bytes) -> tuple[str, str | None, str | None]:
    suffix = path.suffix.lower()
    name = path.name.lower()
    if prefix.startswith(b"\x7fELF"):
        return "ELF", None, "elf"
    if len(prefix) >= 8 and DEX_RE.match(prefix[:8]):
        return "DEX", None, prefix[:8].decode("ascii", "replace").rstrip("\x00")
    if suffix == ".apk":
        return "APK", None, "zip" if prefix.startswith(b"PK") else "unknown"
    if suffix in {".jar", ".aar", ".zip"} and prefix.startswith(b"PK"):
        return suffix[1:].upper(), None, "zip"
    if suffix in ASM_SUFFIXES:
        return "ASM_SOURCE", "assembly", None
    if suffix in C_SUFFIXES:
        return "NATIVE_SOURCE", suffix[1:], None
    if suffix in JVM_SUFFIXES:
        return "JVM_SOURCE", suffix[1:], None
    if name in BUILD_FILENAMES or suffix in BUILD_SUFFIXES:
        return "BUILD_DESCRIPTOR", None, None
    if suffix in DOC_SUFFIXES:
        return "DOCUMENT", suffix[1:], None
    if suffix in TEXT_SUFFIXES:
        return "TEXT", suffix[1:] or None, None
    return "FILE", suffix[1:] or None, None


def decode_text(prefix: bytes) -> str | None:
    if b"\x00" in prefix:
        return None
    try:
        return prefix.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return prefix.decode("latin-1")
        except UnicodeDecodeError:
            return None


def marker_list(text: str | None) -> list[str]:
    if not text:
        return []
    return sorted({match.group(1).upper() for match in MARKER_RE.finditer(text)})


def provenance_sidecars(path: Path) -> list[str]:
    candidates = [
        path.with_name(path.name + ".sha256"),
        path.with_name(path.name + ".spdx.json"),
        path.with_name(path.name + ".provenance.json"),
        path.with_suffix(path.suffix + ".sha256"),
    ]
    found = []
    for candidate in candidates:
        if candidate.is_file():
            found.append(candidate.name)
    return sorted(set(found))


def load_build_descriptors(
    root: Path,
    files: Sequence[Path],
    content_limit: int,
) -> dict[str, str]:
    out: dict[str, str] = {}
    for path in files:
        suffix = path.suffix.lower()
        if path.name.lower() not in BUILD_FILENAMES and suffix not in BUILD_SUFFIXES:
            continue
        text = decode_text(read_prefix(path, content_limit))
        if text is not None:
            out[path.relative_to(root).as_posix()] = text
    return out


def build_references(
    rel_path: str,
    basename: str,
    descriptors: dict[str, str],
) -> list[str]:
    normalized = rel_path.replace("\\", "/")
    matches = []
    for descriptor, content in descriptors.items():
        if normalized in content or basename in content:
            matches.append(descriptor)
    return sorted(matches)


def artifact_id(root_name: str, rel_path: str) -> str:
    raw = f"{root_name}\0{rel_path}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:24]


def scan_root(
    spec: RootSpec,
    excludes: set[str],
    content_limit: int,
    max_hash_bytes: int,
) -> tuple[list[Artifact], dict[str, int]]:
    root = Path(spec.path)
    if not root.is_dir():
        raise FileNotFoundError(f"root not found or not a directory: {root}")

    files = list(iter_files(root, excludes))
    descriptors = load_build_descriptors(root, files, content_limit)
    artifacts: list[Artifact] = []
    stats: dict[str, int] = {"files": 0, "bytes": 0, "gaps": 0}

    for path in files:
        rel = path.relative_to(root).as_posix()
        try:
            size = path.stat().st_size
        except OSError:
            size = -1
        prefix = read_prefix(path, content_limit)
        kind, language, magic = classify(path, prefix)
        text = decode_text(prefix) if kind in {
            "ASM_SOURCE", "NATIVE_SOURCE", "JVM_SOURCE", "BUILD_DESCRIPTOR",
            "DOCUMENT", "TEXT",
        } else None
        markers = marker_list(text)
        spdx = bool(SPDX_RE.search(text)) if text is not None else None
        sha256, hash_status = sha256_file(path, max_hash_bytes)
        refs: list[str] = []
        build_ref: bool | None = None
        if kind in {"ASM_SOURCE", "NATIVE_SOURCE", "JVM_SOURCE"}:
            refs = build_references(rel, path.name, descriptors)
            build_ref = bool(refs)
        sidecars = provenance_sidecars(path)
        gaps: list[str] = []
        if markers:
            gaps.append("UNRESOLVED_MARKERS")
        if kind == "ASM_SOURCE" and not build_ref:
            gaps.append("ASM_NOT_REFERENCED_BY_BUILD")
        if kind in {"ELF", "DEX", "APK", "AAR", "JAR"} and not sidecars:
            gaps.append("BINARY_PROVENANCE_MISSING")
        if hash_status != "complete":
            gaps.append("HASH_INCOMPLETE")
        if kind == "DOCUMENT" and markers:
            gaps.append("DOCUMENT_INCOMPLETE")

        artifacts.append(Artifact(
            artifact_id=artifact_id(spec.name, rel),
            root=spec.name,
            path=rel,
            size_bytes=size,
            kind=kind,
            language=language,
            magic=magic,
            sha256=sha256,
            hash_status=hash_status,
            unresolved_markers=markers,
            spdx_present=spdx,
            build_referenced=build_ref,
            referenced_by=refs,
            provenance_sidecars=sidecars,
            gaps=sorted(set(gaps)),
        ))
        stats["files"] += 1
        stats["bytes"] += max(size, 0)
        stats["gaps"] += len(set(gaps))

    artifacts.sort(key=lambda item: (item.root, item.path))
    return artifacts, stats


def summarize(artifacts: Sequence[Artifact]) -> dict[str, int]:
    summary = {
        "artifacts": len(artifacts),
        "gap_instances": 0,
        "files_with_gaps": 0,
        "asm_sources": 0,
        "asm_unreferenced": 0,
        "elf": 0,
        "dex": 0,
        "apk": 0,
        "documents_incomplete": 0,
        "binary_provenance_missing": 0,
    }
    for item in artifacts:
        summary["gap_instances"] += len(item.gaps)
        if item.gaps:
            summary["files_with_gaps"] += 1
        if item.kind == "ASM_SOURCE":
            summary["asm_sources"] += 1
        if "ASM_NOT_REFERENCED_BY_BUILD" in item.gaps:
            summary["asm_unreferenced"] += 1
        if item.kind == "ELF":
            summary["elf"] += 1
        if item.kind == "DEX":
            summary["dex"] += 1
        if item.kind == "APK":
            summary["apk"] += 1
        if "DOCUMENT_INCOMPLETE" in item.gaps:
            summary["documents_incomplete"] += 1
        if "BINARY_PROVENANCE_MISSING" in item.gaps:
            summary["binary_provenance_missing"] += 1
    return summary


def render_markdown(payload: dict) -> str:
    summary = payload["summary"]
    artifacts = payload["artifacts"]
    roots_display = ", ".join("`" + root["name"] + "`" for root in payload["roots"])
    lines = [
        "# Repository Gap Map",
        "",
        f"- Schema: `{payload['schema']}`",
        f"- Generated at: `{payload['generated_at']}`",
        f"- Roots: {roots_display}",
        f"- Files: **{summary['artifacts']}**",
        f"- Files with gaps: **{summary['files_with_gaps']}**",
        f"- Gap instances: **{summary['gap_instances']}**",
        "",
        "## Binary and build-sensitive inventory",
        "",
        "| Metric | Count |",
        "|---|---:|",
        f"| ASM sources | {summary['asm_sources']} |",
        f"| ASM not referenced by build descriptors | {summary['asm_unreferenced']} |",
        f"| ELF artifacts | {summary['elf']} |",
        f"| DEX artifacts | {summary['dex']} |",
        f"| APK artifacts | {summary['apk']} |",
        f"| Binary provenance missing | {summary['binary_provenance_missing']} |",
        f"| Incomplete documents | {summary['documents_incomplete']} |",
        "",
    ]

    gap_rows = [item for item in artifacts if item["gaps"]]
    lines.extend([
        "## Action map",
        "",
        "| Root | Path | Kind | Gaps | Build references |",
        "|---|---|---|---|---|",
    ])
    if not gap_rows:
        lines.append("| — | — | — | No detected gaps | — |")
    else:
        for item in gap_rows:
            refs = "<br>".join(item["referenced_by"]) or "—"
            gaps = "<br>".join(item["gaps"])
            path = item["path"].replace("|", "\\|")
            lines.append(
                f"| `{item['root']}` | `{path}` | `{item['kind']}` | {gaps} | {refs} |"
            )

    lines.extend([
        "",
        "## Deterministic next actions",
        "",
        "1. Promote or quarantine every `ASM_NOT_REFERENCED_BY_BUILD` file.",
        "2. Add provenance sidecars for ELF/DEX/APK/AAR/JAR artifacts.",
        "3. Replace unresolved markers with implementation, evidence, or explicit `TOKEN_VAZIO` ownership.",
        "4. Re-run the mapper and require a reviewed delta before claiming closure.",
        "",
        "```text",
        "claim_allowed=false until build/runtime evidence closes the corresponding gaps",
        "```",
        "",
    ])
    return "\n".join(lines)


def should_fail(artifacts: Sequence[Artifact], mode: str) -> bool:
    if mode == "none":
        return False
    selected = {
        "markers": {"UNRESOLVED_MARKERS", "DOCUMENT_INCOMPLETE"},
        "asm": {"ASM_NOT_REFERENCED_BY_BUILD"},
        "binary": {"BINARY_PROVENANCE_MISSING"},
        "hash": {"HASH_INCOMPLETE"},
    }
    if mode == "any":
        return any(item.gaps for item in artifacts)
    wanted = selected[mode]
    return any(wanted.intersection(item.gaps) for item in artifacts)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Map loose files and build/document gaps across repositories."
    )
    parser.add_argument(
        "--root", action="append", required=True, metavar="[NAME=]PATH",
        help="Root to scan. Repeat for multiple repositories.",
    )
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    parser.add_argument(
        "--exclude", action="append", default=[],
        help="Additional directory name to exclude.",
    )
    parser.add_argument(
        "--content-limit", type=int, default=1024 * 1024,
        help="Maximum bytes inspected for text markers/build references per file.",
    )
    parser.add_argument(
        "--max-hash-bytes", type=int, default=256 * 1024 * 1024,
        help="Skip full SHA-256 above this size; 0 means unlimited.",
    )
    parser.add_argument(
        "--fail-on", choices=["none", "markers", "asm", "binary", "hash", "any"],
        default="none",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    roots = [parse_root(value) for value in args.root]
    excludes = DEFAULT_EXCLUDES | set(args.exclude)
    all_artifacts: list[Artifact] = []
    root_stats: dict[str, dict[str, int]] = {}

    try:
        for spec in roots:
            artifacts, stats = scan_root(
                spec, excludes, args.content_limit, args.max_hash_bytes
            )
            all_artifacts.extend(artifacts)
            root_stats[spec.name] = stats
    except (OSError, ValueError) as exc:
        print(f"repository-gap-mapper: {exc}", file=sys.stderr)
        return 2

    all_artifacts.sort(key=lambda item: (item.root, item.path))
    payload = {
        "schema": SCHEMA,
        "generated_at": utc_now(),
        "roots": [asdict(root) for root in roots],
        "configuration": {
            "excludes": sorted(excludes),
            "content_limit": args.content_limit,
            "max_hash_bytes": args.max_hash_bytes,
            "fail_on": args.fail_on,
        },
        "root_stats": root_stats,
        "summary": summarize(all_artifacts),
        "artifacts": [asdict(item) for item in all_artifacts],
    }

    json_path = Path(args.output_json)
    md_path = Path(args.output_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(payload), encoding="utf-8")

    print(json.dumps(payload["summary"], sort_keys=True))
    return 1 if should_fail(all_artifacts, args.fail_on) else 0


if __name__ == "__main__":
    raise SystemExit(main())
