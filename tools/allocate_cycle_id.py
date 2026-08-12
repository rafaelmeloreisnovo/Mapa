#!/usr/bin/env python3
import argparse
import fcntl
import json
import os
import socket
import sys
import tempfile
import time
from pathlib import Path

REQUIRED = ("cycle_id", "artifact_role", "provider_id")
LOCK_VERSION = 2


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def _load_registry(path: Path):
    if not path.exists():
        return {"version": 1, "records": []}
    try:
        with path.open("r", encoding="utf-8") as f:
            doc = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"registry unreadable: {exc}") from exc
    records = doc.get("records")
    if not isinstance(records, list):
        raise RuntimeError("registry records must be a list")
    return doc


def _validate_existing(records):
    seen = {}
    for i, rec in enumerate(records):
        if not isinstance(rec, dict):
            raise RuntimeError(f"records[{i}] must be object")
        missing = [k for k in REQUIRED if not _nonempty(rec.get(k))]
        if missing:
            raise RuntimeError(f"records[{i}] missing/empty: {','.join(missing)}")
        key = (rec["cycle_id"], rec["artifact_role"])
        prior = seen.get(key)
        if prior is None:
            seen[key] = rec["provider_id"]
        elif prior != rec["provider_id"]:
            raise RuntimeError(
                f"existing conflicting provider for cycle_id={key[0]} "
                f"artifact_role={key[1]}: {prior} != {rec['provider_id']}"
            )


def _atomic_write_json(path: Path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump(doc, f, indent=2, sort_keys=True, ensure_ascii=False)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
        try:
            dfd = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(dfd)
            finally:
                os.close(dfd)
        except OSError:
            pass
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def _write_lock_metadata(lock_file):
    owner = {
        "version": LOCK_VERSION,
        "pid": os.getpid(),
        "hostname": socket.gethostname(),
        "acquired_unix_ns": time.time_ns(),
    }
    lock_file.seek(0)
    lock_file.truncate(0)
    json.dump(owner, lock_file, sort_keys=True, separators=(",", ":"))
    lock_file.write("\n")
    lock_file.flush()
    os.fsync(lock_file.fileno())


def _acquire_lock(lock: Path):
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock_file = lock.open("a+", encoding="utf-8", newline="\n")
    try:
        try:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            lock_file.close()
            return None
        _write_lock_metadata(lock_file)
        return lock_file
    except Exception:
        lock_file.close()
        raise


def allocate(registry: Path, cycle_id: str, artifact_role: str, provider_id: str):
    values = {"cycle_id": cycle_id, "artifact_role": artifact_role, "provider_id": provider_id}
    missing = [k for k, v in values.items() if not _nonempty(v)]
    if missing:
        return 2, f"REJECT missing/empty: {','.join(missing)}"

    lock = registry.with_name(registry.name + ".lock")
    lock_file = None
    try:
        lock_file = _acquire_lock(lock)
        if lock_file is None:
            return 3, "REJECT lock-busy"

        doc = _load_registry(registry)
        records = doc["records"]
        _validate_existing(records)

        key = (cycle_id, artifact_role)
        matches = [r for r in records if (r["cycle_id"], r["artifact_role"]) == key]
        if matches:
            provider = matches[0]["provider_id"]
            if provider == provider_id:
                return 0, "PASS idempotent"
            return 4, f"REJECT conflicting-provider existing={provider} requested={provider_id}"

        records.append(values)
        _atomic_write_json(registry, doc)
        return 0, "PASS allocated"
    except RuntimeError as exc:
        return 5, f"REJECT {exc}"
    except OSError as exc:
        return 6, f"REJECT io-error: {exc}"
    finally:
        if lock_file is not None:
            try:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            finally:
                lock_file.close()


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("registry")
    p.add_argument("cycle_id")
    p.add_argument("artifact_role")
    p.add_argument("provider_id")
    ns = p.parse_args(argv)
    code, message = allocate(Path(ns.registry), ns.cycle_id, ns.artifact_role, ns.provider_id)
    print(message)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
