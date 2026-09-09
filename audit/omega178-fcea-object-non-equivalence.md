# Ω178 — FCEA cross-provider loose-object non-equivalence

- predecessor: Ω177
- mode: BULK-FIRST | CURSOR-FIRST | FAIL-CLOSED
- claim_allowed: false
- Drive receipt: `1ffC_W6ESFIriuQ6QEw7Pa5R93CQcXB227b_bDP_lbDQ`
- Atlas Δ178: `1Y5pEB7oTkkLVLF_jJP1ApBI5_RSZ1WYUWbM_VL4AjU4`

## SOURCE → TRANSFORM → TEST/EVIDENCE

Three provider-distinct FCEA_REPO `.git/objects` roots A/B/C were preserved as separate occurrences.

### Witness B relative to A

`db34c5ea068fcee703a634d5a2a7d5d8c4ba8226`

The `db` prefix is present in the enumerated B objects root and absent from the enumerated A objects root. The physical Drive leaf was downloaded, zlib-decoded, and canonical Git SHA-1 reproduced exactly. GitHub `rafaelmeloreisnovo/rafaelia-core-enterprise` resolves the same Git blob ID to the same payload.

### Witness C relative to B

`e909c5d818ccaab81a396343c032e4a9f442f972`

The `e9` prefix is present in the enumerated C objects root and absent from the enumerated B objects root. The physical Drive leaf was downloaded, zlib-decoded, and canonical Git SHA-1 reproduced exactly. GitHub resolves the same blob ID to the same payload.

## Claims

- `REPRODUCED`: A != B at the enumerated loose-object-set level.
- `REPRODUCED`: B != C at the enumerated loose-object-set level.
- `REPRODUCED`: both witness objects converge Drive ↔ GitHub by exact Git object ID and payload.
- `TOKEN_VAZIO`: full `EQUIVALENT|SUBSET|SUPERSET|PARTIAL_OVERLAP|DISJOINT` relation remains open until complete loose-leaf census and reachability analysis.

## Gap update

`G031/FCEA_CANONICAL_EQUIVALENCE_SUPERSESSION = MEASURED_NON_EQUIVALENCE_PARTIAL_RELATION`

Closure gate: enumerate every loose leaf, reconstruct full 40-hex object IDs, compute set intersections/differences, verify reachability, then classify the complete relation. No canonical supersession claim is allowed before that gate.

The previous Ω177 audit PR #582 was observed as externally merged by the provider before this delta; Ω178 did not merge, approve, or release it.

## R₃

- F_ok: two physical exclusive witnesses reproduced and cross-provider converged.
- F_gap: complete object-set census/reachability; historical bundle bytes; intact archive/suffix; corruption timing; external signer/device/runtime gates.
- F_next: full A/B/C loose-leaf census → set algebra → reachability → relation classification → resume bundle/archive parent cursor.

`COMPLETE=NO` · `∅=NO`
