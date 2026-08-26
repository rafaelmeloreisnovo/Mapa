# GLOBAL DATA PRIVACY · GNSS · AI GOVERNANCE — V1

**RAFAELIA / Mapa — evidence-first legal-semantic canon**  
Snapshot: **2026-08-26 (America/Sao_Paulo)**  
Status: **REFERENCE / HUMAN_REVIEW_REQUIRED**  
`claim_allowed=false`

> This document is a legal-governance research map, not a certification of compliance and not individualized legal advice. It separates binding law, constitutional doctrine, regulatory acts, case law, executive/national-security policy, voluntary standards, contracts, project policy and unresolved hypotheses.

## 0. Core invariants

1. `law != regulation != case_law != executive_policy != standard != contract != project_policy`.
2. `data_exists_on_device != AI_has_access_to_data`.
3. `OS_PERMISSION != LAWFUL_BASIS`.
4. `USER_CONSENT != UNIVERSAL_LAWFUL_BASIS`.
5. `SENSOR_CAPABILITY != PROVIDER_DUTY_TO_EXPOSE_RAW_TELEMETRY`.
6. `TRANSPARENCY != RAW_DATA_PASSTHROUGH`.
7. `ACCESS_RIGHT != REAL_TIME_SENSOR_API_ENTITLEMENT`.
8. `PORTABILITY != UNBOUNDED_INTEROPERABILITY`.
9. `MINIMIZATION + NECESSITY` may support **not** exposing raw GNSS telemetry when the declared purpose does not require it.
10. Precise geolocation is personal/high-risk data in multiple regimes; its exact statutory classification differs by jurisdiction.
11. `GNSS_FIX != GNSS_RAW_MEASUREMENTS != SATELLITE_STATUS != NMEA != DEVICE/NETWORK GEOLOCATION`.
12. `CIVIL_GPS_OPEN_SERVICE != MILITARY_GPS_SERVICE != EXPORT-CONTROLLED_GNSS_TECHNOLOGY`.
13. `EMBARGO_OR_SANCTIONS != AUTOMATIC_SHUTDOWN_OF_CIVIL_GPS_SIGNAL`.
14. `NATIONAL_SECURITY_EXCEPTION != BLANKET_PRIVACY_WAIVER`.
15. Constitutional restraints on government are not automatically identical to duties imposed on a private platform.
16. `BIG_TECH_ACCOUNTABILITY != GENERAL_DUTY_TO_DELIVER_ALL_AVAILABLE_DEVICE_DATA_TO_AI`.
17. `claim != evidence`; `absence_of_evidence != evidence_of_absence`.
18. `TOKEN_VAZIO` is a valid, auditable state when authority, applicability, interpretation or implementation evidence is missing.

## 1. GNSS / location data taxonomy

Potential device-side GNSS surfaces, when hardware + OS + permission + API permit, include:

- final fix: latitude, longitude, altitude, time, speed, bearing, horizontal/vertical accuracy;
- receiver/fix status and TTFF;
- constellation and satellite identifiers (GPS, Galileo, GLONASS, BeiDou, QZSS, SBAS, NavIC where supported);
- satellites visible/tracked/used-in-fix;
- C/N0, azimuth, elevation, carrier frequency and, on supported devices, baseband C/N0;
- NMEA messages (for example GGA/GSA/GSV/RMC when exposed);
- raw GNSS measurements on supported Android devices: clock data, pseudorange-related observables, pseudorange rate/Doppler-related data, accumulated delta range/carrier-phase-related observables, multipath state and uncertainty fields.

**Governance rule:** the fact that Android/GNSS can expose a field does not prove that a given AI product receives it. Product access requires a separate technical and legal path: `hardware -> OS/API -> permission -> app/service -> declared purpose -> lawful basis -> minimization -> transfer/security -> AI context`.

## 2. Brazil — constitutional + LGPD + ANPD layer

### 2.1 Constitution of the Federative Republic of Brazil

Privacy/data-governance anchors to map together, without treating them as synonyms:

