# Phase 0 Foundation Reconciliation — 2026-08-28

## Status

RECONCILED_WITH_OPEN_FINDINGS
claim_allowed=false

This record is an additive correction to the historical Phase 0 checklist. It
does not delete, rewrite, or promote any previous receipt.

## Exact scope

- Repository: rafaelmeloreisnovo/Mapa
- Baseline: main@ed8a60fce58700a49f2255782529174ca3fdf443
- Comparison checkout: PR #449 head
  c08ccc61b163b30d293c714f2279ad5fc0be172a
- Authority: Mapa for federation, validation, custody, and gap documentation.
  Producer/runtime claims remain owned by their producer repositories.

## Findings from the baseline audit

The four requested documentation artifacts were already present:

1. docs/ARCO_7_ROUTING_EDGE_PROTOCOL.md
2. docs/OBSERVATIONS_MAPPING_MATRIX.md
3. docs/LANES_TOUCHPOINTS_CATALOG.md
4. docs/FRAMEWORK_REFERENCE_CARD.md

No duplicate copies were created. Their presence is now bound by
data/control-plane/phase_0_foundation_manifest.v1.json.

The legacy Phase 0 validator returned 5/5, but the audit found three
limitations:

1. Its observation check reads current_state_snapshot.v1.json, which has no
   modules array, and therefore reports 0% coverage while still passing.
2. Its TOKEN_VAZIO scan traverses JSON files but not the canonical JSONL
   registry, so it does not enforce the registry's full field contract.
3. The legacy security script returns success when unpinned actions are found.
   The legacy scan reported 55 tag references; the strict v2 scan observes 44
   unpinned remote action references under its recursive workflow scope. This
   is an open hardening finding, not a clean security result.

The checklist also references validator filenames that are not present in the
checkout: validate_orchestrator_gates.py, validate_evidence_uniqueness.py,
validate_lane_dag.py, and validate_observation_coverage.py. The versioned v2
validator provides one explicit executable route instead of leaving those
references unresolved.

## Implemented additive correction

- data/control-plane/phase_0_foundation_manifest.v1.json binds the four docs,
  four Phase 0 TOKEN_VAZIO entries, five audit logs, lane DAG, and O1–O8 matrix.
- schemas/phase-0-foundation-manifest.v1.schema.json defines the minimum
  machine-readable shape.
- scripts/validate_phase_0_foundation_v2.py performs strict read-only checks
  for claim boundary, documentation markers, falsifiers, approval locations,
  evidence uniqueness, DAG acyclicity, O1–O8 coverage, and audit-log syntax.
- tools/phase_0_security_audit_v2.py separates hard failures from
  PASS_WITH_OPEN_FINDINGS and never emits secret values.
- tests/test_phase_0_foundation_v2.py adds adversarial tests for each
  fail-closed condition.
- .github/workflows/phase-0-foundation-v2.yml runs the v2 checks with
  immutable action pins and rejects pull-request deletions.

## Non-regression boundary

The historical requirement 106/106 is preserved as a requirement, but no
reproducible current command or test manifest was found that establishes that
scope. It remains TOKEN_VAZIO.

An independent baseline run of the current checkout collected 873 unittest
cases and observed 3 failures plus 9 import/runtime errors, matching the
pre-existing repository state recorded in the older Phase 0 report. The
targeted secret-hygiene tests pass 10/10, and the legacy framework validator
passes 4/4. These results do not certify the full suite as green.

## Acceptance boundary

The additive foundation can be accepted only as:

DOCUMENTATION_AND_VALIDATION_STRUCTURE_VERIFIED_WITH_SECURITY_FINDING

It is not:

- 106/106_NON_REGRESSION_PROVED
- PHYSICAL_RUNTIME_VERIFIED
- GLOBAL_EXHAUSTIVITY_PROVED
- SCIENTIFIC_CLAIM_PROMOTED

## Retroalimentação

F_ok: four documentation artifacts are present, their routes are now
machine-bound, strict gates and adversarial tests are added, and the security
finding is visible instead of masked.

F_gap: action pinning, the historical 106-test scope, existing full-suite
failures/errors, physical runtimes, and provider-side merge enforcement remain
open.

F_next: run the new workflow on the draft branch, pin the 55 reported action
references through a reviewed hardening change, and append a receipt only after
the requested non-regression scope has a reproducible test manifest.
