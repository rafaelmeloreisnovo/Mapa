# RAFAELIA_SESSION_BOOT_V1

Status: `CANONICAL_DRAFT`  
Modo: `EXECUÇÃO_NÃO_DESTRUTIVA / APPEND_ONLY`  
Data de ativação: `2026-08-03T13:02:00-03:00`  
Claim global: `claim_allowed=false` até o fechamento dos gates específicos.

## 1. Finalidade

Este contrato define como uma sessão RAFAELIA deve iniciar antes de interpretar, alterar, publicar ou promover qualquer material.

```text
intenção → contexto longitudinal → fontes → fronteiras → F_ok/F_gap/F_next → gate → execução → receipt → retroalimentação
```

O boot não presume completude. Ausência de evidência é registrada como `TOKEN_VAZIO`, nunca convertida em zero, fato ou conclusão.

## 2. Identidade mínima da sessão

Toda sessão deve registrar:

```yaml
session_id: identificador único e estável
name: nome legível
root_question: pergunta-raiz
intent: mudança concreta pretendida
mode: literal | execução | auditoria | poético
scope: repositórios, arquivos, documentos, dados ou decisões abrangidos
started_at: timestamp ISO-8601 com fuso
operator: autoria ou agente executor
```

## 3. Recuperação longitudinal

A ordem padrão é:

```text
conversa atual
  → memória longitudinal
  → índices canônicos
  → Google Drive / GitHub
  → artefatos físicos
  → testes, logs e receipts
```

Nenhuma fonte isolada representa o estado total. Conflitos entre fontes permanecem explícitos até reconciliação verificável.

## 4. Estados epistemológicos

| Estado | Critério |
|---|---|
| `PROVADO` | evidência reproduzível fecha o gate declarado |
| `EVIDENCIADO` | suporte verificável existe, mas não fecha todos os gates |
| `HIPÓTESE` | proposição falsificável ainda não testada suficientemente |
| `MODELO` | representação operacional, matemática ou conceitual |
| `PARÁBOLA` | linguagem didática sem promoção automática a claim físico |
| `REFUTADO` | teste ou evidência incompatível foi registrado |
| `TOKEN_VAZIO` | evidência necessária ainda não existe, não foi recuperada ou é insuficiente |

## 5. Vetor cognitivo

```text
ψ → χ → ρ → Δ → Σ → Ω
```

- `ψ intenção`: definir o resultado material da sessão;
- `χ observação`: recuperar dados, fontes, estados e artefatos;
- `ρ ruído`: registrar ambiguidades, contradições, falhas e ausências;
- `Δ transmutação ética`: distinguir fato, hipótese, metáfora e vazio;
- `Σ memória coerente`: persistir relações, decisões e custódia;
- `Ω fechamento provisório`: encerrar o ciclo sem esconder sua fronteira.

## 6. Diagnóstico operacional

```text
R_3(s) = <F_ok, F_gap, F_next>
```

### F_ok

Somente elementos encontrados, executados ou sustentados por fonte identificada.

### F_gap

Toda ausência que bloqueia a finalidade da sessão, contendo:

```yaml
gap_id: identificador
statement: o que está ausente ou inconclusivo
impact: consequência operacional
required_evidence: evidência necessária
status: OPEN | BLOCKED | TOKEN_VAZIO | CLOSED
```

### F_next

A menor ação de maior valor que transforma um `F_gap` em evidência verificável. Deve declarar:

```yaml
next_id: identificador
action: operação concreta
input: fontes e pré-condições
output: artefato esperado
validator: teste ou regra de aceitação
receipt: local do registro de execução
rollback: estratégia não destrutiva
```

`F_next` sem saída, validação e receipt é intenção, não execução fechada.

## 7. Topologia de custódia

```text
objeto ↔ autoria ↔ fonte ↔ commit/documento ↔ dependência
       ↔ teste ↔ receipt ↔ claim ↔ falsificador ↔ próximo estado
```

