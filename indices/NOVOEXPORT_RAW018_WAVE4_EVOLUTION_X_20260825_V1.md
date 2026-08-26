# NOVOEXPORT RAW018 — WAVE 4 — X=EVOLUÇÃO — 2026-08-25

State: `ACTIVE_G2_MEMBERSHIP_AND_BATCH_COHERENCE_EVIDENCED_CURRENT_BYTE_CUSTODY_OPEN`  
`claim_allowed=false` · `release_allowed=false`

Direct predecessor: `NOVOEXPORT_RAW018_WAVE3_PID_RECONCILIATION_20260824_V1` (merged in `3ab1eb3a596148e616f0e2d134f2cc8b71b0fafe`).  
Lineage: Wave2 → Wave3 → Wave4.

## Route selected by X

The Stage0 compiler/event baseline is already merged. The NOVOexport custody chain is therefore first priority.

The active authority is not the legacy byte-chunk corpus. It is:

```text
Google Drive NOVOexport
  -> exact export_manifest.json
  -> novoexport_g2_38bb97724a432420
  -> conversations-000.json .. conversations-050.json
```

The exact active manifest was re-read at byte level:

- bytes: `3,812,404`;
- SHA-256: `38bb97724a432420328a322eb27ff1af9de28201c2857448e62d2b2e3a36df4a`;
- raw018 entry: `{path: conversations-018.json, size_bytes: 12115336}`;
- the entry has no provider ID and no content SHA field.

Therefore the manifest closes active logical membership and declared size, **not** current raw-byte custody.

## X axes

| Axis | Evolution |
|---|---|
| `ATLAS` | Selected the highest-dependency unresolved raw source edge after rereading closed predecessor evidence. |
| `NOVO` | Uses the exact active NOVOexport manifest/G2 generation; no fallback to legacy chunks. |
| `L` | Wave2 existence/size + Wave3 PID commitment are preserved; Wave4 only appends. |
| `O` | Active membership, provider, bytes, parse/cardinality, PID commitment, raw-derived commitment match and message projection are separate axes. |
| `T` | Exact manifest ↔ G2 generation ↔ batch-00014 ↔ observed raw017/019/020 ↔ Wave3 PID commitment. |
| `REL` | Adds generation and batch edges without converting them into provider/byte claims. |
| `SCALE` | META authority → generation → batch → shard → conversation identity → future message/node/token. |
| `EVID` | Only byte hashes, manifest records, batch commitments, observed neighbors and merged commitments are promoted. |
| `GAP` | Current provider/bytes/SHA/parse/cardinality/raw-derived PID equality remain `TOKEN_VAZIO`. |
| `LEARN` | Generation membership and arithmetic coherence are routing/provenance evidence, not byte custody. |

## Preserved Wave3 identity evidence

```text
RAW018_PID_HASH_SET = EVIDENCED_RECONCILED_100_PRIVACY_PRESERVING
candidate_count = 100
candidate_set_sha256 = 766644f8a199de4317500e6f40d44f9187f767e2ea453910ab4a4d0ec8cfc69e
candidate_chronological_sha256 = c29cbc493b2401d0d875a49a71999f4b32f8b3faab8a86cd2c1d9a4e4ca83706
historical_object_witness_sha256 = f14cd8767241255d64dba51b818e1bf3d5eefb6af157f1b321199cb102223156
```

Invariant:

```text
PID_HASH_SET_EVIDENCE != CURRENT_RAW_BYTE_CUSTODY
```

## Active G2 generation bridge

The private producer-side generation metadata independently establishes:

- `generation_id = novoexport_g2_38bb97724a432420`;
- source authority = exact active manifest;
- conversation shards = `51`;
- declared conversation-family bytes = `1,107,289,897`;
- raw bodies remain under Drive custody;
- legacy chunks are predecessor only.

The generation's exact-source receipt set contains `11` exact receipts at its snapshot. It includes raw019/raw020 but has **no raw018 exact receipt**. Thus raw018's provider/hash gap already exists at producer-generation level; it is not created by the Mapa projection.

## Batch-00014 transversal coherence

G2 `batch-00014` declares:

```text
first_path = conversations-017.json
last_path = conversations-020.json
record_count = 4
declared_source_bytes = 64,541,017
record_sha256 = f78a9c9b866c351a1257281a9f771b6713b1d363a30e70e77d7186c177c72c7e
records_payload_sha256 = 1eef0ce092d92fd6f6affd1821472b5c1ebde0daee9583726691ad5e14815a88
```

