# ACTIVE REPOSITORY CURRENT-HEAD EXECUTION MATRIX — V3.1

status: `FIRST_STRICT_REPRODUCIBLE_CORE_CLOSED`
claim_allowed: `false`
release_allowed: `false`

V3 is preserved as the historical pre-promotion snapshot. V3.1 records only the verified delta.

## Percentuais atuais

- **Current-HEAD project execution observed:** `1/20 = 5%`
- **Current-HEAD project PASS observed:** `1/20 = 5%`
- **Current-HEAD project FAIL after actual steps:** `0/20 = 0%`
- **Strict reproducible project-core closed:** `1/20 = 5%`
- **Exact-HEAD provider-startup failure:** `4/20 = 20%`
- **Execution unobserved/non-qualifying:** `15/20 = 75%`

The useful denominator remains the fixed 20-repository implementation-rich cohort.

## Promotion: GEOMETRIA_SOLAR_Maia_Inca

Previous state:

`PASS_OBSERVED_REPLAYABLE_BOUNDED @ 9a66958cb35813fae2feeac3d348c69273f09b76`

New verified default-branch state:

`STRICT_REPRODUCIBLE_CORE_PASS @ 0d4d23210414dd1ff6582d453ffbc4009df5168a`

tree:

`c607c1dd9229bf09ba57975b31a55270e5109bd3`

Promotion PR: `GEOMETRIA_SOLAR_Maia_Inca#7`.

### Current-main receipt

- workflow: `.github/workflows/reproducible-core.yml`
- run: `32943310618`
- job: `98098654246`
- conclusion: `success`
- immutable project container: `python:3.12.11-slim-bookworm@sha256:519591d6871b7bc437060736b9f7456b8731f1499a57e22e6c285135ae657bf7`
- checkout action commit: `11d5960a326750d5838078e36cf38b85af677262`
- upload-artifact action commit: `ea165f8d65b6e75b540449e92b4886f43607fa02`
- receipt payload SHA-256: `417c6b653e40d7812bd6ddd8a7f305bb9e8485c581c0144f356708353d4e7b0d`
- artifact id: `9597299796`
- artifact SHA-256: `b518c74da99081bc7108d77a275c1e9a591447da3cf5a772b37b6d4f9a61e1b7`

### Gates actually executed

All completed successfully on the exact current `main` HEAD:

1. container initialization from the immutable digest;
2. immutable checkout action revision;
3. `validate_calendar_matrix.py --check`;
4. `cycle_phase_features.py --self-test`;
5. required-root-files gate;
6. docs-directory gate;
7. machine-readable receipt generation;
8. artifact upload;
9. artifact digest binding to the run summary.

Observed project outputs include:

- `[OK] matrix valid: records=10 relations=9`
- `PASS cycle_phase_features`
- `PASS required_root_files`
- `PASS docs_directory files=6`
- `all_project_gates_passed=true`

## Exact boundary of “strict”

The project core is now reproducible under the declared immutable container and HEAD-bound receipt contract. This is enough to count the repository in `P_reprod_strict_core`.

It does **not** claim the entire GitHub-hosted orchestration layer is hermetic. GitHub still controls the hosted runner and forces the JavaScript runtime used by pinned Actions. Therefore:

`STRICT_REPRODUCIBLE_CORE_PASS != FULL_PROVIDER_HERMETICITY`

It also does not promote scientific claims:

`SOFTWARE/DATA REPRODUCIBILITY != EMPIRICAL SCIENTIFIC VALIDATION`

`scientific_empirical_claims_validated=false`

`claim_allowed=false`

## 20×gate delta

Only one row changes from V3:

| # | Repository | Current-HEAD state | Executed? | PASS? | Strict reproducible core? |
|---:|---|---|---:|---:|---:|
| 5 | GEOMETRIA_SOLAR_Maia_Inca | **STRICT_REPRODUCIBLE_CORE_PASS** | **yes** | **yes** | **yes** |

All other 19 rows retain their V3 execution classification until new evidence is observed.

## Interpretation

`P_executado = 1/20 = 5%`

`P_pass = 1/20 = 5%`

`P_reprod_strict_core = 1/20 = 5%`

This is the first actual closure of the metric the audit was seeking. The next useful movement is not repository discovery; it is `1/20 -> 2/20` through another exact-current-HEAD native gate and receipt.

## F_next

1. Inspect `rafaelmeloreisnovo/Fisica` at its current HEAD and bind the native geophysical-transduction gate into a reproducible receipt, preserving `synthetic fixture != empirical physical validation`.
2. Then inspect `rafaelmeloreisnovo/ZIPRAF_CORE` tests/tools as the next no-run executable candidate.
3. Keep Rafaelia_Core, RafNet-Core, nanoGPT and privadoFazendo classified at `PROVIDER_STARTUP_FAIL` while their jobs have zero project steps; do not manufacture CODE_FAIL or PASS.

## R3

- F_ok: first current-main strict-reproducible project core closed; receipt + artifact digest + immutable project environment bound.
- F_gap: 19/20 do not yet have strict current-HEAD core receipts; four remain provider-gated.
- F_next: target `2/20` with Fisica, then ZIPRAF_CORE.
