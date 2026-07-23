# CI canônica de ingestão científica privada

## Decisão de arquitetura

```text
Mapa privado
  → coleta metadados
  → normaliza e deduplica
  → preserva registros integrais e revisão
  → gera artefatos numerados
  → produz pacote público sanitizado

RLL público
  → recebe somente navegação revisada
  → executa testes científicos locais
  → publica resultados e limites próprios
```

O RLL não deve coletar nem armazenar automaticamente o acervo bruto, consultas privadas,
notas de revisão ou hipóteses não liberadas. A autoridade bibliográfica permanece no `Mapa`.

## Fontes v1

1. Crossref — metadados DOI multidisciplinares.
2. OpenAlex — grafo aberto de obras, autores, instituições e citações.
3. Semantic Scholar — grafo acadêmico e recursos semânticos.
4. Europe PMC — biomedicina e ciências da vida.
5. arXiv — física, matemática, computação e áreas relacionadas.
6. SciELO Livros/OAI-PMH — ciência aberta latino-americana.
7. Google Scholar — somente importação manual; nenhuma raspagem automatizada.

## Artefatos

```text
00_MANIFEST.json
01_RAW_NORMALIZED.jsonl
02_UNREVIEWED.jsonl
03_EVOLVING_SYNTHESIS.json
04_HYPOTHESIS_CANDIDATES.jsonl
05_UNLIKELY_CURRENT_EVIDENCE.jsonl
06_CONFLICTED.jsonl
07_REVIEWED_EVIDENCE.jsonl
08_TOKEN_VAZIO.jsonl
09_RLL_PUBLIC_EXPORT.json
10_ID_REGISTRY_PROPOSAL.json
CHECKSUMS.sha256
```

O artefato 03 evolui por marcos de volume e estrutura. Esses marcos criam um snapshot; não
promovem claims. A promoção depende exclusivamente de ledger de revisão com autoria, data,
razão, falsificador, base de evidência e fronteira de uso. O artefato 10 propõe novas
numerações; somente revisão e commit explícito atualizam o registro canônico, evitando que
novos itens renumerem registros históricos.

## Sete direções

| Direção | Aplicação |
|---|---|
| Direta | registrar exatamente título, autores, identificadores e fonte |
| Inversa | recuperar DOI, dataset, instituição, versão e origem editorial |
| Recíproca | cruzar fontes sem contar duplicatas como evidências independentes |
| Contrária | guardar retratações, críticas, resultados negativos e conflitos |
| Antiderivada | reconstruir consulta, adaptador, timestamp e transformação |
| Derivada | gerar novos candidatos, relações e perguntas testáveis |
| Retroalimentação | atualizar síntese e próximo gate sem apagar estados anteriores |

## 360° XYZ

- **X — sequência:** IDs monotônicos `LIT-00000001...` e artefatos `00...10`.
- **Y — sustentação:** estado editorial, revisão, falsificador e fonte.
- **Z — profundidade:** metadado, texto, claim, teste local, replicação e publicação.
- **360°:** múltiplas fontes e domínios, com o mesmo núcleo de proveniência.

## Estados

`UNREVIEWED` é a entrada padrão. `HYPOTHESIS_CANDIDATE`,
`UNLIKELY_UNDER_CURRENT_EVIDENCE`, `CONFLICTED` e `REVIEWED_EVIDENCE` exigem revisão
explícita. `TOKEN_VAZIO` representa metadado ou evidência insuficiente.

```text
quantidade de papers != verdade
mesmo DOI em três índices != três experimentos independentes
evidência externa != evidência local do RLL
artefato público != acervo privado
```

## Limites operacionais v1

- CI executa somente fixture determinística; não consulta a rede.
- coleta online é manual, limitada e falha fechada.
- cache, backoff, OAI-PMH SciELO e parser Atom do arXiv permanecem `TOKEN_VAZIO_CODE`.
- nenhum token, segredo, abstract privado ou nota de revisão entra no pacote público.
- o RLL público permanece sem alteração automática.
