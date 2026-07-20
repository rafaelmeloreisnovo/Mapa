# ISO Operational Readiness — retroalimentação conservadora

## Autoridade e limite

Este artefato pertence ao `Mapa` porque registra **escopo, maturidade, pessoas,
horas, lacunas, prioridades e dependências**. Ele não copia o texto das normas,
não certifica o ecossistema e não substitui auditoria independente.

```text
ISO 9000 / 9001  → linguagem e sistema de gestão da qualidade
ISO 8000         → qualidade, governança e medição dos dados
ISO/IEC 27000    → visão do SGSI
ISO/IEC 27001    → requisitos do SGSI
ISO/IEC 27002    → controles de segurança
Mapa             → baseline conservador, gaps e capacidade
```

## Correção temporal incorporada

A releitura usa o estado oficial observado em 20 de julho de 2026:

- `ISO 9000:2026` já está publicada;
- `ISO 9001:2015` ainda é a edição vigente de requisitos, com substituição de
  2026 em publicação prevista para setembro;
- `ISO 8000-8:2015`, `8000-51:2023` e `8000-63:2019` permanecem referências
  para conceitos, política e pilha de medição de dados;
- `ISO/IEC 27000:2026` foi publicada em julho de 2026;
- `ISO/IEC 27001:2022` e `27002:2022` continuam como requisitos e controles.

A referência à norma não produz conformidade. O gate permanece:

```text
controle escrito
∩ controle implementado
∩ controle executado
∩ evidência preservada
∩ revisão competente
```

## Retroalimentação do estado atual

O diagnóstico anterior permanece útil, mas foi atualizado com o `main` do
`Mapa` em `debf73d...`:

```text
repositórios observados       126
materializados                 51
TOKEN_VAZIO                    75
completude                  40,48%
adaptadores federados ativos    6
gaps de evidência federada       1
work items de assurance         12
bloqueadores abertos             9
promoções prontas                0
```

A arquitetura evoluiu de L2/L3 para **L3 em governança federada**, mas a
prontidão operacional geral continua entre **L2 e L3**, com ilhas L4 no RLL e
em validadores determinísticos. A razão é simples: adaptador ativo não é
recibo físico; documentação não é execução; e `ZERO_STEP_NO_LOGS` não é PASS.

## Estimativa conservadora preservada

| Escopo | Pessoas | Horas | Calendário |
|---|---:|---:|---:|
| Diagnóstico dos 8 núcleos | 7–9 | 1.800–2.600 | 7–10 semanas |
| Auditoria profunda e backlog | 10–14 | 3.800–5.800 acumuladas | 10–16 semanas |
| Baseline operacional do núcleo | 14–16 | 10.300–15.800 acumuladas | 6–9 meses |
| Portfólio de 126 repositórios | 22–28 | 24.000–40.000 | 12–18 meses |

A estimativa mantém **±30% de incerteza** enquanto 75 repositórios não forem
materializados. Grandes forks devem ser auditados por delta:

```text
upstream pinado → delta RAFAELIA → risco → teste → artefato → evidência
```

Reauditar integralmente Android Framework, AndroidX, Linux, Gradle e QEMU como
código novo elevaria o esforço para 60–90 mil horas e não é recomendado.

## Núcleo de pessoas

O baseline exige 14 funções: arquitetura, QMS, processos, dados, metadados,
SGSI, DevSecOps, Android/NDK, C/ASM/QEMU, IA/privacidade, ciência/estatística,
QA líder, QA automação e configuração/documentação/PMO. O portfólio completo
precisa de 22–28 pessoas para reduzir bus factor e preservar segregação de
funções.

## Nova leitura do que falta

A nova varredura materializou 25 lacunas com dono, prioridade, faixa de horas,
próxima ação e critério de saída.

### P0 — bloqueadores imediatos

1. completar ou excluir formalmente os 126 repositórios;
2. impedir declarações `COMPLETE/COMPLIANT` sem cadeia de prova;
3. criar retenção e deleção para conversas, chunks e corpus privados;
4. definir escopo e classificação de ativos do SGSI;
5. criar registro de riscos federado;
6. tornar CI observável, sem `ZERO_STEP_NO_LOGS`;
7. produzir recibo real do dispositivo e APK instalados;
8. fechar licenças, autoria e direitos de reutilização.

### P1 — sistema de gestão

Inclui QMS federado, CAPA, pilha ISO 8000 de medição, dicionário mestre,
Statement of Applicability, assinatura/proveniência, rollback, continuidade e
baselines de delta dos grandes forks.

### P2/P3 — sustentação

Inclui séries históricas de métricas, incident response, bus factor,
competências, fechamento documental e revisão independente.

## Trinta heurísticas executáveis

O baseline machine-readable registra exatamente 30 heurísticas distintas:

1. autoridade única;
2. interseção escrita–implementação–execução–evidência;
3. auditoria por delta;
4. completude do inventário;
5. lacunas não compensatórias;
6. atualidade temporal;
7. consistência entre claim e métrica;
8. camadas de reprodutibilidade;
9. realidade do dispositivo;
10. confiança da supply chain;
11. rollback real;
12. exposição de secrets;
13. linhagem de dados;
14. drift de schema;
15. preservação semântica;
16. deduplicação;
17. licenças e direitos;
18. minimização de privacidade;
19. vínculo ameaça–risco;
20. raio de impacto;
21. segregação de funções;
22. bus factor;
23. fechamento CAPA;
24. indicadores antecedentes e resultados;
25. equilíbrio do portfólio de testes;
26. taxonomia de falha;
27. identidade do artefato;
28. capacidade e eficiência;
29. desafio independente;
30. retroalimentação com dono e critério de saída.

O validador bloqueia redução dessas heurísticas, duplicidade, baixa diversidade,
faixas inválidas, lacuna sem dono, lacuna sem critério de saída, promoção de
claim e adulteração do selo BLAKE2b-256.

## Ondas operacionais

```text
ONDA 0  identidade, escopo, secrets, direitos e blockers P0
ONDA 1  QMS + CAPA + risco + ativos + SoA
ONDA 2  ISO 8000: dicionário, linhagem, medição e retenção
ONDA 3  build → teste → artefato → dispositivo → rollback
ONDA 4  métricas históricas, exercícios e auditoria independente
```

Nenhuma onda posterior compensa uma falha de segurança, direitos ou evidência
na onda anterior.

## Estado final desta retroalimentação

```text
assessment_type = CONSERVATIVE_OPERATIONAL_READINESS_NOT_CERTIFICATION
claim_allowed    = false
certification    = false
strategy         = DELTA_FIRST_RISK_BASED_WAVES
next_gate        = P0_EVIDENCE_AND_SCOPE_CLOSURE
```

```text
R3 = <
  F_ok   = governança federada e validadores reais,
  F_gap  = 25 lacunas, 9 blockers e 75 repositórios vazios,
  F_next = fechar P0 antes de expandir claims
>
```
