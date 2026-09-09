# Receipt — GeoWord Compiler/Linker Size Gate — 2026-09-09

Route: `ATLAS-X-ZIPRAF-FREESTANDING-GEO-COMPILER-20260909`  
Producer: `rafaelmeloreisnovo/ZIPRAF_CORE#9`  
Claim gate: `claim_allowed=false`

## Measured source profiles

Same carrier source under strict freestanding compilation:

| profile | text bytes | data | bss | undefined |
|---|---:|---:|---:|---:|
| O0 | 999 | 0 | 0 | 0 |
| Os | 854 | 0 | 0 | 0 |
| Oz | 448 | 0 | 0 | 0 |
| O2 | 878 | 0 | 0 | 0 |

`-Oz` was not promoted by source-object size alone because object relocation metadata remained. Final-link audit was required.

## Final loaderless ELF gate

| target | text | data | bss | undefined | runtime reloc | dynamic | result |
|---|---:|---:|---:|---:|---:|---:|---|
| x86_64 host | 471 | 0 | 0 | 0 | 0 | 0 | RUN PASS rc=0 |
| ARMv7 EABI5 | 496 | 0 | 0 | 0 | 0 | 0 | FINAL LINK PASS / device TOKEN_VAZIO |
| AArch64 | 460 | 0 | 0 | 0 | 0 | 0 | FINAL LINK PASS / device TOKEN_VAZIO |

Final ELF SHA-256:

- x86_64: `fa857179d9c656819a323537875fa5cb4427a8b659c3ebbed2bcf87b50dc8753`
- ARMv7: `283f41e972c64be2cfd143d80866bd3d120733c3a6e741090ad952663b0f76fc`
- AArch64: `42f7cea091c8c700fde4d7e9a8f42c7d3b61d646d596b790b1216f32b48084a8`

## Closure

`GF005_CROSS_ABI_SOURCE_PORTABILITY = CLOSED_CROSS_ABI_FINAL_LINK`.

This does **not** close physical ARM execution. It narrows the remaining obligation to device/runtime evidence rather than compiler/linker uncertainty.
