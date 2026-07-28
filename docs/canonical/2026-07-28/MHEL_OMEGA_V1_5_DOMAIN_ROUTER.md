# MHEL-Ω V1.5 — Roteador de Autoridades de Domínio

**Estado:** `IMPLEMENTED_LOCAL_PASS / STACKED_ON_PR80 / claim_allowed=false`

## Objetivo

Receber uma cápsula vetorial validada e encaminhar cada claim para exatamente uma autoridade:

```text
COMPUTATIONAL → gate.computational.v1
SCIENTIFIC    → gate.scientific.v1
LEGAL         → gate.legal.v1
ETHICAL       → gate.ethical.v1
```

O roteador não interpreta texto para adivinhar domínio. O domínio deve ser declarado, o tipo do claim deve pertencer à régua e o estado de entrada deve ser aceito pela autoridade.

## Invariante central

```text
ROUTED_FOR_DOMAIN_REVIEW
!= EVIDENCED
!= PROVED
!= REPLICATED
!= LEGALLY_VALID
!= ETHICALLY_APPROVED
```

Um resultado computacional não pode ser promovido a prova científica, validade jurídica ou aprovação ética. Claims multidomínio devem ser decompostos em claims separados, cada qual com sua própria fonte e gate.

## Gate

```text
vetor identificado
× hash canônico JSON observado = hash declarado
× domínio explícito
× tipo permitido
× estado de entrada permitido
× fontes presentes
× transição limitada a READY_FOR_DOMAIN_SPECIFIC_REVIEW
```

## Segurança

- `stdlib-only`;
- leitura local;
- sem rede;
- sem inferência semântica automática;
- sem YAML novo;
- `claim_allowed=false`;
- `epistemic_promotion_allowed=false`;
- fail-closed.

## F_ok

Roteador, registro de quatro autoridades, schema, envelope, testes e receipt local.

## F_gap

Execução dos gates de domínio, revisão independente, corpus amplo e CI remota com steps/logs.

## F_next

Implementar primeiro `gate.computational.v1` para verificar receipts de testes, identidade dos bytes, ambiente e falsificadores sem extrapolar para ciência.
