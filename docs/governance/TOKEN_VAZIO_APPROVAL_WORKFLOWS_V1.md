# TOKEN_VAZIO Approval Workflows V1

## Governance Framework for Explicit Gap Resolution

**Date**: 2026-08-18  
**Framework**: Rafaelia Governance System  
**Scope**: 10 documented TOKEN_VAZIO entries requiring explicit approval chains  
**Status**: Phase 2-P1-03 (In Progress)

---

## Executive Summary

TOKEN_VAZIO entries represent **explicit, documented gaps** in the system. Rather than silently ignoring or assuming resolution, this framework establishes:

1. **Decision Criteria**: What evidence must exist before a gap can be resolved?
2. **Approval Chain**: Which lanes and roles must sign off on closure?
3. **Audit Trail**: How is the resolution decision recorded and made immutable?
4. **Fail-Closed Gates**: What prevents premature gap closure without evidence?

**Principle**: *Silence is forbidden. Gaps must be explicitly resolved or explicitly preserved.*

---

## Core Design: The 3-Gate Approval Model

All TOKEN_VAZIO resolution follows a 3-gate progression:

```text
GATE 1: Evidence Gathering
  ├─ Observation: Gap documented with concrete impact
  ├─ Provenance: Root cause identified (not fabricated)
  ├─ Evidence: Artifacts, receipts, or test results supporting closure
  └─ State: EVIDENCE_COLLECTED (epistemic state = observed)

         ↓ [Lane 04: Validation]

GATE 2: Validation & Falsification
  ├─ Tests: Falsifiers exist and pass (not just positive tests)
  ├─ Review: Lane 04 (Validação) confirms falsifiers are sound
  ├─ Documentation: Falsifier intent and failure mode documented
  └─ State: VALIDATOR_APPROVED (epistemic state = tested)

         ↓ [Lane 00: Governance + Lane 06: Integracao]

GATE 3: Approval & Integration
  ├─ Policy: Lane 00 (Governança) authorizes closure
  ├─ Integration: Lane 06 (Integração) confirms no cascading gaps
  ├─ Audit: Decision appended to TOKEN_VAZIO_APPROVAL_DECISIONS.jsonl
  └─ State: APPROVED_CLOSED or APPROVED_PRESERVED (epistemic = promoted)

         ↓ Final State Machine Transition

CANONICAL_TOKEN_RESOLVED
```

**Key Rules**:

- No backward transitions: Once EVIDENCE_COLLECTED, cannot revert to DOCUMENTED
- Author cannot self-approve (Lane 00 required)
- All decisions are append-only (immutable history)
- claim_allowed=false until final approval

---

## The 10 TOKEN_VAZIO Entries & Decision Criteria

### Group 1: RUNTIME COMPATIBILITY (P1: High Severity)

#### 1. TOKEN_VAZIO_PINNED_ACTION_NODE24_NATIVE_COMPATIBILITY_NOT_VERIFIED

**Priority**: P2 (Medium)  
**Severity**: medium  
**Affected**: `actions/checkout v11d596`, GitHub Actions runtime  
**Description**: Node 24 native build compatibility unverified (only tested on Node 20).

**Evidence Needed for GATE 1**:

- [ ] Run pinned action SHA on actual Node 24 runner
- [ ] Capture actual runner logs showing Node 24 execution
- [ ] Artifact: GitHub Actions job output with Node 24 timestamp
- [ ] Provenance: Link to specific workflow run that tested on Node 24

**Falsifiers for GATE 2**:

- Falsifier 1: "If action fails on Node 24 with incompatibility error → gap stays open"
- Falsifier 2: "If runtime behavior differs (exit codes, output) → gap stays open"
- Test: Run action on Node 24 runner; capture behavior; compare to Node 20 baseline

**Approval Chain for GATE 3**:

- Lane 04 (Validação): Confirms falsifiers passed
- Lane 06 (Integração): Confirms no other actions broken by Node 24 upgrade
- Lane 00 (Governança): Authorizes closure → Can update production workflows to Node 24

**Resolution Path**:

- If approved: Close and update `.github/workflows/*.yml` to require Node 24
- If rejected: Preserve until GitHub provides Node 24-native action

---

#### 2. NODE20_ACTION_RUNTIME_DEPRECATION_WARNING_OBSERVED

**Priority**: P1 (High - CRITICAL PATH)  
**Severity**: high  
**Affected**: GitHub Actions runtime, all workflows using actions/checkout  
**Description**: GitHub deprecating Node 20. Must migrate before deadline (2026-12-31).

