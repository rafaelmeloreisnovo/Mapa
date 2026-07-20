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