- **Art. 1, III** — dignity of the human person.
- **Art. 5, X** — intimacy, private life, honor and image; compensation for violation.
- **Art. 5, XII** — secrecy of correspondence and communications/data communications within its constitutional contours; do not reduce this provision to a universal rule for every database operation.
- **Art. 5, XXXIII** — access to information from public bodies, subject to constitutionally protected secrecy.
- **Art. 5, LXXII** — habeas data.
- **Art. 5, LXXIX** — fundamental right to protection of personal data, including in digital media, inserted by EC 115/2022.
- **Art. 21, XXVI** — Union competence to organize and supervise protection and processing of personal data.
- **Art. 22, XXX** — Union’s private legislative competence over protection and processing of personal data.
- **Art. 37** — public-administration legality, impersonality, morality, publicity and efficiency; relevant when public-sector data governance is involved.

### 2.2 LGPD — Law 13.709/2018, consolidated

**Integral article index (1–65) by function:**

- **Arts. 1–4** — purpose, foundations, territorial/extraterritorial scope and exclusions. Art. 4 national/public security exceptions do not erase constitutional safeguards; the statute itself requires specific legislation with proportionality/necessity protections for those contexts.
- **Art. 5** — definitions: personal data, sensitive personal data, anonymized data, database, controller, processor, DPO/encarregado, processing, consent, blocking, deletion, transfer, shared use, impact report, research body and national authority.
- **Art. 6** — principles: purpose, adequacy, necessity, free access, data quality, transparency, security, prevention, non-discrimination and accountability/demonstration.
- **Arts. 7–10** — lawful bases, consent, information/transparency and legitimate interest.
- **Arts. 11–13** — sensitive personal data, anonymization/research-related treatment rules.
- **Art. 14** — children and adolescents.
- **Arts. 15–16** — termination and retention after termination in statutory cases.
- **Arts. 17–22** — data-subject rights, confirmation/access, correction/deletion/portability where applicable, automated decision review/information under the current statutory text, and judicial protection.
- **Arts. 23–32** — treatment by public authorities, public purpose, shared use, disclosure/communication conditions, supervisory powers and correction of irregular treatment.
- **Arts. 33–36** — international transfers and mechanisms/adequacy/contractual safeguards.
- **Arts. 37–40** — processing records, data-protection impact report, processor instructions and interoperability/standards-related governance.
- **Art. 41** — DPO/encarregado.
- **Arts. 42–45** — liability, exclusions, irregular processing and consumer-law relationship.
- **Arts. 46–49** — security, confidentiality duty, incident communication and systems structured to meet security/governance requirements.
- **Arts. 50–51** — governance programs, good practices, rules and technical standards.
- **Arts. 52–54** — administrative sanctions and procedural parameters.
- **Arts. 55-A–55-L** — ANPD institutional regime and powers, as amended; read together with Law 15.352/2026 and current ANPD institutional acts.
- **Arts. 58-A–58-B** — National Council for Personal Data Protection and Privacy and its competences.
- **Art. 59** — vetoed.
- **Arts. 60–65** — changes to Marco Civil, foreign-company service of process, specific education-data regulation, legacy database adaptation, cumulative rights/treaties and commencement.

**GNSS consequence under LGPD:** geolocation tied or reasonably linkable to a natural person is personal data. Precise, persistent or inferential location can raise risk substantially. A controller that actually collects/processes it needs purpose, applicable legal basis, necessity, transparency, security, retention/rights handling and, where relevant, impact assessment/transfer safeguards. There is **no general LGPD rule requiring a platform or AI provider to feed raw satellite telemetry to an AI simply because the handset can produce it**.

### 2.3 Current ANPD regulatory layer

At this snapshot, map at minimum:

