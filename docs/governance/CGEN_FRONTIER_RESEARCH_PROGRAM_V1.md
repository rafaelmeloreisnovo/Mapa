# CGEN V1 — Ciência da Governança Epistêmico‑Normativa

**Estado:** `PROPOSED_RESEARCH_PROGRAM / FORMALIZABLE / FALSIFIABLE / HUMAN_RIGHTS_BOUNDED / FAIL_CLOSED`

**Escopo:** governança de sistemas informacionais automatizados, IA, agentes e Robotics sob evidência, autoridade, direitos, normas, auditoria, proveniência, incerteza e contestabilidade.

**Aviso epistemológico:** `CGEN` é uma denominação autoral/proposta para um programa interdisciplinar. Não é apresentada como disciplina acadêmica já reconhecida, nem como substituta de Direito, Ciência da Computação, Estatística, Engenharia, Economia, Psicologia, Ergonomia, Auditoria ou Ética.

---

## 1. Problema de fronteira

Sistemas automatizados contemporâneos cruzam fronteiras que disciplinas isoladas tratam apenas parcialmente:

- uma decisão pode ser tecnicamente correta e juridicamente ilícita;
- uma operação pode ser juridicamente permitida e eticamente inadequada;
- uma política pode ser formalmente transparente e humanamente incompreensível;
- um modelo pode ser estatisticamente eficiente e distributivamente enviesado;
- um certificado pode ser válido e usado fora do seu escopo;
- um algoritmo pode estar implementado e nunca ter sido executado no ambiente alegado;
- uma execução pode existir sem produzir evidência suficiente para um claim;
- uma evidência pode ser verdadeira no tempo `t0` e obsoleta em `t1`;
- uma organização pode declarar governança enquanto seu runtime diverge da declaração.

A CGEN propõe tratar esses fenômenos como um único problema de **governança verificável de transições**.

A unidade mínima não é “o documento”, “o algoritmo” ou “a lei”. A unidade mínima é:

```text
NÓ + AUTORIDADE + ESTADO + TRANSIÇÃO + EVIDÊNCIA + INCERTEZA + FALSIFICADOR + RECIBO
```

---

## 2. Objeto científico

Defina um sistema governado como um grafo temporal dirigido:

\[
G_t=(V_t,E_t,\mathcal A_t,\mathcal P_t,\mathcal R_t)
\]

onde:

- `V_t` = nós: pessoas, dados, modelos, regras, instituições, contratos, certificados, decisões, artefatos e evidências;
- `E_t` = relações/transições;
- `A_t` = autoridade aplicável a cada transição;
- `P_t` = proveniência;
- `R_t` = direitos, riscos, restrições e remédios;
- `t` = tempo de observação, necessário para evitar que evidência antiga seja tratada como verdade atual.

Uma transição material `e_i` não é promovível apenas porque existe. Ela precisa de um envelope:

\[
\Gamma(e_i)=\langle origin,authority,purpose,input,transform,risk,rights,evidence,unknowns,rollback,receipt,time\rangle.
\]

### Invariante de promoção

```text
EXISTS != VALID
IMPLEMENTED != EXECUTED
EXECUTED != VERIFIED
VERIFIED != LEGALLY_AUTHORIZED
LEGAL_AUTHORITY != ETHICAL_ADEQUACY
CERTIFIED != UNIVERSALLY_COMPLIANT
CI_PASS != HUMAN_PROMOTION_AUTHORIZATION
```

---

## 3. Ontologia da verdade e da linguagem

A CGEN não aceita uma classe única chamada “verdade”. Cada enunciado recebe tipo epistemológico.

### 3.1 Tipos mínimos

