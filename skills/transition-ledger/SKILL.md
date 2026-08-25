---
name: transition-ledger
description: Record every material before→after transition with reason, evidence, uncertainty, authority, falsifier, rollback and receipt.
version: 1.0.0
status: DRAFT_FAIL_CLOSED
---

# D7 — Transition Ledger

## Rule

`NO_STATE_TRANSITION_WITHOUT_REASON`.

A correction is a new event (errata/supersession), never silent historical rewrite.

## Transition record

```text
transition_id
from_state
to_state
trigger
observation
interpretation
evidence
counterevidence
uncertainty
risk_before
risk_after
authority
privacy_class
falsifier
test_set
minimum_intervention
blast_radius
rollback
failover
watchdog_state
attention_state
receipt
next_review
```

## Gates

- missing predecessor for a claimed mutation → `TOKEN_VAZIO_PREDECESSOR`;
- missing reason/evidence → do not promote transition;
- irreversible transition with unknown risk → `HOLD`;
- missing receipt after material mutation → `OPEN_CUSTODY_GAP`.

## Output

`transition_record`, `append_only=true`, `receipt_required`, `review_trigger`, `F_ok/F_gap/F_next`.
