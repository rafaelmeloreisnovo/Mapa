# Receipt — Drive Deep Corpus A2 Closure — 2026-08-22

State: `VERIFIED_LIMITED / claim_allowed=false`

Authority: Drive current-provider bytes + frozen historical SHA256 witnesses.  
Routing authority: Mapa.  
Privacy identity: `PID=SHA256(UTF8(canonical conversation_id))`; raw IDs are not persisted here.

## Sources

- RAW048 provider `1zfyYkELQQOiMNeW_no8oYFgdiewhxCdO`, 36,771,626 bytes, SHA256 `ed19ea07f8763a8a4d87204d80c817694ce4d6c339c71b1d2a1b955a8c125256`, JSON roots/PIDs `100/100`.
- RAW049 provider `1e4qhX1taiRY72ZBQZUim-A-jgQojqeEH`, 47,806,754 bytes, SHA256 `608e45449809a47f5931f86328b96dab2b2b86a5abf21a8dfe1c7da6834a2f1a`, JSON roots/PIDs `100/100`.
- RAW050 provider `1rpWFICYTTFKbZzvzHdW3PQV5LzLlEA-C`, 17,115,060 bytes, SHA256 `c5058bf25f682de12de68b54029d13b07e836cd519416752fbc5e4fa320b4979`, JSON roots/PIDs `54/54`.

All three current hashes exactly match the historical hashes frozen in CHECKPOINT_0082.

## Derived index

Drive: `RAFAELIA_CURRENT_RAW_PID_INDEX_000_050_EXCEPT_018.v5`, ID `1xhP6CJZsaLoqPokHvGuuWlvathVS5UKLejgFo9S2J9U`.

- predecessor V4: 4,698 unique PIDs
- additive RAW048..050 PIDs: 254/254 unique
- overlap with V4: 0
- overlap with historical Locator V1.1: 0
- V5 total: 4,952 unique PIDs
- new PID-set SHA256: `74e2a192614ca34a7cfefdc864e64d20a842c3f6d86e9516b004e819ceaeaa25`
- canonical local V5 CSV SHA256: `d39de51776e1a001385d4168c37d0739d75b7b95cdd40084f1154c1e4a324c13`

## Transition

`A2: TOKEN_VAZIO_HARD_CUSTODY -> CLOSED_VERIFIED_CURRENT_PROVIDER_BYTES_HASH_JSON_PIDS`

`A3: BLOCKED_BY_A1_A2 -> BLOCKED_BY_A1_ONLY`

A1 remains `TOKEN_VAZIO_HARD_CUSTODY`; no full-corpus PASS is claimed.

## Boundary

Byte/hash equality proves identity/integrity for the exact current objects. It does not prove semantic correctness, scientific claims, full provider enumeration, or full-corpus runtime execution.
