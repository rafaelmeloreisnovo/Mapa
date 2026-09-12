# RAFAELIA — Base Jurídica, Jurisprudência e Referências V1

**Status:** `RESEARCHED_DRAFT / COUNSEL_REVIEW_REQUIRED`  
**Cut-off:** 2026-09-12

## 1. Constituição Federal

### Art. 5º, XXVII e XXVIII

A Constituição brasileira reconhece ao autor direito exclusivo de utilização, publicação ou reprodução e assegura fiscalização do aproveitamento econômico da obra.

Fonte oficial:  
<https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm>

### Art. 60, § 4º, IV

A Constituição impede proposta de emenda tendente a abolir direitos e garantias individuais.

**Precisão obrigatória:** isso não transforma cláusulas de uma licença privada em "cláusulas pétreas". O pacote usa a expressão jurídica correta **núcleo contratual essencial**.

## 2. Lei nº 9.610/1998 — Direitos Autorais

Pontos centrais:

- art. 22: direitos morais e patrimoniais pertencem ao autor;
- art. 24, I-II: direito de reivindicar autoria e de ter nome/pseudônimo/sinal indicado no uso da obra;
- art. 27: direitos morais são inalienáveis e irrenunciáveis;
- art. 28: direito exclusivo de utilizar, fruir e dispor da obra;
- art. 29: modalidades de utilização dependem de autorização prévia e expressa, ressalvadas hipóteses legais;
- art. 49: admite licenciamento/cessão sob limites legais;
- arts. 101-108: sanções civis, suspensão, apreensão, indenização e correção de omissão de autoria.

Fonte oficial:  
<https://www.planalto.gov.br/ccivil_03/leis/l9610.htm>

## 3. Lei nº 9.609/1998 — Software

O art. 9º estabelece que o uso de programa de computador no Brasil será objeto de contrato de licença.

O art. 12 tipifica violações de direito autoral de software e agrava situações de reprodução/comercialização não autorizada.

Fonte oficial:  
<https://www.planalto.gov.br/ccivil_03/leis/l9609.htm>

## 4. Código Civil

Pontos usados no desenho contratual:

- art. 389: inadimplemento pode gerar perdas e danos, juros, atualização e honorários de advogado, conforme redação vigente;
- art. 403: perdas e danos dependem de efeito direto e imediato;
- art. 404: obrigações pecuniárias incluem atualização, juros, custas e honorários, sem prejuízo de pena convencional;
- arts. 408-416: disciplina da cláusula penal;
- art. 412: a cominação não pode exceder a obrigação principal;
- art. 413: juiz deve reduzir penalidade em cumprimento parcial ou excesso manifesto;
- art. 416, parágrafo único: indenização suplementar acima da pena depende de convenção e prova;
- arts. 421 e 421-A: liberdade contratual, função social, intervenção mínima, alocação de riscos e revisão excepcional em contratos civis/empresariais;
- art. 422: probidade e boa-fé.

Fonte oficial:  
<https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm>

## 5. Código de Processo Civil

O art. 85 disciplina honorários sucumbenciais e os atribui por decisão judicial ao advogado da parte vencedora, segundo os critérios legais.

Fonte oficial:  
<https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm>

## 6. STJ — honorários privados e custos de enforcement

### Posição histórica

REsp 1.134.725/MG, Terceira Turma, 2011, admitiu em contexto específico honorários contratuais como perdas e danos.

Fonte oficial STJ:  
<https://www.stj.jus.br/websecstj/cgi/revista/REJ.cgi/ITA?dt=20110624&formato=HTML&nreg=200900671480&salvar=false&seq=1069449&tipo=0>

### Posição recente relevante

No REsp 1.914.396/DF, Terceira Turma, julgado em 8/6/2026, o STJ assentou que custos de contratação de advogado para ajuizar cobrança não constituem, nessa hipótese, dano material automaticamente repassável à parte adversa por cláusula contratual.

**Efeito de drafting:** a licença não promete recuperação automática de todo honorário judicial privado. Separa:

```text
custos extrajudiciais razoáveis/documentados
+
custas processuais legalmente recuperáveis
+
honorários sucumbenciais por decisão judicial
+
outras verbas admitidas pela lei aplicável
```

## 7. STJ — cláusula penal

