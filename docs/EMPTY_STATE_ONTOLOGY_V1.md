# EMPTY STATE ONTOLOGY V1 — Vazio, Nada e Invisível

**Data:** 2026-09-29  
**Estado inicial:** MATERIALIZED_UNTESTED  
**Autoridade:** `Mapa` governa semântica/manifold; fontes produtoras continuam governando evidência de domínio.  
**claim_allowed:** `false`

## Objetivo

Evitar que palavras visualmente próximas — “vazio”, “nada”, “invisível”, “zero”, “null”, “ausente”, “desconhecido” — colapsem em um único estado.

A ontologia possui 13 tipos:

`TOKEN_VAZIO`, `VOID`, `NOTHING_ABSOLUTE`, `INVISIBLE`, `ABSENCE`, `SILENCE`, `ZERO`, `EMPTY_SET`, `NULL`, `UNKNOWN`, `UNOBSERVED`, `SHADOW`, `LIMIT`.

## Invariantes principais

[
TOKEN\_VAZIO \neq 0 \neq \varnothing \neq NULL
]

[
UNOBSERVED \neq ABSENCE
]

[
INVISIBLE \neq NONEXISTENT
]

[
SILENCE \neq NO\_SOURCE
]

[
SHADOW \neq UNIQUE\_CAUSE
]

[
LIMIT \neq ABSENCE
]

[
VOID \neq NOTHING\_ABSOLUTE
]

## Centro Ω8

A expressão histórica:

[
CENTER=TOKEN\_VAZIO
]

é preservada como **representação**. Esta versão adiciona uma tipagem semântica:

[
CENTER.semantic\_type=VOID
]

Isso não reescreve o predecessor. `TOKEN_VAZIO` continua sendo o marcador de serialização; `VOID` descreve o estado estrutural “posição existente, intencionalmente sem conteúdo atribuído”.

## Vazio

`VOID` significa que existe uma posição estrutural declarada, mas ela está intencionalmente sem conteúdo. Isso exige prova da existência da posição e da política de não atribuição.

`TOKEN_VAZIO` é diferente: é um marcador epistêmico usado para impedir promoção/invenção quando o valor não está determinado ou autorizado.

## Nada

`NOTHING_ABSOLUTE` é tratado somente como conceito-limite metafísico. A ontologia não fornece operador que o promova a conclusão empírica.

[
NOTHING\_ABSOLUTE \not\Rightarrow ABSENCE
]

e também:

[
VOID,\ \varnothing,\ 0,\ NULL \not\Rightarrow NOTHING\_ABSOLUTE
]

## Invisível

`INVISIBLE` significa “não diretamente observável no canal declarado”. Pode existir evidência indireta, mas:

[
efeito\ observado \not\Rightarrow causa\ única
]

`SHADOW` registra justamente o caso de proxy, traço, oclusão ou efeito observável que restringe hipóteses sem identificar uma única causa.

## Ausência, silêncio e não-observado

`UNOBSERVED`: a observação relevante não foi feita ou não está disponível.

`ABSENCE`: algo esperado não foi detectado num escopo, método, janela e limiar declarados.

`SILENCE`: nenhum sinal/mensagem/evento qualificante foi detectado num canal e janela declarados.

Assim:

[
UNOBSERVED \neq ABSENCE \neq SILENCE
]

Uma transição `UNOBSERVED → ABSENCE` só pode ocorrer depois de observação efetiva, modelo de detecção declarado e resultado negativo limitado ao escopo.

## Zero, conjunto vazio e NULL

`ZERO` é valor numérico.

`EMPTY_SET` é objeto matemático com cardinalidade zero.

`NULL` é sentinel de modelo de dados definido por schema/provedor.

Nenhum deles é automaticamente equivalente aos outros.

## UNKNOWN

`UNKNOWN` afirma que o valor ou verdade não está determinado. Não afirma se houve observação.

[
UNKNOWN \neq UNOBSERVED
]

## LIMIT

`LIMIT` marca uma fronteira matemática, observacional, computacional ou epistêmica. A existência de uma fronteira não prova ausência além dela.

## Projeção Ω8

A ontologia aplica as oito direções como operadores metodológicos, não como equivalência cultural:

- **N / invariante:** preservar identidade dos tipos;
- **NE / adaptação:** transições exigem regras explícitas;
- **E / função:** usar a semântica operacional correta;
- **SE / conexão:** ligar estado a fonte/schema/evidência;
- **S / partilha:** serializar sem colapso semântico;
- **SW / evidência:** aplicar gate específico;
- **W / contexto:** preservar escopo, método, canal, janela e schema;
- **NW / ecossistema:** propagar tipos respeitando autoridade e rollback.

## Gap preservado

`ONTO-GAP-001`: não existe ponte operacional desta ontologia entre `NOTHING_ABSOLUTE` e um claim empírico/computacional.

Esse gap não deve ser “fechado” pela mera presença de um campo vazio.

## Reprodução

```bash
python3 tools/validate_empty_state_ontology.py
python3 -m unittest tests.test_empty_state_ontology
```

## R3

F_ok = tipos, distinções, transições, Ω8 e gates definidos.  
F_gap = ponte metafísica→empírica permanece TOKEN_VAZIO; aplicação em domínios concretos exige produtor/evidência.  
F_next = ligar este registry ao manifold canônico e executar CI/adversarial tests.
