# Freestanding Authorial Kernel Contract V1

Status: ENGINEERING_CONTRACT / NOT_LEGAL_CLEARANCE

For modules intentionally rebuilt as RAFAELIA-original low-level kernels, the target contract is:

- freestanding ABI;
- no libc dependency;
- no malloc/heap/GC;
- no hidden runtime helpers unless explicitly audited;
- no compatibility tail/shadow layer unless required by a documented interface;
- explicit entry/exit ABI;
- minimal exported symbol set;
- dead-code and unused-symbol elimination;
- bounded loops or proofs/measurements for iteration counts where applicable;
- branch minimization only where it does not reduce correctness or side-channel safety;
- no undefined dependence on host process state;
- deterministic fixtures where deterministic behavior is claimed;
- source/ref/hash receipt for every promoted binary.

`FREESTANDING_PASS != AUTHORSHIP_PASS != LICENSE_PASS`.

A module may satisfy this technical contract and still be class B/C/D until provenance and rights gates close.
