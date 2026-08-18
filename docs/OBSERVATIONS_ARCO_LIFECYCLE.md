# The 8 Observations Across the 7 Arcos: Data Identity Lifecycle

**Version**: 1.0  
**Date**: 2026-08-18  
**Source**: `/docs/INVARIANTES_NECESSIDADE_URGENCIA_GRUPAMENTOS.md` (I_dados vector)

---

## The 8 Fundamental Observations

All data identity (I_dados) must preserve these 8 attributes across every transformation:

```
I_dados = identidade ∧ proveniência ∧ contexto ∧ privacidade 
         ∧ estado_epistêmico ∧ dependências ∧ evidência ∧ próximo_passo
```

| # | Observation | Description |
|---|-------------|-------------|
| 1 | **identidade** | Unique, stable identifier (cycle_id, SHA256, UUID) |
| 2 | **proveniência** | Origin, history, custody chain (who created, when, from what) |
| 3 | **contexto** | Environment, time, conditions (timestamp, workflow run, phase) |
| 4 | **privacidade** | Access controls, sensitivity, LGPD/GDPR compliance |
| 5 | **estado_epistêmico** | Knowledge level: observed? tested? approved? (OBSERVED → CANONICAL_TOKEN_VALID) |
| 6 | **dependências** | Transitive closure of what this depends on |
| 7 | **evidência** | Supporting data, artifacts, receipts, hashes, signatures |
| 8 | **próximo_passo** | Action required; decision pending; routing target |

---

## 8 Observations Mapped to 7 Arcos

### Arco 1: **PSI** (ψ) — Prospection / Intention

**Module**: `raf_probe`  
**Question**: "What do we intend to observe?"

| Observation | Role in Psi | Example |
|---|---|---|
| **identidade** | Define what we're looking for (search target) | "Find all receipts with cycle_id matching RAF-CYCLE-*" |
| **próximo_passo** | Set prospection goal | "Verify claim_allowed=false in latest four" |
| **contexto** | Time boundary, environment | "Scope: current workflow run, time window: last 24h" |
| **dependências** | Prerequisite checks | "Requires Lane 01 source availability, Lane 05 evidence store" |
| **estado_epistêmico** | Baseline knowledge | "Starting with OBSERVED; need BUILD_VERIFIED before proceeding" |
| **privacidade** | Access policy | "Read receipts only, no modification" |
| **proveniência** | Who authorized this observation | "Authorized by Lane 00 governance policy" |
| **evidência** | What counts as proof | "Receipt signatures, hash chain, timestamp proofs" |

**Output**: Prospection plan with 8 observations defined

---

### Arco 2: **CHI** (χ) — Observation / Decoding

**Module**: `raf_decode`  
**Question**: "What do we actually observe?"

| Observation | Role in Chi | Example |
|---|---|---|
| **identidade** | Verify observed object identity matches target | "Receipt SHA256 hash matches expected value" |
| **evidência** | Collect raw observations, artifacts | "Read receipt JSON from `/data/receipts/`, capture all fields" |
| **contexto** | Record observation context | "Timestamp: 2026-08-17T04:55:31Z, Source run: 31996105693" |
| **proveniência** | Document observation chain | "Came from GitHub Actions artifact, stored by job 95287915344" |
| **privacidade** | Apply access filters | "Log sanitized, no raw token exposure" |
| **estado_epistêmico** | Elevate to OBSERVED | "Object observed in artifact, bytes captured" |
| **próximo_passo** | Plan next transformation | "Route to rho phase for noise measurement" |
| **dependências** | Track observation dependencies | "Depends on artifact store availability" |

**Output**: Observation record with all 8 fields populated, no gaps

---

### Arco 3: **RHO** (ρ) — Noise Measurement / Layout

**Module**: `raf_align`  
**Question**: "What noise or variation did we observe?"

