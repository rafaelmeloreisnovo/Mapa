# RAFAELIA Linker Memory-Map Contract V1

Gap: `G071`  
State: `SPEC_DEFINED_LOCAL / PER-TARGET_MAP_RECEIPTS_OPEN / claim_allowed=false`

For strict freestanding targets, each final ELF receipt must state:
- entry point;
- target architecture/ABI;
- section virtual/file sizes;
- PT_LOAD permissions;
- `.text/.rodata/.data/.bss` sizes;
- dynamic section count;
- runtime relocation count;
- undefined symbol count;
- GNU_STACK/stack executability;
- linker script or linker flag identity.

Baseline strict profile used by the Geo/ZIPRAF line:
- no undeclared dynamic loader dependency;
- no undefined symbols at final link;
- runtime relocations = 0 where static loaderless profile is claimed;
- non-executable stack;
- `data=0` and `bss=0` only where that narrower profile is explicitly claimed;
- W^X: writable and executable permissions must not be silently combined.

A linker map is evidence about binary layout. It is not evidence of physical runtime.

`FINAL_LINK_PASS != PHYSICAL_EXECUTION`.
