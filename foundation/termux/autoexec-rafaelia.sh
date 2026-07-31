#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
RUNNER="$ROOT/.rafaelia/tools/rafaelia_foundation.py"

command -v python3 >/dev/null 2>&1 || {
  printf '%s\n' "TOKEN_VAZIO_TOOL_MISSING: python3" >&2
  exit 127
}
[ -f "$RUNNER" ] || {
  printf '%s\n' "TOKEN_VAZIO_MANIFEST_MISSING: run Foundation init from Mapa first" >&2
  exit 2
}

exec python3 "$RUNNER" "$@" --repo-root "$ROOT"
