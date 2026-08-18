# 10 Operational Lanes: Audit Touchpoints and Governance Flow

**Version**: 1.0  
**Date**: 2026-08-18  
**Source**: `/docs/governance/BRANCH_TOPOLOGY_MAIN_NUMBERED_V1.md`

---

## Overview

The Rafaelia governance structure routes work through 10 operational lanes (00-09), each with a distinct responsibility and audit touchpoint. This document maps each lane to:

1. **Audit artifacts** — Where evidence is recorded

2. **Decision gates** — What triggers work entry/exit

3. **Fail-closed rules** — How the lane prevents silent failure

4. **Workflow touchpoints** — Which GitHub Actions tasks belong here

---

## Lane 00: **GOVERNANCE**

**Branch**: `main_00_governanca`  
**Responsibility**: Authority, scope, vocabulary, policy

### Audit Artifacts

- `/data/control-plane/promotion-control.v1.json` — Promotion policy (invariants, approval count)

- `/docs/SEMENTEIRA_CONTEXT_SUSTAINMENT_5X7_V1.md` — 7 directions vocabulary

- `/docs/INVARIANTES_NECESSIDADE_URGENCIA_GRUPAMENTOS.md` — 15 invariants, 8 observations

- `/root/.claude/plans/*.md` — Framework documents

### Decision Gates
- **ENTRY**: Lane 00 proposal (governance issue, policy change, vocabulary update)
- **VERIFICATION**: Authority review (≥1 independent approval, no self-approval)
- **EXIT**: Policy decision document (immutable, append-only, timestamped)

### Fail-Closed Rules

- ✓ No policy change without explicit decision record

- ✓ No vocabulary changes without 7-directions classification

- ✓ All policy becomes binding for downstream lanes immediately

- ✗ Policy cannot be revoked; only replaced (never silent deletion)

### Workflow Touchpoints

- `promotion-control-v1.yml`: Read Lane 00 policy, enforce approval requirements

- No automatic mutations; changes only via explicit review

---

## Lane 01: **INTAKE & PROVENANCE**

**Branch**: `main_01_intake_fontes`  
**Responsibility**: Source identification, quarantine, custody chain

### Audit Artifacts

- `/data/audits/source-inventory.jsonl` — All source entries with intake timestamp

- `/data/audits/custody-chain.jsonl` — Who had the source when

- `/data/receipts/*.receipt.json` — Intake receipts for each source

### Decision Gates
- **ENTRY**: New source candidate (GitHub API, external dependency, user input)
- **QUARANTINE**: Classify source origin, assess risk (PII? External? Transient?)
- **RELEASE**: Source cleared for Lane 02 normalization
- **CUSTODY**: Handoff record signed by source owner

### Fail-Closed Rules

- ✓ Every source enters quarantine; no direct production use

- ✓ Custody chain never breaks; always document handoff

- ✓ PII sources flagged and restricted (never in transit without encryption)

- ✗ Cannot re-classify source retroactively (only new version accepted)

### Workflow Touchpoints

- `rafaelia-adaptive-cycle.yml` — Step: "Capture reviews without exposing token"
  - Reads GitHub API (authenticated)
  - Writes sanitized intake record
  - Does NOT write raw GITHUB_TOKEN to artifact

---

## Lane 02: **NORMALIZATION**

**Branch**: `main_02_normalizacao`  
**Responsibility**: Names, schemas, deduplication

### Audit Artifacts

- `/data/audits/normalization-rules.jsonl` — Schema rules applied

- `/data/receipts/*.normalized.json` — Output after normalization

- `/data/audits/collision-log.jsonl` — Deduplication decisions

### Decision Gates
- **ENTRY**: Source from Lane 01
- **SCHEMA CHECK**: Does source match known schema or require new one?
- **DEDUPLICATION**: Is this a new object or duplicate of existing?
- **EXIT**: Normalized object ready for Lane 03

### Fail-Closed Rules

- ✓ Every object gets unique ID (cycle_id or content hash)

- ✓ Schema versions immutable (only add new versions, never modify old)

