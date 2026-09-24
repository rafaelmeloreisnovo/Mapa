# Runtime Gap Ledger R4 — 2026-09-24

Status: IMPLEMENTED_IN_BRANCH / CLAIM_ALLOWED_FALSE

This successor was created after a full-session re-reading focused on details that had previously been treated too shallowly.

## Observed code-level defects routed to remediation

- G0019 — RAFCODEPHI P0.2 receipt authority had two correctness defects on main@5cd6d1e:
  - SHA-256 finalization did not correctly emit a second padding block for messages whose final partial block exceeded 55 bytes.
  - the declared 256-entry CRC32C table materialized only 16 entries; the remaining C-initialized entries were zero.
  - remediation: draft PR #458.

- G0020 — Vectras LayersBit zeroing on main@f67632f wrote a fixed 72 x u64 = 576 bytes although the current LayersBit object is 560 bytes.
  - remediation: draft PR #1145.

These are source defects, not architecture claims. They remain PARTIAL_BOUNDED until exact-head CI and main integration are observed.

## Recursive physical-runtime decomposition

G0010 remains the parent physical ARM execution gap and is now PARTIAL-decomposed into:

- G0013 — scalar ↔ NEON equivalence on physical ARMv7 and ARM64.
- G0014 — instruction-level + runtime proof of the CRC32C hardware path.
- G0015 — physical cache/bandwidth measurement separating DRAM traffic from logical reuse/dual-view throughput.

No child is promoted from CI/emulation/source presence alone.

## Structural gaps exposed by the re-reading

- G0016 — no single canonical adapter yet binds NEON 128-bit execution quanta, the 32 x 128-bit AArch64 register plane and the LayersBit 4096-bit logical state.
- G0017 — bounded state size/no-heap/cache-oriented code does not itself prove hot-set residency in registers/cache.
- G0018 — P0.2 sealing functions are present, but default-branch search did not find an active bootstrap caller nor a canonical append-only persistence/replay sink.

## Invariants

- 32 x 128 bits = 4096 bits is register capacity, not proof of a one-instruction 128→4096 transform.
- logical dual-view reuse != doubled physical DRAM bandwidth.
- hot operational kernel != entire Android/Linux/QEMU image.
- CRC32C = integrity/error detection, not cryptographic authenticity.
- SOURCE != EXECUTION != EVIDENCE != CLAIM.
- TOKEN_VAZIO remains an addressable state.

R3 = <F_ok: defects identified in current authorities + draft remediations + recursive physical gap decomposition + typed structural gaps; F_gap: exact-head CI, merge integration, physical ARM receipts, PMU/cache evidence, canonical NEON128↔4096 adapter, P0.2 active append-only call graph; F_next: consume PR #1145/#458 exact-head gates, then supersede G0019/G0020 state without closing unrelated runtime gaps.>
