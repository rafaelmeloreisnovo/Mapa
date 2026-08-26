# ACTIVE REPOSITORY EXACT BINDINGS — 2026-08-26 — V2

status: `MATERIALIZED_EXACT_BINDING_TRANCHE_1`

claim_allowed: `false`
release_allowed: `false`
base: `Mapa/main@12b3fbe453ad57643d79c62e70b3ed4ea63067a3`
predecessor: `ACTIVE_REPOSITORY_BULK_EXAMINATION_20260826_V1`

## Purpose

V1 routed 82/82 pending repositories. V2 changes the evidence level: a repository is not promoted from commit history, documentation volume, or a workflow file alone. Each record must bind the current default branch, exact HEAD, root tree, provenance/license surface, workflow state and execution boundary.

Invariant:

`VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM`

`TOKEN_VAZIO != PASS != FAIL`

A GitHub Actions run with `conclusion=failure` and zero observed steps is classified `PROVIDER_STARTUP_FAIL`; it is **not** a code failure.

## Tranche 1 — six implementation-rich repositories

| Repository | Exact HEAD/tree | Provenance | CI on exact HEAD | Branch protection | Runtime/empirical |
|---|---|---|---|---|---|
| `Rafaelia_Core` | BOUND | TOKEN_VAZIO (`LICENSE`/`LICENSE.md` absent at probed paths) | `PROVIDER_STARTUP_FAIL`, 0 steps | OFF | TOKEN_VAZIO |
| `RafNet-Core` | BOUND | `LICENSE` is incomplete stub (`MIT License` only), API `NOASSERTION` | `PROVIDER_STARTUP_FAIL`, 0 steps | OFF | TOKEN_VAZIO |
| `nanoGPT` | BOUND | full MIT, upstream copyright preserved | `PROVIDER_STARTUP_FAIL`, 0 steps | OFF | partial local receipts exist; not rebound as HEAD-exact remote execution here |
| `Fisica` | BOUND | TOKEN_VAZIO (`LICENSE`/`LICENSE.md` absent at probed paths) | workflow defined; 0 main runs observed | OFF | TOKEN_VAZIO |
| `GEOMETRIA_SOLAR_Maia_Inca` | BOUND | full MIT + academic citation note | **PASS_BOUNDED** on exact HEAD | OFF; web signoff required | empirical science remains TOKEN_VAZIO |
| `privadoFazendo` | BOUND | full MIT | `PROVIDER_STARTUP_FAIL`, 0 steps | OFF | current-tree certification TOKEN_VAZIO |

### Exact bindings

- `Rafaelia_Core/main@f4c0e6ab51bcd74af57eb0ef8c120e76851a0428`, tree `38e6b34e904faf57543c275b046a9d01e6f23350`.
- `RafNet-Core/main@1a772441277bddf9a4daf5a4d87a292f32972fb8`, tree `03cd32c78d93bb320b3283f7d7dc26b27b9315cc`.
- `nanoGPT/master@d839c0d08910dd3bbe87b5e2da40a0ea2c11da61`, tree `7c0c064459dca3a6b91e15f2d0e935ff9ae3ae88`.
- `Fisica/main@4ef974a8eab07e8154ff90308e0dafb251ce1078`, tree `f9ab7461db3093961f83a2f988925924c614df7d`.
- `GEOMETRIA_SOLAR_Maia_Inca/main@9a66958cb35813fae2feeac3d348c69273f09b76`, tree `79ed17f0ac44517f439e01d0f1c5196b5d3eb3e3`.
- `privadoFazendo/master@4ab686f2c233800fe65c5cfbd7c43017ecd086db`, tree `1a83057569b1ba8ecd47ea087061a7e388a621a0`.

All six observed branch heads were unprotected at provider level. This is a governance risk axis and does not imply defective code.

## CI classification

### Provider-startup failures — no code execution observed

Four repositories have latest exact-HEAD Actions runs that ended `failure` but exposed zero job steps:

- `Rafaelia_Core` — run `32689068745`.
- `RafNet-Core` — run `31804298183`.
- `nanoGPT` — run `32932352408`.
- `privadoFazendo` — run `31855741833`.

