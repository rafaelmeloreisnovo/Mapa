# Auditoria do lote local de contexto — 2026-07-28

**Audit ID:** `RLCB-20260728`  
**Modo:** read-only sobre o conteúdo local; registro não destrutivo; `claim_allowed=false`  
**Escopo:** somente os arquivos `.txt` montados em `/mnt/data` nesta sessão.

## 1. Medição material

| Métrica | Resultado |
|---|---:|
| Arquivos | **20** |
| Bytes | **152,698** |
| Linhas | **6,666** |
| SHA-256 únicos | **20** |
| Duplicados exatos locais | **0** |
| Zero-byte | **0** |
| Marcadores `filecite` | **189** |
| URLs brutas | **5** |
| Identificadores hexadecimais de 40 caracteres | **16** |
| Campo explícito `claim_allowed` | **0/20** |

A identidade material dos vinte arquivos está provada por SHA-256. Isso prova **qual texto foi auditado**, mas não promove automaticamente as afirmações externas contidas nesses textos.

## 2. Achados principais

### F-01 — Proveniência frágil por citações de sessão — HIGH

Foram encontrados **189 marcadores `filecite`**. Eles funcionam na interface da conversa, porém não constituem uma referência durável quando o `.txt` é movido para Drive, GitHub ou ZIPRAF. Cada marcador precisa ser convertido para um localizador persistente, por exemplo:

```text
GitHub: repo + path + commit + blob SHA
Drive: file ID + revision ID + trecho/âncora
Local: caminho + tamanho + SHA-256 + origem do snapshot
```

### F-02 — Gate epistemológico ausente — HIGH

Nenhum dos vinte documentos contém campo explícito `claim_allowed`. Neste registro, todos ficam classificados como:

```text
claim_allowed=false
canonical_authority=false
primary_source_for_external_claims=false
```

### F-03 — Texto derivado não é prova primária — MEDIUM

Os arquivos são análises, sínteses, arquiteturas, estimativas ou recibos narrados. O SHA-256 prova o documento; não prova sozinho o build, o runtime, o resultado físico ou a validade científica descritos nele.

### F-04 — Integridade local — PASS

Os vinte SHA-256 são distintos. Não há duplicação byte-idêntica nem arquivo de zero bytes no lote atual.

### F-05 — Reconciliação remota dos identificadores — PASS

Todos os **16 identificadores de 40 caracteres** foram reconciliados:

- **14 commits/caminhos** declarados para RAFAELIA Ω v3.2 foram lidos nos sete repositórios;
- **1 merge commit** da PR `RafGitTools #236` foi confirmado;
- **1 Git blob** do YAML `SAVANT_EQM_KERNEL_20250622_232945.yaml` foi confirmado.

A Ω v3.2 possui **14 colocações remotas**, mas somente **2 blobs de conteúdo únicos**:

```text
manifest blob = 25f057e00508fdc44934e1f51b19118480203af0
README blob   = ffe75dfa53fae914ac1f80dbe757ecb4df892258
```

Portanto:

```text
14 ocorrências remotas ≠ 14 conteúdos autorais distintos
14 ocorrências remotas = 2 conteúdos byte-idênticos distribuídos em 7 repositórios
```

### F-06 — Percentual percorrido — DRAFT_ESTIMATE

O valor `30% ± 5%` é uma síntese heurística útil para planejamento. Não é uma medição obtida por telemetria, cobertura de testes, grafo completo de dependências ou deduplicação integral. Deve permanecer como estimativa declarada.

### F-07 — BLAKE3 — TOKEN_VAZIO

O runtime local desta sessão não contém implementação BLAKE3. Nenhum digest alternativo foi apresentado como se fosse BLAKE3. O SHA-256 foi calculado; BLAKE3 permanece `TOKEN_VAZIO`.

## 3. Inventário por arquivo