- Res. CD/ANPD **15/2024** — communication of security incidents.
- Res. CD/ANPD **18/2024** — DPO/encarregado.
- Res. CD/ANPD **19/2024** — international transfers and standard contractual clauses; rectified in 2025.
- Res. CD/ANPD **30/2025** — priority themes 2026–2027.
- Res. CD/ANPD **32/2026** — recognition of EU adequacy for LGPD transfer purposes.
- Law **15.352/2026**, Decree **12.881/2026** and Res. **33/2026** — ANPD as a regulatory agency and its current institutional structure.
- Law **15.211/2025 (ECA Digital)**, effective 17 March 2026, when children/adolescents are implicated.

**Big Tech / AI rule for this atlas:** responsibility is claim-specific: collection, notice, purpose, legal basis, minimization, security, retention, rights, automated processing, consumer representations, cross-border transfer and incident response. `WITHHOLDING_UNUSED_RAW_GNSS` may be privacy-protective; `CLAIMING_PRECISE_GPS_WHILE_ONLY_USING_COARSE_LOCATION` may instead create transparency/consumer-protection questions. Both require evidence of the actual product architecture.

Primary anchors:
- https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm
- https://planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc115.htm
- https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd
- https://www.gov.br/anpd/pt-br/assuntos/assuntos-internacionais/transferencia-internacional-de-dados
- https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/lei/l15352.htm

## 3. European Union — GDPR + ePrivacy + AI Act

### 3.1 GDPR — Regulation (EU) 2016/679

Article map for this problem:

- **Arts. 4–5** — definitions and principles (lawfulness/fairness/transparency; purpose limitation; minimization; accuracy; storage limitation; integrity/confidentiality; accountability).
- **Arts. 6–7** — lawful bases and consent conditions.
- **Art. 9** — special categories. **Location data is not automatically an Art. 9 special category**, but location can reveal/infer health, religion, political activity or other protected attributes, changing risk and legal analysis.
- **Arts. 12–22** — transparency and data-subject rights, including access, rectification, erasure, restriction, portability, objection and safeguards around solely automated decisions under Art. 22.
- **Arts. 24–25** — controller accountability and data protection by design/default.
- **Arts. 26, 28, 30** — joint controllers, processors and records.
- **Arts. 32–34** — security and breach duties.
- **Art. 35** — DPIA where processing is likely to create high risk.
- **Arts. 37–39** — DPO.
- **Arts. 44–49** — international transfers.
- **Arts. 82–83** — compensation/liability and administrative fines.

### 3.2 ePrivacy Directive 2002/58/EC

**Art. 9** specifically regulates location data other than traffic data in the electronic-communications context: processing generally requires anonymization or consent and must be limited to what is necessary for the value-added service, with prior information and withdrawal/refusal mechanisms. Applicability is service/context-specific; it is not a generic GNSS sensor statute for every app.

### 3.3 EU AI Act — Regulation (EU) 2024/1689

The AI Act entered into force in 2024 and, as of **2 August 2026**, major enforcement powers and Article 50 transparency obligations are active, with transitional exceptions for some categories. The AI Act is risk-based and complements—not replaces—GDPR/ePrivacy. It does **not** create a right for an AI model to ingest every sensor accessible to a device.

Primary anchors:
- https://eur-lex.europa.eu/eli/reg/2016/679/oj
- https://eur-lex.europa.eu/eli/dir/2002/58/oj
- https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai

## 4. United States — constitutional limits, consumer protection, national security and transfers

### 4.1 Constitution

- **First Amendment:** protects speech, press, assembly, petition and religion; Supreme Court doctrine recognizes associational privacy where compelled disclosure by government can chill association (e.g. NAACP v. Alabama). This is **not** a general consumer-data statute binding every private platform as if it were the government.
- **Fourth Amendment:** central constitutional node for government acquisition/search of location information. **Carpenter v. United States (2018)** held that government acquisition of the historical CSLI at issue was a search and generally required a warrant supported by probable cause; the Court deliberately did not decide every future location/surveillance scenario.
- **Fifth Amendment:** due process constrains the federal government; the Supreme Court has in informational-privacy cases sometimes assumed, without definitively deciding, a constitutional informational privacy interest. It should not be represented as a comprehensive U.S. data-protection right equivalent to LGPD/GDPR.
- **Fourteenth Amendment:** due process/equal protection constraints apply to states; informational-privacy doctrine remains bounded and unsettled.

