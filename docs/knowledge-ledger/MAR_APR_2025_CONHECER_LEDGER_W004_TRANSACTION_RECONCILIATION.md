# RAFAELIA — Mar–Abr 2025 — W004 Transaction Reconciliation

**State:** `CONTROL_RECONCILED_PRIVACY_SAFE`  
**Claim:** `claim_allowed=false`

An interrupted write sequence previously created sibling W002 artifact identities. During the public privacy rebuild, the public branch was canonicalized to one W002 path while the private Drive receipt preserves the incident/custody history.

Current route:
`W001 → W002(canonical) → W003(evidence) → W004(control) → W005(March delta)`

Rules:
- path-qualified artifact identity;
- public GitHub contains no raw private conversation/message IDs;
- Drive private custody retains detailed mappings;
- USER_INPUT != ASSISTANT_GENERATION != CLAIM.
