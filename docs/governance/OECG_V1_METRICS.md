# OECG V1 metrics

> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧

Metrics are used for process control, not to claim a statistical Six Sigma level unless opportunities/defects and sampling assumptions are explicitly defined.

## Bounded operational metrics

- `gate_resolution_rate = resolved_applicable_gates / applicable_gates`
- `typed_gap_rate = typed_unresolved_gaps / required_fields`
- `provenance_coverage = records_with_source_revision_or_hash / material_records`
- `reproduction_coverage = reproducible_material_records / material_records`
- `rollback_coverage = records_with_tested_or_explicit_rollback / material_mutations`
- `contradiction_capture_rate = preserved_known_contradictions / observed_known_contradictions`
- `receipt_coverage = material_mutations_with_receipt / material_mutations`
- `stale_pointer_rate = stale_active_pointers / active_pointers_checked`
- `privacy_unknown_rate = applicable_records_with_TOKEN_VAZIO_privacy / applicable_records`
- `nibiguiri_unknown_cause_rate = recovery_candidates_with_CAUSA_DESCONHECIDA / recovery_candidates`

## Interpretation boundary

A ratio is only valid for its declared population/window. No extrapolation from a repository, branch, sample, CI job or fixture to the whole RAFAELIA corpus without an explicit bridge.

`0 unresolved observed` does not mean `0 unresolved exists` unless coverage is demonstrated.
