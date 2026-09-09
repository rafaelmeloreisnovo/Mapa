# RAFAELIA Minimal Rebuild Kit V1

State: `CONTRACT_DEFINED_LOCAL / CLEAN_ROOM_RECEIPT_OPEN / claim_allowed=false`

## Objective
Define the **minimum sufficient custody set** to reconstruct a bounded RAFAELIA implementation without depending on chat history.

## Required classes
1. `ROOT_MANIFEST` — global corpus-root manifest + hash algorithm/version.
2. `CANONICAL_OBJECT_REGISTRY` — stable object IDs, aliases, supersession edges.
3. `SOURCE_SET` — exact source commits/blobs for Mapa, ZIPRAF_CORE, MemRafcode and selected runtime repos.
4. `TOOLCHAIN_LOCK` — compiler/linker/sysroot/flags and target ABI.
5. `SCHEMAS` — gap ledger, semantic namespace, claim-evidence, receipts and carrier schemas.
6. `GOLDEN_VECTORS` — positive + negative vectors for binary, math and semantic gates.
7. `BUILD_RECIPES` — source→binary commands with no hidden network dependency where possible.
8. `RUNTIME_RECIPES` — host reference + Android/ARM native receipt procedure.
9. `EVIDENCE_INDEX` — source/artifact/execution/evidence separation.
10. `MEMORY_INDEX` — L/O/T + reconstruction pointers sufficient to recover current topology.

## Fail-closed rebuild sequence
`ROOT → OBJECTS → SOURCE → TOOLCHAIN → BUILD → INSPECT → TEST → RUNTIME → EVIDENCE → MEMORY`

## Pass criteria
- every required canonical object resolves;
- every byte-bearing input has SHA-256 + size;
- toolchain identity is exact or explicitly `TOKEN_VAZIO`;
- build gates pass without undeclared runtime dependencies;
- golden positives and negatives pass;
- generated receipts route back to evidence + memory;
- no missing pointer is silently replaced by a similarly named object.

## Clean-room receipt
A future rebuild receipt must list each required class as `PASS`, `FAIL` or `TOKEN_VAZIO`, include exact source/toolchain hashes, record target ABI/runtime, and identify every substituted or unavailable object.

## Non-goal
A clean rebuild does **not** independently validate scientific or physical claims. It reconstructs the software/evidence system inside its declared boundary.

`REBUILDABLE != SCIENTIFICALLY_VALIDATED`
