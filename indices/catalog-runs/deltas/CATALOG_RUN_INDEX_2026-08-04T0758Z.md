# RAFAELIA — Catálogo incremental — 2026-08-04T0758Z

Estado: `APPEND_ONLY / CLAIM_ALLOWED=false / FAIL_CLOSED`

Checkpoint anterior: `Mapa@922281e329be499f1d6a4325a1c35cfd6c698070`

Referência prioritária: Google Drive `1g3eVD3zLMuwk0jevAwVL3wSmxhEMkKsAUPFQh2wEn88`.

## Delta distinguido

O Drive recebeu uma árvore extensa de código e superfícies de build depois do corte `2026-08-04T07:01:00Z`. Para evitar duplicação, este índice registra **famílias semânticas e relações pai-filho**, não uma cópia dos arquivos.

### Grupo de ferramentas de modelo

Pai observado: `1t-X8op6O3fROl3tJ-DXxhdEWKW5dKzuO` — título da raiz ainda `TOKEN_VAZIO`.

- `cvector-generator` — `1axd1ye4pREapXsJAyTqy4Id4LHVz0HOy`
- `export-lora` — `1mfC3VtFQ1mWFksdfVYotWXyY8PMwR1Y9`
- `gguf-split` — `1Md7dfcMHgJkFF4J_2lS4mOa6hU8nKy6I`
- `imatrix` — `1d-alxYwdllhfwIFJacGJp_2rkcKovWr0`
- `llama-bench` — `1QW6VS-SJFbpjFokLfB9yQ6IaO30-mQwO`
- `mtmd` — `1ancV9bQt5dcM8abGvziHhFflvhmsKoEy`
- `perplexity` — `19KcQl8Ep00C9-FemHkcj0PQlzgym6hH3`
- `quantize` — `12bQiPfFtX1l00VG6f-Jr08pIO94UnoPX`
- `rpc` — `1sXaQWIAEFAUPEfbbty6970VXQt4WVQfC`

### Grupo de aplicação e testes

- pai `1N4mpNJEUh75x9ryveQQYyof7hdvpltjz`: `bench`, `public`, `public_legacy`, `public_simplechat`, `tests`, `themes`;
- pai `1_Ph-rtt_6SHzyyAWR27MpPlbjPQ_GPAf`: `.storybook`, `e2e`, `scripts`;
- pai `1Wmlq5nDeL-V5xcubYpsUhRE3UFVYHjAT`: `ChatAttachments`, `ChatForm`.

## Rotas para humanos e IAs

- Quantização e formatos: `quantize`, `gguf-split`, `imatrix`.
- Avaliação e desempenho: `llama-bench`, `perplexity`, `bench`.
- Multimodal: `mtmd`, `legacy-models`.
- Interface e conversação: `public*`, `themes`, `ChatForm`, `ChatAttachments`.
- Verificação: `tests`, `unit`, `e2e`, `.storybook`.
- Automação e execução: `scripts`, `run`, `rpc`.

## Claims

| Classe | Registro |
|---|---|
| `PROVADO` | diretórios e relações de parent_id observados existem após o corte |
| `EVIDENCIADO` | os nomes e arquivos amostrados são consistentes com uma ingestão de fonte e build |
| `HIPÓTESE` | a árvore pode ser transformada em catálogo integral após inventário byte a byte |
| `MODELO_ANALÓGICO` | as famílias acima funcionam como mapa semântico de execução |
| `PARÁBOLA` | nenhuma nova |
| `REFUTADO` | nome de pasta prova compilação, origem, integridade ou completude |
| `TOKEN_VAZIO` | raiz canônica, revisão upstream, bytes, hashes, licenças, dependências e receipts de runtime |

## Dependências e limites

A extensão da árvore sugere fonte de software complexa, mas o ciclo não atribui repositório, fork ou revisão sem evidência. O conteúdo bruto permanece no Drive; o `Mapa` contém apenas ponte de proveniência e navegação.

Receipt: `data/catalog_runs/RAFAELIA_CATALOG_CYCLE_2026-08-04T0758Z.json`.

## Próximo gate verificável

`resolver raízes → inventariar arquivos/READMEs/manifests → exportar e hashear → identificar upstream/revisão → mapear dependências/testes → aplicar privacidade/licença → emitir receipt sucessor`
