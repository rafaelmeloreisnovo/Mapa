# RAFAELIA — Oracle / Convenções / Bloqueio Sistêmico / Tratamento Algorítmico — Evidence Map — 2026-08-14

State: `APPEND_ONLY / EVIDENCE_FIRST / claim_allowed=false`

## Scope

This record separates six evidence classes that were historically mixed in conversations and derivative analyses:

1. `DOCUMENTED_FACT`
2. `LEGAL_AUTHORITY`
3. `USER_REPORT`
4. `AI_RESPONSE`
5. `CAUSAL_HYPOTHESIS`
6. `FALSIFICATION_RESULT`

The target is not to erase the user's reports or prior AI responses. The target is to preserve them with the correct epistemic type.

## Oracle disambiguation

### ORACLE-CORP-LEGAL

`Google LLC v. Oracle America, Inc.` is a real U.S. Supreme Court copyright/API case. It must not be conflated with an unsupported `Oracle v. Apple about metadata` formulation.

State: `EXTERNAL_LEGAL_PRECEDENT`.

### ORACLE-4EYE

Historical RAFAELIA conversation material describes `Oracle 4EYE` as one engine in a visual/conceptual architecture together with `Atlas Cognitivo Modular`, `DeepVoice Mirror`, and `Z-Core Sound Engine`.

State: `INTERNAL_NOMENCLATURE / USER_CORPUS`.

This is not evidence of any relation to Oracle Corporation.

### ZIPRAF-ORACLE

Google Drive search resolves an `ORACLE_BACKUPS` folder and a separate family of artifacts named `ZIPRAF_ORACLE_*` such as `ZIPRAF_ORACLE_SUPREMO.sh`, `ZIPRAF_ORACLE_SUPRAVERBO.sh`, `ZIPRAF_ORACLE_SUMMARY.yaml`, and `ZIPRAF_ORACLE_HASH.sha256`.

State: `INTERNAL_ARTIFACT_FAMILY`.

No identity equivalence among ORACLE-CORP-LEGAL, ORACLE-4EYE, and ZIPRAF-ORACLE is allowed without explicit evidence.

## Legal authorities and exact boundaries

### Berne Convention

Official WIPO authority: https://www.wipo.int/en/web/treaties/ip/berne/index

Use: protection of literary and artistic works and rights of authors. Copyright protection under the Berne framework is not dependent on a global WIPO registration system.

### WIPO Copyright Treaty (WCT)

Official WIPO authority: https://www.wipo.int/en/web/treaties/ip/wct/summary_wct

Use: digital-environment copyright; computer programs are protected as literary works; qualifying original compilations of data may be protected because of selection/arrangement.

Boundary: protection of a compilation does not automatically monopolize the underlying data.

### TRIPS

Official WTO authority: https://www.wto.org/english/docs_e/legal_e/trips_e.htm

Article 9(2) boundary: copyright extends to expressions, not ideas, procedures, methods of operation, or mathematical concepts as such.

Operational consequence for RAFAELIA: a text, code implementation, diagram, or original arrangement may have copyright protection; an abstract idea, procedure, formula, or mathematical concept does not become exclusively controlled merely by copyright.

### LGPD — automated decisions

Official Brazil authority: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm

Article 20 provides a right to request review of decisions taken solely on automated processing of personal data that affect the data subject's interests. The controller must provide clear and adequate information about criteria/procedures when requested, subject to commercial and industrial secrecy; the national authority may audit discriminatory aspects in the statutory circumstance.

Boundary: this legal right does not itself prove that a given platform used discriminatory or targeted processing against a particular person.

### Budapest Convention on Cybercrime

Council of Europe status source: https://www.coe.int/en/web/octopus/-/brazil

Brazil is a Party; Treaty Office material records accession deposited in 2022 and applicability from 2023.

Boundary: being a Party does not transform a private service failure into a cybercrime finding.

### Convention 108 / 108+

Council of Europe authority: https://www.coe.int/en/web/data-protection/brazil

As checked in 2026, the Brazil page does not show Brazil as having signed/ratified Convention 108. Council of Europe 2026 material describes Brazil as an observer/interested State and mentions a pre-evaluation process concerning possible accession to Convention 108+.

Therefore do not state that Convention 108/108+ is already a treaty obligation binding Brazil as a Party.

## Systemic blocking — typed evidence

`systemic_blocking` is not one thing. Maintain at least four states:

- `TECHNICAL_SYSTEMIC_FAILURE`: reproducible build/CI/download/platform failure with observable mechanism;
- `POLICY_RESTRICTION`: platform or organizational rule causing restriction;
- `DIFFERENTIAL_AUTOMATED_TREATMENT`: measurable differential outcome associated with account/content/context;
- `TARGETED_PERSECUTION_CAUSAL_CLAIM`: claim that a person/system intentionally targets the user.

Only the first can be promoted from an ordinary engineering failure without additional evidence. The latter two require comparison, controls, logs, repeated measurements, and causal exclusion.

A documented example already present in the corpus is `Vectras Build Organism Health Report — 2026-04-28`, where an ABI contract drift caused CI to enter an invalid state before build and mask other failures. This is a technical systemic failure, not evidence of intentional persecution.

