# ACTIVE REPOSITORY CURRENT-HEAD EXECUTION MATRIX — V3.3

status: `THIRD_STRICT_REPRODUCIBLE_CORE_CLOSED`
claim_allowed: `false`
release_allowed: `false`

V3, V3.1 and V3.2 remain preserved. V3.3 records the third verified current-main promotion.

## Percentuais úteis agora

- **Current-HEAD project execution observed:** `3/20 = 15%`
- **Current-HEAD project PASS observed:** `3/20 = 15%`
- **Current-HEAD project FAIL after actual steps:** `0/20 = 0%`
- **Strict reproducible project-core closed:** `3/20 = 15%`
- **Exact-current-HEAD provider-startup failure:** `4/20 = 20%`
- **Execution unobserved/non-qualifying:** `13/20 = 65%`

## Strict core #1 — GEOMETRIA_SOLAR_Maia_Inca

`main@0d4d23210414dd1ff6582d453ffbc4009df5168a`

- run `32943310618`
- receipt payload SHA-256 `417c6b653e40d7812bd6ddd8a7f305bb9e8485c581c0144f356708353d4e7b0d`
- artifact SHA-256 `b518c74da99081bc7108d77a275c1e9a591447da3cf5a772b37b6d4f9a61e1b7`

## Strict core #2 — Fisica

`main@06c83a3e7e470613d48963d287f1dc6a34f5f544`

- run `32943882726`
- receipt payload SHA-256 `03e36810a79fde609317785429dc28901162bc680b70641bb6231daa8e4ca5cc`
- artifact SHA-256 `742f112b4ade8cf8fad15348228da00b846ad3101c41380a722ed7af61f03ce3`
- `pytest_suite_included=false`
- `empirical_physical_validation=false`

## Strict core #3 — instituto-Rafael/Zrf

Previous state:

`NO_ACTIONS_RUN_OBSERVED @ ea863fc3c096316412b611ad9c167ad4560c7edc`

New default-branch state:

`STRICT_REPRODUCIBLE_MATHEMATICS_CORE_PASS @ 218a52680954e3c7dcbc230ad5780c632f76480f`

tree:

`1b7207478b12861acfe94bcfa17ed51d249e57a9`

Promotion PR: `instituto-Rafael/Zrf#2`.

### Functional defect corrected

The existing verifier inserted a provider-specific absolute path:

`/home/runner/work/Zrf/Zrf/src`

That made the verifier depend on one runner layout. It now resolves `src/` from `Path(__file__).resolve().parents[1]`, so the same verification entry works inside the immutable container and outside the historical GitHub path.

### Current-main evidence

- workflow: `.github/workflows/reproducible-mathematics-core.yml`
- run: `32944655696`
- job: `98102705625`
- conclusion: `success`
- container: `python:3.12.11-slim-bookworm@sha256:519591d6871b7bc437060736b9f7456b8731f1499a57e22e6c285135ae657bf7`
- checkout pin: `11d5960a326750d5838078e36cf38b85af677262`
- upload-artifact pin: `ea165f8d65b6e75b540449e92b4886f43607fa02`
- receipt payload SHA-256: `e0977adc55244a85b107e76105db40515963e7e11a9472d6d0e456c692ef1381`
- artifact id: `9597781180`
- artifact SHA-256: `cd8072d4c45168a25890347ffa9d84e4607007fe02b2a098db0cf7da052d1b7c`

### Gates actually executed

1. Python bytecode compilation of `src/mathematics.py`, verifier and receipt generator;
2. exact operation registry count `69`;
3. exact IDs `1..69`;
4. 69 unique operation names;
5. 69 callable operation entries;
6. repository numerical sample verifier;
7. HEAD-bound machine-readable receipt;
8. receipt/verifier evidence artifact upload and digest binding.

Observed numerical sample PASS includes:

- derivative of sine at π/4;
- power derivative at x=3;
- natural exponential derivative at x=1;
- sine antiderivative at π;
- power antiderivative at x=3;
- exponential antiderivative at x=0;
- inverse linear example;
- inverse exponential example;
- inverse sine example.

## Mathematical boundary

The registry proves that 69 named/callable operation slots exist and are partitioned as 23 derivatives, 23 antiderivatives and 23 inverses.

The current numerical verifier samples selected functions. Therefore:

`69/69 OPERATION SLOTS PRESENT != 69/69 FORMULAS EXHAUSTIVELY PROVEN`

`all_69_operations_numerically_proven=false`

That deeper property remains a separate test/falsification dimension.

## ZIPRAF_CORE probe — no false promotion

A reproducible AO42 C/KAT gate was prepared on branch `audit/reproducible-ao42-core-v1-20260826` and exposed as draft PR `ZIPRAF_CORE#7`.

Run `32944173439` was executed twice, but both attempts ended before any project step (`steps=null`). Therefore:

`PROVIDER_STARTUP_FAIL -> code_execution=TOKEN_VAZIO`

The PR remains draft and unmerged. ZIPRAF current-main state is not promoted.

## Interpretation

`P_executado = 3/20 = 15%`

`P_pass = 3/20 = 15%`

`P_reprod_strict_core = 3/20 = 15%`

No scalar global technological maturity is implied by these numbers. They measure exact-current-HEAD execution evidence for a bounded native project core.

## F_next

Target:

`3/20 -> 4/20`

Prefer another public implementation-rich repository with native executable substance. Inspect exact current trees before choosing between `instituto-Rafael/Bitraf-Bit-quantum`, `instituto-Rafael/ESTADO-FRACTAL-HAJA`, and other public candidates.

Keep the four current-default provider-startup cases and ZIPRAF's branch probe separate from code quality.

## R3

- F_ok: `3/20` current-main strict-reproducible cores — GEOMETRIA, Fisica, Zrf — each with HEAD-bound receipt and artifact digest.
- F_gap: `17/20` without strict current-main core receipts; four exact-current-head cases remain provider-gated; ZIPRAF prepared gate remains unexecuted.
- F_next: target `4/20` through the strongest public native executable candidate; separately expand Zrf from sampled verification toward per-operation falsifiers without claiming exhaustive proof prematurely.
