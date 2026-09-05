# RAFAELIA Reversibility Catalog

Status: APPEND_ONLY / HUMAN+EIA NAVIGABLE

Invariant: VISÃO ≠ ARTEFATO ≠ EXECUÇÃO ≠ EVIDÊNCIA ≠ CLAIM.

This directory is the canonical catalog for reversible operations. Every reversible action must be represented as an immutable event with a stable event_id, before-state, after-state, rollback pointer, evidence pointer, epistemic status, and claim boundary.

## Navigation

- `index.jsonl` — append-only machine-readable event stream.
- `schema.v1.json` — event contract for validators and EIAs.
- `maps/` — derived navigation maps; derivations never replace source events.
- `receipts/` — immutable receipts for rollback-capable operations.

## Required event semantics

Each event records: event_id, timestamp, scope, operation, before_ref, after_ref, rollback_ref, evidence_ref, result, reversibility_state, risk_class, token_vazio, claim_allowed.

Allowed reversibility states:
- PLANNED
- EXECUTED_REVERSIBLE
- ROLLBACK_AVAILABLE
- ROLLED_BACK
- SUPERSEDED
- TOKEN_VAZIO

Rules:
1. Never edit historical events in place; append a successor event.
2. Rollback does not erase history; append a ROLLED_BACK event pointing to the original event.
3. Derived maps/indexes are rebuildable from `index.jsonl`.
4. `TOKEN_VAZIO` is an explicit unknown/open state, never zero or PASS.
5. No event may promote `claim_allowed=true` without its own evidence gate.
6. Human labels and EIA keys must resolve to the same stable event_id.
