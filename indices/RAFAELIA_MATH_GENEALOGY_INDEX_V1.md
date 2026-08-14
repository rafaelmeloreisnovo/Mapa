# RAFAELIA — Índice de Genealogia Matemática — V1

Data: 2026-08-14
Estado: `GOVERNED_PARTIAL / CLAIM_ALLOWED=false`

## Rota principal

`cálculo -> interpretação -> nome -> implementação -> execução -> evidência -> claim -> novidade gate`

## Artefatos desta sessão

1. `docs/canonical/2026-08-14/RAFAELIA_MATH_SESSION_AUDIT_V1.md`
   - auditoria matemática genealógica;
   - equivalências, correções, TOKEN_VAZIO e sobreviventes M2.

2. `data/formulas/RAFAELIA_FORMULA_REGISTRY.v3.json`
   - extensão append-only de V2;
   - não reescreve V1/V2;
   - registra delta matemático desta sessão.

3. `data/governance/novelty_math_ledger_delta_2026-08-14.v1.json`
   - contrato M0–M4;
   - novelty_proven=0;
   - fila M2 e regras anti-regressão.

4. `data/evidence/local/coexistence_math_audit_2026-08-14.v1.json`
   - execução local em CONTAINER_REFERENCE;
   - hashes SHA-256 dos fontes;
   - resultados Coexistence/AETHER/IRON;
   - limites explícitos da evidência.

## Âncoras anteriores preservadas

- `data/formulas/RAFAELIA_FORMULA_REGISTRY.v1.json` — 50 registros históricos;
- `data/formulas/RAFAELIA_FORMULA_REGISTRY.v2.json` — extensão governada por referência;
- `docs/canonical/2026-08-12/RAFAELIA_FORMULA_SESSION_REGISTRY_V1.md` — snapshot de 122 relações da sessão anterior;
- `indices/RAFAELIA_FORMULA_INDEX_V2.md` — índice anterior.

## M2 ativos

### M2-BITRAF64-FORMAL
Formalizar transformação exata e provar/refutar invariantes de álgebra finita.

### M2-G-30-45-42
Definir estado/transições/acoplamento, enumerar órbitas e testar equivalência com sistemas conhecidos.

### M2-NCRIT-SEMANTIC
Definir funcional geometria–entropia e buscar theorem/bound/counterexample.

## Anti-regressão

- `a_n=F_{n+3}-1` não deve voltar a ser tratado como recorrência independente nova;
- XOR uniforme em 16 bits reduzido módulo 42 é levemente enviesado;
- 42 pontos finitos têm dimensão de Hausdorff clássica 0;
- `D_KY` permanece TOKEN_VAZIO sem espectro de Lyapunov completo;
- balanço de índices de Poincaré–Hopf não é automaticamente balanço fonte/sorvedouro;
- `ops_eq/s != FLOP/s`;
- Pipeline B do Coexistence altera instâncias/variáveis e não resolve diretamente 80,05% dos difíceis originais;
- scan O(N) sobre caches pré-computados não demonstra redução universal `N^N -> O(N)`.

## Cobertura

A contagem de 13 famílias é apenas da passagem desta sessão. O restante do inventário matemático não recuperado/normalizado fica em `TOKEN_VAZIO_PARTIAL_COVERAGE`.

## Próxima rota verificável

`BITRAF64 formal -> G_{30,45,42} -> n_crítico -> normalização integral do registry -> prior art por conceito/fórmula -> evidence gate`.
