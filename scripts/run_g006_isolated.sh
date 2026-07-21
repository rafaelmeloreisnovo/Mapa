#!/usr/bin/env sh
set -eu

ROOT=$(git rev-parse --show-toplevel)
EXPECTED_COMMIT=${1:-$(git -C "$ROOT" rev-parse HEAD)}

case "$EXPECTED_COMMIT" in
  ''|*[!0-9a-f]* )
    printf '%s\n' 'g006-isolated: expected commit must be lowercase hexadecimal' >&2
    exit 2
    ;;
esac

if [ "${#EXPECTED_COMMIT}" -ne 40 ]; then
  printf '%s\n' 'g006-isolated: expected commit must contain 40 characters' >&2
  exit 2
fi

TMP_ROOT=${TMPDIR:-/tmp}
AUDIT_ROOT="$TMP_ROOT/mapa-g006-audit"
OUTPUT_DIR="$AUDIT_ROOT/$EXPECTED_COMMIT"

case "$OUTPUT_DIR" in
  "$ROOT"|"$ROOT"/*)
    printf '%s\n' 'g006-isolated: audit output must remain outside the repository root' >&2
    exit 2
    ;;
esac

if [ -e "$OUTPUT_DIR" ]; then
  printf '%s\n' "g006-isolated: output already exists: $OUTPUT_DIR" >&2
  printf '%s\n' 'use a clean directory or preserve the existing receipt as immutable evidence' >&2
  exit 3
fi

umask 077
mkdir -p "$AUDIT_ROOT"

exec python3 "$ROOT/scripts/run_g006_local_gate.py" \
  --root "$ROOT" \
  --output-dir "$OUTPUT_DIR" \
  --expected-commit "$EXPECTED_COMMIT"
