# ATLAS:X — Mission execution boundary — 2026-09-06

**Route ID:** `ATLAS:X-MISSION-EXECUTION-BOUNDARY-20260906`  
**Predecessor:** `ATLAS:X-FEDERATION-RECONCILE-20260906`  
**Execution contract producer:** `rafaelmeloreisnovo/termux-app-rafacodephi` PR #425  
**Observed producer head:** `a13b04693428d21bf9bf411b353f6a79c835afe7`  
**State:** `CONTRACT_BOUND / OPEN_REMOTE_GATES / claim_allowed=false`

## Purpose

Route the federation under one explicit mission boundary without copying execution authority into Mapa.

```text
DATASET/CORPUS -> context + evidence
MODEL          -> retrieve / interpret / propose
MISSION        -> authorized goal/scope
PROGRAM        -> typed execution under Governance + receipts
```

Mapa continues to own route/evidence state. Termux continues to own orchestration. Producer repositories continue to own their own implementation/runtime claims.

## Canonical route

```text
MISSION
 -> ATLAS:X
 -> NOVO:X
 -> L:X
 -> O:X
 -> T:X
 -> REL:X
 -> EVID:X
 -> GAP:X
 -> AtlasLLMContextEnvelope
 -> ContextBundle
 -> IntentIR
 -> Governance
 -> ExecutionPlan
 -> AuthorizedAction
 -> ExecutionResult
 -> ProvenanceReceipt
 -> LEARN:X
```

## Federated invariants

- `DATASET_INFORMS != MISSION_AUTHORITY`
- `RETRIEVAL_CONTEXT != WEIGHT_UPDATE`
- `LEARN_APPEND_ONLY != ONLINE_SELF_TRAINING`
- `CONTINUE_APPROVED_SCOPE != AUTONOMOUS_GOAL_CREATION`
- `SOURCE != DERIVED_INDEX != EXECUTION != EVIDENCE != CLAIM`
- `TOKEN_VAZIO != 0`
- `EXTERNAL_AUTHORITY_REQUIRED != ORCHESTRATOR_PERMISSION`
- `GREEN_GATE_PROMOTES_ONLY_MEASURED_SCOPE`

## Node bindings

| Node | Binding |
|---|---|
| Termux / RAFCODEPHI | orchestration authority and MissionExecution contract producer |
| llamaRafaelia / RMRCTI | retrieval/model provider; no mission authority and no implicit weight update |
| GAIA_phi | bounded retrieval adapter; no mission authority and no trained-model promotion |
| Vectras-VM-Android | optional runtime backend; execution proof remains process/guest/device-scoped |
| Rafaelia_Private | protected implementation authority; disclosure remains bounded/pointer-first |
| MemRafcode + Drive | append-only longitudinal/custody successor |
| Mapa | route/state/evidence pointer authority; does not execute producer code |

## Continuation rule

When one lane is blocked by an external authority or missing execution evidence, the program MAY continue other already-authorized independent safe lanes. It MUST NOT weaken the blocked gate or convert missing evidence to PASS.

Current transverse blocker remains:

`TV-ACTIONS-PRESTEP-ROOT-CAUSE`

Provider/admin/reviewer/secret/device gates remain independent and cannot be simulated.

## Completion semantics

`FINISHED_WITH_EXTERNAL_GATES` means all safe actions available under current authority have either been proven within their scope or mapped to a concrete `TOKEN_VAZIO` / external-authority transition. It does not mean every runtime or scientific claim is proven.

## LEARN:X

The operational learning successor records:

`observation -> action -> result/evidence -> F_ok -> F_gap -> F_next -> successor receipt`

This is longitudinal program memory. It is not implicit neural-weight training.