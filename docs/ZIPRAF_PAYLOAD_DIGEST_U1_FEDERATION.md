# ZIPRAF Payload Digest U1 — Federação de Evidência

Status: `REMOTE_KAT_PASS / PRODUCER_PR_OPEN`  
Data: `2026-08-01`  
Claim global: `claim_allowed=false`

## 1. Resultado

U0 determinou onde o payload está. U1 determina qual sequência de bytes foi observada e qual algoritmo produziu sua identidade.

```text
entry
→ payload_offset + stored_size
→ digest_scope
→ algorithm + provider
→ digest
→ receipt
```

Gate produtor:

```text
ZIPRAF Payload Digest U1
run 30721856193 = success
checks = 17
```

## 2. Produtores

```text
SHA-256:
  RMR_PORTABLE_C

BLAKE3:
  rafaelmeloreisnovo/BLAKE3
  commit ff6991d8b13f5b4b16dc311b5acc9c63ae835152
  C API 1.8.2
  portable backend, SIMD disabled no gate
```

O commit, e não o nome `master`, faz parte da evidência.

## 3. Escopos

```text
STORED_BYTES
  bytes exatos no span do arquivo ZIP.

LOGICAL_BYTES_STORE
  equivalente ao stored span apenas para STORE válido.

LOGICAL_BYTES_DEFLATE
  MATERIALIZATION_REQUIRED.
```

O digest dos bytes DEFLATE não é silenciosamente promovido a digest do conteúdo descomprimido.

## 4. Receipt

```text
gate: ZIPRAF_PAYLOAD_DIGEST_U1_V1
status: PASS
checks: 17
receipt_sha256: 5c02f528713539e33d0cfabf6c99fa6d03b619c16d645b6c3ef099b0c93b2cb4
scope: STORED_BYTES_AND_STORE_LOGICAL_BYTES_NO_DEFLATE_MATERIALIZATION
```

A cota de artefatos impediu o armazenamento redundante, não a validação. O receipt e seu SHA-256 foram produzidos no log antes do upload best-effort.

## 5. Separações obrigatórias

```text
CRC32 != identidade criptográfica
digest != assinatura
digest != autoria
digest != confiança
digest != autorização de execução
digest != autorização DMA
digest != clock
stored digest != DEFLATE logical digest
```

## 6. Reparo de Formula CI

O workflow falhava porque `formula_ci.model` não existia, enquanto a implementação canônica já estava em `engine/model.py`.

A correção criou uma ponte de compatibilidade:

```text
formula_ci.model → engine.model
```

Nenhum peso ou fórmula foi duplicado. O run `30721856200` passou. O próprio modelo continua explicitamente ilustrativo, sem promoção científica.

## 7. Falsificadores federados

O gate rejeita:

- mudança do commit BLAKE3;
- mudança do SHA-256 do receipt;
- CRC32 promovido a identidade;
- digest promovido a assinatura, autoria, execução ou DMA;
- stored digest promovido a conteúdo lógico DEFLATE;
- cópia paralela da fórmula;
- fórmula ilustrativa promovida a claim científico;
- Android ou U2 marcados como provados.

## 8. Próxima dependência

```text
U2 = REAL_ZIP_APK_CORPUS
```

Saída exigida:

```text
manifesto por entrada
+ algorithm
+ scope
+ digest
+ sizes
+ offsets
+ provider commit
+ ação de leitura
+ motivo de rejeição
+ mapping epoch
```

## R3

```text
F_ok:
  SHA-256 e BLAKE3 foram verificados sobre payloads delimitados,
  com provedor pinado, receipt hasheado e escopos separados.

F_gap:
  corpus real ZIP/APK, manifestos por entrada, DEFLATE materializado,
  assinatura de manifesto, Android e replicação independente.

F_next:
  executar U2 sobre corpus real, sem extrair entradas STORE apenas
  para identificá-las, e produzir um relatório append-only por arquivo.
```
