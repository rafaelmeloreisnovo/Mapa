# CGEN Assurance Hardening 10×10 V1

**State:** `PROPOSED_RESEARCH_PROGRAM_EXTENSION / MACHINE_ROUTABLE / FAIL_CLOSED / APPEND_ONLY`

**Parent:** `CGEN V1 — Ciência da Governança Epistêmico-Normativa`

**Target:** governance of AI, Robotics, software, data, scientific claims, legal and technical obligations, formula transfer and cross-domain operational transitions.

**Boundary:** this is an engineering and scientific governance contract. It is not legal advice, certification, a court opinion, or proof that one deployment complies with every possible rule.

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
FORMULA_SIMILARITY != DOMAIN_VALIDITY
DIMENSIONAL_CONSISTENCY != EMPIRICAL_VALIDATION
```

Every material transition must be reconstructible from exact identity, authority, time, evidence, uncertainty, falsifier and receipt. Missing proof is preserved as a typed `TOKEN_VAZIO`; it is never normalized into zero, false, silence or PASS.

---

## 1. The 10×10 assurance lattice

Every material node or transition is projected through **10 depth levels** and **10 correlated lenses**. A cell may be `NOT_APPLICABLE`, but only with a reason, scope and reviewer. Omission is not non-applicability.

### 1.1 Ten depth levels

| Level | Name | Mandatory question | Fail-closed output |
|---|---|---|---|
| L0 | Identity & scope | What exact object, ref, path, hash and time are governed? | `TOKEN_VAZIO_IDENTITY` |
| L1 | Epistemic class | Observation, definition, law, standard, model, hypothesis, theorem, anomaly or other? | `TOKEN_VAZIO_EPISTEMIC_CLASS` |
| L2 | Evidence & falsifier | What supports it, what can falsify or limit it, and how reproducible is it? | `TOKEN_VAZIO_EVIDENCE` |
| L3 | Temporal validity | Current, superseded, expired, withdrawn, revised, stale or unknown? | `TOKEN_VAZIO_TEMPORAL` |
| L4 | Authority & applicability | Which authority, jurisdiction, purpose, population and context apply? | `TOKEN_VAZIO_AUTHORITY` |
| L5 | Norm interaction | Which rules overlap, conflict, specialize, supplement or only inform? | `TOKEN_VAZIO_NORM_CONFLICT` |
| L6 | Risk & harm | Threat, failure, bias, rights impact, blast radius and uncertainty? | `TOKEN_VAZIO_RISK` |
| L7 | Mitigation & reversibility | Preventive, detective and corrective controls; rollback, failover and remedy? | `TOKEN_VAZIO_CONTROL` |
| L8 | Runtime & adaptation | Does observed runtime match declarations; what drift reopens gates? | `TOKEN_VAZIO_RUNTIME` |
| L9 | Oversight & evolution | Who contests, reviews, supersedes, archives and promotes; what receipt closes it? | `TOKEN_VAZIO_OVERSIGHT` |

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

A promotable transition `e` carries:

\[
\Gamma_{10}(e)=
\langle
identity,scope,owner,authority,epistemic\_class,
evidence,falsifier,uncertainty,temporal\_state,
norms,norm\_relations,risk,controls,
rollback,monitoring,contestability,receipt
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

## 3. Gate stack G0 → G9

| Gate | Required proof | Hard blockers |
|---|---|---|
| G0 Identity | exact object, ref, hash and time | ambiguous identity |
| G1 Provenance | source chain and producer authority | unknown source or producer |
| G2 Epistemic | typed claim, scope and uncertainty | claim-class collapse |
| G3 Evidence | reproducible evidence and falsifier | unsupported promotion |
| G4 Normative | current authority, version and applicability | stale or unknown applicable norm |
| G5 Interaction | conflict, overlap and specialization map | unresolved material conflict |
| G6 Risk | threat, harm, bias and blast-radius analysis | critical unknown risk |
| G7 Control | mitigation, rollback, failover and remedy | irreversible unknown rollback |
| G8 Runtime | observed execution, drift and heartbeat | declared-observed mismatch or stale heartbeat |
| G9 Promotion | independent review, receipt and authorization | missing human or authority gate |

**Precedence:** `G0..G9` are not a maturity score. Any applicable hard blocker keeps the transition in `HOLD`, `BLOCKED` or typed `TOKEN_VAZIO`.

---

## 4. Urgency semantics

Urgency derives from **irreversibility × affected rights/safety × blast radius × uncertainty × active exposure × authority gap**, not rhetorical importance.

### P0 — immediate hold

Examples:

- irreversible material action with rollback unknown;
- safety, privacy or security-critical runtime acting on ambiguous or stale evidence;
- missing authority for a material write or promotion;
- superseded applicable norm still authorizing current behavior;
- evidence/claim mismatch capable of material harm;
- attempt to convert `TOKEN_VAZIO` into PASS.

Required response: `HOLD -> CONTAIN -> PRESERVE_EVIDENCE -> ASSIGN_OWNER -> PROBE -> RECEIPT`.

### P1 — high-priority closure

Material uncertainty with bounded current exposure, incomplete independent review, weak provenance, unresolved cross-norm mapping or missing reproducibility.

### P2 — planned reduction

Known non-critical gaps in maintainability, accessibility, performance, sustainability or documentation that cannot silently become P0 through drift.

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
4. `N/A` requires evidence of non-applicability.
5. Critical `TOKEN_VAZIO` causes `HOLD`.
6. Closure never deletes history; a receipt-linked transition supersedes the open state.
7. Reopening preserves the former closure and the invalidation trigger.
8. Aggregates expose count, age, gate, domain and criticality instead of hiding unknowns in averages.

---

## 6. Normative evolution and conflict calculus

A normative source is represented as:

\[
N=\langle authority,type,jurisdiction,scope,version,
effective\_from,effective\_to,status,source,checked\_at\rangle.
\]

Relations are typed, never inferred from proximity:

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

The engine may detect and route a conflict. It may not invent legal hierarchy where jurisdiction, competence, purpose or facts remain unresolved.

### Revalidation triggers

- statute or regulation amendment;
- regulator or court decision material to scope;
- standard revision or withdrawal;
- certification scope or expiry change;
- deployment jurisdiction, purpose or population change;
- sensitive-data class or protected-user-group change;
- runtime architecture change;
- material security incident;
- evidence aging beyond declared validity;
- independent review contradicting a prior classification.

A material trigger reopens all dependent gates through reverse dependency edges.

---

## 7. Risk model: prevent, detect, contain, recover, learn

The existing OMEGA risk vector remains authoritative. This hardening adds temporal and dependency semantics rather than replacing it with one scalar.

Every risk record includes:

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
- Unknown likelihood with catastrophic plausible impact is not automatically low risk.
- Residual risk cannot fall merely because a control exists; effectiveness needs evidence.
- A failed control reopens each risk assessment that depended on it.

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

A change is regression-safe only if it preserves prior evidence or deliberately supersedes it with an explicit reason.

Required suites:

1. **Identity regression** — exact refs and hashes remain resolvable.
2. **Provenance regression** — producer/source lineage is not weakened.
3. **Epistemic regression** — hypothesis, model or analogy cannot become fact or proof by formatting.
4. **Normative regression** — superseded or stale sources cannot remain `CURRENT`.
5. **Security/privacy regression** — protections cannot be silently removed or widened.
6. **Safety/rights regression** — contestability and fail-safe boundaries remain.
7. **Runtime regression** — exact-head evidence cannot be reused for a different head or environment.
8. **Rollback regression** — irreversible operations cannot replace reversible ones without authority.
9. **Observability regression** — disappearance of heartbeat, log or receipt is a signal, not PASS.
10. **Archive regression** — refuted, abandoned, censored and superseded records cannot be erased to improve metrics.

Tests include positive, negative, stale, conflict and mutation fixtures where applicable.

---

## 9. Anomalies, paradoxes and contradictions

These states do not collapse into each other:

- `ANOMALY`: observation diverging from an expected model or baseline.
- `PARADOX`: apparent tension requiring decomposition of assumptions or definitions.
- `CONTRADICTION`: propositions cannot both hold under the same declared scope.
- `OUTLIER`: statistically atypical observation, not automatically error.
- `COUNTEREXAMPLE`: instance falsifying a universal claim.
- `NEGATIVE_RESULT`: predicted effect not observed under protocol.
- `REPLICATION_FAILURE`: prior result not reproduced under a declared comparison protocol.
- `FALSIFIED`: claim fails its declared falsifier under applicable scope.
- `TOKEN_VAZIO`: evidence is insufficient to decide.

Every ledger item records `scope`, `model_expected`, `observation`, `alternative_explanations`, `falsifiers`, `next_probe` and `promotion_prohibited_until`.

---

## 10. Forgotten, ignored, aborted and censored archive

Historical attention state is orthogonal to truth state.

### Attention and history states

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

`HISTORICALLY_CENSORED` requires evidence of actual suppression or censure, not merely weak reception. `ABANDONED_PRE_CONCLUSION` preserves unresolved work without upgrading it. `RETRACTED` captures publication status; the underlying proposition still requires independent epistemic classification.

### Galileo and flat-Earth guardrail

Historical censorship can delay or distort scientific circulation, but censorship itself is not evidence that a proposition is true. A refuted model can remain in the archive as a countermodel, history-of-science object and falsification benchmark.

```text
PRESERVE_HISTORY
+ PRESERVE_REFUTATIONS
+ PRESERVE_NEGATIVE_RESULTS
- NO_EQUIVALENCE_OF_EVIDENCE
```

The archive preserves intellectual memory without collapsing historical injustice, social attention and empirical validity onto one axis.

---

## 11. Obvious and neglected checks

The obvious is explicit because mature incidents frequently arise from omitted basics:

- clock, timezone and observation timestamp;
- unit, scale, coordinate system and sign convention;
- exact dataset, version and sample population;
- null and missing-value semantics;
- identity collision and aliasing;
- environment, toolchain, compiler and runtime;
- permissions and least privilege;
- revocation path;
- backup and restore actually tested;
- human-readable error state;
- accessibility and comprehension;
- localization and jurisdiction;
- retention and deletion semantics;
- third-party and transitive-dependency drift;
- secret and private-locator leakage;
- model, data and license provenance;
- test-oracle validity;
- baseline choice;
- multiple-comparison and selection bias;
- survivorship and publication bias;
- negative results;
- decommission and end-of-life.

No check is omitted merely because it appears elementary.

---

## 12. Formula and dimensional transfer gate

A formula can be mathematically reusable across another representation while remaining physically, statistically or normatively invalid there. Therefore transfer is explicitly typed.

### 12.1 Dimensions that must not be conflated

- mathematical dimension: `R^n`, manifold, vector-space or topological dimension;
- physical dimension: mass, length, time, charge, temperature and derived dimensions;
- measurement unit: SI or another declared unit system;
- tensor or array dimension: axes, shape and indexing semantics;
- statistical dimension: variables, latent factors and parameter spaces;
- semantic dimension: ontology or feature axes;
- operational dimension: state-machine or control-plane axes;
- normative dimension: jurisdiction, authority, purpose and population scope.

### 12.2 Transfer signature

For a formula `F : X -> Y`, any reuse in domain `D'` requires:

\[
T_F=\langle
X,Y,units,scale,coordinates,invariants,boundary\_conditions,
transform,assumptions,error,falsifier,evidence
\rangle.
\]

Required questions:

1. Are domain and codomain well typed?
2. Are units dimensionally homogeneous where physical units exist?
3. Which invariants survive the transformation?
4. Is the transformation an isomorphism, projection, approximation or analogy?
5. Which boundary conditions changed?
6. Does a mathematical identity remain only mathematical, or is empirical interpretation claimed?
7. What measurable observation would falsify the transferred interpretation?
8. Is the new domain merely descriptive, predictive, causal or normative?
9. What uncertainty is introduced by the transfer?
10. What exact evidence authorizes promotion beyond hypothesis?

### 12.3 Transfer states

```text
PROVED_IDENTITY_SAME_DOMAIN
PROVED_ISOMORPHIC_REWRITE
VALID_DIMENSIONAL_TRANSFORM
MODEL_TRANSFER_BOUNDED
HYPOTHESIS_TRANSFER
ANALOGY_ONLY
INVALID_DIMENSIONAL_MISMATCH
OUT_OF_SCOPE
TOKEN_VAZIO_TRANSFER
```

Critical invariant:

```text
PURE_MATH_VALIDITY
!= PHYSICAL_APPLICABILITY
!= EMPIRICAL_SUPPORT
!= CAUSAL_EXPLANATION
!= LEGAL_OR_NORMATIVE_AUTHORITY
```

