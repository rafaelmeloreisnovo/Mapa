# Receipt — Session AI Work Dispatch V1

Date: 2026-09-28  
State: `IMPLEMENTED_UNTESTED`  
claim_allowed: `false`

## Source / authority

- Mapa main baseline: `7853f23053044c9b69d6b81f7f5f71fa285f864c`
- RafGitTools main baseline: `606525722624116c7d7f750f08c59f9462d619f8`
- Rafaelia_Private main baseline: `8a3dbb7f8ad586c059d3f6687e9d92623a0c98cd`
- Practice ATLAS blob: `e93c915fa6ddc73b85f0bd934af508e2627a9994`
- Practice Router blob: `a43e229b19f5dc01b109301f7c15f75f23d7c91a`
- Active Work Ledger V2 blob: `c610030f3aeb73ef02b12b34804d2c8ed845a2bb`
- Current chat provider ID/hash: `TOKEN_VAZIO_SESSION_PROVIDER_ID`

## Before

Session intents were distributed across chat turns plus existing routing/custody artifacts; no single typed session overlay assigned bounded agent roles and output localities.

## Action

Materialize registry, index, route pins, baseline, validator and tests. No producer corpus is copied; private bodies remain outside the public router.

## Expected observable

Validator accepts only packets with core invariants, unique roles/packet IDs, <=3 sources, resolved authority/execution/evidence rule, explicit Drive localities and `claim_allowed=false`.

## Actual observable

`IMPLEMENTED_UNTESTED` until exact-head validator/CI executes.

## Falsifier

Any packet lacking source/authority/execution/evidence rule, copying private payload into the public router, or claiming execution merely because an agent role was assigned invalidates the dispatch.

## Rollback

Drop/revert this branch. Existing Practice ATLAS, Active Work Ledger V2 and Practice Router remain authoritative and untouched.

## Reconstruction minimum

1. Practice ATLAS exact ref/blob.
2. Active Work Ledger V2 exact ref/blob.
3. Practice Router exact ref/blob.
4. Session dispatch registry + routes.
5. Exact-head validation receipt.
6. Drive documentary mirror/readback.

## R3

- F_ok: bounded overlay materialized without replacing existing authority.
- F_gap: exact-head validator/CI and Drive mirror receipt remain pending.
- F_next: validate branch, create RafGitTools consumer adapter, then write Drive pointer docs.
