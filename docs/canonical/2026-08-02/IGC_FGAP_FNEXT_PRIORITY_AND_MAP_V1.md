# RAFAELIA — Invariante Geométrica: F_GAP, F_NEXT, Prioridades e Mapa — V1

**ID:** `IGC-PRIORITY-20260802T2250-0300`  
**Data:** `2026-08-02T22:50:00-03:00`  
**Modo:** `APPEND_ONLY / FAIL_CLOSED / NON_DESTRUCTIVE`  
**Estado:** `PRIORITY_DELTA_MATERIALIZED`  
**Claim:** `claim_allowed=false`

## 1. Decisão operacional

O contrato geométrico existente permanece a autoridade:

```text
objeto
→ representação
→ família de transformações
→ propriedade invariante
→ métrica/tolerância
→ evidência
→ falsificador
→ custódia
→ decisão
```

Não será criada uma “invariante universal”. Uma alegação só é admitida quando todos os campos acima estiverem declarados e compatíveis.

```text
visual_similarity != geometric_identity
analogy != physical_equivalence
embedding != return_map != conjecture
local_test != theorem
hash_valid != claim_true
```

## 2. Invariante de governança entre GitHub e Google Drive

A invariante entre superfícies não é identidade de interface. É preservação controlada do núcleo lógico:

```text
IGC_CORE = {
  object_id,
  representation_id,
  transformation_family,
  invariants,
  tolerance,
  evidence_pointers,
  falsifier,
  claim_state,
  claim_allowed,
  lineage
}
```

Para um registro `r` replicado em GitHub e Drive:

```text
surface_invariant(r) = PASS
iff
  canonical_fields(GitHub,r) == canonical_fields(Drive,r)
  AND lineage is declared
  AND differences of formatting are explicit
  AND no private body is promoted without authorization
```

A identidade byte a byte é um gate adicional, não pressuposto:

```text
cross_surface_byte_identity = TOKEN_VAZIO
```

## 3. Mapa geométrico mínimo

```text
[RAW / desenho / fórmula / imagem]
          ↓ G_S: fonte e autoria
[OBJECT DEFINITION]
          ↓ G_D: representação, dimensão, coordenadas, incidência
[TRANSFORMATION FAMILY]
          ↓ G_T: isometria / similaridade / afim / projetiva /
                 homeomorfismo / colagem discreta / simulação
[INVARIANT CONTRACT]
          ↓ G_I: propriedade compatível
[NUMERIC POLICY]
          ↓ tolerância, unidades, precisão, overflow
[TEST + FALSIFIER]
          ↓ G_E + G_F
[EVIDENCE ENVELOPE]
          ↓ commit, hash, ambiente, resultado, limites
[DECISION]
          ↓ VERIFIED_LIMITED / TOKEN_VAZIO / FAIL
[LONGITUDINAL MEMORY]
          ↓ parent_id, delta, supersedes, next_gate
[INDEX / MAP / PAPER]
```

## 4. Matriz urgência × importância

### U1 — Urgente e importante: executar agora

1. **IGC-P0-001 — CI observável:** obter workflow com steps e logs recuperáveis.
2. **IGC-P0-002 — mapa exato de colagem:** marcar vértices, arestas, faces e junção da pirâmide triédrica dupla.
3. **IGC-P0-003 — proveniência Poincaré:** ligar `raw_block_id → FORM-* → objeto geométrico` sem misturar embedding, retorno e conjectura.
4. **IGC-P0-004 — hash entre superfícies:** exportar o documento Drive e comparar núcleo canônico com GitHub.
5. **IGC-P0-005 — claim gate:** bloquear promoção quando objeto, transformação, tolerância, evidência ou falsificador estiver ausente.
6. **IGC-P0-006 — runtime físico:** repetir o validador no Termux ARMv7 e ARM64 com receipt.

### U2 — Importante, não imediatamente urgente: preparar após P0

1. **IGC-P1-001 — reprodução independente:** segundo executor reproduz fixtures e hashes.
2. **IGC-P1-002 — Ω7 geométrico:** materializar arestas semânticas somente após dataset e tipos de relação.
3. **IGC-P1-003 — D7:** validar 2401 endereços, memória, latência e limites sem confundir cardinalidade com significado.
4. **IGC-P1-004 — política numérica:** tolerâncias por domínio, unidades, arredondamento e overflow.
5. **IGC-P1-005 — matriz Drive:** reconciliar a planilha de rastreabilidade com IDs GitHub, Drive e receipts.

### U3 — Urgente, mas operacionalmente delegável/automatizável

1. verificar schemas e JSONL em cada PR;
2. detectar `claim_allowed=true` indevido;
3. detectar claims geométricos sem `transformation_family`;
4. gerar índice curto a partir dos registros canônicos;
5. verificar pointers quebrados e IDs ausentes;
6. produzir relatório de divergência GitHub ↔ Drive.

### U4 — Nem urgente nem importante agora

- ampliar metáforas antes dos gates P0;
- escalar para D7 antes do D3/IGC físico;
- criar novas famílias de transformação sem caso de uso;
- publicar equivalência física a partir de semelhança visual;
- otimizar desempenho antes da correção e da custódia.

## 5. F_GAP consolidado

