> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ — a ancoragem normativa existe para servir à vida. Quando normas técnicas colidem, a proteção humana é critério ético interno; conflitos jurídicos reais exigem também jurisdição, hierarquia, competência, vigência, lex specialis/lex posterior e interpretação aplicável. Ver `10_INVARIANTES_PRIMEIRA_LINHA.md`.

# 08 — Ancoragem Normativa (a bagagem da ciência aplicada)

> Cada camada e cada conceito do acervo recebe uma **âncora normativa externa** — a
> "bagagem" real de ISO, NIST, IEC, IEEE, IETF/RFC, W3C, ONU, UNICEF, UNESCO, OMS e,
> quando o domínio é jurídico, Constituição, leis, regulamentos, jurisprudência e atos
> de autoridades competentes. A âncora é um `REFERENCE`, **não um atestado de conformidade**.
> Marcar o alvo é excelência operacional; alegar certificação, aplicabilidade ou infração
> sem fatos e autoridade suficientes seria `HIPOTESE` disfarçada de `FATO`.

## Convenção de estado (herdada de RafPolimata)

- `REFERENCE` = especificação/autoridade externa que orienta o trabalho.
- `FATO` = fato demonstrado por evidência adequada ao tipo de claim.
- `HIPOTESE` = alinhamento ou interpretação pretendida, ainda não demonstrada.
- `LACUNA` = fonte/requisito/aplicabilidade ainda não mapeado.
- `TOKEN_VAZIO` = ausência de evidência suficiente preservada como estado válido, auditável e não promovível.

> Estado atual de quase todas as linhas abaixo: **`REFERENCE`**. A passagem para `FATO`
> exige evidência compatível com a alegação; em matéria jurídica, normalmente também exige
> escopo factual, jurisdição, vigência, autoridade e revisão competente.

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

> **Nota de excelência:** os documentos `01`–`06` implementam estruturas compatíveis com
> tesauro, metadados e facetas; isso os torna auditáveis contra os respectivos padrões,
> mas não demonstra conformidade por si só.

## 3. Camada L4 — Ético-Jurídica

| Domínio | Âncora normativa (`REFERENCE`) |
|---|---|
| Brasil — direitos fundamentais e dados | Constituição Federal, especialmente dignidade e art. 5º X/XII/LXXII/LXXIX; Marco Civil da Internet; LGPD Lei 13.709/2018; atos vigentes da ANPD |
| União Europeia — dados e IA | GDPR Reg. (UE) 2016/679; ePrivacy 2002/58/EC quando aplicável; AI Act Reg. (UE) 2024/1689 |
| Estados Unidos — privacidade e plataformas | Constituição/State Action quando aplicável; FTC Act §5; regimes setoriais e estaduais; Data Security Program/controles nacionais quando o caso tocar transferências sensíveis |
| China | PIPL e demais regras aplicáveis ao processamento/transferência conforme fato e jurisdição |
| Rússia | Lei Federal 152-FZ e atos vigentes aplicáveis; consolidação/versionamento deve ser verificado antes de claim |
| Cuba | Lei 149/2022 e demais normas aplicáveis; embargo/sanções dos EUA não são tratados como equivalentes a uma proibição geral de sinal GPS civil |
| Proteção de dados — padrão | ISO/IEC 27701 (privacidade), apenas como padrão/REFERENCE, não como lei ou certificação automática |
| Governança de IA | ISO/IEC 42001 (AI management system), ISO/IEC 23894 (AI risk), OECD AI Principles |
| Ética de IA | UNESCO — Recommendation on the Ethics of Artificial Intelligence (2021) |
| Direitos humanos | ONU — Declaração Universal dos Direitos Humanos (1948) |
| Direitos da criança | ONU — Convenção sobre os Direitos da Criança (1989); UNICEF Child Online Protection |
| Educação / cultura / ciência | UNESCO — Open Science Recommendation (2021), diversidade cultural |
| Saúde | OMS/WHO — princípios de ética em saúde e dados de saúde |
| Acessibilidade | W3C WCAG 2.2 (conteúdo acessível) |