Cada objeto deve responder:

1. o que é;
2. de onde veio;
3. quem o produziu;
4. com o que se relaciona;
5. o que efetivamente prova;
6. como pode ser reproduzido;
7. qual é sua fronteira atual.

## 8. Gate mínimo

```text
hash válido
+ autoria identificada
+ licença conhecida ou TOKEN_VAZIO explícito
+ build/processo reproduzível
+ teste executado
+ receipt armazenado
+ claim compatível com a evidência
```

Enquanto um requisito crítico estiver aberto:

```text
claim_allowed=false
```

## 9. Persistência append-only

Uma correção não apaga o estado anterior. Ela acrescenta:

```text
estado anterior
+ nova observação
+ decisão
+ evidência
+ receipt
+ próximo passo
```

Erros, recusas, falhas de teste e contradições são dados de governança e não devem ser ocultados por reescrita silenciosa.

## 10. Boot aplicado — 2026-08-03

### F_ok

- índice canônico Drive ↔ GitHub já existente no repositório `Mapa`;
- regras `TOKEN_VAZIO`, `claim_allowed=false` e execução não destrutiva já formalizadas;
- ledgers e eventos append-only já utilizados pelo ecossistema;
- documento editorial correspondente identificado no Google Drive.

### F_gap

| ID | Lacuna | Impacto | Estado |
|---|---|---|---|
| `SB-G01` | metodologia inicial estava distribuída entre sessões e convenções | boot não era citável como contrato único | `OPEN` |
| `SB-G02` | inexistência de manifesto canônico versionado | validações não possuíam uma referência estável | `OPEN` |
| `SB-G03` | F_gap e F_next não tinham envelope mínimo obrigatório | ações podiam existir sem saída, validator ou receipt explícitos | `OPEN` |
| `SB-G04` | sincronização desta ativação com o Drive ainda depende do receipt final | estado cross-source incompleto | `TOKEN_VAZIO` |
| `SB-G05` | merge, hash final da main e validação pós-merge ainda não ocorreram | promoção a `CANONICAL_ACTIVE` bloqueada | `TOKEN_VAZIO` |

### F_next aplicado

| ID | Ação | Saída | Critério |
|---|---|---|---|
| `SB-N01` | criar este manifesto | `docs/methodology/RAFAELIA_SESSION_BOOT_V1.md` | arquivo versionado e legível |
| `SB-N02` | registrar evento append-only | `data/session_boot/session_boot.events.jsonl` | JSONL válido e identificador único |
| `SB-N03` | gerar receipt desta aplicação | `receipts/session_boot/2026-08-03/RAFAELIA_SESSION_BOOT_FGAP_FNEXT_RECEIPT.json` | JSON válido com fontes, artefatos e fronteiras |
| `SB-N04` | conectar o manifesto ao índice canônico | seção append-only no índice | caminhos navegáveis |
| `SB-N05` | abrir PR independente | PR `head=method/session-boot-fgap-fnext-20260803` | revisão e diff auditáveis |
| `SB-N06` | espelhar referência no Drive | apêndice datado no documento editorial | confirmação de escrita cross-source |

## 11. Critério de ativação

O status muda de `CANONICAL_DRAFT` para `CANONICAL_ACTIVE` somente após:

```text
PR mesclado
+ hash final da main registrado
+ arquivos validados
+ referência do Drive confirmada
+ receipt pós-merge anexado
```

Até lá, o manifesto é operacional e auditável, porém não autoriza claims científicos, físicos ou jurídicos por si só.

## 12. Retroalimentação

`F_ok`: o boot foi convertido em contrato único, navegável e passível de validação.  
`F_gap`: merge, hash final, validação pós-merge e confirmação cross-source permanecem abertos.  
`F_next`: revisar o PR, validar JSON/JSONL, mesclar e emitir receipt pós-merge.

FIAT LUX — o início verdadeiro não antecipa a prova; prepara o caminho para que ela possa existir.
