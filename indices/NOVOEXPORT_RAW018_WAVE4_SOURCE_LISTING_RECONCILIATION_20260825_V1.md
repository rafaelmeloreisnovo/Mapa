# NOVOEXPORT RAW018 — Wave4 Source Listing Reconciliation — 2026-08-25

State: `HISTORICAL_SOURCE_LISTING_COHERENCE_PASS / CURRENT_BYTE_CUSTODY_OPEN`  
`claim_allowed=false` · `release_allowed=false`

Parent: `NOVOEXPORT_RAW018_WAVE4_EVOLUTION_X_20260825_V1`.

## Exact witness

`temp.locate.txt` was re-read as exact bytes:

- bytes: `1,396,867`;
- SHA-256: `7e291744e7522eeb4a4ce4f843f55ef479205de8305ac126130ff6c5631682bf`;
- parsed file entries: `15,437`;
- raw018 line: `-rw-rw----. 1 root everybody  12115336 Aug  3 05:35 conversations-018.json`.

This directly evidences that a source-directory snapshot listed raw018 as a 12,115,336-byte file. It does not expose the JSON bytes.

## Full reconciliation against active manifest

Exact active `export_manifest.json`:

- bytes: `3,812,404`;
- SHA-256: `38bb97724a432420328a322eb27ff1af9de28201c2857448e62d2b2e3a36df4a`;
- physical entries: `15,439`.

Reconciliation:

```text
common paths                     15,435
common path-size mismatches           0
manifest-only paths                   4
listing-only paths                    2
```

The four manifest-only paths are `.dat` objects. The two listing-only paths are `export_manifest.json` and `temp.locate.txt`.

Therefore:

`NEAR_COMPLETE_PATH_SIZE_SNAPSHOT_COHERENCE = PASS`.

It is deliberately **not** promoted to total snapshot equality.

## Conversation family

For `conversations-000.json..conversations-050.json`:

```text
manifest paths                  51
listing paths                   51
common paths                    51
path-size mismatches             0
manifest aggregate   1,107,289,897 bytes
listing aggregate    1,107,289,897 bytes
```

So:

`CONVERSATION_FAMILY_51_OF_51_PATH_SIZE_COHERENCE = PASS`.

Raw018 itself is present in both snapshots at `12,115,336` bytes.

## Boundary

```text
HISTORICAL_FILESYSTEM_LISTING != RAW_CONTENT_BYTES
PATH_SIZE_COHERENCE != CONTENT_SHA256_EQUALITY
51_OF_51_PATH_SIZE_MATCH != CURRENT_PROVIDER_CUSTODY
LISTING_TIMESTAMP != CONTENT_VERSION_PROOF
NEAR_COMPLETE_SNAPSHOT != TOTAL_SNAPSHOT_EQUALITY
TOKEN_VAZIO != 0
```

Still `TOKEN_VAZIO`: current provider, exact current/immutable raw018 bytes, content SHA-256, current JSON parse/cardinality and equality of a PID commitment recomputed from the recovered raw bytes.

## F_next

Trace the producer/source command or container that created this source directory/manifest. If an immutable raw018 copy is recovered, require:

`12,115,336 bytes -> SHA256 -> JSON parse -> PID commitment == 766644f8a199de4317500e6f40d44f9187f767e2ea453910ab4a4d0ec8cfc69e`.