| Arquivo | Bytes | Linhas | SHA-256 | `filecite` | Verificação remota |
|---|---:|---:|---|---:|---|
| `Análise Estrutural Rafgittools.txt` | 25768 | 995 | `ebbfe745fce04492…` | 62 | TOKEN_VAZIO |
| `Análise Google Drive.txt` | 6856 | 203 | `60f96a74ecc50f97…` | 7 | TOKEN_VAZIO |
| `Análise Omega Kernel V3.txt` | 6924 | 509 | `606354296dde3af7…` | 7 | TOKEN_VAZIO |
| `Análise de arquivo JSON.txt` | 10179 | 454 | `db669ee698045225…` | 9 | TOKEN_VAZIO |
| `Arquitetura Cognitiva Evolutiva.txt` | 5034 | 244 | `f1fda8726f14e401…` | 0 | TOKEN_VAZIO |
| `Arquitetura Omega Governança.txt` | 7313 | 513 | `b28d982409a95c2d…` | 0 | TOKEN_VAZIO |
| `Arquivos no Drive e GitHub.txt` | 5775 | 110 | `7de98b5c5a11ae42…` | 20 | PASS |
| `Auditoria ELF RAFAELIA Ω.txt` | 10106 | 484 | `3b06d632aac2d3fe…` | 0 | TOKEN_VAZIO |
| `Auditoria RAFAELIA Ω v3.2.txt` | 3023 | 49 | `815b085b2121414e…` | 14 | PASS |
| `Auditoria termux-app-rafacodephi.txt` | 15259 | 678 | `884716d37d9ba405…` | 36 | TOKEN_VAZIO |
| `Bare-metal Arduino Inovador.txt` | 6558 | 409 | `a4a8271cc22c5b16…` | 0 | TOKEN_VAZIO |
| `Coerência operacional e excelência.txt` | 2875 | 167 | `1a4cf89dc0b89940…` | 0 | TOKEN_VAZIO |
| `Inovação em RAFAELIA Q16.txt` | 13545 | 519 | `5d78ce888c1b2e2b…` | 0 | TOKEN_VAZIO |
| `Integração de Conhecimento Vivo.txt` | 5480 | 281 | `10845f447c92e689…` | 6 | TOKEN_VAZIO |
| `Integração de Conhecimento.txt` | 3703 | 189 | `98af737d39f59297…` | 2 | TOKEN_VAZIO |
| `Observador e Observado.txt` | 4611 | 216 | `e686c5da32a9ccdc…` | 0 | TOKEN_VAZIO |
| `Parábolas e Estruturas Narrativas.txt` | 5074 | 227 | `4a629edc143dda90…` | 5 | TOKEN_VAZIO |
| `Percentual Percorrido RAFAELIA.txt` | 5898 | 125 | `f76218dbd0cc43cf…` | 4 | TOKEN_VAZIO |
| `RafGitTools Finalização Login.txt` | 4029 | 106 | `a9e26d3dbe33adc8…` | 14 | PASS |
| `Visão ampla e arquitetura.txt` | 4688 | 188 | `5a02e435931ad673…` | 3 | TOKEN_VAZIO |

## 4. Artefatos de custódia

- `indices/consolidation/LOCAL_CONTEXT_BATCH_MANIFEST_2026-07-28.jsonl`
- `resultados/LOCAL_CONTEXT_BATCH_RECEIPT_2026-07-28.json`
- SHA-256 do manifesto: `942941bc78bd6ed36723d87f1657861db84cf5293171f2af7b2a1c014254fed5`
- SHA-256 do receipt: `86edf0ebd3de01fabbc1534df586dcc5ad378648d4e83fc0beda39f1ba5387b3`

## 5. Gate seguinte

```text
filecite de sessão
→ localizador durável
→ claim atômico
→ fonte primária
→ falsificador
→ status
→ claim_allowed
```

Até esse gate, o lote é **registrado e auditado**, mas não é promovido como prova integral das afirmações externas.

## Retroalimentação

- **F_ok:** identidade dos 20 documentos fechada; 16/16 identificadores remotos reconciliados; duplicação externa Ω v3.2 quantificada.
- **F_gap:** 189 citações não duráveis; BLAKE3 ausente; revisão de sensibilidade e ledger atômico ainda incompletos.
- **F_next:** substituir citações de sessão por proveniência persistente e continuar o manifesto transversal Drive ↔ GitHub ↔ snapshots.
