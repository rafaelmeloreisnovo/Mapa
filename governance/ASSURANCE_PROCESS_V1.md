# Assurance Process V1 — controls, evidence, risk and standards references

Status: `PROCESS_DRAFT / claim_allowed=false`

This document defines a working assurance process for Mapa. It does **not** claim
ISO, NIST, IEC, IEEE, IETF, W3C, legal, privacy, security, AI, accessibility, Six
Sigma, or other certification/compliance status.

## 1. Core invariant

```text
REFERENCE != DESIGNED != IMPLEMENTED != EVIDENCED != VERIFIED != EXTERNALLY_ASSESSED != CERTIFIED
TOKEN_VAZIO != PASS
CI_FAIL != MERGE_BLOCKED unless provider enforcement is active and evidenced
```

A standard, law, framework, RFC, guideline, audit method, scanner or checklist is a
`REFERENCE` until its applicability and the relevant control are mapped. A control
becomes `IMPLEMENTED` only when the implementation is observable. It becomes
`EVIDENCED` only when execution evidence exists. `VERIFIED` requires an appropriate
review distinct from the implementation claim. `CERTIFIED` is reserved for a real,
independently verifiable certification with exact issuer, scope, identifier and
validity.

## 2. Assurance state model

| State | Meaning | Minimum evidence |
|---|---|---|
| `REFERENCE` | external/internal source identified | source + edition/version when known |
| `DESIGNED` | control has an explicit objective and design | control statement + owner/gap + falsifier |
| `IMPLEMENTED` | implementation is observable | exact file/configuration/provider readback |
| `EVIDENCED` | control execution has evidence | test/run/receipt + time + subject/version |
| `VERIFIED` | evidence has appropriate independent review | reviewer/authority + review result |
| `EXTERNALLY_ASSESSED` | external party assessed exact scope | assessor + scope + report/receipt |
| `CERTIFIED` | valid certification exists | issuer + certificate id + scope + validity + verifiable source |
| `TOKEN_VAZIO` | required evidence is absent/unknown | gap + next verifiable step |

## 3. Control record

Every material control should be representable with at least:

```yaml
control_id: TOKEN_VAZIO
objective: TOKEN_VAZIO
risk_or_failure_mode: TOKEN_VAZIO
plausible_consequence: TOKEN_VAZIO
owner: TOKEN_VAZIO
control_statement: TOKEN_VAZIO
implementation_pointer: TOKEN_VAZIO
test_or_falsifier: TOKEN_VAZIO
evidence_pointer: TOKEN_VAZIO
state: TOKEN_VAZIO
residual_risk: TOKEN_VAZIO
review_or_expiry: TOKEN_VAZIO
rollback_or_disable_path: TOKEN_VAZIO
mappings: []
```

Mappings are many-to-many references; they do not duplicate controls and do not
create certification claims.

## 4. Risk and decision loop

```text
asset/process/data flow
  -> threat | failure mode | legal/privacy concern
  -> plausible consequence
  -> existing control
  -> evidence
  -> residual risk
  -> decision authority
  -> action: reduce | avoid | transfer | explicitly accept | TOKEN_VAZIO
  -> retest / review / CAPA
```

High-consequence uncertainty fails safe. Silence, inactivity and elapsed time are
not closure criteria.

## 5. Data and privacy loop

For each material personal/sensitive data flow, map:

```text
data
 -> source
 -> permission/access boundary
 -> purpose
 -> applicable authority/legal basis when required
 -> minimization
 -> destination/recipient
 -> retention/deletion
 -> transfer
 -> security controls
 -> data-subject/user rights path
 -> evidence
 -> falsifier
 -> gate
```

Sensitive evidence should remain in an access-controlled system of record. Public
repositories may retain safe receipts, hashes, identifiers or redacted summaries
instead of the sensitive payload itself.

## 6. Software and workflow supply chain

Minimum working controls:

1. external GitHub Actions use immutable full commit SHAs;
2. workflow permissions follow least privilege;
3. credentials are not persisted by checkout unless explicitly justified;
4. third-party scanners/services require target authorization and data-egress review;
5. dependency updates are inventoried and reviewed;
6. build/release provenance is distinguished from a security claim;
7. rollback/disable paths are documented for material automation;
8. provider-side enforcement is proven by provider readback, not inferred from YAML.

## 7. Audit and improvement loop

Use an evidence-oriented improvement cycle compatible with internal audit and DMAIC
thinking:

```text
DEFINE  -> control objective + consequence
MEASURE -> observable evidence and baseline
ANALYZE -> cause, gap, false positive/negative, applicability
IMPROVE -> smallest reversible control change
CONTROL -> regression gate + owner + review/expiry
```

A failed control or audit finding may open CAPA. Closure requires evidence of the
specified closure criterion and, where appropriate, a negative fixture proving the
failure path is blocked.

## 8. Standards and framework families used as references

The following families may be mapped when applicable. Exact editions, clauses and
jurisdiction/applicability must be recorded in the control or standards registry;
the list below is not a claim of conformity.

- ISO/IEC 27000 family — information security and risk;
- ISO/IEC 27701 — privacy information management;
- ISO 8000 family — data quality and master data;
- ISO 9001 — quality management;
- ISO 19011 — management-system auditing guidance;
- ISO 31000 — risk management guidance;
- ISO 37301 — compliance management;
- ISO 22301 — business continuity;
- ISO/IEC 38500 — governance of IT;
- ISO/IEC 42001 and ISO/IEC 23894 — AI management/risk when AI is actually in scope;
- NIST Cybersecurity Framework, Privacy Framework, SP 800-53 and SSDF;
- NIST AI RMF when AI risk is actually in scope;
- IEC standards when the actual hardware/electrotechnical domain makes them applicable;
- IETF RFCs for Internet protocols, formats and normative protocol language;
- W3C standards for Web, semantic data and accessibility when applicable;
- IEEE standards, including relevant software/AI/ethics families when applicable;
- OWASP guidance for application/API security as a technical reference;
- Six Sigma/DMAIC as an improvement method, not a certification claim;
- applicable constitutions, laws, regulations and competent-authority acts, separated
  from voluntary standards and internal policy.

## 9. Provider enforcement boundary

Repository files can detect and document controls but cannot, by themselves, prove
that GitHub will block a merge. Canonical branch/ruleset enforcement remains a
provider-side control and requires authoritative readback plus, when feasible, a
negative merge-blocking receipt.

Until that evidence exists:

```text
provider_enforcement = TOKEN_VAZIO or NOT_ENFORCED (according to current readback)
claim_allowed = false
promotion_allowed = false for claims that depend on that enforcement
```

## 10. Review rule

Every standards mapping must answer four questions:

1. Why is this reference applicable to this exact process/data/system?
2. Which internal control implements the relevant objective?
3. What evidence would falsify or support the implementation claim?
4. Who is authorized and sufficiently independent to review that evidence?

If any required answer is unknown, preserve `TOKEN_VAZIO` and record the next
verifiable step rather than inventing closure.