- `OBSERVATION` — algo observado em fonte, runtime ou experimento;
- `DEFINITION` — convenção explícita;
- `LEGAL_RULE` — texto normativo vinculante dentro de escopo/jurisdição;
- `REGULATORY_GUIDANCE` — orientação de autoridade sem ser automaticamente lei;
- `TECHNICAL_STANDARD` — norma técnica com versão e escopo;
- `THEOREM` — proposição matemática com prova;
- `PROOF` — derivação válida sob premissas declaradas;
- `MODEL` — representação útil, não identidade com a realidade;
- `HYPOTHESIS` — proposição testável ainda não estabelecida;
- `EMPIRICAL_RESULT` — resultado observado sob protocolo;
- `ANOMALY` — observação que diverge do modelo/claim esperado;
- `PARADOX` — tensão aparente entre propriedades que exige decomposição conceitual;
- `FALSIFIER` — condição cuja observação derruba ou limita um claim;
- `TOKEN_VAZIO` — evidência ausente/insuficiente; estado válido, não zero e não falso.

### 3.2 Regra anti-colapso

```text
METAPHOR != MECHANISM
ANALOGY != PROOF
CORRELATION != CAUSATION
LEGAL_TEXT != IMPLEMENTATION
STANDARD_REFERENCE != CERTIFICATION
CERTIFICATE != RUNTIME_EVIDENCE
HYPOTHESIS != ACCUSATION_PROVED
```

---

## 4. Vetorização sem falsa precisão

Cada claim `c` é representado por vetor de evidência, não por uma porcentagem arbitrária:

\[
\mathbf e(c)=
(A,P,S,T,R,I,U,F)
\]

com:

- `A` = autoridade da fonte;
- `P` = qualidade da proveniência;
- `S` = aderência de escopo;
- `T` = atualidade temporal;
- `R` = reprodutibilidade;
- `I` = independência;
- `U` = incerteza explícita;
- `F` = força do falsificador/teste adversarial.

Por padrão, esses componentes **não são somados** em um escore único. Um documento oficial muito antigo pode dominar em `A` e falhar em `T`; um benchmark reproduzível pode dominar em `R` e não possuir autoridade jurídica. A comparação adequada é parcial/Pareto e dependente do claim.

### 4.1 Vetores de viés obrigatórios

Todo sistema Robotics deve considerar, quando aplicável:

```text
sampling_bias
measurement_bias
model_bias
interface_bias
legal_framing_bias
jurisdiction_bias
institutional_bias
economic_incentive_bias
automation_bias
confirmation_bias
survivorship_bias
unknown_bias = TOKEN_VAZIO
```

O objetivo não é pressupor que todo viés existe, mas impedir que ele desapareça por ausência de campo.

---

## PARTE II — INVARIANTE DOS DOIS PONTOS, OITO MOMENTOS E QUATRO EIXOS

## 5. Definição formal do par equidistante

Considere um centro `c ∈ R²` e um vetor não nulo `v`.

Defina dois pontos:

\[
p=c+v,\qquad q=c-v.
\]

Então:

\[
\|p-c\|=\|q-c\|=\|v\|,
\]

\[
p+q=2c.
\]

O par `(p,q)` é antipodal em relação a `c`.

Sob qualquer rotação ortogonal `R_θ` em torno de `c`:

\[
p_θ=c+R_θv,\qquad q_θ=c-R_θv,
\]

as distâncias continuam iguais, pois rotações preservam norma.

### Teorema 1 — Invariância equidistante sob rotação

Para todo `θ`,

\[
\|p_θ-c\|=\|q_θ-c\|.
\]

**Prova:** `R_θ` é ortogonal, portanto `||R_θv||=||v||`. O segundo ponto é o negativo do mesmo vetor rotacionado. QED.

Esse resultado é matemática elementar estabelecida; não depende de interpretação simbólica.

---

## 6. Vercípice: definição autoral auditável

Introduz-se o termo autoral **vercípice** apenas como abreviação operacional:

> `vercípice(c,v)` = classe do par antipodal `{c+v,c-v}` tratada como um único eixo recíproco quando orientação de sinal não é material ao problema.