- ✓ Collisions logged; never silently merged

- ✗ Cannot drop unmatchable fields; must document why

### Workflow Touchpoints

- Schema validation in CI: `promote-control / negative-tests`
  - Runs `tools/verify_promotion_control.py`
  - Ensures no schema violations in promotion data

---

## Lane 03: **SEMANTIC MODELING**

**Branch**: `main_03_modelagem_semantica`  
**Responsibility**: Ontology, relations, navigation

### Audit Artifacts

- `/docs/SEMANTIC_ONTOLOGY.md` — Current ontology version

- `/data/audits/relation-graph.jsonl` — Object relationships

- `/data/audits/navigation-index.jsonl` — Paths through model

### Decision Gates
- **ENTRY**: Normalized object from Lane 02
- **ONTOLOGY CHECK**: Where does this fit in the ontology?
- **RELATION MAPPING**: What connects to this object?
- **EXIT**: Object with semantic position defined

### Fail-Closed Rules

- ✓ Every object positioned in ontology or explicitly marked as unclassified

- ✓ Relations directional (source → target), acyclic (DAG property)

- ✓ Navigation paths reversible (if A→B, can return B to A)

- ✗ Orphaned objects forbidden; must link or quarantine

### Workflow Touchpoints

- CI validation: Check DAG acyclicity (`tools/validate_dag.py`)

- Emit navigable index: `rafaelia-adaptive-cycle.yml` step "Append current receipt to navigable index"

---

## Lane 04: **VALIDATION & TESTING**

**Branch**: `main_04_validacao`  
**Responsibility**: Linting, tests, falsifiers

### Audit Artifacts

- `/tests/test_*.py` — Test suite (106 tests, all passing)

- `/data/audits/falsifier-coverage.json` — Negative test coverage

- `/data/audits/test-execution-log.jsonl` — Test run records

### Decision Gates
- **ENTRY**: Semantically modeled object from Lane 03
- **LINTING**: Style, format, naming consistency
- **UNIT TESTS**: Behavior correctness
- **FALSIFIER TESTS**: What breaks this object?
- **EXIT**: All tests pass, falsifiers documented

### Fail-Closed Rules

- ✓ Every change must pass 106 existing tests (zero regression)

- ✓ Every test must have a documented falsifier (what would make it fail?)

- ✓ Negative tests required (test the "should not" cases)

- ✗ Cannot skip tests; cannot mark tests as "expected to fail"

### Workflow Touchpoints

- `promotion-control-v1.yml` → `negative-tests` job
  - Runs `python tests/test_promotion_control.py`
  - Compiles Python for syntax errors
  - Executes test fixtures

---

## Lane 05: **EVIDENCE & REPRODUCIBILITY**

**Branch**: `main_05_evidencias`  
**Responsibility**: Hashes, artifacts, receipts

### Audit Artifacts

- `/data/receipts/` — All receipt JSON files

- `/data/audits/artifact-manifest.jsonl` — SHA256 hashes, file sizes

- `/data/audits/reproduction-checklist.jsonl` — Steps to reproduce

### Decision Gates
- **ENTRY**: Validated object from Lane 04
- **ARTIFACT CAPTURE**: Store artifact (file, JSON, binary)
- **HASH BINDING**: Compute SHA256, bind to identity
- **RECEIPT EMISSION**: Create receipt with evidence links
- **EXIT**: Artifact + receipt ready for Lane 06

### Fail-Closed Rules

- ✓ Every artifact must have a cryptographic hash (SHA256 minimum)

- ✓ Hash immutable after initial binding (never re-hash unless new artifact)

- ✓ Receipt must link to artifact and all dependencies

- ✗ Artifacts cannot be modified in-place; only versioning allowed

### Workflow Touchpoints

- `rafaelia-adaptive-cycle.yml` steps:
  - "Execute read-only microcycle" → Generate artifact
  - "Verify receipt boundary" → Emit receipt JSON
  - "Append current receipt to navigable index" → Link receipt to prior receipts

---

## Lane 06: **INTEGRATION & STAGING**

