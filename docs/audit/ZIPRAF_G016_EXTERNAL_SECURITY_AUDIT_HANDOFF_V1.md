# ZIPRAF G016 — Independent External Security Audit Handoff V1

State: `HANDOFF_READY / INDEPENDENT_AUDIT_TOKEN_VAZIO`  
Route: `ATLAS-X-ZIPRAF-FREESTANDING-GEO-COMPILER-20260909`  
Claim gate: `claim_allowed=false`

## Audit object

Primary producer: `rafaelmeloreisnovo/ZIPRAF_CORE#9`.

The audit target is the exact PR head selected by the reviewer, not a moving branch name. Record the commit SHA before testing.

In-scope source families:

- `include/raf_geo_word.h`
- `src/raf_geo_word.c`
- `tests/test_raf_geo_word.c`
- `tests/raf_geo_freestanding_smoke.c`
- `tests/raf_geo_entry.S`
- `tools/test_raf_geo_word.sh`
- `tools/run_raf_geo_runtime_receipt.sh`
- `docs/RAFAELIA_GEO_TURING_FREESTANDING_PROFILE_V1.md`
- `docs/RAFAELIA_GEO_TURING_MODULE_PROFILES_V1.json`
- `docs/RAFAELIA_GEO_COMPILER_LINKER_MATRIX_20260909.md`

Context/custody predecessor: uploaded `ra_omega.zip` SHA-256 `b800f88ea26a6308c1e5dcf7d33ede392df10e67efec92eaa3d685c8c816ca59` and its separately recorded ZIPRAF custody chain.

## Independence requirement

G016 is not closed by the author, the assistant that produced the patch, or a CI run controlled only by the same producer. The reviewer must identify organization/person/tooling authority and disclose material conflicts of interest. Automated scanners may contribute evidence but do not alone establish human/organizational independence.

## Threat model / required checks

1. **Carrier integrity boundary**
   - payload42 mutation/recovery behavior;
   - group/epistemic out-of-range inputs;
   - witness8 collision demonstration and confirmation that it is never used as authentication.

2. **Epistemic confusion attacks**
   - ZERO vs NOOP vs TOKEN_VAZIO vs VOID confusion;
   - attempts to promote TOKEN_VAZIO to VALID without evidence state transition.

3. **ABI / parser boundary**
   - x86_64, ARMv7 EABI5, AArch64 object/final-link audit;
   - integer width/alignment/endianness assumptions;
   - malformed or adversarial words.

4. **Link/runtime boundary**
   - undefined symbols = 0;
   - runtime relocations = 0 for final loaderless images;
   - dynamic dependencies = 0;
   - writable static data/bss = 0;
   - entry/exit syscall correctness;
   - W^X/noexecstack observation where toolchain exposes it.

5. **Compiler profile robustness**
   - reproduce O0/Os/Oz/O2 size matrix;
   - confirm `-Oz` semantic KAT equivalence;
   - inspect whether optimization introduces UB or architecture-specific drift.

6. **Negative tests**
   - one-bit payload tamper;
   - one-bit metadata tamper;
   - witness tamper;
   - invalid epistemic states;
   - invalid groups;
   - build without required linker constraints must not be accepted as the same evidence class.

7. **Delegated authentication boundary**
   - verify that no documentation/code calls witness8 a MAC/signature;
   - if the carrier is transported inside signed ZIPRAF evidence, audit the external signature binding independently; do not infer it from this carrier.

8. **Memory-safety / UB**
   - sanitizer/reference-host pass where compatible;
   - static-analysis findings classified by exact source line and reproducibility;
   - absence of allocator/heap does not waive integer/ABI/control-flow review.

## Required independent receipt

The auditor should emit immutable JSON/text containing:

`auditor_identity, independence_statement, target_commit_sha, tool_versions, architecture, test_commands, source_hashes, binary_hashes, positive_results, negative_results, unresolved_findings, severity, reproduction_steps, signed_timestamp_or_external_timestamp_anchor`.

Every unresolved material finding remains a typed gap. A PASS is scoped to the tested commit and environment.

## Closure

`G016=PASS_EXTERNAL_AUDIT` only after the independent receipt is attached to a successor and its identity/hash is routed through Mapa + longitudinal memory. This handoff alone does not close G016.
