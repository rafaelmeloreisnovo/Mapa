# NOVOexport RAW 048–050 — current custody wave 4

State: `PARTIAL_EVIDENCED_CURRENT_CUSTODY_PID_SET_OPEN`  
Claim boundary: `claim_allowed=false`  
Observation window: `2026-08-25T08:06:24.459Z`–`08:07:02.472Z` (`05:06:24.459`–`05:07:02.472 BRT`)

## Delta

The three current private Drive objects were addressed directly, streamed in full and hashed without publishing their locators, bodies or IDs. Their current byte counts and SHA-256 values match the historical parsed streams exactly.

| Shard | Bytes | Current SHA-256 = historical | Current parse/cardinality | PID set |
|---|---:|:---:|---|---|
| 048 | 36,771,626 | yes | bound by exact byte identity | `TOKEN_VAZIO` |
| 049 | 47,806,754 | yes | bound by exact byte identity | `TOKEN_VAZIO` |
| 050 | 17,115,060 | yes | bound by exact byte identity | `TOKEN_VAZIO` |

This successor narrows the predecessor `data/evidence/novoexport_raw048_050_wave3_20260824.v1.json`; it does not rewrite it. Exact-byte identity permits reuse of the deterministic historical parse result. Conversation counts do not substitute for PID enumeration.

## Evidence boundary

```text
current provider observation + exact bytes + SHA-256 match
  => current byte custody and deterministic parse binding
  != PID-set enumeration
  != corpus completeness
  != scientific or operational claim promotion
```

No cache, lock-free, allocator, network, ABI, Vectra, T7, 42-cycle or cosmological claim is made by this receipt.

## R3

`F_ok` = provider/bytes/hash closed for RAW 048–050.  
`F_gap` = PID commitments 048–050 and current RAW018 byte custody.  
`F_next` = compute privacy-preserving PID-set commitments from the exact current streams and reconcile with the private PID index.
