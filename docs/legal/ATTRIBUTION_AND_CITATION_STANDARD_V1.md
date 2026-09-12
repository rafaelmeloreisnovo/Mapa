# RAFAELIA Attribution and Citation Standard V1

Status: DRAFT_FOR_LEGAL_REVIEW

## 1. Purpose

This standard makes authorship, citation, version identity, and third-party provenance reconstructible.

It applies only where incorporated by the applicable license or contract.

## 2. Minimum attribution block

```text
Author: Rafael Melo Reis
Project: RAFAELIA
Title: <artifact/work title>
Canonical source: <repository/URL/DOI>
Version/Revision: <version/release/commit SHA/DOI>
License: <SPDX identifier or LicenseRef>
Modified by: <name/entity or "unmodified">
Modification date: <YYYY-MM-DD or precise timestamp when available>
Third-party notices: <pointer>
```

## 3. Mandatory bibliographic reference

For papers, reports, presentations, books, datasets, documentation, websites, or academic derivative work, include a full bibliographic citation using a recognized citation style.

Recommended machine-readable fields:

```yaml
author: Rafael Melo Reis
title: TOKEN_VAZIO
project: RAFAELIA
year: TOKEN_VAZIO
version: TOKEN_VAZIO
repository: TOKEN_VAZIO
commit: TOKEN_VAZIO
doi: TOKEN_VAZIO
url: TOKEN_VAZIO
accessed: TOKEN_VAZIO
license: TOKEN_VAZIO
modified: false
third_party_notices: TOKEN_VAZIO
```

Unknown metadata remains `TOKEN_VAZIO`; it must not be invented.

## 4. Biographical reference

If the distributed Work includes a canonical author biography or author-identification page, the attribution must preserve its canonical reference.

The biographical reference is for identity/provenance only. It must not imply:

- endorsement;
- sponsorship;
- employment;
- certification;
- institutional partnership.

## 5. Modification transparency

A modified artifact must say that it was modified and must identify the modifier and modification date where reasonably practicable.

A derivative must not be presented as the original author's unchanged work.

## 6. Third-party separation

RAFAELIA attribution never replaces upstream attribution.

```text
RAFAELIA_AUTHORSHIP_NOTICE
+
UPSTREAM_NOTICE
+
THIRD_PARTY_LICENSE_NOTICE
```

must remain separate when applicable.

## 7. Software source headers

For files explicitly placed under the RAFAELIA custom license, a recommended header is:

```text
Copyright (c) <year> Rafael Melo Reis
Project: RAFAELIA
License: LicenseRef-RAFAELIA-RNC-1.0
Canonical source: <repo/path>
Commercial use requires a separate written license.
See: docs/legal/RAFAELIA_LICENSING_POLICY_V1.md
```

Do not place this header on GPL/MIT/third-party code unless the rights audit confirms that doing so is accurate and compatible.

## 8. Legal basis note

Brazilian copyright law recognizes the author's right to claim authorship and, for general works, to have the author's name indicated in use of the work. Software has a specific statutory regime in which the right to claim paternity remains protected.

This standard is designed to operationalize that authorship/provenance interest while preserving upstream rights.

## R3

F_ok: citation and biographical attribution requirements are machine- and human-readable.  
F_gap: canonical public biography URI/ORCID/DOI is not hard-coded until formally selected.  
F_next: create or designate one canonical author-identity page and add CITATION.cff only after repository-specific license scope is resolved.
