# Legal Basis — Brazil — RAFAELIA Licensing V1

Status: RESEARCH / LEGAL_REVIEW_REQUIRED  
Cutoff: 2026-09-12

This file records legal anchors. It is not a legal opinion.

## 1. Constitutional anchors

### Constitution, art. 5, XXVII

Authors have the exclusive right to use, publish, or reproduce their works for the statutory term.

### Constitution, art. 5, XXVIII(b)

Creators are guaranteed, according to law, the right to oversee the economic exploitation of works they created or participated in.

Operational significance: commercial licensing and accounting/audit clauses should be drafted around actual rights and evidence, not merely repository possession.

## 2. Copyright Law — Law 9.610/1998

Relevant provisions:

- art. 4: copyright transactions are interpreted restrictively;
- art. 7: protects literary, artistic, scientific works and computer programs, subject to software-specific law;
- art. 22: moral and economic rights belong to the author;
- art. 24(I)-(II): authorship claim and name indication rights for general copyrighted works;
- art. 27: moral rights are inalienable and non-waivable for works governed by this regime;
- art. 28: exclusive right to use, enjoy, and dispose of the work;
- art. 29: reproduction, editing, adaptation, distribution and other forms of use require prior express authorization unless an exception applies;
- art. 49: author rights may be transferred/licensed subject to statutory limits;
- art. 50: total or partial assignment must be in writing and state essential scope conditions;
- arts. 102-107: civil remedies for unauthorized reproduction/use and rights-management interference.

Important limit: ideas, systems, methods, mathematical concepts as such, and scientific/technical content as such are not protected by copyright in the same way as their expressive form. The licensing package must distinguish expression/code/documentation from abstract method or scientific truth claims.

## 3. Software Law — Law 9.609/1998

Key provisions:

- art. 2: software protection follows the copyright regime applicable to literary works, subject to this special law;
- art. 2 §1: most general moral-right rules do not apply to software, but the author's right to claim paternity remains, as does the right to oppose certain reputation-harming unauthorized modifications;
- art. 2 §3: protection does not depend on registration;
- art. 2 §5: the author/rightsholder has the exclusive right to authorize or prohibit commercial rental;
- art. 9: use of software in Brazil is subject to a license contract; a fiscal document may prove lawful use when there is no contract;
- art. 10: commercial licensing contracts for foreign-origin software must allocate certain taxes/charges, and some clauses are statutorily null;
- art. 12: copyright infringement involving software has criminal provisions, including commercial reproduction without express authorization;
- art. 14: civil action may seek cessation, monetary penalty, and cumulative losses/damages as permitted by law.

## 4. Civil Code — contractual architecture

Relevant provisions:

- art. 389: breach may give rise to losses/damages, interest, monetary adjustment, and attorney fees;
- arts. 408-416: contractual penalty regime;
- art. 412: penalty cannot exceed the principal obligation;
- art. 413: courts must reduce a penalty when partial performance or manifest excess makes reduction appropriate;
- art. 416: a conventional penalty can be demanded without proving damage; supplementary indemnification exceeding the penalty requires express contractual provision, and the creditor must prove the excess;
- art. 421: contractual freedom operates within the social function of the contract;
- art. 421-A: civil/business contracts are presumed symmetric in the stated circumstances, may define objective interpretation/revision parameters, and risk allocation should generally be respected;
- art. 422: objective good faith and probity apply;
- art. 425: atypical contracts are permitted subject to general legal rules.

Therefore:

```text
"ALL COSTS AUTOMATICALLY DUE"
!=
LEGALLY GUARANTEED RESULT
```

A better clause expressly allocates reasonable/documented/causally connected costs, preserves proof requirements, and distinguishes contractual fees from judicially awarded costs.

## 5. Civil Procedure Code

CPC art. 85 provides that the losing party may be ordered to pay attorney fees and defines judicial criteria/percentages.

This is a procedural/judicial consequence. A private license cannot predetermine the court's statutory fee award.

