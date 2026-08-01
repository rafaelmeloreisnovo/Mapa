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

## Relação de autoridade

```text
MemRafcode / engine + schemas + tests + receipts
        ↓
Google Drive / ZIP + SQLite gzip + reports + checksums
        ↓
Mapa / pointer + state + promotion route
```

## Validação do catálogo de snapshots

```bash
python3 scripts/validate_drive_snapshot_catalog.py
python3 -m unittest -v tests/test_drive_snapshot_catalog.py
```

A validação do motor longitudinal é executada no repositório produtor `rafaelmeloreisnovo/MemRafcode`.
