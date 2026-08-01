# Índice navegável dos microciclos RAFAELIA

## Finalidade

O workflow `RAFAELIA Adaptive Cycle` executa quatro microciclos por hora. Cada
execução produz um receipt imutável como artifact. Esta camada acrescenta um
índice append-only e hash-chained para que os quatro ciclos mais recentes sejam
navegáveis sem conceder permissão de escrita ao workflow.

```text
receipt atual
  + último index artifact da mesma branch
  → validação do receipt
  → validação do índice anterior
  → append de uma única entrada
  → cadeia previous_entry_sha256
  → novo microcycle_index.json/.md
  → novo artifact imutável rafaelia-microcycle-index
```

## Onde navegar

Em cada execução do workflow, o artifact `rafaelia-microcycle-index` contém:

- `microcycle_index.json`: ledger machine-readable com toda a sequência do
  segmento, self-hash e cadeia entre entradas;
- `microcycle_index.md`: tabela humana dos quatro microciclos mais recentes,
  com `cycle_id`, `n mod 42`, fase, decisão, run e SHA-256 do receipt.

O artifact individual `rafaelia-adaptive-cycle-<run_id>` passa a carregar também
uma cópia do índice vigente, mantendo receipt e navegação no mesmo pacote.

## Semântica append-only

Cada entrada contém:

```text
cycle_id
receipt_sha256
run_id + run_url
head_branch + head_sha
previous_entry_sha256
entry_sha256
```

O índice contém:

```text
segment_id
entries[]
latest_four[]
previous_index_sha256
index_sha256
continuity.state
```

Uma entrada existente não é sobrescrita. O mesmo `cycle_id` com o mesmo receipt
é idempotente; o mesmo `cycle_id` com hash diferente bloqueia a execução.
Adulteração do índice ou quebra da cadeia também bloqueia.

## Continuidade

Estados válidos:

- `FOUND_VERIFIED_TRANSPORT`: índice anterior recuperado do artifact mais
  recente da mesma branch;
- `TOKEN_VAZIO_NO_PREVIOUS_INDEX`: primeiro ciclo observável daquela branch,
  iniciando um novo segmento;
- `BLOCKED_PREVIOUS_INDEX_RETRIEVAL`: havia necessidade de recuperar o índice,
  mas API, autorização, transporte ou ZIP falhou; não é permitido reiniciar a
  cadeia silenciosamente.

Artifacts possuem retenção limitada. Logo:

```text
artifact append-only != arquivo permanente
```

Antes da expiração, um checkpoint humano pode ser materializado no catálogo
canônico, sempre por PR revisável e nunca por commit automático do cron.

## Fronteiras

```yaml
permissions:
  contents: read
  actions: read
claim_allowed: false
automatic_mutation: false
automatic_merge: false
```

- cron não é evidência científica;
- CI não é runtime físico Termux;
- hash não é verdade;
- índice não promove claim;
- ausência continua `TOKEN_VAZIO` com próximo passo verificável.
