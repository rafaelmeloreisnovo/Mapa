# Public AI Provenance Index Invariant V1

Status: `VERIFIED_LIMITED / PUBLIC-CI / claim_allowed=false`

## Purpose

Anchor a public, reproducible CI in `Mapa` for evaluating **observable provenance signals and technical composition features** of AI-produced text/images without requiring or publishing any private conversation corpus.

The private `Conversations Chunky` side may later export only opaque cryptographic commitments and index relations. Public CI validates the **index graph** and its navigation root, not the private bytes.

## Non-negotiable boundary

`PRIVATE_RAW != PUBLIC_CI_INPUT`

The public repository must not receive private prompts, conversation bodies, image bytes, attachments, titles, account data, or private provider IDs merely to make CI pass.

The bridge is:

`PRIVATE BYTES -> PRIVATE KEYED COMMITMENT -> PUBLIC OPAQUE HASH MANIFEST -> PUBLIC INDEX CI`

Recommended private commitment for conversation chunks: `BLAKE3-256-KEYED`.

The public manifest root is independently reproducible from the already-public commitments:

`navigation_root = SHA256(commitment_0 || "\n" || ... || commitment_n)`

This proves consistency/order of the public manifest. It does **not** prove the underlying private text and is not an authorship claim.

## The invariant is plural: INDICES

The artifact forbids collapsing the system into one magic score. Ten orthogonal index planes are mandatory:

1. `IDX-IDENTITY`
2. `IDX-CONTENT-COMMITMENT`
3. `IDX-TEMPORAL`
4. `IDX-PROVIDER-PROVENANCE`
5. `IDX-MODALITY-SIGNATURE`
6. `IDX-RELATION`
7. `IDX-EVIDENCE-WEIGHT`
8. `IDX-PRIVACY-BOUNDARY`
9. `IDX-SUPERSESSION`
10. `IDX-CLAIM-GATE`

Invariant:

`INDICES_ARE_MULTIPLE_ORTHOGONAL_VIEWS_NOT_ONE_SCORE`

A dynamic weighting layer may rank navigation candidates, but it cannot increase the evidence class of a claim.

## Public observations — OpenAI

Observed on 2026-08-29 from public OpenAI surfaces:

- Supported images generated with ChatGPT, Codex, and the OpenAI API include C2PA Content Credentials and SynthID provenance signals.
- OpenAI exposes a public verifier for supported images and audio.
- The cited public verifier does not provide an equivalent provider-proof claim for text.
- C2PA metadata can be removed/lost, and watermark signals can degrade. Therefore `NO_SIGNAL != PROOF_OF_NON_ORIGIN`.

Public sources:

- [OpenAI content provenance](https://openai.com/index/advancing-content-provenance/)
- [OpenAI Help: provenance signals](https://help.openai.com/en/articles/8912793)
- [OpenAI verification surface](https://openai.com/research/verify/)

These are provider observations, not universal laws. Coverage can vary by product, model, export path, file type, and creation date.

## Signature ladder

### P3 — PROVIDER_VERIFIED

Examples: supported trusted C2PA associated with the provider; supported provider watermark/verifier positive.

This is the strongest class in this V1, but it still means **provenance signal**, not truth, legal ownership, or semantic correctness.

### P2 — PROVENANCE_METADATA

Structured/signed provenance metadata is present but has not been independently reverified in the current execution.

### P1 — TECHNICAL_HEURISTIC

Examples:

- dimensions/aspect ratio;
- MIME/container;
- encoder/compression profile;
- filename/export conventions;
- visual composition/style;
- text style, punctuation, lexical distribution, token statistics.

These may be useful features for clustering and candidate routing. They are **not provider identity proof**.

### P0 — UNKNOWN

Insufficient or absent supported signal. This state remains unknown rather than being converted to a negative attribution.

## Text boundary

Statistical text composition can be indexed as a vector:

`x_text = [length, entropy, punctuation, lexical features, ngrams, formatting, embedding/semantic features, temporal context, model metadata when explicitly present]`

But this V1 enforces:

`TEXT_STYLE_TO_PROVIDER_PROOF = FORBIDDEN`

A classifier may output a bounded heuristic score only if it carries its dataset, calibration, false-positive/false-negative metrics, scope, and falsifier. It cannot be promoted to provider provenance by style alone.

## Image boundary

Technical image features can be indexed as:

`x_img = [MIME, width, height, aspect, byte_size, EXIF/XMP/ICC, PNG/JPEG structure, C2PA, watermark-verifier result, transform history]`

Resolution, aspect ratio, style, or filename alone are non-unique:

`IMAGE_RESOLUTION_TO_PROVIDER_PROOF = FORBIDDEN`

Prefer the evidence order:

`provider verifier/C2PA/watermark > structured provenance metadata > container/codec features > style/resolution heuristic`.

## Complex-network extension to other AI providers

The schema is provider-agnostic. A new provider adapter must independently register:

- provider ID;
- public source URL;
- supported modalities;
- provenance-signal type;
- public verification surface, if any;
- semantics of a negative result;
- observation date.

Until that exists:

`provider_state = TOKEN_VAZIO_PUBLIC_PROVENANCE_ADAPTER`

OpenAI evidence must not be copied by analogy to another provider.

## Private Conversations Chunky bridge

A future private-side exporter may produce one row per chunk:

```text
ordinal | opaque_id | keyed_commitment | temporal_index | relation_index | evidence_state
```

No content is required publicly.

The public CI checks:

- exact 0..N-1 ordering;
- unique opaque IDs;
- unique 256-bit commitments;
- ten invariant index planes;
- public navigation root;
- fail-closed claim state;
- no raw-content dependency.

This allows public navigation of **commitments and indices** while preserving the private corpus boundary.

## Anti-promotion rules

- `HASH != AUTHORSHIP`
- `HASH != SEMANTIC_EQUIVALENCE`
- `SEMANTIC_SIMILARITY != IDENTITY`
- `RESOLUTION != PROVIDER_IDENTITY`
- `TEXT_STYLE != PROVIDER_IDENTITY`
- `NO_SUPPORTED_SIGNAL != NON_ORIGIN`
- `PRIVATE_SOURCE_ABSENT_FROM_PUBLIC_CI != PRIVATE_SOURCE_ABSENT`
- `INDEX_SCORE != EVIDENCE_CLASS`

## CI contract

Workflow: `.github/workflows/public-ai-provenance-index.yml`

The workflow:

1. runs only from the public repository revision;
2. checks out without persisted credentials;
3. reads no secrets;
4. validates the public registry;
5. validates the hash-only sample manifest;
6. runs negative anti-regression tests;
7. leaves `claim_allowed=false`.

## F_ok / F_gap / F_next

### F_ok

- Public CI can anchor provider-visible provenance boundaries.
- OpenAI image/audio provenance has a current public verification surface.
- Hash-only manifests can expose navigable indices without exposing private payloads.
- `INDICES` is a formal invariant, not a single scalar.

### F_gap

- Real private Conversations Chunky commitments are not included here.
- Text provider attribution has no provider-proof surface in the public OpenAI verifier used for this V1.
- Other AI provider adapters require independent public evidence.

### F_next

- Generate keyed commitments privately.
- Export a minimized public-safe manifest.
- Bind the navigation root to an append-only receipt.
- Add provider adapters only after independent source verification.
