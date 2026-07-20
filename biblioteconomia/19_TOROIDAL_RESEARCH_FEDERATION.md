# Federação do Ciclo de Pesquisa Toroidal

## Função do Mapa

O `Mapa` não executa a ciência nem redefine o contrato canônico. Ele registra:

- qual repositório possui autoridade sobre cada camada;
- qual contrato é canônico e em qual commit foi observado;
- quais adaptadores existem;
- quais permanecem `ADAPTER_PLANNED` ou `TOKEN_VAZIO`;
- dependências e critérios objetivos de saída.

## Invariante

```text
RafGitTools -> contrato e governança
Mapa        -> autoridade, dependência e maturidade
RLL         -> ciência e falsificadores
RafPolimata -> roteamento e execução
Termux      -> prova no dispositivo
llama       -> memória e consumo de claims delimitadas
```

Uma relação entre repositórios não transfere autoridade. O `Mapa` aponta para a
fonte; não copia a conclusão.

## Estados

- `ACTIVE`: artefato e evidência observados;
- `ADAPTER_PLANNED`: caminho definido, arquivo ainda não materializado;
- `TOKEN_VAZIO`: prova ou adaptador ainda não localizado.

Todo estado não ativo exige critérios de saída. O registro permanece
`claim_allowed=false`, porque ele descreve infraestrutura e não confirma uma
teoria física externa.

## Estado material em 2026-07-20

```text
GOVERNANCE     ACTIVE  RafGitTools PR #279 / bed562a2...
MAP            ACTIVE  Mapa PR #33
SCIENCE        ACTIVE  RLL PR #583 / 8251a7fc... / 4 gates remotos PASS
ORCHESTRATION  ACTIVE  RafPolimata PR #152 / 2a3d1534... / 13 testes locais PASS
RUNTIME        TOKEN_VAZIO
MEMORY         TOKEN_VAZIO
```

Os runs remotos do `Mapa` e do `RafPolimata` terminaram sem steps e sem logs.
Eles são classificados como `ZERO_STEP_NO_LOGS`, não como falha demonstrada dos
validadores. O RLL, por outro lado, executou quatro gates remotos com sucesso.

A federação está estruturalmente materializada em quatro autoridades. A prova em
dispositivo e o adaptador consumidor de memória continuam abertos com critérios
de saída explícitos.
