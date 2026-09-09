# RAFAELIA Ω184 — FCEA shared-prefix leaf census

Date: 2026-09-09  
Predecessor: Ω183 / Mapa PR #590  
Mode: BULK-FIRST + CURSOR-FIRST  
Claim gate: `claim_allowed=false`

## Evidence delta

Direct Google Drive traversal of the three physical FCEA loose-object roots A/B/C closed four additional shared-prefix relations:

- `99`: A=B=C, exactly leaf `7881680c92769708f09a33b5a775a6addbe9c9`, 88 B.
- `96`: A=B=C, exactly leaf `a5d89fe1f0e2a15b0e8ca05307de7c0ed16d25`, 51 B.
- `94`: A=B=C, exactly leaves `3f0ada2a127541c4141aef64dec43fdab4fa1c` (330 B) and `1971b71c46b4fc9cba3fcc4b4523b1df004f7b` (212 B).
- `92`: A=B=C, exactly leaf `6c82dd6b17e015147fd19f5345420e780a95c5`, 51 B.

These are `MEASURED` provider enumerations. Ω184 did not canonically re-hash the newly traversed object bytes, so they are not promoted to `REPRODUCED`.

Complete shared-prefix relation coverage advances `19 → 23`.

## Gap state

`G031 / TV-FCEA-FULL-LOOSE-OBJECT-SET-RELATION-184`

`MEASURED_PREFIX_STRICT_INCLUSION + MEASURED_23_COMPLETE_SHARED_PREFIX_RELATIONS + TOKEN_VAZIO_REMAINING_OBJECT_SET_RELATION`

Local leaf equality does **not** prove global object-set equality or inclusion. Classification as `EQUIVALENT|SUBSET|SUPERSET|PARTIAL_OVERLAP|DISJOINT` remains gated on complete deterministic leaf census, SHA40 reconstruction, canonical checks, set intersections/differences, and reachability.

Other open gaps remain unchanged: G028 historical bundle bytes (`TOKEN_VAZIO_PROVIDER_OBJECT`), G029 intact archive/suffix (`TOKEN_VAZIO`), G030 corruption timing/provenance (`TOKEN_VAZIO_PROVENANCE`), plus external signer/device/runtime gates.

## Provenance

- Receipt Ω184: Google Drive `1l6asI9BASgqP4QSBMa0W4rIv8HJVDOrQDH-Kx820AmU`
- Atlas Δ184: Google Drive `1ck-voAFjoXofgy-T-6ZGa8nt5Hrclw-QyvJhpqZfOU8`
- Physical roots: A=`1RZmunPJSAE4vCISDbQIC3Ul0sWxD6r-v`; B=`1JOlm4mJU4cUeUsMTk0dK3p1h1j7NUt_e`; C=`1r94VAey-LmxUYqHVkbXVn3_WCMgzvqtX`
- Predecessor PR #590 was observed provider-merged externally; Ω184 performed no merge, approval, or release.

## Cursor

Next deterministic frontier:

`8f → 8e → 8d → 88 → 87 → 82 → 81 → remaining shared prefixes → SHA40 sets → ∩/− → canonical checks → reachability`

`COMPLETE=NO · ∅=NO · claim_allowed=false`
