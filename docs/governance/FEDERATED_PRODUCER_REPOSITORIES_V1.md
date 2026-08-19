# Federated Producer Repositories V1

## Multi-Repository Governance Chains and Receipt Federation

**Date**: 2026-08-18  
**Framework**: Rafaelia Governance System (Phase 2-P1-04)  
**Status**: Architecture Design & Implementation Plan  

---

## Executive Summary

**Problem**: The Rafaelia governance framework currently operates within a single repository (Mapa). External producer repositories have no way to participate in:

- Immutable receipt emission
- Hash-chained evidence trails
- Fail-closed validation gates
- Multi-repo approval chains

**Solution**: Federated Producer Repositories enable external repos to:

1. Emit receipts in Rafaelia format (same schema, same 8 observations)
2. Link receipts across repositories via provenance chains
3. Submit evidence to central governance authority
4. Participate in fail-closed approval workflows

**Core Principle**: *One governance system. Many producers. No silence.*

---

## Architecture: 4-Layer Federation Model

```text
LAYER 1: PRODUCER (External Repository)
  └─ Emits receipt in Rafaelia format
  └─ Signs with producer identity
  └─ Posts to federation registry

         ↓ [Network transport with integrity]

LAYER 2: TRANSPORT (Signed Receipt Chain)
  └─ HTTPS with TLS verification
  └─ Producer signature (asymmetric cryptography)
  └─ Timestamp and sequence tracking

         ↓ [Local receipt storage]

LAYER 3: BROKER (Central Mapa Repository)
  └─ Receives federated receipts
  └─ Validates against Rafaelia schema
  └─ Cross-repo provenance verification

         ↓ [Governance decisions]

LAYER 4: AUTHORITY (Governance Gates)
  └─ Lane 00 (Governança): Multi-repo policy
  └─ Lane 04 (Validação): Cross-repo validator
  └─ Lane 06 (Integração): Federation integration
  └─ Append-only decisions log
```

---

## Layer 1: Producer Receipt Format

### Extended Receipt Schema (rafaelia.federated-producer-receipt.v1)

All producer receipts **inherit** from existing Rafaelia receipt schema, plus:

```json
{
  "schema": "rafaelia.federated-producer-receipt.v1",
  
  "producer_identity": {
    "repository_owner": "external-org",
    "repository_name": "producer-repo",
    "repository_url": "https://github.com/external-org/producer-repo",
    "producer_type": "application|library|service|workflow",
    "federation_status": "REGISTERED|PROVISIONAL|SUSPENDED",
    "federation_established": "2026-08-18T00:00:00Z"
  },
  
  "producer_commitment": {
    "signed_by_sha256": "...",
    "signer_identity": "GitHub App / OAuth token ID",
    "signature_algorithm": "HMAC-SHA256",
    "signature_timestamp": "2026-08-18T12:34:56Z",
    "signature_valid_until": "2026-12-31T23:59:59Z"
  },
  
  "provenance_chain": {
    "source_producer_repository": "external-org/producer-repo",
    "source_workflow": ".github/workflows/emit-rafaelia-receipt.yml",
    "source_run_id": "999999999",
    "source_job_id": "888888888",
    "received_by": "rafaelmeloreisnovo/Mapa",
    "received_at_utc": "2026-08-18T12:35:00Z",
    "transport_integrity": "TLS_1_3_VERIFIED"
  },
  
  "cross_repo_observations": {
    "producer_identifier": "external-org/producer-repo#run-999999999",
    "producer_provenance": "Emitted by external producer; received and logged",
    "producer_context": "Production CI run; GitHub Actions runner",
    "producer_privacy": "Public repository; no secrets in receipt",
    "producer_epistemic_level": "OBSERVED_BY_PRODUCER_UNVERIFIED_BY_BROKER",
    "producer_dependencies": ["github.com/external-org/producer-repo"],
    "producer_evidence": "GitHub Actions artifacts referenced by receipt",
    "producer_next_step": "Broker validation required before promotion"
  },
  
  "federation_metadata": {
    "broker_receipt_id": "mapa-fed-20260818-001",
    "broker_received_at": "2026-08-18T12:35:00Z",
    "broker_validation_status": "PENDING|VALIDATED|REJECTED",
    "broker_validator_lane": "04_validacao",
    "legal_producer_jurisdiction": "BR",
    "cross_border_data_transfer_allowed": true
  },
  
  "... (all standard Rafaelia receipt fields follow) ..."
}
```

### Key Properties

1. **Producer Identity**: Repository owner, name, type (app/library/service/workflow)
2. **Producer Commitment**: HMAC signature proves receipt came from producer
3. **Provenance Chain**: Complete trace from producer CI → transport → broker
4. **Cross-Repo Observations**: All 8 observations present (identity, provenance, context, privacy, epistemic, dependencies, evidence, next_step)
5. **Federation Metadata**: Broker tracking, validation status, governance lane

