# Perfis de mecanismos dos repositórios

Este diretório contém **sobreposições epistemicamente marcadas** sobre o inventário de identidade do GitHub.

O nome de um repositório não prova sua finalidade, arquitetura ou funcionamento. Por isso, o construtor parte de uma regra conservadora:

```text
identidade observada pelo conector = FATO
mecanismo ainda não lido          = TOKEN_VAZIO
```

## Estrutura

```text
data/mechanisms/
├── README.md
└── profiles/
    └── <owner>__<repository>.json
```

Cada perfil pode preencher somente estes campos:

- `purpose`
- `inputs`
- `transformations`
- `outputs`
- `interfaces`
- `invariants`
- `quality_controls`
- `risks`
- `relations`
- `philosophical_context`
- `visual_model`

## Estados epistêmicos

| Estado | Uso |
|---|---|
| `FATO` | afirmação diretamente sustentada por evidência localizável |
| `HIPOTESE` | interpretação testável, com confiança inferior a 1 |
| `PARABOLA` | linguagem simbólica explicitamente separada de prova |
| `TOKEN_VAZIO` | conhecimento ausente, com próxima ação e critério de saída |

Um `TOKEN_VAZIO` não pode conter `value` nem `evidence`: isso impede que uma alegação seja escondida dentro de uma lacuna.

## Fluxo de promoção

1. Ler arquivos estáveis ou um commit fixado do repositório-alvo.
2. Limitar o `claim_scope` ao que a evidência realmente sustenta.
3. Registrar o campo no perfil.
4. Executar o construtor e o validador.
5. Revisar a diferença visual e somente então promover o perfil.

```bash
python3 scripts/build_living_system_index.py --write
python3 scripts/validate_living_system_index.py
python3 -m unittest tests/test_living_system_index.py -v
```

A ausência é dado vivo; a promoção exige prova.
