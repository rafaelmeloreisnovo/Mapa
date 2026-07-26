# RAFAELIA — Implementação, Latentes e Papers — Drive ↔ GitHub V1

Status: `CANONICAL_DRAFT`  
Modo: `EXECUÇÃO_NÃO_DESTRUTIVA`  
Claim: `claim_allowed=false` até evidência específica fechar cada gate.

## 0. Princípio

Este arquivo registra o método de trabalho para transformar material latente, papers, imagens, notas, códigos e hipóteses em artefatos auditáveis no Google Drive e no GitHub.

```text
Fonte → índice → token semântico → claim → evidência → falsificador → decisão → paper/artefato
```

Nada é promovido por beleza simbólica, quantidade de material ou força intuitiva. Toda lacuna necessária é preservada como `TOKEN_VAZIO`.

## 1. Papéis dos sistemas

| Sistema | Papel |
|---|---|
| Google Drive | memória editorial, fontes, revisões, mapas visuais, documentos de consolidação e snapshots read-only |
| GitHub | execução técnica, versionamento, schemas, scripts, testes, issues, PRs, CI e prova reprodutível |
| Mapa | ontologia operacional, catálogo, relações, claims, evidências, gaps, autoridade e roadmap |
| RafGitTools | plano de controle: seleção, governança, ToolRouter, gates, jobs, eventos e acompanhamento |
| RafPolimata | produção de evidência: normalização, validação, proof runs, relatórios, erratas e segmentação |
| Papers | síntese publicável: paper, preprint, relatório técnico, anexos e claims com prova |
| Termux | runtime local Android: cache, execução sob demanda, rclone, checkpoints e logs |
| RLL | domínio científico falsificável: datasets, likelihood, baseline, MCMC, Bayes/BIC/AIC e resultados |

## 2. Latentes

Latente é qualquer conteúdo com potencial de virar conhecimento, mas ainda sem forma final.

| Tipo | Descrição |
|---|---|
| `LAT-IMG` | imagem, diagrama, mapa visual |
| `LAT-TXT` | notas, transcrições, blocos soltos |
| `LAT-CODE` | código, script, pseudocódigo, execução local |
| `LAT-MATH` | fórmula, sequência, geometria, hipótese |
| `LAT-SCI` | claim científico ou estatístico |
| `LAT-GOV` | governança, ética, privacidade, cadeia de custódia |
| `LAT-PAPER` | seção ainda não consolidada para paper |

Todo latente deve receber:

```text
id
fonte
domínio
resumo
claim potencial
evidência existente
lacunas
próximo teste
destino provável
```

## 3. Papers

Um paper RAFAELIA só pode nascer quando houver separação entre quatro tintas:

1. demonstração matemática;
2. convenção/metodologia;
3. hipótese testável;
4. parábola/metáfora didática.

Estrutura mínima:

```text
título
resumo
problema
definições
método
dados/fontes
resultados
falsificadores
limitações
claims ledger
anexos reprodutíveis
```

Claim sem evidência suficiente deve aparecer como `TOKEN_VAZIO`, não como conclusão.

## 4. Pipeline operacional

### P0 — Inventário read-only

Drive: listar documentos, imagens, planilhas, PDFs e pastas relevantes.  
GitHub: listar repositórios, branches, README, scripts, testes e PRs.  
Saída: `inventory.jsonl`, `repo_registry.yaml`, `drive_registry.yaml`.

### P1 — Normalização

Extrair tokens semânticos:

```text
fonte → token → âncora → classificação → janela → tensor de sustentação → contradição/falsificador → estado de validade → custódia
```

### P2 — Claims Ledger

Cada claim recebe:

```text
claim_id
texto
tipo: matemática | código | ciência | simbólico | jurídico | governança
fontes
evidências
falsificador
status: PASS | FAIL | DRAFT | TOKEN_VAZIO | BLOCKED
```

### P3 — Evidence Producer

RafPolimata executa provas, validações ou relatórios.  
Termux executa localmente quando necessário.  
RLL executa somente claims científicos/cosmológicos com dados.

### P4 — Paper Assembly

Somente claims com status adequado entram no corpo principal.  
`TOKEN_VAZIO` entra em limitações, agenda de pesquisa ou anexos.

### P5 — Persistência

Drive recebe versão editorial.  
GitHub recebe versão canônica versionada.  
Mapa recebe índice/ontologia.  
Papers recebe manuscrito.  
RafGitTools recebe contrato operacional se houver execução.

