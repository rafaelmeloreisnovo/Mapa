# RAFAELIA — Universal Indexing and Governance Execution Protocol V1

**Estado:** CANONICAL_DRAFT  
**Escopo:** todos os repositórios, organizações, objetos, modelos e situações  
**Modo:** execução técnica-operacional; não reprodução textual de normas  
**claim_allowed:** false

## Princípio

A indexação não possui tema único. Cada objeto deve ser tratado conforme sua natureza, autoridade, sensibilidade, versão, evidência e dependências.

As boas práticas normativas são aplicadas no procedimento — rastreabilidade, segregação de funções, controle de alterações, minimização de dados, revisão, rollback, evidência e gestão de risco — sem transformar cada repositório em um depósito de textos normativos.

## Fluxo operacional universal

```text
DISCOVER
→ IDENTIFY
→ CLASSIFY
→ ADDRESS
→ VERSION
→ HASH_WHEN_BYTES_EXIST
→ MAP_AUTHORITY
→ MAP_PRIVACY_AND_RISK
→ MAP_DEPENDENCIES
→ VERIFY_EVIDENCE
→ RECORD_CHANGE
→ DEFINE_NEXT_GATE
→ APPEND_RECEIPT
```

## Classes de objetos

- organização, repositório, branch, tag, commit, PR e release;
- diretório, arquivo, documento, dataset, schema e índice;
- código, build, pacote, artifact, imagem, APK, ELF, DEX e container;
- workflow, run, job, check, log, benchmark e receipt;
- claim, hipótese, interpretação, modelo autoral e evidência;
- segredo, dado pessoal, conteúdo privado, licença e obrigação;
- dependência, predecessor, derivação, duplicata, conflito e lacuna.

## Registro mínimo por objeto

```yaml
object_id: stable local identity
source_system: GitHub | Drive | local | external
locator: path, URL, provider ID or ref
object_type: typed class
authority_primary: source of truth for this class
authority_secondary: mirrors or indices
visibility: public | private | restricted | unknown
sensitivity: public | internal | confidential | secret | personal_data | unknown
version_identity: commit, revision, tag, release or provider version
content_hash: real hash or TOKEN_VAZIO_HASH
lineage_parent: predecessor or TOKEN_VAZIO
relation_type: exact typed relation
epistemic_state: KNOWS | FELTS | TOKEN_VAZIO | CONTRADICTED | REFUTED | UNKNOWN_UNKNOWN
change_state: new | unchanged | modified | superseded | removed_reference | access_blocked
risk: critical | high | medium | low
blocking_dependency: typed blocker
next_gate: next verifiable action
claim_allowed: false by default
```

## Governanças aplicadas na execução

### Dados

- identidade estável e proveniência;
- qualidade e completude declaradas;
- deduplicação por bytes e linhagem, não por nome;
- retenção da fonte e transformação reversível;
- minimização de cópias e exposição.

### Versionamento, releases e alterações

- ref imutável sempre que disponível;
- predecessor e sucessor explícitos;
- changelog não substitui commit/tag;
- release não substitui artifact/hash;
- alteração deve possuir motivo, escopo, risco, rollback e receipt;
- nenhuma escrita direta destrutiva na branch padrão.

### Privacidade e segurança

- não copiar segredo, token, credencial ou dado pessoal para índice público;
- registrar incidente sem reproduzir o conteúdo sensível;
- limitar metadados ao necessário;
- separar índice público de ledger privado/restrito;
- ruptura de custódia bloqueia promoção e expansão.

### Evidência e claims

- código não equivale a execução;
- execução não equivale a validade universal;
- workflow existente não equivale a run;
- run sem artifact/log suficiente não equivale a receipt completo;
- claim permanece bloqueado até fechar o gate correspondente.

### Próximos passos

Cada lacuna deve ser convertida em ação verificável com autoridade, dependência, risco e critério de saída. `TOKEN_VAZIO` preserva a lacuna; não a mascara.

## Camadas de indexação

```text
L0 identidade e localização
L1 documentação e declaração
L2 estrutura e conteúdo
L3 versão, mudança e release
L4 execução, artifact e receipt
L5 autoridade, privacidade e risco
L6 dependências e impacto
L7 evidência e estado epistemológico
L8 próximo gate e decisão
```

## Política de escrita

### Pode ser registrado diretamente em branch de trabalho

- índices derivados;
- manifests e catálogos;
- receipts de leitura;
- mapas de autoridade e dependência;
- filas de revisão e pendências;
- correções aditivas que não alterem fonte produtora.

### Requer revisão específica

- mudança em README/AGENTS/MCP do repositório produtor;
- alteração de autoridade canônica;
- publicação de conteúdo privado;
- workflow novo ou mudança operacional;
- release, tag, merge, instalação ou migração;
- qualquer mudança irreversível ou com impacto externo.

## Métricas permitidas

- cobertura de objetos classificados;
- percentual com identidade imutável;
- percentual com hash real;
- objetos órfãos;
- relações sem tipo;
- conflitos de autoridade;
- referências quebradas;
- lacunas por risco;
- deltas por versão.

Métricas estatísticas de processo só são calculadas quando as condições de medição são válidas.

## Resultado esperado

Uma arquitetura navegável em que qualquer humano ou IA possa responder:

```text
O que é?
Onde está?
Qual versão?
De onde veio?
Quem possui autoridade?
Qual sensibilidade?
O que mudou?
Qual evidência existe?
Do que depende?
Qual risco?
Qual próximo passo?
```

## F_next

Aplicar este protocolo a cada repositório por lotes, usando os documentos Markdown apenas como uma das portas de entrada e cruzando-os com o estado material do repositório.
