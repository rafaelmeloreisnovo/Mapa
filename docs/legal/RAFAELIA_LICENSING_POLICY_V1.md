# RAFAELIA Licensing Policy V1

Status: DRAFT_FOR_LEGAL_REVIEW  
Effective only when explicitly adopted by file/repository notice or signed instrument.  
This document is not legal advice and does not retroactively alter rights already granted under GPL, MIT, or other licenses.

## 1. Purpose

This policy separates:

1. existing third-party and open-source license obligations;
2. RAFAELIA-original material that may be placed under a custom research/non-commercial license;
3. commercial permissions that require a separate written instrument;
4. attribution, provenance, audit, and enforcement obligations.

Core invariant:

```text
REPOSITORY_OWNERSHIP != COPYRIGHT_OWNERSHIP_OF_ALL_CONTENT
EXISTING_LICENSE_GRANT != REVOCABLE_BY_NEW_NOTICE
GPL/MIT_RIGHTS != RAFAELIA_RNC_RIGHTS
THIRD_PARTY_LICENSE != AUTHORIAL_INTENT
```

## 2. Current repository boundary

The current root `LICENSE` of `rafaelmeloreisnovo/Mapa` is GNU GPL v3. Existing GPL-covered material remains governed by GPLv3. A non-commercial restriction MUST NOT be added to GPL-covered material where that would create a prohibited further restriction.

The repository `rafaelmeloreisnovo/papers` currently contains an MIT license. Versions already distributed under MIT retain the rights granted under that license, including commercial rights.

Therefore the custom RAFAELIA license may apply only to material for which all of the following are true:

- the relevant copyright rights are controlled by the RAFAELIA licensor;
- the material is not required to remain under an incompatible upstream license;
- the file or artifact contains an explicit license notice;
- the scope matrix identifies the applicable license;
- third-party notices are preserved.

Unknown ownership or compatibility is `TOKEN_VAZIO_LICENSE_SCOPE` and blocks relicensing.

## 3. License architecture

```text
BASE RIGHTS LAYER
  -> upstream / GPL / MIT / third-party obligations

RAFAELIA AUTHORIAL LAYER
  -> LicenseRef-RAFAELIA-RNC-1.0
  -> research/non-commercial permissions only

COMMERCIAL LAYER
  -> separate written commercial license
  -> signed or otherwise formally accepted instrument
  -> commercial field-of-use, term, territory, fees, audit, remedies

ATTRIBUTION LAYER
  -> author identity
  -> bibliographic citation
  -> source/revision
  -> modification notice
  -> third-party provenance

AUDIT / ENFORCEMENT LAYER
  -> records
  -> self-audit or independent audit
  -> proportional access
  -> confidentiality
  -> remediation
  -> reasonable verification costs upon material non-compliance
```

This modular structure is inspired by large commercial licensing programs that separate master terms, use rights, product-specific terms, and compliance verification, without copying their text.

## 4. Essential contractual conditions

For material explicitly licensed under `LicenseRef-RAFAELIA-RNC-1.0`, the following are essential conditions:

1. attribution and bibliographic citation;
2. preservation of provenance and legal notices;
3. no commercial use without a separate written commercial license;
4. no sublicense beyond the permissions expressly granted;
5. no false authorship, false endorsement, or origin misrepresentation;
6. no removal or falsification of rights-management metadata;
7. audit cooperation within the bounded protocol when commercial or institutional use is claimed;
8. prompt cessation and remediation after a material breach notice;
9. preservation of third-party license obligations;
10. no trademark rights unless separately granted.

These are called **Essential Conditions**, not "cláusulas pétreas". In Brazilian constitutional law, "cláusulas pétreas" is a constitutional concept; using that expression for a private license would be technically misleading.

## 5. Attribution rule

Where the RAFAELIA custom license applies, reuse must include a human-readable attribution containing at least:

- author: Rafael Melo Reis;
- work/artifact title;
- project: RAFAELIA;
- repository or canonical source;
- version, release, commit SHA, DOI, or equivalent when available;
- applicable license;
- statement of modifications;
- bibliographic citation in a recognized style;
- third-party notices and upstream attributions where applicable.

Attribution must not imply endorsement.

## 6. Commercial-use rule

"Commercial Use" includes use primarily intended for monetary compensation, paid products or services, resale, sublicensing for consideration, paid consulting deliverables, commercial hosting, commercialization, internal use materially supporting revenue-generating operations when specified in the commercial schedule, or incorporation into a commercial product.

For RAFAELIA-RNC material:

```text
COMMERCIAL_USE -> SEPARATE_WRITTEN_LICENSE_REQUIRED
NO_WRITTEN_COMMERCIAL_LICENSE -> NO_COMMERCIAL_PERMISSION
```

A repository clone, public availability, citation, or technical access is not itself a commercial license.

## 7. Nominal penalty and supplementary loss

The commercial license template uses a nominal contractual penalty of **US$ 1.00 where legally permissible**, or the lawful domestic-currency equivalent/specified local amount where payment in foreign currency is not permitted.

The nominal amount is not intended to cap damages.

Any supplementary recovery must be expressly provided in the signed commercial instrument and remains subject to applicable law, proof, causation, proportionality, judicial control, and mandatory legal limits.

## 8. Costs of enforcement and audit

The commercial template may allocate to a materially non-compliant licensee the reasonable and documented costs causally connected to verification and enforcement, including:

- independent compliance audit;
- forensic preservation and technical analysis;
- expert assistance;
- certified translations, notarization, or registry fees when necessary;
- contractual legal fees where legally recoverable;
- remediation and license true-up costs.

Court costs and statutory/sucumbential attorney fees are governed by procedural law and the court; this policy does not purport to bind the judiciary.

Clean audits are ordinarily borne by the licensor unless the signed instrument validly provides otherwise.

## 9. No automatic retroactive relicensing

No file changes license merely because this policy exists.

A license transition requires:

```text
RIGHTS_AUDIT
-> FILE_SCOPE
-> UPSTREAM_COMPATIBILITY
-> COPYRIGHT_AUTHORITY
-> NOTICE
-> EFFECTIVE_VERSION
-> RECEIPT
```

Previously distributed copies keep the rights already granted under their applicable licenses, subject to those licenses.

## 10. Consumer and adhesion boundary

Any commercial template must be separately reviewed before use in consumer, employment, public-sector, educational, or adhesion contexts.

Nothing in this policy overrides mandatory law, consumer protection, competition law, privacy/data-protection law, labor law, public procurement law, or court powers to review abusive or disproportionate terms.

## 11. Required legal package

Canonical legal package:

- `LICENSES/LicenseRef-RAFAELIA-RNC-1.0.txt`
- `docs/legal/ATTRIBUTION_AND_CITATION_STANDARD_V1.md`
- `docs/legal/COMMERCIAL_LICENSE_TEMPLATE_V1.md`
- `docs/legal/AUDIT_AND_ENFORCEMENT_PROTOCOL_V1.md`
- `docs/legal/LEGAL_BASIS_BR_V1.md`
- `docs/legal/LICENSE_COMPATIBILITY_MATRIX_V1.md`

## R3

F_ok: scope-safe licensing architecture defined without overwriting GPL/MIT rights.  
F_gap: file-level rights ownership, contribution grants, and third-party inventory remain repository-specific.  
F_next: complete file-level license scope audit before changing any root LICENSE or applying the custom license to existing code.
