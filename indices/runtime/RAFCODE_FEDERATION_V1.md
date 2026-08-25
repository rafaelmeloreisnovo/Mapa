# RafCode Federation V1 — evidence-bounded runtime route

**State:** `EVIDENCED_SCOPED_DRAFT_UNMERGED`  
**Claim gate:** `claim_allowed=false`  
**Producer:** `rafaelmeloreisnovo/RafGitTools`  
**Federated authority:** `rafaelmeloreisnovo/Mapa`

## Route

`L/O/T indices → Mapa route → RafGitTools producer → fixed work frame → branchless validator → fixed receipt → ABI ELF gate → append-only receipt`

The implementation is proposed in [RafGitTools PR #381](https://github.com/rafaelmeloreisnovo/RafGitTools/pull/381). The exact implementation commit is `7e72713da20b849a0d975d3dbefedd3d65ca0443`; its dedicated [workflow run 32868449710](https://github.com/rafaelmeloreisnovo/RafGitTools/actions/runs/32868449710) completed successfully. The PR remains draft and unmerged.

## Three memories / three indices

| Axis | Mask | Drive folder | Drive index document | Runtime role |
|---|---:|---|---|---|
| LONGITUDINAL | `0x01` | `1X2-O4-_C-wKqpUbgly6EpbNE4ApLGmvK` | `1XHkixpMruPqrv22EJ5X0TeWUn7fWEXgmjnGSlxtaGzk` | predecessor/successor chronology and append-only receipts |
| ORTHOGONAL | `0x02` | `1p6_xn3kTalwh5uqB4rIhf0k3nyq3NIKx` | `1HXDWFSmHGNo7pouUge3AIGhTq4SL_EkfrurXdJzM6-E` | provenance, identity, runtime, measurement, governance and security axes |
| TRANSVERSAL | `0x04` | `15Ie8OypFVrdl1OU-mQ4moDWer4fhRESe` | `13oy53b9OAm7Fomyt_FANl7pAORrPtBAfnkZny7Kx-f8` | evidence-bounded bridges across domains and repositories |

The binary requires mask `0x07`; no axis may be silently omitted. Canonical GitHub binding: `data/memory/RAFAELIA_TRIAXIAL_MEMORY_INDEX_V1.json` at blob `0b3d43e7fc75d86c6fa8606d4dbc6345734e44ac`.

## Runtime envelope

- 64-byte little-endian input frame;
- 64-byte little-endian receipt;
- all four roles required: `CONTROL | EXECUTOR | EVIDENCE | VM` (`0x0f`);
- eight canonical states and sixteen canonical transition actions;
- one read, one write and architecture-owned raw syscalls;
- no libc, CRT, allocator, malloc, heap, garbage collector, dynamic loader or external runtime library;
- no source loops, writable static state, relocation, undefined/final symbol, GOT/PLT, or executable stack;
- tail/sibling-call optimization disabled and variable shadowing rejected by the compiler;
- validator assembly audited before object creation as zero branches and zero calls.

## Scoped evidence

| ABI | Bytes | SHA-256 | Observed scope |
|---|---:|---|---|
| x86-64 | 1,280 | `2a7d78477d99cdbd0f75d4969141dcc39e0a5427c3f289c51474584465f04a0a` | compile, link, ELF audit, hotpath audit and smoke execution |
| ARMv7 | 1,048 | `07d1a7c0eb59ab06f3b820d762f809a90534caae8561e6e213ce360e310d5bf3` | compile, link, expected-machine ELF and generated-assembly hotpath audit |
| AArch64 | 1,152 | `e33c9b244d908717e914d6176184bf051ab6679a06add24df8bbc8d233974ac1` | compile, link, expected-machine ELF and generated-assembly hotpath audit |

Each ELF has one RX `PT_LOAD`, zero `PT_INTERP`, `DT_NEEDED`, relocations, symbols, undefined symbols, writable static bytes, source loops and heap primitives.

## Drive longitudinal readback

The canonical Drive document `RAFAELIA — Master Navigation Registry V1` (`1x_5x3_NdSaHtPLF9hbu8M1i0kvza_MnhtWeZycav19Y`) received the append-only marker `SUPERSESSÃO APPEND-ONLY — RAFCODE_FEDERATION_V1 — 2026-08-25`. The write used required revision control, returned revision `AIroW37h5TPWuni5fvC6A7ahvnk-truV83UYSpHgRqCUwxHZbq3s2qX2N1XaFEy4mMSEixg2DCenOwBcYbxyQym8WxVS9ZlMMNgimwrjObc`, and readback confirmed the marker as `HEADING_2` plus both PRs, the run, all three index IDs and all three binary hashes.

Drive receipt: `data/receipts/rafcode/2026-08-25-rafcode-federation-drive-append.v1.json`

## Boundary

This evidence does **not** prove physical ARM execution, HMAC/authenticity closure, repository-wide health, merge readiness, post-merge `main`, or complete federation. These remain:

- `TOKEN_VAZIO_PRODUCER_PR_MERGE_AND_MAIN_RECEIPT`;
- `TOKEN_VAZIO_PHYSICAL_ARMV7_DEVICE_RECEIPT`;
- `TOKEN_VAZIO_PHYSICAL_AARCH64_DEVICE_RECEIPT`;
- `TOKEN_VAZIO_HMAC_AUTHENTICITY`;
- `TOKEN_VAZIO_REPOSITORY_WIDE_HEALTH`.

Machine route: `data/federation/rafcode-federation-v1.json`  
Receiving receipt: `data/receipts/rafcode/2026-08-25-rafcode-federation-cross-abi.v1.json`

## R3

- `F_ok`: L/O/T identities, producer boundary, fixed-frame implementation and three cross-ABI compile/link/ELF/hotpath gates are reconstructible.
- `F_gap`: device execution, HMAC authenticity, producer merge/main and repository-wide health remain open/TOKEN_VAZIO.
- `F_next`: keep both PRs draft until global blockers and merge authority are resolved; after authorized integration, collect producer-main and physical-device receipts.