**Branch**: `main_06_integracao`  
**Responsibility**: Module contracts, logical staging

### Audit Artifacts

- `/data/audits/module-contracts.jsonl` — Interface agreements

- `/data/audits/staging-checkpoint.jsonl` — Pre-merge snapshot

### Decision Gates
- **ENTRY**: Evidence + receipt from Lane 05
- **CONTRACT CHECK**: Do all dependencies satisfy module contracts?
- **STAGING**: Place in logical staging area (not production yet)
- **COMPATIBILITY**: No conflicts with existing modules
- **EXIT**: Ready for security/compliance review (Lane 07)

### Fail-Closed Rules

- ✓ Every module dependency must be explicitly declared

- ✓ Version compatibility verified before integration

- ✓ No silent resolution of missing dependencies

- ✗ Cannot integrate if any dependency contract fails

### Workflow Touchpoints

- Integration logic in `raf_emit` module

- Staging area: `/data/receipts/` (immutable, not yet in `main`)

---

## Lane 07: **SECURITY & COMPLIANCE**

**Branch**: `main_07_seguranca_conformidade`  
**Responsibility**: Threat modeling, privacy, regulatory compliance

### Audit Artifacts

- `/data/audits/security-incidents.jsonl` — Threat events

- `/data/audits/compliance-checklist.jsonl` — LGPD/GDPR compliance status

- `/data/audits/token-vazio-registry.jsonl` — Unresolved security gaps

### Decision Gates
- **ENTRY**: Staged module from Lane 06
- **THREAT SCAN**: Vulnerabilities, exposed secrets, injection risks
- **PRIVACY AUDIT**: PII exposure? Data residency? Retention?
- **COMPLIANCE CHECK**: Regulatory requirements met (LGPD, GDPR)?
- **TOKEN VAZIO DECISION**: For unresolved gaps, document and defer or reject
- **EXIT**: Risk opinion (APPROVED / REQUIRES_REMEDIATION / REJECTED)

### Fail-Closed Rules

- ✓ Secrets scan must clear all GitHub tokens, API keys, credentials

- ✓ Privacy violations stop integration (fail-closed)

- ✓ Compliance gaps must be explicitly documented or resolved

- ✗ Cannot proceed if TOKEN_VAZIO_* markers appear in code (must be in docs only)

### Workflow Touchpoints

- Security audit: `promote-control-v1.yml` → Check GitHub token in logs

- Token Vazio tracking: `WORKFLOW_RECEIPTS_VALIDATION_REPORT.md` documents 3 P1/P2 gaps

---

## Lane 08: **OBSERVABILITY & RELEASE**

**Branch**: `main_08_observabilidade_release`  
**Responsibility**: Metrics, regression detection, release decision

### Audit Artifacts

- `/data/audits/regression-log.jsonl` — Performance/correctness regressions

- `/data/audits/release-notes.md` — What changed and why

- `/data/audits/release-decision.json` — Approved for merge to main?

### Decision Gates
- **ENTRY**: Security-approved module from Lane 07
- **METRICS**: Performance within bounds? New tests faster than old?
- **REGRESSION**: No breakage of 106 existing tests? No performance drop >5%?
- **OBSERVABILITY**: Metrics/logs sufficient to debug if production issue arises?
- **RELEASE VOTE**: Is this ready to merge to main?

### Fail-Closed Rules

- ✓ Zero regression allowed (106/106 tests must pass)

- ✓ Performance degradation must be justified and logged

- ✓ Release notes required (documentation of all changes)

- ✗ Cannot release without explicit decision record

### Workflow Touchpoints

- Regression check: `promotion-control-v1.yml` → "Enforce manual promotion decision"

- Manual review required before merge

---

## Lane 09: **ARCHIVE & RETENTION**

**Branch**: `main_09_memoria_arquivo`  
**Responsibility**: Catalog, retention, restoration, historical checkpoints

### Audit Artifacts

- `/data/audits/archive-catalog.jsonl` — What was archived when

- `/data/audits/retention-schedule.jsonl` — When will items expire

