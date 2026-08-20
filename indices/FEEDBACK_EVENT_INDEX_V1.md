# Feedback Event Index V1

Estado: `ACTIVE / APPEND_ONLY / claim_allowed=false`

## Canonical route

```text
schema
  -> schemas/feedback-event.schema.json
ledger
  -> data/feedback-events/feedback-events.v1.jsonl
validator
  -> scripts/validate_feedback_events.py
tests
  -> tests/test_feedback_events.py
CI
  -> .github/workflows/feedback-event-noregression.yml
method
  -> docs/FEEDBACK_EVENT_NO_REGRESSION_V1.md
```

## Operational invariant

`observation -> F_ok + F_gap + F_next -> gate -> receipt -> append event`

Corrections and contradictions are preserved as new events. Existing history is not silently rewritten.
