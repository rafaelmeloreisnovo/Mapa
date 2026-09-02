# RAFAELIA Human Dignity · Child Protection · Privacy · Cultural Governance Overlay V1

**State:** `CANONICAL_DRAFT / FAIL_CLOSED / APPEND_ONLY / HUMAN_REVIEW_REQUIRED_WHEN_APPLICABLE`

Parent canon: `docs/governance/SHARED_DATA_GOVERNANCE_V2.md`

`claim_allowed=false` until applicable evidence and authority gates are satisfied.

## 1. Purpose

This overlay adds a human-impact control plane to technical audit, risk monitoring and federated governance. It does not declare legal certification or universal cultural authority.

Core invariant:

`technical_success != ethical_acceptability != lawful_basis != community_legitimacy != release_authority`

The system SHALL preserve human dignity, privacy, child safety, pluralism, accessibility, non-discrimination, freedom of belief and conscience, and meaningful human accountability. Cultural context may refine safeguards but SHALL NOT be used to excuse violence, exploitation, coercion, abuse, discrimination, trafficking, sexual exploitation of children, or other violations of fundamental rights.

A cooperative ethical north star may be expressed as reciprocity: **treat the other person's dignity and welfare as seriously as one's own**, without imposing one religion or tradition as operational authority.

## 2. Human-impact dimensions

Every material governance decision SHALL evaluate, when applicable:

1. `DIGNITY` — humiliation, dehumanization, coercion, exclusion, autonomy.
2. `CHILD_SAFETY` — age appropriateness, exploitation risk, grooming/contact risk, profiling, parental/guardian and child rights where legally applicable.
3. `PRIVACY` — necessity, purpose limitation, minimization, sensitivity, reidentification, retention, access, revocation and propagation.
4. `CULTURE_BELIEF` — religion/belief, language, local custom, minority viewpoints and legitimate disagreement.
5. `INDIGENOUS_COMMUNITY` — collective interests, cultural knowledge, community protocols, provenance and appropriate consultation/authority where applicable.
6. `EQUITY_ACCESS` — disability/accessibility, disparate impact, digital exclusion and vulnerable groups.
7. `OPERATOR_WELFARE` — workload, psychological safety, exposure to disturbing material, competence, conflict of interest and ability to stop/escalate.

Unknown applicability is `TOKEN_VAZIO`, never `NOT_APPLICABLE` by assumption.

## 3. Child-protection super-gate

When a child or likely child may be affected, default criticality increases by at least one level and the following become mandatory before consequential release or automated action:

- data minimization and age-appropriate design assessment;
- prohibition of unnecessary sensitive profiling;
- heightened access control and retention review;
- foreseeable misuse and contact/exploitation threat assessment;
- human escalation route;
- applicable guardian/child participation or consent analysis without treating guardian consent as universally sufficient;
- documented best-interests analysis;
- redaction/pseudonymization where compatible with the purpose;
- evidence that the action is necessary and proportionate.

`child_best_interests_unknown -> TOKEN_VAZIO -> BLOCK consequential promotion`

No cultural, commercial, research or operator preference overrides the child-safety gate.

## 4. Privacy-by-design audit

For each governed processing/share/action:

`purpose -> lawful/authorized basis -> necessity -> minimization -> data classes -> subjects/communities -> recipients -> transformations -> inference risk -> retention/TTL -> access -> security -> downstream propagation -> revocation -> evidence -> receipt`

Sensitive characteristics, precise location, biometrics, health, intimate life, beliefs, ethnicity/indigenous identity, child data and correlatable identifiers receive heightened review according to applicable law and context.

A hash, fragment, pseudonym, embedding or statistical representation SHALL NOT be presumed anonymous.

## 5. Cultural and belief pluralism

The governance layer SHALL distinguish:

`respect_for_belief != endorsement_of_belief`

`local_context != universal_rule`

`tradition != automatic_authority`

`heated_disagreement != permission_for_harassment`

For decisions materially affecting a local, traditional, minority or indigenous community, record where applicable:

- jurisdiction and locality;
- languages and accessibility needs;
- affected community/communities;
- relevant local norms or protocols;
- competing legitimate viewpoints;
- source and authority for cultural assertions;
- consultation performed and who was not represented;
- dissent/minority report;
- potential irreversible cultural or collective harm;
- unresolved uncertainty as `TOKEN_VAZIO`.

Do not infer a community's beliefs from stereotypes or a single spokesperson.

## 6. Indigenous and traditional knowledge

Where indigenous peoples, traditional communities or culturally restricted knowledge may be implicated:

- preserve provenance and original context;
- identify whether individual and/or collective interests are implicated;
- avoid treating public discoverability as permission for unrestricted reuse;
- assess applicable consultation, consent, benefit-sharing, attribution and access protocols;
- preserve restrictions on sacred, sensitive or community-controlled knowledge when applicable;
- record disagreement between legal permission and community expectations as a governance risk rather than silently choosing one.

