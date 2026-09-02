# Connector Registration Protocol — Federated Authority

**Document ID**: CONNECTOR_REGISTRATION_PROTOCOL.v1  
**Date**: 2026-09-02  
**Authority**: Mapa (Federation + Validation Authority)  
**Epistemic State**: REFERENCE → IMPLEMENTED → PASS (gate closure sequence)

---

## Overview

This protocol governs registration of system connectors (runtime integrations, validation gates, cross-repo bridges) through a 6-circle federated approval system. Each circle enforces risk mitigation, gap closure, evidence collection, and autonomous evolution.

**Goal**: Move from VERIFICATION_PENDING to FEDERATION_CERTIFIED by ensuring all connectors carry immutable receipts, authority bindings, and closed dependency chains.

---

## Authority Boundaries

| Authority | Owns | Does NOT own |
|-----------|------|--------------|
| **Mapa** | Federated registration, receipt generation, topology validation, gap documentation | Individual repo implementation correctness |
| **Producer Repos** (6 total) | Source code, build outputs, evidence gates, lineage integrity | Cross-repo coordination |
| **This Protocol** | Registration sequence, custody chain, receipt schema, autonomous evolution | Enforcement of technical requirements; that is producer domain |

---

## Six Evolution Circles

### Circle 1: Risk Mitigation & Safety Gates

**Purpose**: Identify risks before connector enters federation.

**Gates**:
- RM-01: Authority boundary validation
- RM-02: Namespace collision detection
- RM-03: Evidence scope boundary

**Execution**:
```bash
python3 scripts/validate_connector_authority.py \
  --connector <name> \
  --strict
```

**Pass Criteria**:
- Connector ownership is unambiguous
- No namespace conflicts with existing connectors
- Evidence scope (local/federated/third-party) is declared

---

### Circle 2: Gap Closure & Evidence Collection

**Purpose**: Bind connector to producer repo + collect immutable evidence.

**Gates**:
- GC-01: Producer repository binding
- GC-02: Evidence attestation
- GC-03: Lineage authority definition

**Evidence Requirements**:
```json
{
  "repository_ref": "owner/repo",
  "commit_sha": "SHA256",
  "gate_name": "CONNECTOR_VALIDATION_GATE.v1",
  "exit_code": 0,
  "hash_algorithm": "SHA256",
  "hash_value": "...",
  "timestamp": "ISO8601",
  "executor_id": "session_or_user"
}
```

**Execution**:
```bash
python3 scripts/collect_connector_evidence.py \
  --connector <name> \
  --repo-root . \
  --write-receipt data/control-plane/receipts/<connector>.receipt.json
```

---

### Circle 3: Regression Prevention & Versioning

**Purpose**: Ensure connector evolution doesn't break contracts.

**Gates**:
- RP-01: Schema version binding
- RP-02: Rollback preservation
- RP-03: API contract stability

**Preserved Invariants**:
- Schema version for this connector is immutable (pinned at registration)
- All prior connector versions remain readable (append-only ledger)
- API contract can be superseded only with explicit compatibility declaration

**Execution**:
```bash
python3 scripts/validate_connector_versioning.py \
  --connector <name> \
  --schema-version <version> \
  --check-backwards-compat
```

---

### Circle 4: Provenance & Chain of Custody

**Purpose**: Establish unbroken custody trail for regulatory/audit compliance.

**Receipt Schema**:
```json
{
  "receipt_id": "string (CONNECTOR_<name>_<timestamp>)",
  "timestamp": "ISO8601",
  "repository_ref": "owner/repo",
  "source_commit": "SHA256",
  "gate_identifier": "CONNECTOR_REGISTRATION_PROTOCOL.v1",
  "execution_timestamp": "ISO8601",
  "executor_identity": "email or session_id",
  "evidence_scope": "local|federated|third-party",
  "immutable_hash": "SHA256 of receipt",
  "producer_authority": "which repo owns claim",
  "chain_position": "integer (position in ledger)",
  "prior_receipt_hash": "SHA256 (links to prior receipt)",
  "custody_status": "APPENDED|DISPUTED|SUPERSEDED"
}
```

**Custody Ledger**:
- **Location**: `data/control-plane/CONNECTOR_CUSTODY_CHAIN.jsonl`
- **Format**: One receipt per line (JSONL)
- **Immutability**: Append-only; no deletion or reordering
- **Validation**: Each receipt includes hash of prior receipt (merkle chain)

