# Mapa — GAIA_phi Opt-in Navigation Index Delta V1 — 2026-08-12

Mode: append-only / anti-regression / provenance-first.

## Why this delta exists
A prior repository map risked inferring responsibilities from repository names. This delta records the corrected navigation rule: declared role comes from repository contracts/READMEs; material role comes from observed files/code; execution/evidence/claim remain separate states.

## Canonical epistemic chain
`NAME != DECLARED_ROLE != MATERIAL_IMPLEMENTATION != EXECUTION != EVIDENCE != CLAIM`

Unknown or unverified edges are `TOKEN_VAZIO`.

## GAIA_phi role — evidence-backed
Declared federated role: deterministic indexing, evidence manifests and data-state persistence.
Concrete interface: bounded file set + explicit traversal policy + metadata schema -> deterministic manifest + hashes + status report.
Local authority remains in GAIA's C/Python core, module READMEs, tests, generated manifests and repository-specific audits.

## Navigation anchors
1. `GAIA_phi/docs/README.md` — documentary entrypoint.
2. `GAIA_phi/docs/LEVANTAMENTO_ESTRUTURAL_TOTAL.md` — five-level structural map.
3. `GAIA_phi/gaia_core_v2/README.md` — modular deterministic C core.
4. `GAIA_phi/gaia_engines_v2/README.md` — engine lifecycle/metrics.
5. `GAIA_phi/llama_guard/README.md` — deterministic semantic guard.
6. `GAIA_phi/tests/README.md` — fixtures/baselines/regression intent.
7. `GAIA_phi/docs/federation/REPOSITORY_CONTRACT_V1.md` — federation, replay, fail-safe, TOKEN_VAZIO.
8. `GAIA_phi/docs/federation/GAIA_OPTIN_UPSTREAM_SAFETY_DELTA_2026-08-12.md` — opt-in/upstream-safety target and gap ledger (branch `audit/optin-upstream-safety-contract-20260812`, commit `99e576495a8d9c1afd7dd4ddecfbb91bbadf0d78`).

## Architectural intent indexed
`UPSTREAM -> optional GAIA adapter/sidecar -> deterministic observation/manifest -> canonical export -> migration target`

Target invariant: `GAIA_OFF => UPSTREAM_BEHAVIOR_UNCHANGED`.
This is currently a TARGET, not a verified runtime claim.

## Integration taxonomy
`SIDECAR | ADAPTER | WRAPPER | PATCH_UPSTREAM | HARD_DEPENDENCY | TOKEN_VAZIO`

## Priority gaps
- P0 `TV-GAIA-001`: prove/limit upstream unchanged behavior when GAIA is disabled.
- P0 `TV-GAIA-002`: classify every integration edge by coupling taxonomy.
- P1 `TV-GAIA-003`: independent migration/export proof.
- P1 `TV-GAIA-004`: clean-checkout replay receipt.
- P1 `TV-GAIA-005`: Android/Termux ARM64 receipt for current surface.
- P1 `TV-GAIA-006`: payload/schema compatibility matrix.
- P2 `TV-GAIA-007`: historical/current document supersession map.

## Anti-regression rule
Closing a TOKEN_VAZIO requires an evidence reference. A later failure does not delete the previous PASS; it appends a contradictory/new observation with source version and timestamp. No repository-name inference may overwrite a README/contract-backed role.

## Responsibility routing
- Mapa: navigation, relationships, gaps, provenance and state transitions.
- GAIA_phi: local implementation/evidence authority for its indexing/manifest/persistence machinery.
- External scientific/legal/runtime meaning: remains with the producing/validating authority; GAIA indexing alone cannot promote it.

## Next bounded action
Audit GAIA build scripts and integration entrypoints and produce a machine-readable edge ledger with fields: `edge_id`, `source_path`, `target`, `class`, `payload_mutation`, `upstream_mutation`, `rollback_anchor`, `test_ref`, `evidence_ref`, `status`, `F_gap`, `F_next`.
