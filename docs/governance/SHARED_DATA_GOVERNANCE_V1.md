# RAFAELIA Shared Data Governance V1

**State:** `CANONICAL_DRAFT / PRIVATE_BY_DEFAULT / FAIL_CLOSED / APPEND_ONLY`  
**Date:** 2026-08-21  
**Certification claim:** `false`

## Boundary

This contract adopts practices inspired by security, privacy, data-quality and quality-management standards. It does **not** claim external audit, certification, legal compliance, or complete implementation of any standard.

`standard_reference != implementation != execution != evidence != certification`

## Drive authority

Governed Drive root:

- `[C1_INTERNAL] RAFAELIA_DADOS_COMPARTILHADOS_GOVERNADOS_V1`
- folder id: `1U3G5dJwcbGxGWaSPu3WbH1WI1-Jeyi7x`

Shared-data subtree:

- `[C1_INTERNAL] DADOS_COMPARTILHADOS`
- folder id: `1pOQ68FarWfRmY6hiG4_9F2X0UrnG0pI2`

The names express **classification eligibility**, not actual sharing permissions. No folder is treated as public merely because its prefix is `C0_PUBLIC`.

## Criticality

| Level | Meaning | Automated raw handoff |
|---|---|---|
| `C0_PUBLIC` | approved-for-release candidate | allowed only with manifest/hash/gate |
| `C1_INTERNAL` | internal metadata, manifests, indices | bounded object only; no broad crawl |
| `C2_SENSITIVE` | requires minimization/redaction and risk assessment | raw source prohibited |
| `C3_RESTRICTED` | personal/sensitive/correlatable/high-impact context | raw source prohibited; human gate |
| `C4_CRITICAL` | credentials, secrets, keys, highly identifying or high-impact material | **prohibited**; pointer/hash/approved metadata only |

## Core invariants

1. private by default;
2. fragmentation is not anonymization;
3. hash is not authorization;
4. isolated fragments may become identifying or sensitive after correlation;
5. inference may locate a candidate source but cannot promote a release;
6. high-impact unknowns remain `TOKEN_VAZIO` and block release;
7. purpose, recipient, scope and retention must be explicit;
8. downstream copies, caches, forks, logs and artifacts are part of the impact radius;
9. revocation records a new effective state and never rewrites historical receipts;
10. `claim_allowed=false` is preserved for certification/compliance claims.

## Share Impact Envelope

Every governed release binds at least:

`share_id -> source locator/revision -> authority -> criticality -> data classes -> purpose -> recipient -> selected fields -> minimization/redaction -> reidentification risk -> semantic/correlation risk -> cascade/blast radius -> TTL -> revocation -> human awareness -> approval -> evidence -> receipt`

For `C2+`, `TOKEN_VAZIO` in reidentification risk or semantic reconstruction risk blocks release.

## Release lane

`DISCOVER -> BIND_SOURCE -> CLASSIFY -> PURPOSE -> MINIMIZE -> REDACT -> REIDENTIFICATION_TEST -> SEMANTIC_CORRELATION_TEST -> CASCADE_MAP -> HUMAN_AWARENESS -> APPROVE -> MATERIALIZE_FRAGMENT -> HASH -> HANDOFF -> MONITOR -> EXPIRE/REVOKE -> RECEIPT`

## GitHub Actions boundary

`DRIVE_BRIDGE_ENABLED=false` by default.

Actions must **not** enumerate Drive broadly. The first implementation validates only local/synthetic manifests. A future Drive bridge must consume only explicitly exported objects from the handoff zone and must use separately configured least-privilege identity/secret handling.

C4 bytes are never accepted by the automated handoff.

## Human-awareness requirement

The release summary distinguishes:

- `OBSERVED` — directly evidenced;
- `ESTIMATED` — derived by declared method;
- `HYPOTHESIS` — plausible but not proven;
- `UNKNOWN/TOKEN_VAZIO` — not known.

`unknown_effect != zero_risk`

Awareness includes foreseeable downstream effects and explicitly states that unknown future correlations cannot be guaranteed absent.

## Six Sigma DMAIC control loop

### Define

Purpose, consumer, process boundary, criticality and CTQs for privacy/security/data quality.

### Measure

Count actual selected files/fields, destinations, TTL, redaction tests, blocked releases, incidents, unresolved `TOKEN_VAZIO`, revocations and provenance coverage. Missing baselines remain `TOKEN_VAZIO`.

### Analyze

Use causal analysis/FMEA-style reasoning for leakage, reidentification, semantic reconstruction, structural disclosure and downstream blast radius.

### Improve

Minimize fields, partition bundles, redact/pseudonymize when suitable, reduce privileges/TTL, isolate destinations and strengthen negative tests.

### Control

CI gates, schemas, immutable hashes, append-only receipts, expiry/revocation, periodic reassessment and anti-regression fixtures.

## Reference set — practices, not certification

Observed official/current references on 2026-08-21:

- NIST Cybersecurity Framework 2.0;
- NIST SP 800-53 Rev. 5 security/privacy control catalog;
- NIST SP 800-122 PII confidentiality guidance;
- NIST Privacy Framework 1.0 final; Privacy Framework 1.1 tracked as an evolving draft/IPD;
- ISO/IEC 27001:2022 ISMS requirements;
- ISO/IEC 27002:2022 information-security controls guidance;
- ISO/IEC 27701:2025 privacy information management requirements/guidance;
- ISO 8000-8:2015 data-quality concepts and measurement prerequisites;
- ISO 8000-61:2016 data-quality management process reference model;
- ISO 8000-150:2022 data-quality roles and responsibilities;
- ISO 9001:2015 + Amd 1:2024 remains the current published edition as of this date; Edition 6 is under publication and expected to replace it in September 2026, so the reference must be revalidated before future canonical promotion;
- Brazilian LGPD and ANPD privacy/security guidance where applicable to the concrete processing context.

## Stop rule

Do not release because a fragment “looks harmless.” Stop when the gate requires a fact that is not known. Record `TOKEN_VAZIO + F_next`.

A new release cycle is required if source revision, purpose, recipient, transformation, policy, criticality, TTL or downstream route changes.
