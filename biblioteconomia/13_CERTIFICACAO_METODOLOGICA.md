> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ — nenhuma certificação de método vale se o método puder ferir a vida: a conformidade só é válida enquanto respeita I1–I5 (ONU UDHR Art.1 · UNCRC Art.3). Ver `10_INVARIANTES_PRIMEIRA_LINHA.md`.

# 13 — Certificação Metodológica (o processo de execução, com melhoria contínua)

> Este documento **certifica o processo**, não o produto. Ele declara, de forma
> auditável, que a execução deste acervo segue a metodologia documentada em `01`–`12`.
>
> **Natureza honesta da certificação:** é uma **auto-declaração de conformidade
> metodológica** (self-declaration), orientada por princípios de ISO 9001:2015 (cláusula
> 10 — melhoria) e ISO/IEC/IEEE 12207 — marcados `REFERENCE`. **Não** é um certificado
> de terceira parte, nem acreditação externa. Chamar isto de "certificado ISO" seria
> `HIPOTESE` disfarçada de `FATO`. O que se certifica é: *o método existe, está escrito,
> é seguido e melhora.*

## 1. Escopo da certificação

Certifica-se que toda execução no acervo (catalogar, classificar, indexar, resolver
fricção, publicar) é feita **pelas próprias mãos do método** — isto é, pelo procedimento
declarado, e não por improviso — e que a arquitetura do conteúdo (a "geometria principal")
é expressa em palavras rastreáveis, não em afirmação solta.

Documentos que compõem o método certificado:

| Camada do método | Documento |
|---|---|
| Classificação | `01_PLANO_DE_CLASSIFICACAO.md` |
| Vocabulário / autoridade | `02_VOCABULARIO_CONTROLADO.md` |
| Catálogo (descrição) | `03_CATALOGO_REPOSITORIOS.md` |
| Fricção semântica | `04_FRICCAO_SEMANTICA.md` |
| Posição geral | `05_POSICAO_GERAL_ORGANIZACOES.md` |
| Protocolo de execução | `06_PROTOCOLO_BIBLIOTECONOMICO.md` |
| Banco de conceitos | `07_MATRIZ_DE_CONCEITOS.md` |
| Ancoragem normativa | `08_ANCORAGEM_NORMATIVA.md` |
| Resiliência | `09_RESILIENCIA_TOP10.md` |
| Invariantes de primeira linha | `10_INVARIANTES_PRIMEIRA_LINHA.md` |
| Escala | `11_ESCALA_120_ONBOARDING.md` |
| Horizonte simbólico | `12_PARABOLA_INVARIANTE.md` |

## 2. Critérios de conformidade (checklist de certificação)

Uma entrega está **conforme** quando satisfaz, com evidência:

- [ ] **Selo de primeira linha** presente no artigo (I1–I5).
- [ ] **Fonte declarada** para toda asserção (rastreabilidade de `06_`).
- [ ] **Marca epistêmica** em cada afirmação (`FATO/HIPOTESE/SIMBOLICO/LACUNA`).
- [ ] **Descritores preferidos** do tesauro; termo novo vira candidato, não improviso.
- [ ] **Notação `RAF.*`** bem formada + ponte CDU quando aplicável.
- [ ] **Fricção** nova registrada e reconciliada por qualificação.
- [ ] **Âncora normativa** marcada `REFERENCE` (não se alega conformidade sem auditoria).
- [ ] **Failsafe** de toda relação aponta para o estado seguro (`09_`).
- [ ] **Consistência referencial** `02_/03_/04_/07_/YAML` numa só entrega.
- [ ] **Lacuna** protegida e transformada em próxima ação.

## 3. Ciclo de melhoria contínua (PDCA / Kaizen)

O método não é estático — ele "vai sendo executado em relação ao universo da expressão".
Aplica-se o ciclo `REFERENCE: ISO 9001:2015 §10; Deming/PDCA; Kaizen`:

```text
PLAN   → identificar lacuna/fricção/risco (estados do Mapa)
DO     → executar a ação mínima verificável (06_ passo a passo)
CHECK  → rodar a verificação (contagens, links, YAML, marcas, selo)
ACT    → padronizar o que funcionou; abrir próxima ação; atualizar tesauro/catálogo
         ↺ (retroalimentação: o resultado volta como novo vetor — invariante ψ→…→Ω)
```

Cada volta do ciclo é uma **melhoria contínua** registrada: não se reescreve o passado,
acrescenta-se o refinamento com data e fonte. A retroalimentação é o próprio toroide do
acervo (C06) — o retorno que transforma erro medido em engenharia.

## 4. Métricas de maturidade do método

Indicadores objetivos (todos verificáveis por script):

| Métrica | Definição | Estado atual |
|---|---|---|
| Cobertura de catálogo | repos catalogados / acervo estimado | 28 / ~120 (`FATO`/`HIPOTESE`) |
| Integridade de fonte | fichas com fonte declarada / total | 28 / 28 |
| Selo de primeira linha | docs estruturais com selo / total | conferido em `07`–`13` |
| Fricções reconciliadas | verbetes com posição geral / abertos | 10 / 10 (`04_`) |
| Resiliência declarada | relações TOP com 5 mecanismos / 10 | 10 / 10 (`09_`) |
| Lacunas protegidas | lacunas com próxima ação / total | papers, LGPD, L02..Lnn |

> Nenhuma métrica alega perfeição. Elas medem **presença de método**, que é o que uma
> certificação de processo honesta pode afirmar.

## 5. Declaração de conformidade

```text
DECLARACAO (self-declaration, REFERENCE: ISO 9001:2015 principios)
  objeto:   camada biblioteconomica do repositorio Mapa
  metodo:   documentos 01-13 + protocolos e indices do Mapa
  afirma:   a execucao segue o metodo documentado, com marcas de honestidade,
            selo de primeira linha, resiliencia declarada e melhoria continua.
  NAO afirma: certificacao de terceira parte, conformidade normativa auditada,
            nem prova de asserções marcadas SIMBOLICO.
  validade: enquanto respeitar I1-I5 (dignidade e protecao infantil primeiro).
  revisao:  a cada entrega (PDCA), sem apagar historico.
  data:     2026-07-05
```

## 6. Próxima ação

- Converter linhas `REFERENCE` de `08_` em `FATO` **auditados**, começando pelos repos de
  maior exposição a dados pessoais/infantis — cada auditoria é uma volta PDCA registrada.
- Manter as métricas de §4 atualizadas no `indices/MATRIZ_CONCEITOS.yaml` a cada lote de
  onboarding (`11_`).