**State-action invariant:** `CONSTITUTIONAL_RIGHT_AGAINST_GOVERNMENT != AUTOMATIC_PRIVATE_PLATFORM_DUTY`.

### 4.2 Federal/state privacy and consumer governance

- **FTC Act §5:** unfair/deceptive practices authority is a major federal enforcement route for privacy/security representations and harmful data practices. FTC cases against Mobilewalla and other location-data actors demonstrate that sensitive/precise location practices can create substantial enforcement risk.
- Sectoral federal regimes also matter by context (e.g. COPPA, GLBA, HIPAA-related covered contexts, FCRA, communications/surveillance statutes).
- **California CCPA/CPRA:** precise geolocation is treated as sensitive personal information within that regime, with statutory rights/limits that are California-specific.
- **NIST Privacy Framework / NIST AI RMF:** valuable governance frameworks, but voluntary frameworks are not automatically binding law.

### 4.3 EU–U.S. transfer architecture

Semantic lineage:

`Safe Harbor (invalidated 2015) -> Privacy Shield (invalidated 2020) -> EO 14086 safeguards + DPRC (2022) -> EU–U.S. Data Privacy Framework adequacy (2023)`.

The **Data Protection Review Court (DPRC)** is part of a two-level U.S. redress mechanism for qualifying complaints concerning U.S. signals-intelligence collection. Participating U.S. companies in the DPF self-certify; misrepresentations/noncompliance can trigger FTC §5 enforcement. This may be one of the “agreements” remembered in the originating conversation; exact intended reference remains `TOKEN_VAZIO_LITERAL`.

### 4.4 EO 14117 / DOJ Data Security Program (DSP)

Effective **8 April 2025**, the DOJ Data Security Program establishes restrictions described by DOJ as effectively export-control-like for certain transactions giving countries of concern or covered persons access to U.S. Government-related data or Americans’ bulk sensitive personal data, including **geolocation**. Countries of concern currently identified by DOJ include **China (including Hong Kong and Macau), Russia, Iran, North Korea, Cuba and Venezuela**.

This is a direct legal bridge:

`privacy -> data governance -> cross-border transfer -> national security -> AI/military inference risk`.

Consent does not universally override these national-security restrictions.

Primary anchors:
- https://constitution.congress.gov/
- https://www.justice.gov/nsd/data-security
- https://www.justice.gov/opcl/executive-order-14086
- https://www.ftc.gov/business-guidance/privacy-security/data-privacy-framework

## 5. DeepSeek — what the U.S. actually assumed/responsibly restricted

As of this snapshot:

1. **Pub. L. 119-60, div. F, title LXVI, §6604 (18 Dec 2025)** requires the DNI to develop standards/guidelines requiring removal of DeepSeek (or successor application/service) from **national security systems of the intelligence community**, with national-security/research exceptions plus risk-mitigation standards.
2. U.S. House committees opened/continued 2026 investigations concerning national-security/cybersecurity risks of PRC AI models, including DeepSeek.
3. This is **not equivalent to a universal U.S. civilian ban on DeepSeek**.
4. Reuters reported on 17 June 2026 that Commerce had **held off** placing DeepSeek and more than 100 other firms on the Entity List despite prior interagency approval. Therefore `DEESEEK_IS_ON_ENTITY_LIST` must remain **FALSE/NOT_SUPPORTED at this snapshot**, not inferred from proposals or investigations.

**Governance analogy:** the U.S. response illustrates risk-based procurement/system-access controls for sensitive national-security environments. It does not establish a reciprocal legal duty for a U.S. Big Tech platform to expose raw GNSS telemetry to an AI assistant.

