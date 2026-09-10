# ATLAS:X Ω211 — Geral ↔ Vectras-VM-Android authority boundary

cycle_id: `OMEGA-FED-20260910-211`  
predecessor: `OMEGA-FED-20260910-210`  
state: `DRAFT_AUDITABLE`  
claim_allowed: `false`

## Invariants

`SOURCE ≠ ARTEFATO ≠ EXECUÇÃO ≠ EVIDÊNCIA ≠ CLAIM`  
`TOKEN_VAZIO ≠ 0`

## Source observations

### rafaelmeloreisnovo/Geral

Provider source: `README.md@main`, blob `ee9ca8e2b68d3bbc6dd030539b215541afe66710`.

Observed declarations:

- logical owner: `runtime-maintainer`;
- repository organizes RAFAELIA/VECTRA artifacts in academic and freestanding tracks;
- freestanding track exposes a minimal C core (`include/vectra_core.h`, `src/vectra_core.c`, tests and Makefile), with flags/checkpoints/rollback.

Bounded interpretation: `Geral` is evidence for its own freestanding RAFAELIA/VECTRA core/reference surface. The inspected source does **not** declare it canonical for the Android VM application, Android engine, CI/release pipeline or current Vectras VM documentation.

### rafaelmeloreisnovo/Vectras-VM-Android

Provider source: `README.md@master`, repository default branch `master`.

Observed declarations:

- logical owner: `app-maintainer`;
- README status: `canônico vigente`;
- related sources of truth: `DOC_INDEX.md`, `PROJECT_STATE.md`, `BUILDING.md`, `docs/README.md`;
- `app/`, `engine/`, `tools/ci/`, `.github/workflows/`, `docs/` are classified as **Canônico** and as official source for Android app, engine, CI/release and current documentation;
- `android/` is legacy-compatible, experimental/input directories are explicitly non-promoted, and archive paths are historical;
- official release publisher is `.github/workflows/release-dual-track.yml` subject to the repository's documented signed-release gate.

## Authority reconciliation

The inspected source statements support a non-conflicting bounded partition:

| Domain | Bounded producer/source authority | Evidence state |
|---|---|---|
| Geral freestanding RAFAELIA/VECTRA C core/reference | `rafaelmeloreisnovo/Geral` | `OBSERVED_SOURCE_BOUNDARY` |
| Vectras Android application | `rafaelmeloreisnovo/Vectras-VM-Android:app/` | `OBSERVED_CANONICAL_SOURCE` |
| Vectras engine | `rafaelmeloreisnovo/Vectras-VM-Android:engine/` | `OBSERVED_CANONICAL_SOURCE` |
| Vectras CI/release | `rafaelmeloreisnovo/Vectras-VM-Android:tools/ci/` + `.github/workflows/` | `OBSERVED_CANONICAL_SOURCE` |
| Vectras current technical documentation | `rafaelmeloreisnovo/Vectras-VM-Android:docs/` and routed top-level docs | `OBSERVED_CANONICAL_SOURCE` |

No runtime-execution, build-success or release-success claim is made by this reconciliation.

## Gap transition

### G197-05

- prior: `BLOCKED + TOKEN_VAZIO_RUNTIME_AUTHORITY_BOUNDARY`
- source_pointer: `Geral/README.md@main` + `Vectras-VM-Android/README.md@master`
- missing_field before Ω211: bounded runtime authority versus dedicated Vectras producer
- evidence obtained: explicit, non-conflicting source declarations assigning the Android app/engine/CI/release/docs domain to `Vectras-VM-Android`, while `Geral` describes its own freestanding core surface
- uncertainty_before: producer/domain overlap unresolved
- uncertainty_after: source-domain boundary observed; registry promotion/review remains
- status_after: `OBSERVED_SOURCE_BOUNDARY + BLOCKED_REGISTRY_REVIEW`
- claim_allowed: `false`
- predecessor/lineage: `Ω196→Ω197/G197-05→Ω211`

### G211-01

- TOKEN_VAZIO: `TOKEN_VAZIO_REGISTRY_PROMOTION_REVIEW`
- source_pointer: this Atlas delta + current `indices/repository_authority_registry.json@main`
- missing_field: reviewed/validated canonical registry entries for the bounded Geral/Vectras roles
- blocking_dependency: registry schema/validator review and human/provider governance gate
- evidence_needed: validator PASS on a proposed registry delta and authorized review outcome
- falsifier: a newer authoritative source assigning the same Android app/engine/CI/release domain elsewhere, or validator conflict
- next_probe: prepare/review a minimal registry delta from this bounded source evidence; do not promote claims beyond the declared domains
- owner/authority: repository owner + Mapa control-plane registry review
- urgency: medium
- closure_gate: non-conflicting registry validation + review
- claim_allowed: `false`

## Control

No default-branch write. No merge. No release. No approval. This artifact is a reviewable evidence delta, not a canonical authority promotion.
