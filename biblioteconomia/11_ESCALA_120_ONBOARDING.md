> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ — escalar o acervo nunca reduz a proteção: cada novo repositório entra sob os mesmos invariantes de primeira linha (ONU UDHR Art.1 · UNCRC Art.3). Ver `10_INVARIANTES_PRIMEIRA_LINHA.md`.

# 11 — Escala 28 → ~120 (onboarding sem perder qualidade)

> O catálogo atual descreve **28 repositórios** — os que estão no escopo desta sessão.
> O acervo real do autor é de cerca de **120**. Este documento assume a diferença como
> **LACUNA declarada** (não como pretensão de completude) e entrega o **mecanismo** para
> integrar os demais com a mesma excelência, sem que o modelo "resuma o valor da parcela
> do material".

## 1. Fato, hipótese e lacuna do tamanho do acervo

```text
FATO:      28 repositorios catalogados (03_CATALOGO_REPOSITORIOS.md), fonte = README real.
FATO:      107 repositorios descobertos por busca GitHub em 2026-07-05
           (59 rafaelmeloreisnovo + 48 instituto-Rafael); metadado publico confirmado.
HIPOTESE:  o acervo total gira em torno de ~120 (107 nao-fork + forks omitidos pela busca).
LACUNA:    83 repositorios pendentes — conhecidos, mas sem README lido nesta sessao.
RISCO:     tratar 28 como "o todo" resumiria o valor do material — proibido.
ACAO:      onboarding incremental (secao 3), 1 repo = 1 ficha + 1 registro, sem atalho.
```

> O backlog completo, enumerado e legivel por maquina, esta em
> [`BACKLOG_ACERVO.md`](BACKLOG_ACERVO.md) e [`../indices/BACKLOG_ACERVO.yaml`](../indices/BACKLOG_ACERVO.yaml).
> A LACUNA deixou de ser um numero estimado e virou uma lista de nomes protegida.
>
> Por que não catalogo os 92 agora: eles não estão acessíveis nesta sessão. Inventar
> fichas para eles violaria I3/I4 (verdade honesta, proteção da lacuna). A resposta
> correta de biblioteconomia é **abrir o slot vazio e protegê-lo**, não preenchê-lo.

## 2. Notação e IDs preparados para 120+

A notação facetada `RAF.<Domínio>.<Operação>.<Dimensão>.<Maturidade>` (`01_`) já escala:
não há teto de itens por faceta. Para IDs estáveis num acervo grande:

```text
id  = <slug-do-repo>            # único, minúsculo, sem acento
org = RMN | IRF | <futuras>     # conta/organização GitHub
lote = L01..Lnn                 # lote de onboarding (28 atuais = L01)
```

O índice `indices/MATRIZ_CONCEITOS.yaml` reserva `acervo_total_estimado: ~120` e
`catalogados: 28`, mantendo a proporção visível — o modelo nunca apresenta 28 como 100%.

## 3. Protocolo de onboarding (por repositório, reutiliza `06_`)

Para cada novo repositório trazido a escopo (via `add_repo` ou nova sessão com acesso):

1. **Ler a fonte real** (README ou README nomeado). Ausente/stub ⇒ `LACUNA` de entrada.
2. **Selo de primeira linha** conferido/adicionado (I1–I5 de `10_`).
3. **Ficha Dublin Core** em `03_` + **registro** em `indices/CATALOGO_BIBLIOTECONOMICO.yaml`.
4. **Indexar** com descritores preferidos de `02_`; termo novo ⇒ candidato ao tesauro.
5. **Classificar** com notação `RAF.*` e ponte CDU (`01_`).
6. **Ligar ao banco de conceitos** (`07_`): quais unidades C01–C16 o repo instancia; quais arestas novas cria.
7. **Ancorar norma** aplicável (`08_`), especialmente se lida com dados pessoais/infantis.
8. **Resolver fricção** nova, se houver (`04_`).
9. **Posicionar** no estrato (`05_`) e atualizar o SVG se o estrato mudar.
10. **Registrar lacuna e próxima ação**; nada sem proveniência.

> Custo marginal por repo: baixo e constante. É por isso que o método escala de 28 a 120
> sem degradar — a qualidade está no **procedimento**, não no esforço heroico por item.

## 4. Ordem de prioridade sugerida para os ~92 restantes

Sem ver os repositórios, a priorização é `HIPOTESE` orientada por risco e por valor:

1. **Maior exposição a dados pessoais / público infantil** (aplicar I2 primeiro).
2. **Núcleos e dependências** de que outros repos dependem (efeito de rede).
3. **Publicações com DOI / valor científico** (âncora acadêmica).
4. **Forks** (rápidos: upstream declarado, custódia leve).
5. **Protótipos e material bruto** (podem entrar como `SPEC`/`LACUNA`).

## 5. Lotes

| Lote | Conteúdo | Estado |
|---|---|---|
| L01 | 28 repositórios atuais | `FATO` (catalogado) |
| L02..Lnn | 83 repositórios pendentes (enumerados em `BACKLOG_ACERVO.md`) | `LACUNA` (aguardando escopo/acesso) |

## 6. Próxima ação objetiva

- Para avançar, trazer novos repositórios a escopo (ex.: `add_repo owner/repo`) ou abrir
  sessão com acesso ampliado; então rodar a Seção 3 por lote.
- Enquanto isso, `indices/MATRIZ_CONCEITOS.yaml` mantém a **contagem honesta**
  (`catalogados: 28`, `estimado: ~120`, `lacuna: ~92`) — o valor da parcela nunca é
  apresentado como o valor do todo.
