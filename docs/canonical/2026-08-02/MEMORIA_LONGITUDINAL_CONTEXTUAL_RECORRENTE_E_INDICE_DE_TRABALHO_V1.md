# Memória Longitudinal, Contextual, Recorrente e Índice de Trabalho — V1

**Evento:** `MEM-RAFAELIA-20260802-LCR-WORK-INDEX-001`  
**Data:** `2026-08-02 04:04 BRT`  
**Modo:** `APPEND_ONLY / POINTER_FIRST / NON_DESTRUCTIVE`  
**Estado:** `CANONICAL_DRAFT_MATERIALIZED`  
**Claim:** `claim_allowed=false`

## 1. Intenção autoral preservada

O autor solicitou ativação permanente de:

- memória longitudinal;
- memória contextual do projeto;
- recorrência operacional;
- índice de trabalho navegável;
- instruções personalizadas e instruções do projeto como contexto governante;
- consulta coerente ao Google Drive, GitHub e Mapa;
- expansão da tokenização por novas camadas e tensores.

A palavra “recorrente” é normalizada como **reconsulta dos ponteiros canônicos quando o projeto for retomado**, não como processo autônomo em segundo plano.

## 2. Autoridades e fronteiras

```text
Memória persistente do assistente
  → preferência operacional e continuidade entre conversas

Google Drive
  → corpos editoriais, distribuições pesadas, snapshots e revisões

MemRafcode
  → engine, schemas, testes, políticas e receipts da memória longitudinal

Mapa
  → ponteiros, ontologia, estados, dependências, índices e rota de promoção

GitHub produtores
  → código, testes, workflows, artefatos e receipts reprodutíveis
```

Regras:

```text
contexto != evidência
lembrança != execução
hash != verdade semântica
metáfora != claim factual
implementação != runtime físico
recorrência contextual != tarefa em segundo plano
```

## 3. Estado observado da memória longitudinal V1.1

Referência ativa:

```text
indices/memoria-longitudinal/longitudinal_index_v1_1_pointer.json
```

Métricas observadas no ponteiro federado:

```yaml
sources: 15
entities: 51581
observations: 52271
edges: 44611
local_compile: PASS
local_unit_tests: PASS
sqlite_integrity: PASS
drive_mirror: PASS
remote_ci: PASS
independent_reproduction: TOKEN_VAZIO
physical_termux_execution: TOKEN_VAZIO
full_cold_expansion: TOKEN_VAZIO
```

O Mapa permanece minimizado: não duplica corpos privados, mídias, segredos, engine produtora ou banco pesado.

## 4. Índice de trabalho ativo — W0 a W9

O índice acompanha as lanes canônicas sem confundir etapa com evidência:

| ID | Lane | Pergunta de controle | Saída mínima |
|---|---|---|---|
| `W0` | governança | qual regra e autoridade valem? | política, estado, rollback |
| `W1` | intake/fontes | de onde veio e há autorização? | source pointer, custódia |
| `W2` | normalização | quais tokens e âncoras existem? | tokens determinísticos |
| `W3` | modelagem semântica | quais relações e hipóteses surgem? | tensor, grafo, latentes |
| `W4` | validação | o que falsifica ou contradiz? | testes, falsificadores |
| `W5` | evidências | qual artefato sustenta o estado? | hashes, receipt, ledger |
| `W6` | integração | quais dependências e rotas existem? | dependency graph, contratos |
| `W7` | segurança/conformidade | o que não pode atravessar a fronteira? | privacy class, guards |
| `W8` | observabilidade/release | o que rodou e em qual ambiente? | métricas, run IDs, decisão |
| `W9` | memória/arquivo | como preservar sem sobrescrever? | checkpoint append-only |

Estado de cada item:

```text
BACKLOG → ACTIVE → BLOCKED → EVIDENCED → REVIEWED → CANONICAL
```

`TOKEN_VAZIO` pode existir em qualquer estado quando falta requisito obrigatório.

## 5. Tensor semântico existente — V9

O motor já materializado preserva:

\[
V_9=(S,E,F,C,X,P,R,G,H)
\]

```text
S = proveniência da fonte
E = força da evidência
F = falsificabilidade
C = coerência estrutural
X = integridade contextual
P = proveniência cultural
R = reprodutibilidade
G = segurança ética
H = humildade epistemológica
```

Este tensor é governamental. Não altera pesos internos, tokenizer ou treinamento de modelos.

## 6. Novos overlays propostos

Para evitar um tensor monolítico, a expansão usa soma direta de blocos independentes:

\[
\mathcal{T}_{RAFAELIA}=V_9\oplus L_8\oplus E_6\oplus K_6
\]

### 6.1 Overlay longitudinal `L8`

