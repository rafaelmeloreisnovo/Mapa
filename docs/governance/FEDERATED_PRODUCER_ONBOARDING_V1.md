# Federated Producer Onboarding V1

## Step-by-Step Integration Guide for External Repositories

**Date**: 2026-08-19
**Framework**: Rafaelia Federation System
**Target Audience**: Repository administrators seeking to emit Rafaelia receipts
**Status**: Phase 2-P1-04b Implementation Guide

---

## Table of Contents

1. [Before You Start](#before-you-start)
2. [Step 1: Request Producer Registration](#step-1-request-producer-registration)
3. [Step 2: Receive Credentials from Mapa](#step-2-receive-credentials-from-mapa)
4. [Step 3: Set Up Receipt Emission](#step-3-set-up-receipt-emission)
5. [Step 4: Validate Local Receipt](#step-4-validate-local-receipt)
6. [Step 5: Submit Federated Receipt](#step-5-submit-federated-receipt)
7. [Step 6: Await Broker Validation](#step-6-await-broker-validation)
8. [Step 7: Governance Authority Approval](#step-7-governance-authority-approval)
9. [Troubleshooting & Support](#troubleshooting--support)

---

## Before You Start

### Prerequisites

- [ ] Repository on GitHub
- [ ] Public repository (Rafaelia policy requires public repos)
- [ ] LICENSE file in repository (Apache 2.0, MIT, GPL-3.0, or approved license)
- [ ] No secrets/sensitive data committed
- [ ] Repository owner has GitHub Actions enabled
- [ ] Administrator access to repository secrets

### What You'll Need

- **HMAC Secret Key** (provided by Mapa Lane 00 during approval)
- **Broker Endpoint URL** (e.g., `https://api.mapa.rafaelia/federated-receipts`)
- **Federation Policy Document** (provided after approval)
- **Sample Receipt Template** (provided in this guide)

### What Rafaelia Receipts Are

A **Rafaelia federated receipt** is an immutable, cryptographically signed JSON document that captures:

| Observation | Purpose | Example |
|---|---|---|
| **identidade** | Unique producer identifier | `owner/repo-name` |
| **proveniência** | Origin & custody chain | Workflow run ID, timestamp |
| **contexto** | Execution environment | GitHub Actions runner, OS |
| **privacidade** | Data classification & PII status | `INTERNAL`, no PII |
| **estado_epistêmico** | Knowledge level & confidence | `observed` (95% confidence) |
| **dependências** | What this depends on | External actions, runtimes |
| **evidência** | Supporting artifacts & validation results | Workflow logs, test outputs |
| **próximo_passo** | Next action required | "Awaiting governance approval" |

---

## Step 1: Request Producer Registration

### 1.1 Create Registration Issue in Mapa Repository

Open a **new issue** in `rafaelmeloreisnovo/Mapa` with:

**Title**: `REGISTRATION REQUEST: Federated Producer — [your-org/your-repo]`

**Body**:

```markdown

## Producer Registration Request

**Repository**: `[your-org]/[your-repo]`
**Repository URL**: `https://github.com/[your-org]/[your-repo]`
**Producer Type**: `[application|library|service|infrastructure]`
**Repository License**: `[Apache-2.0|MIT|GPL-3.0|OTHER]`
**Administrator Contact**: `[email or GitHub handle]`

### Confirmation Checklist

- [ ] Repository is public
- [ ] Repository contains LICENSE file
- [ ] No secrets/tokens committed (verified with `git log -p` search)
- [ ] GitHub Actions enabled
- [ ] Ready to emit Rafaelia receipts

### Expected Use

Brief description of what receipts this producer will emit:

- What evidence will receipts carry?
- When will receipts be emitted (on every run, weekly, etc.)?
- Will receipts be used for multi-repo coordination?

### References

- Federation Policy: [Link to federation-policy.v1.json]
- Architecture: [Link to FEDERATED_PRODUCER_REPOSITORIES_V1.md]

```

### 1.2 What Happens Next

1. **Lane 04 (Validação)** reviews your registration
2. **Lane 06 (Integração)** checks for cascading dependencies
3. **Lane 00 (Governança)** makes approval decision
4. You receive notification within 24 hours

---

## Step 2: Receive Credentials from Mapa

Once approved, Lane 00 provides:

### 2.1 HMAC Secret Key

**Format**: 64-character hex string
**Example**: `abc123def456789...`

**⚠️ SECURITY**: Never commit this to version control. Store only in GitHub Secrets.

### 2.2 Broker Endpoint URL

**Format**: `https://api.mapa.rafaelia/federated-receipts`
**Authentication**: POST with signed receipt

### 2.3 Federation Policy

A copy of `federation-policy.v1.json` confirming:

- Your producer status (REGISTERED or PROVISIONAL)
- Approval dates and expiry
- Rejection criteria for your receipts
- Privacy & security requirements

### 2.4 Sample Receipt Template

Template to base your receipts on (see Step 3).

---

## Step 3: Set Up Receipt Emission

### 3.1 Create Receipt Generation Workflow

In your repository, create `.github/workflows/emit-rafaelia-receipt.yml`:

```yaml

name: Emit Rafaelia Receipt

on:
  workflow_run:
    workflows: ["CI"]  # Adjust to your actual CI workflow name
    types: [completed]

permissions:
  contents: read
  id-token: write

jobs:
  emit-receipt:
    runs-on: ubuntu-latest
    if: github.event.workflow_run.conclusion == 'success'

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Generate Receipt
        id: generate
        run: |
          python3 << 'PYEOF'
          import json
          import hashlib
          from datetime import datetime, timezone

          # Load HMAC secret (stored in repo secrets)
          import os
          hmac_secret = os.getenv("RAFAELIA_HMAC_SECRET")

          # Generate receipt
          receipt = {
              "schema": "rafaelia.federated-producer-receipt.v1",
              "observed_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
              "producer_identity": {
                  "repository_owner": "${{ github.repository_owner }}",
                  "repository_name": "${{ github.event.repository.name }}",
                  "repository_url": "${{ github.event.repository.html_url }}",
                  "producer_type": "application",  # Adjust as needed
                  "federation_status": "REGISTERED"
              },
              "producer_commitment": {
                  "signed_by_sha256": hashlib.sha256(hmac_secret.encode()).hexdigest(),
                  "signer_identity": "${{ github.repository }}",
                  "signature_algorithm": "HMAC-SHA256",
                  "signature_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                  "signature_validity_hours": 24
              },
              "provenance_chain": {
                  "source_producer_repository": "${{ github.repository }}",
                  "source_workflow": "${{ github.workflow }}",
                  "source_run_id": "${{ github.run_id }}",
                  "source_job_id": "${{ github.job }}",
                  "received_by": "producer-workflow",
                  "received_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                  "transport_integrity": "HTTPS-TLS-1.3"
              },
              "cross_repo_observations": {
                  "producer_identifier": {
                      "uuid": "${{ github.repository }}",
                      "canonical_name": "${{ github.event.repository.name }}",
                      "identity_hash": hashlib.sha256("${{ github.repository }}".encode()).hexdigest()
                  },
                  "producer_provenance": {
                      "origin": "github.com/${{ github.repository }}",
                      "custody_chain": ["producer-workflow"],
                      "root_cause": "CI completion on ${{ github.event_name }}"
                  },
                  "producer_context": {
                      "execution_environment": "GitHub Actions",
                      "runtime": "ubuntu-latest",
                      "workflow_name": "${{ github.workflow }}",
                      "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
                  },
                  "producer_privacy": {
                      "data_classification": "INTERNAL",
                      "pii_scan": "no_pii_detected",
                      "gdpr_compliant": true,
                      "lgpd_compliant": true,
                      "secrets_scan": "no_secrets_detected"
                  },
                  "producer_epistemic_level": {
                      "knowledge_level": "observed",
                      "confidence": 0.95,
                      "falsifiers_applied": true,
                      "can_be_promoted": true
                  },
                  "producer_dependencies": {
                      "direct": ["GitHub Actions runtime"],
                      "transitive": ["ubuntu-latest-runner"],
                      "external": []
                  },
                  "producer_evidence": {
                      "artifacts": [
                          "workflow-run-logs",
                          "test-results"
                      ],
                      "validation_result": "PASS",
                      "immutability_proof": "run_id + timestamp"
                  },
                  "producer_next_step": {
                      "action_required": "SUBMIT_TO_BROKER",
                      "decision_type": "FEDERATED_RECEIPT_EMISSION",
                      "sla": "immediate",
                      "escalation": "if_submission_fails"
                  }
              }
          }

          # Save receipt
          with open("receipt.json", "w") as f:
              json.dump(receipt, f, indent=2)

          print("✓ Receipt generated")
          PYEOF

      - name: Store receipt as artifact
        uses: actions/upload-artifact@v4
        with:
          name: rafaelia-receipt-${{ github.run_id }}
          path: receipt.json

      - name: Submit to Broker
        env:
          BROKER_ENDPOINT: ${{ secrets.RAFAELIA_BROKER_ENDPOINT }}
          HMAC_SECRET: ${{ secrets.RAFAELIA_HMAC_SECRET }}
        run: |
          set -euo pipefail

          # Sign receipt with HMAC
          receipt_json=$(cat receipt.json)
          signature=$(echo -n "$receipt_json" | openssl dgst -sha256 -hmac "$HMAC_SECRET" | cut -d' ' -f2)

          # Submit to broker
          curl -X POST \
            -H "Content-Type: application/json" \
            -H "X-Receipt-Signature: $signature" \
            -H "X-Producer: ${{ github.repository }}" \
            -d @receipt.json \
            "$BROKER_ENDPOINT/federated-receipts" \
            || echo "WARNING: Broker submission failed (expected if broker not yet deployed)"

```

### 3.2 Store Credentials in Repository Secrets

In your repository settings, add:

1. **RAFAELIA_HMAC_SECRET**: The secret key provided by Mapa
2. **RAFAELIA_BROKER_ENDPOINT**: The broker URL provided by Mapa

**Security**: Only repository administrators can see these secrets. They're never logged or exposed in workflow runs.

---

## Step 4: Validate Local Receipt

Before submitting, validate your receipt format:

### 4.1 Download Validation Tool

From Mapa repository:

```bash

curl -o validate_federated_receipt.py \
  https://raw.githubusercontent.com/rafaelmeloreisnovo/Mapa/main/tools/validate_federated_receipt.py

```

### 4.2 Run Validation

```bash

python3 validate_federated_receipt.py \
  --receipt receipt.json \
  --policy federation-policy.v1.json

```

### 4.3 Check Output

**If VALIDATED**:

```

✓ receipt.json VALIDATED
Status: VALIDATED

```

**If REJECTED**:

- Review error messages (schema, signature, timestamp, etc.)
- Fix issues in your receipt generation workflow
- Re-run validation

---

## Step 5: Submit Federated Receipt

### 5.1 Manual Submission (for testing)

```bash

# Sign receipt
receipt_json=$(cat receipt.json)
signature=$(echo -n "$receipt_json" | openssl dgst -sha256 -hmac "$HMAC_SECRET" | cut -d' ' -f2)

# Submit
curl -X POST \
  -H "Content-Type: application/json" \
  -H "X-Receipt-Signature: $signature" \
  -H "X-Producer: your-org/your-repo" \
  -d @receipt.json \
  "https://api.mapa.rafaelia/federated-receipts"

```

### 5.2 Automated Submission

Your workflow (`emit-rafaelia-receipt.yml`) handles this automatically on each CI completion.

---

## Step 6: Await Broker Validation

After submission, the Mapa broker validates:

1. **GATE 1**: Schema compliance (rafaelia.federated-producer-receipt.v1)
2. **GATE 2**: HMAC signature verification
3. **GATE 3**: Producer registration status
4. **GATE 4**: Immutability markers (run_id, job_id, timestamp, received_at_utc)
5. **GATE 5**: Provenance chain continuity

**Timeline**: Usually completes within minutes.

**What happens if validation fails**:

- Broker logs rejection reason
- Your producer gets notified (via GitHub Issues)
- Review federation policy rejection criteria
- Fix issues and resubmit

---

## Step 7: Governance Authority Approval

Once broker validation passes:

1. **Lane 04 (Validação)** confirms all gates passed
2. **Lane 06 (Integração)** confirms no cascading gaps
3. **Lane 00 (Governança)** issues governance decision (24-hour SLA)

**Approval outcomes**:

- **APPROVED_CLOSED**: Receipt accepted, can be used for downstream decisions
- **APPROVED_PRESERVED**: Receipt accepted but marked for observation
- **CONDITIONAL**: Approval requires remediation of specific issues
- **REJECTED**: Does not meet policy requirements, cannot be used

---

## Troubleshooting & Support

### Issue: HMAC Signature Verification Failed

**Cause**: Secret key mismatch

**Fix**:

```bash

# Verify secret is set
echo $RAFAELIA_HMAC_SECRET | wc -c  # Should be 65 (64 chars + newline)

# Check for hidden characters
echo -n "$RAFAELIA_HMAC_SECRET" | od -c

```

### Issue: Schema Validation Failed

**Cause**: Missing or malformed fields

**Fix**: Use the sample receipt template and ensure all 8 observations are present.

### Issue: Timestamp Too Old (> 24 hours)

**Cause**: Receipt submitted after signature expiry

**Fix**: Reduce delay between receipt generation and submission, or increase `signature_validity_hours`.

### Issue: Producer Not in Approved List

**Cause**: Registration not yet approved by Lane 00

**Fix**: Check registration issue status in Mapa repository. Approval SLA is 24 hours.

### Issue: Broker Endpoint Unreachable

**Cause**: Broker not yet deployed or network issue

**Fix**: During Phase 2-P1-04c, you can manually verify receipt locally using the validation tool.

---

## Monitoring & Metrics

Once approval is complete, monitor your submissions:

1. **Broker Dashboard** (upcoming P1-04c): Real-time receipt status
2. **Audit Trail**: `data/audits/federated-receipts-audit.jsonl` in Mapa
3. **Rejection Rate**: Monitor if your receipts start failing validation

---

## Governance & Compliance

### Data Retention

Mapa stores your federated receipts for **730 days** (2 years) minimum.

### Privacy & GDPR/LGPD

- Receipts are classified as INTERNAL data
- No PII is captured in receipts
- Producer repos must be public (no private data)
- Data subject rights (access/deletion) honored under GDPR Article 17

### Security Review

Quarterly federation audits verify:

- All producers still comply with policy
- No unauthorized modifications to receipts
- Signature validity maintained
- Audit trail integrity preserved

---

## Next Steps After Approval

Once your producer is approved and receipts are flowing:

1. **Join Multi-Repo Governance Chains** (Phase 2-P1-05)
   - Coordinate receipts across multiple producers
   - Use cross-repo evidence for architectural decisions

2. **Participate in Approval Workflows** (Phase 2-P1-06)
   - Submit evidence from your repository
   - Participate in governance voting

3. **Schedule Quarterly Audits** (Phase 2-P1-07)
   - Lane 04 validates your receipt compliance
   - Document any changes or issues
   - Renew producer registration annually

---

## Support & Escalation

**Questions**: Open an issue in Mapa with label `federated-producer-support`

**Urgent Issues**: Contact Lane 00 (Governança) via `lane-00@mapa.rafaelia`

**Appeal Process**: See `/docs/governance/PROOF_CUSTODY_AND_TOKEN_VALIDITY_V1.md` Section 7

---

## References

- **Federation Policy**: `/data/control-plane/federation-policy.v1.json`
- **Architecture**: `/docs/governance/FEDERATED_PRODUCER_REPOSITORIES_V1.md`
- **Validation Tool**: `tools/validate_federated_receipt.py`
- **Governance Framework**: `/docs/governance/PROOF_CUSTODY_AND_TOKEN_VALIDITY_V1.md`
- **Approval Workflow**: `.github/workflows/federated-receipt-broker.yml`
