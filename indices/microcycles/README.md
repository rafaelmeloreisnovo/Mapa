# Índice navegável dos microciclos RAFAELIA

## Finalidade

O workflow `RAFAELIA Adaptive Cycle` executa quatro microciclos por hora. Cada
execução produz um receipt imutável como artifact. Esta camada acrescenta um
índice append-only e hash-chained para que os quatro ciclos mais recentes sejam
navegáveis sem conceder permissão de escrita ao workflow.

```text
receipt atual
  + último cache imutável da mesma branch
  → validação do receipt
  → validação do índice anterior
  → append de uma única entrada
  → cadeia previous_entry_sha256
  → novo microcycle_index.json/.md
  → novo cache imutável por run
  → novo artifact navegável rafaelia-microcycle-index
```

## Onde navegar

Em cada execução do workflow, o artifact `rafaelia-microcycle-index` contém:

- `microcycle_index.json`: ledger machine-readable com toda a sequência do
  segmento, self-hash e cadeia entre entradas;
- `microcycle_index.md`: tabela humana dos quatro microciclos mais recentes,
  com `cycle_id`, `n mod 42`, fase, decisão, run e SHA-256 do receipt.

O artifact individual `rafaelia-adaptive-cycle-<run_id>` passa a carregar também
uma cópia do índice vigente, mantendo receipt e navegação no mesmo pacote.

## Transporte de continuidade

A continuidade entre runs usa `actions/cache/restore` e `actions/cache/save`,
fixados no commit da versão 4.2.0. Cada run usa uma chave nova:

```text
rafaelia-microcycle-index-<branch>-<run_id>
```

Caches existentes são imutáveis. O restore por prefixo recupera a geração mais
recente visível à mesma branch; o run atual cria outra geração, nunca altera a
anterior. O artifact continua sendo a superfície humana de navegação.

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

- `FOUND_IMMUTABLE_CACHE`: índice anterior restaurado da geração imutável mais
  recente da mesma branch;
- `TOKEN_VAZIO_NO_PREVIOUS_INDEX`: primeiro ciclo observável daquela branch ou
  cache anterior já indisponível, iniciando um novo segmento explicitamente.

Cache e artifact possuem retenção/evicção limitada. Logo:

```text
cache append-only != arquivo permanente
artifact append-only != arquivo permanente
```

Antes da expiração, um checkpoint humano pode ser materializado no catálogo
canônico, sempre por PR revisável e nunca por commit automático do cron.

## Fronteiras

```yaml
permissions:
  contents: read
claim_allowed: false
automatic_mutation: false
automatic_merge: false
```

- cron não é evidência científica;
- CI não é runtime físico Termux;
- hash não é verdade;
- índice não promove claim;
- ausência continua `TOKEN_VAZIO` com próximo passo verificável.
