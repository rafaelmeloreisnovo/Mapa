# Rota federada Ω-CUBE-42

A sessão `OMEGA-CUBE42-20260717-001` foi distribuída por autoridade, não replicada
como um mesmo bloco em todos os repositórios:

```text
Matem-tica-  → definição, prova e verificação finita
ChipQuantum  → núcleo C freestanding, KAT e objeto ARMv7
papers       → síntese, ledger de claims e plano de falsificação
Mapa         → ponteiros, estados, limites e próxima ação
```

## Invariante de trabalho

\[
\text{expressão}
\rightarrow
\text{definição}
\rightarrow
\text{implementação}
\rightarrow
\text{teste}
\rightarrow
\text{artefato}
\rightarrow
\text{estado}
\rightarrow
\text{próximo falsificador}.
\]

O arquivo canônico de navegação é:

```text
data/federation/omega-cube42-route-v1.json
```

Ele contém somente ponteiros e resumo seguro. Os corpos privados permanecem em seus
repositórios de autoridade.

## Estado por camada

| Camada | PR | Estado |
|---|---:|---|
| Runtime C no ChipQuantum | #41 | `TESTED_LOCAL_X86_64_AND_ARMV7_OBJECT` |
| Formalização no Matem-tica- | #3 | `PROVED_PLUS_TESTED_FINITE` |
| Research note no papers | #9 | `DRAFT_DEFENSAVEL` |
| Navegação no Mapa | este PR | `NAVIGATION_ONLY` |

## Resultado preservado

```text
KAT host:
  epoch=96
  selected=37
  sigma=732
  delta=918
  crc32c=8A006829

Verificação formal finita:
  candidates=42
  parent_edges_checked=41748
  roots_per_candidate=6
  canonical_sha256=53cd54004a82dcdcf2b20cdc3d9776cdcb613de3df2a071d96971c3d75ce44a5
```

## Fronteira

```text
logical determinism != physical zero jitter
ARM object != Android execution
procedural candidate != proven dynamic attractor
finite verification != universal physical law
map pointer != copied private payload
```

## Ordem operacional

1. revisar prova e verificador no `Matem-tica- #3`;
2. revisar o core e o gate CI no `ChipQuantum #41`;
3. executar o KAT no aparelho ARM32 e registrar o recibo;
4. atualizar o ledger no `papers #9` com o resultado do alvo;
5. substituir `TOKEN_VAZIO` no Mapa somente após evidência vinculada a commit e hash;
6. executar ablação 36/42/48/64 antes de afirmar vantagem da cardinalidade 42.

## Safe state

Falha de qualquer nó não promove o seguinte:

```text
formal falha   → runtime claim bloqueado
runtime falha  → paper preserva TOKEN_VAZIO
paper diverge  → fontes formais/runtime continuam canônicas
mapa diverge   → remover overlay sem alterar as fontes
```

\[
R_3=\langle
F_{ok}:\text{rota privada auditável criada},
F_{gap}:\text{alvo e comparação ainda vazios},
F_{next}:\text{recibo ARM32 e ablação de cardinalidade}
\rangle.
\]
