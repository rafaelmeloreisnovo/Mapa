# JSON Totality Invariant Index V1

- Contract: `docs/canonical/2026-08-25/JSON_TOTALITY_INVARIANT_CONTRACT_V1.md`
- Auditor: `scripts/audit_json_totality_invariants.py`
- Report schema: `schemas/json-totality-invariant-audit.v1.schema.json`
- CI: `.github/workflows/json-totality-invariant.yml`
- Positive fixture: `tests/fixtures/json_totality/messages-pass.jsonl`
- Negative fixture: `tests/fixtures/json_totality/messages-gap.jsonl`
- Tests: `tests/test_json_totality_invariants.py`
- Initial observed Drive scope: `data/audits/JSON_TOTALITY_INVARIANT_SCOPE_20260825.v1.json`
- Receipt namespace: `receipts/json-totality/`

## Mother invariant

`representation_may_evolve_but_identity_provenance_lineage_epistemic_boundary_must_remain_traceable`

## Gate

`FULL_TOTALITY_CLOSED` remains blocked until the complete governed corpus manifest is fixed, hashed and audited with conservation rate 1.0 across all five invariant dimensions.

`claim_allowed=false`
