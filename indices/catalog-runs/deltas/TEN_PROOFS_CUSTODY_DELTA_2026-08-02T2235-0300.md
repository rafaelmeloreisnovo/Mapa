# RAFAELIA — Delta de Custódia `openai/ten-proofs` — 2026-08-02 22:35 BRT

**ID:** `PCR-OPENAI-TEN-PROOFS-94BC0FEB-20260802T2235-0300`  
**Modo:** `AUDIT / APPEND_ONLY / FAIL_CLOSED`  
**Branch:** `audit/ten-proofs-custody-20260802`  
**Base observada:** `Mapa@b32c9a16c7947763c992e19b95bdf068edb66bf2`  
**Fonte externa:** `openai/ten-proofs@94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6`  
**Claim:** `claim_allowed=false`

## Entrelace materializado

```text
external source
  → key blobs
  → source registry delta
  → custody receipt
  → control-plane gate
  → schema
  → local verifier
  → negative/positive tests
  → governance document
  → draft PR
```

## Artefatos

- `docs/governance/PROOF_CUSTODY_AND_TOKEN_VALIDITY_V1.md`
- `data/control-plane/proof-custody-gate.v1.json`
- `schemas/proof-custody-receipt.schema.json`
- `data/receipts/external/openai-ten-proofs.94bc0feb.audit.json`
- `data/sources/source_registry.delta.openai-ten-proofs.20260802T2235-0300.jsonl`
- `tools/verify_proof_custody.py`
- `tests/test_proof_custody.py`

## Classificação do corte

| Camada | Estado |
|---|---|
| Repositório, commit e blobs-chave | `EVIDENCIADO / HASH_BOUND` |
| Manifesto `sorry_count: 0` | `DECLARADO PELO MANIFESTO` |
| Toolchain Lean | `IDENTIFICADA` |
| Build `lake build All` | `TOKEN_VAZIO_NOT_EXECUTED` |
| Comparator | `TOKEN_VAZIO_NOT_EXECUTED` |
| PR/review independente observada | `TOKEN_VAZIO` |
| Required status checks | `TOKEN_VAZIO` |
| Borda protegida de promoção | `TOKEN_VAZIO` |
| `TOKEN_VALIDO` | `false` |

## Decisão de governança

```text
commit aprovado é necessário
commit/merge isolado é insuficiente
self-approval não satisfaz revisão independente
incerteza bloqueante não desaparece por merge
```

## Execução local

```sh
python tools/verify_proof_custody.py \
  data/receipts/external/openai-ten-proofs.94bc0feb.audit.json
python -m unittest tests.test_proof_custody -v
```

## F_GAP

- executar build e Comparator;
- produzir receipt em ambiente independente;
- ligar reviewer ao SHA revisado;
- comprovar required checks e proteção da borda;
- selar digest canônico do receipt após catalogação.

## F_NEXT

- usar este gate em claims matemáticos, papers, datasets e runtimes;
- bloquear promoção quando qualquer predicado obrigatório for falso;
- preservar cada `TOKEN_VAZIO` como nó navegável do grafo de custódia.

## R₃

**F_ok:** cadeia tipada e verificador local materializados.  
**F_gap:** execução e revisão independentes ainda ausentes.  
**F_next:** atravessar gates físicos antes de qualquer promoção epistemológica.
