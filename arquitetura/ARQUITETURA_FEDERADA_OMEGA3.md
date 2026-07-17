# Arquitetura Federada Ω³

## Estado

`DRAFT_AUDITABLE / CLAIM_BLOCKED / NON_DESTRUCTIVE`

## Finalidade

Organizar o ecossistema RAFAELIA/Ω³ como uma federação de repositórios com responsabilidades explícitas, sem transformar proximidade semântica em integração técnica ou prova científica.

A invariante operacional é:

```text
origem -> estado -> transformação -> evidência -> registro -> reentrada
```

## Planos de responsabilidade

| Plano | Autoridade primária | Responsabilidade | Não pode promover sozinho |
|---|---|---|---|
| Controle e catálogo | `rafaelmeloreisnovo/Mapa` | inventário, contratos, relações e auditoria cross-repo | verdade científica ou execução real |
| Memória e custódia | `rafaelmeloreisnovo/MemRafcode` | origem, digest, estado, rota e reentrada | interpretação como fato |
| Formulação | `rafaelmeloreisnovo/papers` | hipóteses, modelos, experimentos e drafts | validação científica final |
| Relações transdisciplinares | `rafaelmeloreisnovo/Cosmos` | matriz relacional, lacunas e percursos | causalidade por semelhança |
| Validação RLL | `rafaelmeloreisnovo/relativity-living-light` | claims, dados, baselines, falsificadores e artefatos RLL | confirmação física universal |
| Inferência e recuperação | `rafaelmeloreisnovo/llamaRafaelia` | busca, memória contextual, classificação e explicação | reescrever o estado científico do repositório produtor |
| Runtime móvel | `rafaelmeloreisnovo/termux-app-rafacodephi` | build, ABI, JNI, execução e evidência real de dispositivo | declarar backend ou integração não executada |
| Núcleo determinístico | `rafaelmeloreisnovo/Rafaelia_Core` | primitivas estáveis, contratos e benchmarks | absorver todo experimento como produção |
| Laboratório low-level | `rafaelmeloreisnovo/ChipQuantum` | C/ASM, geometria, cripto, compilador e experimentos | declarar segurança sem testes próprios |
| Didática | `rafaelmeloreisnovo/CientiEspiritual` | parábolas e tradução humana | usar narrativa como mecanismo físico |

## Fluxo federado

```text
corpus/memória
  -> formulação
  -> relação entre domínios
  -> teste no repositório proprietário
  -> artefato + checksum + estado epistemológico
  -> registro central no Mapa
  -> consumo por IA/runtime/didática
  -> nova observação
```

## Regra de autoridade

1. Cada domínio de claim deve ter um único `canonical_owner`.
2. Consumidores referenciam o export do proprietário; não copiam a conclusão como verdade própria.
3. Toda referência cross-repo deve registrar repositório, caminho, commit ou tag, digest quando disponível e estado epistemológico.
4. Divergência entre produtor e consumidor resulta em `STALE_CONSUMER` ou `CONTRADICTION`, nunca em escolha silenciosa.
5. Ausência de evidência resulta em `TOKEN_VAZIO`.

## Vocabulário mínimo

```text
VERIFIED             evidência localizada no domínio limitado declarado
VERIFIED_LIMITED     comportamento estreito verificado; integração total não provada
DECLARED_BY_AUTHOR   declaração preservada sem prova independente
HYPOTHESIS           relação ou mecanismo testável ainda não executado
TOKEN_VAZIO          evidência necessária não localizada
CONTRADICTION        evidência atual contradiz a alegação
STALE_CONSUMER       consumidor mantém estado anterior ao produtor
CLAIM_BLOCKED        promoção impedida pelo contrato
```

## Critério de integração real

Uma relação só passa de mapa para integração quando contém:

```text
owner repo
source path
input schema
output schema
version pin
reproduction command
result artifact
checksum
failure mode
rollback
claim boundary
```

## Limite

Este documento define governança arquitetural. Ele não prova que todos os repositórios estão integrados, que seus componentes estão em produção ou que hipóteses científicas foram confirmadas.