If authority or consultation requirements cannot be established, record `TOKEN_VAZIO` and restrict consequential reuse.

## 7. Civilizational approval trace

No single `approved=true` is sufficient for high-impact decisions. Use an approval trace:

`decision_id -> source/revision -> scope -> affected_people -> affected_communities -> jurisdiction -> risk_vector -> operator -> proposer -> independent_reviewer -> privacy_review -> child_safety_review -> cultural/community_review -> technical_evidence -> dissent -> conditions -> expiry/revalidation -> final_authority -> receipt`

A role is recorded only when applicable. Missing mandatory roles are explicit gaps.

Approval SHALL be attributable to a role/authority and evidence, not merely a person's identity. Separation of duties is preferred for high-impact decisions.

## 8. Operator conscience, competence and forgotten stakeholders

Every consequential audit SHALL include a `FORGOTTEN_STAKEHOLDER_PROBE`:

- who bears risk but is absent from the decision?
- who cannot meaningfully consent or object?
- who is affected downstream or indirectly?
- whose language, disability, age, poverty, remoteness or institutional position reduces voice?
- which operators are exposed to moral distress or disturbing material?

Operators have stop-work and escalation authority for credible dignity, privacy, child-safety or severe cultural-harm concerns. Retaliation for good-faith escalation is incompatible with this governance model.

## 9. Adaptive audit and risk monitoring

Risk is re-evaluated when source, model, jurisdiction, population, purpose, recipient, threat environment, cultural context or observed harm changes.

Minimum event states:

`DOCUMENTED | OBSERVED | EXECUTED | MEASURED | REPRODUCED | CONTRADICTED | BLOCKED | TOKEN_VAZIO`

Minimum risk vector:

`privacy × child_safety × dignity × discrimination × cultural_harm × security × misuse × irreversibility × operator_welfare`

Monitoring SHALL prefer trend and evidence over raw alert volume. Repeated false positives, missing populations and silent failure modes are themselves audit findings.

High-severity signals trigger bounded containment and human review; they do not automatically establish guilt, abuse, illegality or cultural wrongdoing.

## 10. Gap schema

Every unresolved mandatory control uses:

```text
gap_id
state=TOKEN_VAZIO
source_pointer
missing_field
blocking_dependency
evidence_needed
falsifier
next_probe
owner_or_authority
urgency
closure_gate
claim_allowed=false
predecessor
lineage
human_impact_dimensions
jurisdiction_or_context
```

## 11. Evidence and audit receipt

For consequential decisions preserve append-only:

`SOURCE -> TRANSFORM -> CLAIM -> TEST/EVIDENCE -> HUMAN_IMPACT_REVIEW -> APPROVAL/DISSENT -> RECEIPT -> INDEX -> MEMORY`

Receipt minimum:

- immutable source/ref/hash where available;
- decision and risk-vector version;
- applicable normative/jurisdictional references with snapshot/date;
- reviewers/roles and authority boundaries;
- conflicts of interest;
- dissent and unresolved gaps;
- tests/evidence and falsifiers;
- data minimization/redaction performed;
- expiry/revalidation condition;
- rollback/revocation route;
- `claim_allowed` transition with explicit gate evidence.

## 12. Normative-reference discipline

Standards, laws, treaties, professional codes and community protocols are maintained as versioned references. The repository SHALL NOT claim compliance/certification merely because a control resembles a standard.

`reference_mapped != applicability_established != control_implemented != control_effective != audited_compliance != certification`

Jurisdiction-specific legal conclusions require case facts and competent authority/review where appropriate.

## 13. Conflict resolution

When legitimate values conflict, use:

`SAFETY/FUNDAMENTAL_RIGHTS_FLOOR -> APPLICABLE_LAW/AUTHORITY -> NECESSITY -> PROPORTIONALITY -> LEAST_HARM -> REVERSIBILITY -> PARTICIPATION -> DISSENT_RECORD -> REVALIDATION`

Consensus is desirable but not fabricated. A minority report remains attached to the decision lineage.

## 14. Release gates

Consequential promotion is blocked when any applicable critical gate is unresolved, including:

- credible child-safety risk without best-interests review;
- unknown authority for sensitive personal data;
- unresolved severe reidentification risk;
- absent mandatory human review;
- unresolved high-severity dignity/discrimination harm;
- missing community/indigenous authority or consultation where required;
- inability to identify rollback/revocation for a reversible action;
- evidence insufficient to distinguish allegation from verified fact.

## 15. Final invariant

`HUMAN_DIGNITY + CHILD_SAFETY + PRIVACY + PLURALISM + ACCOUNTABILITY + EVIDENCE > operational convenience`

Cooperation is the preferred mode across disagreement; protection from harm and respect for human dignity are the floor beneath that cooperation.
