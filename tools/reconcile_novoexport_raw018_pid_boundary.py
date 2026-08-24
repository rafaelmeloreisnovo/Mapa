#!/usr/bin/env python3
"""Privacy-preserving RAW018 PID reconciliation.

The tool never prints raw conversation IDs. It reconciles:
  historical Locator PID hashes
  - current PID index hashes
  within the live RAW017/RAW019 temporal boundary.

Optionally it verifies every candidate against a byte-backed historical
conversations.json stored inside a ZIP archive.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import zipfile
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Mapping, Sequence, Tuple

UTC = dt.timezone.utc


class ReconciliationError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def pid_hash(conversation_id: str) -> str:
    return hashlib.sha256(conversation_id.encode("utf-8")).hexdigest()


def parse_iso_utc(value: str) -> float:
    value = value.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.timestamp()


def iso_utc(timestamp: float) -> str:
    return (
        dt.datetime.fromtimestamp(timestamp, UTC)
        .isoformat(timespec="microseconds")
        .replace("+00:00", "Z")
    )


def load_raw_shard(path: Path) -> List[Mapping[str, object]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ReconciliationError(f"{path}: root must be a JSON array")
    return data


def conversation_id(obj: Mapping[str, object]) -> str:
    for key in ("id", "conversation_id"):
        value = obj.get(key)
        if isinstance(value, str) and value:
            return value
    raise ReconciliationError("conversation object lacks canonical id")


def create_time(obj: Mapping[str, object]) -> float:
    value = obj.get("create_time")
    if not isinstance(value, (int, float)):
        raise ReconciliationError("conversation object lacks numeric create_time")
    return float(value)


def assert_monotonic(rows: Sequence[Mapping[str, object]], label: str) -> None:
    times = [create_time(row) for row in rows]
    if any(b < a for a, b in zip(times, times[1:])):
        raise ReconciliationError(f"{label}: create_time is not monotonic ascending")


def read_csv(path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise ReconciliationError(f"{path}: missing CSV header")
        return list(reader.fieldnames), list(reader)


def commitment_lines(lines: Iterable[str]) -> str:
    h = hashlib.sha256()
    for line in lines:
        h.update(line.encode("utf-8"))
    return h.hexdigest()


def iter_json_array(stream: io.TextIOBase, chunk_size: int = 1024 * 1024) -> Iterator[Mapping[str, object]]:
    decoder = json.JSONDecoder()
    buf = ""
    pos = 0
    eof = False
    started = False

    while True:
        if not eof and (len(buf) - pos) < chunk_size:
            chunk = stream.read(chunk_size)
            if chunk == "":
                eof = True
            else:
                if pos:
                    buf = buf[pos:] + chunk
                    pos = 0
                else:
                    buf += chunk

        while True:
            while pos < len(buf) and buf[pos].isspace():
                pos += 1
            if not started:
                if pos >= len(buf):
                    break
                if buf[pos] != "[":
                    raise ReconciliationError("archive conversations.json root is not an array")
                started = True
                pos += 1
                continue

            while pos < len(buf) and (buf[pos].isspace() or buf[pos] == ","):
                pos += 1
            if pos < len(buf) and buf[pos] == "]":
                return
            if pos >= len(buf):
                break

            try:
                value, end = decoder.raw_decode(buf, pos)
            except json.JSONDecodeError:
                if eof:
                    raise ReconciliationError("truncated/invalid archive conversations.json")
                if pos:
                    buf = buf[pos:]
                    pos = 0
                break

            if not isinstance(value, dict):
                raise ReconciliationError("archive array member is not an object")
            yield value
            pos = end

            if pos > 8 * 1024 * 1024:
                buf = buf[pos:]
                pos = 0

        if eof:
            if buf[pos:].strip() not in ("", "]"):
                raise ReconciliationError("unexpected trailing archive JSON")
            return


def reconcile(
    locator_csv: Path,
    current_pid_csv: Path,
    raw017_path: Path,
    raw019_path: Path,
    expected_candidates: int,
    archive_zip: Path | None = None,
    archive_member: str = "conversations.json",
    timestamp_tolerance_seconds: float = 0.0011,
) -> Dict[str, object]:
    locator_fields, locator_rows = read_csv(locator_csv)
    current_fields, current_rows = read_csv(current_pid_csv)

    required_locator = {"Conversation PID (SHA-256)", "Created UTC"}
    required_current = {"conversation_pid_sha256"}
    if not required_locator.issubset(locator_fields):
        raise ReconciliationError("Locator CSV missing required fields")
    if not required_current.issubset(current_fields):
        raise ReconciliationError("current PID CSV missing required fields")

    raw017 = load_raw_shard(raw017_path)
    raw019 = load_raw_shard(raw019_path)
    if not raw017 or not raw019:
        raise ReconciliationError("RAW017 and RAW019 must be non-empty")
    assert_monotonic(raw017, "RAW017")
    assert_monotonic(raw019, "RAW019")

    left_time = create_time(raw017[-1])
    right_time = create_time(raw019[0])
    if left_time >= right_time:
        raise ReconciliationError("invalid sibling temporal boundary")

    current = {row["conversation_pid_sha256"].strip() for row in current_rows}
    historical = {row["Conversation PID (SHA-256)"].strip() for row in locator_rows}
    candidates = historical - current
    if len(candidates) != expected_candidates:
        raise ReconciliationError(
            f"candidate count mismatch: got {len(candidates)}, expected {expected_candidates}"
        )

    locator_by_pid = {
        row["Conversation PID (SHA-256)"].strip(): row
        for row in locator_rows
    }
    candidate_rows = [locator_by_pid[h] for h in candidates]
    outside = []
    for row in candidate_rows:
        t = parse_iso_utc(row["Created UTC"])
        if not (left_time < t < right_time):
            outside.append(row["Conversation PID (SHA-256)"])
    if outside:
        raise ReconciliationError(
            f"{len(outside)} candidate PID hashes fall outside RAW017/RAW019 boundary"
        )

    left_pid = pid_hash(conversation_id(raw017[-1]))
    right_pid = pid_hash(conversation_id(raw019[0]))
    if left_pid not in current or right_pid not in current:
        raise ReconciliationError("sibling boundary PID hashes must be present in current index")
    if left_pid in candidates or right_pid in candidates:
        raise ReconciliationError("sibling boundary PID hash leaked into candidate set")

    candidate_set_sha = commitment_lines(f"{h}\n" for h in sorted(candidates))
    chronological = sorted(
        (row["Created UTC"], row["Conversation PID (SHA-256)"].strip())
        for row in candidate_rows
    )
    candidate_time_sha = commitment_lines(
        f"{timestamp}\t{h}\n" for timestamp, h in chronological
    )

    result: Dict[str, object] = {
        "status": "PASS",
        "classification": "EVIDENCED_RECONCILED_PID_HASH_SET_CURRENT_BYTE_CUSTODY_OPEN",
        "claim_allowed": False,
        "counts": {
            "historical_locator_unique_pids": len(historical),
            "current_index_unique_pids": len(current),
            "reconciled_candidate_pids": len(candidates),
            "candidates_outside_boundary": 0,
        },
        "boundary": {
            "raw017_last_created_utc": iso_utc(left_time),
            "raw019_first_created_utc": iso_utc(right_time),
            "candidate_min_created_utc": min(timestamp for timestamp, _ in chronological),
            "candidate_max_created_utc": max(timestamp for timestamp, _ in chronological),
        },
        "commitments": {
            "candidate_set_sha256": candidate_set_sha,
            "candidate_chronological_sha256": candidate_time_sha,
        },
        "source_digests": {
            "locator_csv_sha256": sha256_file(locator_csv),
            "current_pid_csv_sha256": sha256_file(current_pid_csv),
            "raw017_sha256": sha256_file(raw017_path),
            "raw019_sha256": sha256_file(raw019_path),
        },
        "open_dimensions": [
            "RAW018_CURRENT_PROVIDER",
            "RAW018_CURRENT_BYTES",
            "RAW018_CURRENT_SHA256",
            "RAW018_CURRENT_JSON_PARSE",
        ],
    }

    if archive_zip is not None:
        found: Dict[str, Tuple[float, str]] = {}
        total = 0
        with zipfile.ZipFile(archive_zip) as zf:
            try:
                member_info = zf.getinfo(archive_member)
            except KeyError as exc:
                raise ReconciliationError(f"archive member not found: {archive_member}") from exc
            with zf.open(member_info) as raw:
                text = io.TextIOWrapper(raw, encoding="utf-8")
                for obj in iter_json_array(text):
                    total += 1
                    try:
                        cid = conversation_id(obj)
                    except ReconciliationError:
                        continue
                    h = pid_hash(cid)
                    if h in candidates:
                        canonical = json.dumps(
                            obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
                        ).encode("utf-8")
                        found[h] = (create_time(obj), hashlib.sha256(canonical).hexdigest())

        missing = candidates - found.keys()
        if missing:
            raise ReconciliationError(
                f"historical byte witness missing {len(missing)} candidate PID hashes"
            )

        max_delta = 0.0
        for h, (archive_time, _) in found.items():
            locator_time = parse_iso_utc(locator_by_pid[h]["Created UTC"])
            max_delta = max(max_delta, abs(archive_time - locator_time))
        if max_delta > timestamp_tolerance_seconds:
            raise ReconciliationError(
                f"timestamp witness tolerance exceeded: {max_delta:.9f}s"
            )

        object_witness_sha = commitment_lines(
            f"{h}\t{found[h][1]}\n" for h in sorted(found)
        )
        result["archive_witness"] = {
            "archive_sha256": sha256_file(archive_zip),
            "member": archive_member,
            "member_uncompressed_bytes": member_info.file_size,
            "member_compressed_bytes": member_info.compress_size,
            "archive_total_conversations": total,
            "candidate_pids_found": len(found),
            "candidate_pids_missing": 0,
            "timestamp_agreement_count": len(found),
            "timestamp_max_abs_delta_seconds": round(max_delta, 9),
            "object_witness_sha256": object_witness_sha,
        }

    return result


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--locator-csv", type=Path, required=True)
    p.add_argument("--current-pid-csv", type=Path, required=True)
    p.add_argument("--raw017", type=Path, required=True)
    p.add_argument("--raw019", type=Path, required=True)
    p.add_argument("--expected-candidates", type=int, default=100)
    p.add_argument("--archive-zip", type=Path)
    p.add_argument("--archive-member", default="conversations.json")
    p.add_argument("--timestamp-tolerance-seconds", type=float, default=0.0011)
    p.add_argument("--output", type=Path)
    return p


def main() -> None:
    args = build_parser().parse_args()
    try:
        result = reconcile(
            locator_csv=args.locator_csv,
            current_pid_csv=args.current_pid_csv,
            raw017_path=args.raw017,
            raw019_path=args.raw019,
            expected_candidates=args.expected_candidates,
            archive_zip=args.archive_zip,
            archive_member=args.archive_member,
            timestamp_tolerance_seconds=args.timestamp_tolerance_seconds,
        )
    except ReconciliationError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True))
        raise SystemExit(2)

    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
