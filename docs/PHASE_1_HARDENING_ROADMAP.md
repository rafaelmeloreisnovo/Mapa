# Phase 1: Security Hardening & Integrity Binding
**Date**: 2026-08-18  
**Status**: Planning (Phase 0 Complete)  
**Priority**: P0 (Critical Security)  
**Foundation**: Security audit findings (S1-01 through S1-04)

---

## Overview

Phase 1 hardens the Rafaelia governance system by:
1. **Improving workflow action pinning strategy** (33 workflows, 67 unpinned actions)
2. **Binding 15 Invariants into CI/CD pipeline** (framework enforcement)
3. **Documenting TOKEN_VAZIO approval paths** (explicit gap tracking)
4. **Preparing federated producer repositories** (multi-repo governance)

---

## Phase 1 Tasks (P0/P1)

### Task P1-01: GitHub Actions SHA Pinning (Deferred to Phase 2)

**Status**: Analysis complete, implementation deferred  
**Scope**: 33 workflows, 67 unpinned action references  
**Blocker**: Commit SHAs must be validated against actual action repositories

**Challenge**: 
- Initial approach used hardcoded SHAs (failed CI validation)
- GitHub Actions requires real commit SHAs from source repositories
- Cannot proceed without valid SHAs

**Phase 2 Approach**:
1. Create `tools/resolve_action_shas.py` to query GitHub API
2. For each action (actions/checkout@v4, etc.):
   - Resolve version tag to actual commit SHA
   - Validate SHA is recognized by GitHub Actions
3. Bulk-replace with validated SHAs
4. Comprehensive testing across all 33 workflows

**Workflows Affected**:
- 33 of 56 workflows have unpinned actions
- 67 total action references to pin

---

### Task P1-02: Invariants CI Binding (Phase 2 foundation)

**Status**: Ready for implementation  
**Scope**: 15 invariants → automated CI checks  
**Deliverable**: `tools/check_invariants.py` (CI-integrated validator)

**Maps to invariants**:
1. **fonte original imutável** → artifact immutability checker
2. **privacidade antes da interpretação** → PII exposure scanner
3. **nenhuma reidentificação presumida segura** → anonymization validator
4. **evidência antes da promoção** → evidence requirement gate
5. **causa-raiz não inventada** → root-cause verification
6-15. Individual constraint validators (privacy, dependencies, versioning, etc.)

**Approach**:
- Build CI step that runs invariants checks on every commit
- Block merges if any invariant violated
- Create audit trail of invariant check results

---

### Task P1-03: TOKEN_VAZIO Approval Gates (Deferred)

**Status**: 10 entries documented (Phase 0 complete)  
**Scope**: Each TOKEN_VAZIO → explicit approval chain  
**Next Step**: Define approval processes for each gap

---

### Task P1-04: Federated Producer Repositories (Phase 2+)

**Status**: Architecture design phase  
**Scope**: Support multi-repo workflows with shared governance  
**Goal**: Allow external producers to emit receipts in Rafaelia format

---

## Phase 1 Realistic Scope

Given Phase 0 completion and technical constraints:

**Do in Phase 1**:
- [ ] P1-02: Implement 15 Invariants CI binding (tractable, high value)
- [ ] Document lessons from P1-01 SHA pinning attempt
- [ ] Prepare Phase 2 roadmap with tool requirements

**Defer to Phase 2**:
- [ ] P1-01: GitHub Actions SHA pinning (requires external validation)
- [ ] P1-03: TOKEN_VAZIO approval gate workflows (governance decision required)
- [ ] P1-04: Federated producer repositories (architectural work)

---

## Phase 1 Success Criteria

✓ Phase 0 remains stable (no regressions)  
✓ 15 Invariants CI binding implemented and tested  
✓ Clear Phase 2 roadmap with tool specifications  
✓ GitHub Actions pinning strategy documented (for Phase 2 execution)  

---

## Timeline

- **P1-02 (Invariants CI)**: This session (2-3 hours)
- **Phase 2 prep**: Document tool specs and dependencies
- **Phase 2 (P1-01 + P1-03 + P1-04)**: Next session (6-8 hours)

---

## Lessons Learned (Phase 0→Phase 1)

1. **External validation required**: Actions pinning requires real GitHub data
2. **Hardcoding risky**: SHAs must be validated, not assumed
3. **Modular approach**: Better to defer than to implement halfway
4. **Phase 0 solid**: All documentation and validation frameworks stable

---

## References

- `security-audit.json`: S1-03 identified 33 workflows to pin
- `docs/INVARIANTES_NECESSIDADE_URGENCIA_GRUPAMENTOS.md`: 15 Invariants definition
- `data/audits/TOKEN_VAZIO_REGISTRY.jsonl`: 10 documented gaps
- `.github/workflows/`: 56 workflow files (33 need pinning audit)