O termo não é nomenclatura matemática padrão. O objeto subjacente é a classe de equivalência antipodal, que é matematicamente bem definida.

Defina:

\[
v\sim -v.
\]

Cada classe `[v]={v,-v}` representa um eixo não orientado.

---

## 7. Oito momentos que se reduzem a quatro eixos

Defina oito estados angulares:

\[
\theta_k=\theta_0+k\frac{\pi}{4},\quad k=0,\dots,7.
\]

E pontos complexos ou vetoriais:

\[
z_k=r e^{i\theta_k}.
\]

Como:

\[
z_{k+4}=-z_k,
\]

os oito estados orientados se agrupam em quatro pares antipodais:

```text
{0,4}
{1,5}
{2,6}
{3,7}
```

### Teorema 2 — Quociente 8→4

O quociente dos oito estados pela equivalência antipodal `z ~ -z` possui exatamente quatro classes.

Isto formaliza, sem metáfora, a passagem:

```text
8 momentos orientados -> 4 eixos recíprocos
```

Falsificador: se os oito estados não tiverem passo angular `π/4`, ou se a relação antipodal não for preservada, a redução específica `8→4` não é válida.

---

## 8. Dois quadrados e o octógono

Separe os índices pares e ímpares:

\[
S_0=\{z_0,z_2,z_4,z_6\},
\]

\[
S_1=\{z_1,z_3,z_5,z_7\}.
\]

Cada conjunto é um quadrado regular centrado em `c`, e:

\[
S_1=R_{\pi/4}S_0.
\]

A união dos oito vértices forma um octógono regular.

Assim, a leitura formal é:

```text
quadrado A
+ quadrado B rotacionado 45°
= 8 vértices alternados de um octógono regular
```

Isso é exato para raio comum e passo angular uniforme.

---

## PARTE III — ELEVAÇÃO 3D E O HEXÁGONO

## 9. Dois quadrados como faces opostas de um cubo

Considere o cubo:

\[
C=[-a,a]^3.
\]

As faces `z=+a` e `z=-a` são dois quadrados congruentes e paralelos — uma formalização direta da ideia de “ver a frente e as costas do quadrado”.

### 9.1 Corte central hexagonal

Considere o plano:

\[
\Pi:\;x+y+z=0.
\]

A interseção `C ∩ Π` tem os seis vértices:

\[
(a,-a,0),
(a,0,-a),
(0,a,-a),
(-a,a,0),
(-a,0,a),
(0,-a,a).
\]

Todos possuem distância `√2 a` do centro, e vértices consecutivos também estão separados por `√2 a`.

### Teorema 3 — Seção hexagonal regular do cubo

`C ∩ Π` é um hexágono regular de lado:

\[
s=\sqrt 2\,a.
\]

Sua área é:

\[
A_H=\frac{3\sqrt 3}{2}s^2=3\sqrt 3\,a^2.
\]

Esse resultado dá uma ponte geométrica rigorosa:

```text
2 faces quadradas opostas
→ cubo
→ plano central perpendicular à diagonal espacial
→ seção hexagonal regular
```

### Fronteira mecânica obrigatória

A frase “o hexágono é a área interna mais resistente em 3D” **não decorre** desse teorema.

Resistência mecânica depende de:

- material;
- espessura;
- tipo e direção de carga;
- condições de contorno;
- flambagem;
- ligações;
- defeitos;
- escala;
- critério de falha.

Portanto:

```text
REGULAR_HEXAGON_SECTION = PROVED_GEOMETRY
MECHANICAL_OPTIMALITY = TOKEN_VAZIO_HYPOTHESIS
```

Um claim de superioridade mecânica exigiria FEA/ensaio e comparação contra geometrias alternativas sob a mesma massa, material, volume e condições de contorno.

---

## PARTE IV — ESPIRAL, √3/2 E FIBONACCI

## 10. Separação obrigatória entre raio e ângulo

