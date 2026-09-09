# Ω179 — FCEA physical prefix-set inclusion

- predecessor: Ω178
- mode: BULK-FIRST | CURSOR-FIRST | FAIL-CLOSED
- claim_allowed: false
- Drive receipt: `1tUY3jdZFA9TM0HiMTxWVIOxtEdcLVdlj2fs2oGrTYZc`
- Atlas Δ179: `1S1B5EzthkqiPhQ897p638SveQkXfhw7r25dEgQrAeZc`

## SOURCE → TRANSFORM → TEST/EVIDENCE

Provider-distinct physical `.git/objects` roots were exhaustively enumerated at the direct two-hex-prefix directory layer:

- A: 77 prefixes
- B: 79 prefixes
- C: 87 prefixes

Set deltas:

- `B − A = {b8, db}`; `A − B = ∅`
- `C − B = {0c, 0f, 59, de, e0, e2, e5, e9}`; `B − C = ∅`

Therefore `PREFIX(A) ⊂ PREFIX(B) ⊂ PREFIX(C)` is measured/reproduced **only at the prefix-directory layer**.

Targeted leaves observed in newly introduced prefixes include:

- B/b8 → `b83ac7ce562b0df1a5a8c18b3c38010ba0dc47ff`
- C/e5 → `e5de5fd4704f435731399f2724e7b52fca058246`
- C/e2 → `e24ca6f8ec99de04e4f930bce619e06c89e68ce7`
- C/e0 → `e031641ccdb0843817f646536bef0a98d72842a7`
- C/de → `de4951c3646471b450f3916d1532bbcf5d3af65a`
- C/e9 → `e909c5d818ccaab81a396343c032e4a9f442f972` (previously canonically verified in Ω178)

## Fail-closed claim boundary

Prefix inclusion does **not** imply full loose-object-set inclusion. Shared prefixes may contain divergent leaves. `EQUIVALENT|SUBSET|SUPERSET|PARTIAL_OVERLAP|DISJOINT` remains `TOKEN_VAZIO` until every leaf under shared prefixes is enumerated, SHA40 sets are calculated, canonical object bytes are validated, and reachability is tested.

## Provider reconciliation

PR #585 / Ω178 was observed externally merged at `2026-09-09T08:15:55Z`, merge commit `019ea5cf3c642f540b99bbb33db030ace2b0a7e4`. Ω179 did not merge, approve, or release it.

## Gap update

`G031 = MEASURED_PREFIX_STRICT_INCLUSION + TOKEN_VAZIO_OBJECT_SET_RELATION`

Closure gate: complete shared-prefix leaf census → reconstructed SHA40 sets → intersections/differences → canonical validation → reachability → relation classification.

## R₃

- F_ok: exact direct-prefix census A/B/C; strict prefix-layer inclusion; six targeted leaf witnesses; Drive receipt + Atlas delta.
- F_gap: full shared-prefix leaf census, canonical verification of new leaves, reachability; historical bundle bytes; intact archive/suffix; corruption timing; external signer/device/runtime gates.
- F_next: deterministic shared-prefix leaf census (`d3→d1→d0→…`) → full object-set algebra → reachability → relation classification → resume bundle/archive parent-cursor.

`COMPLETE=NO` · `∅=NO`
