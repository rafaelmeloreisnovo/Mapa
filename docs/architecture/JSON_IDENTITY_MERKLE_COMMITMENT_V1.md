# JSON Identity + Merkle Commitment V1

Status: `IMPLEMENTED_DRAFT`  
Promotion: `claim_allowed=false`

## Scope

This layer is the narrow successor to the existing conversation-custody hashing
layer. It does **not** replace `scripts/index_conversations_export.py`; that
indexer remains the specialized message/conversation custody route.

This V1 adds the missing generic identity plane for JSON/JSONL:

`source occurrence -> exact bytes -> canonical record -> record commitment -> file root -> corpus root`

The source is read-only. No raw payload, message body, secret, or scalar value is
copied into the derived index.

## Identity separation

Four identities are intentionally different:

- `occurrence_id`: where a document/record occurred inside a named source.
- `byte_id`: SHA-256 of exact file bytes.
- `content_id`: SHA-256 of canonical JSON for a top-level record.
- `commitment`: domain-separated SHA-256 used in ordered chains/Merkle trees.

Therefore:

`OCCURRENCE_ID != BYTE_ID != CONTENT_ID != SEMANTIC_ID`

Two records with the same canonical JSON can share a `content_id` while retaining
different occurrence IDs. Whitespace or key-order changes may change `byte_id`
without changing the canonical `content_id`.

Hash equality is an integrity/content-addressing observation. It does not prove
authorship, ownership, semantic equivalence, causal relation, or scientific
truth.

## Hash of hashes

The hierarchy is explicit:

1. canonical record SHA-256;
2. domain-separated record leaf commitment;
3. ordered file Merkle root;
4. file commitment;
5. ordered corpus Merkle root;
6. manifest commitment.

An independent hash chain is also kept for record order and file order. Merkle
and chain serve different falsifiers: tree membership/group commitment versus
sequential order commitment.

## Record boundary

For `.json` with a top-level array, each array element is one record. A non-array
JSON document is one record. For `.jsonl`, each non-empty line is one record.

This layer intentionally does not descend into arbitrary nested objects. Message
and conversation-level extraction belongs to the existing specialized custody
indexer. This avoids turning structural indexing into unbounded semantic
tokenization.

## Operational use

```bash
python3 scripts/build_json_identity_commitments.py \
  /path/to/json-directory \
  --source-id NOVOEXPORT-JSON \
  --out-dir /new/append-only/receipt-directory
```

The output directory must be absent or empty. Generated files:

- `records.index.jsonl`
- `files.index.jsonl`
- `manifest.json`
- `receipt.json`
- `SHA256SUMS`

Large monolithic JSON documents above the configured byte limit fail closed and
must use the specialized streaming custody route instead of silently consuming
unbounded memory.

## Gates

A valid execution must demonstrate:

- repeatability on identical inputs;
- same canonical content can have distinct occurrences;
- byte identity changes when exact bytes change;
- canonical content identity survives harmless formatting/key-order changes;
- record reorder changes ordered commitments;
- malformed JSON fails closed without committed partial indexes.

## Boundary

This is an indexing/custody mechanism, not a model-training mechanism.

`DATASET_INFORMS_INDEX != DATASET_AUTHORIZES_OBJECTIVE`

`HASH != MEANING`

`HASH != AUTHORSHIP`

`INDEXED != VERIFIED_CLAIM`
