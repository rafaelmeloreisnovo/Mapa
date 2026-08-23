# ALL_TOKEN_INDEX_STATUS_V1 — checkpoint lexical sem filtro

Status: `EXECUTED / COMPLETE_FOR_MOUNTED_SOURCE_SET / claim_allowed=false`

Data do checkpoint: `2026-08-23`

## Objetivo

Registrar no Mapa, sem copiar conteúdo privado, o resultado executado da indexação literal `ALL_TOKEN` sobre o conjunto privado efetivamente materializado.

A unidade mínima desta camada é o **token observado**, não uma área escolhida previamente.

## Invariante

`LITERAL != NORMALIZED != CONCEPT != AREA != CLAIM`

Consequências:

- nenhuma palavra é descartada por parecer banal;
- stopwords não são removidas na camada literal;
- símbolos e pontuação são preservados;
- normalização é projeção NFKC + casefold e nunca substitui o literal;
- repetição é informação e permanece como frequência/proveniência;
- classificação semântica acontece depois da preservação literal;
- similaridade não autoriza identidade;
- contagem de menções de área não é contagem final de áreas semânticas.

## Escopo observado

Conjunto privado montado e processado:

- `MESSAGES-00001..00019`
- inventário físico auxiliar equivalente a `temp.locate.txt`
- os registros `MESSAGES` observados apontam para `conversations-003.json` até `conversations-012.json`

O conteúdo bruto, tokens e localizadores privados **não são persistidos neste repositório público**.

## Receipt agregado

| Métrica | Valor observado |
|---|---:|
| message shards | 19 |
| bytes em MESSAGES | 185,953,216 |
| mensagens JSON válidas | 91,232 |
| registros JSON inválidos | 0 |
| conversas distintas | 1,000 |
| ocorrências de tokens | 44,185,626 |
| tokens literais distintos | 675,638 |
| formas normalizadas distintas | 612,471 |
| relações token → fonte | 1,245,720 |
| menções explícitas área/domínio/campo/disciplina | 27,065 |
| cabeçalhos estruturais distintos | 962 |
| entradas reconhecidas no inventário físico | 15,437 |

Artefato derivado privado/local: `RAFAELIA_TOTAL_INDEX_V1.zip`

SHA-256 do pacote derivado: `2e63c1f242ee6670847787b2642f411207c1a1816edfd1ad6453b26946d2853e`

Tamanho observado do pacote: `38,305,760 bytes`.

## Artefatos privados derivados

O pacote contém projeções como:

- `tokens_literal.tsv.gz`
- `tokens_normalized.tsv.gz`
- `token_source_counts.tsv.gz`
- `explicit_area_mentions.tsv.gz`
- `structural_headings.tsv.gz`
- `source_manifest.tsv`
- `top_tokens.tsv`
- `manifest.json`
- `README.md`
- `SHA256SUMS`

Esses nomes documentam a estrutura; **não autorizam publicação do conteúdo privado**.

## Fronteira epistemológica

Este checkpoint prova a execução lexical sobre o conjunto montado. Ele **não** prova:

1. cobertura lexical de todo o NOVOexport;
2. contagem final de áreas semânticas;
3. que um cabeçalho seja automaticamente uma área;
4. que uma forma normalizada seja semanticamente idêntica a outra;
5. qualquer claim científico derivado da frequência dos tokens.

## TOKEN_VAZIO federado

- `TV-RAW-OUTSIDE-003-012` — bytes brutos fora de `conversations-003..012` ainda não foram materializados nesta execução.
- `TV-SEMANTIC-AREA-CLUSTER` — a contagem exata de áreas exige classificação/deduplicação sobre o índice literal completo; 27,065 menções e 962 cabeçalhos são evidência intermediária, não resultado final.
- `TV-GITHUB-FULL-TEXT` — repositórios GitHub não foram exaustivamente tokenizados neste V1.

A autoridade de gaps continua sendo `data/audits/TOKEN_VAZIO_REGISTRY.jsonl`; este documento não cria registry paralelo.

## Próxima transformação permitida

`remaining raw sources → same ALL_TOKEN contract → append-only merge → expression/ngram extraction → concept/entity resolution → semantic families → areas/domains → graph edges → evidence → claim gates`

Nenhuma etapa posterior pode apagar a ocorrência literal ou sua proveniência.

## F_ok / F_gap / F_next

**F_ok:** índice literal executado para o conjunto montado; agregados e pacote derivados registrados com hash.

**F_gap:** cobertura privada fora de `003..012`, clusterização semântica final de áreas e tokenização exaustiva dos repositórios continuam abertos.

**F_next:** materializar o restante do corpus privado sob o mesmo contrato ALL_TOKEN, unir append-only e só então calcular a taxonomia/áreas derivadas completas.