O Mapa já contém evidência de execução limitada para a recorrência radial:

\[
r_{n+1}=\frac{\sqrt3}{2}r_n,
\]

com consistência numérica contra sua forma fechada no harness registrado em `OMEGA_E1_STRUCTURAL_SPIRAL_ROUTE_20260822.v1.json`.

Logo:

```text
RADIAL √3/2 = PASS_NUMERIC_LIMITED
```

Entretanto, a fonte angular:

\[
\theta_{n+1}=\theta_n+\frac{\pi}{\varphi}
\]

não era a mesma lei angular executada pelo produtor `GAIA_phi` no recibo observado.

Logo:

```text
ANGULAR π/φ IMPLEMENTATION-EQUIVALENCE = FAIL_NOT_SAME_FORM
FULL RADIAL+ANGULAR CLAIM = TOKEN_VAZIO
```

A CGEN proíbe recombinar automaticamente uma metade validada com uma metade não validada.

---

## 11. Três leis angulares que não podem ser confundidas

### 11.1 Lei octante

\[
\Delta\theta_8=\frac{\pi}{4}.
\]

Serve para os oito momentos discretos e para a prova `8→4` por antipodalidade.

### 11.2 Lei autoral π/φ

\[
\Delta\theta_{\pi/\varphi}=\frac{\pi}{\varphi}.
\]

Permanece um objeto matemático perfeitamente definível, mas sua equivalência com implementação, fenômeno físico ou benefício de governança exige testes próprios.

### 11.3 Ângulo áureo clássico de filotaxia

\[
\Delta\theta_G=\frac{2\pi}{\varphi^2}.
\]

É outra lei. Não deve ser usada para “validar” `π/φ` por semelhança nominal.

Invariante:

```text
π/4 != π/φ != 2π/φ²
```

---

## 12. Fibonacci como recorrência, não como prova por aparência

A recorrência de Fibonacci é:

\[
F_{n+1}=F_n+F_{n-1},\qquad F_1=F_2=1.
\]

produzindo:

```text
1, 1, 2, 3, 5, 8, 13, ...
```

Um sistema pode usar `F_n` como índice de escala, peso, janela temporal, iteração ou amostragem. Contudo:

```text
visual_similarity_to_spiral != Fibonacci_derivation
pair_symmetry != Fibonacci_proof
hexagon != Fibonacci_consequence
```

Para ligar Fibonacci a um fenômeno Robotics real, é preciso declarar a variável observável e comparar a recorrência contra alternativas.

---

## PARTE V — CORRESPONDÊNCIA ENTRE GEOMETRIA E GOVERNANÇA

## 13. A parábola formal: dois pontos que se fiscalizam

A geometria pode servir como **modelo de arquitetura**, não como prova jurídica.

Associe os pontos antipodais a:

```text
P = poder de processar
Q = poder de contestar/verificar
```

A invariante desejada é que nenhum crescimento material em `P` ocorra sem crescimento correspondente em capacidade de governança `Q`.

Uma forma mensurável é definir vetores de capacidade:

\[
P_t=(collection,inference,decision,sharing,retention),
\]

\[
Q_t=(visibility,choice,contestability,portability,auditability).
\]

Não se exige igualdade numérica entre dimensões heterogêneas. Exige-se um **contrato de cobertura**: para cada capacidade material de `P`, deve existir controle, fundamento, evidência ou justificativa explícita em `Q`.

### Falsificador arquitetural

Se surgir uma capacidade material nova — por exemplo, inferência biométrica — sem nova análise de base legal, risco, informação, direitos e evidência, o sistema quebra a simetria de governança.

---

## 14. Oito momentos como ciclo de revisão

Os oito estados podem ser usados como um ciclo operacional autoral:

