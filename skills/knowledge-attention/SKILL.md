---
name: knowledge-attention
description: Track forgotten, deferred, ignored, aborted, stale, orphaned and contradicted knowledge without equating absence with falsehood.
version: 1.0.0
status: DRAFT_FAIL_CLOSED
---

# Cross — Knowledge Attention

## Attention states

`OBSERVED | ACTIVE | IGNORED_WITH_REASON | IGNORED_WITHOUT_REASON | DEFERRED | ABORTED | QUARANTINED | SUPERSEDED | DEPRECATED | WITHHELD_BY_POLICY | REDACTED_PRIVACY | UNREVIEWED | UNREACHABLE | ORPHANED | CONTRADICTED | ANOMALOUS | PARADOXICAL | FALSIFIED | FORGOTTEN | NORMALIZED | DISMISSED | LOW_PRIORITY | ABANDONED | REOPENED | RECOVERED | TOKEN_VAZIO | CLOSED`.

## Evidence aging

`FRESH | AGING | STALE | HISTORICAL_ONLY | SUPERSEDED | INVALIDATED`.

Aging evidence does not become false automatically; it loses authority for **current-state** claims when identity/freshness no longer match.

## Scans

- forgotten TOKEN_VAZIO;
- abandoned hypothesis;
- unresolved anomaly/paradox;
- untested assumption;
- unowned risk;
- stale receipt/current-state claim;
- warning normalized into background noise;
- index edge to obsolete/missing target.

Never infer `CENSORED`; use `TOKEN_VAZIO_REASON` unless withholding/redaction is documented.

## Output

`attention_state`, `evidence_age`, `owner`, `last_review`, `reason`, `reopen_trigger`, `priority`, `F_ok/F_gap/F_next`.
