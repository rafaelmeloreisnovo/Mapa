# Federated Receipt Operations Runbook V1

## Operational Procedures for Lane 04/06/00/07/08

**Date**: 2026-08-21  
**Framework**: Rafaelia Federation System (Phase 2-P1-04c)  
**Audience**: Lane operators, governance authorities, security team  
**Status**: Operational procedures guide

---

## Table of Contents

1. [Overview](#overview)
2. [Daily Operations (Lane 04)](#daily-operations-lane-04)
3. [Weekly Review (Lane 06)](#weekly-review-lane-06)
4. [Monthly Audit (Lane 07 + Lane 00)](#monthly-audit-lane-07--lane-00)
5. [Incident Response](#incident-response)
6. [Approval Workflow (Lane 00)](#approval-workflow-lane-00)
7. [Escalation Procedures](#escalation-procedures)
8. [Metrics & Dashboards](#metrics--dashboards)

---

## Overview

Federated Producer Infrastructure enables external repositories to emit Rafaelia receipts with complete governance oversight.

**Key components**:
- **Broker Workflow**: `.github/workflows/federated-receipt-broker.yml` (5 validation gates)
- **Receipt Format**: 8 observations + immutability markers
- **Audit Trail**: Append-only logs (federated-receipts-audit.jsonl, hmac-key-audit.jsonl)
- **Approval Process**: 3-gate workflow (Evidence → Validation → Authority)

**Lane responsibilities**:
- **Lane 00 (Governança)**: Authority decisions, policy setting
- **Lane 04 (Validação)**: Receipt validation, schema compliance, falsifier execution
- **Lane 06 (Integração)**: Cross-producer impact assessment, cascading gap detection
- **Lane 07 (Segurança)**: Key management, anomaly detection, incident response
- **Lane 08 (Observabilidade)**: Metrics, release decision, compliance monitoring

---

## Daily Operations (Lane 04)

### Morning Check-In (Start of Day)

**Time**: 9:00 AM or local equivalent  
**Owner**: Lane 04 Operator  
**Duration**: 15-30 minutes

**Steps**:

1. **Check broker workflow status**
   ```bash
   # View recent broker runs
   gh workflow view federated-receipt-broker.yml --json status,conclusion
   ```
   - If any runs failed: Note failure reason
   - If gate validation failed: Investigate specific gate

2. **Review submission errors**
   ```bash
   # Check audit trail for failures in last 24 hours
   tail -100 data/audits/federated-receipts-audit.jsonl | grep REJECTED
   ```
   - Count rejections by error type
   - Flag patterns (e.g., all from one producer)

3. **Verify audit trail integrity**
   ```bash
   # Check append-only property (no deletions)
   wc -l data/audits/federated-receipts-audit.jsonl
   # Compare to yesterday's count (should only increase)
   ```

### Receipt Validation (On Submission)

**Trigger**: New receipt submitted to broker  
**Owner**: Lane 04 Operator (automated workflow, manual review if needed)  
**SLA**: 1 hour from submission

**Steps**:

1. **Run validation tool**
   ```bash
   python3 tools/verify_cross_repo_provenance.py \
     --receipt <receipt_path> \
     --verbose
   ```

2. **Check all 8 observations present**
   - ✓ identidade (producer_identity)
   - ✓ proveniência (provenance_chain)
   - ✓ contexto (producer_context)
   - ✓ privacidade (producer_privacy)
   - ✓ estado_epistêmico (producer_epistemic_level)
   - ✓ dependências (producer_dependencies)
   - ✓ evidência (producer_evidence)
   - ✓ próximo_passo (producer_next_step)

3. **Verify immutability markers**
   - run_id present and matches GitHub run
   - job_id present and matches GitHub job
   - timestamp present and < 24 hours old
   - received_at_utc present

4. **Check HMAC signature**
   - Signature algorithm: HMAC-SHA256
   - Key fingerprint matches registered producer
   - Signature valid (broker already checks; confirm if re-verifying)

5. **Log validation result**
   - Auto-logged by broker workflow
   - Manual validation logged to audit trail if manual review done

### Error Handling (Lane 04)

**Schema Validation Failed**
```
Error: Missing field "X" in receipt
Action:
1. Contact producer via issue or email
2. Reference onboarding guide section on receipt format
3. Request corrected receipt
4. Re-run validation after re-submission
SLA: 24 hours to producer response
```

**Signature Verification Failed**
```
Error: HMAC signature invalid
Possible causes:
1. Producer used wrong key (check key rotation status)
2. Receipt tampered after signing (unlikely via HTTPS)
3. Key mismatch (producer updated key without notifying broker)

Action:
1. Check Lane 07 HMAC key audit for recent rotations
2. Verify producer's GitHub Secrets HMAC_SECRET is current
3. If mismatch found: Request re-submission with correct key
4. If still failing: Escalate to Lane 07 (may indicate key compromise)
SLA: 4 hours investigation, 24 hours resolution
```

**Timestamp Too Old (> 24 hours)**
```
Error: Receipt signature expired (> 24 hours old)
Action:
1. Check producer's submission timing (CI run completion vs submission delay)
2. Review onboarding guide section on timing windows
3. Request producer re-run CI to generate fresh receipt
SLA: Automatic on producer's re-run
```

**Immutability Marker Missing**
```
Error: run_id or job_id not present
Action:
1. Request producer check GitHub Actions environment variables
2. Verify receipt generation workflow includes:
   - ${{ github.run_id }}
   - ${{ github.job }}
3. Request corrected receipt after workflow update
SLA: 48 hours to producer fix
```

### End-of-Day Report (Lane 04)

**Time**: End of shift  
**Owner**: Lane 04 Operator  
**Output**: Slack/email summary

**Content**:
- Receipts validated today: [count]
- Receipts rejected today: [count]
- Validation errors (if any): [list]
- Escalations to Lane 07: [count]
- Status: ✅ OPERATIONAL / ⚠️ ISSUES / 🚨 CRITICAL

---

## Weekly Review (Lane 06)

### Monday Morning Review (Start of Week)

**Time**: 10:00 AM Monday  
**Owner**: Lane 06 Operator  
**Duration**: 1-2 hours

**Steps**:

1. **Run audit aggregator**
   ```bash
   python3 tools/aggregate_federated_audits.py \
     --format markdown \
     --output /tmp/weekly-audit.md
   ```

2. **Check for cascading gaps**
   - Are receipts from producer A affecting validation of producer B?
   - Example: Producer A emits receipt referencing producer B's artifact, but B's artifact not yet available
   - Action: File issue in Mapa with `federated-cascading-gap` label

3. **Verify no producer conflicts**
   - Two producers with same identity? (Should be prevented but verify)
   - Two producers claiming same repository? (Escalate to Lane 00)

4. **Review conditional approvals**
   - Check approval issues with `conditional-approval` label
   - Verify remediation deadlines have not passed
   - If deadline passed without remediation: Trigger re-evaluation (see approval workflow section)

5. **Check federation policy changes**
   - Has `data/control-plane/federation-policy.v1.json` changed?
   - If yes: Verify all producers still compliant with new policy
   - If policy tightened: May require producer updates

### Integration Gate (Lane 06)

**When**: Before marking receipt as READY_FOR_GOVERNANCE  
**Owner**: Lane 06 Operator  
**Checklist**:

- [ ] Receipt passes Lane 04 validation (all 5 gates)
- [ ] No cascading dependencies broken
- [ ] Producer status verified (PROVISIONAL or REGISTERED)
- [ ] HMAC key valid and current
- [ ] Audit trail entries present and immutable
- [ ] No conflicting registrations with existing producers

**Sign-off**: Lane 06 confirmation in audit trail

---

## Monthly Audit (Lane 07 + Lane 00)

### Lane 07 Security Audit (Last Thursday of Month)

**Time**: 14:00 UTC Thursday  
**Owner**: Lane 07 Operator  
**Duration**: 2-4 hours

**Steps**:

1. **Run comprehensive audit**
   ```bash
   python3 tools/aggregate_federated_audits.py --format json > /tmp/monthly-audit.json
   ```

2. **Review key rotation compliance**
   - All keys rotated within 365 days? (Should be annual)
   - Any emergency rotations this month? (Investigate cause)
   - Any keys approaching expiry? (Plan rotation)

3. **Analyze signature verification events**
   ```bash
   grep "RECEIPT_SIGNATURE_VERIFIED" data/audits/hmac-key-audit.jsonl | jq '.signature_valid' | sort | uniq -c
   ```
   - Count failures vs successes
   - If failures > 1%: Investigate why

4. **Detect anomalies**
   - Unusual submission volume (> 100 receipts/hour)?
   - Repeated signature failures from same producer?
   - Keys showing activity after deactivation?
   - Any unauthorized submission attempts?

5. **Generate security report**
   - Include: Key status, anomalies, failures, recommendations
   - Sign with Lane 07 authority
   - Upload to `data/audits/lane-07-monthly-report-YYYY-MM.json`

### Lane 00 Governance Audit (First Friday of Month)

**Time**: 10:00 UTC Friday  
**Owner**: Lane 00 Authority  
**Input**: Lane 07 report + Lane 04 validations + Lane 06 integrations  
**Duration**: 2-3 hours

**Steps**:

1. **Review decision history**
   - Approvals issued this month: [count]
   - Rejections: [count]
   - Conditional approvals: [count]
   - Decision SLA met: [%]

2. **Assess approval quality**
   - All decisions have complete evidence package?
   - All decisions documented with rationale?
   - No decisions reversed (should never happen)?

3. **Check governance compliance**
   - Federation policy complied with: ✅
   - All lanes followed procedures: ✅
   - Audit trail integrity confirmed: ✅
   - No unauthorized modifications: ✅

4. **Update federation status**
   - Producers in good standing: [count]
   - Producers under review: [count]
   - Producers suspended/revoked: [count]

5. **Issue governance statement**
   - Document as `data/audits/lane-00-monthly-governance-YYYY-MM.json`
   - Sign with Lane 00 authority
   - Include: Summary, decisions, recommendations, risk assessment

---

## Incident Response

### INCIDENT-01: Signature Verification Failure

**Symptoms**:
- Broker rejects receipt with "HMAC signature invalid"
- Producer reports their receipt was rejected

**Severity**: HIGH  
**SLA**: 4-hour diagnosis, 24-hour resolution

**Investigation** (Lane 07):

1. Check if producer recently rotated key
   ```bash
   grep -i "KEY_ROTATION" data/audits/hmac-key-audit.jsonl | tail -5
   ```
   - If yes and within 7-day dual-key window: Expected, mark as normal

2. Verify producer's key matches broker's key
   - Lane 00 has authoritative key
   - Lane 07 compares hash: `sha256(producer_key_from_secrets) == sha256(broker_key)`
   - If mismatch: Check if emergency rotation needed

3. Test signature locally
   ```bash
   openssl dgst -sha256 -hmac "$HMAC_SECRET" receipt.json
   # Compare against receipt.producer_commitment.signed_by_sha256
   ```

**Resolution options**:
- **Option A**: Normal key rotation (within 7-day dual-key window) → Accept, log, continue
- **Option B**: Producer key not yet updated → Request update, set 24-hour deadline
- **Option C**: Key mismatch (no rotation in progress) → Emergency rotation, see INCIDENT-02
- **Option D**: Receipt tampered (unlikely) → Reject, escalate to Lane 00

---

### INCIDENT-02: Suspected Key Compromise

**Symptoms**:
- Unauthorized receipt submission with valid signature
- Producer reports accidental secret exposure (e.g., committed to public repo)
- Anomalous submission patterns

**Severity**: CRITICAL  
**SLA**: 15-minute mitigation, 1-hour full response

**Immediate Actions** (< 15 minutes):

1. **Producer side** (notify immediately via GitHub issue or email):
   ```
   URGENT: Rotate RAFAELIA_HMAC_SECRET in GitHub Secrets immediately
   Old key: [fingerprint]
   New key: [regenerate and update]
   Action required within 15 minutes
   ```

2. **Broker side** (Lane 07):
   - Deactivate compromised key immediately
   - Prevent any new receipts with old key signature
   - Add to compromise log: `data/audits/key-compromise-log.jsonl`

3. **Forensic audit** (Lane 07):
   - Query all receipts signed with compromised key (last 30 days)
   - Separate legitimate from forged (check against producer's GitHub Actions runs)
   - Log findings to audit trail

**Investigation** (Within 24 hours):

1. Determine exposure timeline
   - When was secret exposed?
   - How long was it exposed?
   - Who had access?

2. Assess impact
   - How many unauthorized receipts signed?
   - What damage could they cause?
   - Are downstream systems affected?

3. Plan recovery
   - Producer reissues legitimate receipts with new key
   - Forged receipts marked as compromised in audit trail (immutable)
   - Review onboarding for secrets management improvements

**Resolution**:

1. Confirm producer has rotated key and updated GitHub Secrets
2. Broker accepts new receipts with new key signature
3. Issue incident report to Lane 00
4. Document lessons learned

---

### INCIDENT-03: Audit Trail Tampering Detected

**Symptoms**:
- Receipt appears in audit trail with earlier timestamp than actual submission
- Missing audit entries (count decreased)
- Duplicate entries with different signatures

**Severity**: CRITICAL (violates immutability invariant)  
**SLA**: Immediate escalation to Lane 00

**Response**:

1. **STOP all processing** (Lane 04):
   - Pause receipt validation
   - Alert all lanes

2. **Verify integrity** (Lane 07):
   - Compute hash of entire audit trail
   - Compare to last known good hash (if stored)
   - Check git history for unauthorized commits

3. **Escalate to Lane 00**:
   - File incident report with evidence
   - Determine if data recovery possible
   - May require federation system downtime

4. **No recovery without authority approval**:
   - Lane 00 must authorize any tampering response
   - All actions logged with explicit decision

---

### INCIDENT-04: Producer Rate-Limited (Too Many Submissions)

**Symptoms**:
- Producer submitting > 100 receipts/hour
- Broker workflow taking excessive resources
- Lane 08 observability alert triggered

**Severity**: MEDIUM  
**SLA**: 1-hour threshold notification, 24-hour resolution

**Response**:

1. **Check if legitimate** (Lane 04):
   - Is producer running multiple CI jobs in parallel?
   - Did they recently change CI frequency?
   - Check producer's GitHub Actions activity

2. **Contact producer** (Lane 04):
   ```
   We've noticed high receipt submission volume from your repo.
   Current rate: X submissions/hour (threshold: 100/hour)
   
   Is this expected? If yes, confirm with Lane 00.
   If not, check your CI configuration.
   
   Require response within 24 hours.
   ```

3. **Set rate limiting** (if needed):
   - Lane 00 may adjust federation policy for high-volume producers
   - Implement submission throttling in broker workflow
   - Ensure fairness for other producers

---

## Approval Workflow (Lane 00)

### Producer Registration Request

**Trigger**: New issue filed with `federated-producer-registration` label  
**Owner**: Lane 00 Authority  
**SLA**: 24 hours from evidence complete

**Steps**:

1. **GATE 1: Evidence Gathering** (Lane 04)
   ```
   Checklist:
   - [ ] Producer repository exists (public, accessible)
   - [ ] LICENSE file present (Apache-2.0, MIT, GPL-3.0, or approved)
   - [ ] No secrets committed (verify with: git log -p | grep -i secret)
   - [ ] GitHub Actions enabled
   - [ ] Producer is real GitHub user/organization
   ```

2. **GATE 2: Validation** (Lane 04)
   ```
   Checklist:
   - [ ] Schema compliance: rafaelia.federated-producer-receipt.v1
   - [ ] All 8 observations present
   - [ ] Immutability markers present (run_id, job_id, timestamp, received_at_utc)
   - [ ] Signature can be verified (with test key)
   - [ ] Timestamp freshness OK (< 24 hours)
   ```

3. **GATE 3: Integration Check** (Lane 06)
   ```
   Checklist:
   - [ ] No cascading gaps with existing producers
   - [ ] No policy conflicts
   - [ ] HMAC key can be generated and distributed securely
   - [ ] Approval template can be used (no conflicts)
   ```

4. **Authority Decision** (Lane 00)
   ```
   Decision options:
   - APPROVED_REGISTERED: Full production status
   - APPROVED_PROVISIONAL: Testing status (1 month, then re-evaluate)
   - CONDITIONAL: Approval requires remediation (specify deadline)
   - REJECTED: Does not meet requirements (explain why)
   ```

5. **Notification** (Lane 00)
   - Issue comment with decision
   - If approved: Start credential distribution (see below)
   - If rejected/conditional: Explain next steps

### Credential Distribution (After Approval)

**Owner**: Lane 00 Authority  
**Method**: Secure GitHub Issue (private, read-only to producer admin)

**Steps**:

1. **Generate HMAC key**
   ```bash
   openssl rand -hex 32 > /tmp/hmac-secret.txt
   ```

2. **Create secure issue**
   - Title: `[CREDENTIALS] HMAC Secret for [org]/[repo]`
   - Labels: `confidential`, `federated-producer`
   - Assignee: Producer admin (GitHub handle)
   - Body:
     ```
     Producer: [org]/[repo]
     Status: APPROVED_REGISTERED
     Generated: [date]
     
     1. HMAC Secret: [64-char hex from openssl]
     2. Store in GitHub Secrets as: RAFAELIA_HMAC_SECRET
     3. Broker endpoint: https://api.mapa.rafaelia/federated-receipts
     4. Never commit this secret to version control
     5. Notify us when stored: Reply to this issue
     
     See onboarding guide: https://github.com/rafaelmeloreisnovo/Mapa/docs/governance/FEDERATED_PRODUCER_ONBOARDING_V1.md
     
     SLA: Store secret within 24 hours, reply within 48 hours
     ```

3. **Wait for confirmation**
   - Producer replies when secret stored
   - Log confirmation to audit trail
   - Once confirmed: Mark as READY_FOR_EMISSION

4. **Revoke credential** (if needed):
   - Lane 00 can immediately deactivate key
   - Prevents further receipts with that key
   - Requires emergency rotation if in use

---

## Escalation Procedures

### Lane 04 → Lane 07 (Security Issue)

**Trigger**: Lane 04 detects security anomaly  
**Examples**:
- Signature verification failure (repeated)
- Unusual submission patterns
- Possible key compromise indicators

**Process**:
1. File issue: `[SECURITY] Escalation from Lane 04: [description]`
2. Label: `lane-07-security`, `escalation`
3. Lane 07 investigates and responds within 4 hours

### Lane 06 → Lane 00 (Policy Decision Needed)

**Trigger**: Lane 06 finds cascading gap or policy conflict  
**Examples**:
- Two producers with overlapping scope
- New federation policy affects existing producer
- Conditional approval deadline passed

**Process**:
1. File issue: `[GOVERNANCE] Escalation from Lane 06: [description]`
2. Label: `lane-00-governance`, `escalation`
3. Lane 00 issues decision within 24 hours

### Lane 04/07 → Lane 00 (Incident Response)

**Trigger**: Critical incident (key compromise, audit tampering)  
**SLA**: Immediate notification

**Process**:
1. Create incident issue immediately
2. Label: `incident`, `critical`
3. @-mention Lane 00 for immediate response
4. Do not resume federation operations until cleared by Lane 00

---

## Metrics & Dashboards

### Lane 04 Daily Metrics

```
Receipts validated (last 24h): X
Receipts rejected (last 24h): X
Validation success rate: X%
Average validation time: X seconds
```

### Lane 07 Weekly Metrics

```
HMAC signature verifications: X
Verification failures: X
Failure rate: X%
Key rotation events: X
Anomalies detected: X
```

### Lane 00 Monthly Metrics

```
New producers approved: X
Producers under conditional approval: X
Producers revoked: X
Decision SLA compliance: X%
Average approval time: X hours
```

### Observability (Lane 08)

Check dashboard at: `/monitoring/federated-receipts-dashboard` (implementation in Phase 2-P1-05)

Current metrics collected in: `data/audits/federated-receipts-audit.jsonl`

---

## Contact & Support

**Lane-specific contacts**:
- **Lane 00 (Governança)**: lane-00@mapa.rafaelia
- **Lane 04 (Validação)**: lane-04@mapa.rafaelia
- **Lane 06 (Integração)**: lane-06@mapa.rafaelia
- **Lane 07 (Segurança)**: lane-07@mapa.rafaelia
- **Lane 08 (Observabilidade)**: lane-08@mapa.rafaelia

**For questions**: Open issue in Mapa with label `federated-producer-support`

**For emergencies**: Send email to lane-00@mapa.rafaelia with `[URGENT]` prefix

---

## Appendix: Quick Reference Commands

```bash
# View recent receipts
tail -50 data/audits/federated-receipts-audit.jsonl | jq .

# Check HMAC key events
grep "RECEIPT_SIGNATURE" data/audits/hmac-key-audit.jsonl | tail -20

# Run audit aggregator
python3 tools/aggregate_federated_audits.py --format markdown

# Verify receipt
python3 tools/verify_cross_repo_provenance.py --receipt <path>

# Check broker workflow status
gh workflow view federated-receipt-broker.yml
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-08-21 | Initial operational procedures |
| | | Daily/weekly/monthly schedules |
| | | Incident response playbooks |
| | | Lane-specific procedures |