**Evidence Needed for GATE 1**:

- [ ] GitHub announcement: Node 20 deprecation timeline
- [ ] Artifact: Official GitHub Actions runtime deprecation notice
- [ ] Impact analysis: Which workflows are affected
- [ ] Mitigation plan: Upgrade path (Node 24 or alternatives)

**Falsifiers for GATE 2**:

- Falsifier 1: "If no viable Node 24 actions exist → cannot close gap"
- Falsifier 2: "If Node 24 migration breaks existing workflows → cannot close gap"
- Test: Verify Node 24 action replacements exist and work

**Approval Chain for GATE 3**:

- Lane 07 (Segurança): Risk assessment of Node 20 deprecation timeline
- Lane 06 (Integração): Test Node 24 migration plan
- Lane 00 (Governança): Authorize migration schedule before 2026-12-31

**Resolution Path**:

- If approved by 2026-10-01: Execute Node 24 migration via Phase 2-P1-02 extended
- If 2026-12-31 passes: Forced resolution (GitHub removes Node 20 support)

---

#### 3. TOKEN_VAZIO_DEPENDENCY_LICENSE_COMPATIBILITY_NOT_AUDITED

**Priority**: P2 (Medium)  
**Severity**: medium  
**Affected**: External GitHub Actions, CI dependencies  
**Description**: GitHub Actions licenses not formally audited against project policy.

**Evidence Needed for GATE 1**:

- [ ] License audit report: All external actions enumerated
- [ ] Artifact: SPDX license data for each action
- [ ] Compatibility matrix: Action licenses vs project policy
- [ ] Provenance: Links to official action repositories

**Falsifiers for GATE 2**:

- Falsifier 1: "If GPL action found in Apache 2.0 project → incompatible"
- Falsifier 2: "If proprietary action without commercial license → incompatible"
- Test: Run license check tool (e.g., FOSSA, Black Duck) on action commits

**Approval Chain for GATE 3**:

- Lane 07 (Segurança): Legal/compliance review of license compatibility
- Lane 00 (Governança): Approve license list or request action replacements

**Resolution Path**:

- If approved: Document approved action license list
- If incompatible actions found: Flag for removal or replacement

---

### Group 2: VALIDATION & TESTING (P1: High Severity)

#### 4. TOKEN_VAZIO_FALSIFIER_COVERAGE_INCOMPLETE

**Priority**: P1 (High)  
**Severity**: high  
**Affected**: Test suite (106 tests), validation framework  
**Description**: Tests lack explicit falsifier documentation. No structured falsifier registry.

**Evidence Needed for GATE 1**:

- [ ] Falsifier registry created: `tests/FALSIFIER_REGISTRY.jsonl`
- [ ] 106 tests mapped to falsifiers: Test → Falsifier intent
- [ ] Artifact: Tool output listing all falsifier intents
- [ ] Provenance: Link to test implementations

**Falsifiers for GATE 2**:

- Falsifier 1: "If test only checks positive case (no failure scenario) → incomplete"
- Falsifier 2: "If falsifier intent not documented → gap remains open"
- Test: Audit test suite for negative test coverage; document intents

**Approval Chain for GATE 3**:

- Lane 04 (Validação): Review falsifier registry completeness
- Lane 06 (Integração): Confirm all tests still pass with registry
- Lane 00 (Governança): Authorize falsifier registry as source of truth

**Resolution Path**:

- If approved: Falsifier registry becomes binding; tests must declare intent
- Status: PARTIALLY_RESOLVED → (waiting for GATE 1 completion)

---

#### 5. TOKEN_VAZIO_NEGATIVE_TEST_FIXTURES_MISSING

**Priority**: P1 (High)  
**Severity**: high  
**Affected**: Test fixtures, data test inputs  
**Description**: No structured negative test data. Failure scenarios not pre-baked.

**Evidence Needed for GATE 1**:

- [ ] Negative fixture set created: `tests/fixtures/negative/`
- [ ] Artifact: Malformed/invalid data files for each test scenario
- [ ] Provenance: Documented failure modes each fixture triggers
- [ ] Coverage: Minimum 2 negative fixtures per 3 positive tests (ratio)

**Falsifiers for GATE 2**:

- Falsifier 1: "If negative fixture doesn't fail existing positive test → bad fixture"
- Falsifier 2: "If fixture coverage < 2:3 ratio → gap remains open"
- Test: Run fixtures; confirm they trigger expected failures

**Approval Chain for GATE 3**:

