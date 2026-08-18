# Phase 1: Security Hardening & Integrity Binding
**Date**: 2026-08-18  
**Status**: Initiated (Phase 0 Complete)  
**Priority**: P0 (Critical Security)  
**Foundation**: Security audit findings (S1-03, S1-04)

---

## Overview

Phase 1 hardens the Rafaelia governance system by:
1. **Pinning GitHub Actions to specific commit SHAs** (32 workflows identified in S1-03)
2. **Binding 15 Invariants into CI/CD pipeline** (Phase 2 foundation)
3. **Documenting TOKEN_VAZIO approval criteria** (S1-04 prepared 10 entries)
4. **Federating producer repositories** (multi-repo governance)

---

## Phase 1 Tasks (P0 Urgent)

### Task P1-01: GitHub Actions SHA Pinning

**Status**: Ready (audit S1-03 completed)  
**Scope**: 32 workflows identified for pinning upgrade  
**Definition of Done**: All 32 workflows upgraded to commit SHA format

**What**: Convert all `@v1.x`, `@latest`, `@main` references to specific commit SHAs:
- Identifies tampering risk if action source changes
- Enforces reproducibility (same inputs = same action bytecode)
- Prevents automatic updates that could introduce vulnerabilities

**Workflow files to update**:
- `.github/workflows/*.yml` (56 total in Phase 0 scan)
- Focus on 32 unpinned (priority: critical actions first)

**Implementation approach**:
1. Run GitHub API query for each action to get latest commit SHA
2. Replace version tags with commit SHAs
3. Document old→new mapping in audit log
4. Test each workflow to verify pinning doesn't break functionality

**Priority order**:
1. `promotion-control-v1.yml` (high security impact)
2. `rafaelia-adaptive-cycle.yml` (data flow impact)
3. All security/compliance workflows
4. All CI/CD validation workflows
5. Documentation/reporting workflows

---

### Task P1-02: Invariants CI Binding (Planned for Phase 2)

**Status**: Planning (Phase 2 preparation)  
**Scope**: 15 invariants → automated CI checks  
**Tool**: `tools/check_invariants.py` (to be created)

Maps to Phase 2 plan:
- I1-01: fonte original imutável → artifact immutability checker
- I1-02: privacidade antes da interpretação → PII exposure scanner
- I1-03 through I1-15: individual constraint validators

---

### Task P1-03: TOKEN_VAZIO Approval Gates (Planned)

**Status**: Documented (10 entries in audit)  
**Scope**: Each TOKEN_VAZIO → explicit approval chain  
**Criteria**: Each entry includes approval gate and resolution path

---

### Task P1-04: Federated Producer Repositories (Planned)

**Status**: Architecture design (post Phase 1)  
**Scope**: Support multi-repo workflows with shared governance  
**Goal**: Allow external producers to emit receipts in Rafaelia format

---

## Phase 1 Success Criteria

✓ All 32 unpinned workflows converted to SHA format  
✓ Zero regressions: existing tests 106/106 pass  
✓ All 10 TOKEN_VAZIO entries have approval paths defined  
✓ Audit logs record all workflow migrations  
✓ Security rescan: S1-01 through S1-04 still passing  

---

## Timeline

- **P1-01 (GitHub Actions pinning)**: Immediate (this session)
- **P1-02 (Invariants binding)**: Phase 2 (next 4 hours)
- **P1-03 (TOKEN_VAZIO gates)**: Phase 2 (parallel)
- **P1-04 (Federated repos)**: Phase 2+ (architecture work)

---

## References

- `security-audit.json`: S1-03 identified 32 workflows
- `tools/security_audit.py`: Audit tool that found these issues
- `.github/workflows/`: All workflow files to be updated
- `docs/FRAMEWORK_REFERENCE_CARD.md`: Framework layer overview
