# ZIPRAF Corpus U2 — Federação de Evidência

Status: `HARNESS_REMOTE_GATE_PASS / EXTERNAL_CORPUS_TOKEN_VAZIO`  
Data: `2026-08-01`  
Claim global: `claim_allowed=false`

## 1. Resultado federado

O produtor `Vectras-VM-Android#1079` executou o gate:

```text
ZIPRAF Corpus U2
run 30722482763 = success
```

Receipt delimitado:

```text
archives_total = 3
parsed_archives = 2
parse_failures = 1
entries_total = 6
entries_rejected = 0
extraction_performed = false
execution_authorized = false
manifest_sha256 = a92f5e288a596972289a6cff843d2fd5d9bff326964daa71902c56d5ad1635f5
external_real_corpus = TOKEN_VAZIO
```

## 2. Dependência empilhada

```text
PR #1078: U0 spans + U1 digests
         ↓
PR #1079: U2 scanner/manifesto
```

A PR U2 está baseada na branch U0/U1. Ela não deve ser tratada como independente nem retargetada para `master` antes da decisão humana sobre a dependência.

## 3. O que o harness observa

### Arquivo

```text
nome e caminho
container_kind
mapping_epoch
tamanho
SHA-256
BLAKE3
estado de parse
fingerprint de layout
marcadores estruturais APK
```

### Entrada

```text
nome
offsets e tamanhos
método ZIP
CRC32 declarado
ação e flags
SHA-256/BLAKE3 dos bytes armazenados
estado do digest lógico
execution_authorized=false
dma_authorized=false
```

## 4. Fixtures

```text
sample.zip
  readme.txt STORE
  packed.txt DEFLATE

sample.apk
  AndroidManifest.xml STORE
  classes.dex STORE
  resources.arsc DEFLATE
  assets/data.bin STORE

malformed.zip
  arquivo truncado → PARSE_REJECTED
```

O arquivo `.apk` é um candidato estrutural sintético. Não é um APK de produção assinado, instalável ou executado.

## 5. Limites de promoção

```text
fixture ≠ corpus externo independente
extensão .apk ≠ validade APK
marcadores APK ≠ assinatura
marcadores APK ≠ instalação
manifesto ≠ execução
manifesto ≠ DMA
stored DEFLATE digest ≠ logical digest
scanner ≠ extractor
scanner ≠ loader
```

## 6. Privacidade

Corpus público exige fonte, commit/release, SHA-256, licença/proveniência, limite de tamanho e estado esperado.

Corpus privado deve permanecer local. O que pode ser federado é um receipt sanitizado, sem nome pessoal, caminho local sensível ou conteúdo do arquivo.

```text
PRIVATE_CORPUS
→ local scanner
→ sanitized receipt
→ federated evidence
```

## 7. Falsificadores

O gate federado rejeita:

- fixture promovida a corpus externo;
- extensão/marcadores promovidos a validade, assinatura ou instalação;
- manifesto promovido a execução ou DMA;
- DEFLATE armazenado promovido a conteúdo lógico;
- alteração do SHA-256 do manifesto;
- publicação automática de corpus privado;
- U2 marcado como independente de U0/U1;
- APK de produção ou corpus externo marcados como provados.

## 8. Próxima etapa

```text
U2_REAL_CORPUS = TOKEN_VAZIO
```

Caminhos válidos:

1. corpus público pequeno, licenciado e pinado;
2. APK produzido pelo pipeline, com SHA-256 e assinatura verificável;
3. corpus privado no Termux, publicando apenas receipt sanitizado.

## R3

```text
F_ok:
  scanner, determinismo, receipt, manifesto por entrada, privacidade
  e falsificadores foram verificados e federados.

F_gap:
  corpus externo independente, APK real assinado, instalação Android,
  DEFLATE lógico e reprodução Termux.

F_next:
  selecionar a fonte do corpus real e produzir receipts sem permitir
  que observação de bytes seja confundida com autorização de execução.
```
