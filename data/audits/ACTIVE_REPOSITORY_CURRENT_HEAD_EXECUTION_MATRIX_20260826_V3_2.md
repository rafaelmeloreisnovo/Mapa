# ACTIVE REPOSITORY CURRENT-HEAD EXECUTION MATRIX — V3.2

status: `SECOND_STRICT_REPRODUCIBLE_CORE_CLOSED`
claim_allowed: `false`
release_allowed: `false`

V3 and V3.1 remain preserved. V3.2 records the second verified promotion only.

## Percentuais úteis agora

- **Current-HEAD project execution observed:** `2/20 = 10%`
- **Current-HEAD project PASS observed:** `2/20 = 10%`
- **Current-HEAD project FAIL after actual steps:** `0/20 = 0%`
- **Strict reproducible project-core closed:** `2/20 = 10%`
- **Exact-HEAD provider-startup failure:** `4/20 = 20%`
- **Execution unobserved/non-qualifying:** `14/20 = 70%`

## Strict core #1 — GEOMETRIA_SOLAR_Maia_Inca

- current main HEAD: `0d4d23210414dd1ff6582d453ffbc4009df5168a`
- run: `32943310618`
- receipt payload SHA-256: `417c6b653e40d7812bd6ddd8a7f305bb9e8485c581c0144f356708353d4e7b0d`
- artifact SHA-256: `b518c74da99081bc7108d77a275c1e9a591447da3cf5a772b37b6d4f9a61e1b7`

## Strict core #2 — Fisica

Previous state:

`CI_DEFINED_EXECUTION_UNOBSERVED @ 4ef974a8eab07e8154ff90308e0dafb251ce1078`

New default-branch state:

`STRICT_REPRODUCIBLE_GEOPHYSICAL_CORE_PASS @ 06c83a3e7e470613d48963d287f1dc6a34f5f544`

tree:

`3ec45fa1290f5c6f800403616730e0793145fcb9`

Promotion PR: `Fisica#9`.

### Current-main evidence

- workflow: `.github/workflows/reproducible-geophysical-core.yml`
- run: `32943882726`
- job: `98100375198`
- conclusion: `success`
- container: `python:3.12.11-slim-bookworm@sha256:519591d6871b7bc437060736b9f7456b8731f1499a57e22e6c285135ae657bf7`
- checkout pin: `11d5960a326750d5838078e36cf38b85af677262`
- upload-artifact pin: `ea165f8d65b6e75b540449e92b4886f43607fa02`
- receipt payload SHA-256: `03e36810a79fde609317785429dc28901162bc680b70641bb6231daa8e4ca5cc`
- artifact id: `9597503232`
- artifact SHA-256: `742f112b4ade8cf8fad15348228da00b846ad3101c41380a722ed7af61f03ce3`

### Executed project scope

All passed on the exact current `main` HEAD:

1. compile the four deterministic core modules;
2. validate geophysical DOI registry;
3. validate solid-Earth/hydrology registry;
4. verify empty preregistration remains `TOKEN_VAZIO` / `claim_allowed=false`;
5. verify physical-transduction invariant remains fail-closed;
6. build synthetic raw-data receipt and assert `SYNTHETIC_FIXTURE`, `winner=TOKEN_VAZIO`, synchronized fixture clock and `claim_allowed=false`;
7. execute Earth-hum period comparator;
8. execute stdlib adversarial smoke for invalid oscillator, missing orientation and unknown mechanism;
9. emit HEAD-bound machine-readable receipt;
10. upload and digest-bind the receipt artifact.

## Boundaries deliberately not crossed

`pytest_suite_included=false`

The original pytest suite remains a separate completeness dimension and is not retroactively claimed by this strict-core receipt.

`empirical_physical_validation=false`

The fixture is synthetic by construction. Passing this gate proves the software/data contract and fail-closed behavior, not a real precursor, causal geophysical mechanism or empirical physical discovery.

`STRICT_REPRODUCIBLE_CORE_PASS != FULL_PROVIDER_HERMETICITY != EMPIRICAL_PHYSICAL_VALIDATION`

## Delta from V3.1

| Repository | V3.1 | V3.2 |
|---|---|---|
| GEOMETRIA_SOLAR_Maia_Inca | STRICT core PASS | STRICT core PASS |
| Fisica | execution unobserved | **STRICT geophysical core PASS** |

The remaining 18 repositories retain their previous classifications until new current-HEAD evidence exists.

## F_next

The next useful target is now:

`2/20 -> 3/20`

Priority: inspect `rafaelmeloreisnovo/ZIPRAF_CORE` exact current HEAD and bind its existing `src/include/tests/tools` into a repository-native deterministic execution/receipt. Do not add a decorative green workflow that fails to exercise project substance.

The four zero-step repositories remain provider-boundary cases, not code failures.

## R3

- F_ok: `2/20` current-main strict-reproducible project cores; both have immutable project environments, HEAD-bound receipts and artifact digests.
- F_gap: `18/20` without strict current-HEAD core receipts; `4/20` specifically provider-gated; Fisica full pytest dimension still unexecuted in the strict receipt.
- F_next: target `ZIPRAF_CORE` for `3/20`, then decide whether to close Fisica pytest completeness separately.
