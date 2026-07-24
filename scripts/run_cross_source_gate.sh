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
export PYTHONPYCACHEPREFIX="$OUTPUT_DIR/pycache"
cd "$ROOT"

for artifact in \
  cross-source-test-validation.json \
  cross-source-record-validation.json \
  cross-source-registry-validation.json \
  chain-of-custody-validation.json \
  quality-floor-validation.json \
  LOCAL_GATE_STATUS.json \
  CHECKSUMS.sha256
do
  if [ -e "$OUTPUT_DIR/$artifact" ]; then
    rm -f "$OUTPUT_DIR/$artifact"
  fi
done

printf '%s\n' "[1/9] Compile validators, evaluators, comparator and tests"
python3 -m py_compile \
  scripts/validate_cross_source_records.py \
  scripts/validate_cross_source_registry.py \
  scripts/validate_chain_of_custody.py \
  scripts/run_cross_source_tests.py \
  scripts/evaluate_cross_source_gate.py \
  scripts/compare_cross_source_evidence.py \
  tests/test_cross_source_records.py \
  tests/test_cross_source_registry.py \
  tests/test_cross_source_local_gate_contract.py \
  tests/test_cross_source_gate_evaluator.py \
  tests/test_cross_source_test_runner.py \
  tests/test_compare_cross_source_evidence.py \
  tests/test_validate_chain_of_custody.py

printf '%s\n' "[2/9] Parse schema, floor and fixtures"
python3 -m json.tool schemas/cross-source-record.schema.json >/dev/null
python3 -m json.tool indices/CROSS_SOURCE_GATE_FLOOR.json >/dev/null
for fixture in tests/fixtures/cross_source/valid/*.json; do
  python3 -m json.tool "$fixture" >/dev/null
done
for fixture in tests/fixtures/cross_source/invalid/*.json; do
  python3 -m json.tool "$fixture" >/dev/null
done

printf '%s\n' "[3/9] Parse JSONL registries"
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

printf '%s\n' "[4/9] Run and measure canonical adversarial tests"
python3 scripts/run_cross_source_tests.py \
  --write-report "$OUTPUT_DIR/cross-source-test-validation.json"

printf '%s\n' "[5/9] Produce cross-source validation reports"
python3 scripts/validate_cross_source_records.py \
  --write-report "$OUTPUT_DIR/cross-source-record-validation.json"
python3 scripts/validate_cross_source_registry.py \
  --write-report "$OUTPUT_DIR/cross-source-registry-validation.json"

printf '%s\n' "[6/9] Validate and report append-only custody chain"
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

printf '%s\n' "[7/9] Evaluate measured results against growth-safe floor"
python3 scripts/evaluate_cross_source_gate.py \
  --floor indices/CROSS_SOURCE_GATE_FLOOR.json \
  --records-report "$OUTPUT_DIR/cross-source-record-validation.json" \
  --registry-report "$OUTPUT_DIR/cross-source-registry-validation.json" \
  --custody-report "$OUTPUT_DIR/chain-of-custody-validation.json" \
  --test-report "$OUTPUT_DIR/cross-source-test-validation.json" \
  --write-report "$OUTPUT_DIR/quality-floor-validation.json"

printf '%s\n' "[8/9] Enforce non-promotion and append-only boundaries"
OUTPUT_DIR="$OUTPUT_DIR" python3 - <<'PY'
import json
import os
from pathlib import Path

output_dir = Path(os.environ["OUTPUT_DIR"])
floor = json.loads(
    Path("indices/CROSS_SOURCE_GATE_FLOOR.json").read_text(encoding="utf-8")
)
records = json.loads(
    (output_dir / "cross-source-record-validation.json").read_text(encoding="utf-8")
)
registry = json.loads(
    (output_dir / "cross-source-registry-validation.json").read_text(encoding="utf-8")
)
custody = json.loads(
    (output_dir / "chain-of-custody-validation.json").read_text(encoding="utf-8")
)
tests = json.loads(
    (output_dir / "cross-source-test-validation.json").read_text(encoding="utf-8")
)
quality = json.loads(
    (output_dir / "quality-floor-validation.json").read_text(encoding="utf-8")
)
minimums = floor["minimums"]

assert records["status"] == "PASS"
assert records["unexpected_failures"] == 0
assert records["unexpected_passes"] == 0
assert records["claim_allowed"] is False

assert registry["status"] == "PASS"
assert registry["record_count"] >= minimums["registry_records"]
for provider, required in minimums["provider_counts"].items():
    assert registry["provider_counts"].get(provider, 0) >= required
assert registry["defect_count"] == 0
assert registry["claim_allowed"] is False

assert custody["status"] == "PASS"
assert custody["event_count"] >= minimums["custody_events"]
assert custody["defect_count"] == 0
assert custody["claim_allowed"] is False

assert tests["status"] == "PASS"
assert tests["tests_run"] >= minimums["tests_run"]
assert tests["failures"] == 0
assert tests["errors"] == 0
assert tests["claim_allowed"] is False
assert tests["remote_ci_substituted"] is False

assert quality["status"] == "PASS"
assert quality["failed_check_count"] == 0
assert quality["promotion_state"] == "LOCAL_PASS_REMOTE_TOKEN_VAZIO"
assert quality["claim_allowed"] is False
assert quality["remote_ci_substituted"] is False
PY

printf '%s\n' "[9/9] Seal local evidence"
OUTPUT_DIR="$OUTPUT_DIR" python3 - <<'PY'
import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path.cwd()
output_dir = Path(os.environ["OUTPUT_DIR"])
report_names = [
    "cross-source-test-validation.json",
    "cross-source-record-validation.json",
    "cross-source-registry-validation.json",
    "chain-of-custody-validation.json",
    "quality-floor-validation.json",
]
checksums = []
for name in report_names:
    path = output_dir / name
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    checksums.append({"path": name, "sha256": digest})

floor_path = root / "indices" / "CROSS_SOURCE_GATE_FLOOR.json"
floor = json.loads(floor_path.read_text(encoding="utf-8"))
tests = json.loads(
    (output_dir / "cross-source-test-validation.json").read_text(encoding="utf-8")
)
quality = json.loads(
    (output_dir / "quality-floor-validation.json").read_text(encoding="utf-8")
)
manifest = {
    "schema_version": "rafaelia.cross-source-local-gate/v2",
    "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "python_version": sys.version.split()[0],
    "platform": platform.platform(),
    "status": "PASS",
    "test_count_observed": tests["tests_run"],
    "test_file_count": tests["test_file_count"],
    "minimum_test_count": floor["minimums"]["tests_run"],
    "report_count": len(checksums),
    "checksums": checksums,
    "quality_floor": {
        "path": floor_path.relative_to(root).as_posix(),
        "schema_version": floor["schema_version"],
        "sha256": hashlib.sha256(floor_path.read_bytes()).hexdigest(),
        "status": quality["status"],
    },
    "quality_floor_status": quality["status"],
    "promotion_state": quality["promotion_state"],
    "claim_allowed": False,
    "remote_ci_substituted": False,
    "next_verifiable_step": (
        "Restore the remote runner, then compare both bundles with "
        "scripts/compare_cross_source_evidence.py."
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

printf '%s\n' "PASS: local cross-source, custody and growth-safe quality gate"
printf '%s\n' "Evidence: $OUTPUT_DIR"
