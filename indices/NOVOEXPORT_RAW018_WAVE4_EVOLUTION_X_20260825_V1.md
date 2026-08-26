# NOVOEXPORT RAW018 — WAVE 4 — X=EVOLUÇÃO — 2026-08-25

State: `CANDIDATE_REJECTED_PID_COMMITMENT_PRESERVED_CURRENT_BYTE_CUSTODY_OPEN`  
`claim_allowed=false` · `release_allowed=false`

Direct predecessor: `NOVOEXPORT_RAW018_WAVE3_PID_RECONCILIATION_20260824_V1` (merged in `3ab1eb3a596148e616f0e2d134f2cc8b71b0fafe`).  
Lineage: Wave2 → Wave3 → Wave4.

## Why this route

The Stage0 compiler/event baseline is already merged and gated. The canonical NOVOexport orthogonal route identifies `TV-RAW-018-CURRENT-ID` as the first dependency bottleneck before full message/node projection and semantic/vector promotion.

The longitudinal reread also established that Wave3 already closed one orthogonal dimension:

```text
RAW018_PID_HASH_SET = EVIDENCED_RECONCILED_100_PRIVACY_PRESERVING
candidate_set_sha256 = 766644f8a199de4317500e6f40d44f9187f767e2ea453910ab4a4d0ec8cfc69e
```

Wave4 therefore **must preserve** that commitment while keeping current raw-byte custody open.

## X axes

| Axis | Evolution |
|---|---|
| `ATLAS` | Search live corpus/custody state and select the highest-dependency unresolved edge. |
| `NOVO` | Start with raw `conversations-018.json`. |
| `L` | Preserve Wave2 and merged Wave3; Wave4 only appends. |
| `O` | Keep provider/container/bytes/parse/current-cardinality/PID-commitment/raw-derived-commitment-match/message-projection independent. |
| `T` | Cross candidate archive bytes with current shard-017/019 boundary IDs. |
| `REL` | Preserve Wave3 PID commitment; add overlap, non-coverage, rejection and unresolved-provider edges. |
| `SCALE` | META custody → wave → archive → monolith → shard → privacy-preserving conversation identity. |
| `EVID` | Promote only hashes/member observations/boundary membership plus already-merged Wave3 commitments. |
| `GAP` | Preserve provider/bytes/raw-SHA/current-parse/current-cardinality/current-raw PID commitment match as `TOKEN_VAZIO`; do **not** reopen the reconciled 100-PID commitment. |
| `LEARN` | Longitudinal evidence outranks a new local assumption. A successor cannot regress a dimension closed by a merged predecessor. |

## Preserved Wave3 evidence

- privacy-preserving candidate count: `100`;
- candidate-set commitment: `766644f8a199de4317500e6f40d44f9187f767e2ea453910ab4a4d0ec8cfc69e`;
- chronological commitment: `c29cbc493b2401d0d875a49a71999f4b32f8b3faab8a86cd2c1d9a4e4ca83706`;
- historical object witness: `f14cd8767241255d64dba51b818e1bf3d5eefb6af157f1b321199cb102223156`.

Invariant:

```text
PID_HASH_SET_EVIDENCE != CURRENT_RAW_BYTE_CUSTODY
```

The commitment is closed. Equality between a PID commitment recomputed from **current raw018 bytes** and that preserved commitment is still open until those bytes are observed.

## Wave4 evidence delta

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

The candidate monolith `conversations.json` contains the first current shard-017 conversation ID, but does **not** contain the last current shard-017 ID or the first current shard-019 ID.

Therefore:

```text
MONOLITH_OVERLAP != COMPLETE_SHARD_SOURCE
```

and the archive is rejected as a complete source for the current shard range 017–019. It cannot reconstruct or bind raw018.

## Anti-regression

```text
PID_HASH_SET_EVIDENCE != CURRENT_RAW_BYTE_CUSTODY
CANDIDATE_TEMPORAL_AFFINITY != PROVIDER_IDENTITY
MONOLITH_OVERLAP != COMPLETE_SHARD_SOURCE
NEIGHBOR_CARDINALITY != CURRENT_RAW018_CARDINALITY
RECONSTRUCTION != OBSERVED_RAW_SOURCE
DERIVED_ORDINAL != RAW_SOURCE_ORDINAL
TOKEN_VAZIO != 0
```

No inference from the two 100-record neighbors may fill **current raw JSON cardinality**. Conversely, no Wave4 search failure may demote the already-evidenced Wave3 PID commitment.

## Gap state

`TV-RAW-018-CURRENT-ID` remains:

`PARTIAL_EVIDENCED_PID_SET_CURRENT_BYTE_CUSTODY_OPEN`.

Closed dimensions retained:

- existence/path/size from Wave2;
- privacy-preserving 100-PID hash set from Wave3.

Still open:

- current provider/file identity;
- exact current/recoverable raw bytes;
- raw SHA-256;
- current JSON parse/cardinality;
- recompute PID hash set from current raw bytes and require equality with the Wave3 commitment.

The Wave4 information is a **search-space reduction**, not a claim promotion or demotion.

## Next gate

1. Find a current raw018 byte witness or deterministic sharding provenance.
2. Require consistency with current shard-017/019 boundaries before source binding.
3. Extract exact `conversations-018.json`, or derive it only if the sharding recipe itself is evidenced and separately receipted.
4. Require exactly `12,115,336` bytes.
5. SHA-256.
6. Parse fail-closed and observe current cardinality.
7. Compute privacy-preserving PID hash set from those current bytes.
8. Require commitment exactly `766644f8a199de4317500e6f40d44f9187f767e2ea453910ab4a4d0ec8cfc69e`.
9. Join `source_ref → conversation_id → message_id/node_id → file_id → record_sha256`.
10. Only then expand semantic/vector relations and promotion gates.

## Files

- `data/evidence/novoexport_raw018_wave4_evolution_x_20260825.v1.json`
- `tools/validate_novoexport_raw018_wave4_evolution_x.py`
- `.github/workflows/novoexport-raw018-wave4-evolution-x.yml`

## R₃

`F_ok`: Wave3 PID commitment preserved; one candidate container tested/rejected with byte/hash evidence; neighbor boundary evidence added; lineage remains append-only.  
`F_gap`: current raw018 provider/bytes/SHA/parse/cardinality/raw-derived commitment match remain `TOKEN_VAZIO`.  
`F_next`: locate current raw018 bytes or deterministic sharding provenance and validate `12,115,336 → SHA256 → parse → PID commitment equality`.
