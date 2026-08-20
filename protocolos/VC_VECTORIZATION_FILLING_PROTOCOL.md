# Vectra VC Preenchimento Protocol

**Document Version:** 1.0  
**Status:** INITIAL SPECIFICATION  
**Date:** 2026-08-20  
**Author:** RAFAELIA / ∆RafaelVerboΩ  
**Scope:** Verifiable Credential filling with token vectorization integration  

---

## Executive Summary

The Vectra VC Preenchimento (filling) protocol establishes a systematic method to:

1. **Vectorize** claim values through seven semantic directions
2. **Assess** vectorization quality and coherence
3. **Fill** W3C-compatible Verifiable Credentials with vectorized claims
4. **Validate** claims against vectorization gates
5. **Maintain** proof of vectorization lineage and quality metrics

## Core Invariants

```text
VECTORIZED_CLAIM = (claim_key, claim_value, vector[7], coherence, classification)

classification ∈ {FORTE, MODERADO, FRACO, ABORTADO}

VECTORIZATION_GATE:
  - FORTE     → coherence ≥ 0.75  → claim_allowed = true
  - MODERADO  → coherence ≥ 0.50  → claim_allowed = conditional
  - FRACO     → coherence ≥ 0.25  → claim_allowed = false (review required)
  - ABORTADO  → coherence  < 0.25 → claim_allowed = false (rejected)

TOKEN_VAZIO never replaces vectorization result
vectorization_generation tracks lineage
claim custody remains immutable after issuance
```

## Seven Semantic Directions

Each claim value is vectorized along these dimensions:

| Direction | Symbol | Semantic Domain | Function |
|---|---|---|---|
| **D1** | FORMAL_ARITMETICA | Formal proof, arithmetic rigor | `sin(hash × PHI)` |
| **D2** | COMPUTACIONAL | Computational topology, algorithms | `cos(length × SPIRAL)` |
| **D3** | GEOMETRICA_TOPOLOGICA | Geometric structure, topology | `sin(length × π/6)` |
| **D4** | SENSORIAL | Perceptual quality, entropy | `tanh(entropy)` |
| **D5** | LINGUISTICA_SEMANTICA | Linguistic distribution, semantics | `sin(unique_chars × PHI)` |
| **D6** | SISTEMICA_ARQUITETURAL | Systemic role, architecture | `cos(hash × SPIRAL_PI_PHI)` |
| **D7** | ETICA_VALIDACAO | Ethical gates, validation rules | `sin(length_ratio × SPIRAL)` |

## Three Evolution Chains

Claims are assigned to chains that govern their evolution:

| Chain | Designation | Governance | Use Case |
|---|---|---|---|
| **A** | NUCLEO_FORMAL | Tight formal convergence | Scientific claims, cryptographic proofs |
| **B** | PONTE_ENTRE_AREAS | Cross-domain bridges | Interdisciplinary assertions |
| **C** | CONVERGENCIA_DISTANTE | Creative, open convergence | Exploratory claims, speculative content |

Chain assignment is deterministic per vector via:

```text
formal_score   = D1 + D3   (arithmetic + geometric)
bridge_score   = D2 + D5   (computational + linguistic)
distant_score  = D4 + D7   (sensorial + ethical)
```

## VC Structure with Vectorization

### Payload

```json
{
  "@context": "https://example.com/credentials/v1",
  "issuer": "did:example:issuer",
  "subject": "did:example:subject",
  "issuedAt": 1692576000000,
  "expiresAt": 1724112000000,
  "claims": {
    "claim_key_1": "claim_value_1",
    "claim_key_2": "claim_value_2"
  },
  "vectorizedClaims": {
    "claim_key_1": {
      "text": "claim_value_1",
      "vector": [0.5, 0.6, 0.7, 0.4, 0.8, 0.3, 0.65],
      "chain": "NUCLEO_FORMAL",
      "classification": "FORTE",
      "coherence": 0.58
    },
    "claim_key_2": { ... }
  },
  "proof": {
    "vectorization_engine": "TokenVectorizationEngine",
    "vectorization_generation": "5",
    "filled_claims_count": "2",
    "average_coherence": "0.64"
  }
}
```

### Proof Metadata

The `proof` object contains:

| Field | Purpose | Type | Example |
|---|---|---|---|
| `vectorization_engine` | Engine identifier | String | `TokenVectorizationEngine` |
| `vectorization_generation` | Evolution cycle count | String | `"7"` |
| `filled_claims_count` | Number of vectorized claims | String | `"42"` |
| `average_coherence` | Mean coherence across claims | String | `"0.6432"` |

## Filling Process

### Stage 1: Initialization

```text
Input: claim_data ∈ Map<String, String>
Output: TokenVectorizationEngine instance
Action: new TokenVectorizationEngine()
Gate: ENGINE_READY
```

### Stage 2: Claim Vectorization

```text
for each (claim_key, claim_value) in claim_data:
  vector[7] = vectorize(claim_value)
  coherence = aggregate(vector[7])
  classification = classify(coherence)
  chain = assign_chain(vector[7])
  store(claim_key → VectorizedToken{...})
Gate: VECTORIZATION_COMPLETE
```

### Stage 3: Quality Assessment

```text
avg_coherence = mean(all coherence scores)
forte_count = count(classification == FORTE)
abort_count = count(classification == ABORTADO)

if abort_count > 0:
  claim_allowed = false
  reason = "ABORTADO_CLAIMS_PRESENT"
  
if avg_coherence < min_threshold:
  claim_allowed = conditional
  reason = "LOW_AVERAGE_COHERENCE"
  
else:
  claim_allowed = true
  
Gate: QUALITY_ASSESSMENT
```

