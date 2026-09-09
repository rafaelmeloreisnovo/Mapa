# ATLAS:X — ZIPRAF Freestanding Geo-Compiler Successor — 2026-09-09

Cycle: `OMEGA-FED-20260909-GEOFS-001`  
Predecessor route: `ATLAS:X-ZIPRAF-BITRAF-BITOMEGA-42-20260906`  
Mode: `APPEND_ONLY / SOURCE_FIRST / FAIL_CLOSED / NO_AUTO_MERGE`  
Claim gate: `claim_allowed=false`

## Intent

Route the current freestanding/compiler-linker reduction without rewriting existing producer truth. The producer implementation is `rafaelmeloreisnovo/ZIPRAF_CORE#9`; this Mapa delta is pointer/control-plane evidence only.

## NOVO:X

The current uploaded ZIPRAF custody package preserves 51 physical NOVOexport shard receipts, but the 51 raw JSON input bytes are not embedded in that package. Direct semantic re-derivation from those raw inputs in this cycle is therefore `TOKEN_VAZIO_INPUT_BYTES`. A Drive/Git search miss is not promoted to absence.

## L:X — longitudinal

The route extends, rather than replaces:

`ZIPRAF page/container geometry -> BitRAF logical geometry/parity -> BitOmega state -> 42/4242 -> evidence/gate/receipt`

with:

`-> GeoWord64 group/epistemic carrier -> precompiler/compiler/warning/linker boundary -> cross-ABI compile evidence -> device/external gates`

## O:X — orthogonal axes

- `O1_IDENTITY`: BitRAF 42-bit logical payload remains byte/bit-preserved inside the new carrier.
- `O2_EPISTEMIC`: `ZERO != NOOP != TOKEN_VAZIO != VOID != VALID != REJECT`.
- `O3_BUILD`: source object, linked runtime and physical execution are distinct evidence classes.
- `O4_AUTH`: structural witness is not HMAC/signature/authenticity.
- `O5_OPT`: warning != permission to delete source; linker GC requires reachability proof and tests.
- `O6_VECTOR`: NEON/math/Android helpers are adapters, not dependencies of the minimum kernel.
- `O7_CLAIM`: physical performance/capacity claims remain external until measured.

## T:X — transversal sources observed

| Surface | Source | Role | Boundary |
|---|---|---|---|
| ZIPRAF_CORE | `include/raf_geo_word.h`, `src/raf_geo_word.c` on PR #9 | new minimum carrier | source/KAT, not device proof |
| Termux RAFCODEPHI | `docs/RAFCODEPHI_COMPILER_CONTRACT.md` | warnings/loops/linker contract | host/native safety != APK runtime |
| Termux BitRAF | `asm/RAFAELIA_ISA_BITRAF.md` | logical 42-bit encoding | logical ISA != CPU native word |
| RafGitTools | `native/rafcode_federation_v1` | 64-byte loaderless fixed-frame kernel | syscall ELF != bare-metal firmware |
| Vectras | `engine/rmr/bitomega.*`, `bitraf.*`, `rmr_zipraf_core.c` | state/bit/container integration | source integration != exact semantic identity |
| Vectras ASM | `tools/baremetal/rafcode_phi/asm/rafcode_phi_emit_word.S` | physical ABI emitter | writes 32-bit words; does not prove native 42-bit word |
| llamaRafaelia | `rmrCti/rf_core.c` | no-libc BitStack/CRC/cognitive cycle | loops/globals remain; not zero-state kernel |
| Rafaelia_Private | `Low-level/rafcode_phi_core.h` | NEON/math/formula adapter | math.h/NEON/logging dependencies kept outside kernel |
| GAIA_phi | `FCEA_ABSENCE_INDEX.sh`, `FIBER-H-CTX.c` | absence/context/ECC probes | heuristic/runtime probes != source truth |

## REL:X — relations

`42-bit logical instruction` REL `64-bit aligned carrier`: **embedding**, not identity.  
`BitRAF` REL `BitOmega`: **integration edge**, exact state-semantic equivalence remains open.  
`CRC` REL `XOR/parity`: may share an input traversal after equivalence proof; their semantics remain distinct.  
`BitStack` REL `ZIPRAF AO42`: append-only/storage relation; neither is automatically a compressor claim.  
`NOOP` REL `TOKEN_VAZIO`: both may emit no mutation, but NOOP is intentional action while TOKEN_VAZIO is unknown/unproven state.