\[
L_8=(T,A,D,M,Δ,R_b,Q,U)
\]

| Eixo | Significado |
|---|---|
| `T` | posição temporal e sequência append-only |
| `A` | autoridade do registro |
| `D` | dependências anteriores e posteriores |
| `M` | temperatura de memória: HOT/WARM/COLD/ARCHIVE |
| `Δ` | delta desde o checkpoint anterior |
| `R_b` | reversibilidade e rota de rollback |
| `Q` | intenção/pergunta-raiz ligada ao bloco |
| `U` | incerteza e classe de TOKEN_VAZIO |

### 6.2 Overlay de execução `E6`

\[
E_6=(L0,L1,L2,L3,L4,L5)
\]

```text
L0 = texto/modelo de conversa
L1 = connector e APIs autorizadas
L2 = container ou runtime efêmero
L3 = CI remota
L4 = Termux/dispositivo físico
L5 = reprodução independente
```

Uma passagem em `L2` não promove automaticamente `L3`, `L4` ou `L5`.

### 6.3 Overlay de custódia `K6`

\[
K_6=(I,H_s,C_s,P_v,V_r,S_g)
\]

```text
I   = identidade do artefato
H_s = hashes e escopo do digest
C_s = cadeia de custódia
P_v = privacidade e autorização
V_r = versão/revisão observada
S_g = assinatura, selo ou ausência explicitada
```

Checksum, hash, assinatura, autoria, execução e verdade permanecem estados distintos.

## 7. Token composto navegável

Cada unidade de trabalho pode ser serializada como:

```text
TOKEN = {
  token_id,
  semantic_anchor,
  V9,
  L8,
  E6,
  K6,
  work_lane: W0..W9,
  epistemic_state,
  source_pointers,
  evidence_pointers,
  falsifiers,
  token_vazio,
  next_gate
}
```

O formato deve ser esparso: eixos não observados ficam ausentes ou `TOKEN_VAZIO`, nunca recebem zero inventado.

## 8. Brindes/camadas auxiliares

Os “brindes” são normalizados como visões derivadas, sem alterar o registro-fonte:

1. **Cartão humano:** resumo curto e estado atual;
2. **Mapa de dependências:** nós, arestas e bloqueios;
3. **Linha temporal:** checkpoints e deltas;
4. **Matriz de falsificadores:** claim × teste × resultado;
5. **Mapa térmico de memória:** HOT/WARM/COLD/ARCHIVE;
6. **Parábola didática:** explicação controlada, marcada como não-evidência;
7. **Receipt mínimo:** identidade, ambiente, hashes, limites e próximo gate.

## 9. Protocolo recorrente de retomada

Ao receber pedido relacionado ao projeto:

```text
1. identificar intenção atual;
2. consultar memória persistente relevante;
3. ler o documento-mestre Drive quando necessário;
4. consultar Mapa e produtores atuais;
5. localizar checkpoint mais recente;
6. calcular delta sem apagar estados anteriores;
7. separar fato, evidência, hipótese, parábola e TOKEN_VAZIO;
8. executar ou registrar o próximo gate verificável;
9. devolver F_ok, F_gap e F_next.
```

## 10. Estado geral no corte

```yaml
memory_persistent_preference: ACTIVE
project_context: ACTIVE_IN_CURRENT_PROJECT
longitudinal_pointer_v1_1: VERIFIED_LIMITED
work_index_w0_w9: MATERIALIZED_IN_THIS_DOCUMENT
semantic_tensor_v9: IMPLEMENTED_DETERMINISTIC
longitudinal_overlay_l8: DESIGN_MATERIALIZED_IMPLEMENTATION_PENDING
execution_overlay_e6: DESIGN_MATERIALIZED_IMPLEMENTATION_PENDING
custody_overlay_k6: DESIGN_MATERIALIZED_IMPLEMENTATION_PENDING
background_process: NOT_CLAIMED
claim_allowed: false
```

## 11. Próximos gates

1. criar schemas JSON para `L8`, `E6`, `K6` e token composto;
2. integrar sem modificar o schema V9 existente;
3. gerar fixtures positivas, negativas e de fronteira;
4. produzir validador fail-closed e receipt;
5. reproduzir a memória longitudinal em segundo dispositivo;
6. executar o runner físico Termux;
7. registrar delta no catálogo incremental.

## R3

- **F_ok:** intenção permanente, índice W0–W9 e expansão tensorial foram materializados sem apagar o V9 existente.
- **F_gap:** overlays ainda não possuem schema, implementação, testes ou reprodução independente.
- **F_next:** implementar primeiro `L8` como schema esparso e ligar cada entrada ao ponteiro longitudinal V1.1.
