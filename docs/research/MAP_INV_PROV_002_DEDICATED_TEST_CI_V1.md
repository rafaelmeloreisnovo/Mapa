# MAP-INV-PROV-002 — Dedicated T/C Gate V1

## Objective

Materialize a dedicated falsifier suite and CI workflow for `MAP-INV-PROV-002` without promoting external evidence dimensions by narrative.

## Preserved boundary

`first internal mention != first invention != public disclosure != legal priority != scientific novelty`

A passing dedicated test/CI cycle may support only the bounded `T` and `C` dimensions for the extractor contract. It does **not** execute the immutable real NOVOexport bytes and does **not** close public/legal/scientific joins.

Therefore, until separately evidenced:

- `X=TOKEN_VAZIO_REAL_NOVOEXPORT_EXACT_BYTES_NOT_EXECUTED`
- `F=TOKEN_VAZIO_PUBLIC_LEGAL_SCIENTIFIC_JOIN_NOT_CLOSED`
- `claim_allowed=false`

## Materialized surfaces

- `tests/test_novoexport_anteriority_events_v1.py`
- `.github/workflows/prov002-anteriority-audit.yml`
- `data/receipts/invariants/PROV002_DEDICATED_TEST_CI_PREPROMOTION_20260818_V1.json`

## Promotion rule

Creation of tests/workflow is not evidence that CI passed. A fresh run bound to the branch head must be observed before `T` or `C` can be promoted to `PASS` in the canonical invariant registry.

## Next gate

After an observed fresh CI success, append a run-bound receipt and update `MAP-INV-PROV-002` to reference the dedicated test/workflow while preserving `X/F` as `TOKEN_VAZIO`.
