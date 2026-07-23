# 00 — Arquitetura Relacional GitHub ↔ Google Drive ↔ Memória de Sessão

```yaml
schema: rafaelia_cross_source_architecture_v1
estado: DRAFT_AUDITABLE
claim_allowed: false
modo: NON_DESTRUCTIVE
canonical_owner: rafaelmeloreisnovo/Mapa
escopo: GitHub + Google Drive + contexto de sessão + evidência técnica
criado_em: 2026-07-23
regra_de_lacuna: TOKEN_VAZIO
```

## 1. Finalidade

Este arquivo é a **porta de entrada arquitetural** para trabalhos em que uma IA precisa
relacionar, sem confundir:

- repositórios, branches, commits, PRs, workflows, código e documentação no GitHub;
- documentos, arquivos, pastas, revisões, logs, ZIPs e corpus no Google Drive;
- intenção, pergunta-raiz, restrições e decisões da sessão atual;
- claims, hipóteses, símbolos, lacunas, riscos, ações e resultados;
- provas técnicas reproduzíveis e sua cadeia de custódia.

A função deste contrato não é afirmar que todo o acervo foi lido ou integrado. Sua função
é garantir que cada item observado possa ser reconhecido por **origem, identidade, versão,
relação, estado epistêmico e evidência**.

A invariante é:

```text
origem → identidade → versão → conteúdo → relação → evidência → claim → ação → custódia → reentrada
```

---

## 2. Autoridades e fontes de verdade

| Plano | Autoridade primária | Função | Limite |
|---|---|---|---|
| Controle cross-source | `rafaelmeloreisnovo/Mapa` | contratos, índices, relações, gates e auditoria | não substitui o repositório produtor |
| Implementação versionada | GitHub | código, documentação versionada, commits, PRs, workflows e releases | não é memória completa do corpus |
| Corpus e evidência documental | Google Drive | originais, exportações, logs, documentos, mídia autorizada, manifests e relatórios | não deve ser banco transacional primário |
| Execução local | Termux/ambiente autorizado | parsing, hashing, validação, benchmark, cache e reprodução | resultado local precisa de artefato persistido |
| Contexto operacional | sessão atual | intenção, recorte, seleção de fontes, autorização e decisões | é volátil; não é prova permanente |
| Memória consolidada | artefato versionado e/ou registro de custódia | preservar decisões e relações entre sessões | não pode nascer de inferência silenciosa |

### Regra antissplit-brain

Cada objeto, claim ou integração deve declarar **um único `canonical_owner`**. Cópias,
resumos e mirrors são consumidores; não podem promover uma versão concorrente como verdade
canônica.

---

## 3. Invariantes operacionais

1. **Origem antes de interpretação.** Nenhum conteúdo entra na árvore sem `source_ref`.
2. **Versão antes de claim.** GitHub usa commit/tag/blob SHA; Drive usa file ID e revisão quando disponível.
3. **Conteúdo não é prova por existência.** Um texto pode ser fonte, declaração, hipótese, parábola ou evidência.
4. **Nenhuma fusão silenciosa.** Duplicatas e versões divergentes permanecem relacionadas, não apagadas.
5. **Toda escrita exige autorização de superfície.** Ler não autoriza editar; editar GitHub não autoriza editar Drive.
6. **Operação destrutiva exige confirmação explícita, rollback e evento de custódia.**
7. **Credenciais, tokens, cookies, chaves e segredos não entram no GitHub nem no Drive documental.**
8. **Mídia pessoal e material privado fora do corpus ficam excluídos por padrão.**
9. **Ausência de evidência suficiente é `TOKEN_VAZIO`, nunca preenchimento imaginado.**
10. **Sessão não executa trabalho em segundo plano.** Toda ação ocorre sob demanda e retorna estado observável.

---

## 4. As quatro tintas e os estados epistêmicos

