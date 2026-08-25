# JSON Totality Invariant Contract V1

**State:** IMPLEMENTED / VERIFICATION_PENDING  
**claim_allowed:** false  
**Authority:** `rafaelmeloreisnovo/Mapa`  
**Scope:** JSON, JSONL and `*.jsonl.txt` governed artifacts; NOVOexport/MESSAGES; longitudinal memory vectors; receipts and governance objects when classified as governed.

## 1. Invariant-mother

The representation may evolve, but the chain that permits return to origin must remain traceable:

```text
IDENTITY -> PROVENANCE -> LINEAGE -> EPISTEMIC_BOUNDARY -> CLAIM_GATE
```

Equivalent operational rule:

```text
text -> token -> chunk -> vector -> index -> relation
relation -> index -> vector -> chunk -> message -> source_pointer -> source JSON
```

The second path does not require byte-identical reverse transformation of every derived representation. It requires an auditable route back to the governed source identity and custody evidence.

## 2. What is invariant and what is mutable

### Preserved dimensions

1. **Identity** — stable object identity appropriate to the profile (`message_id`, `node_id`, `conversation_id`, `vector_id`, `artifact_id`, etc.).
2. **Provenance** — source pointer/path/ref plus digest or typed gap when the profile requires it.
3. **Lineage** — parent/revision/previous hash/temporal lineage, with explicit root allowed.
4. **Epistemic boundary** — observed/derived/interpreted/hypothesis/TOKEN_VAZIO states cannot collapse into each other silently.
5. **Claim gate** — governed material remains fail-closed (`claim_allowed=false`) until a separate evidence gate authorizes a different claim state in the owning domain.

### Mutable dimensions

Text serialization, tokenization, chunk size, index order, vector embedding, derived labels, view projections, routing order and presentation may change provided the preserved dimensions remain traceable and the delta is explicit.

## 3. Profile-aware application

A single flat schema is not imposed on every JSON object.

### MESSAGE profile

Required structural custody fields:

```text
conversation_id
message_id
node_id
parent_id
source_path
source_pointer
text_hash
epistemic_state
privacy_class
claim_allowed
```

Rules:

- `message_id == node_id` for the current NOVOexport-derived message profile unless a future version explicitly declares a different mapping.
- `parent_id` may be null for a root, but the field must be present.
- `text_hash` must be SHA-256 or a typed `TOKEN_VAZIO_*` only where the producing schema explicitly permits a gap.
- `claim_allowed` must remain false in this audit layer.

### LONGITUDINAL_VECTOR profile

The auditor inherits the mandatory invariants already encoded by `validate_longitudinal_vector_evolution.py`:

```text
source_is_not_interpretation
parable_is_not_physical_proof
token_vazio_is_not_zero
new_dimension_requires_semantics_type_source_and_state
weights_require_calibration_and_evidence
no_hidden_model_state_claim
append_never_silently_overwrites_ancestor
relation_requires_type_and_source
```

And the five gates:

```text
provenance
delta_identity
semantic_consistency
evidence_or_typed_gap
reversibility
```

### GOVERNED_GENERIC profile

Objects exposing governance markers such as `claim_allowed`, `epistemic_state`, `f_gap` or `source_pointer` are audited without pretending to know a domain-specific schema. Missing identity/provenance/lineage/epistemic boundaries become typed gaps.

### UNGOVERNED_GENERIC profile

Ordinary JSON that has no governance marker is reported but not promoted into a governed PASS. Its state is `UNCLASSIFIED_NON_GOVERNED`.

## 4. Conservation metric

For the governed scope:

```text
conservation_rate = governed_pass / governed_records
```

Five orthogonal coverage metrics are emitted independently:

```text
C_identity
C_provenance
C_lineage
C_epistemic_boundary
C_claim_gate
```

A global conservation rate of `1.0` is necessary for full structural closure of the selected governed scope, but it does not prove the truth of the content.

## 5. Fail-closed gaps

Examples:

```text
TOKEN_VAZIO_MESSAGE_SOURCE_POINTER_ABSENT
TOKEN_VAZIO_MESSAGE_TEXT_HASH_ABSENT
TOKEN_VAZIO_IDENTITY_ABSENT
TOKEN_VAZIO_PROVENANCE_ABSENT
TOKEN_VAZIO_LINEAGE_ABSENT
TOKEN_VAZIO_EPISTEMIC_BOUNDARY_ABSENT
TOKEN_VAZIO_CLAIM_GATE_OPEN
TOKEN_VAZIO_GATE_*_NOT_CLOSED
TOKEN_VAZIO_JSON_PARSE_ERROR
```

Gaps are repaired at the source or producing transform; the auditor must never synthesize missing custody evidence.

## 6. Executable materialization

- auditor: `scripts/audit_json_totality_invariants.py`
- report schema: `schemas/json-totality-invariant-audit.v1.schema.json`
- positive fixture: `tests/fixtures/json_totality/messages-pass.jsonl`
- negative fixture: `tests/fixtures/json_totality/messages-gap.jsonl`
- tests: `tests/test_json_totality_invariants.py`

Example:

```bash
python3 scripts/audit_json_totality_invariants.py \
  /path/to/NOVOexport \
  --report out/json-totality-report.json \
  --findings out/json-totality-findings.jsonl \
  --strict
```

## 7. Cross-domain routing

### NOVOexport / Memory N

The message record remains source-bound through IDs, pointer, hash and state. Derived memory nodes must retain a route back to that tuple instead of replacing it.

### Mapa

Mapa owns the invariant-routing contract and typed gaps. It does not become the scientific authority for domain content.

### RLL

RLL equations, hypotheses and derived scientific notes may reference the invariant tuple. The tuple proves custody/traceability, not scientific truth. An RLL claim still requires its own evidence/falsifier gate.

## 8. Non-regression

Forbidden transformations:

```text
source -> interpretation with source identity discarded
TOKEN_VAZIO -> zero/default invented value
message -> chunk without source pointer or recoverable message identity
derived label -> evidence by repetition
symbolic relation -> physical proof by analogy
ancestor -> overwritten state without explicit delta/receipt
claim_allowed false -> true because a transform completed successfully
```

## 9. Gate

`FULL_TOTALITY_CLOSED` is allowed only when:

1. every file in the explicitly declared governed scope was scanned;
2. every governed record was classified;
3. every governed record passed its profile invariant;
4. each dimension coverage is `1.0`;
5. parse failures are zero;
6. the report and findings are hashed/receipted;
7. the input manifest itself is fixed and hashed.

Until the input manifest for the complete intended corpus is fixed and audited, the state remains **VERIFICATION_PENDING** and `claim_allowed=false`.

## F_ok

- mother invariant formalized;
- profile-aware executable auditor materialized;
- positive and negative fixtures materialized;
- fail-closed typed gaps materialized;
- NOVOexport/Memory N/Mapa/RLL routing boundary explicit.

## F_gap

- full Drive corpus has not yet been materialized into one immutable input manifest inside this branch;
- therefore no statement of 100% corpus conservation is authorized yet.

## F_next

Materialize the complete governed input manifest (Drive IDs + sizes + hashes/source pointers), run the auditor over every selected shard, emit a receipt, then close only the gaps at their producing source.
