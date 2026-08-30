# ChatGPT Observable Vector Signature V1

Status: `FORMAL_PUBLIC_EVALUATION_CONTRACT`

`claim_allowed=false`

## Objective

Provide a structured packet that ChatGPT or another Transformer can read in-context to compare public web sources, text, images, code, metadata, provenance and opaque private commitments without claiming access to hidden neural states.

The artifact is intentionally split into two orthogonal vectors:

- `V_CONTENT_16`: similarity, structure, modality, novelty, contradictions, falsifier and privacy-risk features.
- `V_EVIDENCE_10`: authority, primary-source directness, citation support, provenance, retrieval integrity, dates, claim/source alignment, independent corroboration, controls and reproducibility.

Invariant:

`SIMILARITY_NE_EVIDENCE_AND_VECTOR_WEIGHT_CANNOT_UPGRADE_EVIDENCE_CLASS`

## Transformer boundary

This contract does **not** claim access to ChatGPT/OpenAI hidden activations, attention matrices, internal logits or proprietary internal embeddings. The Transformer receives an explicit observable feature packet in context.

If an external embedding or similarity method is used, record:

1. exact method/model,
2. input scope,
3. normalization,
4. score,
5. source references,
6. falsifier/negative control.

An embedding score remains a derived feature and cannot establish authorship, provenance or causality by itself.

## Source/site conditions

Every web node carries a source-condition envelope:

`canonical_url, domain, retrieved_at, source_class, modality, published_at, updated_at, citation_available, content_scope, provenance_signal, dynamic_content_risk, access_boundary, source_specific_caveat`.

This preserves several distinctions:

- retrieval date != publication date;
- search result != source proof;
- dynamic page != stable observation unless captured/cited;
- many pages != independent corroboration if they derive from one origin;
- same domain != same claim or same author.

### Observable statistics

When content is legitimately available to the evaluator, a producer may attach declared statistics such as:

- byte/character/word counts;
- Unicode/script distribution;
- sentence and paragraph length distributions;
- punctuation/symbol/code/math density;
- vocabulary/type-token ratios;
- n-gram or MinHash sketches;
- MIME, dimensions, aspect ratio and codec metadata for images;
- C2PA/SynthID/provider provenance state when publicly verifiable;
- publication/update/retrieval timestamps;
- citation and cross-source relation counts;
- declared embedding/similarity scores from an explicitly named method.

Every statistic must carry its method and source scope. These observable summaries may support ranking, clustering and anomaly detection, but cannot independently prove authorship or provider origin.

## Public OpenAI adapters

The first adapters are provider-primary OpenAI pages for:

- ChatGPT Search and source/citation review;
- OpenAI image/audio provenance signals (C2PA/SynthID);
- OpenAI Platform documentation for optional explicitly declared external similarity/embedding methods.

These are source adapters, not assumptions about other AI providers. Each additional provider requires independent public evidence.

## Pairwise relation tensor

Use:

`R[i,j,r,t]`

where `r` is one of:

`SEMANTIC, LEXICAL, TEMPORAL, CITATION, PROVENANCE, CONTRADICTION, DERIVATION, FALSIFICATION`.

Relations rank or cluster nodes. They do not merge identities or erase provenance boundaries.

## Private Conversations Chunky bridge

Public CI never requires private bytes.

Private side may produce:

`opaque_id + keyed commitment + temporal_index + relation_index + exported aggregate vector features`.

Recommended commitment: `BLAKE3-256-KEYED`.

If semantic/vector features require private text, compute them on the private side and export only explicitly authorized aggregates. Otherwise leave them `TOKEN_VAZIO`.

## Suggested ChatGPT packet

A packet should contain:

1. `question_or_hypothesis`
2. `nodes`
3. `site_conditions`
4. `content_vectors`
5. `evidence_vectors`
6. `relations`
7. `falsifiers`
8. `gaps`
9. `requested_output`

Recommended output from the evaluator:

- ranked relations;
- contradictions;
- supporting evidence;
- falsifiers;
- `TOKEN_VAZIO` fields;
- sensitivity to weight changes;
- final claim gate.

## Dynamic weights

Content dimensions may use dynamic weighting such as:

`w_k(t)=exp(beta*z_k(t))/sum_j exp(beta*z_j(t))`

but evidence remains an orthogonal ceiling. Changing content weights can alter navigation/ranking; it cannot upgrade an evidence class.

## Fail-closed examples

Forbidden promotions include:

- high semantic similarity -> same author;
- text style -> provider proof;
- image style/resolution -> provider proof;
- embedding cosine -> causality;
- correlation -> causality;
- content hash -> semantic equivalence;
- private commitment -> disclosure/reconstruction of private content.

`VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM`