Crossing independent evidence:

```text
raw017 observed bytes          22,560,934
raw018 manifest declared       12,115,336
raw019 observed bytes          16,440,670
raw020 observed bytes          13,424,077
                              ----------
SUM                            64,541,017
batch-00014 declared           64,541,017
```

Result:

```text
TRANSVERSAL_DECLARED_BYTE_COHERENCE = PASS
```

But:

```text
BATCH_SUM_AGREEMENT != RAW018_BYTE_CUSTODY
ACTIVE_GENERATION_MEMBERSHIP != PROVIDER_IDENTITY
MANIFEST_DECLARED_SIZE != OBSERVED_CURRENT_BYTES
```

No SHA, current provider or JSON parse is inferred from the equality.

## Historical candidate falsifier

A plausible historical export archive was read byte-for-byte:

- size `187,756,731`;
- SHA-256 `04ca4578dc2990e740001d9e49c3bdb229b1599bdf44dd366ec9ed19290c2ecb`;
- contains monolithic `conversations.json` but no direct `conversations-018.json`.

Its monolith contains the first current raw017 conversation ID but not raw017-last nor raw019-first. It is rejected as both a direct raw018 container and a complete source for the current 017–019 range.

```text
MONOLITH_OVERLAP != COMPLETE_SHARD_SOURCE
CANDIDATE_TEMPORAL_AFFINITY != PROVIDER_IDENTITY
```

## Gap state

`TV-RAW-018-CURRENT-ID` is now more precisely:

`PARTIAL_EVIDENCED_ACTIVE_MEMBERSHIP_PID_SET_CURRENT_BYTE_CUSTODY_OPEN`.

Closed/preserved:

- existence/path/declared size;
- active G2 logical membership;
- exact batch membership and declared-byte coherence;
- privacy-preserving 100-PID commitment.

Still open:

- current provider/file identity;
- exact current or immutable raw bytes;
- raw SHA-256;
- current JSON parse/cardinality;
- PID commitment recomputed from current raw bytes == preserved Wave3 commitment;
- original shard-construction provenance for `conversations-000..050` (distinct from G2 batch grouping).

## Next gate

1. Trace the **original shard-construction provenance** for `conversations-000..050`; do not confuse it with G2 batching.
2. Use provider/container aliases only when linked by that provenance.
3. Obtain exact raw018 current/immutable bytes.
4. Require exactly `12,115,336` bytes.
5. SHA-256 exact bytes.
6. JSON parse fail-closed and observe current cardinality.
7. Compute privacy-preserving PID commitment from those bytes.
8. Require exactly `766644f8a199de4317500e6f40d44f9187f767e2ea453910ab4a4d0ec8cfc69e`.
9. Append receipt.
10. Then expand `source_ref → conversation_id → message_id/node_id → file_id → record_sha256` and semantic/vector promotion.

## Anti-regression

```text
PID_HASH_SET_EVIDENCE != CURRENT_RAW_BYTE_CUSTODY
ACTIVE_GENERATION_MEMBERSHIP != PROVIDER_IDENTITY
BATCH_SUM_AGREEMENT != RAW018_BYTE_CUSTODY
MANIFEST_DECLARED_SIZE != OBSERVED_CURRENT_BYTES
NEIGHBOR_CARDINALITY != CURRENT_RAW018_CARDINALITY
RECONSTRUCTION != OBSERVED_RAW_SOURCE
DERIVED_ORDINAL != RAW_SOURCE_ORDINAL
TOKEN_VAZIO != 0
```

## Files

- `data/evidence/novoexport_raw018_wave4_evolution_x_20260825.v1.json`
- `tools/validate_novoexport_raw018_wave4_evolution_x.py`
- `.github/workflows/novoexport-raw018-wave4-evolution-x.yml`

## R₃

`F_ok`: Wave2 + Wave3 preserved; active manifest/G2 membership bound; batch-00014 equation closes exactly; historical candidate rejected by evidence.  
`F_gap`: current raw018 provider/bytes/SHA/parse/cardinality/raw-derived PID equality + original shard-construction provenance.  
`F_next`: trace original shard-construction provenance, recover immutable/current raw018 bytes, then execute `12,115,336 → SHA256 → parse → PID commitment equality`.
