# Ω182 — FCEA shared-prefix leaf census continuation

Date: 2026-09-09
Predecessor: Ω181 / PR #588
Mode: BULK-FIRST + CURSOR-FIRST
claim_allowed: false

## Evidence delta

- `a4`: C contains exactly leaf `18206df8fc5d0d9989e6c540a587958c5455b5` (362 B); combined with Ω181 A/B evidence, local relation is `A=B=C` MEASURED.
- `a2`: A/B/C each contain exactly leaf `a5c09c1b31c4a5f77aa276e8a38cc29f583789` (51 B); local relation `A=B=C` MEASURED.
- `9f`: A/B/C each contain exactly leaves `492f46ac3484acb91381f8f2cef5881262d94f` (178 B) and `d6bd497b94207a6d4c72cabbf6dcfca5ddb58c` (179 B); local relation `A=B=C` MEASURED.
- Complete shared-prefix relation coverage advances `15 → 18`.
- No new canonical byte re-hash was performed for these objects in Ω182; do not promote them to REPRODUCED on this cycle.

## G031

`MEASURED_PREFIX_STRICT_INCLUSION + MEASURED_18_COMPLETE_SHARED_PREFIX_RELATIONS + TOKEN_VAZIO_REMAINING_OBJECT_SET_RELATION`

Local equality does not establish global object-set equality/subset. Closure remains gated on complete deterministic leaf census, SHA40 reconstruction, canonical checks, set intersections/differences, and reachability.

## Provenance

- Receipt Ω182: Google Drive `1U0X_V6IS5F9cvhdcUuJUKAsSV7HmpVp7AjouP4iTJws`
- Atlas Δ182: Google Drive `1gaexyc7EPQqJ53oxZWDFS002uiVKHDUeRsU2qWw9mgU`
- A objects root: `1RZmunPJSAE4vCISDbQIC3Ul0sWxD6r-v`
- B objects root: `1JOlm4mJU4cUeUsMTk0dK3p1h1j7NUt_e`
- C objects root: `1r94VAey-LmxUYqHVkbXVn3_WCMgzvqtX`

## Next cursor

`remaining shared prefixes → SHA40 sets → ∩/− → canonical checks → reachability → final G031 classification gate`

`COMPLETE=NO · EMPTY_SET=NO · claim_allowed=false`
