# RAFAELIA Freestanding Kernel Profile V1

Applies only to **new original RAFAELIA low-level kernels** that are intentionally built outside the Android/Java application framework boundary.

## Hard engineering constraints

- freestanding translation unit;
- no libc linkage;
- no malloc/calloc/realloc/free;
- no heap/GC dependency;
- no hidden runtime fallback;
- no external package dependency in the kernel core;
- no shadow implementation that silently takes over when the declared kernel fails;
- no tail layer whose only purpose is to preserve an unnecessary dependency chain;
- minimize exported symbols, relocations, loops and branches subject to correctness;
- architecture-specific code must declare ABI, endianness, alignment, register/clobber contract and test vector;
- use fixed-capacity caller-owned/static storage when state is required;
- integer overflow, bounds, aliasing and alignment behavior must be explicit;
- compiler/linker flags and binary hash belong in the receipt;
- friction is treated as a diagnostic catalyst: a failure must reveal the next falsifiable mechanism, never trigger an undocumented fallback.

## Separation from licensed integrations

A low-level kernel may have an original implementation while the adapter that integrates it with Termux, AndroidX, QEMU, llama.cpp or a GPL application remains governed by the applicable integration/upstream licenses. Do not use the freestanding label to erase derivative/license obligations at integration boundaries.

## Verification receipt

Each kernel should bind at minimum:

`source_sha256 → compiler/version → flags → target/ABI → ELF/object sha256 → test vectors → stdout/stderr digest → exit_code → claim scope`

Unknown values remain `TOKEN_VAZIO`.

## Optimization rule

`smaller/fewer symbols != correct`.

Optimization is accepted only after semantic equivalence or the declared new behavior is tested. Branchless or inline-ASM transformations must preserve a reference test oracle or independently derived invariants.
