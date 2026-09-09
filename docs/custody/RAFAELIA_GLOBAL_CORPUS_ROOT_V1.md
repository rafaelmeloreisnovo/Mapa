# RAFAELIA Global Corpus Root V1

State: `SPEC_DEFINED_LOCAL / ROOT_POPULATION_OPEN / claim_allowed=false`

A global root is a deterministic commitment to an **enumerated canonical object set**, not a claim that every byte in Drive/GitHub belongs to RAFAELIA.

Canonical record:

`object_id<TAB>sha256<TAB>size<TAB>provider<TAB>locator<TAB>role<LF>`

Records are UTF-8 byte-sorted by `object_id`, then committed with SHA-256 under domain prefix:

`RAFAELIA_GLOBAL_CORPUS_ROOT_V1\0 || canonical_records`

Required role separation:

`SOURCE != ARTIFACT != EXECUTION != EVIDENCE != MEMORY != INDEX != CLAIM`

Objects with unavailable bytes may appear in a **pre-root inventory** with `sha256=TOKEN_VAZIO`; they cannot enter the finalized cryptographic root until bytes are observed.

Each finalized record must carry or resolve to:

- stable canonical object ID;
- exact provider + locator;
- byte length;
- SHA-256;
- role;
- provenance state;
- sensitivity classification;
- license/origin reference when applicable;
- supersession edge when applicable.

The root does not authenticate itself. Signature, timestamp, authority, independent review and claim promotion remain separate layers.

`HASH_VALID != AUTHORITY_VALID`
`ROOT_COMPLETE != SCIENTIFIC_CLAIM_TRUE`
