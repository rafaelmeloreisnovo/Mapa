# RAFAELIA — Vectras 8-core × 760+ logical-layer evidence delta — V1

Date: 2026-08-12
Mode: APPEND_ONLY / EVIDENCE_FIRST / NO_SILENT_PROMOTION
State: VERIFIED_LIMITED_STATIC
claim_allowed: false

## Invariant

`8 physical/logical CPU executors != 760 physical CPUs`.

The currently supported narrow statement is:

> Vectras contains static mechanisms that represent and traverse 760 or more logical color/layer/view states while the runtime substrate can be much smaller (including an explicit 8-vCPU orchestration path). This does not yet prove 760-way simultaneous physical execution or performance equivalence to 760 cores.

## Frozen source revisions

- `rafaelmeloreisnovo/Vectras-VM-Android`
  - observed ref: `master`
  - pinned commit: `21ad17f89ce2bf29cb0d8c184c612d76a99a9b3d`
- `rafaelmeloreisnovo/Mapa`
  - base ref: `main`
  - pinned base commit: `8789f29f257af1e958e59cd25e1d30dea10cde98`

## Static evidence

### E1 — BITWALK / BITGHOST logical layer space

Source: `Rafaelia/rafaelia_bitwalk.h`
Blob SHA: `00831ffdca39b0b3ee5820e6d39825b4a33fdae7`

Observed:
- `color_layers` is a logical field explicitly documented as able to exceed 760.
- fallback/reference value `760u` is used when no explicit `color_layers` value is present.
- traversal operators include `CONTINUE`, `BACK`, `FWD1`, `BACK1`, `FWD2`, `BACK2`, `LAYER`, `COLOR`.
- BITGHOST can keep an item in the same container while a view ignores it, with `extracted=0`.

Interpretation boundary:
- This supports `logical multiplexing / views / layer traversal`.
- It does not prove `760 CPU cores`, `760 OS threads`, or `760 simultaneously executing hardware contexts`.

### E2 — explicit 8-vCPU orchestration path

Source: `Rafaelia/rafaelia_orchestrator.c`
Blob SHA: `1184686b6fca4d620afd2da93193a67ad316656c`

Observed:
- `N_VCPU 8`.
- static arena `ARENA_SZ = 2 MiB`.
- declared memory hierarchy `L1 -> L2 -> buffer -> RAM -> storage`.
- per-vCPU state exists in the orchestrator design.

Interpretation boundary:
- Source existence/design != physical execution receipt.

### E3 — Android hardware profile

Source: `app/src/main/java/com/vectras/vm/core/BareMetalProfile.java`
Blob SHA: `665bb90d7f8f06a9ece1d2442a6c50ee02c66379`

Observed:
- core count is derived from runtime and `/sys/devices/system/cpu/possible`.
- `CAP_MULTI_CORE` is set when cores > 1.
- recommended parallelism is bounded by observed cores (`cores - 1` for cores >= 4).
- recommended work block grows when `cores >= 8`.

Interpretation boundary:
- This distinguishes physical/runtime parallelism from the larger logical layer space.

## NOVOexport shards 048–050 — current Stage-1 record

Authority pointer: Google Drive document `RAFAELIA_METRICS_STAGE1_CONVERSATIONS_043_050`, provider id `1ccOoYooH-STuDvrPQQSihtg4nqpmifd7QQ8w25nIr1w`.
Parser contract records SHA-256 over exact downloaded byte streams.

| shard | bytes | conversations | messages | sha256 |
|---|---:|---:|---:|---|
| conversations-048.json | 36,771,626 | 100 | 6,543 | `ed19ea07f8763a8a4d87204d80c817694ce4d6c339c71b1d2a1b955a8c125256` |
| conversations-049.json | 47,806,754 | 100 | 7,196 | `608e45449809a47f5931f86328b96dab2b2b86a5abf21a8dfe1c7da6834a2f1a` |
| conversations-050.json | 17,115,060 | 54 | 3,647 | `c5058bf25f682de12de68b54029d13b07e836cd519416752fbc5e4fa320b4979` |

Aggregate for 048–050 under this record:
- bytes: `101,693,440`
- conversations: `254`
- messages: `17,386`
- user messages: `1,277`
- assistant messages: `16,109`
- characters: `13,782,241`
- textless messages: `12,339`
- tokenizer-exact token count: `TOKEN_VAZIO_TOKENIZER_NOT_FIXED`

## Gaps / TOKEN_VAZIO

1. `TOKEN_VAZIO_RUNTIME_8x760_RECEIPT`
   - no single pinned execution receipt has yet been linked here proving `8 executors -> 760 logical layers` under one run.
2. `TOKEN_VAZIO_PARALLELISM_SEMANTICS`
   - exact mapping between logical layer transitions and OS threads/tasks/vCPUs remains unmeasured in this evidence packet.
3. `TOKEN_VAZIO_PERFORMANCE_SCALING`
   - no governed curve yet links logical layers `{8,64,128,760,1536}` to throughput/latency/cache/memory movement.
4. `TOKEN_VAZIO_NOVOEXPORT_VERSION_RECONCILIATION`
   - other Drive artifacts may refer to historical or differently staged identities for these shard names; no identity should be silently merged without source-id/bytes/hash reconciliation.
5. `TOKEN_VAZIO_DEVICE_RECEIPT_CURRENT`
   - source-level declarations for the 8-vCPU path are not a substitute for a current device execution receipt.

## Required benchmark gate

A promotion beyond `VERIFIED_LIMITED_STATIC` requires, at minimum:

`device identity + Vectras pinned commit + build command + binary/APK hash + workload identity/hash + layer count + executor/core count + throughput + p50/p95/p99 + bytes moved + memory/cache counters when available + exit status + raw log hash + receipt`.

Suggested controlled sweep:

`layers in {8, 64, 128, 760, 1536}` with the same pinned workload and fixed executor policy.

## Claim matrix

- `C-VECTRAS-LAYERSPACE-001`: `color_layers >= 760 is representable in current static code` -> `EVIDENCED_STATIC`, claim_allowed=true only for this narrow source-code statement.
- `C-VECTRAS-8VCPU-001`: `an explicit N_VCPU=8 orchestrator path exists` -> `EVIDENCED_STATIC`, claim_allowed=true only for source existence.
- `C-VECTRAS-8x760-EXEC-001`: `8 cores execute as 760 physical cores` -> `TOKEN_VAZIO / BLOCKED`, claim_allowed=false.
- `C-VECTRAS-8x760-LOGICAL-001`: `a smaller execution substrate can traverse a much larger logical layer/view space` -> `SUPPORTED_BY_DESIGN`, claim_allowed=false for performance or physical-equivalence readings.

## R3

- F_ok: 760+ logical-layer mechanism and explicit 8-vCPU orchestration path are both pinned to current Vectras source revision; shards 048–050 have a byte-read Stage-1 metrics authority record.
- F_gap: runtime coupling, scaling, device receipt, exact scheduler semantics, and shard-version reconciliation remain open.
- F_next: execute and receipt a fixed-workload 8/64/128/760/1536-layer sweep, then bind the result back to Vectras producer evidence and this Mapa control-plane record.