| Observation | Role in Rho | Example |
|---|---|---|
| **evidência** | Identify noise factors | "GitHub runner clock skew: ±12ms, network jitter: ±5ms" |
| **estado_epistêmico** | Remain at OBSERVED; document uncertainty | "Noise measured but not corrected; uncertainty preserved" |
| **contexto** | Contextualize noise patterns | "Observed during peak runner load, 18 concurrent jobs" |
| **identidade** | Noise signature (optional) | "Noise pattern: RFC-5116-TIMING_VARIANCE" |
| **privacidade** | Protect noise data sensitivity | "Timing data not shared externally" |
| **proveniência** | Trace noise origin | "Came from GitHub runner infrastructure" |
| **próximo_passo** | Plan layout alignment | "Route to delta for ethical transmutation (apply noise bounds)" |
| **dependências** | Noise measurement tools availability | "Requires timing instrumentation in chi phase" |

**Output**: Noise report with quantified uncertainties; decision on whether to proceed

---

### Arco 4: **DELTA** (Δ) — Ethical Transmutation

**Module**: `raf_transform`  
**Question**: "What transformations are ethically safe?"

| Observation | Role in Delta | Example |
|---|---|---|
| **estado_epistêmico** | Verify gates before transformation | "Require BUILD_VERIFIED state before mutation" |
| **diprivacidade** | Apply privacy constraints during transform | "Redact sensitive fields before logging transformation" |
| **identidade** | Preserve identity through transformation | "Hash of input object must equal expected value; no object substitution" |
| **próximo_passo** | Document transformation intent | "Transform: add entry_sha256 field, preserve claim_allowed=false" |
| **evidência** | Capture transformation evidence | "Before/after hashes, transformation parameters" |
| **contexto** | Transformation environment | "Applied in isolated, sandboxed job environment" |
| **proveniência** | Authorization trail | "Transformation approved by Lane 04 validation gate" |
| **dependências** | Dependency gates | "Fail-closed if rho noise exceeds thresholds" |

**Output**: Transformation decision (APPROVED / REJECTED); immutable record

---

### Arco 5: **SIGMA** (Σ) — Coherent Memory / Composition

**Module**: `raf_emit`  
**Question**: "How do we compose transformed observations into coherent memory?"

| Observation | Role in Sigma | Example |
|---|---|---|
| **identidade** | Assign persistent identity to composition | "Assign cycle_id: RAF-CYCLE-20260817T045531Z-N25" |
| **evidência** | Emit hash-chained composition | "Build receipt with entry_sha256, link to previous_entry_sha256" |
| **proveniência** | Record composition history | "This cycle composed from 4 prior entries, each from distinct runs" |
| **contexto** | Embed composition context | "Composition timestamp, workflow run ID, job ID" |
| **estado_epistêmico** | Mark epistemic advancement | "Elevate to HASH_BOUND (hash verified), prepare for BUILD_VERIFIED" |
| **dependências** | Track composition dependencies | "Depends on 4 prior receipts; transitive closure: 12 total dependencies" |
| **privacidade** | Ensure composition privacy | "Receipt stored in private artifacts, access logs maintained" |
| **próximo_passo** | Plan verification | "Route to omega for verification gate" |

**Output**: Composed receipt (immutable, hash-chained)

---

### Arco 6: **OMEGA** (Ω) — Bounded Completion / Verification

**Module**: `raf_verify`  
**Question**: "Do we have sufficient proof the composition is complete and correct?"

| Observation | Role in Omega | Example |
|---|---|---|
| **evidência** | Verify all evidence present | "8 observations all present in receipt: ✓✓✓✓✓✓✓✓" |
| **estado_epistêmico** | Advance epistemic state | "HASH_BOUND → BUILD_VERIFIED (hash passed, schema passed)" |
| **identidade** | Confirm identity integrity | "cycle_id format valid, hash matches expected pattern" |
| **proveniência** | Verify provenance chain | "Source run ID matches GitHub API data" |
| **contexto** | Validate context consistency | "Timestamp monotonic, phase valid" |
| **privacidade** | Audit privacy compliance | "No unintended data exposure in receipt logs" |
| **dependências** | Verify dependency acyclicity | "No circular references; DAG property holds" |
| **próximo_passo** | Prepare routing decision | "Decision: VERIFIED_LATEST_FOUR_READ_ONLY → route to psi-prime" |