1. `ORIGIN` — origem/proveniência;
2. `AUTHORITY` — competência e base;
3. `PURPOSE` — finalidade/necessidade;
4. `PROCESS` — transformação/automação;
5. `IMPACT` — riscos, vieses, direitos;
6. `EVIDENCE` — teste/recibo/auditoria;
7. `CONTEST` — revisão humana/titular/contraditório;
8. `FEEDBACK` — correção e novo ciclo.

Por antipodalidade conceitual, quatro pares de controle:

```text
ORIGIN   ↔ IMPACT
AUTHORITY↔ EVIDENCE
PURPOSE  ↔ CONTEST
PROCESS  ↔ FEEDBACK
```

Esta pareação é uma **construção de design**, não teorema jurídico. Ela é útil se produzir maior rastreabilidade e pode ser falsificada por comparação com arquiteturas alternativas.

---

## PARTE VI — NORMAS, DIREITO E EVOLUÇÃO TEMPORAL

## 15. A norma como objeto versionado

Nenhuma referência normativa é armazenada apenas pelo nome.

Forma mínima:

```text
source_id
issuer/authority
authority_type
jurisdiction
number/version
publication/effective date
scope
status
supersedes/superseded_by
source URL
observed_at
impacted controls
falsifier/staleness trigger
```

### Eventos materiais observados em 2026

No snapshot de 26 de agosto de 2026, entre outros:

- a ANPD possui Resolução nº 32/2026 reconhecendo adequação da União Europeia para transferências internacionais;
- o ECA Digital (Lei 15.211/2025) está vigente desde 17 de março de 2026, conforme Lei 15.352/2026;
- o Mapa de Temas Prioritários ANPD 2026–2027 inclui direitos dos titulares, crianças/adolescentes, poder público e IA/tecnologias emergentes;
- a Agenda 2025–2026 inclui direitos dos titulares, RIPD, biometria, medidas mínimas de segurança, IA, tratamento de alto risco, governança e aferição de idade;
- em agosto–novembro de 2026 há período de adaptação/monitoramento de soluções de aferição de idade no plano de implantação do ECA Digital;
- o AI Act da União Europeia tem aplicação geral desde 2 de agosto de 2026, enquanto obrigações de determinados sistemas de alto risco foram postergadas no regime europeu de 2026;
- ISO/IEC 27701:2025 é a edição publicada atual de PIMS;
- ISO 14001:2026 substituiu a edição 2015;
- ISO/IEC 42001:2023 permanece referência publicada para sistema de gestão de IA.

Esses fatos não são eternos. O registro `robotics-normative-evolution.v1.json` existe para reabrir gates quando mudarem.

---

## 16. Não regressão normativa

Defina `B_t` como baseline de direitos/controles sustentados no instante `t`.

Uma mudança `Δ` só pode ser promovida se:

1. não remover silenciosamente direito ou controle já aplicável;
2. não rebaixar evidência (`VERIFIED → ASSUMED`) sem registro explícito;
3. não apagar `TOKEN_VAZIO`;
4. não ampliar finalidade sem novo gate;
5. não ampliar destinatários/transferências sem análise de impacto;
6. não reaproveitar certificado fora do escopo;
7. não tratar norma substituída como corrente;
8. preservar recibo histórico append-only;
9. possuir rollback quando tecnicamente possível;
10. possuir justificativa jurídica quando rollback não for permitido por obrigação legal.

Formalmente:

\[
Promote(\Delta)=1
\]

somente se os invariantes aplicáveis permanecem verdadeiros após `Δ` e todos os novos desconhecidos críticos estão resolvidos ou bloqueiam a promoção.

---

## 17. Proveniência como cadeia causal mínima

Para qualquer claim `c`:

\[
Provenance(c)=source\to extraction\to interpretation\to implementation\to execution\to evidence\to claim.
\]

Qualquer aresta ausente é `TOKEN_VAZIO`, não inferência automática.

### Antiderivada de proveniência

Em linguagem operacional, a “antiderivada” é o acúmulo temporal de exposições e decisões:

