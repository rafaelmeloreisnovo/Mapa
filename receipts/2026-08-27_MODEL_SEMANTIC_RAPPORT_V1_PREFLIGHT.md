# Model Semantic Rapport V1 — Preflight Receipt

**Date:** 2026-08-27
**State:** `BRANCH_PUBLISHED / REMOTE_CI_PENDING / CLAIM_BLOCKED`
**Repository:** `rafaelmeloreisnovo/Mapa`
**Branch:** `feat/model-semantic-rapport-v1-20260827`
**Base:** `77b4d02524b9904b669cd636fa3d498371623de5`
**Local qualification commit:** `a6cccf23706ff635b3673f19dc0aed2368e5d52e`
**Published implementation commit:** `4514452430789bfa5943dfa63ef0376443ecb135`
**Published predecessor head:** `880f5fd70200493734be86d8415cbb7d4a7ab082`
**Verified implementation tree:** `da465c74895e4fa4b29961a85684145d995b2dca`
**Merge authorization:** absent; merge remains blocked for human review

## Scope

This receipt covers the fail-closed boundary between observed language,
provider-controlled tokenization and model computation, observed output, and
external Mapa semantic rapport. It does not claim inspection or modification
of any provider model.

Primary artifacts:

- `contracts/model-semantic-rapport.v1.json`
- `schemas/model-semantic-rapport.v1.schema.json`
- `examples/model-semantic-rapport.closed-provider.v1.json`
- `tools/validate_model_semantic_rapport.py`
- `tests/test_model_semantic_rapport.py`
- `.github/workflows/model-semantic-rapport-v1.yml`
- `docs/architecture/MODEL_SEMANTIC_CONTEXT_RAPPORT_V1.md`

## Local evidence

| Gate | Result | Bounded interpretation |
|---|---|---|
| Semantic validator | `PASS` | 13 nodes, 15 edges, 6 blocking gaps |
| Control SHA-256 | `dcc77790b96c04dada00973b1994bd4a74ab09844009f0fd34df91512121b86a` | canonical JSON digest of the control contract |
| Closed packet SHA-256 | `af34504987ca2e06944a4afc5ab4886c500c068d40de31c8b876f36bc929b063` | canonical JSON digest of the unbound-provider fixture |
| Focused integration | `34/34 PASS` | rapport, contextual packet and external semantic tensor tests |
| Global invariants | `15/15 PASS` | executed in a detached worktree at the implementation commit |
| Diff hygiene | `PASS` | no whitespace error relative to the exact base |
| Remote workflow | `TOKEN_VAZIO_REMOTE_CI_PENDING` | only a GitHub run can promote this state |
| Independent JSON Schema engine | `TOKEN_VAZIO_ENGINE_UNAVAILABLE_LOCAL` | schema parsed and its declared boundary was tested; third-party engine validation is not claimed |

The structural validator returned:

```text
execution_mode              = UNKNOWN_PROVIDER_RUNTIME
internal_access             = PROPRIETARY_WITHHELD
parameter_update_observed   = TOKEN_VAZIO
model_internal_claim_allowed = false
claim_allowed               = false
```

## Non-regression comparison

The full unittest discovery was run both on the feature commit and on a clean
worktree at the exact base.

| Revision | Tests run | Failures | Errors |
|---|---:|---:|---:|
| base `77b4d02` | 855 | 3 | 9 |
| feature tree `da465c7` | 873 | 3 | 9 |

The feature adds 18 passing tests and reproduces the same pre-existing twelve
non-passing outcomes. Their observed classes are:

- import-time `SystemExit` in `test_cycle_artifact_identity`;
- missing `data/omega7-relational-amplifier.v1.json` in six tests;
- two operational tests resolving `tests` as a data file;
- an invalid federated relation, a stale batch-count expectation, and a
  pre-existing source-drift digest.

This comparison establishes no new observed regression in the requested
scope. It does not declare the repository-wide suite green.

## Evidence and rights ceiling

- `LLM` is not architecture proof.
- `LNN` requires an explicit expansion.
- an external semantic vector is not a native model embedding;
- contextual conditioning is not parameter training;
- a tensor is not automatically a learned weight;
- the repository code license does not establish rights for weights,
  tokenizer or dataset;
- exact provider, model, tokenizer, architecture, weights, activations,
  decoder, persistence and parameter updates remain `TOKEN_VAZIO` or
  `PROPRIETARY_WITHHELD` until producer evidence is bound.

## R3

**F_ok:** the semantic/model boundary is implemented, machine-addressable,
fail-closed, locally regression-compared and published with exact tree
identity.

**F_gap:** remote CI, independent JSON Schema engine validation and every
provider-internal or rights claim remain unverified.

**F_next:** open a draft PR, observe the exact GitHub run, then append its URL
and result to the longitudinal Drive receipt without merging.
