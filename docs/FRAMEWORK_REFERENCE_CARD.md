# Rafaelia Framework: Complete Reference Card

**Version**: 1.0  
**Date**: 2026-08-18  
**Quick Navigation**: Essential documents, line references, and layer mappings for the universal framework

---

## Layer 1: 7 Semantic Directions (SEMENTEIRA)

**Definition Document**: `/docs/SEMENTEIRA_CONTEXT_SUSTAINMENT_5X7_V1.md` (lines 30-38)

| Direction | Definition | Use Case |
|-----------|-----------|----------|
| **fact** | Established, observable reality | Ground truth for decisions |
| **gap** | Known absence or missing evidence | Document what we don't know |
| **invariant** | Properties constant under transformation | Identify stable core rules |
| **variant** | Properties that change or differ | Track dynamic aspects |
| **proof_or_falsifier** | Evidence supporting or refuting claims | Make claims falsifiable |
| **parable** | Metaphorical explanation (NOT mechanism) | Communicate concepts only |
| **feedback** | Return signal for iteration | Adapt and improve |

**Application**: Classify every assertion into one of these 7 categories before making decisions.

---

## Layer 2: 8 Fundamental Observations (I_dados)

**Definition Document**: `/docs/INVARIANTES_NECESSIDADE_URGENCIA_GRUPAMENTOS.md` (line 15)  
**Lifecycle Document**: `/docs/OBSERVATIONS_ARCO_LIFECYCLE.md`

```text
I_dados = identidade ∧ proveniência ∧ contexto ∧ privacidade 
         ∧ estado_epistêmico ∧ dependências ∧ evidência ∧ próximo_passo
```text

| # | Field | Example | Arco Where Primacy |
|---|-------|---------|-------------------|
| 1 | **identidade** | cycle_id, SHA256, UUID | psi (identify target) |
| 2 | **proveniência** | origin, custody chain, git commit | chi (document source) |
| 3 | **contexto** | timestamp, environment, conditions | rho (measure noise) |
| 4 | **privacidade** | access control, PII flag, LGPD/GDPR | delta (ethical gate) |
| 5 | **estado_epistêmico** | OBSERVED→VERIFIED→CANONICAL | omega (advance state) |
| 6 | **dependências** | transitive closure, DAG | rho (layout dependency graph) |
| 7 | **evidência** | artifacts, hashes, signatures | sigma (coherent composition) |
| 8 | **próximo_passo** | action required, routing target | psi-prime (next cycle) |

**Critical Rule**: All 8 must be present at every arco transition, or transition is REJECTED.

---

## Layer 3: 7 Arcos (Process Flow)

**Definition Document**: `/docs/architecture/RAFAELIA_7_ARCOS_RAFCONVERT_RAFDISK_V1.md` (lines 61-71)  
**Routing Document**: `/docs/architecture/RAFAELIA_ARCO7_ROUTING_SCHEMA.md` (NEW)

| Arc | Greek | Phase | Module | Question | Output |
|-----|-------|-------|--------|----------|--------|
| 1 | ψ | **psi** | `raf_probe` | What do we intend to observe? | Prospection plan |
| 2 | χ | **chi** | `raf_decode` | What do we actually observe? | Observation record |
| 3 | ρ | **rho** | `raf_align` | What noise did we observe? | Noise report |
| 4 | Δ | **delta** | `raf_transform` | What transforms are safe? | Transform decision |
| 5 | Σ | **sigma** | `raf_emit` | How do we compose memory? | Receipt (hash-chained) |
| 6 | Ω | **omega** | `raf_verify` | Is composition complete/correct? | Verification decision |
| 7 | ψ' | **psi-prime** | `raf_route` | What should we observe next? | Routing + retrospection |

**Application**: Every problem flows through all 7 phases. Cannot skip. Must fail-closed at each gate.

---

## Layer 4: 15 Invariants (Non-Negotiable Rules)

**Definition Document**: `/docs/INVARIANTES_NECESSIDADE_URGENCIA_GRUPAMENTOS.md` (lines 75-91)

