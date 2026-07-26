# RAFAELIA Anchor Mesh — autoridade e indexação transversal

**Data da correção:** 2026-07-26  
**Estado:** `IMPLEMENTED_BRANCHES / TOKEN_VAZIO_RUNTIME_DEVICE`

## Correção canônica

A interpretação anterior reconheceu corretamente que os quatro loops eram intencionais, mas ainda os fundiu em uma instância supervisionada. A autoridade atual é:

```text
PULSAR
→ SENTINEL
→ MEMORY
→ ACTION
→ PULSAR
```

Os quatro são ciclos íntegros e permanentes. A supervisão acontece entre pares. `runit` é mecanismo de recuperação hospedada, não autoridade de estado.

```text
4 ciclos × 2 testemunhos = 8 gates
8 gates + assinatura comum + avanço dos 4 ciclos
→ quinto estado derivado
```

O quinto estado não é um daemon, uma task adicional ou um supervisor central.

## Autoridades

| Plano | Autoridade | Estado |
|---|---|---|
| Fonte histórica | Google Drive — `RAFAELIA_MASTER_BOOT.sh` | `OBSERVED_HASHED` |
| Arqueologia | `rafaelmeloreisnovo/X0` | `CORRECTED_BRANCH` |
| Matemática | `rafaelmeloreisnovo/papers` | `FORMULATED_BRANCH` |
| Núcleo C sem heap | `rafaelmeloreisnovo/RafPolimata` — `M062` | `EXECUTA_PASS_LOCAL_BRANCH` |
| Runtime hospedado | `rafaelmeloreisnovo/home` | `PASS_LOCAL_BRANCH` |
| Catálogo e gates | `rafaelmeloreisnovo/Mapa` | `CANONICAL_CONTROL_RECORD` |
| Execução física | Moto E7 Power / ARM32 / Termux | `TOKEN_VAZIO_RUNTIME_DEVICE` |

## Fonte histórica

- nome: `RAFAELIA_MASTER_BOOT.sh`;
- tamanho: 2.782 bytes;
- SHA-256: `856334d57a3ca801a69cc78bc7e4b962ee5f4875c05da5b3203d7a4bc79db8e0`;
- conteúdo: quatro scripts persistentes;
- riscos observados: `eval`, processos destacados, duplicação possível do pulsar e ausência de contrato explícito de oito gates.

## Quatro órgãos

| Órgão | Gate próprio | Testemunha |
|---|---:|---|
| `PULSAR` | integridade e publicação | `SENTINEL` |
| `SENTINEL` | integridade e publicação | `MEMORY` |
| `MEMORY` | integridade e publicação | `ACTION` |
| `ACTION` | integridade e publicação | `PULSAR` |

Cada órgão mantém PID, contador, assinatura, gate próprio, gate do par e classe de variação.

## Oito gates

\[
G_8=\prod_{i=0}^{3}g_{i,self}g_{i,peer}.
\]

Promoção:

\[
X_5^{n+1}=\Phi(C_0,C_1,C_2,C_3)
\]

somente quando:

1. `G8 = 1`;
2. as quatro assinaturas de entrada são iguais;
3. os quatro contadores avançaram desde o compromisso anterior.

## Ruído não é erro imediato

Estados registrados:

- `NOMINAL`;
- `ACCELERATION_OBSERVED`;
- `LATENCY_OR_NOISE`;
- `INPUT_TRANSITION_OR_NOISE`;
- `RESTART_OR_NOISE`;
- `FAULT_CANDIDATE_STALLED`;
- `FAULT_CANDIDATE_ABSENT`;
- `FAULT_CANDIDATE_REGRESSION`.

O candidato a falha exige persistência em ciclos. O relógio pode ser telemetria, mas não é autoridade do estado.

## Relação com as 60 formulações

A síntese aponta para:

| Grau | Itens | Estrutura |
|---:|---|---|
| 10 | 2, 4, 5 | dinâmica epistêmica, ordem quatro e transporte de memória |
| 9 | 12 | cadeia de oito operadores |
| 8 | 21, 23 | memória 42×4 e quatro fases |
| 6 | 40 | fechamento multiplicativo |
| 4 | 54 | fechamento epistêmico |

A síntese não cria uma 61ª formulação canônica. Ela relaciona formulações existentes.

## Distinção `M059` / `M062`

- `M059`: scheduler cooperativo com quatro slots; as oito invocações do selftest são `2 tarefas × 4 rodadas`;
- `M062`: âncora quaternária, quatro órgãos, oito gates e quinto estado derivado.

## Artefatos operacionais

### `home`

```text
RAFAELIA_ANCHOR_ORGAN.sh
RAFAELIA_ANCHOR_LOOP.sh
RAFAELIA_MASTER_BOOT.sh
.termux/services/rafaelia-pulsar/run
.termux/services/rafaelia-sentinel/run
.termux/services/rafaelia-memory/run
.termux/services/rafaelia-action/run
```

O serviço único `.termux/services/rafaelia-anchor/run` foi removido.

Parada normal é recusada; parada emergencial exige `RAFAELIA_EMERGENCY_STOP=1`.

### `RafPolimata`

```text
RAF_062_quaternary_anchor_eight_gate.c
scripts/test_m062_anchor.sh
```

Núcleo com arrays estáticos, sem heap e selftest C11 estrito.

### `papers`

```text
docs/matematica_autoral/ANCORA_QUATERNARIA_OITO_GATES_QUINTO_ESTADO.md
```

## Evidência

- shell: quatro serviços, oito gates, ruído antes de falha e não execução de JSON — `PASS_LOCAL`;
- C estático `M062` com `-Wall -Wextra -Werror -pedantic` — `PASS_LOCAL`;
- runner remoto — `PENDING`;
- Android/ARM32 real — `TOKEN_VAZIO_RUNTIME_DEVICE`;
- temporização bare-metal — `TOKEN_VAZIO`;
- consumo e estabilidade prolongada — `TOKEN_VAZIO_BENCHMARK`;
- replicação independente — `TOKEN_VAZIO`.

## Gate físico seguinte

No aparelho:

```text
sv up rafaelia-pulsar
sv up rafaelia-sentinel
sv up rafaelia-memory
sv up rafaelia-action
bash ~/RAFAELIA_ANCHOR_LOOP.sh status
```

Verificar:

- quatro PIDs distintos;
- nenhuma quinta task de autoridade;
- oito gates antes do quinto estado;
- divergência transitória sem falso defeito;
- detecção de estagnação por ciclos;
- reinício isolado sem interromper os outros três;
- uso de CPU, wakeups, memória, bateria e jitter.
