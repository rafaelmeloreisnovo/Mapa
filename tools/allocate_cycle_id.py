#!/usr/bin/env python3
import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

REQUIRED = ("cycle_id", "artifact_role", "provider_id")


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


def allocate(registry: Path, cycle_id: str, artifact_role: str, provider_id: str):
    values = {"cycle_id": cycle_id, "artifact_role": artifact_role, "provider_id": provider_id}
    missing = [k for k, v in values.items() if not _nonempty(v)]
    if missing:
        return 2, f"REJECT missing/empty: {','.join(missing)}"

    lock = registry.with_name(registry.name + ".lock")
    lock_fd = None
    try:
        try:
            lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
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
        if lock_fd is not None:
            try:
                os.close(lock_fd)
            finally:
                try:
                    os.unlink(lock)
                except FileNotFoundError:
                    pass


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