A geometric recurrence, ratio or invariant may therefore be explored in higher-dimensional mathematics or another computational representation without claiming that the corresponding physical or social mechanism has been demonstrated.

---

## 13. Monitoring and drift

Monitoring is evidence production, not passive telemetry.

Required drift classes:

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
FORMULA_DOMAIN_DRIFT
UNIT_SCALE_DRIFT
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
- downgrade P0 by averaging;
- self-authorize a material promotion;
- infer PASS from silence;
- treat a stale heartbeat as healthy.

---

## 14. Promotion and human authority

Promotion requires:

1. exact-head or exact-ref evidence;
2. all applicable hard gates closed;
3. independent review where required;
4. material normative snapshot current;
5. residual risk explicitly accepted by an authorized role;
6. rollback or recovery proven, or irreversibility explicitly authorized;
7. receipt emitted;
8. `claim_allowed` changed only by the defined promotion authority.

```text
CI_SUCCESS -> ELIGIBLE_FOR_REVIEW
CI_SUCCESS != PROMOTION
```

Repository server-side protection and independent approval remain external gates. Content inside a PR cannot prove those controls exist.

---

## 15. Current normative crosswalk extension — 2026-08-26

This section routes relevant families without collapsing them into one hierarchy.

### Brazil

- LGPD — Lei 13.709/2018, compiled text;
- ANPD Resolutions 15/2024, 18/2024 and 19/2024;
- ANPD Resolution 30/2025 — priority themes 2026–2027;
- ANPD Resolution 31/2025 — updated regulatory agenda 2025–2026;
- ANPD Resolution 32/2026 — EU adequacy for international transfers;
- Lei 15.211/2025 — Estatuto Digital da Criança e do Adolescente;
- Lei 15.352/2026 — ANPD institutional changes and ECA Digital timing provisions.

