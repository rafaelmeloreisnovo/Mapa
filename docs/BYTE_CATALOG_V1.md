# BYTE_CATALOG_V1 — estrada de bytes, não semântica inventada

State: `IMPLEMENTED_ON_DRAFT_BRANCH / CI_PENDING / claim_allowed=false`

## Parábola componente

A metáfora operacional é a **estrada de terra**:

```text
arquivo
  -> ZIP
  -> membro
  -> página
  -> bloco
  -> byte
  -> bit
```

Uma estrada pode estar mapeada mesmo quando não sabemos o significado do que passa por ela. Por isso a localização física/lógica pode ser `P_CATALOG` enquanto a semântica continua `TOKEN_VAZIO_UNBOUND`.

## BYTE8 antes de texto

O domínio basal é:

```text
BYTE8 = {0, 1, ..., 255}
```

ASCII é apenas a subcamada `0..127`. O catálogo de 256 valores separa:

- classificação ASCII;
- codepoint Latin-1;
- papel estrutural possível em UTF-8;
- bits e popcount;
- semântica, que permanece `TOKEN_VAZIO_UNBOUND`.

Um byte `0x80..0xFF` não recebe automaticamente um caractere UTF-8. O catálogo registra apenas seu papel estrutural possível.

## Duas réguas de memória

Para blocos de 64 bytes:

```text
64 bytes = 8 x 8 bytes = 16 leituras de 32 bits = 8 leituras de 64 bits
```

Para páginas de 256 bytes:

```text
256 bytes = 64 leituras de 32 bits = 32 leituras de 64 bits
```

As leituras são visões do mesmo intervalo de bytes. Elas não implicam uma ISA específica e não executam `ADD/MOV/JUMP/PUSH`.

## ZIP cataloger

`tools/catalog_zip_bytes_v1.py` usa somente a biblioteca padrão Python e **não extrai nem executa** membros do ZIP.

Para cada membro dentro dos limites declarados, registra:

- posição ordinal do membro;
- nome e flag de caminho inseguro;
- tamanho comprimido/descomprimido;
- CRC32 do header e CRC32 recomputado;
- SHA-256;
- estado ASCII/UTF-8;
- blocos de 64 bytes;
- páginas de 256 bytes;
- tiles hexadecimais 8x8;
- grupos de redundância por SHA-256 de bloco;
- contagens de leituras 32/64-bit;
- possível assinatura de ZIP interno como `TOKEN_VAZIO_NOT_EXPANDED`.

Arquivos criptografados, grandes demais ou não suportados não são forçados: recebem estado `TOKEN_VAZIO_*`.

## Redundância enumerada

Cada bloco observado recebe um grupo estável dentro daquela execução:

```text
R000001 -> ocorrência 1
R000001 -> ocorrência 2
...
```

A igualdade de SHA-256 do bloco prova igualdade dos bytes observados no escopo daquela catalogação, não igualdade semântica.

```text
byte_equal != text_equal != semantic_equal
```

## Catálogo e NP

`NP_CATALOG` e `P_CATALOG` continuam sendo notação operacional do roteador, não classes de complexidade.

O BYTE catalog reduz incerteza de **localização e estrutura**:

```text
ZIP -> member -> offset -> tile/page -> CRC/hash/redundancy
```

Ele não prova `P=NP` e não converte redundância em significado.

## Invariantes

```text
BYTE != CHARACTER != TOKEN != SEMANTICS
CRC != ERROR_CORRECTION
HASH_EQUALITY != SEMANTIC_EQUALITY
ADDRESSABLE != UNDERSTOOD
TOKEN_VAZIO != 0
SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM
```

## Reproduction

```bash
python tools/generate_byte_catalog_v1.py --output /tmp/byte_catalog_v1.jsonl
cmp /tmp/byte_catalog_v1.jsonl data/catalog/byte_catalog_v1.jsonl
python -m unittest tests.test_byte_catalog_v1
python tools/catalog_zip_bytes_v1.py sample.zip --include-word-views
```

## R3

`F_ok`: BYTE8 0..255, ASCII/Latin-1/UTF-8 structural layers, ZIP member addressing, CRC32, SHA-256, 8x8 blocks, 256-byte pages and redundancy groups are materialized.

`F_gap`: nested ZIP recursion, semantic interpretation, ISA execution semantics, ECC/error correction and physical-memory correspondence remain TOKEN_VAZIO.

`F_next`: after CI, bind BYTE_CATALOG observations into the manifold with stable source/artifact/observation IDs before adding any semantic relation.

`claim_allowed=false`
