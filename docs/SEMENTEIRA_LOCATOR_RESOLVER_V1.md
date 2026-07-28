# Sementeira Locator Resolver V1

Estado: `READ_ONLY` · `STDLIB_ONLY` · `FAIL_CLOSED` · `claim_allowed=false`

## Problema fechado

O gate 5×7 validava que um locator e um SHA-256 estavam presentes, mas não relia o artefato apontado. Assim, um hash bem formatado podia continuar sem correspondência física comprovada.

## Contrato

```text
locator declarado
→ normalização segura
→ confinamento à raiz autorizada
→ leitura em streaming
→ SHA-256 recalculado
→ comparação
→ receipt determinístico
```

Estados:

- `HASH_MATCH`: o arquivo foi localizado e seu SHA-256 coincide.
- `HASH_MISMATCH`: o arquivo existe, mas os bytes não correspondem.
- `TOKEN_VAZIO_UNRESOLVED`: o artefato não foi localizado ou o esquema não é resolvido localmente.
- `BLOCKED_LOCATOR`: locator absoluto, travessia, NUL, diretório ou escape por symlink.

## Invariantes

1. Nenhuma escrita no artefato resolvido.
2. Nenhuma rede.
3. Nenhum locator absoluto.
4. Nenhum `..` capaz de escapar da raiz.
5. Symlink que sai da raiz é bloqueado.
6. Hash é calculado em streaming.
7. O resolver prova identidade de bytes observados; não prova verdade do claim.
8. Mesmo com todos os hashes coincidentes, `epistemic_promotion_allowed=false`.

## Execução

```sh
python3 scripts/sementeira_locator_resolver.py \
  examples/sementeira-locator-resolution-example.json \
  --root . \
  --output auditoria/SEMENTEIRA_LOCATOR_RESOLUTION_LOCAL_RECEIPT_2026-07-28.json \
  --strict
```

## Gate de promoção

```text
HASH_MATCH de todos os refs
≠ claim comprovado
```

O resultado habilita apenas a próxima análise pelo gate cognitivo, que ainda exige método, falsificador, teste adequado ao domínio e, quando aplicável, replicação independente.
