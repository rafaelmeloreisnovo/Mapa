# RAFAELIA — Mar–Abr 2025 — W004 Transaction Reconciliation

**State:** `CONTROL_RECONCILED`  
**Timestamp:** `2026-09-11T23:49:14-03:00`  
**Evidence predecessor:** `REC-MARAPR-CONHECER-W003-20260911`  
**Claim:** `claim_allowed=false`

## Incident observed

An interrupted write sequence produced two different W002 event files:

1. `data/knowledge-ledger/mar-apr-2025/window-002.events.jsonl`
2. `data/knowledge-ledger/mar-apr-2025/events/window-002.events.jsonl`

Both reuse the logical IDs `MARAPR-W002-E001...`, so event ID alone is ambiguous.

## Resolution

No W002 artifact is deleted or rewritten.

- W002-A and W002-B remain historical sibling artifacts.
- Future supersession references must use **path-qualified artifact identity**.
- W003 is retained as the corrected, schema-complete evidence window.
- W004 is a control-plane reconciliation receipt, not a new scientific evidence claim.
- Active epistemic gaps remain exactly three.

## Validation evidence

`window-003.events.jsonl` was fetched back from GitHub and checked against `schemas/knowledge-ledger-event.v1.schema.json`.

Result: **5 events / 0 validation errors**.

## Current route

`W001 → {W002-A, W002-B} → W003 → W004(control)`

The branch remains draft and `claim_allowed=false`.

## R3

- **F_ok:** interrupted duplicate-ID state detected, preserved, disambiguated and routed; W003 schema gate passed.
- **F_gap:** literal lens/luneta/convex optical binding; March content binding; cross-export identity.
- **F_next:** exact March source/provider probe; create W005 only on material evidence delta.
