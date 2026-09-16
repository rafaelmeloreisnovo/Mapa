# RAFAELIA — Doutrina Internacional de Autoria, Berna, Viena e Montevidéu — V1

**Status:** `CANONICAL_DRAFT / LEGAL_REVIEW_REQUIRED / claim_allowed=false`  
**Data:** 2026-09-16  
**Autor/curadoria do escopo autoral:** Rafael Melo Reis / RAFAELIA  
**Escopo:** somente material autoral ou material cujo direito/licença esteja demonstravelmente controlado; nunca sobrescreve direitos de terceiros.

## 0. Regra-mãe

```text
SOURCE != AUTHORSHIP != COPYRIGHT != LICENSE != PATENT != TRADEMARK != TREATY != EVIDENCE
```

Esta política organiza a leitura jurídica e a proveniência. Ela não cria, por si só, novos direitos, não converte repositório em registro autoral e não rel licencia material de terceiros.

## 1. Camadas normativas

### 1.1 Brasil — legislação interna aplicável

**Lei nº 9.610/1998 — Direitos Autorais**

- regula direitos de autor e conexos;
- protege a expressão autoral, não a ideia abstrata, método, sistema, procedimento ou conceito matemático como tal;
- em matéria científica/técnica, a proteção autoral recai sobre a forma literária ou artística, não sobre o conteúdo científico/técnico em si;
- negócios jurídicos sobre direitos autorais são interpretados restritivamente.

**Lei nº 9.609/1998 — Programa de Computador**

- aplica ao software regime de proteção análogo ao das obras literárias, com regras próprias;
- a proteção independe de registro;
- autoria, licenciamento, titularidade contratual e proveniência permanecem fatos distintos.

## 2. Convenção de Berna — camada internacional de direitos autorais

O Brasil está vinculado à Convenção de Berna, revisão de Paris de 1971, promulgada pelo **Decreto nº 75.699/1975**.

Princípios usados nesta governança:

1. **tratamento nacional**;
2. **proteção automática**, sem formalidade como condição;
3. **independência da proteção** em relação ao país de origem, nos limites do tratado e da lei aplicável.

### Consequências operacionais

```text
NO_REGISTRATION != NO_COPYRIGHT
PUBLIC_REPOSITORY != PUBLIC_DOMAIN
GIT_COMMIT != COPYRIGHT_REGISTRATION
HASH != OWNERSHIP_JUDGMENT
LICENSE_GRANT != TRANSFER_OF_AUTHORSHIP
```

Berna não autoriza:

- apropriar-se de código upstream;
- apagar NOTICE/SPDX;
- transformar ideia, método ou fato em monopólio autoral;
- ignorar licença de terceiros;
- tratar um hash como sentença de titularidade.

## 3. Convenção de Viena sobre o Direito dos Tratados — camada interpretativa

O Brasil promulgou a Convenção de Viena de 1969 pelo **Decreto nº 7.030/2009**, com reservas aos artigos 25 e 66.

Ela não é uma licença de copyright. É usada aqui como régua de interpretação de tratados.

Regras operacionais relevantes:

- **Art. 26 — pacta sunt servanda:** tratado em vigor obriga as partes e deve ser cumprido de boa-fé;
- **Art. 31:** interpretação de boa-fé, segundo sentido comum dos termos, contexto, objeto e finalidade;
- **Art. 32:** meios suplementares quando necessário;
- **Art. 34:** tratado não cria obrigação ou direito para terceiro Estado sem consentimento.

### Consequência RAFAELIA

Nenhum texto interno chamado “tratado”, “pacto”, “cânone” ou “acordo” adquire status de tratado internacional apenas pelo nome.

```text
INTERNAL_PACT != INTERNATIONAL_TREATY
SYMBOLIC_COVENANT != STATE_CONSENT
PRIVATE_LICENSE != VIENNA_CONVENTION_TREATY
```

## 4. Montevidéu — classificação correta

### 4.1 Tratado de Montevidéu de 1889 sobre Propriedade Literária e Artística

Existe historicamente um tratado sul-americano de 1889 sobre propriedade literária e artística.

Para a governança RAFAELIA, ele fica classificado como:

```text
MONTEVIDEO_1889_IP = HISTORICAL_COMPARATIVE_SOURCE
BRAZIL_BINDING_BASE = NOT_ESTABLISHED_IN_THIS_POLICY
CLAIM_ALLOWED_AS_CURRENT_BRAZILIAN_AUTHORITY = false
```

A documentação histórica consultada indica que os acordos de propriedade intelectual adotados em Montevidéu em 1889 **não foram aprovados pelo Brasil**. Portanto, não serão citados como fundamento vinculante brasileiro sem prova documental específica de ratificação/promulgação aplicável.

### 4.2 Tratados de Montevidéu de 1960/1980

Os instrumentos de Montevidéu ligados à ALALC/ALADI e integração econômica são objetos jurídicos distintos.

```text
MONTEVIDEO_1960_OR_1980 != COPYRIGHT_TREATY_1889
```

Não devem ser usados como fundamento de autoria apenas por compartilharem o nome “Montevidéu”.

