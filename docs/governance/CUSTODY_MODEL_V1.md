# RAFAELIA Custody Model V1

## Core distinction

`AUTHORIZATION != PLANNING != EXECUTION != CUSTODY != OBSERVATION != CLAIM_PROMOTION`.

For a user↔assistant↔connector action: the human user authorizes scope; the assistant may plan/request within that scope; the connector/provider executes the external operation; Drive/GitHub/runtime remains custodian of authoritative external state; readback/logs produce evidence; claim promotion remains a separate human/domain gate.

An assistant session is therefore not silently treated as owner, custodian, cryptographic signer, or claim authority.

## Nine custody classes

C01 source/origin · C02 document state · C03 code/repository state · C04 execution · C05 evidence/receipt · C06 authorization/handoff · C07 claim promotion · C08 cross-provider bridge · C09 credential/permission authority.

Machine details: `data/governance/custody/00_INDEX/custody_types_v1.json`.

## Identity semantics

Do not use one generic hash concept for distinct identity systems.

- Git commit/blob OID = provider-native Git object identity. Do not call it SHA-256 unless the repository object format independently proves that.
- Drive revision ID = provider revision identity, not a cryptographic digest.
- Provider request/run ID = operation identity.
- Content digest = explicit algorithm over declared bytes.
- Receipt digest = explicit algorithm plus versioned canonicalization over declared receipt bytes.

A predecessor digest creates a linear hash-linked chain. It is not a Merkle tree unless a tree construction, leaf ordering/canonicalization, root digest, and inclusion-proof semantics actually exist.

## Cross-provider bridge

Use typed pointers instead of duplication:

`artifact_id | drive_file_id | drive_revision_or_modified | repository | git_ref | commit_oid | path | blob_oid | relation | timestamp`

Drive governs documentary state/indexes/receipts. GitHub producer repos govern code/specs/tests. CI/runtime governs execution evidence. Human/domain authority governs claim promotion.

## Legacy boundary

`data/control-plane/CONNECTOR_CUSTODY_CHAIN.jsonl` remains historical and is not rewritten. Its bootstrap digest semantics remain AUDIT until a successor binds reproducible canonicalization and exact identities.

`claim_allowed=false`: taxonomy/documentation alone does not prove historical custody integrity.