Correct state:

`PROVIDER_STARTUP_FAIL -> code_execution=TOKEN_VAZIO`

Not allowed:

`failure -> CODE_FAIL`

### CI defined but not executed in observed branch history

`Fisica` contains `.github/workflows/geophysical-transduction.yml`, including compilation, registry validation, explicit TOKEN_VAZIO assertions, synthetic-receipt checks and adversarial tests. The workflow is path-filtered on pull requests plus `workflow_dispatch`; the Actions query for `main` returned zero runs. Therefore:

`CI_DEFINED != CI_EXECUTED`

and provider execution remains `TOKEN_VAZIO`.

### Exact-HEAD bounded PASS

`GEOMETRIA_SOLAR_Maia_Inca` has Actions run `32819806079` on exact HEAD `9a66958...`, conclusion `success`, with executed steps validating Markdown, the calendar matrix contract, Calendar Round/cycle-phase self-test, required root files and docs structure.

This supports only:

`CI_PASS_BOUNDED(workflow_scope)`

It does **not** establish empirical astronomical, causal, historical, physical, or scientific claims.

## Provenance findings

- `nanoGPT`: full MIT text bound to exact HEAD; copyright `2022 Andrej Karpathy` must remain preserved for upstream-derived material.
- `GEOMETRIA_SOLAR_Maia_Inca`: full MIT text plus academic citation note bound to exact HEAD.
- `privadoFazendo`: full MIT text bound to exact HEAD.
- `RafNet-Core`: API says `NOASSERTION`; the exact `LICENSE` file contains only `MIT License`, so the grant text is incomplete and cannot be treated as a complete standard MIT license.
- `Rafaelia_Core` and `Fisica`: API license is null and `LICENSE`/`LICENSE.md` were not found at the exact HEAD paths probed. This is `TOKEN_VAZIO`, not a claim that no rights or license information exists anywhere else.

## Quantitative closure for this stage

- exact HEAD + root tree: **6/6**
- priority implementation-rich cohort bound: **6/20 = 30%**
- protected default branches: **0/6**
- complete license texts bound: **3/6**
- incomplete license stub: **1/6**
- provenance TOKEN_VAZIO at probed standard paths: **2/6**
- exact-HEAD provider CI PASS, bounded scope: **1/6**
- provider startup failure with zero steps: **4/6**
- CI defined but execution unobserved: **1/6**
- global runtime/empirical promotions: **0**

These are closure percentages for the V2 binding stage, **not scalar repository maturity scores**.

## Gaps that now have concrete shape

1. Branch protection is absent on all six default branches observed.
2. Provider execution infrastructure is currently a major blocker: four exact-HEAD failures never entered the first step.
3. Provenance needs remediation on `RafNet-Core`, `Rafaelia_Core`, and `Fisica`.
4. `nanoGPT` remains architecturally split between the PyTorch main path and the additive freestanding triad; checkpoint equivalence, tensor-free training and 2x speedup remain unpromoted.
5. `Fisica` correctly encodes synthetic fixture and TOKEN_VAZIO boundaries, but provider execution and physical/empirical receipt closure remain open.
6. `GEOMETRIA_SOLAR_Maia_Inca` currently has the strongest exact-HEAD provider CI evidence in this tranche, but the PASS scope is software/document contract validation, not empirical validation.
7. `privadoFazendo` has a substantial remediation/test design surface, but historical remediation commits are not a substitute for a current exact-tree executable security receipt.

## F_next

Continue the same exact-binding contract over the remaining 14 implementation-rich priority repositories, then:

`HEAD/tree -> provenance -> tests/workflow -> exact execution -> receipt -> runtime/empirical -> normalized domain score`

No single maturity percentage is authorized until non-applicable dimensions are explicitly marked `N/A` and current evidence pointers exist.

## R3

- F_ok: six priority repositories have exact HEAD/tree bindings and differentiated CI/provenance states.
- F_gap: fourteen priority repositories still need V2 exact binding; provider startup failures and provenance gaps remain open.
- F_next: bind the next implementation-rich tranche and route provider/runtime blockers without converting TOKEN_VAZIO into failure.
