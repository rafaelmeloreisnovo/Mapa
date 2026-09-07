# ATLAS:X ↔ Frida bounded producer — exact-head successor receipt — 2026-09-07

State: `SOURCE_GOVERNANCE_BOUND / EXTERNAL_RUNTIME_OPEN`

`claim_allowed=false`

## Predecessor

`indices/deltas/ATLAS_X_FRIDA_EXECUTION_PRODUCER_BINDING_20260907.md`

## Frida exact-head evidence

Candidate PR: `rafaelmeloreisnovo/frida-desktop#52`

Candidate head: `995c74b142796e3397c8ab357f720cd2d7ce3fc3`

Observed pull-request workflow runs at that exact head:

| Workflow | Run | Terminal state |
| --- | ---: | --- |
| Workflow Architecture Contract | 34166139804 | `SUCCESS` |
| ATLAS mission consumer gate | 34166139835 | `SUCCESS` |
| RAFAELIA Provenance Non-Regression Gate | 34166139799 | `SUCCESS` |

Bounded source/governance result: `3/3 SUCCESS`.

## Promotion performed

PR #52 was promoted after the terminal exact-head readback.

Merge commit: `a60fb030e9c1d858e10201d93c112784b1efe877`

Frida `main` was read back at that exact merge commit.

The promoted files are:

- `docs/contracts/frida_atlas_mission_execution_consumer.v1.json`
- `tools/validate_frida_atlas_mission_binding.py`
- `.github/workflows/atlas-mission-consumer-gate.yml`

## Authority interpretation

The merge closes only the source/governance navigation edge:

```text
AuthorizedAction
  -> FridaBoundedExecutionProducer
  -> ExecutionResult
  -> ProvenanceReceipt
  -> LEARN:X
```

It does not grant Frida any of the following:

- mission authority;
- orchestration authority;
- provider/legal authority;
- autonomous goal creation;
- model-weight training authority;
- permission to promote missing physical/runtime evidence.

## Preserved open gates

```text
physical_android_termux_execution = TOKEN_VAZIO_DEVICE
exact_multi_repository_runtime_execution = TOKEN_VAZIO_EXECUTION
remote_network_identity = TOKEN_VAZIO_RUNTIME
provider_or_legal_authorization = TOKEN_VAZIO_EXTERNAL_AUTHORITY
model_weight_training_authorization = TOKEN_VAZIO_SEPARATE_EXPLICIT_CONTRACT_REQUIRED
```

Performance/cache/DRAM/eight-core claims remain separately evidence-bound and are not changed by this receipt.

## Mapa candidate state

This receipt is additive inside Mapa PR #554. Mapa provider/server/manual/secret gates remain independent and may stay deliberately red while source CI is evaluated. Their failure cannot be reinterpreted as a Frida source failure, and a source PASS cannot reinterpret them as closed.

## Rollback

- Frida: revert merge `a60fb030e9c1d858e10201d93c112784b1efe877` if the binding itself is later invalidated.
- Mapa: close/revert PR #554 if this routing receipt is invalidated.
- No dataset, model weights, physical runtime, provider ruleset, or external authorization was modified by this promotion.

## Retroalimentação

- `F_ok`: Frida ↔ ATLAS mission-authority binding is now present on Frida `main`, validated 3/3 on the candidate exact head before promotion.
- `F_gap`: physical device/runtime/provider/training gates remain open; Mapa PR #554 still needs terminal source-CI readback.
- `F_next`: read Mapa PR #554 terminal CI, separate expected external gate failures from source regressions, then promote only if source/structure checks support it.