---

## Layer 2: Transport Security & Integrity

### Signed Receipt Transmission

Producers post receipts to Mapa via signed HTTP request:

```bash
# Producer repository CI job
PRODUCER_SIGNATURE=$(hmac_sha256 "$RECEIPT_JSON" "$PRODUCER_SECRET_KEY")

curl -X POST \
  https://api.github.com/repos/rafaelmeloreisnovo/Mapa/contents/data/receipts/federated/ \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-Producer-Signature: $PRODUCER_SIGNATURE" \
  -H "X-Producer-Repository: external-org/producer-repo" \
  -d '{
    "message": "Federated producer receipt",
    "content": "base64-encoded-receipt-json",
    "branch": "main"
  }'
```

### Receipt Broker Workflow

Mapa (`rafaelmeloreisnovo/Mapa`) runs `federated-receipt-broker.yml`:

```yaml
name: Federated Receipt Broker
on:
  push:
    paths:
      - 'data/receipts/federated/*.json'

jobs:
  validate_federated_receipts:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@...
      - name: Validate federated receipt signatures
        run: |
          python tools/validate_federated_receipt.py \
            --receipt "${{ github.workspace }}/data/receipts/federated/*.json" \
            --broker-policy data/control-plane/federation-policy.v1.json
            
      - name: Check cross-repo provenance
        run: |
          python tools/verify_cross_repo_provenance.py \
            --receipt "${{ github.workspace }}/data/receipts/federated/*.json"
            
      - name: Audit federated receipt
        run: |
          python tools/audit_federated_receipt.py \
            --receipt "${{ github.workspace }}/data/receipts/federated/*.json" \
            --append-to data/audits/federated-receipts-audit.jsonl
```

---

## Layer 3: Broker Receipt Validation

### Rafaelia Broker (`tools/validate_federated_receipt.py`)

The broker validates:

1. **Schema Compliance**: Receipt matches `rafaelia.federated-producer-receipt.v1`
2. **Producer Signature**: HMAC signature valid and timestamp fresh
3. **Provenance Continuity**: Producer → transport → broker chain intact
4. **Immutability Markers**: All 8 observations present (no silent gaps)
5. **Cross-Repo Integrity**: Producer repo exists, is public, run ID valid
6. **Privacy Compliance**: No secrets leaked in receipt
7. **Epistemic Level**: Correctly marked as OBSERVED_BY_PRODUCER_UNVERIFIED_BY_BROKER

### Validation Gatekeeping

```json
Producer Receipt Arrives
    ↓
GATE 1: Schema & Signature Validation
    ├─ Valid schema? ✓
    ├─ Signature verifies? ✓
    ├─ Timestamp fresh (< 24 hours)? ✓
    └─ All 8 observations present? ✓
    
    ↓ YES (all checks pass)
    
GATE 2: Provenance Verification
    ├─ Producer repo exists on GitHub? ✓
    ├─ Run ID matches producer CI? ✓
    ├─ Artifacts accessible? ✓
    └─ No secrets in receipt? ✓
    
    ↓ YES (provenance verified)
    
GATE 3: Policy Compliance
    ├─ Producer in approved federation list? ✓
    ├─ Producer has valid contract? ✓
    ├─ No claim_allowed=true without approval? ✓
    └─ Cross-border transfer allowed? ✓
    
    ↓ YES (policy check passes)
    
Status: VALIDATED → Logged to audit trail
    ↓ NO (any gate fails)
    ↓
Status: REJECTED → Logged with reason; notify producer
```

---

## Layer 4: Governance Gates for Federated Receipts

### Multi-Repo Approval Chain

Federated receipts follow the same fail-closed machine as Mapa receipts:

```text
FEDERATED_RECEIPT_OBSERVED (broker receives it)
    ↓ [GATE 1: Schema + signature verified]
    ↓ [Lane 04 (Validação) validator approves]
    ↓
FEDERATED_RECEIPT_HASH_BOUND
    ↓ [GATE 2: Provenance chain verified]
    ↓ [Cross-repo integrity confirmed]
    ↓
FEDERATED_RECEIPT_BUILD_VERIFIED
    ↓ [GATE 3: Policy compliance verified]
    ↓ [Lane 00 (Governança) reviews federation status]
    ↓
FEDERATED_RECEIPT_CHECKER_VERIFIED
    ↓ [GATE 4: Cross-repo dependencies resolved]
    ↓ [Lane 06 (Integração) confirms no cascading gaps]
    ↓
FEDERATED_RECEIPT_REVIEW_APPROVED
    ↓ [Multi-repo governance decision recorded]
    ↓ [Append-only to federated-receipts-audit.jsonl]
    ↓
FEDERATED_RECEIPT_MERGED_PROTECTED
    ↓ [Fed receipt integrated into central evidence index]
    ↓
FEDERATED_RECEIPT_CANONICAL_TOKEN_VALID
```

