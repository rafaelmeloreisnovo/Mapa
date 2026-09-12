# Receipt — RAFAELIA Licensing Framework V1 — 2026-09-12

state: DRAFT_IMPLEMENTED_LEGAL_REVIEW_REQUIRED  
claim_allowed: false  
branch: legal/licensing-framework-v1-20260912  
base: d12cd080323ee4c6d5b60555dbfcbb6550c8d541  
pr: #616

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
- no fabricated "cláusula pétrea" or Súmula Vinculante;
- contributor-rights and third-party-notice controls;
- machine-readable license scope.

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

- LEGAL.md
- LICENSES/README.md
- LICENSES/LicenseRef-RAFAELIA-RNC-1.0.txt
- docs/legal/RAFAELIA_LICENSING_POLICY_V1.md
- docs/legal/ATTRIBUTION_AND_CITATION_STANDARD_V1.md
- docs/legal/AUDIT_AND_ENFORCEMENT_PROTOCOL_V1.md
- docs/legal/COMMERCIAL_LICENSE_TEMPLATE_V1.md
- docs/legal/LEGAL_BASIS_BR_V1.md
- docs/legal/LICENSE_COMPATIBILITY_MATRIX_V1.md
- docs/legal/THIRD_PARTY_NOTICES_POLICY_V1.md
- docs/legal/CONTRIBUTOR_LICENSE_AGREEMENT_TEMPLATE_V1.md
- data/legal/licensing_references.v1.json
- data/legal/license-scope-registry.v1.jsonl
- schemas/license-scope-record.v1.schema.json
- tools/validate_license_scope_registry.py
- tests/test_license_scope_registry.py

## CI observations

- changed-file Markdown regression gate: 0 issues in new legal Markdown files;
- global Markdown debt ratchet failed on historical repository debt spread (97 > 95), not because the new legal Markdown files had lint issues;
- Legal Governance Gate failed before executing legal checks because actions/checkout@v7, setup-python@v7, and upload-artifact@v7 are not pinned to full commit SHAs under repository policy;
- SecurityCodeScan, Branch Topology, main-hardening, and Human Dignity Ethics gates passed on the observed head;
- remaining provider/promotion/codescan enforcement failures are tracked separately and are not promoted to legal-package defects without causal evidence.

## Invariants

```text
EXISTING_LICENSE_GRANT != REVOCABLE_BY_NEW_NOTICE
GPL/MIT_RIGHTS != CUSTOM_RNC_RIGHTS
THIRD_PARTY_LICENSE != AUTHORIAL_INTENT
CONTRACTUAL_PENALTY != DAMAGES_CAP
CONTRACTUAL_COST_ALLOCATION != AUTOMATIC_COURT_AWARD
REPOSITORY_OWNERSHIP != COPYRIGHT_OWNERSHIP_OF_ALL_CONTENT
PULL_REQUEST != COPYRIGHT_ASSIGNMENT
```

## R3

F_ok: full draft legal framework, compatibility guards, contributor and third-party controls, and machine-readable scope registry materialized.  
F_gap: licensed-lawyer review; file-level ownership; final contributor grants; RLL/RafPolimata license state; commercial schedule variables; legal-governance workflow supply-chain pinning.  
F_next: observe successor CI after latest commits; perform file-level rights audit; do not replace root LICENSE until rights and compatibility are closed.
