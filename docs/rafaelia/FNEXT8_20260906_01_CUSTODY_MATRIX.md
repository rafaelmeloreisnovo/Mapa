# RAFAELIA FNEXT8 — 01 — Canonical Custody Matrix

id: FNEXT8-20260906-01
state: IMPLEMENTED_ON_BRANCH
claim_allowed: false
authority: Mapa / governance
mode: append-only, fail-closed, reversible

## Purpose
Define the canonical 7-dimensional custody row used to relate implementation and evidence without collapsing vision, code, execution, evidence or claim.

## Canonical dimensions
`repo × drive × paper × commit × receipt × evidence × token_vazio`

Each row MUST preserve independently:
- `source_pointer`
- `repo_ref`
- `drive_ref`
- `paper_ref`
- `commit_sha`
- `receipt_ref`
- `evidence_state`
- `claim_allowed`
- `token_vazio[]`
- `next_verifiable_step`
- `predecessor`
- `timestamp`

## Invariants
1. `TOKEN_VAZIO != 0` and `TOKEN_VAZIO != false`.
2. `documented != implemented`.
3. `implemented != build_proven`.
4. `build_proven != runtime_proven`.
5. `runtime_proven != device_proven`.
6. `device_proven != reproduced`.
7. No downstream projection may increase evidence level without a receipt that names its source.

## Closure gate
A row is CLOSED only when every required reference for its asserted state resolves and the receipt hash/lineage is present. Otherwise it remains OPEN or TOKEN_VAZIO.

## Cross-project route
Mapa -> Matem-tica- / papers -> ChipQuantum -> RafGitTools -> termux-app-rafacodephi / Vectras-VM-Android -> Drive receipt/index.

No scientific, mathematical, physical or runtime novelty claim is created by this file.
