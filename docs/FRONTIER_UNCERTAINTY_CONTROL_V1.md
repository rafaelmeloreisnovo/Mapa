# FRONTIER UNCERTAINTY CONTROL V1

STATE: `MATERIALIZED_UNTESTED`  
CLAIM_ALLOWED: `false`  
CUT: `2026-10-01T17:30:00-03:00`

## Purpose

This control plane selects the smallest evidence-producing delta that maximizes uncertainty reduction, risk reduction, dependency unlock, and academic reproducibility without silently promoting claims.

It does **not** score truth, intelligence, novelty, authorship, or scientific validity. The score is an operational queueing heuristic only.

## Epistemic invariants

- `SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM`
- `TOKEN_VAZIO != 0`
- `IMPLEMENTED_UNTESTED != PASS`
- `LIVE_PAGE != SCIENTIFIC_VALIDATION`
- `MERGED != VERIFIED`
- `SAME_HASH != AUTHORITY`

## Standards as execution controls, not certification claims

This artifact operationalizes the following disciplines as work controls:

- **BCP 14 / RFC 2119 + RFC 8174:** uppercase `MUST`, `SHOULD`, `MAY` are reserved for explicit normative requirements.
- **IEEE 1012:** verification of conformance and validation of intended use remain distinct evidence problems.
- **ISO/IEC/IEEE 29148:** requirements are made explicit, attributable, testable, and traceable across lifecycle changes.
- **ISO/IEC 27001 + ISO/IEC 27005:** evidence and execution surfaces are treated with confidentiality/integrity/availability and risk treatment boundaries.
- **ISO 8000:** raw, normalized, semantic, and derived data remain distinguishable and quality characteristics must be measurable.
- **ISO 9001 process approach:** inputs, activities, controls, outputs, measurements, risk and continual improvement are explicit.
- **Six Sigma DMAIC:** `DEFINE -> MEASURE -> ANALYZE -> IMPROVE -> CONTROL`; an improvement action does not backfill missing measurement or analysis evidence.

No standards-compliance or certification claim is made by this document.

## Frontier leverage score

For a work item with grounded factors:

`S = ((U + R + D + A) * E) / C`

where:

- `U`: uncertainty reduction, 0..5
- `R`: risk reduction, 0..5
- `D`: dependency unlock, 0..5
- `A`: academic reproducibility gain, 0..5
- `E`: evidence readiness, 0..5
- `C`: effort, 1..5

Maximum = 100. If a required factor is not grounded, the score state is `TOKEN_VAZIO_SCORE` and it MUST NOT be used for promotion.

## Current cut

### Mapa

`rafaelmeloreisnovo/Mapa@8b6bea18d0ffd23e17781b5f7152967daaa990db`

Jekyll deployment workflow was added. The observed runner rejected version-tag Action references because this repository requires full-length Action commit SHAs. That is a repository policy failure before Jekyll build execution, not evidence that Jekyll content is defective.

### BLAKE3

`rafaelmeloreisnovo/BLAKE3@990e3d5a5153c0a3448b633ddaed199d9e6fff18`

GitHub Pages Jekyll build and deploy completed successfully in run `36921898866`. Scope: deployment only.

### RLL

`instituto-Rafael/relativity-living-light@4308b1b7670176e449239b4b17681e728c66b9a3`

A Jekyll deployment workflow was added. The workflow matrix changed and requires scope-specific revalidation. This does not alter scientific claim gates.

### Drive

`RAFAELIA — CURRENT_STATE Ω — HOTSTATE V4.2`, Drive id `1d0J5SkF2S2emBq6jLuTkhYVaSOQiWazJWyRCTMJ-iRI`, still records older Mapa state. GitHub↔Drive parity is therefore stale at this cut.

## Ordered frontier

1. **FUC-001 — Federated current-state and deployment-authority reconciliation.** Score 95.0. Close only when each publication surface has one authoritative producer or an explicit namespaced multi-producer contract, and Drive records exact heads plus scoped run evidence.
2. **FUC-002 — RMR auxiliary parser fail-closed hardening.** Score 32.5. Negative malformed/truncated/overflow fixtures; do not modify BLAKE3 cryptographic core.
3. **FUC-003 — SYMBOL_GRAMMAR_V2.** Score 30.0. Preserve glyph/codepoint/namespace/sense version and test Unicode and semantic collisions adversarially.
4. **FUC-004 — RLL reproducibility package.** Score 14.25. Freeze data/environment/scripts/claim-to-result map and seek independent scoped reproduction.
5. **FUC-005 — HASH→ERASURE→RIVER7→RECONSTRUCT→HASH lab.** Score 13.0. Finite known-erasure scope only; fail closed outside supported conditions.
6. **FUC-006 — Physical ARM32/ARM64 artifact→device receipts.** Score 11.4. Exact artifact hash, ABI, install, runtime and hardware receipts; emulation cannot backfill physical execution.

## False-gold filter

The controller rejects apparent progress that does not reduce the target uncertainty:

- `LIVE_PAGE` is not code correctness or scientific validity.
- `MERGED_PR` is not a verified result.
- `GREEN_CI` is not universal PASS.
- `SAME_HASH` is not producer authority.
- `SYMBOLIC_COHERENCE` is not empirical evidence.
- `BENCHMARK_WIN` is not universal superiority.
- `FINITE_MODEL_PROOF` is not physical implementation.
- `MORE_PERMUTATIONS` is not more knowledge.

This is the intended meaning of going after the `TOKEN_VAZIO` behind other `TOKEN_VAZIO`s: unknown dependencies, unknown authority, unknown falsifiers, unknown closure criteria and unknown measurement quality become typed gaps rather than being silently converted into confidence.

## Academic frontier

The strongest next academic transformation is not another broad claim. It is a reproducibility-grade research artifact package where each declared result maps to a frozen source, executable procedure, environment, result receipt and falsifier. Artifact availability, artifact functionality and independent reproduction remain distinct states.

## R3

`F_ok`: frontier controller materialized from the current GitHub/Drive cut; scoped BLAKE3 deployment PASS preserved; Mapa policy failure separated from Jekyll validity.  
`F_gap`: publication authority remains unresolved across surfaces; Drive is stale; scientific/device gaps remain separately open.  
`F_next`: execute FUC-001 first, then recompute the frontier rather than following this ordering blindly after state changes.
