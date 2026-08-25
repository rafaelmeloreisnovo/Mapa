---
name: omega-assurance-router
description: Route RAFAELIA work across Ω7 assurance skills without manufacturing authority, evidence, or PASS.
version: 1.0.0
status: DRAFT_FAIL_CLOSED
---

# Ω Assurance Router

## Authority

Subordinate to `AGENTS.md`, the canonical bootstrap, producer authority, and explicit user authorization. This skill routes; it does not promote claims by itself.

## Trigger

Use for non-trivial RAFAELIA work involving uncertainty, writes, claims, runtime, privacy, security, risk, transitions, anomalies, gaps, or cross-repository evidence.

## Preflight

Resolve or type as `TOKEN_VAZIO`:

1. objective;
2. exact source/repo/ref/path/revision;
3. authority owner;
4. write boundary;
5. privacy/sensitivity class;
6. evidence state and staleness;
7. rollback/reversibility requirement.

## Route

```text
objective
→ D1 identity-provenance
→ D2 epistemic-discernment when meaning/claim is involved
→ D3 execution-evidence when implementation/runtime is involved
→ D5 privacy-information before disclosure or cross-surface movement
→ D6 authority-governance before mutation/promotion
→ D4 resilience-safety before risky/reversible execution
→ D7 transition-ledger for every material state change
→ knowledge-attention for ignored/deferred/stale/aborted material
→ crossfail-secure-sandbox for negative/fault-injection qualification
```

Only invoke directions that add information; do not create decorative 7×7 expansion.

## Serpent–Dove invariant

`SEE_MORE != CLAIM_MORE` and `CAN_DO != MAY_DO`.

Use maximum discernment for diagnosis and minimum sufficient intervention for action. Prefer contain > destroy, isolate > erase, quarantine > infer, HOLD > fabricated PASS.

## Stop conditions

Stop and emit `HOLD` when material authority, privacy class, provenance, reversibility, or required evidence is unknown and the next action would mutate/promote/disclose.

## Output

```text
F_ok = evidenced facts and gates passed
F_gap = explicit uncertainties/TOKEN_VAZIO/conflicts
F_next = smallest reproducible next gate
claim_allowed = false unless an external authorized promotion gate explicitly closes it
write_authority = ALLOWED | DENIED | TOKEN_VAZIO
receipt_required = true for material mutation/transition
```