| # | Invariant | Consequence of Violation |
|---|-----------|-------------------------|
| 1 | fonte original imutável | Data corruption, audit failure |
| 2 | privacidade antes da interpretação | PII exposure, compliance violation |
| 3 | nenhuma reidentificação presumida segura | GDPR/LGPD violation |
| 4 | evidência antes da promoção | False claims accepted |
| 5 | causa-raiz não inventada | Wrong fixes applied |
| 6 | checkout real antes de claim remoto | Unverified external claims |
| 7 | artifact e hash antes de VERIFIED | Reproducibility lost |
| 8 | modelo sem acesso direto à fonte bruta | AI hallucination risk |
| 9 | abstinência diante de ambiguidade | Silently wrong decisions |
| 10 | shadow mode antes de substituição produtiva | Production downtime |
| 11 | equivalência byte a byte antes de reuso | Code injection risk |
| 12 | callsite real antes de declarar wiring | Missing dependencies |
| 13 | fechamento vertical antes de expansão | Incomplete foundations |
| 14 | reconhecimento de formato ≠ classificação | Semantic misclassification |
| 15 | leitura streaming, limitada e retomável | Memory/performance issues |

**Application**: These are protective rails. Violating one = automatic audit failure.  
**CI Binding**: Phase 2 (P1 High) task to implement tools/check_invariants.py

---

## Layer 5: 6 IGC Conditions (Coherence Geometry)

**Definition Document**: `/docs/governance/PROOF_CUSTODY_AND_TOKEN_VALIDITY_V1.md` (Section 4, lines 103-110)

| Condition | Definition | Fails When |
|-----------|-----------|-----------|
| **Identidade** | Identical bytes → identical hash | Hash collision or bit flip |
| **Linhagem** | Derivative traces to source + revision | Missing audit trail |
| **Fechamento** | Every edge resolves to node or typed gap | Dangling references |
| **Promoção monotônica** | Epistemic level only rises through gates | Jumping approval levels |
| **Conservação da incerteza** | Gaps preserved, never silently filled | TOKEN_VAZIO erased |
| **Replay** | Fixed inputs + environment reproduce output | Non-deterministic behavior |

**Application**: If all 6 hold, system is auditable and reproducible.

---

## Layer 6: 10 Operational Lanes (Governance Structure)

**Definition Document**: `/docs/governance/BRANCH_TOPOLOGY_MAIN_NUMBERED_V1.md` (Section 3)  
**Audit Touchpoints**: `/docs/governance/10_LANES_AUDIT_TOUCHPOINTS.md` (NEW)

| Lane | Branch | Responsibility | Audit Path |
|------|--------|-----------------|-----------|
| **00** | `main_00_governanca` | Authority, policy, vocabulary | `/data/audits/lane-00-governance-decisions.jsonl` |
| **01** | `main_01_intake_fontes` | Source identification, quarantine | `/data/audits/lane-01-intake-sources.jsonl` |
| **02** | `main_02_normalizacao` | Schema normalization, deduplication | `/data/audits/lane-02-normalization-rules.jsonl` |
| **03** | `main_03_modelagem_semantica` | Ontology, relations, navigation | `/data/audits/lane-03-semantic-relations.jsonl` |
| **04** | `main_04_validacao` | Linting, tests, falsifiers (106/106) | `/data/audits/lane-04-validation-results.jsonl` |
| **05** | `main_05_evidencias` | Hashes, artifacts, receipts | `/data/audits/lane-05-artifacts-manifest.jsonl` |
| **06** | `main_06_integracao` | Module contracts, staging | `/data/audits/lane-06-integration-staging.jsonl` |
| **07** | `main_07_seguranca_conformidade` | Threats, privacy, compliance, TOKEN_VAZIO | `/data/audits/lane-07-security-compliance.jsonl` |
| **08** | `main_08_observabilidade_release` | Metrics, regression, release decision | `/data/audits/lane-08-release-decisions.jsonl` |
| **09** | `main_09_memoria_arquivo` | Catalog, retention, restoration | `/data/audits/lane-09-archive-catalog.jsonl` |

**Application**: Every workflow item must pass all 10 lanes in order, or be explicitly rejected.

