# Brazil Platform Data Governance Overlay — Marco Civil + 2026 — V1

Snapshot: **2026-08-26**  
Parent canon: `docs/legal/GLOBAL_DATA_PRIVACY_GNSS_AI_GOVERNANCE_V1.md`  
Status: **REFERENCE / APPLICABILITY_REQUIRES_CASE_FACTS**  
`claim_allowed=false`

## 1. Marco Civil da Internet — Law 12.965/2014

Relevant privacy/platform nodes include:

- **Art. 7, I–III** — privacy and secrecy of internet communications / stored private communications within statutory limits.
- **Art. 7, VI** — clear/complete contractual information on protection of connection/application-access records and network-management practices.
- **Art. 7, VII** — non-disclosure to third parties of personal data and connection/application records except with the required consent or legal basis provided by law.
- **Art. 7, VIII** — clear and complete information on collection, use, storage, processing and protection of personal data, tied to justified, lawful and contract/terms-specified purposes.
- **Art. 7, IX** — highlighted express consent under the statutory wording, read today together with the LGPD rather than in isolation.
- **Art. 7, X** — deletion at the end of the relationship on request, subject to mandatory retention and LGPD rules.
- **Art. 10** — custody/disclosure of records, personal data and private communications must preserve intimacy, private life, honor and image; judicial-order and statutory-access distinctions apply.
- **Art. 11** — Brazilian-law/privacy/data-protection requirements for covered operations where at least one collection/storage/custody/processing act occurs in Brazil, under the provision's territorial criteria.
- **Art. 12** — sanctions for violations of Arts. 10 and 11 under the statute.

Primary source: https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm

## 2. Decree 8.771/2016 as amended by Decree 12.975/2026

Decree **12.975 of 20 May 2026** materially expands the current platform-governance context of the Marco Civil regulatory decree. Among the current nodes exposed in the official text:

- duties/procedures for custody and protection of data by connection/application providers;
- transparency measures concerning government requests and provider duty-of-care context;
- systemic-risk monitoring, identification, assessment and management for covered application providers;
- transparency reports, monitoring and management of systemic risks;
- user profiling, advertising and paid content boosting governance;
- permanent/easily accessible complaint channels and related procedural requirements;
- security and transparency measures;
- terms/conditions and self-regulation covering notification systems, due process and annual transparency reporting;
- ANPD regulatory/enforcement role for relevant user-right/provider-duty provisions, read with Marco Civil Arts. 10–12 and LGPD.

**Non-overclaim rule:** these 2026 duties are not a generic statute requiring an AI assistant to ingest every device sensor. Applicability depends on provider/service/function and the exact provision. They do strengthen the broader proposition that large platforms may face duties of transparency, risk governance, process and accountability.

Primary source: https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/d12975.htm

## 3. Decree 12.976/2026 — women in digital environments

Decree **12.976 of 20 May 2026** establishes guidelines for protecting women online and confronting digital violence. Its principles expressly include data protection/privacy, intimacy/private life/honor/image, victim centrality, evidence preservation and non-revictimization. This is a specialized protection layer, not a general GNSS statute.

Primary source: https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/d12976.htm

## 4. GNSS / AI intersection

For a platform-location feature in Brazil, assess together rather than independently:

`Constitution Art. 5-X/LXXIX`
→ `Marco Civil user rights + records/data rules`
→ `LGPD purpose/basis/necessity/transparency/security/accountability`
→ `ANPD regulations`
→ `2026 platform-governance duties when applicable`
→ `consumer-law truthfulness/service-defect analysis when applicable`
→ `actual product architecture + runtime receipt`.

This produces two symmetrical failure modes:

1. **OVER-COLLECTION:** raw GNSS is captured/shared despite no demonstrated necessity for the feature.
2. **MISREPRESENTATION/UNDER-DISCLOSURE:** the provider collects or uses location more precisely/broadly than represented, or markets a capability in a way inconsistent with actual architecture.

The inverse is not automatically unlawful:

`AI_NOT_RECEIVING_RAW_GNSS` can be a legitimate privacy/minimization design when the declared function only needs a final/coarse location.

## 5. Evidence gate

A Big Tech responsibility claim about a particular GNSS feature is promotable only when the record contains:

- product/version;
- jurisdiction and user context;
- permission state;
- actual fields collected;
- actual recipient/tool/model boundary;
- declared purpose;
- applicable legal basis;
- necessity/minimization analysis;
- retention/deletion behavior;
- third-party/cross-border path;
- user-facing notice/control;
- security controls;
- consumer-facing capability claim;
- falsifier and runtime receipt.

Absent any material field: `TOKEN_VAZIO`, not presumed compliance and not presumed violation.

### F_ok

Marco Civil and its 2026 platform-governance overlay are explicitly connected to the global privacy/GNSS/AI canon.

### F_gap

Case-specific applicability and runtime architecture remain product/fact dependent.

### F_next

Cross-reference this overlay from the semantic atlas on the next versioned append; do not rewrite prior historical normative batches.