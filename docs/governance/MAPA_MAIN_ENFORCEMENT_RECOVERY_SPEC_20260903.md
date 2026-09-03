# Mapa main enforcement recovery specification — cycle 27

Status: `PROPOSED / NOT_APPLIED / claim_allowed=false`

This document is an auditable provider-configuration target, not evidence that the provider is configured.

## Required provider state

The authoritative protection for `main` must, at minimum:

1. be active/enforced at provider side;
2. require at least one independent approving review;
3. require `Promotion Control` or an explicitly equivalent qualifying status check;
4. disallow bypass for the normal promotion path unless a separately governed emergency authority is documented;
5. keep `main` unchanged when a review-ready PR has zero independent approvals;
6. allow capture of a `SERVER_SIDE_ZERO_APPROVAL_MERGE_BLOCKED_RECEIPT` containing the PR head, required-check identities, approval count, rejection result, and before/after `main` SHA.

## Current provider readback bound to this proposal

- `main`: `a7bcc8c16f4ce3a97fb50a30fd94c58f1731a340`
- tree: `947ee83127c6c5302178bd9355ebe9774e43d5f9`
- `protected=false`
- legacy status-check enforcement: `off`
- ruleset `21909304`: `enforcement=disabled`

## Safe test protocol after provider configuration

`provider configuration -> fresh readback -> synthetic/review-ready PR at 0 approvals -> Promotion Control DENIED or equivalent -> provider merge rejection -> assert main_before == main_after -> persist receipt`

Do not call a merge endpoint before the fresh readback proves enforcement is active. This preserves the issue #327 stop condition.

## Boundary

`PROPOSED_CONFIG != PROVIDER_STATE != TEST_EXECUTION != EVIDENCE != CLAIM`

`claim_allowed=false`