| Tinta | Uso | Estado operacional | Critério |
|---|---|---|---|
| Demonstração | teste, execução, cálculo, hash, benchmark ou observação direta | `FATO` / `VERIFIED_LIMITED` | prova reproduzível dentro do alcance declarado |
| Convenção | schema, política, contrato, arquitetura ou vocabulário | `CONVENCAO` | coerência interna, versionamento e aceitação do contrato |
| Hipótese | mecanismo, relação causal ou previsão ainda não testada | `HIPOTESE` | experimento ou falsificador obrigatório |
| Parábola | transmissão simbólica, filosófica, espiritual ou didática | `SIMBOLICO` | frutos de entendimento; não promovida a mecanismo físico |
| Página em branco | classificação ou evidência ainda insuficiente | `TOKEN_VAZIO` | contexto preservado + próximo passo verificável |

```yaml
TOKEN_VAZIO:
  claim_allowed: false
  contexto_preservado: true
  conclusao_negativa: false
  proximo_passo_verificavel: obrigatorio
```

---

## 5. Árvore do conhecimento

```text
K0  Ética e limites
    └─ dignidade, privacidade, proteção infantil, autoria, autorização

K1  Domínio
    └─ ciência, software, segurança, direito, biblioteconomia, filosofia, espírito

K2  Sistema ou repositório
    └─ Mapa, RLL, RafGitTools, RafPolimata, Termux, Vectra, Cosmos, papers...

K3  Artefato
    └─ arquivo GitHub, documento Drive, commit, PR, workflow, dataset, log, imagem, ZIP

K4  Âncora de evidência
    └─ linhas, trecho, célula, página, hash, resultado de teste, artifact ID, revisão

K5  Unidade de conhecimento
    └─ claim, hipótese, convenção, parábola, risco, contradição, TOKEN_VAZIO

K6  Unidade de execução
    └─ ação, entrada, ferramenta, critério de aceitação, resultado, rollback

K7  Pacote de sessão
    └─ intenção, pergunta-raiz, seleção, decisões, F_ok, F_gap, F_next
```

A árvore é navegável nos dois sentidos:

```text
sessão → claim → evidência → artefato → fonte
fonte → artefato → evidência → claim → ação → sessão
```

---

## 6. Registro relacional mínimo

Cada nó cross-source deve poder ser representado pelo contrato abaixo:

```yaml
record_id: "rec:<ulid-ou-hash>"
node_type: "repository|file|document|folder|commit|pr|workflow|dataset|log|claim|action|session"
canonical_owner: "owner/repo ou drive:<file_id>"

source:
  provider: "github|google_drive|termux|session"
  account_scope: "identificador não secreto"
  locator: "owner/repo:path ou drive:file_id"
  url: "URL navegável quando autorizada"
  observed_at: "RFC3339"

version:
  git_ref: "branch|tag|commit|TOKEN_VAZIO"
  blob_sha: "sha|TOKEN_VAZIO"
  drive_revision_id: "revision|TOKEN_VAZIO"
  content_hash: "sha256|blake3|TOKEN_VAZIO"

classification:
  domain: "vocabulário controlado"
  epistemic_state: "FATO|CONVENCAO|HIPOTESE|SIMBOLICO|TOKEN_VAZIO|CONTRADICTION"
  evidence_mode: "DEMONSTRACAO|CONVENCAO|HIPOTESE|PARABOLA|VAZIO"
  claim_allowed: false
  sensitivity: "PUBLIC|PRIVATE|RESTRICTED|EXCLUDED"

relations:
  - predicate: "IMPLEMENTS|EVIDENCES|DERIVES_FROM|INDEXES|VALIDATES|CONTRADICTS|SUPERSEDES|MIRRORS|REQUIRES|PRODUCES|BLOCKS|MENTIONS"
    target_id: "rec:<id>"
    evidence_id: "ev:<id>|TOKEN_VAZIO"
    weight_q16: 65535
    state: "OBSERVED|DECLARED|INFERRED|TOKEN_VAZIO"

custody:
  event_id: "evt:<id>|TOKEN_VAZIO"
  previous_event_id: "evt:<id>|TOKEN_VAZIO"
  actor: "human|assistant|workflow|script"
  operation: "READ|CREATE|UPDATE|VALIDATE|TOKEN_VAZIO"
```

