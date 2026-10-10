# Append-only evidence custody

PRE_RECORD → ACTION → PROVIDER_READBACK → SHA256(payload exact bytes) → GIT_SHA1 → RECEIPT → ROUTE_POINTER → R3.
Git commit timestamps and Drive modifiedTime serve as provider observation evidence; none alone constitutes trusted RFC3161 timestamp.
Receipts must never be edited in place; error creates successor (parent_event_id/supersedes). A Git repository is mutable by administrators: preserve readback and independent off-provider witness for higher assurance.
Minimum per event: id, parent_ref, source URL/hash, actor, UTC time+provenance, operation, committed SHA, Drive ID, alphaXiv folder reference, result, typed gap and rollback.
One ledger event per material change/batch, not a recursive record for each token.
No market records ingested yet. Gate=DOCUMENTATION_ONLY / NOT_CI_TESTED / claim_allowed=false.
