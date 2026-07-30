# Audit note — Reference run

The local reference execution was performed at `2026-07-30T04:18:06Z` in an x86_64 Linux container using CPython 3.13.5.

Observed bounded results:

- nine source hashes matched the registered values;
- APK: 738 ZIP entries and all eight expected native library paths present;
- chat export: ZIP integrity check returned no bad member and exactly five expected root files;
- PNG corpus: seven valid PNG signatures and readable IHDR dimensions;
- tests: 3/3 passed;
- receipt SHA-256: `56621b76527eb626b7b2d93074cf1c0a589d836b9b5934a7e35811904ce6e77c`;
- downloadable bundle SHA-256: `89067a5503d4b06a74026a79abb1fafa915cfbba54e81e8e02f65eff7189819b`.

This is not an Android execution and is not independent replication. The correct state is `S4_RECEIPT_REPRODUCIBLE_REFERENCE` with `TOKEN_VAZIO_RUNTIME_NOT_EXECUTED` for Termux.
