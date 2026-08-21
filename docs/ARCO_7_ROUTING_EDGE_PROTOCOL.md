# ARCO 7: Routing Edge Protocol

## Overview
ARCO 7 defines the routing edge semantics for externalized source resolution and fallback strategy management at the boundary between control-plane contracts and provider-specific implementations.

## Edge Classification

### Type A: Source Resolution Edges
**Condition**: Pinned commit requires recovery
**Detection**: `recovery_rank != rank_0_original_pin`
**Action**: Execute ranked fallback (rank 1 → 2 → 3)
**Custody**: qemu_rafaelia + androidx_RmR providers
**Falsifier**: Resolved SHA validates against consumer ABI contract

### Type B: ABI Validation Edges  
**Condition**: Compiled artifact requires compatibility proof
**Detection**: `abi_validation_state.validated_count < abi_validation_state.contract_count`
**Action**: Execute ABI/integration gate before promotion
**Custody**: Vectras-VM-Android + RafPolimata
**Falsifier**: ANativeActivity observation on actual device

### Type C: Evidence Receipt Edges
**Condition**: Receipt missing for claimed capability
**Detection**: `evidence_id` absent or timestamp stale
**Action**: Block claim until receipt regenerated within current cycle
**Custody**: CI workflow + evidence producer
**Falsifier**: Receipt hash matches canonical artifact

### Type D: Control-plane Reconciliation Edges
**Condition**: Snapshot diverges from HEAD
**Detection**: `observed_at < current_cycle` or commit mismatch
**Action**: Re-validate and update snapshot
**Custody**: Mapa governance layer
**Falsifier**: All 13 live-control-plane tests pass

## Routing Decision Matrix

| Edge Type | Recovery Rank | Status Required | Action | Next Gate |
|-----------|---------------|-----------------|--------|-----------|
| A-Source | rank_0 | VERIFIED_ORIGINAL_PIN | accept | B-ABI |
| A-Source | rank_1+ | TOKEN_VAZIO_PINNED_UNRESOLVED | await | fallback_investigation |
| B-ABI | VALIDATED | token=0 | accept | C-Receipt |
| B-ABI | TOKEN_VAZIO | contract_count>0 | block | abi_investigation |
| C-Receipt | CURRENT | hash_match=true | accept | D-Reconcile |
| C-Receipt | STALE/MISSING | claim=false | block | regenerate_receipt |
| D-Reconcile | SYNCED | tests_pass=13/13 | accept | promotion_gate |
| D-Reconcile | DIVERGED | delta_found | await | snapshot_update |

## Implementation Checklist

- [x] Source resolution fallback hierarchy documented
- [x] ABI validation contract enforcement enabled
- [x] Receipt timestamp and hash validation required
- [x] Snapshot reconciliation on every cycle
- [ ] Type A edges instrumented in CI (verify_external_sources_v2.sh)
- [ ] Type B edges instrumented in build (abi_validation gates)
- [ ] Type C edges instrumented in receipt producer
- [ ] Type D edges instrumented in snapshot validator

## References

- Operational Gaps: `data/routing/operational-gaps/`
- Recovery Procedures: `data/routing/rollback-procedures/`
- Evidence Schema: `schemas/event-envelope.v1.schema.json`
- Live Control Plane: `data/control-plane/current_state_snapshot.v1.json`
