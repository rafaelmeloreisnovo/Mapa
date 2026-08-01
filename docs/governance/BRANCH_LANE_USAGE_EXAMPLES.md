# Exemplos de uso das lanes `main_##`

## Exemplo A — novo documento recebido do Drive

1. `main_01_intake_fontes`: registrar ID, revisão, origem, horário e cadeia de custódia.
2. `main_02_normalizacao`: normalizar nome, metadados e schema; deduplicar.
3. `main_03_modelagem_semantica`: conectar conceitos, claims e rotas.
4. `main_04_validacao`: validar schema, links, invariantes e casos adversariais.
5. `main_05_evidencias`: produzir hashes, receipt e pacote reproduzível.
6. `main_06_integracao`: ligar ao catálogo, Mapa e repositórios produtores.
7. `main_07_seguranca_conformidade`: verificar privacidade e exposição.
8. `main_08_observabilidade_release`: medir cobertura e decidir promoção.
9. `main_09_memoria_arquivo`: registrar checkpoint append-only após decisão.

A passagem entre etapas é uma passagem de responsabilidade e evidência; não exige merge sequencial entre as branches.

## Exemplo B — correção urgente

- A correção nasce em branch curta derivada de `main`.
- `main_00_governanca` define autoridade e escopo.
- `main_04_validacao` registra teste de regressão e falsificador.
- `main_05_evidencias` registra receipt.
- A PR retorna diretamente para `main` com autorização humana.
- `main_09_memoria_arquivo` registra o fechamento.

## Exemplo C — hipótese científica

- A hipótese entra por `main_01_intake_fontes`.
- A formulação tipada pertence a `main_03_modelagem_semantica`.
- Testes e comparação com dados pertencem a `main_04_validacao`.
- Resultados, hashes e ambiente pertencem a `main_05_evidencias`.
- Segurança/conformidade não promove verdade científica; apenas controla risco.
- Sem evidência suficiente: `claim_state=TOKEN_VAZIO` ou `HIPOTESE`.

## Anti-padrões proibidos

- usar `main_09_memoria_arquivo` como depósito de arquivos sem proveniência;
- considerar a numeração como prova de maturidade;
- fazer merge automático de `main_08` para `main`;
- copiar o mesmo conteúdo para todas as lanes;
- manter branches de trabalho indefinidamente;
- declarar sucesso porque o workflow não encontrou erro;
- renomear `main` para acomodar a arquitetura.
