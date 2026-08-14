# RAFAELIA — Δ → ★ → μ‰ → Ω → Δ

Date: 2026-08-13  
State: `FORMALIZED_NOT_FULLY_EXECUTED`  
Boundary: `claim_allowed=false`  
Mode: `append-only / anti-regression / evidence-first`

This lifecycle converts the conceptual sequence `Δ → ★ → μ‰ → Ω` into a bounded operational state machine. It extends the seven-window Operational Coherence Map in PR #223; it does not create a competing architecture.

## Δ — difference intake

Δ is the typed distance between the observed state and the desired state.

Required tuple:

`Δ_i = <source, baseline, objective, scope, provenance, constraints, labels, epistemic_state>`

Every absence must become either evidence-bound data or explicit `TOKEN_VAZIO`. No silent default is allowed.

Discovery labels include: `absence`, `urgent`, `provenance`, `CONTRACT`, `necessary`, `important`, `forgotten`, `ignored`, `obvious`, `censored`, `left_behind`, `suggested`, `should`, `good_candidate`, `aborted`, `uncertain`, and `TOKEN_VAZIO`.

These labels control triage. They do **not** prove anything.

## ★ — routing / attention nodes

★ assigns each actionable object to one primary operational window:

1. Security / integrity
2. Build / runtime
3. Contract / compatibility
4. Evidence / provenance
5. Memory / index
6. Efficiency
7. Evolution

Required tuple:

`★_i = <primary_window, authority, dependencies, route, isolation_boundary, evidence_needed, falsifier>`

The word “attention” is an architectural analogy here. A ★ node may be implemented by a human decision, rule engine, graph router or model; the symbol itself does not imply a Transformer.

## μ‰ — bounded micro-iteration

μ‰ means small, auditable change rather than blind recursion.

Required tuple:

`μ_i = <before, change_set, probe, result, after, uncertainty_delta, receipt_or_TOKEN_VAZIO>`

Core measurements:

- regression rate = reopened/broken closed items ÷ touched closed items;
- closure rate = closed gaps ÷ attempted gaps;
- evidence coverage = evidence-bound required fields ÷ applicable required fields;
- TOKEN_VAZIO resolution rate = resolved TOKEN_VAZIO ÷ initial TOKEN_VAZIO;
- defect density = observed defects ÷ reviewed opportunities;
- optional DPMO = defect density × 1,000,000.

Six Sigma is used only as process instrumentation. A sigma-level claim requires measured defects/opportunities, sampling plan and receipt.

## Ω — bounded operational plateau

Ω is **not** absolute completion. It is a scope-bounded plateau with enough evidence to stop changing that slice until new information appears.

Required tuple:

`Ω_i = <F_ok, F_gap, F_next, closure_gates, remaining_TOKEN_VAZIO, recovery_route>`

Closure rule:

`Ω(scope) iff stated closure gates pass for that scope AND unresolved material uncertainty is explicit`.

Any new material conflict, regression, missing provenance or falsifying observation causes:

`Ω → Δ_new`

Therefore the full lifecycle is:

`Δ → ★ → μ‰ → Ω → Δ' → ...`

not a one-way march toward an unverifiable “final state”.

## Priority geometry

Priority is multidimensional:

`P(gap) = f(impact, urgency, dependency_blocking, evidence_deficit, provenance_risk, regression_risk, reversibility)`

Urgency can increase priority but cannot bypass safety, dependency, provenance or evidence gates.

## Anti-regression invariants

- `idea != implementation != execution != evidence != claim`
- `TOKEN_VAZIO != zero != FAIL != PASS`
- negative result is append-only evidence;
- historical states are superseded, not erased;
- closure requires evidence;
- new conflict reopens Δ;
- a route may be optimized, but authority cannot be silently duplicated.

## Definition of operational excellence in this model

Operational excellence is the continuous reduction of untyped uncertainty and avoidable variation while preserving proof boundaries, provenance, recoverability and the capacity to reopen the model when reality disagrees with it.

It is therefore not “doing everything”. It is executing the **right next bounded action** with enough context to avoid regression.

## Immediate integration

Parent artifacts:

- `docs/canonical/2026-08-13/RAFAELIA_OPERATIONAL_COHERENCE_MAP_V1.md`
- `data/governance/RAFAELIA_OPERATIONAL_COHERENCE_LEDGER_2026-08-13.v1.json`
- `data/governance/RAFAELIA_DELTA_STAR_MICRO_OMEGA_LIFECYCLE_V1.json`

Next gate: validator + adversarial fixtures + one real open gap traversing all four states with a receipt.