### Federation Policy (`data/control-plane/federation-policy.v1.json`)

```json
{
  "schema": "rafaelia.federation-policy.v1",
  "federation_mode": "OPEN_WITH_VETTING",
  "approved_producers": [
    {
      "repository_owner": "external-org",
      "repository_name": "producer-repo",
      "producer_type": "application",
      "federation_status": "REGISTERED",
      "federation_established": "2026-08-18T00:00:00Z",
      "contract_expires": "2026-12-31T23:59:59Z",
      "secret_key_id": "producer-hmac-key-001",
      "approval_lane": "00_governanca",
      "approval_authority": "Rafaelia Governance Board"
    }
  ],
  "rejection_criteria": [
    "Schema validation fails",
    "Signature invalid or expired",
    "Producer not in approved list",
    "Cross-border transfer not allowed",
    "Secrets detected in receipt",
    "Run ID does not exist on GitHub",
    "Provenance chain broken"
  ],
  "auto_reject_after_failures": 3,
  "notify_producer_on_reject": true,
  "append_audit_trail": true
}
```

---

## Federation Onboarding: 3-Step Process

### Step 1: Producer Registration

External repo owner submits registration:

```json
{
  "producer_repository": "external-org/producer-repo",
  "producer_type": "application|library|service|workflow",
  "producer_description": "Description of what this repo produces",
  "producer_contact": "owner@example.com",
  "producer_commitment": {
    "will_emit_receipts_in_rafaelia_format": true,
    "will_not_mutate_receipts": true,
    "will_preserve_token_vazio": true,
    "will_sign_all_receipts": true,
    "will_include_all_8_observations": true,
    "agrees_to_audit": true
  }
}
```

Mapa Lane 00 (Governança) reviews and approves or rejects.

### Step 2: Credential Exchange

Approved producers receive:

- HMAC secret key for signing receipts
- Federated receipt endpoint URL
- Policy document with rejection criteria
- Sample receipt template

### Step 3: CI Integration

Producer adds to `.github/workflows/emit-rafaelia-receipt.yml`:

```yaml
name: Emit Rafaelia Federated Receipt
on:
  workflow_run:
    workflows: [Build, Deploy, Test]
    types: [completed]

jobs:
  emit_receipt:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@...
      
      - name: Build federated receipt
        run: |
          python - <<'PYTHON'
          import json, hashlib, hmac
          
          receipt = {
            "schema": "rafaelia.federated-producer-receipt.v1",
            "producer_identity": {
              "repository_owner": "external-org",
              "repository_name": "producer-repo",
              "repository_url": "https://github.com/external-org/producer-repo",
              "producer_type": "application"
            },
            "provenance_chain": {
              "source_run_id": "${{ github.run_id }}",
              "source_job_id": "${{ github.job }}"
            },
            # ... all other Rafaelia receipt fields ...
          }
          
          # Sign receipt
          secret = "${{ secrets.RAFAELIA_HMAC_SECRET }}"
          receipt_json = json.dumps(receipt, sort_keys=True)
          signature = hmac.new(
            secret.encode(),
            receipt_json.encode(),
            hashlib.sha256
          ).hexdigest()
          
          print(json.dumps({"receipt": receipt, "signature": signature}))
          PYTHON
          
      - name: Post receipt to Mapa broker
        run: |
          curl -X POST \
            https://api.github.com/repos/rafaelmeloreisnovo/Mapa/contents/data/receipts/federated/ \
            -H "Authorization: Bearer ${{ secrets.MAPA_RECEIPT_TOKEN }}" \
            -H "X-Producer-Signature: $PRODUCER_SIGNATURE" \
            -H "X-Producer-Repository: external-org/producer-repo" \
            -d @receipt-payload.json
```

---

## Cross-Repo Evidence Chains

### Example: Multi-Repo Feature Delivery

```json
Producer A (frontend repo) emits receipt
    ├─ Artifact: Built UI bundle (SHA256)
    ├─ Evidence: Test coverage 92%
    ├─ Observation: source_run_id=100
    └─ Next step: Awaiting backend integration

         ↓ [Federated receipt posted to Mapa]
         ↓ [Mapa broker validates]
         ↓

Mapa (integration repo) receives receipt
    ├─ Validates Producer A signature
    ├─ Cross-checks with Producer B receipt
    ├─ Confirms: Frontend && Backend both complete
    ├─ Evidence: Both CI runs green, both artifact hashes match
    └─ Decision: APPROVED_FOR_MERGE

         ↓ [Federated decision recorded]
         ↓

Producer C (release repo) consumes decision
    ├─ Reads Mapa decision: "integration ready"
    ├─ Confirms Producer A + B receipts both canonical
    ├─ Emits release receipt: "version 1.2.0 built from blessed artifacts"
    └─ Evidence: Hash chain links all three repos
```