- `/data/audits/restoration-checklist.jsonl` — Steps to restore from archive

### Decision Gates
- **ENTRY**: After merge to main (released version)
- **CATALOG**: Add to archive catalog with metadata
- **RETENTION**: Apply retention policy (keep N years? keep until policy changes?)
- **CHECKPOINT**: Create historical checkpoint if at major milestone
- **EXIT**: Archived and restorable

### Fail-Closed Rules

- ✓ Nothing is deleted without explicit retention policy decision (Lane 00)

- ✓ Archives must be encrypted and access-logged

- ✓ Restoration procedures must be tested annually

- ✗ Lost archives cannot be recovered; prevent data loss

### Workflow Touchpoints

- Automatic archival: `rafaelia-adaptive-cycle.yml` → Final step catalogs artifacts

- Historical index: `/data/audits/RAFAELIA_ADAPTIVE_CYCLE_LATEST4_*.v1.json`

---

## Full Workflow: Lanes 00-09 in Sequence

```text
USER REQUEST
    ↓
Lane 00 [GOVERNANCE]
  - Is this request in scope?
  - Which policy applies?
  - Who has authority?
    ↓ (policy decision)
Lane 01 [INTAKE]
  - Where did this come from?
  - Quarantine + custody
  - Trace provenance
    ↓ (source identified)
Lane 02 [NORMALIZATION]
  - Apply schema
  - Deduplicate
  - Standardize names
    ↓ (normalized object)
Lane 03 [SEMANTIC MODELING]
  - Build ontology position
  - Map relations
  - Create navigation paths
    ↓ (semantic model)
Lane 04 [VALIDATION]
  - Run tests (106/106 pass)
  - Check falsifiers
  - Lint & format
    ↓ (validated)
Lane 05 [EVIDENCE]
  - Emit artifact
  - Bind hash (SHA256)
  - Create receipt
    ↓ (artifact + receipt)
Lane 06 [INTEGRATION]
  - Check module contracts
  - Verify dependencies
  - Stage for review
    ↓ (staged module)
Lane 07 [SECURITY]
  - Scan threats
  - Audit privacy
  - Check compliance
  - Document TOKEN_VAZIO gaps
    ↓ (risk opinion)
Lane 08 [OBSERVABILITY]
  - Check regressions (0 allowed)
  - Verify metrics
  - Approve release?
    ↓ (release decision)
Lane 09 [ARCHIVE]
  - Catalog entry
  - Apply retention
  - Create checkpoint
    ↓
  MAIN BRANCH (permanent record)
```text

---

## Audit Trail Integration

Each lane writes to `/data/audits/` with append-only logs:

```text
/data/audits/
  ├── lane-00-governance-decisions.jsonl
  ├── lane-01-intake-sources.jsonl
  ├── lane-02-normalization-rules.jsonl
  ├── lane-03-semantic-relations.jsonl
  ├── lane-04-validation-results.jsonl
  ├── lane-05-artifacts-manifest.jsonl
  ├── lane-06-integration-staging.jsonl
  ├── lane-07-security-compliance.jsonl
  ├── lane-08-release-decisions.jsonl
  └── lane-09-archive-catalog.jsonl
```text

**Key principle**: No lane can see or modify a downstream lane's audit trail. Lanes are federated with shared governance (Lane 00) at the top.

---

## Critical Invariant: No Lane Skipping

**Fail-closed rule**: Every workflow item must pass all 10 lanes in order, or be explicitly rejected with a decision record.

- Skipping Lane 04 (validation) = automatic REJECT

- Bypassing Lane 07 (security) = automatic REJECT  

- No automatic merges (Lane 08 vote required)

- All rejections are auditable (reason + lane documented)

---

## References

- `/docs/governance/BRANCH_TOPOLOGY_MAIN_NUMBERED_V1.md` — Full lane definitions

- `/data/control-plane/promotion-control.v1.json` — Governance policy (invariants)

- `WORKFLOW_RECEIPTS_VALIDATION_REPORT.md` — Example: Lanes 04-09 in action (run 407)
