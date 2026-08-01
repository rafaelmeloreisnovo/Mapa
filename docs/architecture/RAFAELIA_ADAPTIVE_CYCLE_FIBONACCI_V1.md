# RAFAELIA Adaptive Cycle — Fibonacci-Rafael V1

## Purpose

This package turns the execution parable into a bounded operational loop:

```text
source → index → semantic token → claim → evidence
→ falsifier → decision → artifact → feedback
```

The workflow is automatic only in the engineering sense: repeatable, observable,
reversible, and auditable. It is not unsupervised authority.

## Two temporal layers

- **Microcycle:** GitHub Actions runs at minutes `07, 22, 37, 52` of each hour.
- **Consolidation:** four microcycles form one hourly observation window.
- **Period:** `n mod 42` rotates the toroidal state and task phase.

Scheduled runs are read-only. They generate artifacts but never push, merge,
delete, publish, or change `claim_allowed`.

## State

The state is typed as:

```text
s = (u, v, ψ, χ, ρ, δ, σ) ∈ [0,1)^7
```

Repository coverage and normalized manifest entropy feed the stable updates:

```text
C[t+1] = 0.75 C[t] + 0.25 C[in]
H[t+1] = 0.75 H[t] + 0.25 H[in]
φmetric = (1-H) C
```

This is a control metric, not a truth probability.

## Fibonacci-Rafael conflict treatment

Two sign conventions are present in the materials:

```text
F+[n+1] = (√3/2)F+[n] + π sin(279°)
F−[n+1] = (√3/2)F−[n] − π sin(279°)
```

Because `sin(279°) < 0`, the variants converge toward attractors with opposite
signs. The engine computes both, records their divergence, and forbids silent
selection. Their value modulates operational priority only; it cannot validate a
scientific or metaphysical claim.

## Formula registry

All 50 supplied equations receive one typed state. Examples:

- formal definition or standard mathematics;
- executable recurrence or heuristic;
- model hypothesis requiring a falsifier;
- underspecified expression;
- empirical `TOKEN_VAZIO`;
- conflicting definition;
- refuted as written.

In particular, the ordinary-sum expressions labelled CRC are recorded as
`REFUTED_AS_WRITTEN`: a CRC requires polynomial division over `GF(2)`.

## Receipts

Each run emits:

- `cycle_receipt.json` — full state, inputs, boundaries and SHA-256;
- `formula_evaluation.json` — classifications and known-answer tests;
- `next_action.json` — ranked operational queue;
- `cycle_summary.md` — human-readable `F_ok`, `F_gap`, `F_next`.

## Promotion boundary

```yaml
claim_allowed: false
publication_ready: false
automatic_mutation: false
automatic_merge: false
maximum_automatic_promotion: READY_FOR_HUMAN_REVIEW
```

A clock tick is not evidence. A hash is not truth. CI is not physical runtime.
A parable is not a mechanism. Every missing proof remains `TOKEN_VAZIO` with a
verifiable next step.
