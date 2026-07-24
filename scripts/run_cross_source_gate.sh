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

printf '%s\n' "[1/8] Compile validators and tests"
python3 -m py_compile \
  scripts/validate_cross_source_records.py \
  scripts/validate_cross_source_registry.py \
  scripts/validate_chain_of_custody.py \
  tests/test_cross_source_records.py \
  tests/test_cross_source_registry.py \
  tests/test_cross_source_local_gate_contract.py \
  tests/test_validate_chain_of_custody.py

printf '%s\n' "[2/8] Parse schema and fixtures"
python3 -m json.tool schemas/cross-source-record.schema.json >/dev/null
for fixture in tests/fixtures/cross_source/valid/*.json; do
  python3 -m json.tool "$fixture" >/dev/null
done
for fixture in tests/fixtures/cross_source/invalid/*.json; do
  python3 -m json.tool "$fixture" >/dev/null
done

printf '%s\n' "[3/8] Parse JSONL registries"
python3 - <<'PY'
import json
from pathlib import Path

for path_text in (
    "indices/CROSS_SOURCE_REGISTRY.jsonl",
    "indices/CADEIA_CUSTODIA_EVENTOS.jsonl",
):
    path = Path(path_text)
    count = 0
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise SystemExit(f"{path}: line {line_number} must be an object")
        count += 1
    if count == 0:
        raise SystemExit(f"{path}: empty JSONL")
    print(f"{path_text}={count}")
PY

printf '%s\n' "[4/8] Run adversarial, custody and local-gate tests"
python3 -m unittest \
  tests/test_cross_source_records.py \
  tests/test_cross_source_registry.py \
  tests/test_cross_source_local_gate_contract.py \
  tests/test_validate_chain_of_custody.py \
  -v

printf '%s\n' "[5/8] Produce cross-source validation reports"
python3 scripts/validate_cross_source_records.py \
  --write-report "$OUTPUT_DIR/cross-source-record-validation.json"
python3 scripts/validate_cross_source_registry.py \
  --write-report "$OUTPUT_DIR/cross-source-registry-validation.json"

printf '%s\n' "[6/8] Validate and report append-only custody chain"
OUTPUT_DIR="$OUTPUT_DIR" python3 - <<'PY'
import importlib.util
import json
import os
from pathlib import Path

root = Path.cwd()
module_path = root / "scripts" / "validate_chain_of_custody.py"
spec = importlib.util.spec_from_file_location("custody_validator", module_path)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

ledger = root / "indices" / "CADEIA_CUSTODIA_EVENTOS.jsonl"
count, defects = validator.validate_ledger(ledger, root)
report = {
    "schema_version": "rafaelia.custody-validation-report/v1",
    "ledger": ledger.relative_to(root).as_posix(),
    "status": "PASS" if not defects else "FAIL",
    "event_count": count,
    "defect_count": len(defects),
    "defects": defects,
    "claim_allowed": False,
    "next_verifiable_step": (
        "Append a VALIDATE event after remote GitHub Actions becomes observable."
        if not defects
        else "Correct custody defects without rewriting valid historical events."
    ),
}
output = Path(os.environ["OUTPUT_DIR"])
(output / "chain-of-custody-validation.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
if defects:
    raise SystemExit("custody ledger validation failed")
PY

printf '%s\n' "[7/8] Enforce non-promotion boundary"
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
custody = json.loads(
    (output_dir / "chain-of-custody-validation.json").read_text(encoding="utf-8")
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

assert custody["status"] == "PASS"
assert custody["event_count"] >= 13
assert custody["defect_count"] == 0
assert custody["claim_allowed"] is False
PY

printf '%s\n' "[8/8] Seal local evidence"
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
    "chain-of-custody-validation.json",
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
    "test_count_expected": 38,
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

printf '%s\n' "PASS: local cross-source and custody gate"
printf '%s\n' "Evidence: $OUTPUT_DIR"