## 5. TRIPS/ADPIC

O Brasil incorporou a Ata Final da Rodada Uruguai pelo **Decreto nº 1.355/1994**, incluindo o Acordo TRIPS/ADPIC.

Na arquitetura jurídica do projeto, TRIPS é tratado como camada internacional complementar de propriedade intelectual e comércio, não como substituto da legislação brasileira nem da licença concreta de cada artefato.

## 6. Convenção de Paris — separar propriedade industrial

Patentes, marcas, desenhos industriais e outros objetos de propriedade industrial pertencem a outra trilha jurídica.

```text
COPYRIGHT_ROUTE = BERNE + BRAZIL_COPYRIGHT/SOFTWARE_LAW + APPLICABLE_LICENSE
PATENT/TRADEMARK_ROUTE = INDUSTRIAL_PROPERTY_LAW + PARIS/TRIPS + INPI/OTHER_VALID_AUTHORITY
```

Uma expressão autoral protegida por copyright não prova novidade, atividade inventiva ou patenteabilidade.

## 7. WIPO Copyright Treaty — não promover por analogia

Na lista WIPO consultada em 2026, o Brasil não aparece como parte do WIPO Copyright Treaty (WCT).

Estado nesta política:

```text
WCT_BRAZIL = NOT_OPERATIVE_AS_PARTY_AT_THIS_CUT
FUTURE_ACCESSION = TOKEN_VAZIO_TEMPORAL
```

Se a situação mudar, criar sucessor versionado; não reescrever silenciosamente este registro.

## 8. RAFCODE / RAFAELIA — natureza jurídica

RAFCODE-Φ, assinaturas, hashes, Bitraf64, selos, DOI, commits, receipts e cadeias hash podem servir como:

- evidência de integridade;
- evidência temporal;
- apoio de proveniência;
- identificação autoral;
- cadeia de custódia;
- referência contratual.

Eles **não equivalem automaticamente** a:

- registro estatal;
- patente;
- marca registrada;
- decisão judicial;
- tratado internacional;
- exclusividade sobre ideias/métodos/fatos;
- transferência de direitos de terceiros.

## 9. Regra para núcleos autorais

Aplicar esta doutrina apenas onde o material estiver classificado como:

- `AUTHORIAL_PROVEN`; ou
- autoria/titularidade suficientemente documentada para o arquivo específico.

Não aplicar como “licença-mãe” a:

- forks;
- mirrors;
- upstream imports;
- Vectras herdado;
- Termux herdado;
- AndroidX/QEMU/Linux/OpenSSL/BLAKE3 upstream;
- qualquer componente cuja licença/proveniência seja `TOKEN_VAZIO`.

Para material misto, usar escopo por arquivo/diretório.

## 10. Regra de precedência

```text
MANDATORY_LAW
→ VALID_TREATY_BINDING_BRAZIL
→ FILE/COMPONENT_UPSTREAM_LICENSE
→ SIGNED_CONTRACT / VALID_LICENSE_SCOPE
→ RAFAELIA_INTERNAL_POLICY
→ SYMBOLIC_OR_PARABOLIC_LANGUAGE
```

Uma política interna nunca reduz permissões já concedidas validamente por GPL, MIT, Apache, BSD ou outra licença aplicável, nem apaga obrigações de atribuição/NOTICE/copyleft.

## 11. Gate de reutilização autoral

Antes de declarar um artefato “protegido RAFAELIA”:

```text
SOURCE
→ AUTHORSHIP_PROVENANCE
→ THIRD_PARTY_BOUNDARY
→ COPYRIGHT_SCOPE
→ LICENSE_SCOPE
→ PATENT/TRADEMARK_SEPARATION
→ TREATY_APPLICABILITY
→ RELEASE_RECEIPT
```

Se qualquer elo essencial estiver ausente:

```text
status = TOKEN_VAZIO_LEGAL_SCOPE
claim_allowed = false
```

## 12. Referências oficiais e históricas consultadas

- Brasil, Decreto nº 75.699/1975 — Convenção de Berna (Paris 1971).
- WIPO — Berne Convention / summary and contracting-party status.
- Brasil, Lei nº 9.610/1998 — Direitos Autorais.
- Brasil, Lei nº 9.609/1998 — Programa de Computador.
- Brasil, Decreto nº 7.030/2009 — Convenção de Viena sobre o Direito dos Tratados.
- Brasil, Decreto nº 1.355/1994 — Ata Final da Rodada Uruguai / TRIPS.
- WIPO Lex — Tratado de Montevidéu de 1889 sobre Propriedade Literária e Artística, como fonte histórica.
- Repertório/estudos de prática internacional brasileira — status histórico dos tratados de Montevidéu de 1889.

## R3

**F_ok:** Berna, Viena, legislação brasileira, TRIPS e Montevidéu foram separados por função jurídica; fronteira de terceiros preservada.  
**F_gap:** validade jurídica concreta de cada arquivo/contrato continua dependente de inventário de direitos e, quando material, revisão profissional.  
**F_next:** aplicar ponte curta nos núcleos autorais; não alterar root LICENSE de forks ou repositórios mistos sem auditoria por arquivo.
