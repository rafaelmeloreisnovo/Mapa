---
name: epistemic-discernment
description: Classify statements by epistemic type and require the correct falsifier/evidence gate for each class.
version: 1.0.0
status: DRAFT_FAIL_CLOSED
---

# D2 — Epistemic Discernment

## Classes

`OBSERVATION | DEFINITION | FORMULA | DERIVATION | HYPOTHESIS | MODEL | THEORY | THEOREM | PROOF | EMPIRICAL_RESULT | ANOMALY | PARADOX | COUNTEREXAMPLE | FALSIFIER | REFUTED | REPLICATED | META_ANALYSIS | PARABLE | ANALOGY | TOKEN_VAZIO`.

## Rules

- Formula != hypothesis.
- Hypothesis != theory.
- Anomaly != root cause.
- Metaphor/parabola != physical evidence.
- Repetition/consensus != proof by itself.
- `TOKEN_VAZIO` remains explicit until a named gate closes it.

## Gate templates

### Hypothesis

`variables → falsifiable prediction → dataset → protocol → test → result → uncertainty`.

### Theorem

`axioms → definitions → derivation/proof → checker/review scope`.

### Anomaly

`observation → baseline → reproducibility → competing explanations`; causal claim remains separate.

### Parable/analogy

`declared meaning → scope`; no automatic promotion to empirical claim.

## Output

`epistemic_class`, `claim_text_or_hash`, `evidence`, `counterevidence`, `falsifier`, `uncertainty`, `promotion_gate`, `F_ok/F_gap/F_next`.
