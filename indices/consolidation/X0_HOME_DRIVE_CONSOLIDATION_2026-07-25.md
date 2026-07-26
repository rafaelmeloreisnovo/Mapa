# Consolidação operacional `X0` + `home` + Google Drive

**Data:** 2026-07-25  
**Estado:** mitigação inicial executada  
**Regra:** ocorrência de arquivo não equivale a artefato único nem capacidade operacional.

## Quantidade observada

| Fonte | Ocorrências observadas | Escopo |
|---|---:|---|
| `X0` | 8.916 | inventário programático excluindo `.git` e `node_modules` |
| `home` | 1.524 | audit read-only, profundidade máxima 5 e diretórios recriáveis ignorados |
| Soma bruta | 10.440 | contém sobreposição e histórico |
| Total único deduplicado | `TOKEN_VAZIO` | exige manifesto cruzado SHA-256/BLAKE3 |

O índice canônico anterior de 2.258 arquivos era uma seleção federada de integridade, não a totalidade física do acervo.

## Papéis arquiteturais

- `X0`: monorepositório-arca com núcleo, recuperações, versões, logs, APIs, sensores, Android, FCEA, ZIPRAF/ZRF e dependências incorporadas.
- `home`: fotografia operacional Termux com boot, serviços, dotfiles, memória, atalhos, backups e material sensível.
- Google Drive: proveniência histórica, snapshots, relatórios, arquivos grandes e cópias não necessariamente canônicas.
- `Mapa`: control plane que deve registrar autoridade, proveniência, integridade, risco e prova.

## Mitigações aplicadas

### `home`

- `RAFAELIA_MASTER_BOOT.sh` reconstruído a partir da proveniência do Drive;
- remoção de `eval` e geração dinâmica de processos;
- boot único, lock atômico, `umask 077`, estado JSON e ciclo monotônico;
- serviço de índice fail-closed, com timeout, logs e remoto desativado por padrão;
- `.gitignore` ampliado para chaves, tokens, rclone, GitHub, ADB, GnuPG e estados locais;
- preenchimento de `INVENTARIO_COMPLETO.md` e `CONHECIMENTO_CIENTIFICO.md`;
- README corrigido para não alegar documentos vazios de 1,4 MB e 5,3 MB.

### `X0`

- API local alterada de `0.0.0.0` para loopback por padrão;
- autenticação Bearer obrigatória;
- remoção de `shell=True` e `os.system`;
- `/run` substituído por allowlist;
- limites de payload, base64 e saída;
- contrato estático de segurança em teste unitário;
- `.gitignore` ampliado para material sensível.

## Proveniência do Drive

Arquivo histórico localizado:

```text
RAFAELIA_MASTER_BOOT.sh
size: 2782 bytes
sha256: 856334d57a3ca801a69cc78bc7e4b962ee5f4875c05da5b3203d7a4bc79db8e0
```

O conteúdo histórico não foi restaurado literalmente porque continha execução de ação via `eval`, loops sem supervisão e inicialização recursiva.

## Riscos não encerrados

1. segredos já versionados continuam no histórico Git até purge e rotação;
2. deduplicação cruzada completa ainda não foi executada;
3. builds e runtime no Moto E7 Power continuam `TOKEN_VAZIO`;
4. componentes externos dentro de `X0` devem ser separados de autoria RAFAELIA;
5. APIs OCR/voz possuem dependências e fluxo externo ainda não auditados integralmente;
6. o Drive pode conter versões mais novas ou divergentes dos mesmos nomes.

## Próximo gate

Produzir `X0_HOME_DRIVE_MANIFEST.jsonl` com, por objeto:

```text
source, path, size, sha256, blake3, git_commit_or_drive_id,
class, canonical_authority, duplicate_of, sensitive, executable,
build_proof, runtime_proof, epistemic_class, token_vazio_reason
```

Somente depois desse manifesto será possível calcular o total único e promover autoridades canônicas sem apagar história.
