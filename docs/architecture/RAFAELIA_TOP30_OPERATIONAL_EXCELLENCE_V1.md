# RAFAELIA Top-30 Operational Excellence V1

## Finalidade

Este plano de controle ranqueia as trinta práticas de maior valor operacional para a evolução viva do RAFAELIA. O ranking ordena trabalho de engenharia; não é certificado, verdade, probabilidade científica ou conclusão jurídica.

## Invariante

```text
fonte → identidade → execução → teste → receipt → revisão
→ decisão → ponto de rollback → retroalimentação
```

Cada controle possui:

- ranking fixo e valor relativo;
- potencial de uso vivo;
- estado conservador;
- objetivo de controle;
- falsificador explícito;
- próximo passo verificável;
- limite entre automação e julgamento humano.

## Top 10 por valor

1. Mudança vinculada à evidência.
2. Menor privilégio e promoção protegida.
3. Receipts determinísticos e proveniência.
4. Build e runtime reproduzíveis.
5. Testes e falsificadores obrigatórios.
6. Rollback e checkpoints seguros.
7. Custódia de segredos e credenciais.
8. Integridade de dependências e supply chain.
9. Observabilidade acionável.
10. Resposta e contenção de incidentes.

Os vinte seguintes cobrem linhagem de dados, restore, SLOs, revisão independente, auditoria append-only, threat modeling, privacidade, promoção gradual, percentis, orçamento de recursos, fault injection, drift, compatibilidade, acessibilidade, ADRs/runbooks, direitos, replicação, capacidade, retenção e melhoria contínua.

## Cálculo conservador

```text
EVIDENCED        = 1,00
PARTIAL          = 0,50
TOKEN_VAZIO      = 0,00
BLOCKED_EXTERNAL = 0,00
```

A prioridade dinâmica é:

```text
value_score × live_potential × unresolved_gap_weight
```

Essa função prioriza lacunas valiosas. Ela não promove claim.

## Ciclo vivo

O avaliador executa no minuto `57`, depois dos quatro microciclos de 15 minutos. Produz:

- `top30_receipt.json`;
- `top30_next_actions.json`;
- `top30_summary.md`.

O workflow possui permissão apenas de leitura, não persiste credenciais e não pode fazer push ou merge.

## Fronteira de promoção

```yaml
claim_allowed: false
publication_ready: false
automatic_mutation: false
automatic_merge: false
maximum_automatic_decision: READY_FOR_HUMAN_REVIEW
```

Configurações externas, runtime em dispositivo físico, revisão independente e evidência científica permanecem `TOKEN_VAZIO` até observação direta.