### 3.1 Cânone jurídico-semântico vigente do Mapa

Para privacidade, governança de dados, IA, GNSS/geolocalização, transferências internacionais,
Big Tech e segurança nacional, a camada detalhada e versionada está em:

- `docs/legal/GLOBAL_DATA_PRIVACY_GNSS_AI_GOVERNANCE_V1.md` — cânone humano evidence-first;
- `data/normative-graph/GLOBAL_DATA_PRIVACY_GNSS_AI_SEMANTIC_ATLAS_V1.json` — atlas navegável;
- `docs/legal/OPENAI_CHATGPT_LOCATION_BOUNDARY_20260826_V1.md` — fronteira produto/localização;
- `docs/legal/BR_PLATFORM_DATA_GOVERNANCE_MARCO_CIVIL_2026_V1.md` — overlay Brasil/plataformas;
- `data/receipts/legal/GLOBAL_DATA_PRIVACY_GNSS_AI_GOVERNANCE_RECEIPT_20260826_V2.json` — cadeia de custódia append-only.

Invariantes de roteamento:

```text
lei != regulamento != jurisprudência != política executiva != padrão != contrato != política de projeto
data_existe_no_dispositivo != app_acessa != serviço_recebe != modelo_recebe
permissão_do_SO != base_jurídica
localização_precisa != telemetria_GNSS_bruta
transparência != dever_geral_de_passthrough_de_sensor
embargo/sanção != desligamento_automático_de_GPS_civil
TOKEN_VAZIO != falso
```

## 4. Camada L5 — Filosófico-Espiritual

Sem norma técnica que a certifique — e isso é correto. A âncora aqui é **declarativa e
ética**, lida como `SIMBOLICO`:

- Universalismo e não-dano orientam-se pela UDHR (dignidade) e pela Ética da IA da UNESCO
  (bem comum), como `REFERENCE` de horizonte — nunca como prova metafísica.
- A regra de honestidade impede que L5 reivindique autoridade normativa de L1–L4.

## 5. Regra de resolução de conflito normativo

A regra “mais protetiva ao humano” permanece como **política ética interna de projeto**, mas
não é promovida a regra universal de conflito de leis. A sequência operacional é:

```text
GATE JURÍDICO
  1. identificar fato, produto, sujeito, território e atividade
  2. identificar jurisdição, autoridade, competência e vigência
  3. aplicar hierarquia normativa e regras pertinentes de conflito/escopo
  4. verificar lex specialis / lex posterior quando juridicamente cabíveis
  5. separar obrigação legal de padrão voluntário, contrato e política interna
  6. aplicar proteção humana como piso ético e critério interno onde houver discricionariedade legítima
  7. registrar conflito, interpretação, evidência, falsificador, revisão e TOKEN_VAZIO
```

Prioridade ética interna, sem substituir a análise jurídica:

```text
  1. Vida, criança e dignidade humana
  2. Direitos fundamentais e proteção de dados
  3. Segurança e integridade
  4. Interoperabilidade e acessibilidade
  5. Eficiência / desempenho
```

Um ganho técnico não justifica, por política interna, sacrificar o nível 1; mas nenhuma norma
técnica interna pode contrariar direito positivo aplicável ou criar competência que o projeto
não possui.

## 6. Estado e próxima ação

- Estado global desta ancoragem: **`REFERENCE` / `TOKEN_VAZIO` por aplicabilidade**.
- **Matriz de conformidade (esqueleto): FEITO** — `codigo/matriz_conformidade.py` →
  `indices/MATRIZ_CONFORMIDADE.md`; as linhas continuam tarefas de auditoria, não selos.
- Repositórios com dados pessoais permanecem prioridade ALTA, mas a nova camada jurídica
  deve ser aplicada por **fluxo de dados real**, não apenas pelo nome do repositório.
- **Próxima ação:** para cada fluxo material, mapear `dado -> origem -> permissão -> finalidade ->
  base/autoridade -> minimização -> destino -> retenção -> transferência -> segurança -> direitos ->
  evidência -> falsificador -> gate`; qualquer elo não provado permanece `TOKEN_VAZIO`.