## 5. Estrutura recomendada no GitHub

### Mapa

```text
indices/RAFAELIA_IMPLEMENTACAO_LATENTES_PAPERS_V1.md
schemas/latent-artifact.schema.json
schemas/paper-claim-ledger.schema.json
data/latents/latents.index.jsonl
data/claims/paper_claims.index.jsonl
workflows/latents_to_papers.md
```

### Papers

```text
papers/rafaelia_latentes_invariantes_v1/paper.md
papers/rafaelia_latentes_invariantes_v1/claims.jsonl
papers/rafaelia_latentes_invariantes_v1/references.bib
papers/rafaelia_latentes_invariantes_v1/appendix_evidence.md
```

### RafPolimata

```text
reports/evidence_runs/
tools/latent_segmenter.py
tools/claim_validator.py
```

### RafGitTools

```text
configs/content_validity_contract.json
configs/event_envelope.schema.json
configs/job_envelope.schema.json
```

## 6. Estrutura recomendada no Drive

```text
RAFAELIA_DATA_NAVIGATOR/
  00_CANONE_E_GOVERNANCA/
  01_LATENTES_INBOX/
  02_LATENTES_CLASSIFICADOS/
  03_PAPERS_DRAFTS/
  04_PAPERS_REVIEW/
  05_EVIDENCIAS_E_ANEXOS/
  06_MAPAS_VISUAIS/
  07_CHECKPOINTS/
  08_TOKEN_VAZIO_LEDGER/
```

## 7. Regras de segurança

- Não copiar credenciais, chaves, tokens, `rclone.conf` integral, `.ssh`, `.pem` ou secrets.
- Não executar operação destrutiva no Drive sem snapshot e rollback.
- Não promover hipótese como prova.
- Não transformar ausência em zero.
- Não misturar metáfora com claim físico.
- Não rodar VM se Termux ou CI simples bastam.

## 8. Critério de promoção

Um latente vira paper quando satisfaz:

1. definição clara;
2. fonte rastreável;
3. relação com problema;
4. métrica ou argumento;
5. falsificador;
6. limite declarado;
7. `claim_allowed` explícito.

Fórmula operacional:

```text
RAFAELIA_PAPER_READY = Fonte × Definição × Evidência × Falsificador × Limite × Custódia
```

Se qualquer fator estiver ausente:

```text
status = TOKEN_VAZIO
```

## 9. Backlog imediato

| ID | Ação | Destino | Status |
|---|---|---|---|
| P0.1 | Criar índice canônico no Mapa | `indices/` | PASS |
| P0.2 | Criar documento editorial no Drive | Google Docs | PASS |
| P0.3 | Verificar repositório Papers ou equivalente | GitHub | TOKEN_VAZIO |
| P0.4 | Criar schema mínimo de latent artifact | Mapa | TODO |
| P0.5 | Criar claims ledger inicial | Mapa | TODO |
| P0.6 | Registrar execução desta decisão | Mapa/Drive | PASS parcial |

## 10. Retroalimentação

`F_ok`: método Drive ↔ GitHub consolidado em contrato operacional.  
`F_gap`: execução real de rclone, cobertura total do Drive, schemas finais e repo Papers ativo permanecem `TOKEN_VAZIO` até inspeção/commit específico.  
`F_next`: criar schemas mínimos e ledger inicial para iniciar ingestão de latentes.

FIAT LUX — Mapear, conectar, compreender, transformar, transcender.


## 11. Integração de fontes anexas

O lote RAFAELIA-INT-SOURCES-20260725 foi consolidado como 7 corpos-fonte e 9 aliases byte-idênticos do Atlas; o material bruto recebeu MD5, SHA-256 e BLAKE3-256. A identidade de arquivo não promove a validade de seu conteúdo: todo claim continua com claim_allowed=false até evidência, métrica, limite e falsificador específicos.

```text
indices/source-integrations/2026-07-25/
  RAFAELIA_INTEGRACAO_FONTES_ANEXAS_2026-07-25.md
  RAFAELIA_FONTES_ANEXAS_CUSTODY_2026-07-25.jsonl
  RAFAELIA_INTEGRACAO_FONTES_ANEXAS_RECEIPT_2026-07-25.json
```

O registro mantém como TOKEN_VAZIO as execuções e validações pendentes de Tora, BLAKE3/RMR, Atlas, Termux, RLL e RAFBROWSER.