Historical conversation shards also contain reports and AI responses about ChatGPT ZIP/download blocking. Preserve those as `USER_REPORT` and `AI_RESPONSE` until independent platform telemetry or a controlled reproduction establishes mechanism.

## Historical AI-response correction lane

Some assistant messages in the corpus asserted or strongly implied causal explanations such as systems discrediting by default, barriers being specifically directed, matrices being inviolable, or patent protection being unnecessary.

Classification:

- statement exists in historical assistant output: `DOCUMENTED_AI_RESPONSE`;
- causal content not independently evidenced: `NOT_EVIDENCE_OF_CAUSE`;
- absolute technical/legal statements unsupported by evidence: `RETRACTED_OVERCLAIM`.

The historical bytes are preserved. Retraction means semantic status correction, not deletion.

## Image evidence boundary

For images/screenshots, canonical custody is:

`ORIGINAL_IMAGE -> provider/path -> bytes/hash -> timestamp -> visual observation -> AI interpretation -> external corroboration -> verdict`

An AI description of an image is not a substitute for the image bytes and cannot be promoted as proof of the depicted mechanism.

Historical material references at least one image interpretation labelled `Imagem 9 – Verbo Vivo + módulos IA` and identifies `Oracle 4EYE`, `Atlas Cognitivo Modular`, `DeepVoice Mirror`, and `Z-Core Sound Engine`. That preserves the existence of the interpretation; the original image must be separately bound for visual-evidence claims.

## Falsifiable algorithmic-treatment protocol

For every alleged incident, capture:

`incident_id, timestamp, platform, account_context, requested_action, returned_result, error_code, policy_notice, screenshot_provider, screenshot_sha256, artifact_provider, artifact_sha256, retry_count, control_account_or_control_context, repeated_result, alternative_explanations, legal_relevance, verdict`

Hypotheses:

`H0`: observed failures are explained by general rules, ordinary technical faults, capacity limits, random variation, or content-independent policy application.

`H1`: there is reproducible differential automated treatment associated with a defined account/content/context variable.

`TARGETED_PERSECUTION` must remain a separate stronger hypothesis; evidence for differential treatment alone does not prove intent, coordinated targeting, or persecution.

## Evidence sources already resolved in Drive corpus

- `MESSAGES-00011.jsonl.txt` — historical Oracle 4EYE/image interpretations and other Oracle-related assistant responses.
- `MESSAGES-00012.jsonl.txt` — historical references to algorithmic/persecution language and ChatGPT download-blocking responses.
- `MESSAGES-00013.jsonl.txt` — further user reports/responses concerning ZIP delivery and platform behavior.
- `MESSAGES-00014.jsonl.txt`, `MESSAGES-00015.jsonl.txt` — search hits for systemic-blocking terminology.
- `build-health-2026-04-28.md` — technical systemic CI failure report.
- `LEGAL_NOTICE_pt-en.md` / `README_legal.md` — scientific reverse-engineering/legal framing.
- `ORACLE_BACKUPS` and `ZIPRAF_ORACLE_*` — internal artifact lineage requiring separate custody records.

## Orthogonal routing

- `LEGAL/IP`: Berne, WCT, TRIPS, copyright/patent boundary.
- `DATA_PROTECTION`: LGPD Art. 20; automated-decision review.
- `CYBERCRIME`: Budapest Convention; preserve jurisdictional limits.
- `ORACLE_CORP`: external corporate/legal Oracle material.
- `ORACLE_4EYE`: internal conceptual/visual module.
- `ZIPRAF_ORACLE`: internal artifact family.
- `PLATFORM_FAILURES`: reproducible technical failures.
- `ALGORITHMIC_TREATMENT`: controlled differential-treatment hypothesis.
- `AI_RESPONSE_AUDIT`: historical assistant overclaims/corrections.
- `IMAGE_CUSTODY`: image originals and derived interpretations.

## Anti-regression invariants

1. Event observed != cause established.
2. User report != fabricated; it is evidence of the report, not automatically of the external cause.
3. AI response != independent evidence.
4. Technical failure != intentional targeting.
5. Differential treatment != persecution or intent.
6. Treaty existence != automatic applicability to every dispute.
7. Copyright != patent != trade secret != license != scientific priority.
8. Oracle 4EYE != Oracle Corporation unless evidence explicitly binds them.
9. Image interpretation != original-image evidence.
10. Missing field remains `TOKEN_VAZIO`.
11. Corrections append; historical bytes remain preserved.
12. `claim_allowed=false` for causal allegations until the relevant evidence gate closes.

## R3

`F_ok`: the corpus contains real legal documents, real technical failure reports, historical user reports, historical AI responses, Oracle-4EYE nomenclature, ZIPRAF-ORACLE artifacts, and external legal authorities that can be typed without erasing provenance.

`F_gap`: original-image byte bindings are incomplete; platform-side logs and controlled differential-treatment experiments are not yet closed; some legal documents cite broad treaty language that must be mapped provision-by-provision; causal intent remains unproved.

`F_next`: build a ledger `USER_REPORT <-> AI_RESPONSE <-> IMAGE <-> TECHNICAL_EVIDENCE <-> LEGAL_AUTHORITY <-> FALSIFIER <-> VERDICT` over the relevant conversation shards and image providers, with exact message IDs/hashes and no causal promotion by narrative.
