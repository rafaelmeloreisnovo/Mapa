# RAFAELIA Third-Party Notices Policy V1

Status: DRAFT_AUDITABLE

## 1. Rule

No RAFAELIA license notice may erase or replace third-party rights information.

```text
RAFAELIA_NOTICE + UPSTREAM_LICENSE + COPYRIGHT_NOTICE + REQUIRED_NOTICE
```

must coexist where applicable.

## 2. Required inventory fields

For every external component/material:

- component/material name;
- source repository/URL;
- exact version/tag/commit/hash when available;
- upstream author/copyright holder;
- upstream license and version;
- destination path inside RAFAELIA;
- what was copied, adapted, linked, translated, or derived;
- modifications made;
- NOTICE/attribution obligations;
- source-code/distribution obligations;
- patent/trademark clauses where applicable;
- compatibility with intended RAFAELIA distribution;
- evidence/ref/hash;
- unresolved gap;
- required action.

Unknown values are `TOKEN_VAZIO`.

## 3. Prohibited practice

Do not:

- replace an upstream copyright notice with Rafael Melo Reis;
- state "all rights owned by RAFAELIA" for a mixed work;
- apply LicenseRef-RAFAELIA-RNC-1.0 to GPL-covered code as an added non-commercial restriction;
- remove MIT/Apache/BSD/GPL notices;
- treat a fork or refactor as new authorship;
- treat repository ownership as copyright ownership.

## 4. Distribution gate

A distributable package must include a third-party notice bundle when required.

Minimum:

```text
THIRD_PARTY_NOTICES.md
LICENSES/
SBOM or dependency inventory
source-offer/corresponding-source pointer where required
copyright/attribution notices
```

## 5. Conflict handling

If a RAFAELIA term conflicts with an upstream license governing a component:

```text
UPSTREAM_COMPONENT -> UPSTREAM_LICENSE_GOVERNS
RAFAELIA_CUSTOM_TERM -> DOES_NOT_ATTACH_TO_THAT_COMPONENT
```

unless a valid separate rights grant authorizes otherwise.

## R3

F_ok: third-party provenance is mandatory and independent from RAFAELIA authorship.  
F_gap: repository-by-repository NOTICE inventory remains incomplete.  
F_next: generate THIRD_PARTY_NOTICES from a verified component ledger, not from repository names alone.
