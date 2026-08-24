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
5. Nenhum `CLAIM` é permitido sem fechamento integral do gate.
6. Toda mutação derivada deve ser reversível e feita fora da fonte canônica.
7. Correções são append-only: um registro novo pode `SUPERSEDE` o anterior, mas não apaga a cadeia histórica.
8. Segredos, credenciais, identificadores privados não necessários e dados pessoais não pertinentes ficam fora deste ledger.
9. `VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM`.
10. Heurística, metáfora ou semelhança semântica nunca substituem prova.

## 1. Estados

- `OBSERVED`: diretamente lido/recuperado de uma fonte identificada.
- `DERIVED`: transformação ou inferência explicitamente derivada de observações.
- `TOKEN_VAZIO`: evidência insuficiente, acesso ausente ou estado ainda não verificável.
- `CLAIM_CANDIDATE`: afirmação que passou pelos gates técnicos, ainda sujeita a revisão quando aplicável.
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

## 3. Esquema mínimo de cada registro

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

## 4. Gate de evidência

- `G0 SOURCE_REACHABLE`: fonte recuperável.
- `G1 REVISION_CAPTURED`: locator + revisão/hash exatos quando o provedor expõe versão.
- `G2 STATE_CLASSIFIED`: `OBSERVED`, `DERIVED` ou `TOKEN_VAZIO` explícito.
- `G3 ASSERTION_SUPPORTED`: evidência sustenta exatamente a afirmação feita.
- `G4 CONTRADICTION_SCAN`: conflitos relevantes foram procurados e registrados.
- `G5 REVERSIBILITY`: qualquer mutação é isolada e reversível.
- `G6 SECURITY_PRIVACY`: não há segredo/dado privado desnecessário no artefato público.

Regra: somente `G0..G6 = PASS` torna um registro elegível a `CLAIM_CANDIDATE`.

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
next_gate: "Ao derivar claim específico, citar trecho + revisão que sustenta a afirmação."
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
source_revision: "branch:chatgpt/observed-risk-ledger-20260824"
observation: "Foi criada uma camada derivada para registrar observações, riscos, evidências, lacunas e gates sem alterar as fontes canônicas."
state: DERIVED
evidence: "arquivo novo em branch isolada"
derivation: "OBS-20260824-001 + OBS-20260824-002 → controle de proveniência e mutação"
risk_class: R3
risk_reason: "Um índice derivado pode tornar-se fonte falsa se sobrescrever ou ocultar as fontes canônicas."
mitigation: "novo caminho + branch isolada + PR + claim_allowed=false por padrão"
gap: "revisão humana/diff antes de merge"
next_gate: "abrir PR e revisar o delta"
claim_allowed: false
```

## 6. Receipt de mutação

Para cada escrita derivada, registrar:

```yaml
before_ref:
action:
after_ref:
branch:
timestamp:
rollback:
reason:
evidence_delta:
```

Uma escrita sem `before_ref` ou sem rollback fica em `TOKEN_VAZIO` para claim.

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

`Fonte → Revisão → Observação → Estado → Evidência → Risco → Mitigação → Gap → Gate → Delta → Receipt`

A ordem impede dois atalhos perigosos:

- `interpretação → fato`
- `artefato criado → evidência de execução`

## 9. Checklist antes de merge

- [x] fontes canônicas não foram editadas por este fluxo
- [x] Drive possui revisão observada explícita (`296`)
- [x] bootstrap possui blob SHA explícito
- [x] `OBSERVED` separado de `DERIVED`
- [x] `TOKEN_VAZIO` preservado como estado válido
- [x] branch de trabalho isolada
- [ ] diff do PR revisado
- [ ] contradições com índices produtores verificadas
- [ ] receipt final do merge registrado
- [ ] somente então avaliar promoção de registros específicos

## 10. Regra de ouro

> Quanto maior a incerteza, menor deve ser a força do claim e maior a precisão da proveniência.

`Risco↓ = Proveniência↑ × Reversibilidade↑ × Gates↑ × Suposições↓`
