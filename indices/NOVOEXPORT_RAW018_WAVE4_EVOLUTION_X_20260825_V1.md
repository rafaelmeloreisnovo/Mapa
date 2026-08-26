# NOVOEXPORT RAW018 — WAVE 4 — X=EVOLUÇÃO — 2026-08-25

State: `CANDIDATE_REJECTED_RAW018_PROVIDER_STILL_UNBOUND`  
`claim_allowed=false` · `release_allowed=false`

Predecessor: `NOVOEXPORT_RAW018_WAVE2_20260824_V1`.

## Why this route

The Stage0 compiler/event baseline is already merged and gated. The canonical NOVOexport orthogonal receipt identifies `TV-RAW-018-CURRENT-ID` as the first dependency bottleneck before full message/node projection and semantic/vector promotion.

Therefore this cycle does **not** reopen Stage0 F1/F2/F3. It advances NOVOexport provenance first.

## X axes

| Axis | Evolution |
|---|---|
| `ATLAS` | Search the live corpus/custody state and select the highest-dependency unresolved edge. |
| `NOVO` | Start with raw `conversations-018.json`. |
| `L` | Append Wave 4 to Wave 2; no predecessor rewrite. |
| `O` | Keep provider/container/bytes/parse/PIDs/message projection independent. |
| `T` | Cross candidate archive bytes with current shard-017/019 boundary IDs. |
| `REL` | Record overlap, non-coverage, rejection and unresolved-provider edges. |
| `SCALE` | META custody → archive → monolith → shard → conversation ID. |
| `EVID` | Promote only hashes, archive members and observed boundary membership. |
| `GAP` | Preserve raw018 provider/bytes/SHA/cardinality/PIDs as `TOKEN_VAZIO`. |
| `LEARN` | Temporal/name affinity is navigation evidence, not provider identity. Rejected candidates stay queryable. |

## Evidence delta

A historical export archive was downloaded from the connected Drive and read byte-for-byte.

Observed archive:

- size: `187756731` bytes;
- SHA-256: `04ca4578dc2990e740001d9e49c3bdb229b1599bdf44dd366ec9ed19290c2ecb`;
- exactly five members: `user.json`, `conversations.json`, `message_feedback.json`, `shared_conversations.json`, `chat.html`;
- no direct `conversations-018.json` member;
- no `export_manifest.json` member;
- no `temp.locate.txt` member.

So it is rejected as the direct raw018 container.

## Transversal boundary probe

Current Drive bytes were read for the two observable neighbors:

- `conversations-017.json`: 22,560,934 bytes, JSON array cardinality 100, SHA-256 `b4b6a6080b89102699e6dbd9958c715264464d74f9782126af3085296eb3ce4f`.
- `conversations-019.json`: 16,440,670 bytes, JSON array cardinality 100, SHA-256 `f90bfc11a9088772570c1f81503c1bedcc9bd475c5435ce809d62812ff351436`.

The archive monolith `conversations.json` contains the first current shard-017 conversation ID, but does **not** contain the last current shard-017 ID or the first current shard-019 ID.

Therefore:

```text
MONOLITH_OVERLAP != COMPLETE_SHARD_SOURCE
```

and the archive is also rejected as a complete source for the current shard range 017–019. It cannot be used to reconstruct or bind raw018.

## Anti-regression

```text
CANDIDATE_TEMPORAL_AFFINITY != PROVIDER_IDENTITY
MONOLITH_OVERLAP != COMPLETE_SHARD_SOURCE
NEIGHBOR_CARDINALITY != RAW018_CARDINALITY
RECONSTRUCTION != OBSERVED_RAW_SOURCE
DERIVED_ORDINAL != RAW_SOURCE_ORDINAL
TOKEN_VAZIO != 0
```

No inference from the two 100-record neighbors is allowed to fill raw018 cardinality.

## Gap state

`TV-RAW-018-CURRENT-ID` remains:

`PARTIAL_EVIDENCED_PHYSICAL_INVENTORY_PROVIDER_UNBOUND`.

Still open:

- current provider/file identity;
- exact current/recoverable raw bytes;
- raw SHA-256;
- JSON parse/cardinality;
- exact conversation/PID set.

The new information is a **search-space reduction**, not a claim promotion.

## Next gate

1. Find a newer/full export container or the actual deterministic sharding provenance.
2. Require compatibility with current shard-017-last and shard-019-first boundaries before binding the source.
3. Extract the exact `conversations-018.json`, or derive it only if the sharding recipe itself is evidenced and separately receipted.
4. Require exactly `12,115,336` bytes.
5. SHA-256.
6. Parse fail-closed.
7. Enumerate exact conversation IDs/PIDs.
8. Join `source_ref → conversation_id → message_id/node_id → file_id → record_sha256`.
9. Only then expand semantic/vector relations and promotion gates.

## Files

- `data/evidence/novoexport_raw018_wave4_evolution_x_20260825.v1.json`
- `tools/validate_novoexport_raw018_wave4_evolution_x.py`
- `.github/workflows/novoexport-raw018-wave4-evolution-x.yml`

## R₃

`F_ok`: one candidate container tested and rejected with byte/hash evidence; neighbor boundary evidence added; predecessor preserved.  
`F_gap`: raw018 provider/bytes/SHA/cardinality/PIDs remain `TOKEN_VAZIO`.  
`F_next`: locate a source/provenance chain spanning the current 017/019 boundaries and close exact raw018 byte identity.
