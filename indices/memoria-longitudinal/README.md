# Índice de Memória Longitudinal

Esta pasta contém somente catálogos minimizados e auditáveis de fontes privadas.

## Regras

- nenhum corpo de conversa;
- nenhum perfil de usuário;
- nenhuma mídia;
- nenhum segredo;
- hashes ausentes permanecem `null`;
- snapshots são checkpoints, não fragmentos concatenáveis;
- `claim_allowed=false` para inferências de conteúdo sem revisão.

## Arquivo ativo

- `drive_snapshot_catalog.v1.json`

Validação:

```bash
python3 scripts/validate_drive_snapshot_catalog.py
python3 -m unittest -v tests/test_drive_snapshot_catalog.py
```
