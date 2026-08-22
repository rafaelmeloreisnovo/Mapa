# RAFAELIA — Drive Deep Corpus Delta 0004

Date: 2026-08-22  
State: `VERIFIED_LIMITED / APPEND_ONLY / claim_allowed=false`

This is an additive successor to `RAFAELIA_DRIVE_DEEP_CORPUS_ROUTING_V1.md` and `RAFAELIA_DRIVE_DEEP_CORPUS_SNAPSHOT_0003.json`. It records applied closure methods and does not rewrite predecessor evidence.

## Durable Drive anchors

- INGEST_0004: `1JTrw1CDhh13gkeBayt8jhpsftLV2DFw2OgQveyyc2Y8`
- applied-method receipt DELTA_0001: `1Qb1THLu3_QjxQ4FMfZgERg6c1JttWDmY_W-HHMl_zBc`
- privacy PID index V5: `1xhP6CJZsaLoqPokHvGuuWlvathVS5UKLejgFo9S2J9U`
- OPDASH-001: `1JUSbJlHlVWznJJ5O1vzQwdd3yPc_J8faUcXA_ov0kkk`

Machine-readable sibling: `data/indexes/RAFAELIA_DRIVE_DEEP_CORPUS_SNAPSHOT_0004.json`.

## Applied dependency delta

```text
A2 RAW048..050
  current provider IDs
  -> primary bytes
  -> SHA256 equality with frozen historical witnesses
  -> JSON parse
  -> canonical conversation identity
  -> privacy PID derivation
  -> CLOSED_VERIFIED

A1 RAW018
  exact current-provider search negative
  -> TOKEN_VAZIO_HARD_CUSTODY_CONFIRMED
  -> next gate changes to alternative immutable witness

A3 FULL_CORPUS_V2
  BLOCKED_BY(A1,A2)
  -> A2 closed
  -> BLOCKED_BY(A1_ONLY)

A4 TERMINAL_PROVIDER_ENUMERATION
  search/list inference rejected as terminal proof
  -> parent-aware pagination + inventory reconciliation + per-object/revision identity
```

## A2 evidence summary

| RAW | current provider ID | bytes | SHA256 | JSON roots | PIDs |
|---|---|---:|---|---:|---:|
| 048 | `1zfyYkELQQOiMNeW_no8oYFgdiewhxCdO` | 36,771,626 | `ed19ea07f8763a8a4d87204d80c817694ce4d6c339c71b1d2a1b955a8c125256` | 100 | 100 |
| 049 | `1e4qhX1taiRY72ZBQZUim-A-jgQojqeEH` | 47,806,754 | `608e45449809a47f5931f86328b96dab2b2b86a5abf21a8dfe1c7da6834a2f1a` | 100 | 100 |
| 050 | `1rpWFICYTTFKbZzvzHdW3PQV5LzLlEA-C` | 17,115,060 | `c5058bf25f682de12de68b54029d13b07e836cd519416752fbc5e4fa320b4979` | 54 | 54 |

For all three: current SHA256 exactly equals the frozen historical SHA256.

Privacy identity rule preserved:

```text
PID = SHA256(UTF8(canonical conversation_id))
raw_id_persisted = false
```

- new PIDs from RAW048..050: `254`
- unique new PIDs: `254`
- overlap with V4 (4,698 PIDs): `0`
- overlap with historical Locator V1.1 (2,573 PIDs): `0`
- V5 total unique PIDs: `4,952`
- new PID-set SHA256: `74e2a192614ca34a7cfefdc864e64d20a842c3f6d86e9516b004e819ceaeaa25`
- canonical local V5 CSV SHA256: `d39de51776e1a001385d4168c37d0739d75b7b95cdd40084f1154c1e4a324c13`

Hash equality proves byte identity only. It does not imply semantic/scientific claim validation.

## Deep-corpus method application

```text
TV-DEEP-026 -> parent-aware BFS/paginated census
TV-DEEP-027 -> Google Photos exclusion only by proven ancestry
TV-DEEP-028 -> metadata-first enumeration of STREAM_BACKUP/FILES
TV-DEEP-029 -> container hash -> zstd test -> TAR member manifest -> member lineage
TV-DEEP-030 -> manifest + provider MIME + magic/content classification
TV-DEEP-031 -> identity=(provider_id,parent_lineage,byte_or_revision_identity)
TV-DEEP-032 -> direct-list ceiling is non-terminal
TV-DEEP-033 -> archive container identity != archive member identity
TV-DEEP-034 -> sensitive material metadata-first
```

## PR113 succession

Observed current state for `rafaelmeloreisnovo/llamaRafaelia#113`:

- merged: true
- head: `c50f4012a627a782fb5db98779d6359abbdd1fe0`
- merge commit: `b983ca43f778614be4bc95773dffd8dab56fef99`
- submitted reviews observed: `0`
- inspected final-head remote job path: `steps=[]`

Therefore the historical `BLOCKED_NO_MERGE` instruction is `SUPERSEDED_WITHOUT_ERASING` by the observed merge. The correct successor state is `POST_MERGE_AUDIT_REQUIRED`; missing review and zero-step remote execution remain evidence gaps and are not converted into PASS or code failure.

## Anti-regression

1. A2 must not regress to `HASH_UNKNOWN` without contradictory evidence.
2. A1 cannot be fabricated from a count coincidence or similarly named derived object.
3. A3 cannot be called full-corpus PASS while A1 remains outside verified custody.
4. Search/list miss is not absence or provider terminality.
5. Raw conversation IDs remain absent from the privacy PID index.
6. PR merge does not retroactively manufacture review or execution evidence.
7. `claim_allowed=false` remains unchanged.

## F-state

**F_ok**: A2 closed with current bytes/hash/JSON/PIDs; PID V5 materialized with 4,952 unique PIDs; A3 blocker reduced to A1 only; OPDASH and Drive receipt updated; deep-corpus methods made explicit.

**F_gap**: A1 RAW018 custody; A3 full-corpus execution after A1; A4 terminal provider enumeration/global hash; deep census/archive-member lineage; commit-bound runtime/review evidence.

**F_next**: recover RAW018 through a new immutable witness; continue parent-aware census and archive lineage; only then execute full-corpus Official V2 and freeze source/output manifests and hashes.
