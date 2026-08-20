# RAFAELIA Feedback Event & No-Regression Gate V1

Status: `ACTIVE / CLAIM_ALLOWED=false`

## Purpose

Every material observation becomes an append-only `F_event`:

```text
observation -> F_ok + F_gap + F_next -> gate -> receipt -> next event
```

The ledger does not force reality to improve monotonically. **Evidence may invalidate an earlier state.** What is forbidden is a silent downgrade, unsupported promotion, or historical rewrite.

## Invariants

1. Append order is explicit through `sequence`.
2. Each event is SHA-256 chained to the previous event.
3. `predecessor_event_ids` may reference only earlier events.
4. `claim_allowed=true` requires `VERIFIED|PASS`, evidence, a named gate, and a promotion/execution transition.
5. A lower evidence state requires `CORRECTION|CONTRADICTION|REGRESSION` plus evidence.
6. `TOKEN_VAZIO` remains a valid state and must retain a verifiable `F_next`.
7. Leverage classes are prioritization labels, not mathematical proof of exponential/factorial growth.

## Leverage prioritization

- `LOCAL`: one bounded artifact.
- `SYSTEMIC`: affects a subsystem or policy.
- `MULTIPLICATIVE`: one change protects/enables multiple later operations.
- `EXPONENTIAL_CANDIDATE`: plausible combinatorial reuse; requires measurement before any growth claim.
- `FACTORIAL_CANDIDATE`: large interaction-space candidate; never treated as measured complexity without proof.

The priority function is therefore practical rather than mystical:

```text
priority = expected reusable value × number of dependent gates × evidence confidence / execution cost
```

A candidate with large theoretical leverage is not promoted merely because its label sounds exponential.

## Validation

```sh
python3 -m unittest -v tests.test_feedback_events
python3 scripts/validate_feedback_events.py \
  --ledger data/feedback-events/feedback-events.v1.jsonl \
  --write-report build/feedback-events/report.json
```

## Truth boundary

`no regression` means **no unsupported epistemic regression** and **no destruction of history**.
It never means that `FAIL` or `CONTRADICTION` are prohibited. A truthful contradiction is progress because it increases information and prevents later false branches.

## Current seed events

The V1 ledger starts with four bounded observations:

1. cross-repository README evidence-boundary audit;
2. anti-regression gate design and local validation;
3. Termux claim-boundary correction target;
4. ApkC host-verifiable proof-chain target.

Each next execution appends a new event; existing events are never silently rewritten to manufacture continuity.
