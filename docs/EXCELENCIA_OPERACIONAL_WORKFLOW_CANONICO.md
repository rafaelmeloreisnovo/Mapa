> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ — nenhuma automação promove conteúdo acima da evidência disponível; executar mais nunca vale mais que executar com limite, prova, privacidade e possibilidade de rollback.

# Excelência Operacional — Workflow Canônico RAFAELIA

## 1. Finalidade

Este pacote converte a auditoria de fontes, workflows e “olhos” especializados em um contrato executável. Ele não substitui a cadeia de custódia, a ontologia, o registro cross-source ou a topologia do `Mapa`; ele os conecta por uma unidade operacional comum.

```text
fonte
→ ingestão
→ validação
→ normalização
→ indexação
→ decisão epistemológica
→ execução autorizada
→ verificação
→ publicação revisada
→ controle append-only
```

A unidade do processo nasce do contrato, não da fusão dos componentes:

```text
RafGitTools governa
Termux executa
RafPolimata estrutura
GPT/Llama interpreta
RLL classifica evidência
Mapa preserva proveniência, estado e decisão
```

## 2. Artefatos

| Artefato | Função |
|---|---|
| `schemas/operational-workflow.schema.json` | contrato estrutural JSON Schema |
| `data/workflows/rafaelia-operational-workflow.v1.json` | DAG canônico com estados reais e planejados |
| `scripts/validate_operational_workflow.py` | gate semântico determinístico em Python stdlib |
| `tests/test_operational_workflow.py` | invariantes positivos e negativos |
| `.github/workflows/operational-workflow-contract.yml` | CI, relatório e checksums |

## 3. Invariante de estágio

Nenhum estágio pode ser apenas “ativo”. Todo estágio declara:

```text
identidade literal
+ fase
+ estado epistêmico
+ dependências
+ entradas
+ transformação
+ saídas
+ critérios de sucesso
+ evidências exigidas
+ modos de falha
+ rollback
+ limites de recurso
+ implementação
+ próximo passo verificável
```

\[
10.000\times\text{ativo}
\neq
1\times\text{execução verificável}
\]

## 4. Estados preservados

| Estado | Regra |
|---|---|
| `active` | implementação presente; estado `FATO` ou `VERIFIED_LIMITED` |
| `planned` | `epistemic_state=TOKEN_VAZIO` e `claim_allowed=false` |
| `blocked` | não executa nem promove claim |
| `retired` | preservado historicamente, sem claim operacional atual |

O workflow canônico contém:

```yaml
stages_total: 10
active: 6
planned: 4
workflow_claim_allowed: false
```

Os estágios ativos correspondem a artefatos já existentes no `Mapa`:

- ingestão científica canônica;
- validação cross-source;
- normalização ontológica;
- indexação relacional;
- gate topológico e epistemológico;
- cadeia de custódia.

Permanecem planejados e honestamente limitados:

- interpretação semântica governada;
- execução autorizada;
- verificação independente do artefato;
- publicação revisada ponta a ponta.

## 5. Gates bloqueantes

O validador rejeita:

1. IDs repetidos;
2. dependência inexistente, auto-dependência ou ciclo;
3. estágio ativo marcado como hipótese ou `TOKEN_VAZIO`;
4. estágio ativo sem implementação;
5. estágio ativo dependente de estágio não ativo;
6. entrada sem origem externa ou ancestral;
7. saída duplicada, órfã ou terminal inexistente;
8. claim sem requisito de evidência;
9. execução ou publicação sem revisão humana;
10. caminho absoluto ou `../` em referência de implementação;
11. referência ativa ausente no checkout;
12. timeout acima da política;
13. promoção global quando ainda há estágios planejados.

## 6. Evidência produzida pela CI

A Action gera, sem modificar automaticamente o repositório:

```text
build/operational-workflow/report.json
build/operational-workflow/SHA256SUMS
```

O relatório inclui status, contagens, ordem topológica, defeitos, entradas externas, saídas terminais e próximo passo verificável.

## 7. Comandos oficiais

```bash
python3 -m py_compile \
  scripts/validate_operational_workflow.py \
  tests/test_operational_workflow.py

python3 -m unittest tests/test_operational_workflow.py -v

python3 scripts/validate_operational_workflow.py \
  data/workflows/rafaelia-operational-workflow.v1.json \
  --repo-root . \
  --write-report build/operational-workflow/report.json
```

## 8. Fronteira de segurança

Este contrato não concede ao modelo acesso direto a credenciais, arquivos brutos privados ou execução irrestrita. O modelo recebe segmentos, relações, proveniência e política. Execução e publicação exigem revisão humana explícita.

```text
interpretação ≠ autorização
compilação ≠ produção
artifact ≠ validade científica
commit ≠ prova de execução
```

## 9. Próximo vertical

O próximo trabalho não é ativar os quatro estágios de uma vez. É fechar somente:

```text
relation_index
→ interpret_context
→ semantic_hypotheses
```

com fixture privada sintética, política de redação, teste contra exposição de identidade, vínculo obrigatório entre hipótese e evidência e saída `TOKEN_VAZIO` quando interpretações concorrentes permanecem próximas.

Até esse vertical produzir evidência:

```yaml
interpret_context: TOKEN_VAZIO
execute_operation: TOKEN_VAZIO
verify_artifact: TOKEN_VAZIO
publish_result: TOKEN_VAZIO
claim_allowed: false
```
