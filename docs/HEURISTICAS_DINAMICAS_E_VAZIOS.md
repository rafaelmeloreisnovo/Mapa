# Heurísticas de Dinâmicas Estruturais e Vazios

## Princípio

As heurísticas localizam candidatos, anomalias, pontes, ausências e trajetórias.
Elas não autorizam conclusão científica:

\[
h(x)\rightarrow candidato,
\qquad
h(x)\not\rightarrow prova
\]

## Catálogo executável

| Heurística | Detecta | Saída conservadora |
|---|---|---|
| `H-DEF` | termo sem definição, unidade ou contraexemplo | `TV-DEF` |
| `H-PROVENANCE` | origem, caminho, commit ou dataset ausente | `TV-PROVENANCE` |
| `H-EVIDENCE` | estado promovido sem evidência | bloquear ou rebaixar estado |
| `H-FALSIFIER` | causalidade sem teste destrutivo | `TV-TEST` |
| `H-GAP-CLASS` | `TOKEN_VAZIO` sem classe | classificar antes de agir |
| `H-GAP-REASON` | vazio sem motivo | registrar ausência real |
| `H-DEAD-END` | vazio/tema sem próximo gate | criar ação verificável ou fechamento honesto |
| `H-SPECIAL-STATUS` | abortado, ignorado, potencial etc. sem motivo | registrar decisão e contexto |
| `H-CENSORSHIP` | alegação de censura sem prova documental | rebaixar para `WITHHELD/NOT_FOUND` |
| `H-EMPTY-NOT-ZERO` | desconhecido codificado como zero | máscara de validade/`TOKEN_VAZIO` |
| `H-BOUNDARY` | relação sem domínio, tempo, língua ou escala | `TV-BOUNDARY` |
| `H-RECON` | reversão sem métrica de reconstrução | `TV-RECON` |
| `H-LOOP` | recursão sem critério de saída | `TV-LOOP` |
| `H-DERIVATIVE` | derivada sem eixo/unidade/espaçamento | bloquear interpretação |
| `H-ANTIDERIVATIVE` | antiderivada sem origem/constante | preservar família de soluções |
| `H-LOGLOG` | reta log-log sem domínio positivo e alternativas | comparar modelos concorrentes |
| `H-NESTED-LOG` | `log(log(x))` sem finalidade e domínio | `TV-DOMAIN` |
| `H-INDEPENDENCE` | fontes com mesma linhagem | não contar como replicações independentes |

## Temas interrompidos ou escondidos pelo fluxo

### `ABORTED`

Significa que havia uma intenção de execução, mas ela foi encerrada. Deve registrar:

- razão;
- risco ou condição que interrompeu;
- responsável ou `TOKEN_VAZIO_OWNER`;
- se é reversível;
- evidência necessária para reabrir.

### `IGNORED`

Significa que o tema existia, mas ficou fora da prioridade. Não implica má-fé.
A heurística procura temas com alta conectividade ou muitos dependentes que
continuam sem próximo gate.

### `POTENTIAL`

É possibilidade útil, ainda não validada. Exige hipótese, baseline, falsificador
e proibição explícita de claim prematuro.

### `SUGGESTED`

É uma ação proposta. Deve possuir custo, risco, ganho informacional esperado e
dono; caso contrário vira uma lista infinita de desejos.

### `WITHHELD`

A informação pode existir, mas está retida por privacidade, permissão, contrato
ou limitação de acesso. Não equivale a inexistência ou censura.

### `CENSORED`

Só pode ser usado com evidência de remoção/supressão deliberada e origem da
decisão. Sem isso, o estado correto é `WITHHELD`, `NOT_FOUND` ou `TOKEN_VAZIO`.

## Trajetórias paralelas

O motor agrupa registros por trajetória e procura tags comuns. Uma ponte entre
neurociência, semântica, governança e estatística recebe sempre:

```text
METHODOLOGICAL_BRIDGE_NOT_PHYSICAL_EQUIVALENCE
```

Isso permite aprender com formas comuns — estado oculto, observável incompleto,
incerteza, proveniência — sem declarar que cérebro, plasma, clima e software são
o mesmo mecanismo.

## Paradoxos como detectores

- repetição reduz surpresa e pode aumentar significado;
- compressão reduz tamanho e pode destruir topologia;
- mais dados com má proveniência aumentam incerteza;
- hash prova integridade e não prova verdade;
- automação aumenta eficiência e pode reduzir auditabilidade;
- norma preserva estabilidade e pode impedir evolução;
- vazio reduz conclusão imediata e aumenta honestidade futura.

Cada paradoxo deve gerar uma pergunta operacional, não uma conclusão ornamental.

## Priorização futura

Uma ação candidata pode ser avaliada por:

\[
F_{next}(a)=
\frac{EIG(a)\,O(a)\,I_d(a)\,T_r(a)\,R_p(a)}
{C(a)+R_c(a)+R_s(a)+L(a)}
\]

Os pesos permanecem `TOKEN_VAZIO_CALIBRATION`. A fórmula é um contrato de
fatores, não uma pontuação pronta.
