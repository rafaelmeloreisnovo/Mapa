# Model Semantic Rapport V1 — Navigation Leaf

**State:** `IMPLEMENTED_PROPOSED`
**Authority:** subordinate leaf under `Mapa`; not a model producer.

## Route

```text
objective
→ contextual semantic packet
→ model semantic rapport
→ producer identity and observability boundary
→ typed nodes and edges
→ falsifier/gap
→ receipt
```

## Pointers

- Human contract: `ART:Mapa:docs/architecture/MODEL_SEMANTIC_CONTEXT_RAPPORT_V1.md`
- Machine control: `ART:Mapa:contracts/model-semantic-rapport.v1.json`
- Schema: `ART:Mapa:schemas/model-semantic-rapport.v1.schema.json`
- Closed-provider fixture: `ART:Mapa:examples/model-semantic-rapport.closed-provider.v1.json`
- Validator: `ART:Mapa:tools/validate_model_semantic_rapport.py`
- Tests: `ART:Mapa:tests/test_model_semantic_rapport.py`
- CI: `ART:Mapa:.github/workflows/model-semantic-rapport-v1.yml`

## Invariants

```text
semantic_token != tokenizer_token_id
external_semantic_vector != native_model_embedding
tensor != weight
context_conditioning != parameter_training
llm_label != transformer_architecture_proof
```

This leaf does not create a second ontology and does not replace the Session
Semantic Ledger, Contextual Semantic Packet, Semantic Tensor overlay or GPT
Layout. It composes their model-facing evidence boundary.

## R3

**F_ok:** the new contract is navigable from one bounded leaf.
**F_gap:** producer-level model evidence remains `TOKEN_VAZIO`.
**F_next:** qualify the exact branch and CI receipt without promoting runtime claims.
