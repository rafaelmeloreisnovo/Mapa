# Ω177 — FCEA loose-object prefix census

- predecessor: Ω176
- mode: BULK-FIRST / CURSOR-FIRST / fail-closed
- claim_allowed: false
- Drive receipt: `1FUkmGMSl8HAA6dmVFaeNcr417TsUxilq2zoJz4DbRCE`
- Atlas Δ177: `1D2HQjfvw4VoZwwp5Q78nmyVhCf0YptpM28IH4fcFCnM`

## Physical provider roots

- A/FCEA_REPO: `1BtjJ9YPFL-wymQj_7wl0GqINAczGbpT2`
- B/FCEA_REPO: `1Ur04MJSznzv13n4IYWkVz17VF7LtR3Lz`
- C/FCEA_REPO: `1dRW-lvJicxD-8AMBooFal9XcObr2yMHh`
- A `.git/objects`: `1RZmunPJSAE4vCISDbQIC3Ul0sWxD6r-v`
- B `.git/objects`: `1JOlm4mJU4cUeUsMTk0dK3p1h1j7NUt_e`
- C `.git/objects`: `1r94VAey-LmxUYqHVkbXVn3_WCMgzvqtX`

## Evidence

Direct provider enumeration of all three `.git/objects` roots exposed two-hex loose-object prefix directories and no direct child named `pack`. This closes only the narrow pack-child-presence probe for these enumerated physical occurrences. It does **not** establish complete object-set inclusion/equivalence.

Prefix-directory topology is progressive across A/B/C and is compatible with the already reproduced linear tip ancestry, but prefix presence is weaker than exact object identity. No `A⊂B⊂C` claim is promoted here.

Exact-name Drive reprobes for `backup.bundle`, `backup_supreme.bundle`, `FCEA_SNAPSHOT_ROOT_FINAL_1750558602.tar.gz`, `FCEA_ROOT_FINAL_LIVE_1750561044.tar.gz`, and `FCEA_ROOT_FINAL_CLEAN_1750559862.tar.gz` returned documentary/index references rather than provider-resolved physical files carrying those titles. Search references are not byte custody.

Provider reconciliation: predecessor PR #577 is now externally merged. Ω177 did not approve, merge, release, or write to `main` directly.

## Gaps

`TV-FCEA-FULL-LOOSE-OBJECT-SET-RELATION-177 = TOKEN_VAZIO`

- missing: exact reconstructed SHA set per A/B/C, intersections/differences, reachability
- evidence needed: enumerate every nested leaf under every two-hex prefix; reconstruct `<prefix><leaf>`; verify representative/common/unique objects by Git SHA-1
- falsifier: incomplete provider listing or non-object leaves
- closure gate: complete nested census + deterministic set relation
- next probe: recursive A/B/C loose-object leaf census
- claim_allowed: false

`TV-FCEA-HISTORICAL-BUNDLE-BYTES-177 = TOKEN_VAZIO_PROVIDER_OBJECT`

- missing: physical bundle bytes
- closure gate: provider file ID + bytes + SHA-256/SHA-512 + `git bundle verify`/`list-heads`
- next probe: parent-cursor traversal around FCEA roots/SNAPSHOTS and inventory sources
- claim_allowed: false

`TV-FCEA-ALTERNATE-INTACT-ARCHIVE-177 = TOKEN_VAZIO_PROVIDER_OBJECT`

- missing: byte-distinct intact archive or missing suffix
- closure gate: physical object + hashes + gzip/tar integrity + member census
- claim_allowed: false

## R3

- F_ok: three physical objects roots enumerated; direct pack child not exposed; prefix topology retained per occurrence; exact bundle/archive names reprobed; predecessor provider state reconciled.
- F_gap: exact loose SHA sets/intersections/reachability; physical historical bundle bytes; intact archive/suffix; corruption timing; signer/device/runtime external gates.
- F_next: nested prefix leaves → reconstructed SHA sets → set intersections/differences → hash verification → reachability → relation classification; then bundle/archive parent-cursor.

`COMPLETE=NO` · `∅=NO`
