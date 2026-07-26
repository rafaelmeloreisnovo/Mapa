# Roadmap DMAIC — Sessão das quatro tintas e memória vetorial

```yaml
programa: C09-FOUR-INKS-MEMORY-DMAIC
state: DEFINE_COMPLETE_MEASURE_READY
claim_allowed: false
sigma_level: TOKEN_VAZIO
certification: TOKEN_VAZIO
baseline_window: TOKEN_VAZIO
```

## DEFINE

### Problemas

1. demonstração, convenção, hipótese e parábola misturadas;
2. string convertida em número antes da tipagem;
3. vazio material confundido com ausência semântica;
4. matriz 7x6 promovida de convenção para ontologia;
5. ruído tratado como sinal sem reprodução;
6. recorrência de forma confundida com identidade histórica;
7. nome usado como conhecimento sem testemunho;
8. lacuna apagada em vez de preservada;
9. código observado promovido a execução;
10. hipótese 40–45% promovida sem payload/digest;
11. erro físico usado como dado sem classificação;
12. pointer do Mapa envelhecido em relação ao produtor.

### CTQs — requisitos críticos de qualidade

- tinta correta;
- tipo declarado;
- owner canônico único;
- source ref/path/blob;
- relação sem alvo órfão;
- falsificador;
- promoções proibidas;
- próximo passo;
- `claim_allowed=false`;
- `TOKEN_VAZIO` com gate e artefato esperado.

## MEASURE

### Métricas estruturais iniciais

| ID | Métrica | Fórmula | Estado inicial esperado |
|---|---|---|---|
| `FI-M1` | completude | registros completos / registros | medir em CI |
| `FI-M2` | compatibilidade de tinta | tinta-estado válidos / registros | medir em CI |
| `FI-M3` | relações válidas | relações com alvo / relações | medir em CI |
| `FI-M4` | falsificabilidade | vetores com falsificador / vetores | medir em CI |
| `FI-M5` | vazios acionáveis | vazios com gate e artefato / vazios | medir em CI |
| `FI-M6` | evidência fixada | demonstrações com refs / demonstrações | medir em CI |
| `FI-M7` | prevenção de promoção | mutações inválidas rejeitadas / mutações de teste | medir em testes |
| `FI-M8` | drift de pointer | pointers sincronizados / pointers | medir no Mapa |
| `FI-M9` | lead time de vazio | resolução - abertura | `TOKEN_VAZIO` |
| `FI-M10` | DPMO | defeitos / oportunidades x 1.000.000 | `TOKEN_VAZIO` até janela estável |
| `FI-M11` | nível sigma | convenção aprovada em processo estável | `TOKEN_VAZIO` |

Não publicar DPMO ou sigma a partir de uma única execução, jobs sem steps ou fixtures
construídas para passar.

## ANALYZE

### Estratificação

- por tinta;
- por prioridade;
- por owner;
- por tipo de objeto;
- por origem: sessão, papers, RLL, Mapa ou Vectras;
- por falha: ausência, ambiguidade, contradição, drift ou bloqueio operacional.

### Ferramentas

- Pareto somente após amostra suficiente;
- 5 Porquês para repetição de promoção indevida;
- Ishikawa para split-brain de autoridade;
- matriz risco x frequência x impacto x verificabilidade;
- teste de hipótese para benefícios da grade 7x6;
- análise de sobrevivência para tempo de fechamento de `TOKEN_VAZIO` somente quando houver série.

## IMPROVE

### Onda I — realizada nesta PR

- fonte autoral preservada;
- ledger vetorial no `papers`;
- schema fechado;
- validador fail-closed;
- testes de regressão;
- cinco pointers no `Mapa`;
- contrato C09 e rota federada;
- CI de produtor e consumidor.

### Onda II — código e memória

- corrigir zeroing de `LayersBit` por `sizeof`;
- criar full export opcional com digest;
- substituir alocação por buffers ping-pong onde apropriado;
- admission policy com eviction, emergency slots e receipt;
- separar consenso total de conflito triplo;
- schema de observação de desgaste físico.

### Onda III — recuperação

- máscaras 0, 10, 20, 30, 40 e 45%;
- padrões aleatórios, contíguos, anel e adversariais;
- centralidade e vizinhança;
- reconstrução de payload;
- digest original;
- preservação de negativos.

### Onda IV — memória de projeto

- manifest integral de fontes autorizadas;
- transcript selado quando permitido;
- hashes SHA-256/BLAKE3;
- pointers Drive por ID/revisão;
- política de privacidade e minimização;
- reentrada entre sessões.

## CONTROL

- CI em produtor e control plane;
- hashes de entradas quando checkout ocorrer;
- histórico append-only;
- detecção de drift por ref e blob;
- revisão periódica do vocabulário;
- exceções registradas;
- rollback por commit/evento corretivo;
- `TOKEN_VAZIO` com prioridade e próxima ação;
- nenhum `CLAIM_ALLOWED` automático.

## Critérios de promoção

| Estado atual | Promoção | Evidência mínima |
|---|---|---|
| `SIMBOLICO` | permanece simbólico | uso didático rastreado |
| `CONVENCAO` | contrato adotado | schema, versão, testes e owner |
| `HIPOTESE` | `VERIFIED_LIMITED` | protocolo, execução, negativos e falsificador sobrevivente |
| `CODE_OBSERVED` | `TESTED_LOCAL` | comando, ambiente, exit code e receipt |
| `TOKEN_VAZIO` | `RESOLVED` | artefato esperado e evento de fechamento |

## Próxima execução verificável

1. observar os runs de CI;
2. distinguir falha de conteúdo de job sem steps;
3. se houver steps, ler logs e corrigir regressões reais;
4. gerar baseline estrutural;
5. manter sigma e claims fortes em `TOKEN_VAZIO`.
