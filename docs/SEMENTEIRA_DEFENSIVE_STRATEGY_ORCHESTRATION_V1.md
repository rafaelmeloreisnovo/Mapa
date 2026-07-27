# Sementeira — Orquestração Defensiva de Estratégias V1

Status: `CANONICAL_DRAFT / WHITE_HAT_DEFENSIVE / MANUAL / READ_ONLY / CLAIM_ALLOWED=false`

Autoria conceitual: Rafael Melo Reis — ∆RafaelVerboΩ

## 1. Propósito

Esta extensão impede que ideias latentes, laterais, esquecidas, desprezadas ou óbvias que passaram batido sejam simplesmente descartadas. Cada estratégia útil entra num ledger rastreável e é submetida a dois riscos simultâneos:

- risco de adotar;
- risco de não adotar.

Conhecer categorias de ameaça serve para prevenção, detecção, resposta e recuperação. Não autoriza operacionalizar comportamento nocivo, acesso indevido ou capacidade reutilizável de alto risco.

```text
conhecer o risco
→ modelar abstratamente
→ detectar
→ mitigar
→ testar com segurança
→ registrar receipt

não:
conhecer o risco
→ operacionalizar abuso
```

## 2. Origem vetorial

Uma estratégia pode nascer de:

- `OBSERVED`;
- `LATENT`;
- `LATERAL`;
- `FORGOTTEN`;
- `DISREGARDED`;
- `OBVIOUS_MISSED`;
- `MODEL_INHIBITION_CANDIDATE`.

`MODEL_INHIBITION_CANDIDATE` não presume censura ou defeito interno. Apenas registra que uma ideia pode ter deixado de emergir por compressão contextual, prioridade concorrente, restrição de segurança, falta de evidência ou outra causa ainda não identificada.

## 3. Conhecimento em cinco níveis

| Nível | Conteúdo permitido | Estado normal |
|---|---|---|
| `K0_PUBLIC_CONCEPT` | conceitos, riscos, governança, ética | público/auditável |
| `K1_DETECTION_MITIGATION` | indicadores, detecção, mitigação, resposta | defensivo |
| `K2_SAFE_SIMULATION` | fixtures sintéticos e emulação não operacional | piloto isolado |
| `K3_RESTRICTED_AUTHORIZED_LAB` | conhecimento sensível sob necessidade, autorização e contenção | quarentena |
| `K4_PROHIBITED_HIGH_RISK_DETAIL` | detalhe ofensivo reutilizável | proibido; não armazenar |

O registro K4 conserva somente categoria, motivo de bloqueio e controle defensivo. Não conserva instrução operacional.

## 4. Gates fail-closed

Antes da priorização:

1. dignidade e direitos fundamentais;
2. legalidade e autorização explícita;
3. segurança física e psicológica;
4. privacidade, autonomia e proporcionalidade;
5. risco de transferência para abuso;
6. isolamento, rollback e observabilidade;
7. supervisão humana e possibilidade de recurso.

Falha em gate crítico produz `P3_QUARANTINE` ou `P4_PROHIBITED`.

## 5. Ordem normativa interna

```text
HUMAN_DIGNITY_AND_FUNDAMENTAL_RIGHTS
→ APPLICABLE_LAW_AND_AUTHORIZATION
→ PHYSICAL_AND_PSYCHOLOGICAL_SAFETY
→ PRIVACY_AND_AUTONOMY
→ SECURITY_AND_RESILIENCE
→ ORGANIZATIONAL_POLICY
→ PERFORMANCE_OPTIMIZATION
```

Essa ordem é uma política de governança do projeto, não parecer jurídico universal. Conflitos reais exigem revisão humana competente e registro da jurisdição aplicável.

## 6. Risco de adoção e risco de omissão

Para cada estratégia `s`:

```text
R_adopt(s) = dano possível ao implementar
R_omit(s)  = dano possível ao ignorar
```

Decisões que registram somente `R_adopt` podem rejeitar controles necessários. Decisões que registram somente `R_omit` podem justificar vigilância, coerção ou exposição desproporcional.

A decisão precisa registrar ambos, mais:

- risco residual;
- pessoas afetadas;
- evidência;
- reversibilidade;
- data de revisão;
- responsável;
- caminho de recurso;
- condição de suspensão.

## 7. Priorização sem fórmula mágica

Não há pesos estatisticamente calibrados. Portanto o motor usa:

1. gates categóricos;
2. classificação P0–P4;
3. ordenação lexicográfica transparente.

