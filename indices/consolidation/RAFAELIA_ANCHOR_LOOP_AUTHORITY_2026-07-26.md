# RAFAELIA Anchor Mesh — autoridade e indexação transversal

**Data da correção:** 2026-07-26  
**Estado:** `MERGED_MATH_CORE_RUNTIME_HISTORY_MAPA / TOKEN_VAZIO_RUNTIME_DEVICE`

## Correção canônica

Os quatro ciclos não são fases descartáveis de um supervisor único:

```text
PULSAR → SENTINEL → MEMORY → ACTION → PULSAR
```

Eles permanecem íntegros e testemunham-se em anel. `runit` é apenas recuperação hospedada; não é autoridade de estado.

```text
4 ciclos × 2 testemunhos = 8 gates
8 gates + assinatura comum + avanço dos 4 ciclos
→ quinto estado derivado
```

O quinto estado não é daemon, task adicional nem ponto único de falha.

## Autoridades imutáveis

| Plano | Autoridade | Commit | Estado |
|---|---|---|---|
| Fonte histórica | Google Drive — `RAFAELIA_MASTER_BOOT.sh` | SHA-256 `856334d5…db8e0` | `OBSERVED_HASHED` |
| Arqueologia | `rafaelmeloreisnovo/X0` | `089d7140de083201cda21f8828ccd9ae93b391a2` | `MERGED` |
| Matemática | `rafaelmeloreisnovo/papers` | `1e2ce959482659f58aa909b11ada17f621f8d64f` | `MERGED` |
| Núcleo C sem heap | `rafaelmeloreisnovo/RafPolimata` — `M062` | `146c0b549878e95644c2d5523e86e00d86662d1b` | `MERGED / PASS_LOCAL` |
| Runtime hospedado | `rafaelmeloreisnovo/home` | `bb777eac8e94532243cc31dfc989c14a64e89c68` | `MERGED / PASS_LOCAL` |
| Catálogo e gates | `rafaelmeloreisnovo/Mapa` | `34148185afa5d407a77169780392959817335f80` | `CANONICAL_CONTROL_RECORD_MERGED` |
| Execução física | Moto E7 Power / ARM32 / Termux | — | `TOKEN_VAZIO_RUNTIME_DEVICE` |

## Fonte histórica

- nome: `RAFAELIA_MASTER_BOOT.sh`;
- tamanho: 2.782 bytes;
- SHA-256: `856334d57a3ca801a69cc78bc7e4b962ee5f4875c05da5b3203d7a4bc79db8e0`;
- conteúdo: quatro scripts persistentes;
- riscos da versão antiga: `eval`, processos destacados, duplicação possível do pulsar e ausência de contrato explícito de oito gates.

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

O quinto estado:

\[
X_5^{n+1}=\Phi(C_0,C_1,C_2,C_3)
\]

só é promovido quando:

1. `G8 = 1`;
2. as quatro assinaturas são iguais;
3. os quatro contadores avançaram desde o compromisso anterior.

## Ruído antes de falha

Estados operacionais:

- `NOMINAL`;
- `ACCELERATION_OBSERVED`;
- `LATENCY_OR_NOISE`;
- `INPUT_TRANSITION_OR_NOISE`;
- `RESTART_OR_NOISE`;
- `FAULT_CANDIDATE_STALLED`;
- `FAULT_CANDIDATE_ABSENT`;
- `FAULT_CANDIDATE_REGRESSION`.

A promoção para candidato a falha exige persistência em ciclos. Tempo é telemetria; não é autoridade da transição.

## Relação com as 60 formulações

| Grau | Itens | Estrutura |
|---:|---|---|
| 10 | 2, 4, 5 | dinâmica epistêmica, ordem quatro e transporte de memória |
| 9 | 12 | cadeia de oito operadores |
| 8 | 21, 23 | memória 42×4 e quatro fases |
| 6 | 40 | fechamento multiplicativo |
| 4 | 54 | fechamento epistêmico |

A âncora é uma síntese transversal. O inventário permanece com 60 formulações.

## Distinção `M059` / `M062`

- `M059`: scheduler cooperativo com quatro slots; as oito invocações do selftest são `2 tarefas × 4 rodadas`;
- `M062`: quatro órgãos íntegros, oito gates e quinto estado derivado.

## Artefatos mesclados

### `home`

```text
RAFAELIA_ANCHOR_ORGAN.sh                 100755
RAFAELIA_ANCHOR_LOOP.sh                  100755
RAFAELIA_MASTER_BOOT.sh                  100755
.termux/services/rafaelia-pulsar/run     100755
.termux/services/rafaelia-sentinel/run   100755
.termux/services/rafaelia-memory/run     100755
.termux/services/rafaelia-action/run     100755
```

O serviço único `.termux/services/rafaelia-anchor/run` foi removido. Parada normal é recusada; emergência exige `RAFAELIA_EMERGENCY_STOP=1`.

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

### `X0`

```text
docs/architecture/RAFAELIA_ANCHOR_LOOP_HISTORICAL_RECONSTRUCTION.md
```

## Evidência

- shell: quatro serviços, oito gates, ruído antes de falha e não execução de JSON — `PASS_LOCAL`;
- C `M062`, `-Wall -Wextra -Werror -pedantic` — `PASS_LOCAL`;
- GitHub Actions: encerrou antes do checkout e não produziu artefato `always()` — `TOKEN_VAZIO_RUNNER`;
- Android/ARM32 real — `TOKEN_VAZIO_RUNTIME_DEVICE`;
- temporização bare-metal — `TOKEN_VAZIO`;
- energia e estabilidade prolongada — `TOKEN_VAZIO_BENCHMARK`;
- replicação independente — `TOKEN_VAZIO`.

## Gate físico seguinte

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
- estagnação classificada por ciclos;
- reinício isolado sem interromper os outros três;
- CPU, wakeups, memória, bateria e jitter.
