# Sementeira Cognitive × Locator Gate V1

Estado: `FAIL_CLOSED` · `STDLIB_ONLY` · `claim_allowed=false`

## Lacuna fechada

O resolver já provava a identidade dos bytes observados, mas o gate cognitivo ainda não verificava que **cada evidência usada por cada claim** correspondia exatamente a um resultado `HASH_MATCH`.

A integração agora é:

```text
claim
→ evidence_ref
→ evidência declarada no payload cognitivo
→ resultado do locator
→ locator idêntico
→ SHA declarado = SHA esperado = SHA observado
→ somente então READY_FOR_DOMAIN_SPECIFIC_REVIEW
```

## Bloqueios obrigatórios

Qualquer um destes estados impede o claim de atravessar o portão:

```text
HASH_MISMATCH
TOKEN_VAZIO_UNRESOLVED
BLOCKED_LOCATOR
resultado ausente
locator divergente
SHA divergente
receipt adulterado
payload e receipt sem vínculo criptográfico
```

## Limite invariável

```text
READY_FOR_DOMAIN_SPECIFIC_REVIEW
≠ EVIDENCED
≠ PROVED
≠ REPLICATED
```

A identidade dos bytes habilita somente o próximo julgamento adequado ao domínio. O gate mantém:

```text
claim_allowed=false
epistemic_promotion_allowed=false
```

## Execução

```sh
python3 scripts/sementeira_cognitive_locator_gate.py \
  examples/sementeira-cognitive-locator-gate-example.json \
  --output auditoria/SEMENTEIRA_COGNITIVE_LOCATOR_GATE_LOCAL_RECEIPT_2026-07-28.json \
  --strict
```