\[
X(T)=\int_0^T r(t)\,dt.
\]

É um modelo de acumulação. Só deve ser calculado se `r(t)` tiver definição/unidade mensurável. Caso contrário, a integral permanece representação conceitual.

### Derivada inversa operacional

Um resultado adverso `y` deve poder ser rastreado de volta a:

```text
output -> model/rule version -> input/provenance -> purpose -> authority -> controller -> receipt
```

Se a trilha quebrar, `ROOT_CAUSE=TOKEN_VAZIO`.

---

## PARTE VII — FALSIFICABILIDADE

## 18. Matriz de falsificadores

| Claim | Estado | Falsificador/teste |
|---|---|---|
| par antipodal mantém equidistância sob rotação | `THEOREM` | matriz usada não ortogonal ou rotação não centrada em `c` |
| 8 momentos `π/4` reduzem a 4 eixos antipodais | `THEOREM` | passo/identificação não satisfaz `z[k+4]=-z[k]` |
| pares/ímpares formam dois quadrados | `THEOREM` | raios não iguais ou ângulos não uniformes |
| os 8 vértices formam octógono regular | `THEOREM` | distância angular/radial não uniforme |
| plano `x+y+z=0` corta cubo em hexágono regular | `THEOREM` | domínio não é cubo ou plano não é o especificado |
| hexágono é mecanicamente ótimo | `TOKEN_VAZIO/HYPOTHESIS` | geometria alternativa supera sob protocolo controlado |
| recorrência radial `√3/2` corresponde ao harness registrado | `PASS_NUMERIC_LIMITED` | rerun com artefato/hash divergente falha tolerância |
| lei angular `π/φ` corresponde ao produtor GAIA observado | `FAIL_NOT_SAME_FORM` | só fecha com implementação explicitamente equivalente + teste |
| governança antipodal melhora accountability | `HYPOTHESIS` | experimento comparativo mostra ausência de ganho ou piora |
| UGC melhora compreensão do usuário | `TOKEN_VAZIO` | estudo de compreensão/usabilidade não mostra benefício |
| crosswalk normativo reduz não conformidades | `TOKEN_VAZIO` | auditoria comparativa sem redução mensurável |

---

## 19. Critérios experimentais para a nova área

A CGEN só amadurece como programa científico se produzir resultados adversarialmente testáveis.

### Experimento E1 — Compreensão humana

Comparar interface convencional de privacidade versus UGC:

- compreensão de finalidade;
- identificação do controlador;
- entendimento de inferências;
- acerto sobre compartilhamento;
- tempo para localizar direito/contato;
- taxa de falso entendimento de consentimento.

Pré-registrar hipótese, amostra, métricas e critério de sucesso.

### Experimento E2 — Proveniência

Injetar 100 claims com proveniência parcialmente quebrada e medir:

- taxa de detecção de aresta ausente;
- falsos `PASS`;
- tempo até `TOKEN_VAZIO` correto;
- capacidade de reconstrução causal.

### Experimento E3 — Deriva normativa

Modificar versões simuladas de lei/norma e verificar se:

- gates afetados reabrem;
- referências superseded não permanecem `CURRENT`;
- direitos não desaparecem por atualização;
- recibos históricos permanecem íntegros.

### Experimento E4 — Auditoria independente

Dois avaliadores independentes recebem o mesmo UGC/ledger e devem chegar a resultados compatíveis dentro de critérios previamente definidos. Divergência relevante vira dado, não erro escondido.

### Experimento E5 — Geometria

Executar verificador exato/numérico para:

- antipodalidade;
- oito estados;
- quatro classes;
- dois quadrados;
- octógono;
- seção hexagonal do cubo.

A camada geométrica deve passar independentemente de qualquer narrativa jurídica.

---

## PARTE VIII — URGÊNCIAS E FECHAMENTO DE LACUNAS

## 20. P0 — bloqueios que não podem ser mascarados

