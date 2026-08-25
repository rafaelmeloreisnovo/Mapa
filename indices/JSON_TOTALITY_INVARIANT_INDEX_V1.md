# JSON Totality Invariant Index V1

- Contract: `docs/canonical/2026-08-25/JSON_TOTALITY_INVARIANT_CONTRACT_V1.md`
- Content auditor: `scripts/audit_json_totality_invariants.py`
- Provider-scope validator: `scripts/validate_json_totality_scope.py`
- Report schema: `schemas/json-totality-invariant-audit.v1.schema.json`
- CI: `.github/workflows/json-totality-invariant.yml`
- Positive fixture: `tests/fixtures/json_totality/messages-pass.jsonl`
- Negative fixture: `tests/fixtures/json_totality/messages-gap.jsonl`
- Tests: `tests/test_json_totality_invariants.py`
- Observed Drive scope: `data/audits/JSON_TOTALITY_INVARIANT_SCOPE_20260825.v1.json`
- Receipt namespace: `receipts/json-totality/`

## Mother invariant

`representation_may_evolve_but_identity_provenance_lineage_epistemic_boundary_must_remain_traceable`

## Provider identity invariant

`filename_alone_is_not_identity`

Provider objects are routed by provider ID + parent ID + title. Homonymous files from different parents are never silently collapsed.

## Current observed coverage

- primary `MESSAGES-00001..00019`: provider IDs observed;
- primary `NODES-00001..00019`: provider IDs observed;
- primary `ASSETS-00001..00003`: provider IDs observed;
- secondary homonymous family: observed partially and kept distinct.

This is provider-scope recovery, not yet a byte-level audit of every object.

## Gate

`FULL_TOTALITY_CLOSED` remains blocked until the complete governed corpus manifest is fixed, hashed and audited with conservation rate 1.0 across all five invariant dimensions.

`claim_allowed=false`
