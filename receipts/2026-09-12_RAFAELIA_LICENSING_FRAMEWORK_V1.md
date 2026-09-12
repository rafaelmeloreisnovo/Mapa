# Receipt — RAFAELIA Licensing Framework V1 — 2026-09-12

state: DRAFT_IMPLEMENTED_LEGAL_REVIEW_REQUIRED
claim_allowed: false
branch: legal/licensing-framework-v1-20260912
base: d12cd080323ee4c6d5b60555dbfcbb6550c8d541

## Intent

Create a professional licensing architecture with:

- mandatory attribution and bibliography;
- canonical author/provenance reference;
- non-commercial public license for eligible RAFAELIA-original material;
- separate written commercial licensing;
- audit/compliance terms;
- nominal US$1 concept where lawful, without making it a damages cap;
- allocation of reasonable breach-related verification/enforcement costs;
- real statutory/jurisprudential anchors;
- no fabricated "cláusula pétrea" or Súmula Vinculante.

## Source observations

- Mapa root LICENSE = GPLv3.
- papers root LICENSE = MIT.
- RafPolimata root LICENSE not found in bounded check.
- RLL root LICENSE not found in bounded check.
- Drive Canon V1 already states repository ownership != copyright ownership of all content and license permission != trademark permission.
- RLL integrity charter already requires SPDX where possible, third-party license review, and separate commercial instruments.

## Legal anchors

- Constitution art. 5 XXVII-XXVIII.
- Laws 9.610/1998 and 9.609/1998.
- Civil Code arts. 389, 408-416, 421-425.
- CPC art. 85.
- Law 14.286/2021 art. 13.
- STJ software-license/copyright precedents.
- STF Theme 1403 as a repercussion-general reference, not mislabeled as a Súmula Vinculante.
- Microsoft licensing structure used only as drafting architecture reference.

## Materialized artifacts

- docs/legal/RAFAELIA_LICENSING_POLICY_V1.md
- LICENSES/LicenseRef-RAFAELIA-RNC-1.0.txt
- docs/legal/ATTRIBUTION_AND_CITATION_STANDARD_V1.md
- docs/legal/AUDIT_AND_ENFORCEMENT_PROTOCOL_V1.md
- docs/legal/COMMERCIAL_LICENSE_TEMPLATE_V1.md
- docs/legal/LEGAL_BASIS_BR_V1.md
- docs/legal/LICENSE_COMPATIBILITY_MATRIX_V1.md

## Invariants

```text
EXISTING_LICENSE_GRANT != REVOCABLE_BY_NEW_NOTICE
GPL/MIT_RIGHTS != CUSTOM_RNC_RIGHTS
THIRD_PARTY_LICENSE != AUTHORIAL_INTENT
CONTRACTUAL_PENALTY != DAMAGES_CAP
CONTRACTUAL_COST_ALLOCATION != AUTOMATIC_COURT_AWARD
REPOSITORY_OWNERSHIP != COPYRIGHT_OWNERSHIP_OF_ALL_CONTENT
```

## R3

F_ok: complete draft framework and compatibility boundary materialized.  
F_gap: licensed-lawyer review; file-level ownership; contributor grants; RLL/RafPolimata root-license state; commercial schedule variables.  
F_next: open draft PR; append Drive canon pointer; do not replace root LICENSE until file-level rights audit is complete.
