# RAFAELIA — Matriz Federada de Referências V1

Estado: `CANONICAL / APPEND_ONLY_REFERENCES / CLAIM_ALLOWED=false`

## Entrada rápida

| Necessidade | Autoridade inicial | Próxima superfície |
|---|---|---|
| Navegação e ontologia | `Mapa` | Google Drive / repositório produtor |
| Automação e diagnóstico | `RafGitTools` | repositório-alvo / receipt |
| Semântica, compilação e evidência | `RafPolimata` | Termux ou Vectras |
| Runtime Android/terminal | `termux-app-rafacodephi` | receipt físico |
| VM e isolamento | `Vectras-VM-Android` | logs, artifacts e rollback |
| Ciência e falsificabilidade | `relativity-living-light` | datasets / papers / replicação |
| Publicação | `papers` | revisão independente |
| Custódia e memória editorial | Google Drive | índice do `Mapa` |
| Core/FCEA | memória não ordinal no Drive | contrato, fonte e gate específicos |

## Invariante

```text
referência ≠ autoridade ≠ dependência ≠ execução ≠ evidência ≠ claim
```

## Matriz navegável

```text
Google Drive (custódia/memória)
        ↕ pointers + revisões
Mapa (ontologia/índice)
        ├── RafGitTools (controle/automação)
        ├── RafPolimata (semântica/evidência)
        │       ├── termux-app-rafacodephi (runtime terminal)
        │       └── Vectras-VM-Android (runtime VM)
        ├── RLL (pesquisa e falsificabilidade)
        ├── papers (publicação)
        └── Core/FCEA (memória de pesquisa)
```

## Contextos de leitura

### Humano
Começar no `Mapa`, localizar a autoridade e abrir a fonte original. Não assumir que o índice contém o payload completo.

### IA
Selecionar a rota por `authority_role`. Antes de responder como fato, exigir `evidence_state`, `receipt_locator` e limite epistemológico.

### Engenharia
Usar a sequência `fonte → hash → build → artifact → handoff → quarantine → runtime → receipt → decisão`.

### Pesquisa
Usar `hipótese → dataset → método → falsificador → incerteza → resultado → replicação → publicação`.

### Auditoria
Comparar IDs, revisões, commits, hashes, receipts, autoria, licença, ambiente e ações não executadas.

## Artefatos machine-readable

- Schema: `schemas/federated-reference-matrix.v1.schema.json`
- Matriz: `data/control-plane/federated-reference-matrix.v1.json`
- Validador: `tools/validate_federated_reference_matrix.py`
- Testes: `tests/test_federated_reference_matrix.py`

## Gate local

```sh
python3 tools/validate_federated_reference_matrix.py \
  data/control-plane/federated-reference-matrix.v1.json
python3 -m unittest tests.test_federated_reference_matrix
```

## Limites

A matriz não prova disponibilidade, integração, runtime, conformidade, desempenho ou replicação. Relações sem receipt permanecem `HIPÓTESE`, `MODELO_ANALÓGICO` ou `TOKEN_VAZIO`.
