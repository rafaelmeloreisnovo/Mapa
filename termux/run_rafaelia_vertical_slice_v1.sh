#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
SOURCE_ROOT="${1:-/sdcard/Download}"
RECEIPT_OUT="$ROOT/receipts/vertical_slice/RECEIPT-VSLICE-001.termux.json"

command -v python3 >/dev/null 2>&1 || {
  echo "FAIL: python3 unavailable" >&2
  exit 127
}
command -v sha256sum >/dev/null 2>&1 || {
  echo "FAIL: sha256sum unavailable" >&2
  exit 127
}

python3 "$ROOT/scripts/run_vertical_slice_v1.py" \
  --source-root "$SOURCE_ROOT" \
  --repository-root "$ROOT" \
  --runtime-class ANDROID_TERMUX_LOCAL \
  --receipt-out "$RECEIPT_OUT"

sha256sum "$RECEIPT_OUT" > "$RECEIPT_OUT.sha256"
printf 'RECEIPT=%s\n' "$RECEIPT_OUT"
printf 'RECEIPT_SHA256_FILE=%s\n' "$RECEIPT_OUT.sha256"
