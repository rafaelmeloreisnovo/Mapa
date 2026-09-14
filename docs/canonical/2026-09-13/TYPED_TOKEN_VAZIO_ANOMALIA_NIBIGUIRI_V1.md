# RAFAELIA — TOKEN_VAZIO tipado · Anomalia Sistêmica · Nibiguiri V1

Status: DRAFT_AUDITABLE  
Data: 2026-09-13  
claim_allowed=false

## 1. Intenção

Separar formas diferentes de ausência, descarte, interrupção, anomalia e recuperação sem converter lacuna em zero e sem atribuir causas invisíveis.

Invariantes:

`TOKEN_VAZIO != 0`  
`SOURCE != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM`  
`TOKEN_ID != OCCURRENCE_ID != SENSE_VERSION != CLAIM`  
`AUSÊNCIA != CENSURA`  
`NÃO_SELECIONADO != PESO_OCULTO`  
`ANOMALIA_LOCAL != ANOMALIA_SISTÊMICA`

## 2. TOKEN_VAZIO como gênero

`TOKEN_VAZIO` continua sendo o estado-raiz para informação necessária não determinada.

A regra nova é tipar a causa observável sem colapsar estados diferentes:

- `TOKEN_VAZIO_NOT_OBSERVED`: execução/fato necessário não observado.
- `TOKEN_VAZIO_BASELINE`: baseline necessário ausente.
- `TOKEN_VAZIO_SEMANTIC`: significado/regra não vinculado.
- `TOKEN_VAZIO_CAUSE_UNKNOWN`: efeito/ausência observada, causa não demonstrada.
- `TOKEN_VAZIO_CENSORSHIP_CAUSE`: hipótese de supressão sem evidência suficiente.
- `TOKEN_VAZIO_PROVIDER_INTERNALS`: mecanismo interno/peso/seleção não exposto pelo provedor.
- `TOKEN_VAZIO_SEMANTIC_NUMERIC_ROUTE`: relação numérica autoral preservada sem completar regra ausente.

Esses tipos são estados epistemológicos; não são valores aritméticos.

## 3. TOKEN_ANOMALIA_SISTEMICA com sinal

Para uma medida `x`, baseline `b` e escala positiva `s`:

`A = (x - b) / s`, com `s > 0`.

- `A < 0`: desvio abaixo do baseline.
- `A = 0`: coincide com o baseline escolhido.
- `A > 0`: desvio acima do baseline.

O sinal é direção, não qualidade moral, não prova de falha e não evidência negativa.

Se `b` ou `s` não estiverem vinculados, o valor numérico de `A` permanece `TOKEN_VAZIO_BASELINE`.

A palavra **sistêmica** só é promovida quando a anomalia atravessa componentes/rotas com relação observada. Caso contrário, registrar `ANOMALIA_LOCAL`.

## 4. TOKEN_NIBIGUIRI

`TOKEN_NIBIGUIRI` é um contêiner autoral de **recuperação**. Ele não afirma que o material recuperado é verdadeiro nem que houve censura.

Forma mínima:

`N_i = <source, state, reason/evidence, gap, next>`

Estados tipados:

| Estado | Regra |
|---|---|
| `NIBIGUIRI:IGNORADO` | fonte observada, candidato não promovido; motivo separado |
| `NIBIGUIRI:ESQUECIDO_OU_DESINDEXADO` | existência anterior rastreável, ponteiro/índice ativo perdido |
| `NIBIGUIRI:ABORTADO` | rota iniciada e interrompida antes do fechamento |
| `NIBIGUIRI:CENSURA_EVIDENCIADA` | somente com política/ação/bloqueio observável |
| `NIBIGUIRI:FILTRO_PESO_EVIDENCIADO` | somente com score/threshold/receipt observável |
| `NIBIGUIRI:OBVIO_NAO_INDEXADO` | relação formal verificável ausente do índice |
| `NIBIGUIRI:CAUSA_DESCONHECIDA` | ausência/não promoção observada; causa preservada vazia |

### Regra de segurança epistemológica

`CENSURADO` sem evidência -> `TOKEN_VAZIO_CENSORSHIP_CAUSE`.  
`PESO_DESCARTOU` sem score/trace observável -> `TOKEN_VAZIO_PROVIDER_INTERNALS`.

## 5. Âncora geométrica: equilátero e o “óbvio não indexado”

Para triângulo equilátero de lado `a`:

`h = a cos(30°) = a sin(60°) = (sqrt(3)/2)a`

`a/2 = a sin(30°) = a cos(60°)`

`Area = (a h)/2 = (sqrt(3)/4)a^2`

A mediana traçada de um vértice é simultaneamente altura e bissectriz; divide o ângulo de `60°` em `30° + 30°`.

Os `15°` aparecem somente se houver **uma segunda bisseção de 30°**. Não pertencem automaticamente à primeira mediana.

`150 = 10 * 15` é uma relação de escala numérica; não é identidade geométrica com `15°` sem um operador definido.

A expressão autoral envolvendo `15`, `45`, `50`, `150` e “variação de 1” fica preservada como `TOKEN_VAZIO_SEMANTIC_NUMERIC_ROUTE` até a regra ser explicitada.

## 6. Escala de grandeza

Operador decimal:

`S_k(x) = 10^k x`.

Multiplicar por `100` equivale a `k=2`. A operação muda a escala numérica; equivalência física exige preservar unidades/normalização.

## 7. Polinômios e “área que não existe” literalmente

Produtos com fator negativo podem ser visualizados por **área algébrica orientada/sinalizada**, sem afirmar área física negativa.

Exemplo:

`(x-a)(x+b) = x^2 + (b-a)x - ab`.

O termo `-ab` pode ser desenhado como tile/área **assinada** para contabilidade algébrica. Isso é uma representação de sinais na álgebra, não uma área euclidiana positiva literal.

Regra:

`SIGNED_AREA_MODEL != PHYSICAL_AREA_CLAIM`.

Esse mecanismo é útil para reconstruir expansão de polinômios, cancelamentos e fatores negativos mantendo a geometria como linguagem auxiliar.

## 8. Operação de recuperação

Fluxo:

`OBSERVE -> TYPE -> BIND_SOURCE -> SEPARATE_CAUSE -> TEST -> RECOVER_OR_KEEP_TOKEN_VAZIO`

Não promover um item Nibiguiri apenas por recorrência ou plausibilidade.

## 9. R3

F_ok: taxonomia tipada de TOKEN_VAZIO, anomalia com sinal, Nibiguiri e âncoras geométrico-algébricas formalizadas sem converter ausência em causa.

F_gap: regra exata de 15/45/50/150 e “variação de 1”; qualquer alegação sobre pesos internos/censura sem receipt; calibração empírica de anomalia sistêmica.

F_next: criar fixtures determinísticos para classificação Nibiguiri e anomalia signed; validar que censura/peso desconhecidos caem em TOKEN_VAZIO e que a geometria 30-60-90 reproduz identidades formais.

