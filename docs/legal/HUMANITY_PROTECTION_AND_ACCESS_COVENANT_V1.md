# RAFAELIA Humanity Protection and Access Covenant V1

**Lifecycle:** `SUPERSEDED_FOR_AUTHORIAL_SCOPE_BY_BERNE_ROLLBACK_V2`  
**Successor:** `docs/legal/BERNE_AUTHORIAL_SCOPE_ROLLBACK_V2.md`  
**Boundary:** historical covenant preserved; it no longer sets the primary direction for opening RAFAELIA-original material. Existing valid license grants remain unchanged.

Status: DRAFT_IMPLEMENTED / LEGAL_REVIEW_REQUIRED  
Adopted as governance intent: 2026-09-19  
claim_allowed: false

## 1. Purpose

Record the human intention expressed by Rafael Melo Reis that RAFAELIA should protect authorship and provenance for every human being while making eligible RAFAELIA-original knowledge as broadly accessible as law, rights authority, safety, privacy, and license compatibility allow.

This covenant is a governance layer. It is **not** a blanket relicensing instrument.

```text
BERNE_PROTECTION != LICENSE_GRANT
LICENSE_GRANT != PUBLIC_DOMAIN
COPYRIGHT != PATENT != TRADEMARK != PRIVACY_RIGHT
REPOSITORY_OWNERSHIP != COPYRIGHT_OWNERSHIP_OF_ALL_CONTENT
HUMANITY_INTENT != AUTHORITY_TO_RELICENSE_THIRD_PARTY_MATERIAL
TOKEN_VAZIO != CLEARED
```

## 2. Universal human authorship protection

RAFAELIA governance SHALL preserve, where factually and legally applicable:

- the identity or chosen attribution of every human author/contributor;
- upstream copyright and license notices;
- provenance, version, modification, and source references;
- the distinction between author, repository owner, contributor, publisher, employer/contracting party, and rights holder;
- moral-rights and attribution interests that applicable law preserves;
- the right of a person not to be falsely represented as author, endorser, or originator.

No RAFAELIA notice may erase another person's authorship or lawful upstream rights.

This protection principle is nationality-neutral and does not depend on whether a contributor is part of the RAFAELIA project.

## 3. Berne boundary

The Berne Convention protects works and authors through national treatment, automatic protection, and independence of protection in Contracting States. It is not a private license that an author can "give" to other people.

Therefore RAFAELIA implements the human intention through two distinct controls:

1. **PROTECTION:** preserve lawful authorship/provenance and do not misappropriate third-party rights.
2. **ACCESS:** grant reuse permissions only through an applicable license or other rights instrument where the licensor has authority.

## 4. Humanity access principle

For RAFAELIA-original material whose rights authority is proven, the preferred direction is broad public benefit and reuse using established standard licenses whenever practical.

No license is changed merely because this covenant exists.

A public grant requires:

```text
RIGHTS_AUDIT
-> MATERIAL_CLASS
-> THIRD_PARTY_BOUNDARY
-> PRIVACY/SECURITY_GATE
-> LICENSE_COMPATIBILITY
-> EXPLICIT_LICENSE_NOTICE
-> EFFECTIVE_VERSION/REF
-> RECEIPT
```

Previously granted GPL, MIT, Creative Commons, or other valid permissions remain in force according to their own terms.

## 5. Material-class routing

| Material class | Default governance route |
|---|---|
| Existing GPL/MIT/other licensed software | Preserve existing license; no added incompatible restriction |
| New standalone RAFAELIA-original software | Select a standard software license after dependency, patent, contributor, and copyleft-compatibility review |
| RAFAELIA-original documentation/text/figures | CC BY 4.0 is a candidate after rights and third-party review; not automatic |
| Research papers | Publisher/venue/DOI rights first; CC BY 4.0 candidate only where rights permit |
| Datasets | Dataset/database rights + privacy + consent + contractual-source audit before any public license |
| Equations, ideas, methods, facts | Do not claim copyright over the abstract idea/method/fact as such; protect/licence only copyrightable expression and other legally protectable rights where applicable |
| Third-party/mixed works | Upstream rights govern; RAFAELIA may license only its separable authorized contribution |
| Personal/sensitive/confidential data | No public grant; distribution blocked until a separate lawful gate passes |
| Credentials, secrets, exploit-enabling restricted material | No public grant by this covenant |
| Patents/trademarks/names/logos | No grant unless an explicit separate instrument says otherwise |

## 6. Non-discrimination and humanity scope

When an eligible work is deliberately released under a standard public license, access is offered under that license's terms without creating a separate nationality, ethnicity, religion, political, economic, or geographic eligibility rule.

This clause does not override sanctions, export controls, court orders, privacy law, platform rules, or other mandatory law that may apply to a particular transaction or distribution channel.

## 7. Commercial-use boundary

This covenant does not silently decide commercial rights.

```text
COMMERCIAL_USE = DETERMINED_BY_APPLICABLE_LICENSE_OR_SIGNED_INSTRUMENT
```

Existing licenses that already permit commercial use keep doing so. Material under a valid non-commercial license remains non-commercial unless the rights holder issues an additional permission.

## 8. Safety, privacy, and dignity

"Access for humanity" does not mean publishing material that exposes private persons, credentials, security secrets, regulated data, or content that RAFAELIA lacks authority to distribute.

The least-restrictive lawful release that preserves human dignity, security, provenance, and third-party rights is preferred.

## 9. Operational gates

A release claiming conformance with this covenant must have evidence for:

- material identity and canonical ref;
- rights-holder/licensor authority;
- contributor-rights status;
- third-party inventory;
- applicable license;
- patent/trademark boundary where relevant;
- privacy/security classification where relevant;
- modification/provenance notice;
- release ref/hash;
- receipt.

Unknown fields remain `TOKEN_VAZIO` and block only the affected grant, not unrelated cleared material.

## 10. Conflict rule

If this covenant conflicts with a valid upstream license, signed agreement, court order, mandatory law, privacy duty, or third-party right, the higher-authority legal obligation governs that scope.

This covenant MUST NOT be interpreted to withdraw rights already validly granted to recipients.

## 11. Human-readable invariant

> Protect every human author's origin. Open only what we have the right and duty to open. Preserve every valid grant already made. Never turn uncertainty into permission.

## R3

F_ok: universal authorship/provenance protection and broad-access intent are separated into legally safer control layers.  
F_gap: file-level rights authority, contributor grants, patent/trademark status, privacy classification, and commercial policy remain repository/material-specific.  
F_next: validate the machine-readable humanity policy and expand the license-scope registry only from observed repository/file evidence.