Primary anchors:
- https://uscode.house.gov/ (Pub. L. 119-60 §6604 note)
- https://homeland.house.gov/2026/04/29/chairmen-garbarino-moolenaar-announce-joint-investigation-into-national-security-risks-posed-by-prc-ai-models/

## 6. GPS as civil infrastructure + military capability

The GPS governance stack is dual-use:

- In **1983**, following the Korean Air Lines 007 tragedy, President Reagan committed to worldwide civil availability of GPS when operational; official U.S. historical materials describe this as a civil-access guarantee.
- In **2000**, the U.S. discontinued global **Selective Availability (SA)**. Official GPS policy says SA is not intended to be reactivated; SA itself was global degradation, not a regional switch.
- U.S. policy nevertheless preserves **localized denial/jamming capability against hostile use**, designed not to unduly disrupt civil/commercial access outside the area of military operations.
- The **2004 U.S.–EC GPS/Galileo cooperation process/agreement** established interoperability/open-service principles, non-discrimination and an agreement not to restrict end-user access to respective open services while preserving national-security capabilities.
- The 2004 U.S. PNT policy calls for continuous worldwide civil PNT service free of direct user fees and open access to information needed to build civil receivers, while sensitive/advanced PNT technologies may remain subject to ITAR/EAR/export-control rules.

Therefore:

`CUBA_EMBARGO != GPS_SIGNAL_PROHIBITED_IN_CUBA`.

A Cuban user receiving an open civil GPS signal is conceptually distinct from export/re-export of controlled military, anti-jam, high-performance or otherwise restricted PNT technology. Separate sanctions/export-control analysis is required for hardware/software transactions.

Primary anchors:
- https://www.gps.gov/policies-and-documentation
- https://archive.gps.gov/policy/docs/2004/
- https://archive.gps.gov/policy/cooperation/europe/2004/joint-statement/

## 7. China

**Personal Information Protection Law (PIPL)** nodes relevant here:

- purpose/necessity, transparency and accountability principles across the statute;
- **Art. 23** — providing personal information to another processor requires notice and separate consent in the described conditions;
- **Art. 24** — automated decision-making transparency, fairness/impartiality, alternatives/refusal mechanisms for targeted marketing and rights concerning decisions with significant impact;
- **Arts. 28–30** — sensitive personal information; Art. 28 expressly includes a person’s **whereabouts** and requires specific purpose, necessity and strict protective measures; separate consent is generally required under Art. 29;
- cross-border transfer mechanisms and security-assessment/localization rules apply by category/context;
- **Art. 58** — enhanced governance obligations for very large/complex internet platforms.

Use alongside the Data Security Law, Cybersecurity Law and current CAC cross-border data-flow provisions. Do not translate Chinese concepts into GDPR labels as if the statutes were identical.

Primary anchor:
- https://en.spp.gov.cn/2021-12/29/c_948419.htm

## 8. Russia

Core node: **Federal Law No. 152-FZ on Personal Data**, with later amendments.

- Russian personal-data law contains consent/processing, security, data-subject and cross-border/localization mechanisms that must be mapped from the current official text rather than assumed equivalent to GDPR.
- **Federal Law No. 23-FZ of 28 Feb 2025** amended 152-FZ and related laws; from the current text, collection of Russian citizens’ personal data through the Internet may not use databases located outside Russia for recording/systematization/accumulation/storage/clarification/extraction, subject to statutory exceptions.
- Further 2026 cross-border amendments were detected during research but the exact consolidated impact requires article-level Russian-language legal review before a stronger claim: `TOKEN_VAZIO_RU_2026_CONSOLIDATED_CROSS_BORDER`.

Primary anchors:
- https://government.ru/docs/all/98196/
- https://publication.pravo.gov.ru/document/0001202502280034

## 9. Cuba

Cuba is not a privacy-law void:

- The 2019 constitutional order contains privacy/dignity/communications and data-control guarantees that should be mapped from the official final constitutional text, not from embargo assumptions.
- **Law 149/2022 on Personal Data Protection**, published in Gaceta Oficial Ordinary Edition No. 90, establishes protection for personal data in public/private, physical/digital records and rights concerning access, correction, rectification, modification, updating/cancellation and improper/unauthorized use.
- Cuban cybersecurity/telecommunications rules coexist with this data-protection layer.
- U.S. sanctions/embargo rules and U.S. DOJ DSP country-of-concern treatment are a **different legal axis** from Cuba’s internal privacy law and from reception of the civil GPS signal.

Primary contextual anchor:
- https://www.granma.cu/cuba/2022-08-25/publican-en-la-gaceta-oficial-la-ley-de-proteccion-de-datos-personales-25-08-2022-10-08-45

`TOKEN_VAZIO_CUBA_OFFICIAL_FINAL_CONSTITUTION_ARTICLE_CROSSWALK`: validate exact final 2019 article numbering from an authoritative current constitutional publication before encoding article-by-article citations in a binding-law registry.

## 10. International / standards layer

Map separately from domestic law:

- **UDHR Art. 12** and **ICCPR Art. 17** — international privacy anchors, with treaty/applicability/enforcement analysis dependent on the state and legal context.
- **OECD Privacy Guidelines** — collection limitation, data quality, purpose specification, use limitation, security safeguards, openness, individual participation and accountability.
- **NIST Privacy Framework** and **NIST AI RMF** — voluntary risk-management frameworks unless incorporated by a specific authority/contract/procurement regime.
- **ISO/IEC 27001:2022** — information security management system standard; voluntary unless incorporated.
- **ISO/IEC 27701:2025 (Edition 2)** — privacy information management system standard. Important version-control note: do not freeze the old 2019 edition as if current.

`STANDARD != LAW`; conformance/certification requires scope + control + implementation + test + evidence, not citation alone.

## 11. Big Tech responsibility matrix for GNSS-to-AI

| Gate | Question | Evidence required | Default if absent |
|---|---|---|---|
| Capability | Can device/OS expose the GNSS field? | OS/API/hardware evidence | TOKEN_VAZIO |
| Collection | Does the app/service actually collect it? | runtime/network/log evidence | TOKEN_VAZIO |
| Purpose | Why is it collected? | product notice/spec/DPIA/RIPD | TOKEN_VAZIO |
| Legal basis | What permits processing? | jurisdiction-specific basis | TOKEN_VAZIO |
| Necessity | Is raw telemetry needed, or is coarse/final location enough? | minimization analysis | FAIL_CLOSED |
| Permission | Did OS/user grant access? | permission state | not sufficient alone |
| AI boundary | Is the data injected into model context, used in a tool, or retained outside the model? | architecture + receipts | TOKEN_VAZIO |
| Transfer | Does it cross controller/vendor/country boundaries? | data-flow map + contracts/transfer mechanism | TOKEN_VAZIO |
| Security | Encryption/access/logging/retention/deletion? | control evidence | TOKEN_VAZIO |
| Rights | Can subject access/correct/delete/object/limit where law grants it? | operational workflow | TOKEN_VAZIO |
| Claim | Does UI/marketing accurately state precision/access? | UI + policy + runtime comparison | HUMAN_REVIEW |
| National security | Is use restricted by sanctions/export/data-security rules? | applicable-law matrix | HOLD if high-risk |

### Resulting legal proposition

There is **no verified cross-jurisdictional invariant that forces a Big Tech AI assistant to ingest every GNSS metric available on the user’s handset**. The stronger cross-jurisdictional invariant is almost the reverse:

`collect/use/share only what is authorized + necessary + transparent + secured + accountable for the declared purpose`.

A provider may nevertheless incur responsibility if it **does** collect location improperly, misrepresents what it collects/can access, fails to protect it, unlawfully transfers it, uses it beyond purpose, denies statutory rights, or designs a feature whose promised function cannot be reconciled with its actual data path.

## 12. Seven-axis semantic topology (Ω7)

For each legal/technical node create seven projections:

