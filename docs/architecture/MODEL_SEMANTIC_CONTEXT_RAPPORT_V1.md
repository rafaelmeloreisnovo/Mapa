# Model Semantic Context Rapport V1

**Date:** 2026-08-27
**State:** `IMPLEMENTED_PROPOSED / STRUCTURAL_PASS_LOCAL`
**Authority:** `Mapa` for ontology, relations, gaps and routing; the exact model producer remains authority for tokenizer, weights, tensors, architecture and runtime.
**Claim:** `claim_allowed=false`

## 1. Objective

This contract connects four surfaces without collapsing them:

```text
human language
→ provider tokenization
→ native model computation
→ observed output
→ external semantic interpretation and rapport
```

It answers what can be represented about tokens, embeddings, layers, weights
and tensors while keeping a closed or proprietary model fail-closed.

The implementation does **not** inspect, modify or reconstruct provider model
weights. It prevents the absence of access from being replaced by a plausible
story.

## 2. The acronym boundary

The letters are not interchangeable. Every acronym must be expanded before it
is used as architecture evidence.

| Symbol | Expansion | What it denotes | Boundary |
|---|---|---|---|
| `ANN` | Artificial Neural Network | broad family | says little about sequence dynamics |
| `RNN` | Recurrent Neural Network | recurrent hidden-state family | not automatically LSTM, Transformer or LLM |
| `LSTM` | Long Short-Term Memory | gated recurrent architecture | four letters name an architecture, not a model license or artifact |
| `GRU` | Gated Recurrent Unit | gated recurrent architecture | requires exact producer evidence when attributed to a model |
| `LNN` | ambiguous | Liquid Time-constant **or** Logical Neural Network | expansion is mandatory; silent resolution fails |
| `LTC` | Liquid Time-constant Network | continuous-time recurrent family | primary liquid-network paper uses LTC terminology |
| `LLM` | Large Language Model | capability/scale class | does not prove a Transformer implementation |
| `Transformer` | Transformer architecture | attention-based architecture | generic paper does not prove a closed provider runtime |

Primary anchors:

- Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762).
- Hochreiter and Schmidhuber, [Long Short-Term Memory](https://pubmed.ncbi.nlm.nih.gov/9377276/).
- Hasani et al., [Liquid Time-constant Networks](https://arxiv.org/abs/2006.04439).
- Riegel et al., [Logical Neural Networks](https://arxiv.org/abs/2006.13155).

These papers define families. They are not evidence that a particular unbound
provider uses one of those families.

## 3. The computational chain

Let the observed text be `s` and a tokenizer artifact be `T_v`:

\[
(t_1,\ldots,t_n)=T_v(s)
\]

The token IDs may index rows in an embedding table `E`:

\[
x_i=E[t_i]
\]

For a recurrent architecture, a candidate form is:

\[
h_i=f_\theta(x_i,h_{i-1})
\]

For a layered architecture, the more general form is:

\[
H^{(\ell+1)}=B_\ell(H^{(\ell)};\theta_\ell)
\]

An output head can produce logits and a decoder can select a continuation:

\[
z=W_o h+b,\qquad p=\operatorname{softmax}(z),\qquad y\sim D(p,c)
\]

These equations explain candidate mechanisms. Until `T_v`, `E`, `theta`, the
architecture, decoder and execution receipt are bound, the concrete internal
path remains `TOKEN_VAZIO`.

## 4. Tensor is not weight

| Object | Typical role | Persists as learned parameter? |
|---|---|---|
| Token ID | discrete index | no |
| Embedding row | vector selected from a table | table may be a parameter |
| Weight | learned parameter | normally yes between inference calls |
| Activation | runtime value produced by computation | normally no |
| Hidden/recurrent state | runtime sequence state | depends on runtime boundary |
| KV/runtime cache | inference acceleration/context state | not the same as trained weights |
| Logit | output score before decoding | no |
| External semantic vector | Mapa/index projection | never assumed equal to a native embedding |

Every weight can be represented by a tensor, but not every tensor is a weight.

## 5. Context does not silently mean training

| Execution mode | What context may change | What requires separate evidence |
|---|---|---|
| `INFERENCE_FIXED_PARAMETERS` | inputs and activations | any weight update |
| `INFERENCE_STATEFUL_CACHE` | inputs, activations and cache | persistent memory or parameter training |
| `TRAINING_FULL_PARAMETERS` | full parameter set | before/after digests and training receipt |
| `ADAPTATION_PARAMETER_SUBSET` | adapters or declared subset | exact subset, optimizer and artifact identity |
| `ONLINE_LEARNING` | runtime-selected parameters | update trigger, rollback and execution receipt |
| `UNKNOWN_PROVIDER_RUNTIME` | only input/output are safely assumed observed | weights, cache, architecture, memory and training remain typed gaps |

The governing invariant is:

```text
context_conditioning != parameter_training
```

If a system actually performs online learning, the contract accepts an
`UPDATES_PARAMETER` edge only when the execution mode permits it and a typed
provider/local execution receipt is attached.

## 6. Rapport is an external governed projection

`RAPPORT` here means a typed relation between addressable concepts or stages.
It is not a hidden neuron connection and its score is not a native model weight.

```text
native output text
→ INTERPRETED_AS
→ external semantic map
```

The packet also requires:

```text
native embedding → NOT_EQUIVALENT_TO → external semantic vector
context → DOES_NOT_ESTABLISH → parameter update
```

This preserves useful semantic navigation without claiming access to the
provider's latent space.

## 7. Closed-box treatment

For a proprietary or unbound model:

- input and output text may be `DIRECT_OBSERVED`;
- model declarations may be `PROVIDER_DECLARED` within their stated scope;
- tokenizer IDs, embedding table, weights, activations, logits and decoder are
  `PROPRIETARY_WITHHELD` or `TOKEN_VAZIO` unless separately bound;
- `MEASURED_LOCAL` requires an authorized artifact and local receipt;
- an `LLM` label cannot promote the architecture to `TRANSFORMER`;
- absence of a visible weight update is not proof that no provider-side update
  process exists.

The current fixture deliberately binds no provider model. Its six blocking
gaps cover tokenizer, weights, activations, decoder, architecture and rights.

## 8. Rights are separate artifacts

The following units are independently governed:

```text
CODE | WEIGHTS | TOKENIZER | DATASET
```

A repository license cannot silently relicense model weights, tokenizer files
or training/evaluation data. Each non-empty rights state requires an
authoritative license source in the packet.

## 9. Artifacts and gate

```text
contracts/model-semantic-rapport.v1.json
schemas/model-semantic-rapport.v1.schema.json
examples/model-semantic-rapport.closed-provider.v1.json
tools/validate_model_semantic_rapport.py
tests/test_model_semantic_rapport.py
.github/workflows/model-semantic-rapport-v1.yml
navigation/MODEL_SEMANTIC_RAPPORT_V1.md
```

Local gate:

```bash
python3 tools/validate_model_semantic_rapport.py
python3 -m unittest -v tests.test_model_semantic_rapport
```

`PASS` means that IDs, relations, observability boundaries, update modes,
rights units, gaps and falsifiers are internally coherent. It does not mean
that hidden model internals were observed.

The CI parses the schema and packet as JSON, then applies the dependency-free
semantic validator. Validation by an independent third-party JSON Schema
engine is not claimed by this gate.

## R3

**F_ok:** external semantics, native-model stages, context effects, rights and
closed-box gaps are separately machine-addressable.
**F_gap:** exact provider, model, tokenizer, architecture, weights, activations,
decoder and licenses remain unbound.
**F_next:** bind an authorized inspectable producer artifact before promoting
any internal tensor or parameter claim.
