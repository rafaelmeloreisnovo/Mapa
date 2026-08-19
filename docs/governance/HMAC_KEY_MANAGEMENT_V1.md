# HMAC Key Management & Security V1

## Cryptographic Key Lifecycle for Federated Receipt Signing

**Date**: 2026-08-19  
**Framework**: Rafaelia Federation System (Phase 2-P1-04b)  
**Audience**: System Administrators, Lane 00 (Governança), Lane 07 (Segurança)  
**Status**: Operational Guidelines

---

## Table of Contents

1. [Key Generation & Storage](#key-generation--storage)
2. [Key Rotation Policy](#key-rotation-policy)
3. [Distribution & Access Control](#distribution--access-control)
4. [Monitoring & Audit](#monitoring--audit)
5. [Incident Response](#incident-response)
6. [Compliance & Attestation](#compliance--attestation)

---

## Key Generation & Storage

### 1.1 Key Generation

HMAC secrets for Rafaelia federation are **randomly generated 256-bit keys** (64 hex characters).

**Generation Method**:

```bash
# Using OpenSSL (FIPS-compliant)
openssl rand -hex 32 > hmac-secret.txt

# Using Python (for verification)
import secrets
key = secrets.token_hex(32)
print(key)  # e.g., abc123def456...
```

**Security Properties**:
- **Length**: 32 bytes (256 bits) minimum
- **Entropy**: Cryptographically random (≥128 bits effective entropy)
- **Format**: Hex-encoded ASCII string (no binary storage)
- **Algorithm**: HMAC-SHA256 (not HMAC-MD5 or HMAC-SHA1)

### 1.2 Storage

**Primary Storage**: GitHub Secrets (production)

| Location | Purpose | Encryption | Access |
|----------|---------|-----------|--------|
| **GitHub Secrets** | Producer repo secrets | GitHub-managed encryption | Repo admins only |
| **Mapa Vault** | Broker-side backup | AES-256 | Lane 07 (Segurança) only |
| **Audit Trail** | Hashed key fingerprint (never raw key) | SHA256 | Lane 00 (Governança) |
| **Local (dev)** | Development/testing only | N/A (test keys only) | Developer laptops |

**Never Store**:
- ❌ In version control (git)
- ❌ In workflow logs
- ❌ In comments or documentation
- ❌ In unencrypted files
- ❌ In email or Slack

---

## Key Rotation Policy

### 2.1 Rotation Schedule

| Scenario | Rotation Frequency |
|----------|-------------------|
| **Scheduled rotation** | Annually (365 days) |
| **Producer status change** | PROVISIONAL → REGISTERED (immediate) |
| **Producer deregistration** | Immediate (within 1 hour) |
| **Suspected compromise** | Immediate emergency rotation |
| **Signature verification failure** | Diagnostic rotation (7-day audit) |

### 2.2 Scheduled Rotation Process

**Timeline**: 2 weeks notice + 1 week dual-key period

**Week 1: Announcement**
1. Lane 00 schedules rotation date
2. Notify producer (via GitHub Issue)
3. Provide new key via secure channel

**Week 2: Dual-Key Period**
1. Producer activates new key in GitHub Secrets
2. Keep old key for 7 days (fallback)
3. Broker accepts both keys during transition
4. Both signatures log to audit trail

**Week 3: Old Key Deactivation**
1. Broker stops accepting old key
2. Producer confirms all receipts using new key
3. Old key securely deleted
4. Rotation logged to audit trail

### 2.3 Emergency Rotation

**Triggers**:
- Suspected key compromise (e.g., accidental commit to public repo)
- Unauthorized signature detection
- Storage breach on producer or broker side
- Security incident affecting related systems

**Process** (within 1 hour):
1. **Immediate**: Rotate key in GitHub Secrets (producer side)
2. **Immediate**: Rotate key in Vault (broker side)
3. **Within 15 min**: Audit recent receipts for unauthorized signatures
4. **Within 1 hour**: Notify Lane 00 & Lane 07 of incident
5. **Within 24 hours**: Incident report to governance

**Fallback**: If broker key lost, refuse all receipts until key recovery (fail-closed).

---

## Distribution & Access Control

### 3.1 Secure Delivery to Producer

**Initial Key Distribution** (during registration approval):

1. **Lane 00 generates key** using cryptographically secure RNG
2. **Lane 00 creates encrypted message**:
   - Encrypt key using producer's GitHub organization public key (if available)
   - Fallback: Provide via secure private GitHub Issue (read-only to producer admin)
   - Include: Key, expiry date, broker endpoint, policy document

3. **Producer receives & stores**:
   - Decrypt if encrypted
   - Store in GitHub Secrets immediately
   - Delete all unencrypted copies
   - Confirm receipt (reply to issue)

4. **Audit log**:
   ```json
   {
     "timestamp": "2026-08-19T12:00:00Z",
     "event": "KEY_DISTRIBUTION",
     "producer": "external-org/external-repo",
     "key_fingerprint_sha256": "abc123def456...",
     "delivery_method": "github-secrets",
     "recipient_confirmed": true,
     "lane_authority": "00_governanca"
   }
   ```

### 3.2 Access Control Matrix

| Role | Can Generate | Can Distribute | Can Audit | Can Rotate |
|------|---|---|---|---|
| **Producer Admin** | ❌ | ❌ | ✅ (own keys only) | ❌ |
| **Broker Admin** | ✅ | ✅ | ✅ | ✅ |
| **Lane 00** | ✅ | ✅ | ✅ | ✅ |
| **Lane 07** | ❌ | ❌ | ✅ | ✅ (emergency) |
| **Lane 04** | ❌ | ❌ | ✅ (validation only) | ❌ |

### 3.3 Producer-Side Secret Management

**GitHub Secrets Configuration**:

```yaml
# In producer repository settings → Secrets and variables → Actions

RAFAELIA_HMAC_SECRET: [64-char hex string from Mapa Lane 00]
RAFAELIA_BROKER_ENDPOINT: "https://api.mapa.rafaelia/federated-receipts"
```

**Workflow Usage** (NEVER print secret):

```yaml
env:
  HMAC_SECRET: ${{ secrets.RAFAELIA_HMAC_SECRET }}

jobs:
  emit-receipt:
    runs-on: ubuntu-latest
    steps:
      - name: Generate Receipt
        run: |
          # ✅ CORRECT: Use secret without logging
          signature=$(echo -n "$receipt" | openssl dgst -sha256 -hmac "$HMAC_SECRET")
          
          # ❌ WRONG: Never do this
          # echo "Secret: $HMAC_SECRET"  # Would be logged!
          # echo $HMAC_SECRET > file.txt # Would be committed!
```

---

## Monitoring & Audit

### 4.1 Key Usage Audit Trail

**Every receipt submission logged**:

```json
{
  "timestamp": "2026-08-19T12:05:30Z",
  "event": "RECEIPT_SIGNATURE_VERIFIED",
  "producer": "external-org/external-repo",
  "key_fingerprint": "abc123def456...",
  "signature_algorithm": "HMAC-SHA256",
  "signature_valid": true,
  "receipt_id": "receipt-123456789",
  "run_id": "12345678901"
}
```

**Append-only storage**: `data/audits/hmac-key-audit.jsonl`

### 4.2 Anomaly Detection

**Alert on**:
- ⚠️ Signature verification failure from trusted producer
- ⚠️ Unusual submission frequency (e.g., 100+ receipts/hour)
- ⚠️ Receipts from unexpected GitHub Actions runners
- ⚠️ Multiple failed signature attempts (potential attack)

**Thresholds**:
- **1 failure**: Log and investigate
- **3 failures in 24 hours**: Notify producer & Lane 07
- **10 failures in 24 hours**: Suspend producer pending review

### 4.3 Monthly Key Audit Report

**Lane 07 generates monthly**:

```markdown
# HMAC Key Audit Report — August 2026

## Key Status
- Active keys: 15
- Recently rotated: 3
- Expired/deactivated: 5
- Total submissions this month: 12,543

## Security Events
- Signature failures: 2 (investigated, cleared)
- Key compromise incidents: 0
- Unauthorized submissions: 0

## Compliance
- Rotation schedule adherence: 100%
- Audit trail completeness: 100%
- Producer acknowledgment rate: 100%

## Recommendations
- [List any security improvements]
```

---

## Incident Response

### 5.1 Signature Verification Failure

**Occurs when**: Broker cannot verify receipt signature with stored key

**Investigation**:
1. Check if producer recently rotated key (expected)
2. Compare signature with audit trail (look for new key fingerprint)
3. Verify receipt hasn't been tampered with (check all fields)
4. Contact producer if issue persists

**Resolution**:
- ✅ If expected rotation: Accept receipt (2-week dual-key period)
- ✅ If producer rotated early: Update broker key, confirm with producer
- ❌ If tampering suspected: Reject receipt, escalate to Lane 07

### 5.2 Suspected Key Compromise

**Indicators**:
- Unauthorized receipt from producer
- Signature verification fails when it shouldn't
- Producer reports accidental secret exposure

**Immediate Actions** (within 15 minutes):
1. **Producer**: Rotate key in GitHub Secrets immediately
2. **Broker**: Deactivate old key, prevent new receipts with old signature
3. **Lane 07**: Begin forensic audit of recent receipts
4. **Lane 00**: Prepare incident response plan

**Investigation** (within 24 hours):
- Review all receipts signed with compromised key
- Identify which ones were legitimate vs. forged
- Determine exposure timeline
- Implement long-term mitigations

**Recovery**:
- Producer can request re-submission of legitimate receipts with new key
- Forged receipts remain in audit trail (marked as compromised)
- Post-incident review with Lane 00

---

## Compliance & Attestation

### 6.1 Security Standards

**Rafaelia federation key management complies with**:

| Standard | Requirement | Compliance |
|----------|-------------|-----------|
| **OWASP** | Secrets not in logs/VC | ✅ GitHub Secrets only |
| **NIST SP 800-57** | Key rotation ≤ 1 year | ✅ Annual rotation |
| **GDPR/LGPD** | Data protection | ✅ AES-256 at rest |
| **FIPS 140-2** | Cryptographic module | ✅ OpenSSL FIPS-capable |
| **SOC 2** | Access controls | ✅ Role-based, audited |

### 6.2 Annual Attestation

**Lane 07 (Segurança) signs off annually**:

```json
{
  "timestamp": "2026-12-31T23:59:59Z",
  "attestation": "HMAC_KEY_MANAGEMENT_SECURE",
  "scope": "Rafaelia Federation System",
  "period": "2026-01-01 to 2026-12-31",
  "findings": [
    "0 unauthorized access incidents",
    "100% key rotation compliance",
    "All producers rotated keys on schedule",
    "No audit trail tampering detected"
  ],
  "signed_by": "Lane 07 Security Authority",
  "status": "APPROVED"
}
```

### 6.3 Proof of Custody

Every key carries immutable proof:

1. **Generation timestamp**: When key was created
2. **Distribution record**: Who received it and when
3. **Usage history**: Every receipt signed with this key
4. **Rotation record**: When key was rotated or deactivated

**Cannot be forged**: Requires authority signature (Lane 00 or Lane 07)

---

## Key Recovery & Disaster Recovery

### 7.1 If Broker Key Lost

**Scenario**: Broker's HMAC key store is lost/corrupted

**Process**:
1. **Fail-closed**: All receipts rejected until key recovery
2. **Backup activation**: Restore HMAC keys from encrypted backup
3. **Verification**: Confirm key fingerprints match audit trail
4. **Incident report**: Document RTO/RPO (max 1 hour RTO)

### 7.2 If Producer Key Lost

**Scenario**: Producer can't access GitHub Secrets

**Process**:
1. Producer contacts Lane 00 (via secure channel)
2. Lane 00 regenerates key
3. Secure delivery to producer (same as initial distribution)
4. Producer updates GitHub Secrets
5. Confirm with test receipt before resuming production

---

## References

- **Federation Policy**: `/data/control-plane/federation-policy.v1.json`
- **Producer Onboarding**: `/docs/governance/FEDERATED_PRODUCER_ONBOARDING_V1.md`
- **Governance Framework**: `/docs/governance/PROOF_CUSTODY_AND_TOKEN_VALIDITY_V1.md`
- **Architecture**: `/docs/governance/FEDERATED_PRODUCER_REPOSITORIES_V1.md`

---

## Appendix: Key Generation Command Reference

**Generate new key**:
```bash
openssl rand -hex 32
```

**Get key fingerprint** (for audit):
```bash
echo -n "abc123def456..." | sha256sum
```

**Test HMAC signature**:
```bash
echo -n "test message" | openssl dgst -sha256 -hmac "your-secret-key"
```

**Verify receipt signature** (producer-side):
```bash
# Inside workflow
signature=$(echo -n "$receipt_json" | openssl dgst -sha256 -hmac "$RAFAELIA_HMAC_SECRET" | cut -d' ' -f2)
echo "Signature: $signature"
```