1. **IDENTITY** — who is controller/processor/provider/deployer/state/subject?
2. **EPISTEMIC** — observation, claim, law, interpretation, hypothesis, falsifier?
3. **EXECUTION** — what data actually flows at runtime?
4. **SAFETY/SECURITY** — what harm, inference or hostile-use surface exists?
5. **PRIVACY** — purpose, basis, minimization, rights, retention, transfer?
6. **AUTHORITY** — which jurisdiction/source/version binds whom?
7. **TRANSITION** — what evidence authorizes movement from `TOKEN_VAZIO -> OBSERVED -> VERIFIED -> CLAIM_ALLOWED`?

Cross-relations to encode:

`GNSS -> precise_location -> personal_data -> inference -> AI_context -> transfer -> sovereignty/national_security`  
`constitutional_right -> state_action -> remedy`  
`privacy_statute -> controller_duty -> processor_contract -> technical_control -> receipt`  
`open_civil_signal -> receiver_capability -> OS_permission -> application_access -> AI_tool_access`  
`sanction/export_control -> technology_or_transaction_scope != civil_signal_availability`.

## 13. Falsifiers / negative tests

Reject any assertion that:

- a phone’s ability to expose satellite status proves ChatGPT/another AI receives it;
- a user granting Android location permission automatically establishes every privacy-law basis;
- GDPR/LGPD creates a general obligation to provide raw GNSS channels to an AI;
- the First or Fifth Amendment directly turns every private platform into a U.S. state actor;
- Cuba’s embargo means GPS civil signals are necessarily disabled there;
- DeepSeek is generally banned for all U.S. civilian use;
- DeepSeek is on the Commerce Entity List without current listing evidence;
- a cited ISO/NIST standard proves certification/compliance;
- national-security exceptions erase necessity, authorization and scope analysis;
- `TOKEN_VAZIO == FALSE`.

## 14. Open gaps / TOKEN_VAZIO

- `TOKEN_VAZIO_LITERAL`: exact referent of the user phrase remembered as “acordo no tempo de psic”. Candidate nodes: 1983 civil GPS commitment; 2004 GPS–Galileo; 2022 EO 14086/2023 EU–U.S. DPF.
- `TOKEN_VAZIO_PRODUCT_ARCHITECTURE`: exact GNSS fields, if any, exposed by the current ChatGPT Android product path to the assistant/model/tool layer.
- `TOKEN_VAZIO_BIGTECH_CONTRACT`: product-specific Terms/Privacy commitments for the exact service/version need a separate current contract audit.
- `TOKEN_VAZIO_RU_2026_CONSOLIDATED_CROSS_BORDER`: complete article-level effect of July 2026 Russian amendments.
- `TOKEN_VAZIO_CUBA_OFFICIAL_FINAL_CONSTITUTION_ARTICLE_CROSSWALK`: authoritative final article numbering/source validation.
- `TOKEN_VAZIO_SECTORAL_US`: exact sector-specific U.S. law depends on data/use/actor (health, finance, child, telecom, employment, etc.).

## 15. Non-regression contract

- Do not rewrite historical normative batches silently.
- Preserve source/version/retrieval date and supersession.
- Any new legal claim must carry: `authority + jurisdiction + binding_force + effective_date + applicability + evidence + uncertainty + falsifier + F_next`.
- Any product-specific claim must carry runtime evidence.
- Promote no legal/compliance state from documentation alone.

### F_ok

- Brazil, EU, U.S., China, Russia and Cuba connected in one privacy/GNSS/AI/national-security topology.
- GPS civil/military/export-control distinction made explicit.
- U.S. DeepSeek restriction scoped to the intelligence-community national-security context rather than generalized.
- Big Tech GNSS-to-AI responsibility framed through purpose/necessity/transparency/security/accountability instead of unsupported entitlement.

### F_gap

See §14; all remain non-claimable until source/runtime gates close.

### F_next

Generate a machine-readable semantic atlas + append-only receipt; connect this canon to the Mapa normative graph and Drive compliance material without overwriting historical evidence.