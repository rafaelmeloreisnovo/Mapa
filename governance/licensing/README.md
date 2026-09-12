# RAFAELIA — Licensing Governance

**Status:** `DRAFT_COUNSEL_REVIEW_REQUIRED`  
**Version:** `2.0.0-draft`  
**Canonical language:** Portuguese (Brazil)  
**claim_allowed:** `false`

## Purpose

This directory separates five legal surfaces that must not be collapsed:

```text
ORIGINAL RAFAELIA WORK
!=
THIRD-PARTY MATERIAL
!=
LICENSE GRANT
!=
COMMERCIAL AUTHORIZATION
!=
ENFORCEMENT / REMEDIES
```

The documents here are a governance draft for legal review. They do not silently relicense third-party code, inherited forks, datasets, papers, images, fonts, dependencies, or other material whose rights are controlled by someone else.

## Canonical package

- `RAFAELIA_ORIGINAL_WORKS_NC_ATTRIBUTION_LICENSE_V1_PTBR.md` — default non-commercial license for original RAFAELIA material.
- `ATTRIBUTION_AND_CITATION_STANDARD_V1.md` — mandatory author/project/citation format.
- `COMMERCIAL_LICENSE_FRAMEWORK_V1.md` — separate written authorization path for commercial use.
- `THIRD_PARTY_LICENSE_BOUNDARY_V1.md` — inherited-license and NOTICE boundary.
- `LEGAL_BASIS_AND_REFERENCES_V1.md` — legal basis, jurisprudence, international references, and structural comparison with Microsoft terms.
- `NOTICE_TEMPLATE_V1.md` — repository/package NOTICE template.
- `LICENSE_DEPLOYMENT_MANIFEST_V1.json` — machine-readable rollout contract.

## Non-negotiable drafting invariants

1. Attribution is mandatory for licensed use of original RAFAELIA material.
2. Commercial use is prohibited unless a separate written commercial license expressly authorizes it.
3. No custom RAFAELIA license overrides a third-party license.
4. Source, authorship, version, modification status, and license pointer must remain reconstructible.
5. Removal or falsification of rights-management information is prohibited.
6. Breach does not erase statutory copyright remedies.
7. The Licensor's aggregate liability under the free license is capped at the greater of the amount paid under the license and USD 1.00, only to the maximum extent permitted by mandatory law.
8. The liability cap does not cap the infringer/licensee's liability for unauthorized commercial exploitation, copyright infringement, fraud, willful misconduct, breach of confidentiality, or indemnity obligations where applicable.
9. Enforcement-cost clauses are limited to amounts recoverable under applicable law and to reasonable/documented extrajudicial audit and enforcement costs; statutory court costs and fee awards remain governed by procedural law.
10. No document here is described as a constitutional "cláusula pétrea", and no nonexistent binding precedent is cited.

## Adoption model

This package is a **control-plane policy**. Repository-by-repository adoption requires:

```text
path inventory
→ authorship / rights authority
→ third-party license map
→ compatibility review
→ NOTICE
→ license pointer
→ CI validation
→ receipt
```

A public repository being owned by the author does not prove that every file is exclusively authored by the repository owner.

## Legal review gate

Before production adoption or commercial contracting, review is required by qualified intellectual-property counsel in the relevant jurisdiction.

