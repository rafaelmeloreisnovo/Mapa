# Tegmark × Arruda × Artefatos RAFAELIA — Índice de Auditoria 2026-08-04

## Estado

- `event_sha256`: `73e397a57237bf11d3ece9e5cabf850b98165c4721e5acbb34c21dbe16d6447f`
- `predecessor_event_sha256`: `c1916b4116a28651ceeb401e8aa123ae7b1edd4cb9e3a127f846a6220dec31ac`
- `claim_allowed`: `false`
- `append_only`: `true`
- `rollback`: `COMPENSATING_EVENT_ONLY`
- `privacy`: ponteiros públicos/privados separados; ZIPs pesados não copiados para o GitHub.

## Autoridades

| Camada | Autoridade |
|---|---|
| fontes pesadas, ZIPs e relatório completo | Google Drive `04_AUDIT` |
| claims, índices, gates e relações | `rafaelmeloreisnovo/Mapa` |
| ciência cosmológica | repositório RLL, após likelihood e replicação |
| correção do kernel/orquestrador | repositório de implementação de origem, ainda `TOKEN_VAZIO` neste evento |

## Âncora Drive

- Documento: `RAFAELIA — Auditoria Integral Aplicada — Tegmark × Arruda × Artefatos — 2026-08-04`
- ID: `1SpgCN8c3x1Vtv_7VaEwDDU8ZxPxkGAXRWoHnSTfJX_c`
- Pasta: `04_AUDIT` (`1FZ3gnajkNDwUttw5UUVcIti8YENj0fK6`)
- SHA-256 do relatório-fonte: `9a1944660405a9a53d8b7604f0c3101546c8b9e7217d596f214ea6abcab0256f`
- SHA-256 do claim ledger auditado: `49539ede44771a61f8efd3b6819cc1cc364c9faaf201ce7010f18b9fb67b4fc5`

## Decisões materializadas

1. **Kernel:** claim de determinismo refutado na implementação auditada — 20 execuções, 20 hashes/contagens distintos.
2. **Orquestrador:** cobertura executável observada de três entradas; estágio `S2` documentado falha; resultados simulados não são validação empírica.
3. **Voynich protegido:** `PASS_LIMITED_LOCAL` de governança, mantendo corpus real e claims científicos bloqueados.
4. **Tegmark × Arruda:** ponte temática/metodológica; ausência de citação cruzada permanece busca negativa escopada, não prova universal.
5. **T^7:** `TOKEN_VAZIO`; começar por controles `T^1` e `T^2`, homologia persistente e estabilidade.
6. **Cosmologia:** comparação de ponto fixo reproduzida; não equivale a evidência Bayesiana nem ajuste final.

## Artefatos versionados neste delta

- `data/claims/tegmark_arruda_artifact_audit.claims.jsonl`
- `data/control-plane/TEGMARK_ARRUDA_ARTIFACT_AUDIT_EVENT.v1.json`
- `docs/canonical/2026-08-04/TEGMARK_ARRUDA_ARTIFACT_AUDIT_INDEX.md`

## Próximos gates

- corrigir race no índice compartilhado e offsets globais;
- executar gate de determinismo por 100 repetições;
- substituir fixtures simuladas por receipts;
- validar os seis registros contra `paper-claim-ledger.schema.json`;
- testar `T^1 → T^2 → T^7` com controles positivos e negativos;
- encaminhar patches de código somente após localizar o repositório de autoridade de cada fonte.

## R3

- **F_ok:** auditoria, hashes, âncora Drive, claims e predecessor definidos.
- **F_gap:** repositórios de origem dos códigos auditados ainda não foram identificados por identidade de bytes.
- **F_next:** abrir PR controlado no Mapa; depois resolver cada implementação por `source_hash → repo/path/blob`, sem inferência por nome.