| ID | Lacuna | Risco | Estado | Gate de fechamento |
|---|---|---|---|---|
| `IGC-GAP-001` | CI sem steps/logs | falha nominal confundida com falha do código | `OPEN_P0` | run observável |
| `IGC-GAP-002` | colagem exata da pirâmide ausente | identidade geométrica fabricada | `OPEN_P0` | mapa V/E/F + orientação |
| `IGC-GAP-003` | coordenadas/mesh da pirâmide ausentes | métrica e topologia não testáveis | `OPEN_P0` | fixture canônico |
| `IGC-GAP-004` | proveniência de fórmulas Poincaré parcial | mistura de objetos distintos | `OPEN_P0` | `raw_block_id → FORM-*` |
| `IGC-GAP-005` | Drive export/hash ausente | espelhos não comparáveis | `OPEN_P0` | export + SHA-256 + normalização |
| `IGC-GAP-006` | runtime físico ausente | host tratado como dispositivo | `OPEN_P0` | receipts ARMv7/ARM64 |
| `IGC-GAP-007` | enforcement global de claims parcial | publicação prematura | `OPEN_P0` | gate fail-closed |
| `IGC-GAP-008` | reprodução independente ausente | resultado não replicado | `OPEN_P1` | segundo executor |
| `IGC-GAP-009` | tolerância/unidades por objeto incompletas | falso PASS numérico | `OPEN_P1` | política por domínio |
| `IGC-GAP-010` | Ω7 sem arestas materializadas | estrutura vazia promovida como rede | `OPEN_P1` | dataset + relações tipadas |
| `IGC-GAP-011` | D7 físico ausente | cardinalidade confundida com execução | `OPEN_P1` | benchmark e receipt |
| `IGC-GAP-012` | matriz Drive não reconciliada com receipts | navegação sem custódia | `OPEN_P1` | IDs + hashes + estado |

## 6. Perguntas obrigatórias antes de qualquer claim geométrico

1. Qual é o **objeto** exato?
2. Qual é sua **representação**: coordenadas, grafo, complexo, mesh, matriz ou imagem?
3. Qual é a **família de transformações** permitida?
4. Qual propriedade é alegada como **invariante**?
5. Essa propriedade é compatível com a família escolhida?
6. A comparação é exata ou numérica? Qual é `epsilon`?
7. Quais são as unidades, precisão e regra de arredondamento?
8. Qual evidência positiva sustenta o registro?
9. Qual caso negativo deve ser rejeitado?
10. O resultado foi observado em sandbox, CI ou dispositivo físico?
11. Qual commit, hash, ambiente e entrada produziram o resultado?
12. O que continua `TOKEN_VAZIO`?
13. Existe autorização para mover o conteúdo entre Drive privado e GitHub?
14. O claim é matemática padrão, modelo, analogia, hipótese, evidência limitada ou resultado físico?
15. Qual é o próximo falsificador mais barato e decisivo?

## 7. Especificações diferentes que não podem ser misturadas

| Camada | Especificação | Não confundir com |
|---|---|---|
| geométrica | objeto, transformação, invariante | semântica autoral |
| topológica | conectividade, Betti, Euler, colagem | distância e ângulo |
| métrica | comprimento, ângulo, área, curvatura | homeomorfismo |
| combinatória | incidência, V/E/F, adjacência | identidade física |
| numérica | tolerância, precisão, amostra | teorema universal |
| semântica | RAPPORT, tipos de relação | geometria física |
| computacional | parser, validador, runtime | prova matemática |
| epistemológica | evidência, falsificador, decisão | pontuação numérica |
| documental | índice, mapa, pointer, hash | conteúdo verdadeiro |
| física | unidades, instrumento, experimento | analogia visual |

## 8. F_NEXT executável

```text
F0  congelar este delta
F1  reconciliar registros geométricos atuais
F2  validar JSONL/schema no checkout exato
F3  produzir mapa V/E/F da pirâmide triédrica dupla
F4  ligar blocos Poincaré às fórmulas tipadas
F5  exportar e hashear documento Drive
F6  executar CI observável
F7  executar Termux ARMv7/ARM64
F8  reproduzir em segundo executor
F9  somente então materializar Ω7/D7 com relações reais
F10 atualizar índice, mapa, memória e claims ledger
```

## 9. Critérios de parada

A execução para e registra `TOKEN_VAZIO` ou `FAIL` quando:

- o objeto não pode ser identificado;
- a transformação não está declarada;
- o invariante é incompatível com a transformação;
- a tolerância numérica é omitida;
- não existe caso negativo;
- a origem ou autorização é desconhecida;
- o runtime alegado não corresponde ao ambiente observado;
- Drive e GitHub divergem sem `derived_from` ou versão explícita.

## 10. Memória longitudinal

Este delta deriva de:

```text
IGC-CR-20260802-V1
→ PR #128 / contrato e validador
→ PR #129 / reprodução local
→ PR #130 / amplificador, 42 F_GAP e memória lateral
→ PR #131 / Ω7 Nexus
→ PR #132 / auditoria Poincaré-áudio-eletromagnetismo
→ IGC-PRIORITY-20260802T2250-0300
```

Nenhum registro anterior é sobrescrito. Mudança de prioridade gera novo evento.

## R3

**F_ok:** contrato IGC existente, fixtures positivas/negativa, índice inicial, Ω7 e Poincaré delimitados, Drive editorial localizado.  
**F_gap:** CI observável, mapa exato de colagem, proveniência completa, hashes cruzados, Termux, reprodução e relações D7.  
**F_next:** fechar P0 na ordem `claim gate → objeto/colagem → proveniência → hash Drive → CI → Termux`.
