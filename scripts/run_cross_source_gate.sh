#!/usr/bin/env sh
# Offline, dependency-free entry point for the RAFAELIA cross-source gate.
# Invoke explicitly with: sh scripts/run_cross_source_gate.sh [output-directory]

set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
OUTPUT_DIR=${1:-"$ROOT/.artifacts/cross-source-local"}

fail() {
  printf '%s\n' "ERROR: $*" >&2
  exit 1
}

command -v python3 >/dev/null 2>&1 || fail "python3 is required"
mkdir -p "$OUTPUT_DIR"
cd "$ROOT"

printf '%s\n' "[1/7] Compile validators and tests"
python3 -m py_compile \
  scripts/validate_cross_source_records.py \
  scripts/validate_cross_source_registry.py \
  tests/test_cross_source_records.py \
  tests/test_cross_source_registry.py

printf '%s\n' "[2/7] Parse schema and fixtures"
python3 -m json.tool schemas/cross-source-record.schema.json >/dev/null
for fixture in tests/fixtures/cross_source/valid/*.json; do
  python3 -m json.tool "$fixture" >/dev/null
done
for fixture in tests/fixtures/cross_source/invalid/*.json; do
  python3 -m json.tool "$fixture" >/dev/null
done

printf '%s\n' "[3/7] Parse JSONL registry"
python3 - <<'PY'
import json
from pathlib import Path

path = Path("indices/CROSS_SOURCE_REGISTRY.jsonl")
count = 0
for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
    if not raw.strip():
        continue
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise SystemExit(f"line {line_number}: registry entry must be an object")
    count += 1
if count == 0:
    raise SystemExit("registry is empty")
print(f"registry_records={count}")
PY

printf '%s\n' "[4/7] Run adversarial tests"
python3 -m unittest \
  tests/test_cross_source_records.py \
  tests/test_cross_source_registry.py \
  -v

printf '%s\n' "[5/7] Produce deterministic validation reports"
python3 scripts/validate_cross_source_records.py \
  --write-report "$OUTPUT_DIR/cross-source-record-validation.json"
python3 scripts/validate_cross_source_registry.py \
  --write-report "$OUTPUT_DIR/cross-source-registry-validation.json"

printf '%s\n' "[6/7] Enforce non-promotion boundary"
OUTPUT_DIR="$OUTPUT_DIR" python3 - <<'PY'
import json
import os
from pathlib import Path

output_dir = Path(os.environ["OUTPUT_DIR"])
records = json.loads(
    (output_dir / "cross-source-record-validation.json").read_text(encoding="utf-8")
)
registry = json.loads(
    (output_dir / "cross-source-registry-validation.json").read_text(encoding="utf-8")
)

assert records["status"] == "PASS"
assert records["valid_fixture_count"] >= 2
assert records["invalid_fixture_count"] >= 1
assert records["unexpected_failures"] == 0
assert records["unexpected_passes"] == 0
assert records["claim_allowed"] is False

assert registry["status"] == "PASS"
assert registry["record_count"] == 10
assert registry["provider_counts"] == {"github": 2, "google_drive": 8}
assert registry["token_vazio_count"] == 1
assert registry["defect_count"] == 0
assert registry["claim_allowed"] is False
PY

printf '%s\n' "[7/7] Seal local evidence"
OUTPUT_DIR="$OUTPUT_DIR" python3 - <<'PY'
import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

output_dir = Path(os.environ["OUTPUT_DIR"])
report_names = [
    "cross-source-record-validation.json",
    "cross-source-registry-validation.json",
]
checksums = []
for name in report_names:
    path = output_dir / name
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    checksums.append({"path": name, "sha256": digest})

manifest = {
    "schema_version": "rafaelia.cross-source-local-gate/v1",
    "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "python_version": sys.version.split()[0],
    "platform": platform.platform(),
    "status": "PASS",
    "report_count": len(checksums),
    "checksums": checksums,
    "claim_allowed": False,
    "remote_ci_substituted": False,
    "next_verifiable_step": (
        "Restore GitHub Actions runner startup and reproduce the same PASS remotely."
    ),
}
(output_dir / "LOCAL_GATE_STATUS.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
(output_dir / "CHECKSUMS.sha256").write_text(
    "".join(f"{item['sha256']}  {item['path']}\n" for item in checksums),
    encoding="utf-8",
)
print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
PY

printf '%s\n' "PASS: local cross-source gate"
printf '%s\n' "Evidence: $OUTPUT_DIR"
