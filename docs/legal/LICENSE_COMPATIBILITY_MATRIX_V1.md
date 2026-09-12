# RAFAELIA License Compatibility Matrix V1

Status: DRAFT_AUDITABLE / FAIL_CLOSED

## 1. Rule

No repository-wide relicensing occurs from preference alone.

```text
RIGHTS_HOLDER_AUTHORITY
+
UPSTREAM_LICENSE_COMPATIBILITY
+
CONTRIBUTOR_RIGHTS
+
FILE_SCOPE
=
RELICENSING_GATE
```

If any factor is unknown: `TOKEN_VAZIO_LICENSE_SCOPE`.

## 2. Observed current surfaces

| Repository/surface | Observed license state | Commercial use under current license | Can RAFAELIA-RNC simply replace it? | State |
| --- | --- | --- | --- | --- |
| rafaelmeloreisnovo/Mapa root | GPL-3.0 text at root | Yes, subject to GPL | No, not for existing GPL-covered work merely by adding a non-commercial restriction | BLOCKED_FOR_BLANKET_RELICENSE |
| rafaelmeloreisnovo/papers root | MIT | Yes | Not retroactively for previously distributed MIT versions; future wholly-owned materials can be separately licensed if scoped | REVIEW_REQUIRED |
| rafaelmeloreisnovo/RafPolimata root | LICENSE not found in bounded check | TOKEN_VAZIO | No | TOKEN_VAZIO_LICENSE |
| instituto-Rafael/relativity-living-light root | LICENSE not found in bounded check | TOKEN_VAZIO | No | TOKEN_VAZIO_LICENSE |
| third-party/imported components | component-specific | component-specific | Never by RAFAELIA notice alone | THIRD_PARTY_GOVERNS |

## 3. GPL boundary

GNU GPLv3 permits commercial distribution/use subject to its terms and generally bars adding further restrictions outside the limited categories it permits.

Therefore:

```text
GPL_COVERED_WORK + NO_COMMERCIAL_RESTRICTION
= INCOMPATIBLE_APPROACH
```

The custom RAFAELIA non-commercial license must not be presented as restricting rights already granted by GPLv3.

File-level original material may be separately licensed only where legally and technically separable and where all rights needed for that licensing choice are controlled.

## 4. MIT boundary

MIT expressly permits use, modification, distribution, sublicensing, and sale subject to preservation of its notice.

A later policy cannot claw back those permissions from copies already received under MIT.

For new versions/material:

- verify ownership;
- verify contributor grants;
- define effective version/date;
- keep old version history;
- do not misstate retroactive effect.

## 5. Dual licensing

Where RAFAELIA owns all necessary rights, dual licensing may be possible:

```text
PUBLIC_LICENSE_A
OR
SEPARATE_COMMERCIAL_LICENSE_B
```

But dual licensing cannot eliminate upstream obligations in third-party-derived material.

## 6. Contribution governance

Before accepting contributions to material intended for commercial dual licensing, use one of:

- a contributor license agreement reviewed by counsel;
- a copyright assignment reviewed by counsel;
- a Developer Certificate of Origin plus a license model that does not require rights beyond the contribution grant.

Do not assume a GitHub pull request transfers copyright ownership.

## 7. File-level metadata

Recommended:

```text
SPDX-License-Identifier: GPL-3.0-only
SPDX-License-Identifier: MIT
SPDX-License-Identifier: LicenseRef-RAFAELIA-RNC-1.0
```

Only one that is factually applicable should be placed on a given file unless an explicit dual-license expression is intended and valid.

## 8. Release gate

No release under the custom license until:

- file-level inventory complete;
- third-party notices complete;
- authorship/control documented;
- contributor rights documented;
- SPDX/LicenseRef metadata correct;
- README/license scope matches packaged files;
- commercial/non-commercial boundary reproducible.

## R3

F_ok: blanket relicensing hazards identified.  
F_gap: RafPolimata/RLL licensing and file-level ownership remain unresolved.  
F_next: perform component-by-component rights audit before changing any root license.
