# Ω187 — FCEA permutation / missing-field contract

State: `APPEND_ONLY / EVIDENCE_FIRST / claim_allowed=false`
Predecessor: Ω186 / PR #593

## Purpose
Materialize the mathematical relation discovered in G031 as an executable audit contract for filling missing fields without promoting unsupported global claims.

For each custody root `X∈{A,B,C}` and shared two-hex prefix `p`, define

`S_X(p) = { p || leaf : leaf is a provider-enumerated direct child of prefix p under root X }`.

The six directed pair permutations are:

- `Δ_AB(p)=S_A(p)−S_B(p)`
- `Δ_BA(p)=S_B(p)−S_A(p)`
- `Δ_AC(p)=S_A(p)−S_C(p)`
- `Δ_CA(p)=S_C(p)−S_A(p)`
- `Δ_BC(p)=S_B(p)−S_C(p)`
- `Δ_CB(p)=S_C(p)−S_B(p)`

Local relation classification is mechanical:

- `A=B` iff `Δ_AB=∅ ∧ Δ_BA=∅`
- `A⊂B` iff `Δ_AB=∅ ∧ Δ_BA≠∅`
- `A⊃B` iff `Δ_AB≠∅ ∧ Δ_BA=∅`
- `A⋈B` (partial overlap / incomparable locally) iff both directional differences are non-empty

The same rule is applied to `(A,C)` and `(B,C)`.

## Missing-field vector
For G031, materialize

`M = (P_rem, L_rem, SHA40, CANON, INTERSECT, DIFF, REACH)`

where:

- `P_rem`: remaining shared prefixes not fully enumerated A/B/C;
- `L_rem`: unresolved leaves inside enumerated/shared prefixes;
- `SHA40`: reconstructed complete object IDs `prefix||leaf`;
- `CANON`: canonical Git object verification status (`zlib decode + git-object SHA-1`);
- `INTERSECT`: global `A∩B`, `A∩C`, `B∩C`, `A∩B∩C`;
- `DIFF`: global directional differences for all six pair permutations;
- `REACH`: reachability from known refs/tips through commit/tree/blob ancestry.

A field is filled only by provider evidence. Empty search is not absence. Prefix equality is not global object-set equality. Local subset is not global subset.

## Closure gate
Global relation may be promoted only when:

`P_rem=∅ ∧ L_rem=∅ ∧ SHA40=complete ∧ DIFF=complete ∧ REACH=complete-enough-for-claim`

Then classify `EQUIVALENT|SUBSET|SUPERSET|PARTIAL_OVERLAP|DISJOINT` per pair. Until then: `TOKEN_VAZIO_REMAINING_OBJECT_SET_RELATION`.

## Falsifiers
- any `o∈A` with `o∉B` falsifies `A⊆B`;
- any `o∈B` with `o∉C` falsifies `B⊆C`;
- any provider-resolved additional child under an allegedly complete prefix reopens that local relation;
- any canonical hash mismatch demotes identity to `CONTRADICTED`.

## Applied Ω187 frontier
Roots preserved separately:
- `A=1RZmunPJSAE4vCISDbQIC3Ul0sWxD6r-v`
- `B=1JOlm4mJU4cUeUsMTk0dK3p1h1j7NUt_e`
- `C=1r94VAey-LmxUYqHVkbXVn3_WCMgzvqtX`

New direct provider census:

### prefix 68
`S_A(68)=S_B(68)=S_C(68)={68defcdcb58947a74deafa28f1654b11bf42925b}`; compressed size 208 B in all three physical occurrences.

Permutation result: all six directional differences are empty for `p=68`; local state `MEASURED A=B=C`.

### prefix 67
`S_A(67)=S_B(67)=S_C(67)={6731f1fc18dccbea508d8fe41b68527c1d982e51}`; compressed size 169 B in all three physical occurrences.

Permutation result: all six directional differences are empty for `p=67`; local state `MEASURED A=B=C`.

### prefix 63
`S_A(63)=S_B(63)=S_C(63)={63da0b7d9b8db6a453b5ba486d509286d7b6e766, 63957c4408eb709ae0412220c805ac441ab0f557}`; compressed sizes 271 B and 208 B in all three physical occurrences.

Permutation result: all six directional differences are empty for `p=63`; local state `MEASURED A=B=C`.

Therefore G031 complete-local-relation coverage advances `39→42` while the global object-set relation remains fail-closed.

## Next deterministic cursor
`61 → remaining shared prefixes → reconstruct complete SHA40(A,B,C) → six global directional differences → intersections → canonical representative/common/exclusive checks → reachability → final G031 classification`.

Other gaps remain independent:
- `G028=TOKEN_VAZIO_PROVIDER_OBJECT` historical bundle bytes;
- `G029=TOKEN_VAZIO` intact archive/suffix;
- `G030=TOKEN_VAZIO_PROVENANCE` corruption timing/causality;
- signer/device/runtime stay external-gated where provider/physical authority is required.

`claim_allowed=false · COMPLETE=NO · ∅=NO`
