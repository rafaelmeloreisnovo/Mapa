# Papers × ChipQuantum × RLL — Auditoria de Fórmulas e Autoridades

**Data:** 2026-08-04  
**Evento:** `6612b91f06ae1499cccf0553c8546595db5f76755e90644516d86e616217cfdb`  
**Predecessor:** `4853a7b04b9d270ea34cec0096195692d54ba9db351070a4240bf0096649c057`  
**Estado:** `EVIDENCIADO_PARCIAL / claim_allowed=false / APPEND_ONLY`

## 1. Resultado executivo

A leitura dos três repositórios mostra três classes que não devem ser fundidas:

1. `papers`: síntese, fórmulas propostas, parábolas técnicas e ledgers de claims;
2. `ChipQuantum`: algoritmos, validadores, núcleos freestanding isolados e protótipos;
3. `RLL`: equação cosmológica, dados, likelihoods, resultados e falsificadores.

Regra canônica:

```text
fórmula escrita ≠ definição completa ≠ implementação ≠ teste ≠ evidência científica
```

## 2. Papers

O arquivo `src/asm/RAFAELIA_MATH_FORMULAS.md` mistura:

- definições clássicas, como dimensão box-counting e normalização L2;
- padrões de engenharia, como hashchain, Merkle tree e KDF;
- heurísticas autorais, como `Retroalimentação(n)=1+log2(1+n)`;
- objetos incompletos, como `F_R(n)` com `Delta_Rafael` não tipado;
- parábolas matemáticas, como `F_Love`.

Ele é útil como catálogo de sementes, mas não como autoridade matemática homogênea.

A parte Ω-CUBE-42 é mais madura: `C(4,2)×7=42` e a aciclicidade por potencial estrito possuem formalização e testes limitados. O termo “atrator” continua provisório.

## 3. ChipQuantum

O núcleo `src/toroidal_engine.py` implementa:

```math
C_{t+1}=(1-\alpha)C_t+\alpha C_{in}
```

```math
H_{t+1}=(1-\alpha)H_t+\alpha H_{in}
```

```math
\phi=(1-H)C
```

com atualização:

```math
s'_i=(s_i+\phi b_i)\bmod 1.
```

A variante Q16 preserva a ideia com `alpha=1/4` e máscara de 16 bits. O índice denominado “atrator” é uma redução modular do acumulador por 42. Isso prova um roteador determinístico, não bacias de atração.

O claim global do README — sistema inteiro freestanding, um arquivo, sem libc — não é sustentável: `src/kernel/main.c` usa `stdio.h`, `time.h`, `clock_gettime` e `printf`. Entretanto, o núcleo Ω-CUBE-42 é um artefato isolado com gate freestanding limitado.

O validador Paper 6 sustenta formalmente:

```math
M^2=\frac{9}{16}I,\qquad M^{-1}=\frac{16}{9}M,
```

```math
D_\theta=-2ab\cos\theta,\qquad D_Q=-\frac{\Delta}{4A}.
```

A presença de `sqrt(3)/2` é correta somente quando o domínio triangular/hexagonal ou o ângulo de 30/60 graus está explicitado.

## 4. RLL

A equação de background é:

```math
E^2(a)=\Omega_r a^{-4}+\Omega_m a^{-3}+\Omega_\Lambda+
\Omega_{s0}[f(a)+(1-f(a))a^{-3}]+\Omega_{B0}a^{-4}+\Omega_{P0}a^{-4}.
```

com:

```math
f(z)=\frac{1}{1+\exp((z-z_t)/w_t)}.
```

O limite:

```math
\Omega_{s0}=\Omega_{B0}=\Omega_{P0}=0
```

recupera exatamente ΛCDM. Esse é um ponto forte de falsificabilidade.

O script `rll_vs_lcdm.py` implementa H(z), distâncias BAO, blocos de covariância, chi-quadrado, AIC e BIC. Seu contrato informa que o fator de Bayes derivado do BIC é aproximação de Schwarz, não nested sampling.

O artefato FASE 20 registra:

```text
Omega_s0 95% UL = 0.0017772301590821408
ln(B10)          = -6.190210762419383 ± 0.6906527421175422
```

Esse resultado favorece fortemente ΛCDM e mantém RLL próximo do limite nulo. A cadeia MCMC é mais curta que o ideal, e continuam pendentes unificação de covariâncias, sensibilidade a priors e reprodução independente.

## 5. Autoridade correta

| Objeto | Autoridade |
|---|---|
| síntese e manuscrito | `papers` |
| fórmula matemática clássica/prova | repositório formal + verificador |
| algoritmo e runtime | `ChipQuantum`, por arquivo/commit/receipt |
| equação cosmológica e likelihood | RLL |
| resultado científico | RLL + dados + pipeline + reprodução |
| relação transversal | `Mapa` |

## 6. Próximos gates

1. tipar cada fórmula de `papers` como `CLASSICAL`, `DEFINITION`, `AUTHOR_MODEL`, `ENGINEERING_PATTERN`, `PARABLE` ou `TOKEN_VAZIO`;
2. criar manifestos freestanding por artefato no ChipQuantum;
3. testar T¹ e T² antes de T⁷, com controles positivos e negativos;
4. unificar no RLL a covariância DESI completa, Pantheon+ STAT+SYS e o sampler Bayesiano;
5. reproduzir FASE 20 de forma independente;
6. manter claims físicos bloqueados até fechamento covariante e estabilidade.

## R3

- **F_ok:** fórmulas, códigos, resultados e limites foram separados por autoridade.
- **F_gap:** tipagem integral do compêndio, topologia empírica T⁷, manifestos artifact-scoped e reprodução RLL.
- **F_next:** anexar esta matriz ao Mapa e ao Drive, mantendo os três repositórios como autoridades independentes.