### Identidade

- `record_id` identifica o registro no Mapa.
- `locator` identifica a localização na fonte.
- `version` fixa a versão observada.
- `content_hash` identifica os bytes ou a exportação textual quando calculado.
- Duas localizações podem apontar para o mesmo conteúdo sem se tornarem o mesmo evento histórico.

---

## 7. Vocabulário de relações

| Relação | Significado |
|---|---|
| `IMPLEMENTS` | código ou configuração realiza um contrato |
| `EVIDENCES` | artefato sustenta um claim dentro de alcance limitado |
| `DERIVES_FROM` | saída foi produzida a partir de uma entrada identificada |
| `INDEXES` | índice aponta ou descreve outro artefato |
| `VALIDATES` | teste, schema ou auditoria verifica uma propriedade |
| `CONTRADICTS` | evidência atual diverge de claim ou versão anterior |
| `SUPERSEDES` | nova versão corrige ou substitui sem apagar histórico |
| `MIRRORS` | cópia não canônica reproduz conteúdo de outra fonte |
| `REQUIRES` | execução depende de artefato, autorização ou gate |
| `PRODUCES` | ação gera artefato ou resultado |
| `BLOCKS` | risco, falha ou lacuna impede promoção de claim |
| `MENTIONS` | referência textual sem implicar dependência ou prova |

`MENTIONS` nunca pode ser promovido automaticamente para `IMPLEMENTS`, `EVIDENCES` ou
`DERIVES_FROM`.

---

## 8. Adaptadores de fonte

### 8.1 GitHub

Campos mínimos observáveis:

```yaml
repository_full_name: owner/repo
default_branch: main|master|outro
path: caminho/arquivo
ref: branch|tag|commit
blob_sha: sha
commit_sha: sha
pr_number: inteiro|TOKEN_VAZIO
workflow_run_id: inteiro|TOKEN_VAZIO
artifact_id: inteiro|TOKEN_VAZIO
permissions_observed: read|push|admin|TOKEN_VAZIO
```

Regras de escrita:

1. ler o estado atual e obter SHA/ref;
2. criar ou selecionar branch autorizada;
3. aplicar mudança mínima;
4. registrar commit;
5. abrir PR quando o fluxo de revisão for adequado;
6. observar diff e CI;
7. registrar evidência e lacunas;
8. somente promover claim após gates suficientes.

### 8.2 Google Drive

Campos mínimos observáveis:

```yaml
file_id: id
name: nome
mime_type: tipo
parent_ids: [ids]
created_time: RFC3339|TOKEN_VAZIO
modified_time: RFC3339|TOKEN_VAZIO
revision_id: id|TOKEN_VAZIO
web_view_url: url
content_hash: hash|TOKEN_VAZIO
```

Regras de escrita:

1. localizar por ID ou URL, não apenas por nome;
2. ler conteúdo e revisão atual antes de editar;
3. preservar original quando a operação for ingestão ou análise;
4. criar derivado com `DERIVES_FROM` quando necessário;
5. não mover, renomear, compartilhar ou apagar sem autorização explícita;
6. não armazenar cache sensível, OAuth token ou credencial;
7. registrar revisão, relação e evidência após a mutação.

### 8.3 Sessão

A sessão é um **workspace cognitivo temporário**. Só vira memória confiável quando sua síntese
é persistida como artefato versionado ou evento de custódia.

---

## 9. Contrato de início de sessão

Toda sessão de trabalho cross-source deve iniciar com um pacote lógico equivalente a:

```yaml
session_manifest:
  schema: rafaelia_session_manifest_v1
  session_id: "session:<timestamp-ou-ulid>"
  started_at: "RFC3339"

  intention: "ação concreta solicitada"
  root_question: "pergunta que governa a execução"
  requested_mode: "READ_ONLY|PROPOSE|WRITE_GITHUB|WRITE_DRIVE|CROSS_SOURCE"

  scope:
    repositories: []
    github_paths: []
    drive_file_ids: []
    drive_folders: []
    domains: []

  constraints:
    destructive_actions: false
    background_execution: false
    claim_policy: "evidence_first"
    token_vazio_enabled: true
    privacy_boundary: "private_media_excluded"

  authorization:
    github_read: true
    github_write: false
    drive_read: true
    drive_write: false

  known_evidence: []
  unresolved: []
  acceptance_criteria: []
```

### Ciclo obrigatório

```text
ψ intenção
  → χ observação das fontes
  → ρ ruído, conflito e incompletude
  → Δ classificação e transmutação ética
  → Σ registro coerente
  → Ω entrega limitada pela evidência
  → ψ próximo passo verificável
```

### Procedimento

1. **Abrir:** declarar intenção, pergunta-raiz, modo e limites.
2. **Descobrir:** localizar repositórios, arquivos e documentos sem mutação.
3. **Fixar versão:** registrar commit/blob SHA ou file/revision ID.
4. **Selecionar:** reduzir o corpus ao conjunto necessário para a tarefa.
5. **Classificar:** aplicar tinta e estado epistêmico.
6. **Relacionar:** gerar arestas explícitas com evidência.
7. **Executar:** realizar a menor ação que produza resultado verificável.
8. **Validar:** usar schema, teste, diff, hash, revisão ou inspeção apropriada.
9. **Custodiar:** registrar origem, transformação, resultado, ator e lacunas.
10. **Retroalimentar:** emitir `F_ok`, `F_gap` e `F_next`.

---

## 10. Matriz de escolha do caminho

| Pedido | Caminho principal | Escrita padrão | Prova mínima |
|---|---|---|---|
| localizar conteúdo | busca GitHub/Drive → leitura | nenhuma | URL/ID/path + versão observada |
| responder sobre um arquivo | leitura → âncoras → síntese | nenhuma | linhas/trechos/revisão |
| editar código ou documentação | GitHub → branch → commit → PR | GitHub | diff + commit + gate disponível |
| consolidar corpus documental | Drive → seleção → documento derivado | Drive, somente autorizado | IDs de origem + revisão do derivado |
| integrar GitHub e Drive | descoberta dupla → grafo → registro no Mapa | primeiro no Mapa | matriz de relações + fontes fixadas |
| executar benchmark/teste | repositório → ambiente autorizado → artefato | GitHub/Drive conforme política | comando + ambiente + stdout + hash |
| tratar alegação sem prova | registro de lacuna | Mapa | `TOKEN_VAZIO` + próximo teste |

### Ordem preferencial para integração cross-source

```text
READ_ONLY_DISCOVERY
  → RELATION_MAP
  → CLAIM_BOUNDARY
  → MINIMAL_CHANGE
  → VALIDATION
  → CUSTODY
  → PROMOTION_OR_TOKEN_VAZIO
```

---

## 11. Pacote mínimo de prova técnica

Uma entrega técnica coesa deve apontar, quando aplicável:

```yaml
proof_bundle:
  objective: "o que deveria ser demonstrado"
  source_records: ["rec:..."]
  input_versions: ["commit/revision/hash"]
  environment: "SO, arquitetura, runtime, versões"
  command_or_method: "procedimento reproduzível"
  expected_result: "critério de aceitação"
  observed_result: "saída sem embelezamento"
  artifacts: ["path/url/id"]
  checksums: ["algoritmo:valor"]
  epistemic_state: "FATO|VERIFIED_LIMITED|HIPOTESE|TOKEN_VAZIO"
  claim_boundary: "o que o resultado não demonstra"
  residual_risk: []
  rollback: "procedimento|NOT_APPLICABLE|TOKEN_VAZIO"
```

