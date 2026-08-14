# RAFAELIA — Operational Pending Map — Receipt C83 — 2026-08-13

State: `VERIFIED_LIMITED`

Claim gate: `claim_allowed=false`

Scope: `C80_BOUNDED_WORK_ITEMS_ONLY`

## Authority boundary

The dashboard is a derived view. The authority remains the versioned work-item ledger plus append-only transition events on GitHub. A spreadsheet cell is not allowed to silently supersede ledger/event state.

## Source state

Provider-observed main before C83 branch: `b577012a55aedf00ca648d4888d039acc1223426`, which includes merged C80/C81/C82 material.

Inputs:

- `data/governance/operational-work-items.c80.v1.json`;
- `data/governance/operational-work-item-transitions.c80.v1.json`;
- C81 receipt;
- C82 receipt.

## Workbook evidence

Local workbook: `RAFAELIA_OPERATIONAL_PENDING_MAP_C82.xlsx`

SHA-256: `f787c3f2c1b3d227bddf613f8c8a6e61666b8092c52fdfed0e6ff74396802b08`.

Sheets:

- Dashboard;
- Work Items;
- Transition Ledger;
- Contracts;
- Sources.

The local workbook inspection found no `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?` or `#N/A` matches in the verification scan.

## Drive materialization

Provider ID: `1JUSbJlHlVWznJJ5O1vzQwdd3yPc_J8faUcXA_ov0kkk`.

Native Google Sheet: yes.

Timezone normalized after import to `Etc/UTC`.

Provider readback of `Dashboard!A1:H20` observed:

- work items = `3`;
- open or TOKEN_VAZIO closure = `3`;
- MUST/IMPORTANT = `3`;
- provenance PARTIAL/MISSING = `2`;
- contracts not SATISFIED = `3`;
- transition events = `3`;
- claim_allowed TRUE = `0`.

The Priority / Closure window readback preserved the three governed C80 items and their distinct urgency, importance, attention, provenance, contract, execution and closure states.

## TOKEN_VAZIO delta

`TOKEN_VAZIO_OPERATIONAL_DASHBOARD` -> `RESOLVED_BOUNDED_C80_DASHBOARD`.

New boundedness tokens:

- `TOKEN_VAZIO_GLOBAL_OPERATIONAL_DASHBOARD`;
- `TOKEN_VAZIO_DASHBOARD_AUTO_REGENERATION_GATE`.

This replacement is intentional: a bounded view exists, but global coverage and deterministic auto-regeneration are not yet proven.

## F_ok

A legible operational view now exists across orthogonal dimensions, includes a risk-priority chart, preserves claim gate status, is materialized in Drive and has provider readback.

## F_gap

Only three C80 work items are represented; historical/global gaps are not yet ingested. The current dashboard was generated from versioned source material, but an automated regeneration/checksum comparison gate is not yet materialized.

## F_next

Ingest one bounded historical Gap Atlas/receipt batch into the work-item lattice without retroactive inference, append transition events where temporal evidence exists, regenerate this dashboard, and verify that the new view is derived rather than manually authoritative.
