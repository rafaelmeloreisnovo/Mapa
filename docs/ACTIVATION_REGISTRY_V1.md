# RAFAELIA — Activation Registry V1

**State:** `IMPLEMENTED_PROPOSED`  
**Role:** subordinate activation/routing contract; **not** a competing master registry  
**Machine source:** `governance/ACTIVATION_REGISTRY_V1.json`  
**Federated control plane:** `Mapa`  
**Longitudinal navigation authority:** Google Drive `RAFAELIA — Master Navigation Registry V1`

## 1. Purpose

Turn RAFAELIA activation into an explicit, auditable state machine. The registry answers, for every activation edge:

`who/what activates → under which condition → with which input → behind which gate → producing which output → with which TOKEN_VAZIO fallback`.

It does not transfer authority from the producer repository, does not turn semantic interfaces into executors, and does not promote evidence into claims by implication.

## 2. Canonical activation chain

```text
objective
  → bootstrap
  → authority_resolution
  → route_resolution
  → evidence_collection
  → gate_evaluation
  → execution
  → receipt
  → delta
  → index_feedback
  → retrofeedback
  ↺ next_cycle
```

The corresponding control question is:

`objective → authority → route → evidence → gate → delta → index`.

## 3. Invariants

- `MASCOTE != AGENTE`
- `AGENTE != AUTORIDADE`
- `AUTORIDADE != EXECUTOR`
- `VISAO != ARTEFATO != EXECUCAO != EVIDENCIA != CLAIM`
- `TOKEN_VAZIO != PASS`
- unresolved absence is retained as an auditable state rather than completed by inference
- no operational promotion without applicable gate, evidence and receipt
- this registry is subordinate to the existing navigation/authority model

## 4. Gate ladder

The observed Ω-ACTIVATE longitudinal contract defines:

```text
G0_TRIAGEM
  → G1_DERIVADA
  → G2_REPLICA_LOCAL
  → G3_REPLICA_REDHAT
  → G4_MULTIVERIFICADA
```

A `verified` claim requires at least `G4_MULTIVERIFICADA`. Research/papers stay at the evidence-supported claim ceiling; the registry never upgrades them merely because they are indexed.

## 5. TOKEN_VAZIO lifecycle

```text
ABERTO → EM_TESTE → CONFIRMADO → REBAIXADO → FECHADO
```

Minimum actionable fields:

`id + priority + gap + signals + computable_action + exit_criterion + provenance`.

This makes a missing edge navigable and falsifiable instead of invisible.

## 6. Activation edges

| From | Activates | Minimum condition | Gate | Output | Fallback |
|---|---|---|---|---|---|
| bootstrap | authority_resolver | objective + readable bootstrap | bootstrap contract loaded | bounded objective context | `GAP:ACTIVATION_BOOTSTRAP_UNAVAILABLE` |
| authority_resolver | route_resolver | authority candidate observed | authority match or explicit TOKEN_VAZIO | canonical owner + primary artifact | `GAP:ACTIVATION_AUTHORITY_UNRESOLVED` |
| route_resolver | evidence_collector | authority resolved | addressable bounded route | evidence targets | `GAP:ACTIVATION_ROUTE_UNRESOLVED` |
| evidence_collector | gate_engine | targets addressable | traceable provenance | evidence bundle + missing-evidence gaps | `GAP:ACTIVATION_EVIDENCE_UNTRACEABLE` |
| gate_engine | executor | applicable gate identified | G0…G4 + claim ceiling | execution authorization | `GAP:ACTIVATION_GATE_UNSATISFIED` |
| executor | receipt_writer | authorization allows action | APPLY policy passed | execution delta/state | `GAP:ACTIVATION_EXECUTION_BLOCKED_OR_FAILED` |
| receipt_writer | index_feedback | delta or bounded failure observed | provenance complete | receipt | `GAP:ACTIVATION_RECEIPT_MISSING` |
| index_feedback | retrofeedback | receipt addressable | discoverable delta without authority replacement | indexed delta + supersession edges | `GAP:ACTIVATION_INDEX_FEEDBACK_MISSING` |
| retrofeedback | next_cycle | completed cycle or declared gap | R3 complete | `F_ok + F_gap + F_next` | `GAP:ACTIVATION_NEXT_STEP_UNRESOLVED` |

## 7. Operational profiles

### Code

A code change can be implemented before it is verified. Promotion requires a bounded change, test/CI evidence, receipt and index feedback.

### Research and papers

A paper/concept remains `derived`, `applied` or `research` until its method, evidence, falsifier and applicable gate justify a stronger state. Bibliographic proximity is not validation.

### Memory sync

Longitudinal memory is append-only. New state supersedes prior state through explicit edges; prior evidence is not erased.

### Mascots and agents

A mascot is a semantic interface, not authority or executor. An agent is a bounded capability whose authority and execution permission must be resolved per objective.

## 8. Observed gap: master-navigation pointer drift

`GAP:ACTIVATION_MASTER_NAV_POINTER_DRIFT` is opened because the Drive Master Navigation Registry currently points to:

`Mapa/docs/RAFAELIA_MASTER_NAV_REGISTRY_V1.md`

while that path was not found on the observed `main`. Current GitHub navigation artifacts are:

- `navigation/RAFAELIA_MASTER_REGISTRY.v1.json`
- `navigation/INDEX.md`

This registry does **not** silently rewrite the historical Drive pointer. Closure requires an explicit provenance receipt and a resolvable current pointer.

## 9. Activation result contract

Every cycle terminates in:

```text
R3 = <F_ok, F_gap, F_next>
```

A failed or blocked action still produces useful state when the failure is bounded, traceable and indexed.

## 10. R3

- `F_ok`: activation semantics are explicit and machine-readable.
- `F_gap`: pointer drift remains open; runtime/CI automation is not implied by this registry.
- `F_next`: validate JSON and navigation discoverability, review/merge this delta, then reconcile the Drive pointer through append-only provenance.
