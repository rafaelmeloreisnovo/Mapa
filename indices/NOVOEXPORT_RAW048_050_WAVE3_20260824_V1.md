# NOVOexport RAW048–050 — Wave 3 — Historical Bytes vs Current Custody

**Date:** 2026-08-24  
**State:** `PARTIAL_EVIDENCED_HISTORICAL_BYTES_CURRENT_PROVIDER_UNBOUND`  
**claim_allowed:** `false`

## Delta

The prior hard-custody label bundled already observed historical facts together with genuinely missing current-provider evidence. This wave decomposes them without deleting the old record.

| Raw | bytes | historical conversations | historical messages | historical downloaded SHA-256 |
|---|---:|---:|---:|---|
| `conversations-048.json` | 36,771,626 | 100 | 6,543 | `ed19ea07f8763a8a4d87204d80c817694ce4d6c339c71b1d2a1b955a8c125256` |
| `conversations-049.json` | 47,806,754 | 100 | 7,196 | `608e45449809a47f5931f86328b96dab2b2b86a5abf21a8dfe1c7da6834a2f1a` |
| `conversations-050.json` | 17,115,060 | 54 | 3,647 | `c5058bf25f682de12de68b54029d13b07e836cd519416752fbc5e4fa320b4979` |

The historical metrics authority explicitly defines the hash as SHA-256 over the exact downloaded byte stream and records successful JSON parsing/cardinality under one parser contract. The physical inventory independently records the same filenames and sizes.

## Closed dimensions

- raw filename identity for 048–050;
- physical/historical size agreement;
- historical downloaded-byte SHA-256;
- historical JSON parse;
- historical root conversation cardinality;
- historical message/user/assistant counts.

## Remaining TOKEN_VAZIO

- directly addressable current provider object for each raw;
- current retrievable byte stream;
- current SHA-256 rehash;
- exact current `conversation_id` / PID sets.

## Mother invariant

```text
HISTORICAL_DOWNLOADED_BYTES != CURRENT_PROVIDER_CUSTODY
HISTORICAL_SHA256 != CURRENT_REHASH_UNTIL_REOBSERVED
CONVERSATION_COUNT != PID_SET
SEARCH_MISS != ABSENCE
```

No `MESSAGES-xxxxx.jsonl.txt` derived object may substitute the raw shard identity.

## F_ok / F_gap / F_next

**F_ok:** 048–050 are no longer treated as if hashes/parse/cardinality were globally unknown; those historical byte-level dimensions are evidenced.  
**F_gap:** current provider custody/current bytes/current rehash/PID sets remain `TOKEN_VAZIO`.  
**F_next:** recover an authoritative current provider/container route, stream exact raw bytes, require size equality, rehash, parse fail-closed and enumerate exact IDs.
