> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ — a ancoragem normativa existe para servir à vida. Quando normas técnicas colidem, prevalece a que mais protege o ser humano e a criança (ONU UDHR Art.1 · UNCRC Art.3). Ver `10_INVARIANTES_PRIMEIRA_LINHA.md`.

# 08 — Ancoragem Normativa (a bagagem da ciência aplicada)

> Cada camada e cada conceito do acervo recebe uma **âncora normativa externa** — a
> "bagagem" real de ISO, NIST, IEC, IEEE, IETF/RFC, W3C, ONU, UNICEF, UNESCO, OMS.
> A âncora é um `REFERENCE` (padrão externo ao qual o trabalho se orienta), **não um
> atestado de conformidade**. Marcar o alvo é excelência operacional; alegar
> certificação sem auditoria seria `HIPOTESE` disfarçada de `FATO`.

## Convenção de estado (herdada de RafPolimata)

- `REFERENCE` = especificação externa (RFC/ISO/IEEE/tratado) que orienta o trabalho.
- `FATO` = conformidade demonstrada com evidência (auditoria, teste, certificado).
- `HIPOTESE` = alinhamento pretendido, ainda não medido.
- `LACUNA` = norma aplicável ainda não mapeada.

> Estado atual de quase todas as linhas abaixo: **`REFERENCE`** (alvo declarado). A
> passagem para `FATO` exige auditoria — registrada como próxima ação, nunca presumida.

## 1. Camada L1–L2 — Computacional / Estrutural

| Conceito | Âncora normativa (`REFERENCE`) |
|---|---|
| Linguagem/execução | ISO/IEC 9899 (C), ISO/IEC 14882 (C++), IEEE 754 (ponto flutuante) |
| Hashing | NIST FIPS 180-4 (SHA-2), FIPS 202 (SHA-3), NIST SP 800-107; BLAKE3 = spec própria (não-NIST) |
| Assinatura | IETF RFC 8032 (EdDSA/Ed25519), RFC 5280 (PKI/X.509) |
| Determinismo / build | SLSA, Reproducible Builds, ISO/IEC/IEEE 12207 (ciclo de vida de software) |
| Custódia / proveniência | W3C PROV-O, ISO 15489 (records management), ISO 27037 (evidência digital) |
| Qualidade de produto | ISO/IEC 25010, ISO/IEC 25012 (qualidade de dados) |
| Segurança da informação | ISO/IEC 27001/27002, NIST CSF, NIST SP 800-53 |
| Formatos de dados | IETF RFC 8259 (JSON), RFC 3629 (UTF-8), W3C XML/SVG |

## 2. Camada L3 — Semântica / Organização do Conhecimento

Esta é a bagagem **biblioteconômica** propriamente dita — a que dá qualidade acadêmica
ao acervo:

| Instrumento | Âncora normativa (`REFERENCE`) |
|---|---|
| Tesauro / vocabulário controlado | ISO 25964-1/-2 (thesauri & interoperability); ISO 2788 (legado) |
| Metadados descritivos | ISO 15836 (Dublin Core); RDA; FRBR/LRM (IFLA) |
| Classificação | CDU/UDC; CDD (Dewey); esquema facetado (Ranganathan) |
| Vocabulários ligados | W3C SKOS, W3C RDF, W3C OWL |
| Identificadores persistentes | DOI (ISO 26324), ORCID, Handle |
| Interoperabilidade de busca | ISO 23950 (Z39.50), OAI-PMH |

> **Nota de excelência:** os documentos `01`–`06` já implementam, na prática, ISO 25964
> (tesauro), ISO 15836 (Dublin Core) e Ranganathan (facetas). Esta linha os torna
> auditáveis contra o padrão.

## 3. Camada L4 — Ético-Jurídica

| Domínio | Âncora normativa (`REFERENCE`) |
|---|---|
| Proteção de dados | LGPD (Lei 13.709/2018, Brasil); GDPR (Reg. UE 2016/679); ISO/IEC 27701 (privacidade) |
| Governança de IA | ISO/IEC 42001 (AI management system), ISO/IEC 23894 (AI risk), OECD AI Principles |
| Ética de IA | UNESCO — Recommendation on the Ethics of Artificial Intelligence (2021) |
| Direitos humanos | ONU — Declaração Universal dos Direitos Humanos (1948) |
| Direitos da criança | ONU — Convenção sobre os Direitos da Criança (1989); UNICEF Child Online Protection |
| Educação / cultura / ciência | UNESCO — Open Science Recommendation (2021), diversidade cultural |
| Saúde | OMS/WHO — princípios de ética em saúde e dados de saúde |
| Acessibilidade | W3C WCAG 2.2 (conteúdo acessível) |

## 4. Camada L5 — Filosófico-Espiritual

Sem norma técnica que a certifique — e isso é correto. A âncora aqui é **declarativa e
ética**, lida como `SIMBOLICO`:

- Universalismo e não-dano orientam-se pela UDHR (dignidade) e pela Ética da IA da UNESCO
  (bem comum), como `REFERENCE` de horizonte — nunca como prova metafísica.
- A regra de honestidade impede que L5 reivindique autoridade normativa de L1–L4.

## 5. Regra de resolução de conflito normativo

Quando duas normas técnicas colidem (ex.: eficiência × privacidade; desempenho ×
acessibilidade; automação × supervisão humana), a decisão **não** é técnica pura:

```text
PRIORIDADE (do maior ao menor peso):
  1. Proteção da vida, da criança e da dignidade humana   (UDHR, UNCRC)  ← inviolável
  2. Direitos fundamentais e proteção de dados            (LGPD/GDPR)
  3. Segurança e integridade                              (ISO 27001, NIST)
  4. Interoperabilidade e acessibilidade                  (W3C, ISO)
  5. Eficiência / desempenho                              (métricas técnicas)
```

> Um ganho técnico que exija sacrificar o nível 1 é **recusado por design**, não
> negociado. Isso é a "melhor forma de proteção humana" pedida: a tendência estrutural
> a fazer o bem e boas práticas, inscrita antes de qualquer otimização.

## 6. Estado e próxima ação

- Estado global desta ancoragem: **`REFERENCE`** (alvos declarados, alinhamento
  pretendido). Nenhuma linha é declarada `FATO` sem auditoria.
- **Matriz de conformidade (esqueleto): FEITO** — `codigo/matriz_conformidade.py` →
  `indices/MATRIZ_CONFORMIDADE.md`: 153 linhas norma × evidência × gap, **todas `PENDENTE`**,
  com prioridade ALTA nos 5 repos de dados pessoais (`conversations_chunks_private`, `home`,
  `gaia_phi`, `x0`, `lgpd_constituicoes`).
- **Próxima ação (LACUNA):** auditar `PENDENTE`→`CONFORME`/`GAP` por norma (exige critérios
  de auditoria reais). Ver contabilidade em `18_ROADMAP_ESTADO.md`.
