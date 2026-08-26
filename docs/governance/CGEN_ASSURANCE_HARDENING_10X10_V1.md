# CGEN Assurance Hardening 10×10 V1

**State:** `PROPOSED_RESEARCH_PROGRAM_EXTENSION / MACHINE_ROUTABLE / FAIL_CLOSED / APPEND_ONLY`

**Parent:** `CGEN V1 — Ciência da Governança Epistêmico-Normativa`

**Target:** governance of AI, Robotics, software, data, scientific claims, legal/technical obligations and cross-domain operational transitions.

**Boundary:** this document is an engineering/scientific governance contract. It is not legal advice, certification, a court opinion, or proof that a deployment complies with every applicable rule.

---

## 0. Hard invariants

```text
VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM
METAPHOR != MECHANISM
ANALOGY != PROOF
ATTENTION != TRUTH
CENSORSHIP != VALIDATION
RETRACTION != AUTOMATIC_FALSITY
ABANDONMENT != FALSIFICATION
REFUTATION != ERASURE
LEGAL_AUTHORITY != SCIENTIFIC_TRUTH
STANDARD != STATUTE
GUIDANCE != LAW
CERTIFICATION != UNIVERSAL_COMPLIANCE
CI_PASS != HUMAN_PROMOTION_AUTHORIZATION
TOKEN_VAZIO != FALSE
TOKEN_VAZIO != PASS
TOKEN_VAZIO != FAIL
UNKNOWN_CRITICAL -> HOLD
P0_CANNOT_BE_AVERAGED_AWAY
STALE_NORM_CANNOT_AUTHORIZE_CURRENT_PROMOTION
IRREVERSIBLE_ACTION_WITH_UNKNOWN_ROLLBACK -> BLOCK
```

Every state transition must be auditable by exact identity, authority, time, evidence and falsifier. Missing proof is preserved as typed `TOKEN_VAZIO`, never normalized into zero or silence.

---

## 1. The 10×10 assurance lattice

Every material node or transition is projected through **10 depth levels** and **10 correlated lenses**. A cell may be `NOT_APPLICABLE`, but only with an explicit reason and reviewer; omission is not equivalent to non-applicability.

### 1.1 Ten depth levels

| Level | Name | Mandatory question | Fail-closed output |
|---|---|---|---|
| L0 | Identity & scope | What exact object/ref/path/hash/time is governed? | `TOKEN_VAZIO_IDENTITY` |
| L1 | Epistemic class | Is it observation, definition, law, standard, model, hypothesis, theorem, anomaly, etc.? | `TOKEN_VAZIO_EPISTEMIC_CLASS` |
| L2 | Evidence & falsifier | What evidence supports it, what would falsify/limit it, and how reproducible is it? | `TOKEN_VAZIO_EVIDENCE` |
| L3 | Temporal validity | Is the evidence/norm current, superseded, expired, withdrawn, revised or stale? | `TOKEN_VAZIO_TEMPORAL` |
| L4 | Authority & applicability | Which authority, jurisdiction, purpose, population and processing context make it applicable? | `TOKEN_VAZIO_AUTHORITY` |
| L5 | Norm interaction | Which rules overlap, conflict, pre-empt, specialize, supplement or merely inform? | `TOKEN_VAZIO_NORM_CONFLICT` |
| L6 | Risk & harm | What threat, failure, bias, rights impact, blast radius and uncertainty exist? | `TOKEN_VAZIO_RISK` |
| L7 | Mitigation & reversibility | What preventive/detective/corrective controls, rollback, failover and remedy exist? | `TOKEN_VAZIO_CONTROL` |
| L8 | Runtime & adaptation | Does observed runtime match declarations, and do monitoring/drift triggers reopen gates? | `TOKEN_VAZIO_RUNTIME` |
| L9 | Oversight & evolution | Who can contest, review, supersede, archive and promote; what receipt closes the cycle? | `TOKEN_VAZIO_OVERSIGHT` |

### 1.2 Ten correlated lenses

1. `LAW_REGULATION`
2. `TECHNICAL_STANDARD`
3. `SECURITY_RESILIENCE`
4. `PRIVACY_DATA_GOVERNANCE`
5. `AI_ALGORITHMIC_GOVERNANCE`
6. `SAFETY_HUMAN_RIGHTS`
7. `ACCESSIBILITY_HUMAN_FACTORS`
8. `ENVIRONMENT_SUSTAINABILITY`
9. `SCIENTIFIC_EPISTEMIC_INTEGRITY`
10. `OPERATIONAL_CONTRACTUAL_GOVERNANCE`

