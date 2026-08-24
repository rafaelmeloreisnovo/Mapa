# RAFAELIA — Risk Observation Ledger V1

Status: `DERIVED | APPEND_ONLY | CLAIM_BLOCKED_BY_DEFAULT`
Data: `2026-08-24`
Escopo: material observado no bootstrap canônico do GitHub e no índice canônico do Google Drive.
Objetivo: reduzir risco operacional convertendo observações em registros auditáveis, versionados e reversíveis, sem promover inferência a fato.

## 0. Invariantes de segurança

1. Fonte bruta/canônica permanece imutável neste fluxo.
2. Toda observação deve carregar proveniência e revisão verificável quando disponível.
3. `OBSERVED != DERIVED != CLAIM`.
4. Ausência ou insuficiência de evidência = `TOKEN_VAZIO`.
5. Nenhum `CLAIM` é permitido sem fechamento dos gates canônicos aplicáveis.
6. Toda mutação derivada deve ser reversível e feita fora da fonte canônica.
7. Correções são append-only: um registro novo pode `SUPERSEDE` o anterior, mas não apaga a cadeia histórica.
8. Segredos, credenciais, identificadores privados não necessários e dados pessoais não pertinentes ficam fora deste ledger.
9. `VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM`.
10. Heurística, metáfora ou semelhança semântica nunca substituem prova.
11. Este ledger complementa controles existentes; não cria uma governança paralela.

## 1. Estados

- `OBSERVED`: diretamente lido/recuperado de uma fonte identificada.
- `DERIVED`: transformação ou inferência explicitamente derivada de observações.
- `TOKEN_VAZIO`: evidência insuficiente, acesso ausente ou estado ainda não verificável.
- `CLAIM_CANDIDATE`: registro que satisfaz a pré-checagem deste ledger e pode seguir aos gates canônicos; não equivale a claim autorizado.
- `SUPERSEDED`: registro histórico preservado, substituído por registro mais recente e verificável.

## 2. Classes de risco

| Classe | Risco | Controle mínimo |
|---|---|---|
| `R0` | informacional | registrar |
| `R1` | ambiguidade / deriva semântica | delimitar termos + fonte |
| `R2` | proveniência / versão | capturar revisão/hash |
| `R3` | mutação / overwrite | branch isolada + nova rota + rollback |
| `R4` | conflito / inconsistência entre índices | varredura de contradições + supersession explícita |
| `R5` | segurança / privacidade / segredo | minimização + exclusão + revisão antes de publicação |

## 3. Esquema mínimo de cada observação

Este esquema é uma visão de ingestão. Se o registro virar evento de custódia, deve ser projetado no contrato canônico `schemas/cadeia_custodia_evento.schema.json` e encadeado em `indices/CADEIA_CUSTODIA_EVENTOS.jsonl`.

```yaml
record_id:
timestamp:
source_system:
source_locator:
source_revision:
observation:
state:
evidence:
derivation:
risk_class:
risk_reason:
mitigation:
gap:
next_gate:
supersedes:
receipt:
claim_allowed: false
```

## 4. Pré-gate de ingestão — não substitui o gate canônico

Os controles abaixo são filtros locais deste ledger. Eles existem para impedir que observação incompleta avance como material confiável:

- `G0 SOURCE_REACHABLE`: fonte recuperável.
- `G1 REVISION_CAPTURED`: locator + revisão/hash exatos quando o provedor expõe versão.
- `G2 STATE_CLASSIFIED`: `OBSERVED`, `DERIVED` ou `TOKEN_VAZIO` explícito.
- `G3 ASSERTION_SUPPORTED`: evidência sustenta exatamente a afirmação feita.
- `G4 CONTRADICTION_SCAN`: conflitos relevantes foram procurados e registrados.
- `G5 REVERSIBILITY`: qualquer mutação é isolada e reversível.
- `G6 SECURITY_PRIVACY`: não há segredo/dado privado desnecessário no artefato público.

`G0..G6 = PASS` significa apenas `READY_FOR_CANONICAL_GATE`.

A resolução de `TOKEN_VAZIO` continua subordinada a `docs/governance/TOKEN_VAZIO_APPROVAL_WORKFLOWS_V1.md`, cujo modelo observado é:

```text
Gate 1 — Evidence Gathering
Gate 2 — Validation & Falsification
Gate 3 — Approval & Integration
→ CANONICAL_TOKEN_RESOLVED
```

`claim_allowed=false` permanece até a aprovação final prevista pela governança canônica.

## 5. Registros iniciais observados

### OBS-20260824-001 — Índice canônico do Drive versionado