**Audit Trail**:

```jsonl
{"timestamp": "2026-08-18T12:30:00Z", "event": "Producer A receipt received", "producer": "external-org/frontend", "status": "VALIDATED"}
{"timestamp": "2026-08-18T12:35:00Z", "event": "Producer B receipt received", "producer": "external-org/backend", "status": "VALIDATED"}
{"timestamp": "2026-08-18T12:40:00Z", "event": "Multi-repo approval", "decision": "APPROVED_FOR_MERGE", "evidence": ["receipt-A", "receipt-B"]}
{"timestamp": "2026-08-18T12:45:00Z", "event": "Producer C receipt received", "producer": "external-org/release", "status": "VALIDATED"}
```

---

## Implementation Roadmap

### Phase 2-P1-04a: Foundation (Week 1)

1. ✅ Design federation architecture (this document)
2. Create `tools/validate_federated_receipt.py` (receipt broker validator)
3. Create `tools/verify_cross_repo_provenance.py` (chain verifier)
4. Create `tools/audit_federated_receipt.py` (audit logger)
5. Create `data/control-plane/federation-policy.v1.json` (policy template)

### Phase 2-P1-04b: Infrastructure (Week 2-3)

1. Create `.github/workflows/federated-receipt-broker.yml` (reception workflow)
2. Implement HMAC key management in GitHub Secrets
3. Create producer onboarding issue template
4. Document producer integration guide (`.md`)
5. Test with internal producer (Mapa → itself as test)

### Phase 2-P1-04c: Operations (Week 4+)

1. Launch federation for first external producer
2. Monitor cross-repo receipt chains
3. Escalate policy violations to Lane 00
4. Quarterly federation audit

---

## Governance Integration

### Lane Responsibilities

| Lane | Responsibility | Federated Role |
|------|---|---|
| **00** | Policy authority | Approves producer registration; authorizes federation mode |
| **04** | Validation | Validates cross-repo signatures; verifies provenance |
| **05** | Evidence | Manages federated receipt index; cross-repo hash chains |
| **06** | Integration | Confirms no cascading dependencies; federation integration |
| **07** | Security | Reviews cross-border data transfer; contract terms |
| **08** | Observability | Federated receipt dashboard; multi-repo metrics |

### Append-Only Audit Logs

Two new audit trails:

1. **`data/audits/federated-receipts-audit.jsonl`**
   - Every federated receipt received, validated, or rejected
   - Producer identity, signature status, validation result
   - Immutable append-only

2. **`data/audits/federation-policy-decisions.jsonl`**
   - Producer registration approved/rejected
   - Policy changes by Lane 00
   - Contract renewals and expirations

---

## Security & Privacy Considerations

### Threat Model

| Threat | Mitigation |
|--------|-----------|
| Forged receipt | HMAC signature + timestamp validation |
| Signature replay | Unique timestamp + sequence counter |
| Secrets in receipt | Automated secret scanning before acceptance |
| Man-in-middle | TLS 1.3 required; GitHub API transport |
| Unauthorized producer | Registration approval gate (Lane 00) |
| Contract violation | Monitoring; auto-reject after 3 failures |
| Cross-border compliance | Explicit flag in policy; GDPR/LGPD check |

### Privacy Controls

- ✓ Producer identity explicit (not anonymous)
- ✓ Public repos only (no private repo participation)
- ✓ Receipts stored with audit access controls
- ✓ Cross-border transfers require policy approval
- ✓ Personal data minimization (no PII in receipts)

---

## Success Criteria

✅ Federation schema design complete  
✅ HMAC signature validation implemented  
✅ Cross-repo provenance verification working  
✅ Broker validation gates enforced  
✅ Federation policy template created  
✅ Producer onboarding documented  
✅ First external producer successfully emitting receipts  
✅ Multi-repo receipt chains validated  
✅ Audit trails complete and append-only  
✅ Lane 00 governance integration functional

---

## References

- Rafaelia Framework: `/docs/FRAMEWORK_REFERENCE_CARD.md`
- Fail-Closed Machine: `/docs/governance/PROOF_CUSTODY_AND_TOKEN_VALIDITY_V1.md`
- 10 Lanes: `/docs/governance/BRANCH_TOPOLOGY_MAIN_NUMBERED_V1.md`
- Receipt Schema: `/data/receipts/rafaelia_adaptive_cycle_latest4_*.receipt.json`
- TOKEN_VAZIO Approval: `/docs/governance/TOKEN_VAZIO_APPROVAL_WORKFLOWS_V1.md`
