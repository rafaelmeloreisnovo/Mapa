# NOVOexport Raw 018 — Wave 2 — 2026-08-24

Status: `PARTIAL_EVIDENCED_PHYSICAL_INVENTORY_PROVIDER_UNBOUND`  
Claim: `claim_allowed=false`

## What changed

`TV-RAW-018-CURRENT-ID` is no longer treated as if raw shard 018 itself were unevidenced.

Two independent NOVOexport evidence planes agree on the same raw member:

- `export_manifest.json` → `conversations-018.json` → `12,115,336` bytes;
- `temp.locate.txt` → physical inventory entry `conversations-018.json` → `12,115,336` bytes.

Therefore:

`RAW018_EXISTENCE + PATH + HISTORICAL_SIZE = EVIDENCED`

The remaining uncertainty is narrower:

`DIRECT_PROVIDER + RAW_BYTES + RAW_SHA256 + JSON_PARSE + PID_SET = TOKEN_VAZIO`

## Anti-substitution

`MESSAGES-00018.jsonl.txt` is a derived shard and must not stand in for `conversations-018.json`.

Invariant:

`DERIVED_ORDINAL != RAW_SOURCE_ORDINAL`

## Evidence artifact

Machine-readable evidence:

`data/evidence/novoexport_raw018_wave2_20260824.v1.json`

Validator:

`tools/validate_novoexport_raw018_wave2.py`

Dedicated gate:

`.github/workflows/novoexport-raw018-wave2.yml`

## Next gate

Recover the original export container/provider that holds the raw member, then:

- extract/stream exactly `conversations-018.json`;
- require byte length `12,115,336`;
- compute SHA-256;
- parse JSON fail-closed;
- enumerate exact conversation/PID set;
- compare with the historical unmatched candidate set;
- emit an append-only custody receipt.

## R3

**F_ok:** raw018 existence, path and byte size are now supported by two independent NOVOexport planes.

**F_gap:** directly addressable provider, current raw byte stream, raw SHA-256, parse result and PID set remain `TOKEN_VAZIO`.

**F_next:** recover the export container/member bytes; do not substitute derived ordinal 00018.