```yaml
record_id: OBS-20260824-001
timestamp: 2026-08-24
source_system: Google Drive
source_locator: "RAFAELIA — Implementação Latentes e Papers — Drive GitHub V1.txt"
source_revision: "296"
previous_revision: "295"
observation: "A fonte canônica foi alcançada e sua revisão corrente foi obtida pelo histórico de versões do Drive."
state: OBSERVED
evidence: "Google Drive revision history: currentRevisionId=296, previousRevisionId=295"
risk_class: R2
risk_reason: "Conteúdo operacional muda ao longo do tempo; leitura sem revisão fixa pode gerar deriva de contexto."
mitigation: "Fixar a revisão observada no registro derivado e não editar a fonte canônica neste fluxo."
gap: TOKEN_VAZIO
next_gate: "Ao derivar claim específico, ligar trecho/conteúdo + revisão à autoridade correspondente."
claim_allowed: false
```

### OBS-20260824-002 — Bootstrap canônico do GitHub versionado

```yaml
record_id: OBS-20260824-002
timestamp: 2026-08-24
source_system: GitHub
source_locator: "rafaelmeloreisnovo/Mapa:bootstrap/RAFAELIA_CHATGPT_BOOTSTRAP_V1.md@main"
source_revision: "2fdb05b786f1d42db12182bc4e7023a28499cb46"
observation: "O bootstrap canônico declara APPEND_ONLY, PROVENANCE_FIRST e TOKEN_VAZIO_VALID e define a rota objetivo→autoridade→rota→evidência→gate→delta→índice."
state: OBSERVED
evidence: "blob SHA + conteúdo recuperado do caminho canônico"
risk_class: R0
risk_reason: "Baixo risco enquanto usado como roteador e não como substituto da autoridade produtora."
mitigation: "Preservar distinção entre roteamento, evidência e claim."
gap: TOKEN_VAZIO
next_gate: "Verificar autoridade produtora antes de qualquer conclusão sobre estado de implementação."
claim_allowed: false
```

### DER-20260824-003 — Ledger derivado de redução de risco

```yaml
record_id: DER-20260824-003
timestamp: 2026-08-24
source_system: GitHub
source_locator: "indices/RAFAELIA_RISK_OBSERVATION_LEDGER_V1.md"
source_revision: "branch:chatgpt/risk-ledger-canonical-alignment-20260824"
observation: "Foi criada uma camada derivada para registrar observações, riscos, evidências, lacunas e pré-gates sem alterar as fontes canônicas."
state: DERIVED
evidence: "arquivo versionado em branch corretiva isolada"
derivation: "OBS-20260824-001 + OBS-20260824-002 → controle de proveniência e mutação"
risk_class: R3
risk_reason: "Um índice derivado pode tornar-se fonte falsa se sobrescrever, ocultar ou concorrer com controles canônicos."
mitigation: "branch isolada + PR corretiva + claim_allowed=false + alinhamento explícito à cadeia de custódia e ao workflow TOKEN_VAZIO"
gap: "contradiction scan amplo com autoridades produtoras ainda TOKEN_VAZIO"
next_gate: "revisar delta e, quando necessário, projetar registros na cadeia de custódia canônica"
claim_allowed: false
```

### OBS-20260824-004 — Governança TOKEN_VAZIO existente

```yaml
record_id: OBS-20260824-004
timestamp: 2026-08-24
source_system: GitHub
source_locator: "docs/governance/TOKEN_VAZIO_APPROVAL_WORKFLOWS_V1.md"
source_revision: "cb9407a81c8a180dee9e5f61d60fe9b1993585f2"
observation: "Existe modelo canônico de 3 gates para fechamento de TOKEN_VAZIO, com falsificação, aprovação e claim_allowed=false até aprovação final."
state: OBSERVED
risk_class: R4
risk_reason: "Criar gates concorrentes fragmentaria a governança."
mitigation: "G0..G6 deste ledger são pré-gate de ingestão; fechamento continua no workflow canônico."
gap: TOKEN_VAZIO
next_gate: "usar o workflow canônico em qualquer tentativa de resolver gap"
claim_allowed: false
```

### OBS-20260824-005 — Cadeia de custódia existente

