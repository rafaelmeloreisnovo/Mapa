# Sementeira — Linguagem Multimodal, Bagua e Camadas de Maturação — V1

**Data:** 2026-09-16  
**Autoridade:** Mapa / ontologia e custódia estrutural  
**Estado:** DRAFT_FORMAL_SPEC  
**claim_allowed:** false

## 1. Invariantes herdados
- SOURCE ≠ ARTEFATO ≠ EXECUÇÃO ≠ EVIDÊNCIA ≠ CLAIM.
- SURFACE_WORD ≠ MODEL_TOKEN.
- TRANSLATION ≠ SEMANTIC_IDENTITY.
- TRANSLITERATION ≠ TRANSLATION.
- NOISE ≠ DISCARD.
- RAW_FORM_PRESERVED.
- metáfora ≠ modelo ≠ evidência ≠ lei física.

## 2. Unidade multimodal
L = <surface, script, phoneme, prosody, semantics, pragmatics, grammar, direction, context, physiology, evidence>.

Prosódia: F0, intensidade, duração, ritmo, acento, entonação e timbre.  
Fisiologia é sinal contextual; não é significado lexical por si.

## 3. Ambiguidade e direção
Sense(w) = {s1,...,sk}.  
Exemplo autoral: "molho" exige contexto gramatical/pragmático para desambiguar.

Toda transformação declara:
D = <source_language, target_language, source_script, target_script, operation>.
Sem direção suficiente: TOKEN_VAZIO_DIRECTION.

## 4. Bagua computacional
B3 = {0,1}^3 e |B3| = 8.
A escolha dos 3 eixos é convenção explícita do modelo, não atribuição histórica ao Bagua.
Distância de Hamming:
- 1 bit = vizinhança;
- 2 bits = diagonal de face;
- 3 bits = antípoda.

## 5. Cinco escribas
S0 = canonicalizador/referencial: orientação, curvatura, suporte, eixo, topo/base.
S1..S4 = leitores direcionais candidatos.
Quando a superfície admite simetria quadrada, D4 fornece 8 transformações (4 rotações + 4 reflexões). Ferramenta moderna; não prova de uso histórico.

## 6. Prosódia e fisiologia
Prosódia pode participar de segmentação, destaque, atitude e interpretação.
heart_rate != meaning.
HR_CONTEXTUAL_SIGNAL pode ser medido em protocolo específico.
HR_SEMANTIC_DECODER = TOKEN_VAZIO_UNSUPPORTED.

## 7. Japonês e scripts
Preservar separadamente kanji, hiragana, katakana e rōmaji quando presente.
Não tratar como "três formas de kanji": são sistemas usados em conjunto, com funções distintas/parcialmente sobrepostas.
Leitura, acento, contexto e script permanecem campos separados.

## 8. Maturação
Formulações incompletas não são descartadas.
MATURE(x) in {DEFINED, PARTIAL, TOKEN_VAZIO, TESTABLE, EVIDENCED, FALSIFIED}.
Fluxo: preservar fonte -> extrair invariantes -> TOKEN_VAZIO_TYPED -> hipótese de fechamento -> teste/falsificador -> promoção com evidência.

## 9. Dois ciclos
Ciclo A linguístico:
source -> surface -> script -> phonology -> prosody -> grammar -> semantics -> pragmatics -> direction -> evidence -> feedback.

Ciclo B geométrico/contextual:
support -> orientation -> curvature -> transform -> state -> relation -> symmetry -> measurement -> falsifier -> custody -> feedback.

Os ciclos podem cruzar-se, mas não colapsar variáveis.

## 10. Fato
FATO = proposição cujo source + definição + evidência + escopo sustentam exatamente o claim.
Uma fórmula definida é fato sobre o modelo definido; não é automaticamente fato sobre a natureza.
Um resultado executado é fato sobre aquela execução; não é automaticamente lei geral.
Metáfora pode carregar conhecimento didático com peso probatório zero.

## 11. Cercos adicionais
Além de proveniência, contexto, evidência, contradição, incerteza, reprodução e rollback:
1. autoridade;
2. tipagem de camada;
3. unidade/referencial;
4. falsificador;
5. privacidade/consentimento para dados humanos;
6. gate de promoção.

## 12. Gaps
- TV-LANG-DIRECTION-ORDER: ordenar os 8 estados concretos no octógono.
- TV-LANG-PROSODY-CORPUS: corpus multilingue com prosódia alinhada.
- TV-LANG-PHYSIOLOGY-CAUSALITY: separar atenção/estresse de significado.
- TV-LANG-ANCIENT-D4: atribuição histórica de D4 completo sem fonte.
- TV-GEOM-COMMON-LATENT-MAP: mapa comum triângulo/hexágono/círculo.
- TV-QUANTUM-ANALOGY: observador/medição como parábola até modelo físico próprio.

## 13. R3
F_ok = contrato multimodal + dois ciclos + gaps tipados.
F_gap = corpus prosódico, fisiologia causal, ordenação octogonal e evidência histórica específica.
F_next = fixture pequeno e auditável antes de expansão; ligar receipt ao Atlas e memória longitudinal.