Thus each material object has up to `10 × 10 = 100` explicit assurance cells.

```text
MISSING_CELL != NOT_APPLICABLE
NOT_APPLICABLE requires reason + scope + reviewer
```

---

## 2. Transition contract

A promotable transition `e` must carry:

\[
\Gamma_{10}(e)=
\langle
identity, scope, owner, authority, epistemic\_class,
evidence, falsifier, uncertainty, temporal\_state,
norms, norm\_relations, risk, controls,
rollback, monitoring, contestability, receipt
\rangle.
\]

Minimum machine fields:

```text
transition_id
source_state
target_state
object_ref
exact_ref
epistemic_class
authority_owner
promotion_authority
normative_snapshot
evidence_refs[]
falsifiers[]
unknowns[]
risk_state
mitigations[]
rollback_state
monitoring_state
non_regression_gates[]
human_review_state
receipt_ref
claim_allowed
```

Promotion is conjunctive, not compensatory. A favorable dimension cannot cancel a critical unknown in another dimension.

---

## 3. Gate stack: G0 → G9

| Gate | Required proof | Hard blockers |
|---|---|---|
| G0 Identity | exact object/ref/hash/time | ambiguous identity |
| G1 Provenance | source chain + producer authority | unknown source/producer |
| G2 Epistemic | typed claim + scope + uncertainty | claim class collapse |
| G3 Evidence | reproducible evidence + falsifier | unsupported promotion |
| G4 Normative | current authority/version/applicability | stale/unknown applicable norm |
| G5 Interaction | conflict/overlap/lex-specialis/contract map | unresolved material conflict |
| G6 Risk | threat/harm/bias/blast-radius analysis | critical unknown risk |
| G7 Control | mitigation + rollback/failover/remedy | irreversible unknown rollback |
| G8 Runtime | observed execution + drift/heartbeat | declared≠observed or stale heartbeat |
| G9 Promotion | independent review + receipt + authorization | missing human/authority gate |

**Precedence:** `G0..G9` are not a maturity score. Any applicable hard blocker keeps the transition in `HOLD`, `BLOCKED` or typed `TOKEN_VAZIO`.

---

## 4. Urgency semantics

Urgency is derived from **irreversibility × affected rights/safety × blast radius × uncertainty × active exposure × authority gap**, not from rhetorical importance.

### P0 — immediate hold
Examples:
- irreversible material action with rollback unknown;
- safety/privacy/security-critical runtime acting on ambiguous or stale evidence;
- missing authority for a material write/promotion;
- applicable norm known to be superseded while still authorizing current behavior;
- evidence/claim mismatch that can materially harm rights, safety, custody or integrity;
- attempt to convert `TOKEN_VAZIO` into PASS.

Required response: `HOLD -> CONTAIN -> PRESERVE_EVIDENCE -> ASSIGN_OWNER -> PROBE -> RECEIPT`.

### P1 — high-priority closure
Material uncertainty with bounded current exposure, incomplete independent review, weak provenance, unresolved cross-norm mapping, or missing reproducibility.

### P2 — planned reduction
Known non-critical gaps, maintainability, accessibility, performance, sustainability or documentation debt that cannot silently become P0 through drift.

### P3 — research queue
Hypotheses, alternative models and exploratory relations with no authorization to drive material action.

### P4 — archive/watch
Refuted, superseded, abandoned, retracted, historically censored, ignored or policy-withheld material preserved for learning, falsification and provenance.

`P4` means low operational urgency, **not epistemic deletion**.

---

## 5. TOKEN_VAZIO hardening

Every `TOKEN_VAZIO` must be typed:

```text
id
domain
blocked_gate
missing_evidence
why_missing
owner
f_next
falsifier_or_closure_test
created_at
last_reviewed_at
staleness_trigger
impact_if_unresolved
dependencies[]
```

Rules:

1. `TOKEN_VAZIO` is a first-class state.
2. It cannot satisfy a gate.
3. It cannot be coerced to `false`, `0`, `N/A` or PASS.
4. `N/A` requires proof of non-applicability; uncertainty about applicability remains `TOKEN_VAZIO`.
5. Critical `TOKEN_VAZIO` causes `HOLD`.
6. A closed token is not deleted; it is superseded by a receipt-linked transition.
7. Reopened tokens preserve the previous closure receipt and the trigger that invalidated it.
8. Aggregates must report token counts by gate/domain/age/criticality, not hide them in averages.

---

## 6. Normative evolution and conflict calculus

A normative source is represented as:

\[
N=\langle authority,type,jurisdiction,scope,version,
effective\_from,effective\_to,status,source,checked\_at\rangle.
\]

Relations between norms are typed, never inferred from proximity:

```text
IMPLEMENTS
INTERPRETS
AMENDS
SUPERSEDES
DEROGATES
SPECIALIZES
SUPPLEMENTS
CONFLICTS_WITH
CROSS_REFERENCES
NON_BINDING_GUIDANCE_FOR
TECHNICAL_CONTROL_SUPPORT_FOR
NO_DIRECT_LEGAL_HIERARCHY
TOKEN_VAZIO_RELATION
```

Conflict resolution must preserve a human/legal review boundary. The engine may **detect and route** conflicts; it may not invent legal hierarchy where jurisdiction, competence or facts are unresolved.

### Revalidation triggers
- statute/regulation amendment;
- regulator/court decision material to scope;
- standard revision/withdrawal;
- certification scope/expiry change;
- deployment jurisdiction/purpose/population change;
- new sensitive-data class or user group;
- runtime architecture change;
- material security incident;
- evidence aging beyond declared validity;
- independent review that contradicts a prior classification.

Any material trigger reopens all dependent gates through reverse dependency edges.

---

## 7. Risk model: prevent, detect, contain, recover, learn

The existing OMEGA risk vector remains authoritative; this hardening adds **temporal and dependency semantics**, not a replacement scalar.

For each risk record:

```text
hazard_or_threat
affected_assets_or_rights
preconditions
likelihood_state
impact_state
uncertainty
blast_radius
detectability
velocity
controls_preventive[]
controls_detective[]
controls_corrective[]
rollback
failover
residual_risk
acceptance_authority
monitoring_signal
reopen_threshold
```

### Non-compensation
- P0 dimensions cannot be averaged away.
- `unknown likelihood` with catastrophic plausible impact is not automatically low risk.
- residual risk cannot be declared lower merely because a control exists; control effectiveness requires evidence.
- a failed control reopens every risk assessment that depended on it.

### Adaptive loop

```text
OBSERVE
→ CLASSIFY
→ BIND PROVENANCE
→ ESTIMATE/BOUND RISK
→ MITIGATE
→ TEST
→ MONITOR
→ DETECT DRIFT
→ REOPEN DEPENDENCIES
→ APPEND RECEIPT
→ LEARN
```

No autonomous loop may self-promote its own authorization boundary.

---

## 8. Non-regression contract

A change is regression-safe only if it preserves or deliberately supersedes prior evidence with an explicit reason.

Required suites:

1. **Identity regression** — exact refs and hashes remain resolvable.
2. **Provenance regression** — producer/source lineage is not weakened.
3. **Epistemic regression** — hypothesis/model/analogy cannot become fact/proof by formatting.
4. **Normative regression** — superseded/stale sources cannot remain `CURRENT`.
5. **Security/privacy regression** — protections cannot be silently removed or widened.
6. **Safety/rights regression** — human contestability and fail-safe boundaries remain.
7. **Runtime regression** — exact-head execution evidence cannot be reused for a different head/environment.
8. **Rollback regression** — irreversible operations cannot replace reversible ones without authority.
9. **Observability regression** — heartbeat/log/receipt disappearance is a failure signal, not silence.
10. **Archive regression** — refuted/abandoned/censored/superseded records cannot be erased to improve metrics.

Tests should include positive fixtures, negative fixtures, stale fixtures, conflict fixtures and mutation tests.

---

## 9. Anomalies, paradoxes and contradictions

These categories must not collapse into each other.

