# Legal Release Gate V1

Status: FAIL_CLOSED / claim_allowed=false

A release may be described as provenance-complete or authorial-clean only if all distributed components satisfy the applicable gates below.

## Gate A — Inventory
- every distributed file/component has object identity and source pointer;
- provenance class is A, B or E;
- C/D material is excluded from the distributable set.

## Gate B — Licensing
- applicable license identified;
- required license text/NOTICE retained;
- source/corresponding-source obligations satisfied where applicable;
- modifications are clearly identified;
- trademark permission is evaluated separately from copyright/license permission.

## Gate C — Clean-room claims
For class E only:
- independent specification exists and predates implementation;
- implementation receipt identifies authorship lineage;
- independent tests exist;
- dissimilarity review is recorded;
- known upstream code was not copied into the new implementation;
- assurance limitations are explicit.

## Gate D — Dependencies
- dependency inventory is current;
- AndroidX/Gradle/QEMU/Termux/llama-related and other third-party dependencies are classified;
- no unresolved binary/asset is silently bundled.

## Gate E — Security/privacy
- no release keystore or secret is committed;
- third-party services/data processing are inventoried;
- privacy policy/data minimization requirements are documented where applicable.

## Gate F — Evidence
- source/ref/path/blob SHA or equivalent provider identity exists;
- build/test/runtime evidence is separated;
- hashes/receipts are linked;
- `claim_allowed` remains false for unresolved fields.

## Gate G — Human/legal review boundary
If redistribution, linking, trademark, patent, privacy, or jurisdiction-specific obligations remain ambiguous, state `LEGAL_REVIEW_REQUIRED`. This engineering gate does not replace professional legal advice.

## Closure
`LEGAL_RELEASE_READY = true` only when all applicable gates A–G have explicit PASS evidence and no class C/D item remains in the release manifest.
