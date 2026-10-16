# ATLAS Ω — SAT estrutural L0 · ponte falsificável V1

- **Estado:** CANDIDATE / DRAFT / NÃO PROMOVER / `claim_allowed=false`.
- **Objeto de navegação:** estruturar perguntas sobre P versus NP, sem reivindicar uma demonstração de P=NP.
- **Fonte produtora:** [RafGitTools PR #683](https://github.com/rafaelmeloreisnovo/RafGitTools/pull/683) (draft; commit `16eb6a106ccf2274576fc53875f1fb8797c6d186`).
- **Código do produtor:** `native/sat_structure_l0_v1/{sat_structure_l0.c,sat_structure_l0.h}`.
- **Teste/receipt:** `tests/sat_structure_probe.py` e `receipts/SAT_STRUCTURE_LOCAL_MEASUREMENT_20261016.json` no mesmo commit.
- **Nó de autoridade:** RafGitTools governa fonte/experimento; Mapa governa somente roteamento e tipagem; Drive governa ledger/índice.
- **Rota:** START HERE Ω V2.2 → CURRENT_STATE → CANONICAL_INDEX_MINIMUM → esta ponte → PR#683@SHA → receipt → falsificador → μWRITE → R3.
- **Grafo:** `CNF_INSTANCE -STRUCTURED_BY-> PRIMAL_GRAPH -MEASURED_BY-> INDUCED_WIDTH_FIXED_ORDER`; `ALGORITHM_RESULT -EVIDENCED_BY-> LOCAL_RECEIPT`; `CLAIM -BLOCKED_BY-> UNRESOLVED_REVIEW`.
- **Medida observada (somente local):** 178 casos verificados; 24/24 locais VE SAT; 9/24 controles VE SAT; 15/24 controles `WIDTH_BUDGET`; DPLL SAT 48/48 controles plantados.
- **Evidência não herdável:** testes locais != CI remoto; teto de largura != prova geral de NP/P; coerência semântica != correção do algoritmo.
- **F_gap:** CI exact-head terminal, ARM32 físico, benchmark hold-out, revisão independente e cruzamento por hashes dos shards reais `TOKEN_VAZIO`.
- **F_next:** ler PR#683 workflow run exato e falsificador independente; fazer successor desta ponte em vez de editar evidência histórica.
- **Rollback:** este arquivo fica em PR draft, sem modificar os registries canônicos ou a `main`.