A jurisprudência do STJ trata o art. 413 do Código Civil como norma cogente: penalidade manifestamente excessiva ou referente a obrigação parcialmente cumprida pode/deve ser reduzida equitativamente.

Referências:

- REsp 1.447.247/SP, Quarta Turma, DJe 4/6/2018.
- REsp 1.898.738/SP, Terceira Turma, DJe 26/3/2021.

Por isso este pacote evita construir uma "multa infinita" ou uma renúncia fictícia à revisão legal.

## 8. Convenção de Berna / WIPO

O art. 6bis da Convenção de Berna reconhece, independentemente dos direitos econômicos, o direito de reivindicar autoria e de se opor a determinadas modificações prejudiciais à honra ou reputação.

Fontes:

- WIPO Lex — Berne Convention, Art. 6bis: <https://www.wipo.int/wipolex/en/text/577519>
- WIPO — Summary of the Berne Convention: <https://www.wipo.int/en/web/treaties/ip/berne/summary_berne>

## 9. Microsoft — referência estrutural, não fonte normativa

Os documentos Microsoft foram consultados como **comparadores de arquitetura contratual**, não como autoridade jurídica nem como texto a copiar.

Estruturas observadas incluem:

- reserva de direitos;
- uso pessoal/não comercial em determinados produtos;
- proibições de redistribuição/sublicenciamento;
- limites de responsabilidade;
- exclusões sujeitas à lei aplicável;
- indenização por determinados usos;
- alocação de custos e honorários em determinadas cláusulas.

Em Termos Padrão de Aplicativos Microsoft, há exemplo estrutural de limite de danos diretos ao maior entre o valor pago e US$ 1, sujeito à lei aplicável.

Fontes oficiais:

- Microsoft Services Agreement (Brasil): <https://www.microsoft.com/pt-BR/servicesagreement>
- Microsoft Developer Agreement: <https://learn.microsoft.com/pt-br/legal/mdsa>
- Microsoft Product Terms: <https://www.microsoft.com/licensing/terms/>

A RAFAELIA não copia os termos Microsoft; usa somente padrões abstratos de organização contratual.

## 10. Súmulas vinculantes

Nesta auditoria **não foi identificada Súmula Vinculante do STF que estabeleça diretamente o regime contratual de atribuição, proibição de uso comercial, custo de auditoria ou limite de responsabilidade de licença autoral/software aqui tratado**.

Portanto, nenhuma Súmula Vinculante é inventada ou citada artificialmente.

Precedentes, súmulas não vinculantes, enunciados doutrinários e decisões de tribunais podem ser relevantes, mas sua força jurídica deve ser identificada corretamente.

## 11. Referências bibliográficas/normativas mínimas

- BRASIL. Constituição da República Federativa do Brasil de 1988.
- BRASIL. Lei nº 9.610, de 19 de fevereiro de 1998.
- BRASIL. Lei nº 9.609, de 19 de fevereiro de 1998.
- BRASIL. Lei nº 10.406, de 10 de janeiro de 2002 (Código Civil), texto compilado.
- BRASIL. Lei nº 13.105, de 16 de março de 2015 (Código de Processo Civil).
- WORLD INTELLECTUAL PROPERTY ORGANIZATION. Berne Convention for the Protection of Literary and Artistic Works, Article 6bis.
- SUPERIOR TRIBUNAL DE JUSTIÇA. REsp 1.134.725/MG.
- SUPERIOR TRIBUNAL DE JUSTIÇA. REsp 1.447.247/SP.
- SUPERIOR TRIBUNAL DE JUSTIÇA. REsp 1.898.738/SP.
- SUPERIOR TRIBUNAL DE JUSTIÇA. REsp 1.914.396/DF.
- MICROSOFT. Microsoft Services Agreement; Developer Agreement; Product Terms. Consultados apenas como referências estruturais de drafting.

## 12. Gate profissional

Este documento é pesquisa jurídica técnica e drafting de governança, não parecer jurídico assinado.

Antes de adoção definitiva, registrar:

```text
COUNSEL_REVIEW
jurisdiction
lawyer/OAB
review_date
approved_version
exceptions
commercial_template
```

Sem essa revisão, o estado permanece `DRAFT_COUNSEL_REVIEW_REQUIRED`.
