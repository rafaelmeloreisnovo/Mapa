# ACTIVE REPOSITORY CURRENT-HEAD EXECUTION MATRIX — V3

status: `MATERIALIZED_CURRENT_HEAD_EXECUTION_BOUNDARY`
claim_allowed: `false`
release_allowed: `false`

## Resultado principal

A coorte implementation-rich permanece com identidade/tree fechada em 20/20, mas execução é um eixo separado.

### Percentuais atuais

- **Current-HEAD project execution observed:** `1/20 = 5%`
- **Current-HEAD project PASS observed:** `1/20 = 5%`
- **Current-HEAD project FAIL after actual steps:** `0/20 = 0%`
- **Strict reproducibility closed:** `0/20 = 0%`
- **Exact-HEAD provider-startup failure:** `4/20 = 20%`
- **Execution unobserved/non-qualifying:** `15/20 = 75%`

The 5% observed PASS must not be mislabeled as strict reproducibility.

## Why strict reproducibility is still 0%

`rafaelmeloreisnovo/GEOMETRIA_SOLAR_Maia_Inca@9a66958c...` is the only repository in the cohort with verified current-HEAD project validation steps observed in this pass. Run `32819806079`, job `97715355081`, executed on Ubuntu 24.04.4 / runner 2.336.0 / image version 20260816.277.1 / git 2.55.0 and completed successfully.

Observed project outputs include:

- markdownlint-cli2 `0.23.2`: `Summary: 0 issues`
- `validate_calendar_matrix.py --check`: `[OK] matrix valid: records=10 relations=9`
- `cycle_phase_features.py --self-test`: `PASS cycle_phase_features`
- required root-file gate: PASS
- docs-directory gate: PASS

However the workflow declares `runs-on: ubuntu-latest`, installs `markdownlint-cli2` without a pinned package version, and emits no workflow artifact. Therefore it is classified:

`PASS_OBSERVED_REPLAYABLE_BOUNDED`

not:

`STRICT_REPRODUCIBLE`

The run log records the environment that happened to execute, making the event auditable and replayable in a bounded sense, but it does not guarantee deterministic future environment reconstruction.

## Provider re-run probe performed now

Four exact-HEAD failed runs were re-run without modifying source code:

| Repository | Run | Attempt | HEAD | Job | Result | Steps |
|---|---:|---:|---|---|---|---|
| Rafaelia_Core | 32689068745 | 2 | `f4c0e6ab...` | Publish benchmark metrics into docs | failure | none observed |
| RafNet-Core | 31804298183 | 2 | `1a772441...` | runtime-evidence | failure | none observed |
| nanoGPT | 32932352408 | 2 | `d839c0d0...` | falsify | failure | none observed |
| privadoFazendo | 31855741833 | 2 | `4ab686f2...` | security-regression | failure | none observed |

All four repeated the same startup boundary on attempt 2. Therefore:

`PROVIDER_STARTUP_FAIL -> code_execution=TOKEN_VAZIO`

They do **not** count as executed, PASS, or CODE_FAIL.

## 20×gate matrix

| # | Repository | Current-HEAD state | Executed? | PASS? | Strict reproducible? |
|---:|---|---|---:|---:|---:|
| 1 | Rafaelia_Core | PROVIDER_STARTUP_FAIL attempt 2 | no | no | no |
| 2 | RafNet-Core | PROVIDER_STARTUP_FAIL attempt 2 | no | no | no |
| 3 | nanoGPT | PROVIDER_STARTUP_FAIL attempt 2 | no | no | no |
| 4 | Fisica | CI_DEFINED_EXECUTION_UNOBSERVED | no | no | no |
| 5 | GEOMETRIA_SOLAR_Maia_Inca | PASS_OBSERVED_REPLAYABLE_BOUNDED | **yes** | **yes** | no |
| 6 | privadoFazendo | PROVIDER_STARTUP_FAIL attempt 2 | no | no | no |
| 7 | ZIPRAF_CORE | NO_ACTIONS_RUN_OBSERVED | no | no | no |
| 8 | Semente | NO_ACTIONS_RUN_OBSERVED | no | no | no |
| 9 | rafaelia-core-enterprise | OLD_SHA_PLATFORM_RUN_ONLY | no | no | no |
| 10 | templo-vivo-arcs | EXACT_HEAD_PLATFORM_AUTOMATION_ONLY | no | no | no |
| 11 | instituto-Rafael/RAFAELIA_CORE | NO_ACTIONS_RUN_OBSERVED | no | no | no |
| 12 | instituto-Rafael/Zrf | NO_ACTIONS_RUN_OBSERVED | no | no | no |
| 13 | instituto-Rafael/Bitraf-Bit-quantum | NO_ACTIONS_RUN_OBSERVED | no | no | no |
| 14 | instituto-Rafael/ESTADO-FRACTAL-HAJA | NO_ACTIONS_RUN_OBSERVED | no | no | no |
| 15 | instituto-Rafael/Clay-Maths | NO_ACTIONS_RUN_OBSERVED | no | no | no |
| 16 | instituto-Rafael/Atomic_EX_WASTE | NO_ACTIONS_RUN_OBSERVED | no | no | no |
| 17 | instituto-Rafael/Eletron-efeitos-qu-ntico | NO_ACTIONS_RUN_OBSERVED | no | no | no |
| 18 | instituto-Rafael/Whilehole | NO_ACTIONS_RUN_OBSERVED | no | no | no |
| 19 | instituto-Rafael/Etica-nas-Intelig-ncia-artificial- | NO_ACTIONS_RUN_OBSERVED | no | no | no |
| 20 | instituto-Rafael/Unify_Teory_of_mission_holly_espiritual_ciencias_ | NO_ACTIONS_RUN_OBSERVED | no | no | no |

## Interpretation

The denominator is no longer discovery coverage. It is the fixed 20-repository implementation-rich cohort.

`P_executado = 1/20 = 5%`

`P_pass = 1/20 = 5%`

`P_reprod_strict = 0/20 = 0%`

This does not mean 95% of the repositories are broken. It means current-HEAD project execution evidence satisfying the contract is absent or non-qualifying for 19/20, and strict reproducibility is not yet closed for any repository.

## F_next

1. Harden GEOMETRIA_SOLAR_Maia_Inca from replayable-bounded to strict reproducibility: pin dependency versions/environment sufficiently and emit a machine-readable receipt/artifact tied to HEAD/tree.
2. Treat the four repeated zero-step failures as a provider gate; diagnose/replace the execution route rather than editing code to chase a non-code failure.
3. For NO_ACTIONS_RUN_OBSERVED repositories, bind repository-native runnable gates first; avoid generic CI that only creates green badges without testing project substance.
4. Only after actual project steps run, classify `PASS_REPRODUCIBLE`, `FAIL_REPRODUCIBLE`, or a bounded equivalent.

## R3

- F_ok: 20×gate matrix materialized; four provider failures re-probed; one real current-HEAD PASS bound with logs and environment.
- F_gap: strict reproducibility remains 0/20; 19/20 lack qualifying current-HEAD project execution evidence.
- F_next: convert the GEOMETRIA bounded PASS into the first strict receipt, then consume the provider and no-run gaps without conflating them with code quality.
