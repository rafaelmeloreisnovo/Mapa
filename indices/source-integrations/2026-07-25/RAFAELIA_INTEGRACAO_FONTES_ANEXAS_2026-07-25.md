# RAFAELIA — Integração de Fontes Anexas — 2026-07-25

**Artefato:** `RAFAELIA-INT-SOURCES-20260725`  
**Estado:** `CANONICAL_DRAFT · READ_ONLY_INGEST · CLAIM_ALLOWED=false`  
**Escopo:** 16 anexos recebidos nesta sessão; 7 corpos-fonte semânticos; 9 cópias idênticas consolidadas como aliases do Atlas.

## 1. Regra de integração

Este registro não promove conteúdo por volume, estética, recorrência ou valor simbólico. Ele conecta cada fonte à camada correta do ecossistema:

```text
arquivo recebido → digest → source object → índice → claim/gap → evidência/falsificador → decisão → artefato
```

Os arquivos originais permanecem imutáveis. O Mapa recebe ponteiros, relações, hashes e estados de evidência; o Google Drive recebe a cópia editorial dos manifests. Código, teoria, imagem e metáfora permanecem separados até existir prova própria.

## 2. Recibo criptográfico do lote

Foram calculados, para cada anexo bruto, `MD5`, `SHA-256` e `BLAKE3-256`.

- `MD5` é mantido somente para compatibilidade e comparação legada; não é prova adversarial.
- `SHA-256` é o digest geral de custódia deste lote.
- `BLAKE3-256` foi calculado com a implementação C contida no snapshot BLAKE3 recebido. O snapshot exigiu uma definição de compatibilidade de compilação para `BLAKE3_LIKELY`; após isso, os vetores BLAKE3 de 0, 1, 64 e 1.024 bytes coincidiram com os vetores fornecidos no próprio snapshot.
- Essa validação comprova o procedimento de digest deste lote; ela **não** certifica, por si só, build integral do fork, desempenho, segurança do RMR ou equivalência total com o upstream.

Os comentários internos dos ZIPs que parecem SHA Git foram registrados apenas como `archive_comment_candidate_commit`: não são tratados como commits verificados sem consulta/replay do repositório correspondente.

O manifest de máquina completo está em `RAFAELIA_FONTES_ANEXAS_CUSTODY_2026-07-25.jsonl`.

## 3. Deduplicação semântica

Os nove Markdown avulsos são byte-a-byte idênticos às respectivas entradas do `atlas_rafaelia_cosmos.zip`. Portanto, eles não contam como nove provas independentes nem como nove fontes conceituais novas.

| Alias avulso | Entrada canônica no Atlas | Estado |
| --- | --- | --- |
| `04_BIOLOGIA_BIOENGENHARIA.md` | `04_BIOLOGIA_BIOENGENHARIA.md` | `IDENTICAL` |
| `01_MATEMATICA_GEOMETRIA_SAGRADA.md` | `01_MATEMATICA_GEOMETRIA_SAGRADA.md` | `IDENTICAL` |
| `07_IA_COMPUTACAO.md` | `07_IA_COMPUTACAO.md` | `IDENTICAL` |
| `03_FISICA_QUANTICA_TOPOLOGIA.md` | `03_FISICA_QUANTICA_TOPOLOGIA.md` | `IDENTICAL` |
| `08_MATEMATICA_SIMBOLICA.md` | `08_MATEMATICA_SIMBOLICA.md` | `IDENTICAL` |
| `06_CONSCIENCIA_ESPIRITUALIDADE.md` | `06_CONSCIENCIA_ESPIRITUALIDADE.md` | `IDENTICAL` |
| `05_ENGENHARIA_ELETROMAGNETISMO.md` | `05_ENGENHARIA_ELETROMAGNETISMO.md` | `IDENTICAL` |
| `10_GEOMETRIA_CAMPOS_ATRATORES.md` | `10_GEOMETRIA_CAMPOS_ATRATORES.md` | `IDENTICAL` |
| `09_TERMODINAMICA_SISTEMAS.md` | `09_TERMODINAMICA_SISTEMAS.md` | `IDENTICAL` |

## 4. Integração por corpo-fonte