### Stage 4: VC Assembly

```text
VC = {
  context, issuer, subject,
  claims (original key-values),
  vectorizedClaims (vectorized representations),
  proof (metadata),
  timestamps (issued_at, expires_at),
}
Gate: VC_READY_FOR_ISSUANCE
```

### Stage 5: Custody & Custody Chain

```text
VC.custody = {
  generation_timestamp,
  vectorization_generation_id,
  issuer_identity,
  claim_allowed (bool),
  next_verifiable_step,
}
Gate: CUSTODY_RECORDED
```

## Validation Gates

### Pre-Issuance Gates

| Gate | Condition | Action on Fail |
|---|---|---|
| `VECTORIZATION_COMPLETE` | All claims vectorized successfully | Reject VC, log error |
| `QUALITY_ASSESSMENT` | Coherence gates pass | Mark conditional / reject based on threshold |
| `NO_ABORTADO_CLAIMS` | Count(ABORTADO) == 0 | Escalate for review |
| `PROOF_METADATA_VALID` | All proof fields populated | Reject VC |

### Post-Issuance Gates

| Gate | Condition | Cadence |
|---|---|---|
| `EXPIRATION_CHECK` | `now < VC.expiresAt` | On every claim validation |
| `LINEAGE_AUDIT` | Proof.generation matches engine.generation | Audit cycle |
| `COHERENCE_DRIFT` | Compare issued vs. re-computed coherence | Quarterly |

## Governance Rules

### Claim Custody

```text
claim_allowed(VC) ⟺ (
  VC.proof.vectorization_generation is defined ∧
  VC.coherence >= min_threshold ∧
  count(ABORTADO) == 0 ∧
  VC.issuedAt is immutable ∧
  issuer_custody_chain is continuous
)
```

### Coherence Thresholds (Configurable)

| Mode | FORTE | MODERADO | FRACO | Default |
|---|---|---|---|---|
| **Strict** | ≥ 0.80 | ≥ 0.60 | ≥ 0.30 | `0.80` |
| **Standard** | ≥ 0.75 | ≥ 0.50 | ≥ 0.25 | `0.50` |
| **Permissive** | ≥ 0.60 | ≥ 0.40 | ≥ 0.20 | `0.25` |

### Evidence Requirements

- **VectorizedClaim.coherence** — auditable, deterministic recomputable
- **VectorizedClaim.vector[7]** — cryptographic hash proof optional
- **Proof.vectorization_generation** — links to engine state snapshot
- **Custody chain** — immutable ledger of creation, issuance, validation, revocation

## Integration Points

### With Mapa Governance

```text
VC.proof.vectorization_generation
  ↓
RafaeliaKernelV22 (generation counter)
  ↓
TokenVectorizationEngine (engine state)
  ↓
Governance.claim_allowed (yes/no/conditional)
```

### With Vectras-VM-Android Runtime

```text
VerifiableCredentialFiller
  → TokenVectorizationEngine.vectorize()
  → BuildCredential()
  → ProofMetadata.attach()
  → VC.issue()
```

## Implementation Status

| Component | Status | Location |
|---|---|---|
| TokenVectorizationEngine | ✅ STABLE | `rafaelia/token/TokenVectorizationEngine.java` |
| VerifiableCredential | ✅ IMPLEMENTED | `rafaelia/token/VerifiableCredential.java` |
| VerifiableCredentialFiller | ✅ IMPLEMENTED | `rafaelia/token/VerifiableCredentialFiller.java` |
| Test Suite | ✅ COMPREHENSIVE | `test/rafaelia/token/VerifiableCredentialFillerTest.java` |
| Governance Integration | 🔄 IN PROGRESS | Mapa control plane |
| Custody Ledger | 🔄 IN PROGRESS | `data/control-plane/vc-custody-ledger.v1.json` |

## Next Verifiable Steps

1. **Cryptographic Proof** — Attach JWS/JWZ signatures to VC payload
2. **Custody Ledger** — Record VC issuance, validation, and revocation in immutable ledger
3. **Governance Integration** — Link VC.claim_allowed to Mapa control plane
4. **Revocation Registry** — Implement DID-based revocation status lists
5. **Portability** — Export/import VC in W3C standard formats (JSON-LD, CBOR)

## Boundaries & Limitations

- **Vectorization is deterministic, not cryptographic:** Coherence serves as quality indicator, not proof of integrity
- **Chain assignment is probabilistic:** Same value may assign to different chains across engine generations
- **Coherence threshold is configurable:** No universal "safe" threshold; governance determines acceptance
- **TOKEN_VAZIO protocol:** Claims with ABORTADO classification never proceed to issuance without human review
- **Generation tracking:** VC tied to specific engine generation; re-vectorization on engine upgrade creates new VC

## References

- `TokenVectorizationEngine` — 7-direction semantic vectorization
- `RafaeliaKernelV22` — Mathematical constants (PHI, SPIRAL, PI)
- `CADEIA_DE_CUSTODIA_DADOS.md` — Governance and custody rules
- `INVARIANTE_EVOLUTIVA_ABSOLUTA_V1.md` — Scientific claim boundaries
- W3C Verifiable Credentials Data Model 1.1

---

**Document Signature Block:**

- Version: 1.0
- Locked: 2026-08-20
- Approver: RAFAELIA-GOVERNANCE
- claim_allowed for governance integration: false (until custody ledger initialized)
