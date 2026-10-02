# RAFAELIA — Matriz Federada de Referências V1

Estado: `CANONICAL / APPEND_ONLY_REFERENCES / CLAIM_ALLOWED=false`

## Entrada rápida

| Necessidade | Autoridade inicial | Próxima superfície |
|---|---|---|
| Navegação, ontologia e atlas | `Mapa` | Google Drive / repositório produtor |
| Controle operacional, automação e diagnóstico | `RafGitTools` | repositório-alvo / receipt |
| Semântica, falsificadores e evidência | `RafPolimata` | repositório produtor / runtime |
| Produção de pacotes Termux | `termux-packages` | `termux-app-rafacodephi` |
| Runtime Android/terminal | `termux-app-rafacodephi` | receipt físico |
| VM e isolamento | `Vectras-VM-Android` | logs, artifacts e rollback |
| Ciência e falsificabilidade | `relativity-living-light` | datasets / papers / replicação |
| Publicação | `papers` | revisão independente |
| Custódia e memória editorial | Google Drive `NOVOexport/1NIv_E2NdtdLaKi3dWTwqPVl7B9zIKrRk` | índice do `Mapa` |
| Core/FCEA | memória não ordinal no Drive | contrato, fonte e gate específicos |

## Escopo das autoridades

`Mapa` é o control-plane ontológico do atlas/registry; `RafGitTools` é o control-plane operacional da federação. O Drive guarda a custódia documental; nenhum desses planos substitui a autoridade de implementação do repositório produtor.

```text
SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM
TOKEN_VAZIO != 0
```

## Matriz navegável

```text
Google Drive / NOVOexport (custódia longitudinal)
        ↕ pointers + revisões + μWRITE
Mapa (ontologia / índice / atlas)
        ↔ RafGitTools (controle operacional / gates / routing)
                ↔ RafPolimata (classificação de evidência / falsificadores)
                ↔ termux-packages (produtor package + proveniência)
                        → termux-app-rafacodephi (runtime Android/terminal)
                                ↔ Vectras-VM-Android (runtime VM)
        ├── RLL (pesquisa e falsificabilidade)
        ├── papers (publicação)
        └── Core/FCEA (memória de pesquisa)
```

## Drive atual

- Custódia canônica: `NOVOexport / 1NIv_E2NdtdLaKi3dWTwqPVl7B9zIKrRk`.
- Ledger de federação/orquestração: `1n7ZiUL8gpVr0cZe1NDXCxXdyXK5lgoEk2jk9uHWWQ0o`.
- Locators antigos `1g3eVD3zLMuwk0jevAwVL3wSmxhEMkKsAUPFQh2wEn88` e `1HlBedJvhjj1WO4yQszwcSRRlHY7lhSgt` retornaram `NOT_FOUND` no readback de 2026-10-02 e permanecem apenas como referências históricas.
- O folder duplicado `19zVJ_zTOzTsUq0ax7SQwMb1Y1WckeSXX` recebeu dois receipts durante a reconciliação. Ambos foram movidos para o folder canônico; o duplicado foi renomeado `NOVOexport__SUPERSEDED_DUPLICATE_20261002`, verificado vazio e preservado sem exclusão. O escritor que voltou a selecionar esse ID permanece `TOKEN_VAZIO` caso a recorrência reapareça.

## Contextos de leitura

### Humano

Começar no `Mapa`, localizar a autoridade e abrir a fonte original. Não assumir que o índice contém o payload completo.

### IA

Selecionar a rota por `authority_role`. Antes de responder como fato, exigir `evidence_state`, `receipt_locator` e limite epistemológico.

### Engenharia

Usar a sequência `fonte → hash → package/build → artifact → handoff → quarantine → runtime → receipt → decisão`.

### Pesquisa

Usar `hipótese → dataset → método → falsificador → incerteza → resultado → replicação → publicação`.

### Auditoria

Comparar IDs, revisões, commits, hashes, receipts, autoria, licença, ambiente e ações não executadas.

## Artefatos machine-readable

- Schema: `schemas/federated-reference-matrix.v1.schema.json`
- Matriz: `data/control-plane/federated-reference-matrix.v1.json`
- Validador: `tools/validate_federated_reference_matrix.py`
- Testes: `tests/test_federated_reference_matrix.py`
- Fonte operacional: `rafaelmeloreisnovo/RafGitTools/configs/rafaelia-federation.json`

## Gate local

```sh
python3 tools/validate_federated_reference_matrix.py \
  data/control-plane/federated-reference-matrix.v1.json
python3 -m unittest tests.test_federated_reference_matrix
```

## Limites

A matriz não prova disponibilidade, integração física, guest boot, runtime no dispositivo, conformidade, desempenho ou replicação. Relações sem receipt permanecem `HIPÓTESE`, `MODELO_ANALÓGICO` ou `TOKEN_VAZIO`.
