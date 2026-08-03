# Índice — IGC F_GAP, F_NEXT, Prioridades e Mapa — V1

**ID:** `IDX-IGC-PRIORITY-20260802T2250-0300`  
**Estado:** `APPEND_ONLY / claim_allowed=false`

## Entrada canônica

- `docs/canonical/2026-08-02/IGC_FGAP_FNEXT_PRIORITY_AND_MAP_V1.md`

## Autoridade anterior

- `docs/canonical/2026-08-02/INVARIANTE_GEOMETRICA_COERENTE_E_COESAO_REAL_V1.md`
- `schemas/geometric-invariant-contract.schema.json`
- `tools/validate_geometric_invariant_contract.py`
- `data/geometry/geometric_invariants.index.jsonl`
- `receipts/geometry/IGC_CR_20260802_RECEIPT_V1.json`

## Registros deste delta

- `data/gaps/igc_priority_fgap.20260802T2250-0300.jsonl` — 12 lacunas priorizadas;
- `data/questions/igc_urgent_questions.20260802T2250-0300.jsonl` — 15 perguntas obrigatórias;
- `data/geometry/geometric_invariants.delta.20260802T2250-0300.jsonl` — 4 registros geométricos adicionais;
- `data/memory/longitudinal_igc_priority.20260802T2250-0300.jsonl` — memória e rotas;
- `data/receipts/igc_priority_cycle.20260802T2250-0300.receipt.json` — receipt federado.

## Mapa rápido

```text
fonte
→ objeto
→ representação
→ transformação
→ invariante
→ tolerância/unidades
→ teste + falsificador
→ evidência
→ decisão
→ memória longitudinal
→ índice/mapa
→ publicação
```

## Prioridade P0

```text
claim gate
→ colagem e representação exatas
→ proveniência Poincaré
→ export/hash Drive
→ CI observável
→ Termux ARMv7/ARM64
```

## Prioridade P1

```text
política numérica
→ reconciliação da matriz Drive
→ reprodução independente
→ arestas Ω7 tipadas
→ D7 físico
```

## Mapas de superfície

| Superfície | Objeto | ID/pointer | Papel |
|---|---|---|---|
| GitHub | contrato IGC | `IGC-CR-20260802-V1` | autoridade operacional |
| GitHub | delta de prioridade | `IGC-PRIORITY-20260802T2250-0300` | F_GAP/F_NEXT atual |
| Google Drive | documento editorial IGC | `1eGLmUTXAgcm4M9hJNCXoB5OLnc9ZSGMqTXvsFJasags` | leitura e reflexão |
| Google Drive | documento-mestre | `1g3eVD3zLMuwk0jevAwVL3wSmxhEMkKsAUPFQh2wEn88` | mapa federado |
| Google Drive | matriz de rastreabilidade | `1FMuZ-WVvuI7qbQJ8E5LjfHOKShI83VMsJfGB2zyWHgE` | reconciliação tabular |

## Objetos geométricos navegáveis

1. toro padrão `T²` sob homeomorfismo;
2. pirâmide triédrica dupla sob colagem discreta — mapa exato aberto;
3. triângulo normalizado em coordenadas baricêntricas sob transformação afim;
4. lattice Ω7 de 2401 endereços — estrutura, não significado;
5. embedding no modelo de bola de Poincaré — separado de retorno e conjectura;
6. núcleo IGC replicado entre GitHub e Drive — hash ainda aberto.

## Regra de navegação

```text
sem object_id → parar
sem transformation_family → parar
invariante incompatível → FAIL
sem epsilon/unidade quando numérico → parar
sem falsificador → parar
sem evidência/custódia → TOKEN_VAZIO
```

## R3

- `F_ok`: contrato, schema, validador, fixtures e rotas atuais existem.
- `F_gap`: P0 e P1 estão enumerados e não devem ser ocultados por novos conceitos.
- `F_next`: executar P0 em ordem e registrar cada fechamento como evento append-only.