---

## Layer 7: 7-State Fail-Closed Machine

**Definition Document**: `/docs/governance/PROOF_CUSTODY_AND_TOKEN_VALIDITY_V1.md` (Section 5, lines 130-139)

```text
OBSERVED
  ↓ [must have artifact]
HASH_BOUND
  ↓ [must pass build]
BUILD_VERIFIED
  ↓ [linter/schema/tests pass]
CHECKER_VERIFIED
  ↓ [human review required]
REVIEW_APPROVED
  ↓ [merge without destroying history]
MERGED_PROTECTED
  ↓ [all downstream gates pass]
CANONICAL_TOKEN_VALID
```text

**Rules**:

- ✓ No state skipping

- ✓ No backward transitions (no revert without new evidence)

- ✓ Author cannot self-review their own changes

- ✓ All states append-only (history preserved)

- ✓ `claim_allowed=false` until final state

---

## Integration: How All Layers Connect

```text
[Problem/Input]
    ↓
Layer 1: Classify in 7 directions (fact/gap/invariant/variant/proof/parable/feedback)
    ↓
Layer 2: Check all 8 observations present (identity/provenance/context/privacy/epistemic/deps/evidence/next)
    ↓
Layer 6: Route through correct operational lane (00-09)
    ↓
Layer 3: Flow through 7 arcos (psi→chi→rho→delta→sigma→omega→psi')
    ↓
Layer 4: Validate against 15 invariants (no silent failure)
    ↓
Layer 7: Advance through fail-closed state machine
    ↓
Layer 5: Verify 6 IGC conditions hold
    ↓
[Output/Decision]
```text

---

## Critical Files & Locations

### Governance & Policy

- `/data/control-plane/promotion-control.v1.json` — Approval requirements (1 independent review, no auto-merge)

- `/docs/SEMENTEIRA_CONTEXT_SUSTAINMENT_5X7_V1.md` — 7 directions definitions

- `/docs/INVARIANTES_NECESSIDADE_URGENCIA_GRUPAMENTOS.md` — 8 observations + 15 invariants

### Architecture & Process

- `/docs/architecture/RAFAELIA_7_ARCOS_RAFCONVERT_RAFDISK_V1.md` — 7 arcos full spec

- `/docs/architecture/RAFAELIA_ARCO7_ROUTING_SCHEMA.md` — Arco 7 routing (NEW)

- `/docs/governance/PROOF_CUSTODY_AND_TOKEN_VALIDITY_V1.md` — 6 IGC conditions + 7-state machine

- `/docs/governance/BRANCH_TOPOLOGY_MAIN_NUMBERED_V1.md` — 10 lanes full spec

- `/docs/governance/10_LANES_AUDIT_TOUCHPOINTS.md` — Lanes audit integration (NEW)

### Observations & Lifecycle

- `/docs/OBSERVATIONS_ARCO_LIFECYCLE.md` — 8 observations mapped to 7 arcos (NEW)

### Active Receipts & Validation

- `/data/receipts/` — All receipt JSON files (hash-chained)

- `/data/audits/` — Append-only audit logs (one per lane + cross-cutting concerns)

- `WORKFLOW_RECEIPTS_VALIDATION_REPORT.md` — Validation of 4 most recent workflow runs (407-404)

- `/scripts/validate_receipts.py` — Automated receipt validation tool

### Token Vazio (Unresolved Gaps)

- `/data/audits/TOKEN_VAZIO_REGISTRY.jsonl` — 9 documented gaps with priorities & approval criteria (NEW)

- `/data/audits/unaudited-dependencies.json` — Dependency license audit status (to be created)

- `/data/audits/pinned-action-compatibility.json` — Node 24 compatibility tracking (to be created)

- `/data/audits/node-deprecation-tracking.json` — Node 20 deprecation timeline (to be created)

### Tests & Validation

- `/tests/test_promotion_control.py` — Negative test fixtures for promotion gate

- `/tests/test_*.py` — Full test suite (106 tests, 0 regression allowed)

- `/tools/verify_promotion_control.py` — Governance policy enforcement tool