```text
P0_MANDATORY_GUARDRAIL
P1_DEFENSIVE_PILOT
P2_OBSERVE_AND_RESEARCH
P3_QUARANTINE
P4_PROHIBITED
```

Dentro da mesma classe, a ordem considera:

1. maior risco de omissão;
2. maior valor defensivo;
3. maior força de evidência;
4. maior observabilidade;
5. maior reversibilidade;
6. menor risco de adoção;
7. menor risco à dignidade;
8. menor transferibilidade para abuso.

Os pesos permanecem `TOKEN_VAZIO_CALIBRATION`.

## 8. Conflito normativo

Uma norma ou controle pode proteger uma dimensão e ferir outra. Exemplos abstratos:

- monitoramento de segurança versus privacidade;
- retenção de logs versus minimização de dados;
- bloqueio automatizado versus devido processo e recurso;
- detecção de fraude versus discriminação indireta;
- segredo operacional versus transparência e auditabilidade;
- eficiência versus acessibilidade.

Registro mínimo:

```text
norma_a
norma_b
controle_em_conflito
pessoas_afetadas
risco_adocao
risco_omissao
fundamento_superior
medida_temporaria
responsavel_revisao
sunset_date
appeal_path
```

Exceção sem data de expiração tende a virar regra invisível. Por isso toda exceção precisa de `sunset_date` ou `TOKEN_VAZIO_REVIEW_DATE` bloqueante.

## 9. Compatibilidade com referências externas

A arquitetura é compatível, sem alegar certificação, com:

- Constituição Federal brasileira, dignidade da pessoa humana;
- LGPD, privacidade, autodeterminação informativa, direitos humanos e dignidade;
- NIST CSF 2.0: Govern, Identify, Protect, Detect, Respond, Recover;
- NIST AI RMF: Govern, Map, Measure, Manage;
- ISO/IEC 27001:2022, gestão de riscos de segurança da informação;
- ISO/IEC 42001:2023, sistema de gestão e melhoria contínua para IA;
- Recomendação da UNESCO sobre Ética da IA, direitos humanos, dignidade e supervisão humana.

O projeto não declara conformidade ou certificação com nenhuma dessas referências.

## 10. Estratégias iniciais

O baseline contém oito estratégias:

1. ledger de ideias latentes e esquecidas;
2. modelagem adversarial abstrata;
3. emulação segura e isolada;
4. risco duplo adoção/omissão;
5. gate de dignidade;
6. registro de conflito normativo;
7. laboratório autorizado restrito;
8. bloqueio de detalhe ofensivo reutilizável.

## 11. Invariantes

```text
white_hat_intent != unrestricted_capability
threat_awareness != harmful_operationalization
defensive_simulation != live_target
authorization != implied_permission
standard_compliance != human_dignity
security_gain != automatic_proportionality
not_adopting != zero_risk
adopting != guaranteed_protection
latent_idea != validated_strategy
quarantine != deletion
prohibited_detail != forgotten_risk
```

## 12. Fluxo

```text
DETECT_LATENT_OR_OBSERVED_STRATEGY
→ PRESERVE_SOURCE
→ CLASSIFY_KNOWLEDGE_TIER
→ CALCULATE_DUAL_RISK
→ APPLY_DIGNITY_AND_AUTHORIZATION_GATES
→ REGISTER_NORM_CONFLICTS
→ DEFINE_FALSIFIER
→ CLASSIFY_P0_P4
→ ORDER_LEXICOGRAPHICALLY
→ PILOT_OR_QUARANTINE
→ APPEND_RECEIPT
→ REVIEW_AND_FEEDBACK
```

## 13. Estado

### F_ok

- estratégia defensiva separada de detalhe ofensivo;
- risco de adoção e omissão registrados;
- dignidade e autorização como gates;
- conflitos normativos preservados;
- priorização P0–P4 implementada;
- oito estratégias iniciais;
- motor stdlib-only;
- testes negativos e positivos;
- nenhum workflow novo.

### F_gap

- pesos calibrados;
- corpus humano rotulado para medir qualidade de recuperação de ideias latentes;
- revisão jurídica por jurisdição e caso concreto;
- exercícios autorizados externos;
- evidência independente de redução de incidentes;
- métricas reais de falso positivo, falso negativo e dano humano.

### F_next

Aplicar o registro a três decisões históricas do ecossistema e comparar o que teria sido perdido ao olhar apenas o risco de adoção ou apenas o risco de omissão.