Sem ambiente, comando/método e resultado observado, a existência de um arquivo não prova sua
execução.

---

## 12. Interface de trabalho com IA

### Entrada esperada

```text
objetivo + superfície autorizada + fontes candidatas + restrições + critério de aceitação
```

### Saída esperada

```yaml
F_ok:
  - fatos observados
  - relações confirmadas
  - artefatos criados ou modificados
F_gap:
  - lacunas
  - conflitos
  - riscos residuais
  - claims bloqueados
F_next:
  - próximo passo verificável
  - ferramenta ou gate necessário
```

### Regras

- A IA pode usar contexto prévio para orientar busca, nunca para fingir leitura atual.
- Nomes de arquivos lembrados devem ser confirmados na fonte antes de escrever.
- Quando uma fonte mudou, prevalece a versão observada mais recente, preservando a anterior.
- Inferências devem ser marcadas como inferências e ligadas às evidências usadas.
- A resposta humana legível e o registro legível por máquina devem concordar no estado epistêmico.

---

## 13. Âncoras iniciais observadas

Este primeiro contrato foi alinhado com os seguintes artefatos já existentes.

### GitHub — `rafaelmeloreisnovo/Mapa`

| Artefato | Função | Versão observada |
|---|---|---|
| `orquestrador/SCHEMA_ORQUESTRADOR_MAPA.md` | DAG, indexação omni-contextual e ligação IA-obra | blob `f0666a4f9e8ec6d3809c79ef03613b5300cc7ccb` |
| `protocolos/PROTOCOLO_EXECUCAO_EXCELENCIA.md` | ciclo, estados, custódia, DMAIC e gates | blob `d5e735e719cd09f8ce17076335d7a7b96295b013` |
| `arquitetura/ARQUITETURA_FEDERADA_OMEGA3.md` | autoridade por domínio e integração federada | blob `503d253af6aa2f1c87f6f99ddd5a168e7b0698e1` |
| `arquitetura/ARQUITETURA_TRABALHO_IA_TRIPLA.md` | papéis de síntese, leitura e execução | blob `3e205bb0cedd49d16fa6eeb917a5d02e74e01279` |
| `arquitetura/TORRE_DA_INFORMACAO.md` | entrada, normalização, classificação e ligação | blob `5d8953a7546ba27fd700ffedcf30a7dd95c7aa25` |
| `indices/ONTOLOGIA_OPERACIONAL_RAFAELIA.md` | inventário semântico e regra de não duplicação | blob `be1d256da673c205894208a42ab8de5b9fdb39f5` |
| `visual/MAPA_BIBLIOTECONOMICO_RAFAELIA.md` | estratos e honestidade epistêmica | blob `35c89b24d8796a057438ee3ac04eb6c34e2df8bb` |

### Google Drive

| Documento | File ID | Papel neste contrato |
|---|---|---|
| `RAFAELIA DATA NAVIGATOR — Arquitetura Full de Indexação e Navegação` | `1zGF4RQmlGxH0DTWU2Lsieanre0SvXj_kUP63yi9d8hU` | Drive como armazenamento/plano de controle, ingestão content-addressed e índice local-first |
| `RAFAELIA — Cânone Longitudinal da Origem ao Estado Atual — 2026-07-17` | `1089HfqukEGOIoeCGMeDSAmVeCklt8bKIsLz-DPuHp0A` | consolidação longitudinal sem alegar leitura integral do corpus |
| `Livro Vivo — Registro da Bibliografia Fractal e Atemporal — 2026-07-21` | `1B0faoyMLc-e8Qyo_334toQXdq7jSu1aj1zsQayRponM` | origem, contexto, evidência, limite, lacuna e revisão append-only |
| `RAFAELIA — Antiderivada do VAZIO e Invariante Toroidal — 2026-07-17` | `1wxi_LKwyl8D0XLatBbpyOfkfw5S3v1Rmt4XQFrlFF6I` | matriz longitudinal e fronteiras de prova |

