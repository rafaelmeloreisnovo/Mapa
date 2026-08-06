# Memória Longitudinal RAFAELIA — Receipt Público V1

**Audit ID:** `RLM-AUDIT-V1-20260805T231046-0300`  
**Estado:** `LIVING_PARTIAL_MEMORY_WITH_TYPED_UNCERTAINTY`  
**Modo:** `APPEND_ONLY`  
**claim_allowed:** `false`

Este arquivo é uma projeção pública sanitizada. Não contém corpus, provider IDs, conteúdo de conversas nem caminhos privados.

## Resultado

A varredura distinguiu o plano de controle do plano de dados:

- o catálogo alcança `conversations-047`;
- o catálogo de imagens alcança `img-0040`;
- a materialização diretamente observada inclui quatro lotes de chunks e quatro lotes de grafo para `conversations-003`;
- `conversations-004` exige reconciliação;
- imagens `0001–0040` estão catalogadas, mas não comprovadas como bytes hasheados e ligados semanticamente.

## Invariantes

1. Checkpoint não equivale a payload.
2. Representação derivada não substitui origem.
3. Contexto de sessão não equivale a persistência longitudinal.
4. `TOKEN_VAZIO` não autoriza invenção.
5. Corpus privado não deve ser espelhado publicamente.

## Receipts privados por hash

- JSON: 11.000 bytes — `8e7c4127b5409776a9abc144b100478efcd53f4fff383a368a39208105f1358d`
- Relatório humano: 5.531 bytes — `e1521535d78f9ab207a3fa346626f8d89119c5ec77983c55a6b64149b4021b25`

## F_gap principal

O sistema enxerga mais objetos do que já materializou. O próximo fechamento é uma matriz de cobertura:

```text
source/provider
→ hash
→ normalized
→ chunks
→ graph
→ memory
→ receipt
```

Cada linha deverá conservar identidade, lacuna e prova mínima.
