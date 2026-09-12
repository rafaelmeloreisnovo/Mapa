# RAFAELIA Audit and Enforcement Protocol V1

Status: DRAFT_FOR_LEGAL_REVIEW

## 1. Design principle

Compliance verification must be proportionate, confidential, evidence-bound, and minimally intrusive.

The structure is informed by established commercial software licensing practice in which licensees retain records, may perform self-audits, and may be subject to independent verification.

## 2. Trigger

A compliance verification may be requested only when at least one of the following exists:

- the licensee asserts a Commercial License;
- there is a reasonable, documented indication of use outside the granted scope;
- a signed commercial agreement contains a scheduled verification right;
- a distribution/reporting obligation requires confirmation.

Purely private non-commercial research use does not create an unrestricted inspection right.

## 3. Records

A commercial licensee should retain records reasonably sufficient to verify:

- licensed entities and affiliates;
- licensed products/artifacts;
- copies, seats, deployments, instances, or distributions where applicable;
- license term and territory;
- source/revision used;
- sublicense or redistribution rights;
- required attribution and notices;
- commercial payments and true-ups;
- third-party license compliance.

Retention periods must be stated in the signed commercial schedule and aligned with applicable law.

## 4. Verification methods

Verification should proceed in this order:

1. written certification/self-audit;
2. documentary review;
3. remote evidence review;
4. independent third-party audit;
5. on-site review only when contractually authorized and proportionate.

## 5. Notice and timing

Unless urgent preservation of evidence is legally justified, an independent audit should ordinarily provide at least 30 calendar days' prior written notice.

Verification should occur during normal business hours and should minimize disruption.

## 6. Independent auditor

Where a third-party audit is used:

- the auditor must be independent;
- confidentiality obligations must apply;
- the auditor should disclose only information reasonably necessary to determine compliance;
- unrelated personal, confidential, privileged, or trade-secret information should be minimized;
- technical access must follow least-privilege principles.

## 7. Cost allocation

Default rule:

- compliant or immaterial-deviation audit: Licensor bears ordinary audit cost;
- material non-compliance: Licensee reimburses reasonable, documented verification costs causally connected to the breach, to the extent permitted by law and the signed agreement.

A commercial schedule may define a materiality threshold, for example unlicensed use of 5% or more, but the threshold must be expressly negotiated and should not be imported automatically from another company's contract.

## 8. Remediation

A verified commercial-license deficiency may require:

- cessation of unauthorized use;
- purchase or execution of sufficient commercial rights;
- correction of attribution/provenance notices;
- removal of unauthorized branding;
- delivery of a written compliance certification;
- payment of contractually due amounts;
- reimbursement of qualifying verification costs;
- preservation of evidence required for a dispute.

## 9. Nominal contractual penalty

A signed commercial instrument may include:

```text
Nominal contractual penalty:
US$ 1.00, but only where lawful for the transaction and governing law;
otherwise the local-currency amount expressly stated in the commercial schedule.
```

For Brazil-resident domestic obligations, the commercial schedule should use Brazilian currency unless a statutory exception permits foreign-currency payment.

The nominal penalty is not intended as the exclusive remedy.

## 10. Supplementary indemnification

The signed commercial instrument should expressly state, if intended:

```text
The nominal penalty is a minimum contractual amount and does not exclude
supplementary indemnification for proven loss exceeding that amount, to the
extent permitted by applicable law.
```

Potential recoverable categories, only when legally available and supported by proof/causation, may include:

- direct loss;
- unpaid license fees;
- reasonable verification/audit costs;
- forensic preservation;
- expert technical analysis;
- reasonable contractual legal fees;
- translation/notarial/registry expenses;
- other proven remediation costs.

Court-awarded costs and statutory/sucumbential attorney fees remain governed by procedural law and judicial decision.

## 11. Evidence discipline

```text
SUSPICION != BREACH
BREACH != DAMAGE_QUANTUM
AUDIT_FINDING != COURT_JUDGMENT
CONTRACTUAL_COST_ALLOCATION != AUTOMATIC_JUDICIAL_AWARD
```

## 12. Privacy and security

An audit does not authorize indiscriminate data collection.

The audit plan must specify:

- purpose;
- scope;
- systems;
- categories of data;
- retention;
- access control;
- redaction/minimization;
- destruction/return after the review where appropriate.

## R3

F_ok: audit flow is proportional, Microsoft-style in structure, but original in wording and tailored to RAFAELIA.  
F_gap: materiality threshold and retention period remain commercial-schedule variables.  
F_next: require licensed legal review before using this protocol in a real commercial agreement.