**Output**: Verification decision (VERIFIED / FAILED); epistemic state advance

---

### Arco 7: **PSI-PRIME** (ψ') — Routing & Retrospection

**Module**: `raf_route`  
**Question**: "What should we observe next?"

| Observation | Role in Psi-Prime | Example |
|---|---|---|
| **próximo_passo** | Define next-cycle prospection targets | "Lane 01: Monitor for injection attempts; Lane 04: Add falsifier; Lane 07: Audit license compatibility" |
| **estado_epistêmico** | Document final epistemic state | "Reached CANONICAL_TOKEN_VALID; preserve uncertainty for N+1 cycle" |
| **identidade** | Create retrospection record | "Cycle N25 complete; identity: RAF-CYCLE-20260817T045531Z-N25" |
| **proveniência** | Trace full custody chain | "Artifact → chi → rho → delta → sigma → omega → psi-prime" |
| **evidência** | Emit retrospection evidence | "Arco timeline, decision log, TOKEN_VAZIO preservation record" |
| **contexto** | Document cycle context | "Total duration: 847ms, 18 verification steps completed" |
| **dependências** | Route transitive dependencies | "Cycle N+1 depends on Lane 01-09 routed work queue" |
| **privacidade** | Protect retrospection data | "Logs sanitized; sensitive timing data remains private" |

**Output**: Routing decision with 8 observations intact; forward arrow to Cycle N+1

---

## Critical Principle: **No Observation Left Behind**

At every arco transition, verify all 8 observations are present:

```
psi → chi: identidade, proveniência, contexto, privacidade present? ✓
chi → rho: stato_epistêmico, dependências, evidência marked? ✓
rho → delta: próximo_passo documented? ✓
delta → sigma: All 8 carried forward or explicitly replaced? ✓
sigma → omega: identidade immutable? ✓
omega → psi-prime: stato_epistêmico advanced? ✓
psi-prime → [cycle N+1 psi]: Next prospection targets defined? ✓
```

**Fail-closed rule**: If any observation is missing or elided, the arco transition is REJECTED.

---

## Application Example: Run 407 Receipt

From WORKFLOW_RECEIPTS_VALIDATION_REPORT.md, Entry 4 (N25, chi phase):

```json
{
  "identidade": "RAF-CYCLE-20260817T045531Z-N25",
  "n_mod_42": 25,
  "phase": "chi",
  "decision": "EXECUTED_READ_ONLY",
  "entry_sha256": "be85d13aaf606d6ce67fdbccafcf65bb070ce5d171a146148940d478a64b2552",
  "latest_four_count": 4,
  "claim_allowed": false,
  
  "proveniência": {
    "source_run_id": 31996105693,
    "source_job_id": 95287915344,
    "creation_timestamp": "2026-08-17T04:55:31Z"
  },
  "contexto": {
    "phase": "chi",
    "workflow": "rafaelia-adaptive-cycle.yml"
  },
  "privacidade": {
    "access_level": "private_artifact",
    "exposure_risk": "low"
  },
  "estado_epistêmico": "HASH_BOUND",
  "dependências": [
    "RAF-CYCLE-20260817T040657Z-N22",
    "RAF-CYCLE-20260817T031016Z-N18",
    "RAF-CYCLE-20260817T020627Z-N14"
  ],
  "evidência": [
    {"type": "hash", "value": "be85d13aaf606d6ce67fdbccafcf65bb070ce5d171a146148940d478a64b2552"},
    {"type": "prior_hash", "value": "feb2cf5ae682cc43fa2f196415a7de9ea5e4533be1e231d25469c8454728dd62"}
  ],
  "próximo_passo": "VERIFY_OMEGA_GATE"
}
```

**Analysis**: All 8 observations present. Receipt passes arco transition gate.

---

## References

- `/docs/INVARIANTES_NECESSIDADE_URGENCIA_GRUPAMENTOS.md` — I_dados definition
- `/docs/architecture/RAFAELIA_7_ARCOS_RAFCONVERT_RAFDISK_V1.md` — Full arco descriptions
- `WORKFLOW_RECEIPTS_VALIDATION_REPORT.md` — Live receipt data examples
