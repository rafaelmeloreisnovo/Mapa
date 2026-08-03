# RAFAELIA — F_GAP / F_NEXT — MAPA EVOLUTIVO AUTOCOERENTE

**ID:** `FGAP-FNEXT-AUTOCOHERENCE-20260803T1048-0300`  
**Estado:** `CANONICAL_DRAFT / APPEND_ONLY / claim_allowed=false / automatic_merge=false`  
**Ciclo observado:** `2026-08-03T10:48:00-03:00`  
**Base GitHub:** `rafaelmeloreisnovo/Mapa@6af36865094947b37f38ebbc6a6b8283e7fc2b26`  
**Espelho editorial Drive:** `19EZxirK63AsX6hssvLjkDvWBfx7oboUED2quwBXoQvc`

## 1. Invariante

```text
fonte
→ identidade
→ índice
→ evidência
→ falsificador
→ decisão
→ receipt
→ memória longitudinal
```

Ausência de evidência não vira zero, `PASS` ou conclusão. Vira `TOKEN_VAZIO`.
Nenhum conceito novo deve ocultar um gate anterior ainda aberto.

## 2. F_OK observado

- o método Drive ↔ GitHub está consolidado no documento-mestre;
- o mapa IGC já enumera prioridades, perguntas-gate, memória e receipts;
- schemas, validadores stdlib-only, fixtures adversariais e contratos fail-closed existem em várias famílias;
- a memória longitudinal V1.1 já materializa índices, hashes, entidades, observações e arestas;
- custódia Ω7, autoria/proveniência e Invariante Evolutiva Absoluta foram formalizadas;
- as PRs `Mapa#140`, `Mapa#141` e `Mapa#142` foram mescladas e constituem fatos históricos observáveis.

## 3. F_GAP / F_NEXT priorizado

| ID | Prioridade | F_GAP | Evidência/estado | F_NEXT mínimo | Critério de fechamento |
|---|---:|---|---|---|---|
| `P0-01` | P0 | Controle real de promoção | Os corpos de `#140` e `#141` determinavam permanência em draft/revisão humana; ambas foram mescladas em 2026-08-03. `#142` também foi mesclada. | Criar contrato machine-readable `promotion_intent`, required check e ruleset em modo Evaluate. | Teste negativo observado, receipt com run/job/steps e review ligado ao head SHA. |
| `P0-02` | P0 | CI observável no head integrado | Nenhum status check ou workflow run foi recuperado para `6af3686...`. | Disparar gate focal de mapa, JSON/JSONL, links e política de promoção. | Workflow commit-bound com steps observáveis; ausência nunca classificada como PASS. |
| `P0-03` | P0 | Credenciais, backup e superfícies Ω7 | Rotação não evidenciada; backup fonte truncado; isolamento incompleto. | Evidenciar rotação sem valores, substituir backup, calcular hash e emitir evento. | Receipt sanitizado + backup íntegro hash-bound. |
| `P0-04` | P0 | Identidade cross-surface | GitHub raw, export Drive, aliases e representações sem reconciliação integral. | Comparar identidade física e lógica sem confundi-las. | Matriz de aliases e divergências, sem falso `byte_exact`. |
| `P0-05` | P0 | Runtime físico Termux/Android | ARMv7/ARM64, APK instalado, DNS/TLS/repos e recovery ainda incompletos. | Executar o menor gate no commit exato e capturar ambiente, comando, saída, exit code e hashes. | Receipt físico reproduzível; claim permanece bloqueado até replicação. |
| `P0-06` | P0 | Integridade do inventário privado | Hashes integrais, `asset_pointer → Drive file_id → hash` e duplicados candidatos permanecem abertos. | Hashing streaming read-only, deduplicação governada e reconciliação de pointers. | Cobertura declarada, duplicados provados e nenhum corpo privado publicado. |
| `P1-01` | P1 | Reprodução independente | Segundo ambiente independente = `TOKEN_VAZIO`. | Reproduzir o contrato congelado e comparar raízes determinísticas. | Receipt independente, ambiente distinto e comparação registrada. |
| `P1-02` | P1 | Ω7 semântica/causal | 2.401 endereços existem como estrutura; dataset, arestas tipadas e causalidade não estão provados. | Materializar somente arestas com fonte e falsificador. | Similaridade nunca cria identidade automática. |
| `P1-03` | P1 | RLL científico | Bayes real não foi repetido no contrato full-covariance congelado; replicação e piloto ausentes. | Replay Bayes commit-bound → relatório → replicação → decisão fail-closed. | Resultado reproduzido e claim ledger atualizado. |
| `P1-04` | P1 | Privacidade, licenças e autoria retroativa | Cobertura total de repos, fontes, autores e compatibilidade de licenças incompleta. | Varredura por lote e registry append-only; conflitos como `DISPUTED/TOKEN_VAZIO`. | Cobertura e limites declarados + revisão humana. |
| `P1-05` | P1 | Piloto operacional real | Contratos/simuladores existem, mas o circuito E2E ainda não fechou. | Executar caso pequeno, read-only e reversível. | `OperationalRecord → RuntimeJob → ExecutionResult → EvidenceEnvelope → Decision` com receipt. |

## 4. Grafo de dependências

```text
G0 controle de promoção
→ G1 CI observável
→ G2 identidade/custódia
→ G3 runtime físico
→ G4 reprodução independente
→ G5 promoção de claims/publicação
```

Fluxo paralelo de dados privados:

```text
inventário
→ hashing
→ deduplicação
→ Navigator
→ cobertura declarada
```

RLL e Ω7 só promovem claims depois de `G0–G4` nos respectivos contratos.

## 5. Microciclo de excelência operacional

1. observar o estado real, sem inferência;
2. congelar commit, fonte, escopo e falsificador;
3. executar uma única dependência mínima;
4. emitir receipt navegável e append-only;
5. reconciliar GitHub ↔ Drive ↔ índice ↔ memória;
6. classificar `F_OK / F_GAP / F_NEXT`;
7. decidir: promover, bloquear, corrigir ou manter `TOKEN_VAZIO`.

## 6. Menor próximo passo executável

Implementar primeiro `P0-01`: tornar executável o controle de promoção já declarado.
Sem essa barreira, novos mapas podem ser corretos no papel e incoerentes na integração.

## 7. Fronteiras

- este documento não prova CI, runtime físico, reprodução ou conformidade;
- `claim_allowed=false`;
- `automatic_merge=false`;
- nenhuma ausência foi convertida em falha de código ou PASS;
- mudanças futuras devem ser append-only ou correções explicitamente versionadas.

## 8. R3

- **F_OK:** contratos, mapas, receipts locais e memória federada formam uma base real;
- **F_GAP:** a governança declarada ainda não controla integralmente a promoção, e o head observado não possui CI recuperada;
- **F_NEXT:** `promotion gate → CI focal → receipt commit-bound → custódia → Termux → reprodução`.

> A paciência operacional não é espera: é sequência verificável sem saltar dependências.