| Source object | Conteúdo lido | Papel operacional | Estado de evidência | Destino canônico |
| --- | --- | --- | --- | --- |
| `SRC-ATT-TORA-001` | APK Android, JNI/C, Basiclow Hex, núcleo determinístico, documentação de benchmark e integração multi-arquitetura | Referência de conversão/validação de baixo nível e telemetria | Implementação e documentação presentes; build, equivalência por ISA e benchmarks independentes não foram executados neste ciclo | Mapa: execução/compilação; Drive: fonte técnica; `TOKEN_VAZIO` para métricas declaradas |
| `SRC-ATT-BLAKE3-RMR-001` | BLAKE3, `rmr/`, auditoria de diff e proveniência | Limite criptográfico + camada externa de custódia/execução | Separação BLAKE3/RMR documentada e digest do lote validado; integração persistente RMR→BLAKE3 e build completo permanecem não demonstrados aqui | Mapa: proveniência, hashchain, licenças; Drive: recibo de fonte |
| `SRC-ATT-ATLAS-001` | Atlas de domínios: matemática, física, biologia, IA, consciência, engenharia, termodinâmica, geometria de campos | Banco de hipóteses, definições, metáforas e relações interdomínio | Conteúdo disponível como corpus conceitual e visual; qualquer enunciado físico, biomédico, neurocientífico ou cosmológico exige fonte primária e teste próprio | Mapa: latentes e relações; Drive: corpus editorial; Papers: somente após gate científico |
| `SRC-ATT-TERMUX-001` | Fork Termux RAFCODEΦ, documentação Android/low-level e RMR | Runtime local Android e fronteira de execução móvel | Código e documentação presentes; compatibilidade Android 15/16, APK, assinatura, instalação e desempenho em dispositivo continuam dependentes de recibo de CI/dispositivo | Mapa: runtime Android; Drive: documentação e manifests; `TOKEN_VAZIO` para produção física |
| `SRC-ATT-RLL-001` | Código, dados, documentação e livro do Relativity Living Light | Programa científico falsificável e pipeline de cosmologia | O snapshot declara status `Sintético`, com trilha `Parcial real` em andamento e sem validação real concluída; não elevar a resultado observacional sem recibo de execução | Mapa: claims científicos, datasets, falsificadores; Drive: fontes/papers; RLL: execução reproduzível |
| `SRC-ATT-RAFBROWSER-001` | RAFBROWSER Enterprise v1: C/ASM, TLS, TCP, SHA-256, X25519, ChaCha20 | Protótipo de stack de rede baixo nível | O próprio README declara `Prototype Advanced (3.5/5)` e enumera gaps de cadeia de certificado, AES-GCM, vetores RFC e fechamento de build | Mapa: segurança/runtime; Drive: protótipo; `TOKEN_VAZIO` para uso seguro de produção |
| `SRC-ATT-RAFBROWSER-002` | Variante RAFBROWSER com CI, autenticação, HTTP, TLS e assembly | Snapshot paralelo de implementação | Há código e workflow declarados; não houve build, execução de CI nem teste contra serviços reais neste ciclo | Mapa: comparação de variantes; Drive: snapshot técnico; credenciais reais nunca entram no corpus |

## 5. Contradições e lacunas preservadas

| ID | Observação | Estado | Próximo teste verificável |
| --- | --- | --- | --- |
| `GAP-B3-001` | `FORK_NOTES.md` diz que o core BLAKE3 permanece inalterado; `RELATORIO_AUDITORIA.md` informa 40 arquivos divergentes na árvore `CORE`. | `TOKEN_VAZIO` | Reproduzir `git diff` contra o commit upstream citado e classificar cada alteração como código, build, documentação ou metadado. |
| `GAP-TORA-001` | Documentação descreve conversão, equivalência e suporte multi-ISA; o snapshot não foi compilado nem os alvos foram inicializados neste ciclo. | `TOKEN_VAZIO` | Build limpo por ABI, testes de equivalência e recibo de benchmark com ambiente completo. |
| `GAP-ATLAS-001` | O Atlas contém fórmulas, correlações e leituras de imagens; parte delas é apresentada sem dados, bibliografia primária ou protocolo experimental correspondente. | `TOKEN_VAZIO` | Transformar cada item em definição, hipótese ou metáfora; anexar fonte, unidade, previsão e falsificador quando claim físico/científico. |
| `GAP-TERMUX-001` | Compatibilidade, page size e otimizações Android são declaradas no snapshot, mas faltam recibos de APK assinado, instalação e teste físico desta versão. | `TOKEN_VAZIO` | Executar CI/build, verificar assinatura e registrar teste em aparelho com ABI/API identificadas. |
| `GAP-RLL-001` | O snapshot se define como sintético/parcial real; não sustenta conclusão observacional final por si só. | `TOKEN_VAZIO` | Rodar pipeline com dados reais versionados, baseline ΛCDM, métricas, cadeias de custódia e revisão independente. |
| `GAP-RAFBROWSER-001` | TLS/HTTPS de produção não pode ser inferido da presença de arquivos C/ASM ou de README. | `TOKEN_VAZIO` | Build limpo, vetores RFC, validação de certificados/hostname/data, análise estática e teste de integração isolado sem credenciais reais. |

## 6. Relações que entram no Mapa

```text
Atlas ──conceptual_source──> latentes de matemática/física/IA/biologia
Tora ──implementation_source──> compilação determinística e benchmark
BLAKE3 ──cryptographic_boundary──> digest de conteúdo
RMR ──external_execution_custody_layer──> recibos e estado de execução
Termux RAFCODEΦ ──android_runtime_source──> execução local sob demanda
RLL ──scientific_program_source──> claims cosmológicos falsificáveis
RAFBROWSER ──prototype_security_source──> experimentos de rede baixo nível
```

RMR não é renomeação de BLAKE3, e cópias Atlas não são evidência independente. A relação correta é **camada externa de custódia** em torno de um primitivo criptográfico, preservando autoria, licença e validação próprias.

## 7. Política de promoção

1. `digest confirmado` prova a identidade do arquivo recebido, não a veracidade do seu conteúdo.
2. `código lido` prova presença de implementação, não build, teste nem comportamento em hardware.
3. `documentação` prova intenção, especificação ou relato, não desempenho ou resultado externo.
4. `imagem/símbolo` pode gerar latente e hipótese; não substitui observação, unidade, dataset ou falsificador.
5. Para qualquer claim novo: `claim_allowed=false` até haver fonte, execução/reprodução, métrica, limite e falsificador ligados ao mesmo source object.

## 8. Próxima sequência auditável

1. Importar este manifest no Mapa como source objects, aliases e gaps.
2. Associar cada fonte a um commit verificado do repositório de origem, quando existir.
3. Selecionar um único alvo executável por camada: Tora, BLAKE3/RMR, Termux, RLL ou RAFBROWSER.
4. Produzir recibo `ambiente → comando → saída → digest → decisão` antes de promover qualquer claim de funcionamento ou vantagem de mercado.

\[
R_3=\langle F_{ok}:\text{fontes deduplicadas e custodiadas},\;F_{gap}:\text{execuções e validações},\;F_{next}:\text{source object → recibo reproduzível}\rangle
\]
