# S7F-Ω V1 — Auditoria de anterioridade das sete construções formais

**Origem autoral:** ∆RafaelVerboΩ  
**Data de custódia:** 2026-07-28  
**Estado global:** `RESEARCH_CANDIDATE`  
**claim_allowed:** `false`

## Regra

A ausência de resultado numa busca não prova inexistência mundial. Similaridade não prova identidade. Uma forma conhecida pode receber uma semântica ou um acoplamento novo, mas a novidade deve ser localizada no delta formal exato.

```text
candidato autoral
≠ novidade global provada
≠ resultado científico validado
```

## Matriz conservadora

| ID | Construção | Núcleo conhecido | Delta candidato | Estado |
|---|---|---|---|---|
| S7F-01 | mapa radial com denominador adaptativo | mapas Lorentz/Poincaré e reparametrizações radiais | parâmetro tensorial dinâmico | `CANDIDATE_ADAPTIVE_RADIAL_MAP` |
| S7F-02 | operador de Reclusão | integral de fronteira com dual de Hodge | semântica de informação confinada e acoplamento a atenção | `STANDARD_FORM_NOVEL_SEMANTICS_CANDIDATE` |
| S7F-03 | regularizador recíproco log-log | cálculo log-log e penalidades logarítmicas | função recíproca exata e uso proposto | `EXACT_FUNCTION_CANDIDATE_WITH_BROAD_PRIOR_ART` |
| S7F-04 | atenção hiperbólica com vazio tipado | atenção hiperbólica e máscaras | contrato geométrico/epistêmico do vazio | `PARTIAL_PRIOR_ART_FORMULATION_REQUIRES_CORRECTION` |
| S7F-05 | BLENDDIGS | bases mistas e mixed-radix | composição autoral entre bases | `AUTHORIAL_NOTATION_UNDERDEFINED` |
| S7F-06 | PDE com fonte de atenção | PDEs semilineares, operadores neurais e Transformers/PDEs | combinação exata do Laplaciano, amortecimento e fonte | `HYBRID_PDE_CANDIDATE_UNPROVEN` |
| S7F-07 | ação log-log/Chern–Simons/atenção | ações cinéticas, massa e Chern–Simons | acoplamento variacional de atenção ainda ausente | `ACTION_INCOMPLETE_REQUIRES_VARIATIONAL_COUPLING` |

## Correções invariantes

### 1. Centro da bola de Poincaré

Para `||p||<1`:

\[
d_{\mathbb D}(p,0)=2\operatorname{artanh}(||p||)<\infty.
\]

A distância diverge quando `||p||→1⁻`, não no centro. Logo, `TOKEN_VAZIO` deve ser implementado por máscara/estado tipado, e não por uma distância fictícia infinita na origem.

### 2. Regularizador recíproco log-log

\[
L(r)=\frac{\eta}{\log(\log(1+r^2))}
\]

possui polo em:

\[
r=\sqrt{e-1}\approx1.3108324944.
\]

Na bola unitária, com `η>0`, o denominador é negativo. Portanto, sinal, domínio, convexidade e estabilidade precisam ser demonstrados antes de chamá-lo de penalidade positiva.

### 3. Ação e fonte de atenção

A ação apresentada não contém funcional explícito de atenção. Assim, sua variação não produz automaticamente `T(Ψ)`. É necessário escrever `S_att[Ψ,A]` com:

\[
-\frac{\delta S_{att}}{\delta\Psi}=T(\Psi),
\]

ou declarar a atenção como força externa não conservativa. Se `M` é 7D, `M×S¹` é 8D; o grau da forma de Chern–Simons e a medida precisam ser consistentes.

### 4. BLENDDIGS

Antes de ser operador matemático completo, deve definir `⊕`, `⊗`, semântica das bases, domínio, codomínio, coeficientes, carry, overflow, colisões e invertibilidade.

## Escopo da busca

A busca desta revisão foi mecanística e não exaustiva. Ela confirmou anterioridade clara para redes neurais hiperbólicas, atenção hiperbólica, Transformers/operadores para PDEs, bases mistas e Chern–Simons em dimensões ímpares. Não foi localizado nesta passagem um registro idêntico que feche todos os detalhes das sete construções. Isso preserva `RESEARCH_CANDIDATE`, mas não prova novidade mundial.

Referências primárias registradas:

- arXiv:1805.09112 — Hyperbolic Neural Networks.
- arXiv:1805.09786 — Hyperbolic Attention Networks.
- arXiv:2105.14686 — Fully Hyperbolic Neural Networks.
- arXiv:2205.13671 — Transformer for PDE Operator Learning.
- arXiv:2405.19798 — Mixed radix numeration bases.
- arXiv:hep-th/0502193 — Chern–Simons gravities.
- arXiv:1712.05190 — Chern–Simons densities in dimensions.

## O ativo real

O corpus possui agora uma família coerente de **sete objetos de pesquisa**:

1. mapa radial adaptativo candidato;
2. semântica de reclusão sobre forma de fronteira conhecida;
3. família regularizadora exata a corrigir e testar;
4. protocolo de vazio tipado para atenção hiperbólica;
5. linguagem autoral de bases mistas a completar;
6. PDE híbrida contínuo-discreta candidata;
7. programa variacional/topológico que necessita de acoplamento explícito.

A originalidade mais defensável neste estágio está na síntese arquitetural, nas semânticas autorais, no contrato de `TOKEN_VAZIO` e na combinação específica a ser testada. Não está ainda em prova de ausência mundial de anterioridade nem em teoria física validada.

## Gate de propriedade intelectual

```text
AUTORIA/PROVENIÊNCIA DA FORMULAÇÃO NESTE CORPUS = REGISTRADA
NOVIDADE GLOBAL = TOKEN_VAZIO_PRIOR_ART_EXHAUSTIVE
ATIVIDADE INVENTIVA = TOKEN_VAZIO_TECHNICAL_EFFECT
VALIDADE CIENTÍFICA = TOKEN_VAZIO_REPLICATION
```

Hashes, commits e revisões constituem proveniência técnica datada; não equivalem a patente concedida, parecer jurídico ou revisão por pares.

## F_next

1. congelar definições e notação;
2. pesquisar anterioridade por subexpressão, semântica e mecanismo;
3. implementar invariantes e testes determinísticos;
4. comparar cada operador com baselines;
5. obter revisão matemática independente;
6. somente depois avaliar publicação e propriedade intelectual.
