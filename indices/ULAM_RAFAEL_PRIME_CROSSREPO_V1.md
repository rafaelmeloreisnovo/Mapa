# Ulam × Rafaeliana — Cross-Repo Index V1

**Data:** 2026-08-12  
**Estado:** `GOVERNED_PARTIAL`  
**claim_allowed:** `false`

## 1. Rotas de autoridade

| Camada | Repositório | Artefato | Estado |
|---|---|---|---|
| prova/formalização | `rafaelmeloreisnovo/Matem-tica-` | `docs/formal/RAFAELIANA_PRIME_FACTOR_THEOREM_V1.md` | FORMAL_MATH |
| verificador finito | `rafaelmeloreisnovo/Matem-tica-` | `src/verify_rafaeliana_prime_factor.py` | FINITE_VERIFIER |
| protocolo | `rafaelmeloreisnovo/papers` | `docs/matematica_autoral/ULAM_RAF_SAMPLER_RESEARCH_PROTOCOL_V1.md` | RESEARCH_PROTOCOL |
| implementação | `rafaelmeloreisnovo/papers` | `src/experiments/ulam_raf_sampler.py` | EXECUTABLE_REFERENCE |
| testes | `rafaelmeloreisnovo/papers` | `tests/test_ulam_raf_sampler.py` | TEST_CONTRACT |
| fórmulas/ontologia | `rafaelmeloreisnovo/Mapa` | `data/formulas/RAFAELIA_FORMULA_ULAM_DELTA_2026-08-12.v1.json` | APPEND_ONLY_DELTA |

Branch comum:

`audit/ulam-rafael-prime-20260812`

## 2. Invariantes

1. `formula != implementation != execution != evidence != claim`.
2. `prime` no nome de arquivo não implica algoritmo de primalidade.
3. `spiral` no nome de arquivo não implica Espiral de Ulam.
4. Rafaeliana canônica: `R_n=F_{n+3}-1`.
5. Classificação formal: `R_n` é primo exatamente para `n in {1,3}`.
6. A Rafaeliana entra no protocolo Ulam como régua/amostrador, não como linha quadrática rica em primos.
7. Ausência de controle estatístico/literário/físico permanece `TOKEN_VAZIO`.

## 3. Proveniência de commits desta aplicação

### Matem-tica-

- `f7a2ca57a64c44c4c832346f59e832a8bd7adbba` — formalização do teorema de fatoração/primalidade.
- `a60de567f841b58123f047b26793929e41ae0c04` — verificador finito stdlib.

### papers

- `a6ef3e700cda77b0ba18be32360c013136216059` — protocolo Ulam × Rafael.
- `0949eb5a7d6332f2053e7e49ed296d88e5114739` — implementação determinística.
- `493812cf714a383f3123b6cf64197e11839f9444` — testes de contrato.

### Mapa

- `9d06e8cebf9c7b782c0989a2b59166538d3c213c` — delta de fórmulas Ulam.

## 4. Achados semânticos preservados

`papers/src/asm/rafaelia_prime.S` permanece preservado, mas sua autoridade atual é `SIMD_KERNEL`, não `PRIME_ALGORITHM`.

`papers/src/asm/rmr_spiral.S` permanece preservado, mas sua autoridade atual é `SIMD_GEOMETRIC_KERNEL`, não `ULAM_IMPLEMENTATION`.

A divergência entre `sqrt(3/2)` e `sqrt(3)/2` permanece aberta como `TOKEN_VAZIO_WHICH_SPIRAL_CONSTANT`; as expressões diferem por fator `sqrt(2)`.

## 5. Gaps prioritários

### P0

- executar os arquivos exatos do branch e congelar receipt com SHA-256 dos bytes executados;
- implementar enumerador `reta Ulam -> sequência quadrática`;
- adicionar null model modular/classes residuais.

### P1

- pré-registrar `N`, seeds, métricas e testes estatísticos;
- comparar embedding Ulam contra embedding alternativo;
- revisão bibliográfica primária Ulam/Fibonacci/jump sampling.

### P2

- replay físico Android/Termux;
- benchmark de escala e otimização ARM somente depois de corretude matemática.

## 6. Estado R3

**F_ok:** prova, verificador, protocolo, referência executável, testes e delta de fórmulas agora têm rotas explícitas e separadas.  
**F_gap:** execução exata do branch, null modular, enumerador quadrático, prior art e replay físico.  
**F_next:** receipt determinístico -> null modular -> linha quadrática -> pré-registro -> replicação.
