# RAFAELIA — F_NEXT executado: registry e grafo tipado

**Data:** 2026-08-02  
**Parent:** OMEGA7_FIBONACCI_TRIBONACCI_123_REVIEW_V1  
**Estado:** PASS_LIMITED_LOCAL · claim_allowed=false

## Circuito materializado

    schema
    → registry de famílias
    → gerador determinístico
    → matriz/recorrência
    → grafo tipado
    → testes
    → receipt
    → espelhos Drive/GitHub

Famílias:

- SEED_123: literal textual, três nós;
- FIB_FROM_123: ordem 2, termos 1,2,3,5,8,13,21,34,55,89,144,233;
- TRIB_FROM_123: ordem 3, termos 1,2,3,6,11,20,37,68,125,230,423,778.

Resultado local:

    27 nós
    26 arestas
    6 testes PASS
    0 testes FAIL após correção
    graph_sha256 =
    cac6169b89ac88d04c2381d372578e875a54c39e40f27807c44efca2d7b44b08

## Falha observada e corrigida

Na primeira iteração, a ordenação lexical dos IDs colocou 144 antes de 3. A matemática estava correta; a topologia de apresentação estava errada. O índice canônico foi corrigido para:

    (family_id, sequence_index)

O receipt preserva esse evento como INDEXING_DEFECT → FIXED → RETEST PASS.

## Invariantes fechadas localmente

1. raw_token="123" preservado em todos os nós;
2. endpoints de todas as arestas existem;
3. claim_allowed=false em nós, arestas e receipt;
4. ordem de recorrência declarada;
5. termos Fibonacci e Tribonacci reproduzidos;
6. hash determinístico em segunda construção no mesmo ambiente.

## Ainda não promovido

TOKEN_VAZIO permanece para CI observável, Termux/ARM, reprodução independente, hash cruzado entre superfícies e qualquer interpretação física/cosmológica.

## Próximo eixo

    reprodução independente
    → comparação de graph_sha256
    → property tests de transformações
    → integração no mapa longitudinal
