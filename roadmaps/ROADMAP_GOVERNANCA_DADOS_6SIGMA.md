# Roadmap de Governança de Dados e Cadeia de Custódia — DMAIC

## Estado global

```yaml
programa: GOV-CUSTODY-6SIGMA
repositorio_piloto: rafaelmeloreisnovo/Mapa
modo: incremental
estado: PILOT_MEASURED
claim_allowed_programa: false
certificacao_six_sigma: TOKEN_VAZIO
nivel_sigma: TOKEN_VAZIO
principio: medir antes de afirmar
```

Este roadmap implanta governança sem paralisar o acervo. Cada fase possui entrada,
saída, evidência e critério de interrupção.

## P0 — Fundação determinística

### DEFINE

**Objetivo:** fixar escopo, defeitos e responsáveis.

- [x] contrato de evento de custódia;
- [x] estados epistêmicos, incluindo `TOKEN_VAZIO`;
- [x] regra `claim_allowed=false` sem evidência suficiente;
- [x] definição inicial de defeitos;
- [x] oito oportunidades de qualidade por evento piloto;
- [ ] responsáveis formais por domínio — `TOKEN_VAZIO`;
- [ ] classificação de dados por sensibilidade em todos os repositórios — `TOKEN_VAZIO`.

**Saída:** problema e fronteira operacional explícitos.

### MEASURE

**Objetivo:** criar linha de base sem inventar números.

- [x] ledger JSONL append-only;
- [x] validador local sem dependências externas;
- [x] inventário do ledger piloto;
- [x] contagem de oportunidades por tipo de evento;
- [x] baseline piloto de completude, rastreabilidade, integridade e
  reprodutibilidade;
- [x] DPMO observado do snapshot piloto;
- [ ] idade mediana dos `TOKEN_VAZIO` — `TOKEN_VAZIO`;
- [ ] convenção estatística para capacidade e nível sigma — `TOKEN_VAZIO`;
- [ ] estabilidade em janelas repetidas — `TOKEN_VAZIO`.

**Evidência:**

- `auditoria/PR39_EXECUTION_EVIDENCE.json`;
- `auditoria/BASELINE_CADEIA_CUSTODIA_2026-07-21.json`.

**Gate:** nenhuma certificação ou taxa de capacidade sigma é publicada sem
processo estável, convenção estatística aprovada e janelas repetidas.

## P1 — Diagnóstico e priorização

### ANALYZE

**Objetivo:** localizar causas, não apenas sintomas.

- agrupar defeitos por repositório, tipo de objeto e etapa;
- aplicar Pareto 80/20 somente com amostra suficiente;
- usar 5 Porquês e Ishikawa para defeitos recorrentes;
- separar falha de processo, ausência de dado e ambiguidade semântica;
- cruzar eventos com o catálogo biblioteconômico e o mapa de dependências;
- registrar causalidade não demonstrada como `HIPOTESE` ou `TOKEN_VAZIO`.

**Saída:** backlog priorizado por risco × frequência × impacto × verificabilidade.

## P2 — Melhoria controlada

### IMPROVE

**Objetivo:** reduzir defeitos sem criar dependência ou complexidade desnecessária.

- gerar eventos automaticamente em operações estáveis;
- acrescentar hashes quando o objeto estiver disponível localmente;
- criar adaptadores para commits, PRs, relatórios e datasets;
- integrar o ledger ao indexador do `Mapa`;
- adicionar testes de regressão para regras consolidadas;
- manter revisão humana em claims científicos, jurídicos e éticos;
- pilotar assinatura digital apenas após modelo de ameaça aprovado.

**Gate de mudança:** toda automação deve demonstrar redução de defeito ou custo,
sem diminuir auditabilidade.

## P3 — Sustentação

### CONTROL

**Objetivo:** impedir regressão e tornar a melhoria contínua.

- painel mensal de métricas por processo;
- amostragem de auditoria por risco;
- limites de controle somente após série temporal suficiente;
- política de expiração e revalidação de evidências;
- revisão periódica do vocabulário controlado;
- SLA por classe de `TOKEN_VAZIO`;
- relatório de exceções e risco residual;
- retrospectiva PDCA após cada ciclo DMAIC.

## Métricas canônicas

| ID | Métrica | Fórmula | Snapshot piloto |
|---|---|---|---|
| M1 | Completude estrutural | eventos válidos / eventos | `1.0` |
| M2 | Rastreabilidade | eventos com evidência / eventos | `1.0` |
| M3 | Integridade | hashes verificados / hashes declarados | `1.0` |
| M4 | Reprodutibilidade | eventos com controle verificado / eventos | `0.666667` |
| M5 | Resolução de lacunas | vazios resolvidos / vazios totais | `TOKEN_VAZIO` |
| M6 | Lead time de vazio | resolução − abertura | `TOKEN_VAZIO` |
| M7 | DPMO observado | defeitos / oportunidades × 1.000.000 | `0.0` |
| M8 | Nível sigma | convenção aprovada sobre processo estável | `TOKEN_VAZIO` |

Os valores M1–M4 e M7 pertencem apenas ao checkpoint auditado de 12 eventos e 96 oportunidades. Não são
generalizados para outros repositórios nem equivalem a certificação Six Sigma.

## Mapa de riscos

| Risco | Controle preventivo | Controle detectivo | Resposta |
|---|---|---|---|
| conclusão sem prova | `claim_allowed=false` | validador + revisão | converter em `TOKEN_VAZIO` |
| alteração sem origem | campos obrigatórios | auditoria do ledger | bloquear publicação |
| hash falso ou inválido | formato estrito | recomputação local | evento `CORRECT` |
| exposição de segredo | minimização | varredura de conteúdo | revogar e retirar acesso |
| cadeia quebrada | predecessor imediato | validação sequencial | reparar por evento corretivo |
| evento inválido como âncora | aceitação somente sem defeitos | teste regressivo | rejeitar elo posterior |
| excesso de burocracia | ação mínima verificável | métrica de lead time | simplificar controle |
| automação sem benefício | hipótese mensurável | comparação antes/depois | rollback |

## Roadmap por ondas

### Onda 1 — `Mapa`

- governança, biblioteconomia, índices, validadores e baseline;
- estado: piloto medido, PR ainda em draft;
- objetivo: provar o método no repositório orquestrador.

### Onda 2 — repositórios de infraestrutura

- Termux, RafGitTools, Vectras/QEMU;
- foco: build, artefato, versão, proveniência e segurança;
- estado: `ROADMAP`, sem expansão automática nesta etapa.

### Onda 3 — repositórios científicos

- RLL, papers e datasets;
- foco: fonte, experimento, parâmetros, resultado, falsificadores e claim;
- estado: `ROADMAP`.

### Onda 4 — acervo filosófico e simbólico

- CientiEspiritual, Livro Vivo e correlatos;
- foco: autoria, versão, remissivas e marca `SIMBOLICO`, sem falsa equivalência experimental;
- estado: `ROADMAP`.

## Próximo passo verificável

Repetir a medição em janelas futuras do ledger, registrar defeitos reais como
eventos, aprovar a convenção estatística e somente então avaliar capacidade do
processo. O PR permanece em draft e `main` não é alterada nesta etapa.
