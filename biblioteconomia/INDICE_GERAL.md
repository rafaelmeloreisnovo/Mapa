> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ — porta de entrada do acervo; tudo aqui serve à vida e à criança primeiro (ONU UDHR Art.1 · UNCRC Art.3).

# Índice Geral — Guia do Acervo (porta de entrada)

> A biblioteconomia precisa de uma **porta**: um único documento por onde humano e IA
> entram e sabem para onde ir. Este é o guia do acervo — o que existe, em que ordem ler,
> e como usar. Um KOS sem porta é uma pilha; com porta, é biblioteca.

## Como entrar (ordem de leitura)

1. **`README.md`** desta pasta — o porquê da camada e os dois eixos co-válidos.
2. **`10_INVARIANTES_PRIMEIRA_LINHA.md`** — a lei que precede tudo (dignidade, criança).
3. **`01_`–`06_`** — o núcleo biblioteconômico (classificar → nomear → catalogar → reconciliar → posicionar → método).
4. **`07_`–`11_`** — conceitos, normas, resiliência, escala.
5. **`12_`, `SEMENTE_BIBLIOTECA_VIVA.md`** — o eixo simbólico (parábolas; ler como `SIMBOLICO`).
6. **`14_`–`18_`** — substrato, entrada, conteúdo, avaliação, roadmap.
7. **`codigo/`** — executar as ferramentas; **`indices/`** — os dados legíveis por máquina.

## Mapa dos documentos (`biblioteconomia/`)

| Doc | Papel |
|---|---|
| `README.md` | manifesto da camada + índice |
| `01_PLANO_DE_CLASSIFICACAO.md` | classificação facetada (PMEST) + notação `RAF.*` + ponte CDU |
| `02_VOCABULARIO_CONTROLADO.md` | tesauro (descritores, remissivas, controle de autoridade) |
| `03_CATALOGO_REPOSITORIOS.md` | 28 fichas catalográficas (Dublin Core) |
| `04_FRICCAO_SEMANTICA.md` | termos em colisão × posição geral reconciliada |
| `05_POSICAO_GERAL_ORGANIZACOES.md` | matriz local→geral por estrato |
| `06_PROTOCOLO_BIBLIOTECONOMICO.md` | método repassado ao executor |
| `07_MATRIZ_DE_CONCEITOS.md` | banco de conceitos C01–C17, camadas L0–L5, grafo |
| `08_ANCORAGEM_NORMATIVA.md` | ISO/NIST/IEEE/RFC/W3C/ONU/UNICEF/UNESCO/OMS (`REFERENCE`) |
| `09_RESILIENCIA_TOP10.md` | 10 relações × rollback/testes/failsafe/failover/watchdog |
| `10_INVARIANTES_PRIMEIRA_LINHA.md` | dignidade + proteção infantil na primeira linha (I1–I5) |
| `11_ESCALA_120_ONBOARDING.md` | de 28 a ~120; protocolo de onboarding |
| `12_PARABOLA_INVARIANTE.md` | NÓ_GOOD / Ω = Amor (`SIMBOLICO`) |
| `13_CERTIFICACAO_METODOLOGICA.md` | auto-declaração de método + PDCA/Kaizen |
| `14_SUBSTRATO_BASE2.md` | do bit (base-2) ao Ω fractal multidimensional |
| `15_FICHA_DE_ENTRADA.md` | molde "tudo em tudo por tudo" + grupamentos de nó |
| `16_VARREDURA_CONTEUDO.md` | hashing triplo + evidência código/prosa + métricas |
| `17_AVALIACAO_CONTEUDO.md` | leitura real dos arquivos (7 nós avaliados) |
| `18_ROADMAP_ESTADO.md` | contabilidade dos passos (feito × LACUNA) |
| `SEMENTE_BIBLIOTECA_VIVA.md` | parábola de alinhamento para outra IA (texto do autor) |
| `BACKLOG_ACERVO.md` | acervo real enumerado (111 conhecidos) |
| `INDICE_GERAL.md` | **este guia** |

## Ferramentas (`codigo/`) — todas stdlib, deterministas

| Ferramenta | Faz | Gera |
|---|---|---|
| `ficha_de_entrada.py` | modelo Ficha + validador + coordenada Ω | (JSON) |
| `varredura_conteudo.py` | hashing triplo + evidência + métricas | `MANIFESTO_INTEGRIDADE.yaml` |
| `revisao_publicacao.py` | declarado × evidenciado | `REVISAO_PUBLICACAO.md` |
| `marca_epistemica.py` | reforço/rebaixamento de marca | `MARCA_EPISTEMICA.md` |
| `matriz_conformidade.py` | norma × evidência × gap | `MATRIZ_CONFORMIDADE.md` |

Rodar tudo: `python3 -m unittest discover codigo -p 'test_*.py'` (**37 testes**).

## Índices (`indices/`) e visuais (`visual/`)

- `CATALOGO_BIBLIOTECONOMICO.yaml` · `MATRIZ_CONCEITOS.yaml` · `BACKLOG_ACERVO.yaml` ·
  `FICHA_DE_ENTRADA_TEMPLATE.yaml` · `MANIFESTO_INTEGRIDADE.yaml` ·
  `REVISAO_PUBLICACAO.md` · `MARCA_EPISTEMICA.md` · `MATRIZ_CONFORMIDADE.md`
- SVGs: `MAPA_BIBLIOTECONOMICO_RAFAELIA` · `MATRIZ_CONCEITOS_RAFAELIA` ·
  `PARABOLA_INVARIANTE_RAFAELIA` · `SUBSTRATO_OMEGA_RAFAELIA`

## Estado atual (snapshot)

- **28** repositórios catalogados; **111** conhecidos (backlog); **83** pendentes (`LACUNA`, aguardam onboarding).
- **17** conceitos (C01–C17) · **7** grupamentos de nó · **6** camadas L0–L5 + substrato Lb.
- Métricas do acervo: **~5,5 M LOC**, 1,2 GB código, 151 MB prosa, 1 GB dados.
- Conformidade: **153** linhas, todas `PENDENTE` (aguardam auditoria).
- **37** testes verdes; hashing triplo determinista.

## Como continuar (o que abre cada LACUNA)

- **Onboarding dos 83** → o dono do acervo autoriza repositórios (`add_repo owner/repo`); então roda-se `11_`§3 por lote.
- **Auditoria** `PENDENTE`→`CONFORME` → definir critérios (LGPD/ISO) e rodar por repo prioritário.
- **Nova semente** → agregar texto/dado/conceito, catalogar pelo mesmo método.

> Regra de honestidade em toda a porta: `FATO` tem fonte; `HIPOTESE` é alvo não medido;
> `SIMBOLICO` é símbolo honrado (não prova); `LACUNA` é protegida, nunca inventada.