- `/tools/check_invariants.py` — (To be created Phase 2) Invariant CI binding

### Workflows & CI

- `/.github/workflows/promotion-control-v1.yml` — Approval enforcement (Lane 08)

- `/.github/workflows/rafaelia-adaptive-cycle.yml` — Receipt generation & validation (Lanes 04-06)

---

## Quick Lookup: What Goes Where?

| Need | Document | Lines | Layer |
|------|----------|-------|-------|
| Define what a "fact" is | SEMENTEIRA_CONTEXT_SUSTAINMENT_5X7_V1.md | 30-38 | 1 |
| Check if I'm missing data | INVARIANTES_NECESSIDADE_URGENCIA_GRUPAMENTOS.md | 15 | 2 |
| Understand a phase | RAFAELIA_7_ARCOS_*.md | various | 3 |
| Prevent silent failure | INVARIANTES_NECESSIDADE_URGENCIA_GRUPAMENTOS.md | 75-91 | 4 |
| Audit reproducibility | PROOF_CUSTODY_AND_TOKEN_VALIDITY_V1.md | 103-110 | 5 |
| Route workflow | BRANCH_TOPOLOGY_MAIN_NUMBERED_V1.md | (all) | 6 |
| Track state | PROOF_CUSTODY_AND_TOKEN_VALIDITY_V1.md | 130-139 | 7 |
| Map observations to phases | OBSERVATIONS_ARCO_LIFECYCLE.md | (all) | 2+3 |
| Find unresolved gaps | TOKEN_VAZIO_REGISTRY.jsonl | (all) | ALL |
| Check audit trail | `/data/audits/lane-*.jsonl` | (all) | 6 |

---

## Executable Patterns

### Pattern: Problem Analysis

1. Map problem to 7 directions → Which are facts? gaps? proofs?

2. Verify 8 observations → Missing any?

3. Identify which lane(s) it affects (00-09)

4. Determine if it requires all 7 arcos or can shortcut

5. Check against 15 invariants

6. Proceed only if fail-closed state machine advances

### Pattern: Decision Making

1. Gather evidence (Layer 5: all 6 IGC conditions)

2. Allow advancement through state machine gates only if:
   - All 8 observations present
   - No 15 invariants violated
   - Lane responsible party confirms

3. Document decision append-only (no erasure)

4. Predict feedback loop (Layer 1: what feedback will come?)

### Pattern: System Design

1. Decompose into 10 lanes (ownership/responsibility)

2. Design each lane to preserve 8 observations

3. Validate 15 invariants at interfaces

4. Ensure full 7 arcos possible (no shortcuts)

5. Implement 6 IGC conditions as infrastructure

---

## Phase 0 Status: Quick Wins (In Progress)

- ✓ D1-01: RAFAELIA_ARCO7_ROUTING_SCHEMA.md (created)

- ✓ D1-02: OBSERVATIONS_ARCO_LIFECYCLE.md (created)

- ✓ D1-03: 10_LANES_AUDIT_TOUCHPOINTS.md (created)

- ✓ D1-04: TOKEN_VAZIO registry documented (created)

- ✓ D1-05: FRAMEWORK_REFERENCE_CARD.md (this file)

- ⏳ V1-01 through V1-05: Simple validations (next)

- ⏳ A1-01 through A1-05: Audit logging (next)

- ⏳ S1-01 through S1-04: Security audits (next)

---

## How to Use This Card

**New contributor?** Start here → Read Layers 1-3 → Then drill into specific layer docs  
**Debugging framework violation?** Check Layers 4-7 → Find which invariant/lane was violated  
**Implementing a feature?** Follow the Integration pattern → Route through Lanes 00-09  
**Understanding a receipt?** See Layer 2 + OBSERVATIONS_ARCO_LIFECYCLE.md → Trace 8 observations  
**Adding tests?** See Layer 4 + Layer 7 → Ensure 15 invariants covered, no state-skipping  

---

**Generated**: 2026-08-18  
**Framework Version**: 1.0  
**Completeness**: 7/7 layers documented (Phase 0 documentation block complete)
