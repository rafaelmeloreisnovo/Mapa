# Registro inicial de anterioridade — Ineditismo Formalizável V1

**Estado:** `NON_EXHAUSTIVE_SEED_REGISTER`  
**prior_art_complete:** `false`  
**claim_allowed:** `false`

Este arquivo não decide novidade ou patenteabilidade. Ele registra referências mínimas que já impedem afirmações absolutas antes de uma busca profissional completa.

## Geometria hiperbólica e Transformers

1. Nickel, M.; Kiela, D. **Poincaré Embeddings for Learning Hierarchical Representations**. NeurIPS, 2017.
   - embeddings no disco de Poincaré;
   - otimização Riemanniana;
   - hierarquia e similaridade.

2. Ganea, O.; Bécigneul, G.; Hofmann, T. **Hyperbolic Neural Networks**. NeurIPS, 2018.
   - camadas neurais hiperbólicas;
   - operações no espaço de Poincaré.

3. Chami et al. **Hyperbolic Graph Convolutional Neural Networks**. NeurIPS, 2019.
   - curvatura treinável distinta por camada.

4. **Curve Your Attention: Mixed-Curvature Transformers for Graph Representation Learning**. ICLR/OpenReview, 2023.
   - Transformer em espaços de curvatura mista;
   - curvatura aprendida de ponta a ponta.

**Consequência:** “geometria adaptativa”, “curvatura aprendida” e “Transformer não euclidiano” não podem ser tratados como classes vazias de anterioridade. O delta precisa estar na carta/gauge específico, na implementação e no efeito técnico.

## Memória fracionária e contexto longo

5. Tarasov, V. **Discrete Map with Memory from Fractional Differential Equation of Arbitrary Positive Order**. 2011.
   - derivadas fracionárias e memória de potência.

6. Wang et al. **Fractional-order gradient descent learning of BP neural networks with Caputo derivative**. Neural Networks, 2017.
   - Caputo aplicado ao treinamento de redes neurais.

7. Martins, Marinho e Martins. **∞-former: Infinite Memory Transformer**. 2021.
   - memória contínua de longo prazo com custo independente do comprimento total, sujeito a aproximação.

8. Qu, Ly e Gong. **Fractional Neural Attention for Efficient Multiscale Sequence Processing**. 2025.
   - mecanismo de atenção fracionária e dependências multiescala.

9. Behnam et al. **RocketKV: Accelerating Long-Context LLM Inference via Two-Stage KV Cache Compression**. ICML, 2025.
   - compressão de KV e avaliação de memória/latência.

10. Lee, Lee e Kim. **Fast and Scalable Caputo Fractional Gradient Descent via Perturbation-Preserving Memory Compression**. 2026.
    - soma de exponenciais e agregação diádica para reduzir custo da memória de Caputo.

**Consequência:** Caputo, memória de potência, atenção fracionária e compressão KV possuem anterioridade. O candidato RAFAELIA precisa demonstrar uma composição específica e um efeito técnico inesperado ou superior.

## Propriedade intelectual no Brasil

11. INPI. **Diretrizes de Exame de Pedidos de Patente envolvendo Invenções Implementadas por Programa de Computador**.

12. INPI. **Diretrizes de Exame de Pedidos de Patente — Patenteabilidade**.

13. INPI. **Guia de Registro de Programa de Computador**.

**Separação obrigatória:**

```text
registro de software
≠ patente de invenção
≠ prova de autoria científica
≠ prova de novidade
≠ prova de funcionamento
```

## F_next de anterioridade

- pesquisar por fórmula exata e variantes algébricas;
- pesquisar famílias de patentes por função, não apenas por palavras;
- decompor cada candidato em elementos de claim;
- registrar datas de prioridade, titulares e jurisdições;
- construir matriz `claim_element × reference`;
- manter `TOKEN_VAZIO_IP` até revisão especializada.
