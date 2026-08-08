# Índice de Memória Longitudinal

Esta pasta contém catálogos minimizados, auditáveis e ponteiros federados. O `Mapa` não duplica corpos privados, motores produtores ou bancos pesados.

## Regras

- nenhum corpo de conversa;
- nenhum perfil de usuário;
- nenhuma mídia;
- nenhum segredo;
- hashes ausentes permanecem `null`;
- snapshots são checkpoints, não fragmentos concatenáveis;
- engines permanecem no repositório produtor;
- distribuições pesadas permanecem no Google Drive;
- `claim_allowed=false` para inferências de conteúdo sem revisão.

## Arquivos ativos

| Arquivo | Função |
|---|---|
| `drive_snapshot_catalog.v1.json` | catálogo privado minimizado dos exports e pools de assets |
| `longitudinal_index_v1_1_pointer.json` | ponteiro federado para o motor no `MemRafcode` e a distribuição no Drive |
| `../../docs/canonical/2026-08-02/MEMORIA_LONGITUDINAL_CONTEXTUAL_RECORRENTE_E_INDICE_DE_TRABALHO_V1.md` | ativação contextual, índice W0–W9 e overlays tensoriais V9⊕L8⊕E6⊕K6 |
| `../../indices/canonical/2026-08-08/RAFAELIA_MEMORY_ORDINAL_LONGITUDINAL_URGENT_V2.md` | ponte O⊕L⊕U: ordinalidade, continuidade e fila urgente |
| `../../data/memory/urgent-memory.public.v1.jsonl` | projeção pública sanitizada dos gaps P0/P1 com closure contracts |

## Relação de autoridade

```text
MemRafcode / engine + schemas + tests + receipts
        ↓
Google Drive / ZIP + SQLite gzip + reports + checksums
        ↓
Mapa / pointer + ordinal state + longitudinal state + urgent closure queue + promotion route
```

## Validação do catálogo de snapshots

```bash
python3 scripts/validate_drive_snapshot_catalog.py
python3 -m unittest -v tests/test_drive_snapshot_catalog.py
python3 tools/validate_urgent_memory.py data/memory/urgent-memory.public.v1.jsonl
python3 -m unittest -v tests.test_urgent_memory
```

A validação do motor longitudinal é executada no repositório produtor `rafaelmeloreisnovo/MemRafcode`.