```yaml
record_id: OBS-20260824-005
timestamp: 2026-08-24
source_system: GitHub
source_locator: "governanca/CADEIA_DE_CUSTODIA_DADOS.md"
source_revision: "47634e3ce9c8da1de8343f12d055f7d4be50c64d"
observation: "Já existe contrato canônico de evento imutável, previous_event_id, supersedes_event_id, evidence, controls e next_verifiable_step."
state: OBSERVED
risk_class: R4
risk_reason: "Um receipt ad hoc paralelo duplicaria o ledger oficial."
mitigation: "usar o esquema deste documento apenas para ingestão; eventos materiais devem ser projetados no contrato canônico de custódia."
gap: "registro efetivo destes eventos no JSONL canônico ainda não realizado nesta correção"
next_gate: "materializar evento canônico somente após validar schema/elo anterior"
claim_allowed: false
```

### OBS-20260824-006 — Cross-source local não promove claim

```yaml
record_id: OBS-20260824-006
timestamp: 2026-08-24
source_system: GitHub
source_locator: "docs/CROSS_SOURCE_LOCAL_GATE.md"
source_revision: "e32fe3c6e0555b73675b7d85d9f3c18029720714"
observation: "O gate cross-source distingue reprodução estrutural local de autorização de merge/claim e mantém claim_allowed=false."
state: OBSERVED
risk_class: R0
mitigation: "preservar a mesma separação neste ledger"
gap: "execução atual do cross-source gate para este delta não foi realizada"
next_gate: "se o artefato passar a participar da superfície governada, executar o gate aplicável e anexar receipt"
claim_allowed: false
```

## 6. Receipt e cadeia de custódia

Não criar um ledger concorrente. Para mutações materiais, usar a unidade canônica descrita em `governanca/CADEIA_DE_CUSTODIA_DADOS.md`:

```text
event_id
timestamp_utc
repository / branch
actor
operation
object
previous_event_id
supersedes_event_id
epistemic_state
claim_allowed
evidence
controls
sigma
next_verifiable_step
```

Regras herdadas:

- cada evento é imutável;
- correção usa `CORRECT` + `supersedes_event_id`;
- evento inválido não vira âncora;
- hash ausente é `null`, nunca inventado;
- dado sensível não necessário não é duplicado no ledger.

## 7. Semântica de falha segura

Quando tempo, acesso, versão ou evidência forem insuficientes:

```text
TOKEN_VAZIO
preservar contexto
não completar por imaginação
registrar o dado ausente
registrar a próxima ação independentemente verificável
```

## 8. Ordem de redução de risco

`Fonte → Revisão → Observação → Estado → Evidência → Risco → Mitigação → Gap → Pré-gate → Gate canônico → Delta → Custódia`

A ordem impede atalhos perigosos:

- `interpretação → fato`
- `artefato criado → evidência de execução`
- `índice derivado → autoridade produtora`
- `pré-gate local → aprovação canônica`

## 9. Contradiction scan — 2026-08-24

Fontes comparadas:

- `bootstrap/RAFAELIA_CHATGPT_BOOTSTRAP_V1.md`
- `docs/governance/TOKEN_VAZIO_APPROVAL_WORKFLOWS_V1.md`
- `governanca/CADEIA_DE_CUSTODIA_DADOS.md`
- `docs/CROSS_SOURCE_LOCAL_GATE.md`

Resultado:

```yaml
parallel_governance_risk: OBSERVED
parallel_custody_risk: OBSERVED
semantic_conflict_after_alignment: NOT_OBSERVED_IN_SCANNED_SET
broad_producer_conflict_scan: TOKEN_VAZIO
claim_allowed: false
```

Correção aplicada: os gates `G0..G6` deixam de ser descritos como gate final e passam a ser pré-gate de ingestão. O receipt ad hoc é substituído por referência ao contrato canônico de cadeia de custódia.

## 10. Checklist antes de promoção

- [x] fontes canônicas não foram editadas por este fluxo
- [x] Drive possui revisão observada explícita (`296`)
- [x] bootstrap possui blob SHA explícito
- [x] `OBSERVED` separado de `DERIVED`
- [x] `TOKEN_VAZIO` preservado como estado válido
- [x] branch corretiva isolada
- [x] risco de governança paralela identificado
- [x] alinhamento com workflow TOKEN_VAZIO verificado
- [x] alinhamento com cadeia de custódia verificado
- [x] alinhamento com cross-source claim semantics verificado
- [ ] contradiction scan amplo com repositórios/autoridades produtoras
- [ ] evento de custódia canônico, se este delta for promovido
- [ ] receipt final da promoção
- [ ] somente então avaliar promoção de registros específicos

## 11. Regra de ouro

> Quanto maior a incerteza, menor deve ser a força do claim e maior a precisão da proveniência.

`Risco↓ = Proveniência↑ × Reversibilidade↑ × ReusoCanônico↑ × Gates↑ × Suposições↓`
