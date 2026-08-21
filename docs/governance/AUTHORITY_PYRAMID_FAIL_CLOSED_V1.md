# RAFAELIA Authority Pyramid — Fail-Closed V1

Status: `CANONICAL_CANDIDATE / claim_allowed=false`

## Why this exists

A repository can have green tests and still be blocked by authority, privacy, security, compliance or evidence. A debugger can identify a symptom without owning the fix. A standard can describe good practice without proving conformance. A rollback can repair damage without proving prevention.

The pyramid makes those boundaries explicit.

## Authority pyramid

```text
L7 CLAIM PROMOTION
   ↑ only bounded evidence may pass
L6 EXECUTION EVIDENCE
   ↑ run / job / artifact / device / receipt
L5 PRODUCER AUTHORITY
   ↑ owning repository + exact ref/hash
L4 FEDERATED GOVERNANCE
   ↑ Mapa route/state/gap/receipt index
L3 TECHNICAL NORMATIVE REFERENCE
   ↑ NIST / OWASP / ISO / RFC within scope
L2 BINDING EXTERNAL AUTHORITY
   ↑ applicable law/regulation/private obligation
L1 PROTECTED-SUBJECT + CONTEXT INTEGRITY
   ↑ real subject/use/context, never stereotype
L0 OBSERVABLE REALITY / SILICON-RUNTIME FLOOR
   exact bits, artifact, OS, ABI, process, device when observable
```

“Silicon floor” here means the lowest **observable technical evidence layer** relevant to a computer/device claim. It does not mean that hardware observation overrides law, dignity or governance. If the hardware/runtime state cannot be observed, it remains `TOKEN_VAZIO`.

## No layer may impersonate another

```text
documentation != runtime
source identity != execution identity
hash != semantic correctness
CI != physical device
policy decision != server barrier
standard reference != certification
legal reference != legal applicability
best-interest review != compliance certificate
group label != cultural meaning
```

## Two-dimensional failure state

A finding has both an **evidence state** and an **attention state**.

Example:

```text
BUG_CONFIRMED + URGENT
TOKEN_VAZIO + FORGOTTEN_REDISCOVERED
PRIVACY_RISK + UNDERPRIORITIZED
SECURITY_WEAKNESS + BLOCKED_EXTERNAL
```

This prevents “ignored” from being mistaken for “false” and prevents “aborted” work from disappearing.

### Evidence-state vocabulary

`TOKEN_VAZIO`, `OBSERVED`, `PARTIAL`, `EVIDENCED_SCOPED`, `FAILURE`, `BUG_CONFIRMED`, `REGRESSION`, `SECURITY_WEAKNESS`, `VULNERABILITY_SUSPECTED`, `VULNERABILITY_CONFIRMED`, `PRIVACY_RISK`, `COMPLIANCE_GAP`, `GOVERNANCE_GAP`, `DEBUG_BLOCKER`, `NEAR_MISS`, `INCIDENT`, `SUPERSEDED`, `NOT_APPLICABLE_WITH_EVIDENCE`.

### Attention-state vocabulary

`ACTIVE`, `URGENT`, `IGNORED_DISCOVERED`, `FORGOTTEN_REDISCOVERED`, `UNDERPRIORITIZED`, `DEFERRED_WITH_OWNER`, `ABORTED_WITH_REASON`, `BLOCKED_EXTERNAL`.

## Priority

Priority ranks work; it does not increase truth.

```text
priority = impact × unblock × risk × urgency × information_gain × forgetting_risk
```

P0 privacy/security/governance/protected-subject blockers are **non-compensatory**. Twenty green unit tests cannot cancel one unresolved critical authorization or private-data boundary.

## Protected subjects, culture and dignity

The system must preserve context without stereotyping people or groups.

```text
child_status_unknown != adult
age_threshold != cultural_context_resolved
group_label != cultural_meaning
cultural_reference_missing -> TOKEN_VAZIO_CONTEXT
guardian_role != automatically_valid_consent
```

A person's culture, ethnicity, religion, family role, age or vulnerability must not be inferred from a repository name, group label, geography, device, user name or usage pattern.

When a real or potential child/vulnerable-subject use is established, the gate becomes P0 and requires purpose, data categories, flow, recipients, retention, minimization, transparency, authority/legal basis, best-interest review, jurisdiction, alternatives and receipt.

The African Charter, UN child-rights guidance, LGPD/ANPD and POPIA references in the normative graph are routing authorities within their respective scope. Their presence does not certify a repository.

## Debug route

```text
symptom
→ reproducible observation
→ owning component
→ exact repo/ref/path/hash
→ local falsifier
→ producer execution evidence
→ cross-repo edge evidence
→ receipt
→ federated state
→ bounded claim, if allowed
```

Stop at the first unresolved authority/evidence/privacy/security boundary and record a typed `TOKEN_VAZIO` rather than guessing.

## Minimum P0 triggers

Promotion is held when any of these is observed or gating state is unknown:

- secret/credential exposure;
- critical authorization/permission/bypass uncertainty;
- direct authoritative-branch mutation without demonstrated server rejection barrier;
- arbitrary command/IPC surface without bounded authorization and result-integrity evidence;
- raw VM/guest/user/device payload crossing a public receipt boundary;
- child/vulnerable-subject data with unresolved context/authority/best-interest gate;
- high-impact mutation without rollback;
- physical/runtime/security claim without the required exact device/artifact evidence.

## Producer adapters

The central contract does not copy local implementation authority. Each producer keeps a local adapter:

- RafGitTools: executor/debug/security routing;
- Vectras: VM/QEMU consumer, guest-data/privacy and IPC boundary;
- Termux RAFCODEΦ: Android runtime/provider, command/permission/bootstrap/runtime boundary.

A producer adapter may block a federated promotion. It cannot independently promote another producer's runtime truth.

## Normative evidence boundary

NIST Privacy Framework, NIST SSDF, OWASP MASVS and legal/human-rights sources are mapped as references. For every conformance/compliance claim require exact reference/version, applicable scope, implementation mapping, execution evidence, falsifier, receipt and independent/legal review where applicable.

## Falsifier

This architecture is violated if any lower unresolved layer is bypassed, an unknown becomes PASS, a protected/cultural attribute is inferred from a label, or a normative reference is presented as certification/compliance without the required scoped evidence.
