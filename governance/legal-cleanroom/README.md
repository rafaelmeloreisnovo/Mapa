# RAFAELIA Legal / Authorship / Clean-Room Control Plane V1

State: `CANONICAL_DRAFT / FAIL_CLOSED / release_allowed=false / legal_compliance_claim=false`

## Purpose

This directory is the federated authority for distinguishing **original RAFAELIA authorship**, **licensed third-party/derivative material**, **clean-room reimplementations**, and **quarantined/unknown-rights material**. It does not rewrite history and cannot erase upstream copyright, license, trademark, patent, attribution, source-offer, NOTICE, or other obligations.

Core invariant:

`IDEA/DOMAIN != EXPRESSION/CODE != DERIVATIVE_WORK != CLEANROOM_IMPLEMENTATION != LEGAL_CLEARANCE`

`NEW_AUTHORSHIP_OF_MODIFICATIONS != OWNERSHIP_OF_UPSTREAM`

`RENAME != LICENSE_RESET`

`REIMPLEMENTED != NON_DERIVATIVE` unless the clean-room gate is actually evidenced.

## Mandatory source classes

- `A_ORIGINAL_RAFAELIA`: authorship/provenance sufficiently evidenced for the specific artifact.
- `B_THIRD_PARTY_LICENSED`: external material retained under its applicable license/notice obligations.
- `C_RIGHTS_UNRESOLVED`: source/rights/license incomplete; distribution blocked.
- `D_DERIVATION_RISK`: suspicious or insufficiently separated implementation; quarantine/reimplementation required.
- `E_CLEANROOM_CANDIDATE`: independent specification exists but implementation gate incomplete.
- `F_CLEANROOM_VERIFIED_SCOPED`: independent specification + independent implementation + tests + provenance + similarity review completed in the stated scope.

No class may be inferred from filename, repository ownership, commit author, or rename alone.

## Clean-room method

1. Forensic inventory: `repo/ref/path/blob_sha/content_hash/origin/license/notice/risk`.
2. Freeze C/D material from release surfaces.
3. Produce functional specification from public interfaces, standards, documented behavior, and legally usable references; do not copy implementation expression.
4. Separate specification and implementation evidence. Where practical, implementation authors should not consult quarantined legacy source while implementing.
5. Build the replacement from zero under a declared original architecture and coding contract.
6. Execute independent tests against behavior/invariants, not against copied structure.
7. Perform structural/textual/naming similarity review; suspicious overlap reopens D.
8. Bind a `LEGAL_TECHNICAL_RECEIPT` and source hashes.
9. Release only after component-specific license/notice/trademark/privacy/security gates close.

## Upstream authority rule

Official/upstream repositories and their license files have authority over their own terms. RAFAELIA may add stricter internal release gates, but it must not reinterpret an upstream license to remove obligations or claim upstream authorship.

## Product naming

The existing name `Vectras VM` is treated as an upstream/legacy identifier. The provisional clean-room product codename is **RAFAELIA Virtual Runtime (RVR)**. This is only a technical working name:

`trademark_clearance = TOKEN_VAZIO`

No automatic repo rename, package rename, public release, or claim of trademark availability is authorized by this document.

## Architecture boundary

The Android application shell is not a freestanding environment and may necessarily use Android/Java/Kotlin/Gradle and licensed upstream components. **Original RAFAELIA low-level kernels** may use the stricter `FREESTANDING_KERNEL_PROFILE_V1` contract. Do not falsely label Android framework code as freestanding.

## Release gate

A release candidate is blocked if any shipped artifact has:

- missing origin or license;
- unresolved required attribution/NOTICE;
- missing corresponding-source obligation where applicable;
- rights-unknown binary/asset;
- clean-room claim without evidence;
- trademark/name clearance marked TOKEN_VAZIO for a new public brand;
- privacy/data-processing obligations not assessed when the feature processes user/account data;
- secret/keystore committed as distributable source material;
- `claim_allowed=true` without a legal-technical receipt.

This control plane is an engineering/compliance framework, not legal advice or a declaration of legal compliance.
