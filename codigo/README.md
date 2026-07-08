# codigo/ — a ficha de entrada, codificada e coerente

> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ (ONU UDHR Art.1 · UNCRC Art.3)

Codificação executável do modelo descrito em `../biblioteconomia/15_FICHA_DE_ENTRADA.md`
e `../biblioteconomia/14_SUBSTRATO_BASE2.md`. **Só stdlib, determinista, sem dependências.**

## Arquivos

| Arquivo | Papel |
|---|---|
| `ficha_de_entrada.py` | modelo (`Ficha`), vocabulário fechado, validador, coordenada Ω reprodutível, os **28** já mapeados como exemplos |
| `test_ficha_de_entrada.py` | 11 testes de coerência (stdlib `unittest`) |
| `varredura_conteudo.py` | lê os arquivos/conteúdo dos 28, **hashing triplo** (coerência·integridade·prova), conceitos evidenciados e correlações; gera `../indices/MANIFESTO_INTEGRIDADE.yaml` |
| `test_varredura_conteudo.py` | 6 testes das funções deterministas (sem git) |
| `revisao_publicacao.py` | cruza **declarado (ficha) × evidenciado (conteúdo)**; gera `../indices/REVISAO_PUBLICACAO.md` |
| `marca_epistemica.py` | sugere reforço/rebaixamento de marca (`FATO`/`HIPOTESE`) por evidência+estrato; gera `../indices/MARCA_EPISTEMICA.md` |
| `matriz_conformidade.py` | esqueleto **norma × evidência × gap** (`PENDENTE`); gera `../indices/MATRIZ_CONFORMIDADE.md` |
| `test_*.py` | testes de coerência (revisão, passos futuros, …) |

Suite completa: **37 testes** (`python3 -m unittest discover codigo -p 'test_*.py'`).

A varredura agora inclui **métricas** por repo (`metricas`): `loc_codigo`, `kb_codigo/prosa/dados`,
`arquivos_vendored`, `original_ratio` — no `../indices/MANIFESTO_INTEGRIDADE.yaml`.

O manifesto distingue **evidência em código vs em prosa** (`evidencia_origem` por conceito):
`codigo` = implementado (fonte), `prosa` = discutido (`.md`), `codigo+prosa` = ambos.

## Rodar

```bash
python3 codigo/ficha_de_entrada.py           # relatório (nós, marcas, coordenada Ω)
python3 codigo/ficha_de_entrada.py --json     # JSON canônico e determinista
python3 -m unittest codigo/test_ficha_de_entrada -v
```

Estado verificado (2026-07-05): **28 fichas coerentes, 0 problemas; 11/11 testes OK;
JSON idêntico entre execuções** (determinismo = invariante C01).

## O que o código garante (coerência, não enfeite)

- **Vocabulário fechado**: só entram conceitos `C01–C17`, camadas `L0–L5`, substrato
  `Lb0–Lb5`, grupamentos `NG1–NG7`, marcas `FATO/HIPOTESE/SIMBOLICO/LACUNA`.
- **Honestidade obrigatória**: toda `LACUNA` exige `proxima_acao` (I4); marca fora do
  conjunto é erro; `notacao` mal formada é erro.
- **Primeira linha**: `primeira_linha_ok` conferido em toda ficha.
- **Coordenada Ω reprodutível**: `omega_coord()` usa `blake2b` (mesma linhagem de hashing
  do acervo) → raio (nó-grupo) + θ (digest) + z (camada) + φ (coerência). Mesma ficha →
  mesma coordenada, sempre.

## Como estender (você preenche o campo, que é maior)

Adicione uma `Ficha` em `EXEMPLOS` (ou construa em runtime) e rode o validador. Para
mapear "tudo em tudo por tudo", preencha `substrato` (Lb0–Lb5), `camada_L`, `conceitos`,
`no_grupo`, `relacoes` e `marca`. O código recusa incoerência antes de entrar no mapa.