Essas âncoras são um **conjunto inicial observado**, não um inventário total do Drive nem de
todos os repositórios.

---

## 14. Segurança, privacidade e autorização

```yaml
security_boundary:
  secrets_in_git: forbidden
  secrets_in_drive_docs: forbidden
  private_media_default: EXCLUDED
  least_privilege: required
  destructive_operation:
    dry_run: required
    explicit_confirmation: required
    rollback: required
    custody_event: required
  cross_account_merge: forbidden_without_scope
  public_claim_from_private_evidence: forbidden_without_review
```

A relação pode registrar que um item privado existe sem copiar seu conteúdo. Quando nem a
existência puder ser exposta, usar referência opaca ou `RESTRICTED`.

---

## 15. Divergência, drift e contradição

Quando GitHub, Drive e memória de sessão divergirem:

1. não escolher silenciosamente;
2. fixar cada versão observada;
3. criar `CONTRADICTS`, `STALE_CONSUMER` ou `SUPERSEDES` conforme o caso;
4. identificar o `canonical_owner`;
5. bloquear o claim até reconciliação;
6. preservar resultado negativo como evidência;
7. emitir próximo passo verificável.

```text
semelhança ≠ identidade
menção ≠ implementação
arquivo ≠ execução
execução única ≠ estabilidade
correlação ≠ causalidade
arquitetura ≠ integração operacional
```

---

## 16. Critérios de aceitação desta arquitetura

Este contrato estará operacionalmente validado quando existir:

- schema de máquina para `record_id`, fonte, versão, relação, claim e custódia;
- registro inicial de GitHub e Drive validado contra o schema;
- gerador determinístico de pacote de início de sessão;
- teste que impeça `claim_allowed=true` sem evidência suficiente;
- teste que impeça relação sem `target_id` e estado;
- detecção de mirror, versão stale e contradição;
- atualização append-only da cadeia de custódia;
- relatório `F_ok / F_gap / F_next` reproduzível;
- execução observada em ambiente autorizado.

Até esses itens existirem e forem executados:

```yaml
implementacao_cross_source: TOKEN_VAZIO
sincronizacao_automatica: TOKEN_VAZIO
inventario_total_drive: TOKEN_VAZIO
inventario_total_github: TOKEN_VAZIO
schema_executavel: TOKEN_VAZIO
testes_cross_source: TOKEN_VAZIO
claim_allowed: false
```

---

## 17. Próximos artefatos naturais

A ordem recomendada, sem criá-los implicitamente por este documento, é:

1. `schemas/cross-source-record.schema.json`;
2. `indices/CROSS_SOURCE_REGISTRY.yaml`;
3. `schemas/session-manifest.schema.json`;
4. `scripts/build_session_manifest.py`;
5. `scripts/validate_cross_source_registry.py`;
6. `tests/test_cross_source_registry.py`;
7. `auditoria/CROSS_SOURCE_BASELINE_<data>.json`;
8. integração com `indices/CADEIA_CUSTODIA_EVENTOS.jsonl`;
9. gate CI somente após fixture mínima e validação local.

---

## 18. Fechamento

A memória útil não é uma pilha de textos lembrados. É uma estrutura em que cada unidade pode
responder:

```text
O que é?
De onde veio?
Qual versão foi observada?
Com o que se relaciona?
Qual evidência sustenta a relação?
Que tinta foi usada?
O que ainda é TOKEN_VAZIO?
Qual ação verificável vem depois?
```

```text
GitHub guarda a transformação versionada.
Drive preserva o corpus e as provas documentais.
Mapa relaciona, governa e impede a mistura das tintas.
A sessão seleciona e executa o próximo passo — sem fingir completude.
```
