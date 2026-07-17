# Mapa Biblioteconômico — Codec Semântico-Parabólico

**Operation ID:** `PSC-FEDERATION-20260716-001`

## 1. Regra de catalogação

O ecossistema não recebe cópias indiferenciadas do mesmo texto. Cada repositório mantém somente o artefato que pertence ao seu domínio e aponta para as demais autoridades.

```text
obra original -> fonte canônica -> adaptadores de domínio -> evidência local
```

## 2. Catálogo de autoridade

| Repositório | Classe | Responsabilidade | Não deve declarar |
|---|---|---|---|
| `Rafaelia_Core` | protocolo | token, estado, sete direções e fronteiras | benchmark não executado |
| `ZIPRAF_OMEGA_FULL` | runtime experimental | encode/decode, hash, corrupção e tamanho | equivalência humana automática |
| `ChipQuantum` | laboratório | ambiguidade, vetores, geometria e métricas | universalidade física |
| `Matem-tica-` | formal | definições, injetividade, provas e contraexemplos | prova por teste finito |
| `papers` | publicação | síntese técnica derivada | fonte normativa independente |
| `RafPolimata` | governança | routing, claim gates, rollback | preencher lacunas |
| `Mapa` | KOS | catálogo, proveniência e relações | validar ciência local |
| `CientiEspiritual` | didática | parábolas e tradições humanas | diagnóstico ou efeito físico |
| `Cosmos` | adaptador | relações multiescala e linguagem | evidência cosmológica nova |
| `Eletron-efeitos-qu-ntico` | adaptador | limites entre representação e experimento | efeito quântico por semelhança |
| `relativity-living-light` | boundary | `NOT_EVIDENCE_FOR` e claims científicos | promoção cosmológica automática |

## 3. Relações

```text
Rafaelia_Core DEFINES_PROTOCOL_FOR ZIPRAF_OMEGA_FULL
ZIPRAF_OMEGA_FULL IMPLEMENTS_REFERENCE_CODEC
ChipQuantum MEASURES_PROPERTIES_OF REFERENCE_CODEC
Matem-tica- FORMALIZES_CONDITIONS_OF REFERENCE_CODEC
papers SUMMARIZES VERIFIED_AND_GATED_RESULTS
RafPolimata ROUTES_CLAIMS_TO OWNER_REPOSITORY
Mapa CATALOGS ALL_RELATIONS
CientiEspiritual PROVIDES_DIDACTIC_PARABLES
Cosmos ADAPTS_WITHOUT_PHYSICAL_PROMOTION
Eletron-efeitos-qu-ntico REQUIRES_DOMAIN_EVIDENCE
RLL MARKS_NOT_EVIDENCE_FOR_COSMOLOGY
```

## 4. Invariantes de segunda ordem

As relações abaixo devem sobreviver à mudança de domínio:

1. sinal fraco pode ter alta relevância;
2. ausência de evidência não prova ausência do fenômeno;
3. contradição deve ser registrada antes de ser resolvida;
4. latência pode acumular eventos reversíveis em dano irreversível;
5. nenhum observador contém sozinho todo o sistema;
6. contexto compartilhado é requisito para decodificação;
7. `TOKEN_VAZIO` deve gerar nova observação, não preenchimento.

Esses itens começam como princípios metodológicos. Sua validade empírica precisa ser testada em cada domínio.

## 5. Estados de cobertura

```text
IMPLEMENTED_IN_BRANCH
DOCUMENTED
TESTED_LOCAL
CI_ARTIFACT_BOUND
INDEPENDENTLY_REPRODUCED
TOKEN_VAZIO
BLOCKED
```

Nenhum estado posterior pode ser inferido apenas pelo tempo ou pelo tamanho da documentação.

## 6. Nomes citados sem correspondência confirmada

- `BlackXM`: `TOKEN_VAZIO` — nenhum repositório acessível com esse nome foi localizado.
- `Caridário/Calendário`: `TOKEN_VAZIO` — nome exato não localizado; não foi associado por aproximação.
- `RML`: interpretado somente como possível referência ao RLL; a ponte explícita deve usar o nome completo do repositório.

## 7. Próxima varredura

O catálogo deve ser atualizado por delta:

```text
novo commit -> nova relação -> mudança de estado -> evidência -> próximo gate
```

Não recontar toda a obra como se cada revisão começasse do zero.