- `ANOMALY`: observed datum diverging from an expected model or baseline.
- `PARADOX`: apparent tension requiring decomposition of assumptions/definitions.
- `CONTRADICTION`: propositions cannot simultaneously hold under the same declared scope.
- `OUTLIER`: statistically atypical observation; not automatically error.
- `COUNTEREXAMPLE`: instance falsifying a universal claim.
- `NEGATIVE_RESULT`: predicted effect not observed under protocol.
- `REPLICATION_FAILURE`: prior result not reproduced under a declared comparison protocol.
- `FALSIFIED`: claim fails its declared falsifier under applicable scope.
- `TOKEN_VAZIO`: evidence is not yet sufficient to decide.

Every ledger item records `scope`, `model_expected`, `observation`, `alternative_explanations`, `falsifiers`, `next_probe` and `promotion_prohibited_until`.

---

## 10. The forgotten / ignored / aborted / censored archive

Historical attention state is orthogonal to truth state.

### Attention/history states

```text
MAINSTREAM_CURRENT
LOW_ATTENTION
IGNORED_WITH_REASON
HISTORICALLY_IGNORED
ABANDONED_PRE_CONCLUSION
WITHDRAWN
RETRACTED
SUPERSEDED
HISTORICALLY_CENSORED
SUPPRESSED_BY_POLICY
REDACTED_PRIVACY
UNPUBLISHED
ORPHANED
LOST_SOURCE
TOKEN_VAZIO_HISTORY
```

### Hard separations

```text
HISTORICALLY_CENSORED != TRUE
HISTORICALLY_IGNORED != FALSE
ABANDONED_PRE_CONCLUSION != REFUTED
RETRACTED != FALSIFIED
POPULAR != VALID
UNPOPULAR != INVALID
```

A `HISTORICALLY_CENSORED` label requires evidence of actual suppression/censure, not merely poor reception. `ABANDONED_PRE_CONCLUSION` preserves unresolved work without upgrading it. `RETRACTED` captures publication status; the underlying proposition still requires independent epistemic classification.

### Galileo / flat-Earth guardrail

Historical censorship can delay or distort scientific circulation, but censorship itself is not evidence that a proposition is true. Conversely, a refuted model can remain in the archive as a valuable countermodel and falsification benchmark. The governance lesson is therefore:

```text
PRESERVE_HISTORY
+ PRESERVE_REFUTATIONS
+ PRESERVE_NEGATIVE_RESULTS
- NO_EQUIVALENCE_OF_EVIDENCE
```

The archive protects intellectual memory without collapsing historical injustice, social attention and empirical validity into one axis.

---

## 11. Obvious and neglected checks

The “obvious” must be explicit because mature incidents often arise from omitted basics:

- clock/timezone and observation timestamp;
- unit, scale, coordinate system and sign convention;
- exact dataset/version/sample population;
- null/missing value semantics;
- identity collision/aliasing;
- environment/toolchain/compiler/runtime;
- permissions and least privilege;
- revocation path;
- backup/restore actually tested;
- human-readable error state;
- accessibility and comprehension;
- localization/jurisdiction;
- retention and deletion semantics;
- third-party/transitive dependency drift;
- secret/private locator leakage;
- model/data/license provenance;
- test oracle validity;
- baseline choice;
- multiple-comparison/selection bias;
- survivorship/publication bias;
- negative results;
- decommission/end-of-life.

No check is omitted merely because it appears elementary.

---

## 12. Monitoring and drift

Monitoring is evidence production, not passive telemetry.

Required classes:

```text
AUTHORITY_DRIFT
NORMATIVE_DRIFT
PROVENANCE_DRIFT
SCHEMA_DRIFT
DATA_DRIFT
MODEL_DRIFT
BEHAVIOR_DRIFT
DEPENDENCY_DRIFT
SECURITY_DRIFT
PRIVACY_DRIFT
PERFORMANCE_DRIFT
ACCESSIBILITY_DRIFT
EVIDENCE_AGING
WATCHDOG_HEARTBEAT_STALE
```

A monitor may:
- detect;
- classify;
- quarantine;
- reopen gates;
- request review;
- emit append-only events.

It may not:
- erase history;
- downgrade a P0 by averaging;
- self-authorize a material promotion;
- infer PASS from silence;
- treat a stale heartbeat as healthy.

---

## 13. Promotion and human authority

Promotion requires:

1. exact-head/ref evidence;
2. all applicable hard gates closed;
3. independent review where required;
4. material norm snapshot current;
5. residual risk explicitly accepted by authorized role;
6. rollback/recovery proven or irreversibility explicitly authorized;
7. receipt emitted;
8. `claim_allowed` changed only by the defined promotion authority.

```text
CI_SUCCESS -> eligible_for_review
CI_SUCCESS != PROMOTION
```

Repository server-side protections and independent approval remain external gates; content in a PR cannot prove those controls exist.

---

## 14. Current normative crosswalk extension — 2026-08-26

This hardening routes, but does not collapse, the following current/relevant families:

### Brazil
- LGPD — Lei 13.709/2018, compiled text.
- ANPD Resolutions 15/2024, 18/2024, 19/2024.
- ANPD Resolution 30/2025 — priority themes 2026–2027.
- ANPD Resolution 31/2025 — updated regulatory agenda 2025–2026.
- ANPD Resolution 32/2026 — EU adequacy for international data transfers.
- Lei 15.211/2025 — Estatuto Digital da Criança e do Adolescente.
- Lei 15.352/2026 — ANPD institutional changes and ECA Digital effective-date provisions.

### European Union
- Regulation (EU) 2024/1689 (AI Act), including timing changes introduced by Regulation (EU) 2026/1744. Application is phased; high-risk obligations have category-specific later dates.

### Technical and risk-management references
- ISO/IEC 27701:2025 — Privacy Information Management System.
- ISO/IEC 42001:2023 — AI Management System.
- ISO 14001:2026 — Environmental Management System.
- NIST Cybersecurity Framework 2.0.
- NIST AI RMF 1.0, noting that NIST reports it is under revision.
- NIST AI 600-1 — Generative AI Profile.
- NIST Privacy Framework: Version 1.0 remains the published framework while 1.1 is still an initial-public-draft / forthcoming evolution as of this snapshot.
- RFC 6973 and RFC 3552/BCP 72 where protocol privacy/security analysis applies.

This list is a bounded crosswalk, **not a claim of universal legal applicability**. Applicability is deployment-specific and belongs to L4/L5.

---

## 15. Falsification plan for CGEN itself

CGEN is not protected from falsification.

The program is weakened or falsified in a proposed use if evidence shows that:

1. its state machine cannot distinguish unknown from false in practice;
2. gates cannot prevent claim promotion after a critical evidence loss;
3. dependency reopening fails after a normative change;
4. independent auditors cannot reconstruct a transition from receipts;
5. risk controls cannot be traced to the harms they purport to mitigate;
6. conflict routing systematically invents hierarchy instead of escalating uncertainty;
7. the archive produces false equivalence between refuted and supported claims;
8. monitoring generates unbounded false positives/negatives without measurable control;
9. human oversight is nominal and cannot actually halt or contest material action;
10. the framework's complexity creates more critical failure modes than it prevents.

Every such finding becomes an anomaly/counterexample ledger event and must be allowed to modify or supersede CGEN.

---

## 16. F_ok / F_gap / F_next

### F_ok
- 10-level depth and 10-lens correlation model defined.
- gate precedence and non-compensation explicit.
- typed `TOKEN_VAZIO` contract strengthened.
- normative drift/conflict and reverse-dependency reopening defined.
- risks linked to controls, monitoring and residual acceptance.
- anomaly/paradox/contradiction separation explicit.
- ignored/abandoned/retracted/censored/refuted material preserved without false equivalence.
- non-regression expanded to epistemic, normative, runtime and archive dimensions.

### F_gap
- server-side merge enforcement remains externally unproven.
- independent promotion approval remains unresolved.
- runtime Robotics remains `TOKEN_VAZIO`.
- deployment-specific legal applicability remains `TOKEN_VAZIO`.
- independent legal/privacy/security review remains `TOKEN_VAZIO`.
- human comprehension/accessibility evidence remains `TOKEN_VAZIO`.
- no claim of universal completeness of the normative universe is authorized.

### F_next
1. validate the machine-readable 10×10 contract;
2. bind it into PR #434 tests/workflow;
3. emit an exact-head receipt after CI;
4. reopen any field affected by normative or evidence drift;
5. retain `claim_allowed=false` until the external promotion gates close.

---

**Canonical principle:** preserve uncertainty, preserve history, preserve falsifiers — and promote only what survives provenance, scope, evidence, risk, norms, runtime and independent authority.