## SCALE:X

`META/Atlas -> repository -> module group -> procedure -> GeoWord64 -> BitRAF42 -> field/bit`.

The smallest audited unit in this successor is the field/bit in `GeoWord64`; no yocto/physical-scale claim is inferred from the naming hierarchy.

## EVID:X — bounded evidence

Producer branch `ZIPRAF_CORE#9` materializes:

- 10 module groups with one minimal procedure each;
- host KAT `PASS` for payload preservation and witness tamper rejection;
- host freestanding source object `.text=854`, data=0, bss=0, undefined symbols=0;
- ARMv7 Android compile-only object, zero undefined symbols, SHA-256 `f51639ea1b29bfa43e6c2c2484a93f594b1e6fc1265a572c28fbe18b13a4fe30`;
- AArch64 Android compile-only object, zero undefined symbols, SHA-256 `8d0d3c0a9268f58e14f7e6f389fe282d1f92b52b0ea41ba27ca69710de4c0899`.

Cross compilation is not physical execution.

## GAP:X — closure ledger

| Gap | State after this cycle | Closure boundary |
|---|---|---|
| `GF001_NOOP_TOKEN_VOID_COLLAPSE` | `CLOSED_SOURCE_CONTRACT` | explicit independent enum states + KAT |
| `GF002_LOGICAL42_NATIVEWORD_AMBIGUITY` | `CLOSED_BOUNDARY` | logical 42-bit ISA separated from 32-bit/ABI emitter |
| `GF003_KERNEL_ADAPTER_DEPENDENCY_COLLAPSE` | `CLOSED_ARCHITECTURE` | NEON/math/logging isolated as adapter surface |
| `GF004_WARNING_AUTODELETION_AMBIGUITY` | `CLOSED_ROUTED_EXISTING_CONTRACT` | warning -> classify -> linkage -> GC -> verify |
| `GF005_CROSS_ABI_SOURCE_PORTABILITY` | `CLOSED_COMPILE_ONLY` | ARMv7 + AArch64 objects produced; no runtime claim |
| `GF006_BITRAF_BITOMEGA_EXACT_STATE_BINDING` | `TOKEN_VAZIO` | Vectras `bitraf.h` exposes codec API, not a tested 10-state binding table |
| `GF007_GEOWORD_AUTHENTICITY` | `TOKEN_VAZIO` | witness8 is intentionally non-cryptographic |
| `GF008_GEOWORD_DEVICE_RUNTIME` | `TOKEN_VAZIO_DEVICE` | requires physical ARM device receipt |
| `G015_ZIPRAF_SECOND_PHYSICAL_ARCHITECTURE` | `OPEN_EXTERNAL_GATE` | tracked in Mapa #573 |
| `G016_ZIPRAF_EXTERNAL_SECURITY_AUDIT` | `OPEN_EXTERNAL_GATE` | tracked in Mapa #573 |
| `G017_ZIPRAF_PLANNING_PHI_0_7_EVIDENCE` | `OPEN_TOKEN_VAZIO` | measurement/model evidence required |
| `G018_ZIPRAF_R2_CONFIDENCE_VALIDATION` | `OPEN_TOKEN_VAZIO` | statistical validation required |

## LEARN:X

Append-only learning from this cycle:

1. the strongest reduction is contract composition, not another duplicate runtime;
2. logical word width must remain separate from physical ABI word width;
3. intentional silence (`NOOP`) and absent evidence (`TOKEN_VAZIO`) require separate machine states;
4. loop removal is valid only after semantic equivalence, not from aesthetics or warning count;
5. a fixed carrier can route module identity/evidence without importing the heavier module into the kernel.

## F_ok / F_gap / F_next

`F_ok`: source-level semantic gaps GF001–GF005 are now explicit and bounded; producer code exists on ZIPRAF_CORE#9; external gaps were not silently promoted.  
`F_gap`: GF006–GF008 and G015–G018 remain authority-matched external/device/crypto/statistical gates.  
`F_next`: create one evidence-producing successor per open gap; no combined PASS is authorized.
