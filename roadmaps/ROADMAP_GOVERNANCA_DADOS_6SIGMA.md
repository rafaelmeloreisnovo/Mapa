# Roadmap de Governança de Dados e Cadeia de Custódia — DMAIC

## Estado global

```yaml
programa: GOV-CUSTODY-6SIGMA
repositorio_piloto: rafaelmeloreisnovo/Mapa
modo: incremental
claim_allowed: false
certificacao_six_sigma: TOKEN_VAZIO
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
- [ ] responsáveis formais por domínio — `TOKEN_VAZIO`;
- [ ] classificação de dados por sensibilidade em todos os repositórios — `TOKEN_VAZIO`.

**Saída:** problema e fronteira operacional explícitos.

### MEASURE

**Objetivo:** criar linha de base sem inventar números.

- [x] ledger JSONL append-only;
- [x] validador local sem dependências externas;
- [ ] inventário de eventos dos fluxos P0;
- [ ] contagem de oportunidades por tipo de evento;
- [ ] baseline de completude, rastreabilidade e integridade;
- [ ] idade mediana dos `TOKEN_VAZIO`.

**Gate:** nenhuma taxa ou nível sigma é publicado sem universo e janela definidos.

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

| ID | Métrica | Fórmula | Estado inicial |
|---|---|---|---|
| M1 | Completude estrutural | eventos sem defeito estrutural / eventos | `TOKEN_VAZIO` |
| M2 | Rastreabilidade | eventos com evidência válida / eventos | `TOKEN_VAZIO` |
| M3 | Integridade | hashes verificados / hashes declarados | `TOKEN_VAZIO` |
| M4 | Reprodutibilidade | validações repetíveis / validações | `TOKEN_VAZIO` |
| M5 | Resolução de lacunas | vazios resolvidos / vazios totais | `TOKEN_VAZIO` |
| M6 | Lead time de vazio | resolução − abertura | `TOKEN_VAZIO` |
| M7 | DPMO | defeitos / oportunidades × 1.000.000 | `TOKEN_VAZIO` |

## Mapa de riscos

| Risco | Controle preventivo | Controle detectivo | Resposta |
|---|---|---|---|
| conclusão sem prova | `claim_allowed=false` | validador + revisão | converter em `TOKEN_VAZIO` |
| alteração sem origem | campos obrigatórios | auditoria do ledger | bloquear publicação |
| hash falso ou inválido | formato estrito | recomputação local | evento `CORRECT` |
| exposição de segredo | minimização | varredura de conteúdo | revogar e retirar acesso |
| cadeia quebrada | `previous_event_id` | validação sequencial | reparar por evento corretivo |
| excesso de burocracia | ação mínima verificável | métrica de lead time | simplificar controle |
| automação sem benefício | hipótese mensurável | comparação antes/depois | rollback |

## Roadmap por ondas

### Onda 1 — `Mapa`

- governança, biblioteconomia, índices e scripts;
- objetivo: provar o método no repositório orquestrador.

### Onda 2 — repositórios de infraestrutura

- Termux, RafGitTools, Vectras/QEMU;
- foco: build, artefato, versão, proveniência e segurança.

### Onda 3 — repositórios científicos

- RLL, papers e datasets;
- foco: fonte, experimento, parâmetros, resultado, falsificadores e claim.

### Onda 4 — acervo filosófico e simbólico

- CientiEspiritual, Livro Vivo e correlatos;
- foco: autoria, versão, remissivas e marca `SIMBOLICO`, sem falsa equivalência experimental.

## Próximo passo verificável

Executar o validador sobre o ledger piloto, registrar o primeiro baseline e abrir
um evento por defeito observado. Qualquer métrica ainda não medida permanece
`TOKEN_VAZIO`.