### European Union

- Regulation (EU) 2024/1689, AI Act, including timing changes introduced by Regulation (EU) 2026/1744. Application is phased; category-specific high-risk obligations have later dates.

### Technical and risk-management references

- ISO/IEC 27701:2025 — privacy information management;
- ISO/IEC 42001:2023 — AI management systems;
- ISO 14001:2026 — environmental management systems;
- NIST Cybersecurity Framework 2.0;
- NIST AI RMF 1.0, explicitly tracked as under revision in the 2026 snapshot;
- NIST AI 600-1 — Generative AI Profile;
- NIST Privacy Framework 1.0 as published framework while 1.1 remains a draft/forthcoming evolution in this snapshot;
- RFC 6973 and RFC 3552/BCP 72 where protocol privacy and security analysis applies.

This list is a bounded crosswalk, **not universal legal applicability**. Applicability belongs to L4 and L5 for the declared deployment.

---

## 16. Falsification plan for CGEN itself

CGEN is not protected from falsification. The program is weakened or falsified in a proposed use if evidence shows that:

1. its state machine cannot distinguish unknown from false in practice;
2. critical evidence loss does not reopen dependent gates;
3. normative change does not reopen dependent controls or claims;
4. independent auditors cannot reconstruct a transition from receipts;
5. risk controls cannot be traced to the harms they purport to mitigate;
6. conflict routing invents hierarchy instead of escalating uncertainty;
7. the archive produces false equivalence between refuted and supported claims;
8. monitoring produces uncontrolled false positives or negatives;
9. human oversight cannot actually halt or contest a material action;
10. framework complexity creates more critical uncontrolled failure modes than it prevents.

Each finding becomes an anomaly, counterexample or falsifier ledger event and may modify or supersede CGEN.

---

## 17. F_ok / F_gap / F_next

### F_ok

- 10-level depth and 10-lens correlation model defined;
- 10 hard gates and non-compensation semantics explicit;
- typed `TOKEN_VAZIO` strengthened;
- normative drift, conflict and reverse-dependency reopening defined;
- risks connected to controls, monitoring and residual acceptance;
- anomaly, paradox and contradiction separated;
- ignored, abandoned, retracted, censored and refuted material preserved without false equivalence;
- non-regression expanded across epistemic, normative, runtime and archive dimensions;
- formula/domain dimensional transfer receives a dedicated falsifiable gate.

### F_gap

- server-side merge enforcement remains externally unproven;
- independent promotion approval remains unresolved;
- runtime Robotics remains `TOKEN_VAZIO`;
- deployment-specific legal applicability remains `TOKEN_VAZIO`;
- independent legal, privacy and security review remains `TOKEN_VAZIO`;
- human comprehension and accessibility evidence remains `TOKEN_VAZIO`;
- universal completeness of the normative universe is not claimed.

### F_next

1. validate the machine-readable 10×10 contract;
2. execute repository lint and non-regression gates at the exact new head;
3. append an exact-head qualification receipt after CI;
4. reopen any field affected by normative, evidence or dimensional-domain drift;
5. retain `claim_allowed=false` until external promotion gates close.

---

**Canonical principle:** preserve uncertainty, history, falsifiers and negative results; promote only what survives provenance, scope, evidence, risk, norms, runtime and independent authority.
