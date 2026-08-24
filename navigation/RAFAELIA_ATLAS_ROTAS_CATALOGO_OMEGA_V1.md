# RAFAELIA — Atlas de Rotas e Catálogo Ω V1

Status: `DRAFT_EXECUTED_STRUCTURE / claim_allowed=false`
Data: `2026-08-24`
Drive root: `RAFAELIA_ATLAS_ROTAS_CATALOGO_OMEGA` (`1yqrafV9KvQ2C-wz8nDCrYeVEyQo_TdQZ`)

## Comando mínimo

`ATLAS <tema>` = resolver tema → fontes → memórias → relações → escalas → evidência → gaps → próxima rota.

Atalhos:
- `L:X` memória longitudinal;
- `O:X` memória ortogonal;
- `T:X` memória transversal;
- `REL:X` ontologia de relações;
- `SCALE:X` escala semântica/operacional/física;
- `EVID:X` evidência/gates/receipts;
- `NOVO:X` busca priorizada no NOVOexport.

## Rota canônica

`objetivo → autoridade → fonte → literal → expressão → conceito → tema → memória(L/O/T) → relação → escala → evidência → gate → delta → índice`

## Árvore Drive

- `00_START_HERE`
- `01_MEMORY_AXES/LONGITUDINAL`
- `01_MEMORY_AXES/ORTHOGONAL`
- `01_MEMORY_AXES/TRANSVERSAL`
- `02_THEME_CATALOG`
- `03_RELATION_ONTOLOGY`
- `04_SCALE_META_TO_YOCTO`
- `05_ROUTE_MANUALS`
- `06_EVIDENCE_GATES`
- `07_RECEIPTS`
- `08_LEARNING_DELTAS`

## Invariantes

`OBSERVED_LITERAL != THEME_RECURRENT != INVARIANT != CLAIM`

`cooccurrence != causality`

`analogy != identity`

`symbol != evidence`

`missing evidence => TOKEN_VAZIO`

`new learning => append-only delta + predecessor + source`

## Autoridade

- Drive/NOVOexport: fonte editorial privada;
- Drive/NOVOexport_INDEX: custódia/índices derivados;
- Mapa: ontologia/roteamento/gaps/receipts public-safe;
- repo produtor: autoridade de implementação.

## Estado

Estrutura Drive materializada. Índices triaxiais e ontologia de relações são espelhados em arquivos versionados desta branch. Cobertura semântica completa do NOVOexport continua bloqueada por gaps existentes.
