# GPT Layout Operational Workflow V1

## Contract

Every significant RAFAELIA GPT task follows:

```text
objective
-> bootstrap
-> authority
-> route
-> evidence
-> gate
-> execution
-> receipt
-> delta
-> index feedback
-> retrofeedback
```

## Required fields

- `id`: stable objective or event identifier.
- `origem`: source, prompt or authority anchor.
- `tipo`: session, research, code, memory or status.
- `estado`: current epistemic or execution state.
- `ação`: bounded operation selected by the gate.
- `resultado`: evidence, failure or TOKEN_VAZIO.

## Fail-closed rule

A missing source, unresolved authority, unsatisfied gate or missing receipt
must become a typed `TOKEN_VAZIO` rather than an invented completion.

## Stop rule

Stop when the objective is fulfilled, the applicable gate fails,
a required authority is unavailable, or further work would add no evidence.

## Output

```text
F_ok
F_gap
F_next
DELTA when a write occurred
```
