# MHEL-Ω — F_next source-ingestion capsule

State: `FNEXT_PARTIAL_PASS`

- Previous event: `4e28ef81e935a33e75c35d6251b4bffacb9d79fad8d0276f5ea30973b04623e7`
- Child event: `22289eddb0bd94b0070cc88d6eaa650992f915f24af408224f0de806f8c3a7ff`
- Materialized source files: `14`
- Duplicate content hashes: `0`
- Source-set root SHA-256: `d95672fa102632601e6fd5ec39f8e7589cc82efd7c7c2fa1abc043dec094e676`
- `claim_allowed=false`

## Fato

The exact bytes of 14 final materialized `.txt` files were ingested and hashed.

## Lacuna

The original Termux `receipt.json`, `execution.log`, and `HASHES.sha256` were not present. Earlier upload instances that reused the same path are not independently available.

## Invariante

No source text, authorship, interpretation, prior event or ciphertext was overwritten. Source snapshots were not promoted to validated claims.

## Próxima prova

Ingest the three original Termux artifacts, verify their internal hash relationships, and append a new child event.
