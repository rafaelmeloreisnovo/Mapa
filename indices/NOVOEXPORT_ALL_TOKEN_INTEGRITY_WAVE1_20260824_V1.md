# NOVOexport — ALL_TOKEN Integrity Wave 1 — 2026-08-24

State: `PARTIAL_EVIDENCE_MATERIALIZED`  
Policy: `APPEND_ONLY | PROVENANCE_FIRST | NO_SILENT_REWRITE | TOKEN_VAZIO_VALID`  
`claim_allowed=false`

## Materialized delta

The previous `TV-TOKEN-OCCURRENCE-OFFBY1` uncertainty is now split into two dimensions:

- **artifact location:** evidenced;
- **generator/code root cause:** still `TOKEN_VAZIO`.

Private V1 detailed stores were materialized transiently and reconciled by immutable SHA-256 identity. No private raw/token content is committed here.

## Reproduction

| Plane | Result |
|---|---:|
| `sum(tokens_literal.count_total)` | `44,185,627` |
| `sum(token_source_counts.count)` | `44,185,627` |
| `sum(source_manifest.token_occurrences)` | `44,185,627` |
| embedded `manifest.source_manifest` sum | `44,185,627` |
| `manifest.token_occurrences_total_raw` | `44,185,626` |
| per-literal mismatches | `0` |
| per-source mismatches | `0` |
| scalar delta | `-1` |

Therefore:

```text
DETAILED_STORES = CONSISTENT(44,185,627)
MANIFEST_SCALAR = 44,185,626
STATE = MANIFEST_AGGREGATE_DRIFT
GENERATOR_ROOT_CAUSE = TOKEN_VAZIO_NOT_LOCATED
```

The frozen V1 is not rewritten. Any correction must be an errata or rebuildable V2 with a differential gate.

## Shard 018

Preserved facts:

- historical `conversations-018.json` size: `12,115,336` bytes;
- 100 historical PIDs remain unjoined, but equality of cardinality is not identity proof;
- a derived `MESSAGES-00018` was previously proved to reference `conversations-012.json`, therefore **derived ordinal 00018 != raw shard 018**;
- a bounded exact-name Drive query did not expose a current raw provider; absence from that query is not file-absence evidence.

State remains `TOKEN_VAZIO_CURRENT_PROVIDER`.

## Chunk lineage

Current ALL_TOKEN provenance closes source bytes/hash/counts, but not the full graph:

```text
source_ref
  -> conversation_id/PID
  -> message_id/node_id
  -> attachment_id/file_id
  -> record_sha256
  -> chunk_id/chunk_sha256
```

The previously observed chunk trees remain scoped as prototype/partial upload. They must not be promoted to full corpus lineage.

## New executable support

- `tools/reconcile_all_token_aggregate.py`
- `tests/test_reconcile_all_token_aggregate.py`
- `data/evidence/novoexport_all_token_integrity_wave1_20260824.v1.json`

The reconciler fails closed on detailed-store divergence and distinguishes manifest-only drift from store corruption.

## F_ok

- off-by-one reproduced from exact private V1 artifact hashes;
- detailed stores agree exactly;
- drift localized to the manifest scalar projection;
- raw018 anti-substitution invariant preserved;
- chunk-lineage missing dimensions typed.

## F_gap

- generator statement/path producing `44,185,626` is not located;
- current provider/bytes/hash/PIDs of raw018 remain unresolved;
- global message/node/file/chunk lineage remains unresolved.

## F_next

`generator path -> raw018 provider -> stable-ID chunk lineage -> incremental receipts`