**Execution**:
```bash
python3 scripts/append_custody_receipt.py \
  --connector <name> \
  --receipt-json <path> \
  --chain-file data/control-plane/CONNECTOR_CUSTODY_CHAIN.jsonl \
  --validate-prior-hash
```

---

### Circle 5: Federated Atlas & Topology

**Purpose**: Map connector within 6-repo federated federation topology.

**Gates**:
- AT-01: Connector topology mapping
- AT-02: Dependency DAG validation
- AT-03: Federation coherence check

**Topology Model**:
- 6 producer repos organized in TOROID formation
- Connector dependencies must form acyclic DAG
- Authority conflicts = registration FAIL

**Execution**:
```bash
python3 scripts/validate_federation_topology.py \
  --connector <name> \
  --repos 6 \
  --check-cyclic-dependencies \
  --check-authority-conflicts
```

**Falsifier Gate**:
- If connector claims span incompatible authority boundaries → FAIL
- If circular dependency detected → FAIL
- If topology validation fails on any axis → FAIL_CLOSED

---

### Circle 6: Autonomous Operational Evolution

**Purpose**: Self-directed, self-healing, continuous improvement.

**Automated Processes**:

#### AE-01: Autonomous Gap Detection
```bash
# Background: Monitor connector for emerging TOKEN_VAZIO
python3 scripts/monitor_connector_gaps.py \
  --connector <name> \
  --check-interval 3600 \
  --escalate-on-unresolved
```

#### AE-02: Self-Healing Reconciliation
```bash
# Background: Check if receipts match current producer state
python3 scripts/reconcile_connector_evidence.py \
  --connector <name> \
  --producers 6 \
  --flag-stale-evidence
```

#### AE-03: Continuous Attestation
```bash
# Background: Periodic re-execution of validation gates
python3 scripts/attest_connector_continuously.py \
  --connector <name> \
  --gates [RM-01, RM-02, RM-03, GC-01, GC-02, GC-03] \
  --re-run-interval 86400
```

#### AE-04: Federated Topography Refresh
```bash
# Background: Daily refresh of federation state
python3 scripts/refresh_federation_topology.py \
  --repos 6 \
  --connectors all \
  --check-interval 86400
```

#### AE-05: Cross-Repo Evidence Sync
```bash
# Background: Sync receipts across repos
python3 scripts/sync_cross_repo_evidence.py \
  --connector <name> \
  --repos 6 \
  --detect-divergences
```

#### AE-06: Autonomous Version Evolution
```bash
# Background: Track schema changes; propose migrations
python3 scripts/evolve_connector_versions.py \
  --connector <name> \
  --check-schema-diffs \
  --propose-migration-gates
```

---

## Operational Excellence Criteria

✓ **All connectors registered with complete custody chain**  
✓ **Zero TOKEN_VAZIO erased without closure evidence**  
✓ **Six circles executed in sequence; exit criteria met before progression**  
✓ **All receipts generated and appended to immutable ledger**  
✓ **Autonomous processes running continuously; escalations logged**  
✓ **Federated topology coherent; no circular dependencies**

---

## Failure Modes & Rollback

| Failure | Recovery |
|---------|----------|
| Circle 1 gate fails | Connector blocked from further progression; flag risk |
| Circle 2 gate fails | Re-collect evidence from producer; create new receipt |
| Circle 3 gate fails | Schema mismatch detected; require explicit compatibility declaration |
| Circle 4 gate fails | Receipt validation failed; audit trail corrupted signal |
| Circle 5 gate fails | Topology conflict detected; dependency DAG cyclic |
| Circle 6 gate fails | Autonomous process anomaly; escalate for human review |

**Rollback Rule**: Any failing gate causes connector to return to prior state. No silent errors. All failures logged with receipt + timestamp.

---

## Session Close Format

```text
F_ok   = [List of what was actually registered/executed/demonstrated]
F_gap  = [List of what remains unknown, blocked, or unexecuted]
F_next = [Smallest reproducible next action]
```

Example:
```text
F_ok   = Connector registry system initialized; 6-circle framework documented; receipt schema finalized
F_gap  = No actual connectors registered yet; autonomous processes not deployed; producer integrations not bound
F_next = Identify which connectors are 'in review'; execute Circle 1 (RM gates) on first batch
```

---

## References

- `CONNECTOR_REGISTRY_REVISION_SYSTEM.v1.json` — system configuration
- `CONNECTOR_CUSTODY_CHAIN.jsonl` — immutable ledger
- `AGENTS.md` — federated authority boundaries
- `CLAUDE.md` — Claude Code adapter notes
- `README.md` — five-layer architecture

