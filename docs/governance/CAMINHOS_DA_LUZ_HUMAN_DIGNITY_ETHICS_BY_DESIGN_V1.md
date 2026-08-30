# Caminhos da Luz — Human Dignity Ethics by Design V1

Status: **CONTROL-PLANE CONTRACT / CLAIM_ALLOWED=false**  
Date: **2026-08-30**

## Purpose

“Caminhos da luz” is used here as a human-centered routing metaphor. The operational contract is not mystical or jurisdiction-substituting: it prevents technical progress from silently weakening dignity, child protection, privacy, appeal, reversibility, cultural respect, humanitarian sensitivity or evidence boundaries.

The control-plane invariant is:

```text
PERSON != RESOURCE != TOKEN != DATASET != COST_FUNCTION
```

and:

```text
MODEL_RECOMMENDATION != HUMAN_VALUE_DECISION
```

Technical optimization happens only after hard human-protection gates are satisfied.

## Non-negotiable hierarchy

```text
HUMAN DIGNITY > EFFICIENCY
RIGHTS CONSTRAINTS -> FEASIBLE SET -> OPTIMIZATION
```

This does **not** mean a single universal moral formula exists. It means the system must refuse to turn dignity, a child’s best interest, privacy or basic human rights into a tunable weight that can be outweighed by throughput, engagement, cost reduction or novelty.

## Protected domains

A change enters enhanced review when it materially touches one or more of:

- children and adolescents;
- health or mental health;
- education;
- personal or sensitive data;
- civil or human rights;
- culture, belief or identity;
- accessibility or disability;
- livelihoods or essential resources;
- public safety;
- humanitarian contexts;
- environmental or ecosystem externalities.

## Human-impact decision ladder

```text
LOW IMPACT + LOW UNCERTAINTY
  -> ALLOW_LOW_IMPACT or ALLOW_WITH_MONITORING

HIGHER IMPACT or HIGHER UNCERTAINTY
  -> REQUIRE_PLURAL_REVIEW

AFFECTED GROUP MATERIAL + DISTRIBUTIONAL RISK
  -> REQUIRE_AFFECTED_GROUP_REVIEW

CHILD / HEALTH / RIGHTS / SENSITIVE PRIVACY / IRREVERSIBLE HARM
  -> FAILSAFE_HOLD until applicable review and evidence exist
```

The direction is a ratchet:

```text
uncertainty ↑ AND consequence_radius ↑ => autonomous_authority ↓
```

## Child-protection hard gate

For systems that can materially affect a child or adolescent:

```text
BEST_INTEREST_OF_CHILD = HARD_CONSTRAINT
```

It must **not** be implemented as a scalar such as:

```text
utility = 0.18 * child_safety + 0.82 * revenue
```

A final high-impact determination affecting a child must not be exclusively algorithmic. Applicable privacy, safeguarding, age-appropriate design, domain expertise and human review remain independent gates.

## Unknown-risk rule

```text
UNKNOWN_RISK != SAFE
NO_AUDITOR_FINDING != PROVEN_ABSENCE
NO_HARM_OBSERVED != HARM_IMPOSSIBLE
TOKEN_VAZIO != PASS
```

A reviewer may report uncertainty without fabricating a conclusion. Missing expertise, missing community voice, missing jurisdictional review or an unmeasured externality stays typed and visible.

## Distribution before average

A project may improve an aggregate metric while making one subgroup substantially worse. Therefore:

```text
AVERAGE_WELFARE != PROTECTION_OF_EACH_GROUP
```

For high-impact changes, the review records who receives the benefit, who carries the risk, who was not measured, and whether a burden is concentrated on people with less power to refuse it.

## Privacy and data governance

The minimum privacy route is:

```text
purpose -> necessity -> minimization -> sensitivity -> retention -> access -> deletion/appeal -> evidence
```

Rules:

- collect only what the declared purpose needs;
- sensitive data defaults to hold/review rather than opportunistic reuse;
- retention requires a reason;
- a model’s desire for more data is not sufficient necessity;
- a hash, pseudonym or identifier does not automatically make data anonymous;
- privacy PASS is independent from runtime, science or performance PASS.

## Culture, belief and social dignity

The system may model cultural context, language and plural values to reduce harm. It must not use culture, belief, ethnicity, disability or identity to rank personal worth.

```text
CONTEXT_AWARENESS != HUMAN_WORTH_SCORING
```

Where a change materially affects a community, local or affected-group review is a governance input rather than a decorative consultation.

## Health and education

Research code, a benchmark or a plausible mechanism does not authorize diagnosis, treatment, educational exclusion or other high-impact action.

```text
SCIENTIFIC_HYPOTHESIS != CLINICAL_AUTHORITY
BENCHMARK_GAIN != EDUCATIONAL_PERMISSION
```

Applicable professional/domain review remains external and independently auditable.

## Environment and future people

The consequence radius includes material energy, hardware, waste, environmental and infrastructure externalities when relevant. Unmeasured environmental impact is not silently converted to zero.

## Authority fragmentation

No single actor should possess unconditional final authority over a high-impact human-value decision solely because that actor is:

- the repository owner;
- an AI system;
- a developer;
- an auditor;
- a domain specialist;
- a funder;
- a regulator;
- a majority user group.

Applicable decisions should combine independent roles and retain an appeal route.

A conceptual authorization envelope is:

```text
VALID_AUTHORITY = RIGHTS
                AND SUFFICIENT_EVIDENCE
                AND APPLICABLE_REVIEW
                AND AFFECTED-GROUP VOICE_WHEN_MATERIAL
                AND REVERSIBILITY_OR_MITIGATION
```

This is a governance conjunction, not a claim that every domain uses identical law or procedure.

## Anti-regression

A successor policy or implementation cannot silently weaken a protected gate because it is newer, faster or more convenient.

Supersession requires:

1. durable provenance pointer;
2. evidence at least as strong as the predecessor or direct falsification;
3. explicit consequence radius;
4. applicable human-impact review when scope expands;
5. rollback or mitigation path;
6. no loss of child, privacy, dignity or appeal protection.

```text
LATEST != STRONGER
RECENCY != AUTHORITY
```

## Relation to existing Mapa invariants

This contract **extends**, and does not replace:

```text
VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM
TOKEN_VAZIO != PASS
FIXTURE != LIVE
HEURISTIC != PROOF
RECENCY != RELEVANCE != AUTHORITY != EVIDENCE
```

A technical validator cannot self-certify human-rights compliance. Its job is narrower: fail closed when a declared hard protection is missing or weakened.

## Machine-readable authority

Canonical control-plane record:

`data/control-plane/HUMAN_DIGNITY_ETHICS_RATCHET_V1.json`

Executable structural validator:

`scripts/validate_human_dignity_ethics_ratchet.py`

Passing that validator means only that the repository still contains the declared governance protections. It is **not** proof of ethical adequacy, legal compliance, child-safety certification, clinical safety or absence of social harm.

## Normative routing anchors

For applicable work, review should route to current authoritative sources such as:

- universal human-rights and human-dignity principles;
- UNESCO AI ethics guidance;
- UNICEF guidance for AI and children;
- WHO ethics/governance guidance for AI in health;
- NIST AI Risk Management Framework;
- ISO/IEC 42001 AI management-system controls;
- Brazilian LGPD and applicable ANPD guidance.

These are **routing anchors**, not a declaration that one checklist satisfies every jurisdiction or application.

## Closure rule

A human-impact `TOKEN_VAZIO` closes only with a successor record identifying the evidence, reviewer/role, scope and exit criterion. Historical uncertainty is preserved append-only rather than rewritten as if it never existed.

## R3

```text
F_ok   = hard human protections are explicit and machine-checkable for presence
F_gap  = machine validation cannot replace legitimate human/community/domain review
F_next = bind this contract into cross-repo impact review and domain-specific repositories
```
