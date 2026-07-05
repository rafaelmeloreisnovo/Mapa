# 06 — Protocolo Biblioteconômico (boas práticas para o executor)

> A "bagagem" do bibliotecário acadêmico, repassada ao **lógico/execução** como um
> procedimento operável. Amarra-se ao ciclo de excelência já existente em
> `protocolos/PROTOCOLO_EXECUCAO_EXCELENCIA.md` — não o substitui.

## Princípio-mestre

> Organizar é decidir **onde uma obra vive**, **como ela é chamada** e **sob que regime
> de verdade ela fala** — e registrar essas decisões de forma que outro agente (humano
> ou IA) chegue à mesma conclusão. Reprodutibilidade também vale para catalogação.

## Ciclo de catalogação (7 passos)

1. **Coletar a fonte.** Ler o README real do repositório (ou o README nomeado, ex.
   `README_MASTER.md`). Se ausente/stub → registrar `LACUNA` de entrada (passo 7),
   nunca inventar descrição.
2. **Descrever (Dublin Core).** Preencher título, âmbito, tipo, resumo, relacionados —
   só com o que a fonte diz. Fork → declarar o upstream.
3. **Indexar com vocabulário controlado.** Escolher descritores **preferidos** de
   `02_VOCABULARIO_CONTROLADO.md`. Encontrou termo novo? Não improvisar: propor
   inclusão no tesauro (passo 6 do vocabulário).
4. **Classificar (facetas).** Atribuir a notação `RAF.<Domínio>.<Operação>.<Dimensão>.<Maturidade>`
   por `01_PLANO_DE_CLASSIFICACAO.md`. Registrar âmbito (S) em campo.
5. **Marcar o regime de verdade.** Cada asserção recebe `FATO` / `HIPOTESE` / `SIMBOLICO`
   / `LACUNA`. Leitura filosófico-espiritual = `SIMBOLICO` com dignidade, nunca "falso".
6. **Resolver fricção.** Se um descritor colide entre organizações, abrir/atualizar
   verbete em `04_FRICCAO_SEMANTICA.md` com sentidos locais + posição geral qualificada.
7. **Registrar e proteger lacunas.** Toda ausência vira entrada `LACUNA` no modelo de
   `protocolos/TOKEN_VAZIO_LACUNAS.md` — e, quando possível, uma próxima ação objetiva
   (ex.: "criar `README.md` de topo no LGPD apontando para `README_MASTER.md`").

## Controle de autoridade (regras)

- **Um conceito, um descritor preferido.** Variantes entram como `USE →`.
- **Nunca fundir referentes distintos** sob um glifo só (ver Φ, 42, ZIPRAF). Qualificar.
- **Nota de escopo obrigatória** para todo descritor polissêmico.
- Mudou um descritor? Atualizar `02_`, `03_`, `04_` e o YAML **na mesma entrega**
  (consistência referencial).

## Os dois eixos (regra de honestidade aplicada)

| Situação | Ação correta | Erro a evitar |
|---|---|---|
| Afirmação com evidência (arquivo, hash, DOI, medição) | `FATO` | inflar para "prova universal" |
| Alegação de desempenho/conformidade não medida | `HIPOTESE` | tratar como `FATO` |
| Leitura filosófica/espiritual universalista | `SIMBOLICO` | rebaixar a "falso" ou promover a prova |
| Ausência de fonte | `LACUNA` | preencher com invenção |

CientiEspiritual e afins são **par ordenado**: costura visível entre ciência (provável)
e espírito (simbólico). Manter a costura, não dissolver a fronteira.

## Interoperabilidade

- Notação primária = facetada `RAF.*`. A **ponte CDU** (em `01_`) serve para diálogo com
  bibliotecas acadêmicas reais; em contexto formal, a CDU oficial prevalece.
- O índice legível por máquina é `indices/CATALOGO_BIBLIOTECONOMICO.yaml`. Toda alteração
  no catálogo markdown deve refletir no YAML (e vice-versa).

## Critério de excelência (herdado e estendido)

Uma catalogação só está completa quando responde (estende o critério de
`protocolos/PROTOCOLO_EXECUCAO_EXCELENCIA.md`):

- O que é a obra? (descrição)
- De onde veio a informação? (fonte)
- Onde ela vive? (notação/estrato)
- Como ela é chamada? (descritores preferidos)
- Sob que verdade ela fala? (marca epistêmica)
- Com o que colide e como reconciliar? (fricção)
- O que ficou em aberto? (lacuna + próxima ação)

## Manutenção

- Ao **adicionar um repositório**: rodar os 7 passos; +1 ficha em `03_`, +1 registro no YAML,
  atualizar a matriz de `05_` e o SVG se mudar o estrato.
- Ao **renomear/depreciar um descritor**: propagar por `02_/03_/04_/YAML` numa só entrega.
- Ao **encontrar nova fricção**: registrar antes de agir sobre o termo.
- **Data e fonte** sempre declaradas; nada de catalogação sem proveniência.
