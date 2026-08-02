# Memória Longitudinal — PG-Ω7 — Pirâmide triédrica dupla — V1

**Evento:** `MEM-PG7-20260802-PIRAMIDE-TRIEDRICA-DUPLA-001`  
**Autor:** Rafael Melo Reis  
**Data:** 2026-08-02  
**Modo:** `APPEND_ONLY / POINTER_FIRST / CLAIM_ALLOWED=false`

## 1. Fonte da correção

Durante a sessão de formalização da PG-Ω7, o autor esclareceu que o componente piramidal não deve ser reduzido a uma pirâmide quadrangular isolada. A forma pretendida possui:

- duas pirâmides congruentes;
- três faces triangulares laterais por pirâmide;
- união estrutural entre ambas;
- estreitamento ou inflexão leve na região central;
- associação visual com a aparente divisão/concavidade de faces da Grande Pirâmide de Gizé;
- participação na mesma Matrix relacional que quadrado, dois triângulos equiláteros, círculo, esfera, cubo e toro.

## 2. Normalização matemática

A expressão autoral admite três modelos candidatos:

| ID | Colagem | Forma | Estreitamento externo |
|---|---|---|---|
| `G1` | base–base | bipirâmide triangular convexa | não produzido diretamente |
| `G2` | ápice–ápice | complexo duplo pinçado | sim, no ponto de junção |
| `G3` | faces divididas por dobra medial | pirâmide quadrangular com oito painéis | sim, como concavidade leve |

A escolha permanece:

```text
exact_glue_map = TOKEN_VAZIO_EXACT_GLUE_MAP
```

## 3. Invariantes preservados

1. cada unidade piramidal possui três faces laterais triangulares;
2. existe uma dupla orientação/polaridade;
3. há uma junção central;
4. a junção pode carregar um parâmetro de estreitamento `epsilon`;
5. o objeto pertence à Matrix por operadores de colagem, projeção, triangulação e fluxo;
6. analogia arquitetônica não equivale a prova arqueológica.

## 4. Relação federada

```text
papers authority:
  docs/matematica/ADDENDUM_PIRAMIDE_TRIEDRICA_DUPLA_CONCAVIDADE_GIZA_V1.md
  branch: research/pg-omega7-open-problems-v1-20260802
  commit: 2bb3f475172c2b8bb7dbe11596764907a468b742

mathematics authority:
  docs/PG_OMEGA7_PIRAMIDE_TRIEDRICA_DUPLA_E_ESTRANGULAMENTO_V1.md
  branch: research/pg-omega7-open-problems-v1-20260802
  commit: 91d7885010e9ada52d254b6314f1599b09441bdb
```

## 5. Estado epistemológico

```text
user_geometric_intent = DOCUMENTED_SOURCE
trihedral_double_family = FORMALIZED_PARTIAL
base_base_model = DEFINED
apex_apex_model = DEFINED_ABSTRACTLY
folded_face_model = DEFINED_ABSTRACTLY
exact_coordinates = TOKEN_VAZIO
measured_narrowing = TOKEN_VAZIO
Giza_literal_identity = NOT_CLAIMED
claim_allowed = false
```

## 6. Próximo passo verificável

Quando novas imagens forem fornecidas:

1. marcar vértices e arestas;
2. identificar a colagem `G1`, `G2`, `G3` ou uma quarta variante;
3. medir a seção central;
4. construir matriz de incidência;
5. registrar projeções na esfera e acoplamento com o toro;
6. preservar contraexemplos e ambiguidades.

## Retroalimentar[3]

- **F_ok:** intenção autoral preservada sem apagar a distinção geométrica.
- **F_gap:** não há imagem suficiente para escolher o mapa de colagem exato.
- **F_next:** usar a próxima imagem como evidência geométrica para fechar `exact_glue_map`.