Contractual legal-cost reimbursement should therefore be drafted as a separate contractual obligation, to the extent legally valid, rather than falsely describing it as automatic statutory sucumbential fees.

## 6. Foreign-currency clause

Law 14.286/2021, art. 13 permits foreign-currency payment for specified categories and provides that a foreign-currency payment clause outside permitted cases is null.

Accordingly, a universal "US$ 1" payment obligation is unsafe for every Brazil-only contract.

Recommended architecture:

- international/permitted transaction: US$ 1.00 where lawful;
- domestic Brazil schedule: state the nominal penalty in BRL;
- never treat the dollar denomination as jurisdiction-independent.

## 7. Jurisprudential anchors

### STJ — REsp 443.119/RJ

The STJ recognized software as protected under the copyright regime and addressed material damages for unauthorized commercial reproduction/distribution.

### STJ — REsp 1.911.383/RJ

The STJ examined a software license and emphasized the need to read the actual contractual grant before characterizing distribution as unauthorized; breach/damages cannot be inferred merely from a broad allegation.

### STJ — contractual loss proof

The STJ has held that breach of an accessory contractual obligation does not automatically justify damages without proof of loss and causation.

### STJ — REsp 1.907.034 (reported 2026)

The STJ reported that contractual claims involving alleged breach of a software-license clause fall under the ten-year general prescription period in the circumstances analyzed, rather than automatically becoming a three-year extra-contractual copyright claim.

### STJ — art. 416 line

STJ jurisprudence recognizes that supplementary damages beyond a contractual penalty require express contractual reservation and proof of the excess under Civil Code art. 416, sole paragraph.

### STF — Theme 1403

The STF recognized general repercussion regarding creators' oversight of economic exploitation of intellectual works on digital platforms.

As of the current research snapshot, this is a repercussion-general theme and must not be mislabeled as a binding precedent thesis if the merits thesis has not been finally established.

## 8. Súmula vinculante status

No directly applicable STF **Súmula Vinculante** was identified in this research for the specific package of:

- software/copyright license;
- mandatory author attribution;
- non-commercial field-of-use restriction;
- commercial audit;
- nominal contractual penalty;
- reimbursement of audit/legal costs.

Therefore the licensing documents must not invent or cite a nonexistent Súmula Vinculante.

Use actual statutes, contractual doctrine, and identified case law.

```text
SÚMULA_VINCULANTE_APLICÁVEL = TOKEN_VAZIO_NONE_FOUND
```

## 9. Microsoft-style structural comparison

Microsoft's current licensing materials use layered structures such as:

- master agreement;
- Product Terms / Use Rights;
- product-specific terms;
- compliance verification;
- records/self-audit/independent audit;
- remediation for unlicensed use.

RAFAELIA may adopt the **structural idea** of modular terms and compliance verification.

It should not copy Microsoft's text or imply Microsoft approval/affiliation.

## 10. Primary references

1. Constituição da República Federativa do Brasil de 1988, art. 5, XXVII-XXVIII.
2. Lei 9.610/1998 — Direitos Autorais.
3. Lei 9.609/1998 — Programa de Computador.
4. Lei 10.406/2002 — Código Civil, especially arts. 389, 408-416, 421-425.
5. Lei 13.105/2015 — CPC, especially art. 85.
6. Lei 14.286/2021 — foreign-currency obligations, art. 13.
7. INPI — Programa de Computador, legislation/registration guidance.
8. STJ — REsp 443.119/RJ.
9. STJ — REsp 1.911.383/RJ.
10. STJ — REsp 1.907.034, reported 2026.
11. STF — Tema 1403 (economic exploitation oversight of intellectual works).
12. Microsoft Product Terms / Licensing Resources — structural reference only.
13. GNU GPLv3 and GNU GPL FAQ — further restrictions / commercial-use compatibility.
14. OSI — MIT License.

## R3

F_ok: statutory and jurisprudential foundation mapped with limits.  
F_gap: contract-specific governing law, party status, tax, arbitration/forum, and consumer/adhesion analysis require licensed counsel.  
F_next: legal counsel should review the commercial template before execution with a counterparty.
