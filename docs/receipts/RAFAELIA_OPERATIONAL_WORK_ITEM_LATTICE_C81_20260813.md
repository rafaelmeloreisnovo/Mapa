# RAFAELIA — Operational Work-Item Lattice — Receipt C81 — 2026-08-13

State: `VERIFIED_LIMITED`

Claim gate: `claim_allowed=false`

Mode: `APPEND_ONLY / ORTHOGONAL_STATE_MODEL / FAIL_CLOSED / LOCAL_CONTENT_EXECUTION + PROVIDER_MATERIALIZATION`

## Purpose

Prevent semantic collapse between urgency, importance, attention history, epistemic state, provenance, contract satisfaction, execution state, temporal window, Six Sigma control and closure.

Canonical invariant:

`W = <origin, priority, attention, epistemic, provenance, contract, execution, time_window, six_sigma, bibliotechnics, closure>`

`urgent != proved`; `forgotten != refuted`; `ignored != unnecessary`; `aborted != invalidated`; `blocked/suppressed != code failure`; `obvious != evidenced`; `suggested != authorized`; `executed != verified`; `absence != zero`; `TOKEN_VAZIO != negative conclusion`.

## Provider-materialized artifacts

Branch: `audit/operational-workitem-lattice-20260813`

- schema: `schemas/operational-work-item.v1.schema.json`
  - Git blob: `7763b321f17d75ac6c68d76418af967266526dac`
  - local content SHA-256: `92c464a74492431d3dd4b3a5cfcc8fcbac412f30109722ab4b4a21db463220cf`
- validator: `tools/validate_operational_work_item.py`
  - Git blob: `2b2a714be439dde57963e6201e29d4b52c4db5d8`
  - local content SHA-256: `fb696eec906c0a485a9f14306990d33f5489909d394be801a6dad827c922a8ec`
- C80 work items: `data/governance/operational-work-items.c80.v1.json`
  - Git blob: `7e6cd9396a7ff4b4a3dc86b97226af496dbe6e70`
  - local content SHA-256: `8251e8239872f314a6a6839e5223c70790c57228b9852adf5fce0ad59b12d377`
- adversarial tests: `tests/test_operational_work_item.py`
  - Git blob: `6f52a852974cf8149da747cd48e34b9f4aa7b347`
  - local content SHA-256: `f99e4ecc7ff55e792163ad432c569d3692d9ba47d103bb1a330e46a8eff0de94`
- semantic document: `docs/canonical/RAFAELIA_OPERATIONAL_WORK_ITEM_LATTICE_V1.md`
  - Git blob: `dc45024e1bcbc4fa7b2d44e52f828a99c68eb66f`

## Local execution evidence

Current local re-execution:

- C80 ledger validation: `PASS`, items=`3`, errors=`[]`, `claim_allowed=false`
- validation transcript SHA-256: `45a3afe8ca886d8c15a8b92db9181ee202ce8457dfb176666a5fd8811179db2c`
- adversarial battery: `10/10 PASS`, exit=`0`
- adversarial transcript SHA-256: `bd979262cd4e06f8487989c625df9e709c008e7fee62a51c5eadcfb3eca3cc99`

Adversarial controls require rejection for:

1. RPN mismatch;
2. VERIFIED without evidence;
3. TOKEN_VAZIO without F_gap/F_next;
4. SUPPRESSED_BY_POLICY without policy_ref;
5. contract marked SATISFIED with open requirement;
6. CLOSED with non-PASS gate;
7. EVIDENCED with provenance MISSING;
8. claim_allowed=true;
9. unexpected extra property;
while the positive baseline must PASS.

## Six Sigma boundary

`RPN = severity × occurrence × detectability` is a configured operational risk-priority number over ordinal 1..5 scales. It is not a physical constant or empirical probability. A mismatch fails closed.

## First governed work items

C80 gaps were encoded without flattening their meanings:

- semantic-topic privacy review: `SOON + MUST + ACTIVE + TOKEN_VAZIO + provenance BOUND + contract PARTIAL`;
- bounded chunk graph: `SOON + IMPORTANT + LEFT_INCOMPLETE + TOKEN_VAZIO + provenance PARTIAL + execution PLANNED`;
- cross-export dedup: `ROUTINE + IMPORTANT + DEFERRED + TOKEN_VAZIO + provenance PARTIAL`.

## Evidence boundary

This receipt proves local behavior of the materialized content family and provider existence of the versioned artifacts. It does not claim that GitHub Actions executed these tests. Provider CI remains `SEM_EVIDENCIA` until a workflow/job with executed steps is observed.

It also does not claim a complete inventory of all historical work items in RAFAELIA.

## F_ok

Orthogonal schema, fail-closed semantic validator, three real C80 work items, canonical terminology bridge, 3/3 ledger validation and 10/10 adversarial controls.

## F_gap

- `TOKEN_VAZIO_C81_PROVIDER_CI_EXECUTION`
- `TOKEN_VAZIO_GLOBAL_WORK_ITEM_INVENTORY`
- `TOKEN_VAZIO_HISTORICAL_PRIORITY_INGESTION_WITHOUT_RETROACTIVE_INFERENCE`
- `TOKEN_VAZIO_WORK_ITEM_TRANSITION_EVENT_LEDGER`
- `TOKEN_VAZIO_OPERATIONAL_DASHBOARD`

## F_next

1. open a draft PR and inspect provider CI without promoting absent execution;
2. ingest a bounded set of existing Gap Atlas/receipts into this lattice, preserving their original temporal states;
3. add append-only transition events rather than mutating history in place;
4. generate views by urgency, importance, provenance, contract, execution and closure gate;
5. only after bounded validation expand toward a global work-item inventory.
