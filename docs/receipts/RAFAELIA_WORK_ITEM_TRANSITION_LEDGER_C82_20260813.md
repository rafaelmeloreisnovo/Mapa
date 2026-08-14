# RAFAELIA — Work-Item Transition Ledger — Receipt C82 — 2026-08-13

State: `VERIFIED_LIMITED`

Claim gate: `claim_allowed=false`

Mode: `APPEND_ONLY / NON_RETROACTIVE_BASELINE / FAIL_CLOSED`

## Purpose

C81 defines orthogonal work-item state. C82 prevents later state changes from erasing how an item evolved.

A transition event records:

`event_id + work_item_id + observed_at + prior_event_id + from_state + to_state + reason + evidence`.

The initial C80 events are `CREATE` events only. They do not reconstruct unobserved history before formal materialization.

## Provider materialization

Branch: `audit/operational-workitem-lattice-20260813`

- transition schema: `schemas/operational-work-item-transition.v1.schema.json`
  - Git blob: `7608327ba0e1bc159f68bf30e1deb5d527aea1d6`
  - local content SHA-256: `17f3e62ae348d6fc46573668f2275528f88849b8abdeabe0721eeedae45abe86`
- transition validator: `tools/validate_operational_work_item_transitions.py`
  - Git blob: `7df31b03177cf2fa7e5e238fdd10a54288dc432f`
  - local content SHA-256: `4954609994f8c43b2e6e4ce2426efe710ad4fa0997391e2b424104f3e7f3f350`
- initial transition ledger: `data/governance/operational-work-item-transitions.c80.v1.json`
  - Git blob: `b050f4f8c23ed58cbecb5469ac9dcaa51f184044`
  - local content SHA-256: `762686c427e1c68af97603550effae550af930a7307611705ec471c9f397c127`
- adversarial tests: `tests/test_operational_work_item_transitions.py`
  - Git blob: `2b40cef0d13c4d8bb63711c902032b18cfef93f3`
  - local content SHA-256: `4b73572bbc3ac8f1af7e0a769405ee39be7fdd535ba1413c1d9c082cd48f689c`

## Local execution evidence

Baseline transition ledger validation:

`PASS / events=3 / unique_event_ids=3 / errors=[] / claim_allowed=false`

Validation transcript SHA-256: `cad381175f098a56e1e2ec5901916cdf9359a3b489098c9084131ace16785d01`.

Adversarial battery:

`11/11 PASS`, exit `0`.

Adversarial transcript SHA-256: `130368311aa7163c6b7d7de7657ead5810b0fa5e5ce502b66873f284b01bb06a`.

The validator rejects duplicate event IDs, CREATE with a non-empty prior chain, CREATE with non-null from_state, non-CREATE with TOKEN_VAZIO prior, no-op transitions, unknown prior events, evidence promotions without evidence refs, malformed SUPERSEDE, non-monotonic event time and `claim_allowed=true`.

## Initial event baseline

Three CREATE events establish the first formal transition-ledger boundary for:

- `WI-C80-SEMANTIC-TOPIC-PRIVACY`;
- `WI-C80-CHUNK-GRAPH`;
- `WI-C80-CROSS-EXPORT-DEDUP`.

Their `prior_event_id=TOKEN_VAZIO` means “no earlier event is represented in this ledger”, not “no earlier real-world state existed”.

## TOKEN_VAZIO delta

- `TOKEN_VAZIO_WORK_ITEM_TRANSITION_EVENT_LEDGER` -> `PARTIAL_INITIAL_LEDGER_MATERIALIZED`

Still open:

- `TOKEN_VAZIO_HISTORICAL_TRANSITION_INGESTION_WITHOUT_RETROACTIVE_INFERENCE`
- `TOKEN_VAZIO_GLOBAL_WORK_ITEM_EVENT_COVERAGE`
- `TOKEN_VAZIO_C82_PROVIDER_CI_EXECUTION`

## Evidence boundary

Local execution validates the current content family; provider blobs prove GitHub materialization. GitHub Actions execution is not promoted from provider failures with no executed steps.

C82 does not infer historical transitions that were never observed. Future changes must append new events instead of rewriting these CREATE events.

## F_ok

Transition schema + fail-closed validator + three initial CREATE events + 11/11 adversarial controls.

## F_gap

Historical/global coverage is absent; only the formal baseline from C80 forward is represented.

## F_next

When any governed work item changes, append a TRANSITION/CORRECTION/SUPERSEDE event linked to its prior event, then validate monotonic time, prior-event topology, evidence requirements and state difference before updating any materialized current-state view.