1. `Mapa/main` sem enforcement server-side observado no gate atual;
2. promoção exige uma aprovação independente e havia zero no PR observado;
3. qualquer tentativa de transformar CI verde em autorização final viola o próprio contrato;
4. claims econômicos/criminais/sistêmicos fortes permanecem hipóteses até evidência competente;
5. runtime Robotics ainda não possui produtor/execução vinculados.

## 21. P1 — lacunas que esta branch pode fechar documentalmente

- UGC schema: **implementado nesta branch**;
- registro de evolução normativa: **implementado nesta branch**;
- crosswalk jurídico LGPD: vincular por repo/ref/commit;
- contrato de handoff jurídico: criar sem promover matrícula de produtor;
- testes zero-dependency: criar e executar em CI;
- geometria dual-anchor: registrar separando teorema, modelo e hipótese.

## 22. P2 — exige execução externa ou independente

- runtime Robotics real;
- recibo de processamento real;
- pentest/assurance independente;
- auditoria de privacidade independente;
- estudo com usuários;
- parecer jurídico jurisdicional quando necessário;
- branch protection/ruleset server-side e aprovação independente.

Essas lacunas não podem ser “resolvidas por redação”.

---

## 23. Contrato de ciência de fronteira

A nova área só se sustenta se aceitar resultados contra si mesma.

```text
SE um teorema falhar -> corrigir matemática.
SE um teste falhar -> registrar FAIL.
SE a norma mudar -> reabrir gate.
SE a fonte não sustentar o claim -> reduzir o claim.
SE a hipótese econômica não tiver evidência -> TOKEN_VAZIO.
SE a interface não for compreendida -> não chamar de transparência efetiva.
SE o usuário não puder contestar onde deveria -> governança incompleta.
SE o certificado estiver fora de escopo -> não usar como prova.
SE a cadeia causal quebrar -> provenance gap.
```

A ética aqui não é ornamento. Ela aparece operacionalmente como limites verificáveis de finalidade, autoridade, não discriminação, minimização, contestabilidade, reversibilidade e não ocultação de incerteza.

---

## 24. Síntese geométrica

A parábola dos dois pontos pode ser preservada sem sacrificar rigor:

> Dois pontos permanecem equidistantes porque uma transformação válida preserva a métrica. Oito posições tornam-se quatro eixos quando cada direção reconhece seu oposto. Dois quadrados, vistos como faces de um mesmo sólido, não competem pela verdade: tornam-se partes do cubo. E o cubo revela um hexágono quando o corte é declarado com precisão. A espiral não é validada por beleza; cada componente — raio, ângulo e recorrência — precisa do seu próprio teste. Assim também a governança: poder e contrapoder, automação e contestação, regra e evidência, avanço e retorno devem permanecer ligados por distâncias auditáveis.

Essa parábola é interpretação. Os teoremas geométricos que a sustentam são separados e testáveis.

---

## 25. Invariante final

```text
Truth_operational =
  Authority ∩ Provenance ∩ Scope ∩ Time ∩ Reproducibility ∩ Falsifiability ∩ Ethics
```

O símbolo de interseção expressa que a perda de uma dimensão relevante limita o claim total.

```text
F_ok:
  - programa CGEN definido;
  - matemática antipodal 8→4 formalizada;
  - cubo→hexágono provado para seção especificada;
  - radial √3/2 separado da lei angular;
  - UGC e evolução normativa transformados em contratos verificáveis.

F_gap:
  - optimalidade mecânica;
  - equivalência angular π/φ;
  - efeito empírico da UGC sobre compreensão;
  - runtime Robotics;
  - assurance independente;
  - matrícula formal do produtor jurídico no Mapa.

F_next:
  - executar validadores da branch;
  - ligar o crosswalk jurídico por commit exato;
  - produzir contrato de handoff e ledger de proveniência;
  - preservar os gaps externos como TOKEN_VAZIO até evidência real.
```
