# Workflow de Varredura Operacional

## Objetivo

Executar varredura coerente dos ativos e transformar resultados em unidades documentadas,
rastreáveis e repetíveis.

## Etapas

1. Coletar entrada.
2. Registrar origem.
3. Classificar tipo.
4. Marcar estado.
5. Criar ligação com itens relacionados.
6. Definir ação mínima.
7. Executar ou encaminhar.
8. Validar resultado.
9. Atualizar índice.
10. Registrar próxima ação.

## Tipos de entrada

conversa, arquivo, imagem, banco, zip, pasta, commit, log, documento e resultado manual.

## Saída mínima

- id
- origem
- tipo
- estado
- relacionados
- ação
- resultado
- lacunas
- próxima ação

## Implementação executável — Parte 1

O procedimento manual possui agora uma implementação `stdlib-only`:

```text
tools/repository_gap_mapper.py
```

Contrato:

```text
schemas/repository-gap-map.schema.json
```

Documentação operacional:

```text
docs/REPOSITORY_GAP_MAPPER.md
```

Teste e geração de evidência:

```text
.github/workflows/repository-gap-map.yml
tests/test_repository_gap_mapper.py
```

### Fluxo executável

```text
raízes locais
  -> enumeração determinística
  -> classificação por extensão/magic bytes
  -> SHA-256
  -> marcadores de lacuna
  -> referência textual em Gradle/CMake/Meson/Make
  -> JSON canônico
  -> Markdown de ação
```

### Comando mínimo

```bash
python3 tools/repository_gap_mapper.py \
  --root projeto=. \
  --output-json resultados/REPOSITORY_GAP_MAP.json \
  --output-md resultados/REPOSITORY_GAP_MAP.md \
  --fail-on none
```

### Comando multirrepositório

```bash
python3 tools/repository_gap_mapper.py \
  --root Vectras=../Vectras-VM-Android \
  --root qemu=../qemu_rafaelia \
  --root termux=../termux-app-rafacodephi \
  --root rafgit=../RafGitTools \
  --root androidx=../androidx_RmR \
  --output-json resultados/ECOSYSTEM_GAP_MAP.json \
  --output-md resultados/ECOSYSTEM_GAP_MAP.md
```

## Invariante de interpretação

```text
arquivo existe        != integrado
integrado ao build    != compilado
compilado             != empacotado
empacotado            != instalado
instalado             != executado
executado             != validado
```

A varredura produz mapa e prioridade. Ela não transforma ausência de prova em prova.

## Critério de parada

Parar quando houver uma entrega documentada ou uma lacuna protegida por:

- identificador estável;
- origem registrada;
- owner definido;
- próxima ação concreta;
- estado de evidência explícito.

```text
claim_allowed=false enquanto a cadeia de prova permanecer aberta
```