- Lane 04 (Validação): Confirm fixture quality and coverage
- Lane 06 (Integração): Verify negative tests don't break positive cases
- Lane 00 (Governança): Approve negative fixtures as test requirement

**Resolution Path**:

- If approved: Negative fixtures become mandatory for new tests
- If rejected: Document coverage gaps; defer to Phase 3

---

### Group 3: AUDIT & DOCUMENTATION (P1: High Severity)

#### 6. TOKEN_VAZIO_INVARIANTS_CI_BINDING_MISSING

**Priority**: P1 (High)  
**Severity**: high  
**Affected**: CI gates, invariant enforcement  
**Description**: 15 invariants not enforced in CI. No automated validation on every commit.

**Status**: ✅ **RESOLVED in Phase 1-P1-02**

**Evidence Presented**:

- ✅ `tools/check_invariants.py` created (550+ LOC)
- ✅ Integrated into `promotion-control-v1.yml` negative-tests job
- ✅ All 15 invariants validating (15/15 PASS) in production
- ✅ Blocks merge if any invariant fails (fail-closed)

**Falsifiers Verified**:

- ✅ Invariant violations detected before merge
- ✅ No commits land with invariant breaches
- ✅ Audit trail in `data/audits/invariants-validation.json`

**Approval Chain Completed**:

- ✅ Lane 04 (Validação): Confirmed validator correctness
- ✅ Lane 06 (Integração): Verified no gate conflicts
- ✅ Lane 00 (Governança): Authorized as mandatory gate

**Final State**: **APPROVED_CLOSED (2026-08-18)**

---

#### 7. TOKEN_VAZIO_AUDIT_LOGGING_INCOMPLETE

**Priority**: P2 (Medium)  
**Severity**: medium  
**Affected**: CI audit trails, promotion decisions  
**Description**: No centralized audit trail for validation runs or approval history.

**Status**: PARTIALLY_RESOLVED

**Evidence Partial**:

- ✅ Individual audit trails exist:
  - `data/audits/invariants-validation.json` (append-only)
  - `data/audits/action-pinning-audit.jsonl` (Phase 2-P1-01)
  - `data/audits/git-audit.jsonl` (GitHub API calls)
- ❌ No unified audit log aggregator
- ❌ No audit dashboard for approval decisions

**Falsifiers for GATE 2**:

- Falsifier 1: "If audit entry missing timestamp → gap remains open"
- Falsifier 2: "If audit log is mutable (not append-only) → gap remains open"
- Test: Attempt to modify historical audit entry; confirm immutability

**Approval Chain for GATE 3**:

- Lane 08 (Observabilidade): Aggregate audit trails
- Lane 00 (Governança): Approve centralized audit access

**Resolution Path**:

- If approved: Create `tools/aggregate_audit_trail.py` to unify logs
- Estimated completion: Phase 2-P1-05 (Observability layer)

---

#### 8. TOKEN_VAZIO_PRIVACY_AUDIT_NOT_PERFORMED

**Priority**: P1 (High)  
**Severity**: high  
**Affected**: Audit trails, CI logs, receipts  
**Description**: Report and audit trails may contain sensitive GitHub runner metadata.

**Status**: PARTIALLY_RESOLVED

**Evidence Partial**:

- ✅ Security audit conducted (`tools/security_audit.py`)
- ✅ Sensitive fields identified in `WORKFLOW_RECEIPTS_VALIDATION_REPORT.md`
- ✅ CI logs configured for no persistent storage
- ❌ No formal LGPD/GDPR compliance audit
- ❌ No data retention policy documented

**Falsifiers for GATE 2**:

- Falsifier 1: "If GitHub token found in logs → gap remains open"
- Falsifier 2: "If runner IP/hostname leaked → gap remains open"
- Test: Scan `data/audits/` and `WORKFLOW_RECEIPTS_VALIDATION_REPORT.md` for PII

**Approval Chain for GATE 3**:

- Lane 07 (Segurança): Formal privacy audit (LGPD/GDPR assessment)
- Lane 00 (Governança): Approve data retention and privacy policy

**Resolution Path**:

- If approved: Document approved data retention policy
- If rejected: Redact sensitive fields from stored reports

---

### Group 4: DOCUMENTATION & VISION (P2: Low Severity)

#### 9. TOKEN_VAZIO_DOCUMENTATION_GAPS_ARCO7_LANES_INVARIANTS

**Priority**: P2 (Low)  
**Severity**: low  
**Affected**: Framework documentation, cross-references  
**Description**: Arco 7 schema incomplete. Lanes audit touchpoints unclear. Invariants not cross-referenced.

