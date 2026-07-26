# Índices de consolidação transversal

Esta área registra leituras que cruzam múltiplas fontes sem confundir soma bruta, objeto único, autoridade canônica e capacidade executada.

## X0 + home + Google Drive — 2026-07-25

- [`X0_HOME_DRIVE_CONSOLIDATION_2026-07-25.md`](X0_HOME_DRIVE_CONSOLIDATION_2026-07-25.md): análise, mitigação e riscos remanescentes.
- [`X0_HOME_DRIVE_MANIFEST_2026-07-25.json`](X0_HOME_DRIVE_MANIFEST_2026-07-25.json): estado legível por máquina, fontes, contagens, gates e `TOKEN_VAZIO`.
- [`DRIVE_ANALOG_SOURCE_REGISTRY_2026-07-25.json`](DRIVE_ANALOG_SOURCE_REGISTRY_2026-07-25.json): nomes exatos, fontes análogas, menções de inventário e gate de promoção sem substituição automática.

## RAFAELIA Anchor Loop — 2026-07-26

- [`RAFAELIA_ANCHOR_LOOP_AUTHORITY_2026-07-26.md`](RAFAELIA_ANCHOR_LOOP_AUTHORITY_2026-07-26.md): correção canônica da intenção histórica, fronteira fechada, ciclo e gates.
- [`RAFAELIA_ANCHOR_LOOP_AUTHORITY_2026-07-26.json`](RAFAELIA_ANCHOR_LOOP_AUTHORITY_2026-07-26.json): autoridades por plano, commits observados, invariantes e lacunas runtime.

Invariante específica:

```text
loop infinito intencional
≠ busy loop
≠ processo órfão
≠ execução sem gate
```

O próximo ciclo é autorizado por `COMMIT`, não pelo tempo de espera.

## Invariante de contagem

```text
ocorrência observada
≠ objeto único
≠ artefato canônico
≠ componente executável
≠ capacidade validada
```

## Invariante de proveniência

```text
nome análogo
≠ mesmo conteúdo
≠ mesmo contrato
≠ autoridade canônica
≠ permissão de executar
```

Toda consolidação deve preservar:

- fonte e revisão observada;
- hash quando disponível;
- papel arquitetural;
- risco de sensibilidade;
- prova de build e runtime separadas;
- motivo explícito para cada `TOKEN_VAZIO`.