**Status**: PARTIALLY_RESOLVED (3/4 docs completed)

**Evidence Partial**:

- ✅ 7 Arcos documented: `/docs/architecture/RAFAELIA_7_ARCOS_RAFCONVERT_RAFDISK_V1.md`
- ✅ 10 Lanes documented: `/docs/governance/BRANCH_TOPOLOGY_MAIN_NUMBERED_V1.md`
- ✅ 15 Invariants documented: `/docs/INVARIANTES_NECESSIDADE_URGENCIA_GRUPAMENTOS.md`
- ❌ Arco 7 (psi' / routing / retrospection) incomplete
- ❌ Lane audit touchpoints not all mapped
- ❌ Cross-reference index missing

**Falsifiers for GATE 2**:

- Falsifier 1: "If Arco 7 schema doesn't match actual routing behavior → incomplete"
- Falsifier 2: "If invariant not mentioned in test suite → gap remains open"
- Test: Verify every invariant has at least one test; every lane has audit point

**Approval Chain for GATE 3**:

- Lane 06 (Integracao): Verify documentation consistency
- Lane 00 (Governanca): Approve documentation as canonical

**Resolution Path**:

- If approved: Mark documentation complete; add cross-reference index
- Estimated: Phase 2-P1-06 (Documentation refinement)

---

#### 10. TOKEN_VAZIO_MISSING_RECEIPTS_WORKFLOW_8_9_10

**Priority**: P2 (Low)  
**Severity**: low  
**Affected**: Historical receipt validation  
**Description**: Only runs 404-407 examined. No continuous validation for all historical runs.

**Evidence Needed for GATE 1**:

- [ ] Extended receipt validation: Runs 1-407 examined
- [ ] Artifact: `data/audits/RAFAELIA_ADAPTIVE_CYCLE_COMPLETE_HISTORY.json`
- [ ] Provenance: Links to historical run artifacts
- [ ] Coverage: Confirmed no receipt gaps in sequence

**Falsifiers for GATE 2**:

- Falsifier 1: "If any run 1-407 missing receipt → gap remains open"
- Falsifier 2: "If receipt sequence has breaks → gap remains open"
- Test: Verify continuous receipt chain; no missing entries

**Approval Chain for GATE 3**:

- Lane 05 (Evidências): Confirm historical receipt chain complete
- Lane 00 (Governança): Approve historical audit closure

**Resolution Path**:

- If approved: Historical receipts considered complete
- If gaps found: Document which runs lack receipts; update estimate
- Estimated completion: Phase 2-P1-04 (Federated Producer Repositories)

---

## Decision Matrix: Approval Criteria by Group

| TOKEN_VAZIO | Priority | Evidence | Validator | Approver | Timeline |
|---|---|---|---|---|---|
| LICENSE_COMPATIBILITY | P2 | SPDX audit | Lane 07 | Lane 00 | 2026-09-30 |
| NODE24_COMPATIBILITY | P2 | Node 24 test run | Lane 04 | Lane 00 | 2026-09-15 |
| NODE20_DEPRECATION | P1 | GitHub notice | Lane 07 | Lane 00 | 2026-10-01 |
| FALSIFIER_COVERAGE | P1 | Registry audit | Lane 04 | Lane 00 | 2026-09-30 |
| NEGATIVE_FIXTURES | P1 | Fixture validation | Lane 04 | Lane 00 | 2026-09-30 |
| INVARIANTS_CI_BINDING | P1 | ✅ RESOLVED | ✅ Lane 04 | ✅ Lane 00 | ✅ 2026-08-18 |
| AUDIT_LOGGING | P2 | Audit aggregation | Lane 08 | Lane 00 | 2026-10-15 |
| PRIVACY_AUDIT | P1 | LGPD assessment | Lane 07 | Lane 00 | 2026-09-15 |
| DOCUMENTATION_GAPS | P2 | Cross-reference index | Lane 06 | Lane 00 | 2026-09-30 |
| MISSING_RECEIPTS | P2 | Historical chain | Lane 05 | Lane 00 | 2026-09-30 |

---

## Append-Only Approval Decision Log

New decisions logged to: `data/audits/TOKEN_VAZIO_APPROVAL_DECISIONS.jsonl`

Format per decision:

```json
{
  "timestamp": "2026-08-18T23:54:00Z",
  "token_vazio_id": "TOKEN_VAZIO_INVARIANTS_CI_BINDING_MISSING",
  "decision": "APPROVED_CLOSED",
  "evidence_package": {
    "pr": "#278",
    "commit_sha": "3a2c8f...",
    "artifact": "tools/check_invariants.py",
    "audit_trail": "data/audits/invariants-validation.json"
  },
  "validator_lane": "04_validacao",
  "approver_lane": "00_governanca",
  "resolution_notes": "15 invariants binding enforced in CI; blocks merge on violation",
  "state_transition": "DOCUMENTED → EVIDENCE_COLLECTED → VALIDATOR_APPROVED → APPROVED_CLOSED",
  "epistemic_level": "CANONICAL_TOKEN_RESOLVED"
}
```

---

## Integration with Fail-Closed State Machine

Each TOKEN_VAZIO approval follows the 7-state machine:

```text
TOKEN_VAZIO → DOCUMENTED (entry point)
    ↓ [Gap explicitly identified, not silent]
    ↓ [Layer 2: Gap in 7 directions]
    ↓
EVIDENCE_COLLECTED (GATE 1 passed)
    ↓ [Artifacts exist; provenance clear]
    ↓ [Layer 5: Identidade + Linhagem hold]
    ↓
VALIDATOR_APPROVED (GATE 2 passed)
    ↓ [Falsifiers pass; validators sign off]
    ↓ [Layer 4: Invariant I2-I7 verified]
    ↓
REVIEW_APPROVED (GATE 3a passed)
    ↓ [Governance lane reviews decision]
    ↓ [Layer 6: Lane 00 authority invoked]
    ↓
MERGED_PROTECTED (GATE 3b passed)
    ↓ [No cascading gaps; integration holds]
    ↓ [Layer 5: Fechamento verified]
    ↓
CANONICAL_TOKEN_RESOLVED (final)
    ↓ [Decision append-only; immutable]
    ↓ [claim_allowed can now be true for this gap]
```

**Key Difference from Normal State Machine**:

- TOKEN_VAZIO starts at DOCUMENTED (not OBSERVED)
- Can transition to APPROVED_PRESERVED (gap stays open by design)
- Decision is tracked as governance event, not code merge

---

## Next Steps: Phase 2-P1-03 Execution

### Week 1 (2026-08-18 to 2026-08-25)

1. Create `data/audits/TOKEN_VAZIO_APPROVAL_DECISIONS.jsonl` (append-only log)
2. Record GATE 3 completion for `TOKEN_VAZIO_INVARIANTS_CI_BINDING_MISSING`
3. Start GATE 1 for top-3 P1 entries (Node20, Falsifier, Privacy)

### Week 2-3 (2026-08-26 to 2026-09-08)

1. Complete GATE 1 & 2 evidence gathering for P1 entries
2. Submit to Lane 00 for GATE 3 approval decisions
3. Create PR with approval decisions log

### Week 4+ (2026-09-09 onwards)

1. Track resolution timelines; escalate blockers to Lane 00
2. Integrate resolved gaps into appropriate phases (P1-04, P1-05, etc.)
3. Preserve approved-but-unresolved gaps in documentation

---

## Appendix: TOKEN_VAZIO Philosophy

**Why Track Gaps Explicitly?**

In traditional systems, gaps become:

- **Silent assumptions**: "It probably works"
- **Technical debt**: "We'll fix it later"
- **Lost knowledge**: "Who knew about this?"

In Rafaelia, TOKEN_VAZIO means:

- **Explicit documentation**: "We know about this"
- **Tracked timeline**: "Here's when we plan to resolve it"
- **Audit trail**: "Here's who approved leaving it open"
- **Decision context**: "Here's why we made this choice"

**The Socratic principle applies**: *I know that I do not know this thing. Let me document it explicitly rather than pretend.*

When a gap is APPROVED_PRESERVED (kept open by design), that decision itself is governance. When a gap is APPROVED_CLOSED (resolved), the decision trail proves it.

Silence → Safety is an illusion.  
**Explicit gaps → Auditable system.**

---

## References

- Framework: `/docs/SEMENTEIRA_CONTEXT_SUSTAINMENT_5X7_V1.md`
- Invariants: `/docs/INVARIANTES_NECESSIDADE_URGENCIA_GRUPAMENTOS.md`
- Governance: `/docs/governance/PROOF_CUSTODY_AND_TOKEN_VALIDITY_V1.md`
- Lane topology: `/docs/governance/BRANCH_TOPOLOGY_MAIN_NUMBERED_V1.md`
- Registry: `/data/audits/TOKEN_VAZIO_REGISTRY.jsonl`
- Approval decisions: `/data/audits/TOKEN_VAZIO_APPROVAL_DECISIONS.jsonl` (to be created)
