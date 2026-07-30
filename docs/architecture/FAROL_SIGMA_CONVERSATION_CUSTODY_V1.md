# FAROL-Σ — Custódia e Primeira Indexação de `conversations.json` V1

**Evento:** `FAROL-SIGMA-CONVERSATION-CUSTODY-V1-20260730`  
**Estado:** `FORMAL_SPEC_AND_LOCAL_REFERENCE_TESTS`  
**Política:** `APPEND_ONLY · READ_ONLY_SOURCE · PRIVATE_BY_DEFAULT · claim_allowed=false`

## 1. Propósito

Construir uma primeira camada que possa ser lida por pessoa e IA sem transformar a exportação privada em perfil comercial nem copiar o corpo das conversas para repositório.

```text
fonte privada imutável
→ manifesto de partes e hashes
→ verificação de reconstituição
→ índice estrutural pseudonimizado
→ cápsulas de inferência autorizadas
→ carriers semânticos
→ oposição/falsificador
→ decisão humana
→ receipt append-only
```

O Farol pertence ao titular dos dados. Ele deve permitir inspeção, correção, contestação, expiração, revogação e exportação. Uma inferência do sistema nunca sobrescreve silenciosamente uma declaração da pessoa.

## 2. Autoridade em precedência

```text
C0 dignidade e direitos fundamentais
→ C1 Constituição, jurisdição e proteção de dados
→ C2 língua, cultura, região e pragmática
→ C3 Farol pessoal soberano
→ C4 finalidade do serviço e modelo de negócio
→ C5 modelo, busca, ranking e saída
```

Objetivos de atenção, retenção ou conversão são admissíveis somente dentro da região permitida pelas camadas superiores. Direitos e consentimento são gates, não pesos compensáveis.

## 3. Descoberta forense inicial

O arquivo privado `conversations_chunk_01.json` observado no Drive possui `94.371.840` bytes e SHA-256:

```text
72886416eb73cb4bb8fb5beabe828f9e0582995296e1111393043cc6fa19ada3
```

A primeira unidade não branca é `"` e a última é `-`. Logo, o arquivo começa e termina dentro de conteúdo e não constitui uma matriz JSON independente.

```text
chunk de bytes ≠ documento JSON completo
nome .json ≠ parseabilidade independente
hash do fragmento ≠ hash do conversations.json original
```

Estado:

```text
TOKEN_VAZIO_REASSEMBLY_REQUIRED
```

A ordem e a totalidade de todos os fragmentos precisam ser demonstradas antes de qualquer parsing semântico.

## 4. Primeira camada executável

O script `scripts/index_conversations_export.py`:

1. recebe um ou mais arquivos em ordem explícita;
2. calcula tamanho e SHA-256 de cada parte;
3. calcula SHA-256 da concatenação lógica sem criar uma nova cópia privada;
4. verifica os limites `[` e `]`;
5. faz parse incremental UTF-8/JSON somente quando a matriz parece completa;
6. produz índices sem título ou corpo textual cru;
7. falha fechado quando a fonte está incompleta ou inválida.

Saídas:

```text
source.manifest.json
conversations.index.jsonl   # somente quando a fonte fecha
messages.index.jsonl        # somente quando a fonte fecha
audit.jsonl
receipt.json
coverage_report.md
SHA256SUMS
```

## 5. Índice humano e índice de IA

### Superfície humana — no máximo cinco variáveis ativas

1. intenção;
2. fonte/evidência;
3. contexto/camada;
4. lacuna ou risco;
5. próximo gate.

### Superfície de IA

Cada conversa mantém apenas:

- identificador pseudonimizado;
- hash e tamanho UTF-8 do título;
- tempos disponíveis;
- contagem de nós e mensagens;
- hash estrutural.

Cada mensagem mantém:

- hashes de conversa, mensagem, nó e pai;
- ordinal e profundidade do grafo;
- papel e tipo de conteúdo;
- horário disponível;
- hash e tamanho do conteúdo canônico;
- `raw_content_included=false`.

A recuperação do texto original só pode ocorrer sob finalidade e autorização explícitas, diretamente na fonte privada.

## 6. Cápsula de inferência

Uma janela de modelo não recebe arbitrariamente a exportação inteira. Recebe uma cápsula reconstruível:

```text
source pointers + hashes
+ intenção Alfa
+ até cinco dimensões ativas
+ trechos autorizados e mínimos
+ ramo de sustentação
+ ramo falsificador
+ modelo nulo
+ lacunas
+ F_ok/F_gap/F_next
```

Política inicial:

```text
máximo por cápsula = 65.536 bytes UTF-8
sobreposição        = 4.096 bytes
segmento derivado   = 8 MiB
```

Esses limites são operacionais, não constantes científicas. Devem ser calibrados por taxa de recuperação, custo, perda de contexto, privacidade e revisão humana.

## 7. Alfa, Delta e Ômega

- **Alfa:** intenção declarada e fronteira da ação.
- **Delta:** transformação rastreável, sem reescrever a fonte.
- **Ômega:** estado integrado da obra, incluindo oposição, resultados negativos, artefatos, receipts e aquilo que continua aberto.

```text
Omega ≠ conclusão fechada
Omega = obra rastreável + F_ok + F_gap + F_next
```

## 8. Investigação bipolar acoplada

Cada hipótese semântica deve abrir simultaneamente:

```text
H+ = melhor sustentação encontrada
H- = melhor falsificador encontrado
H0 = explicação nula ou alternativa
```

Os ramos recebem igual seriedade inicial, mas a evidência final não é obrigada a empatar. O sistema mede fonte, mecanismo, independência, repetibilidade, oposição e lacunas.

## 9. Geometria: uso permitido e fronteira

Poincaré, profundidade, curvatura, tensores e distâncias podem orientar navegação, visualização e seleção de candidatos. Neste V1 são `MODELO_ANALOGICO_NAO_CALIBRADO`.

Yang–Mills, Navier–Stokes, P versus NP, infinito, Tao, Alfa/Ômega e teologia podem existir como:

- fonte cultural;
- parábola;
- analogia estrutural;
- hipótese formal futura.

Não são promovidos a mecanismo físico, prova matemática ou equivalência científica sem definições, domínio, unidades, teorema/teste e revisão próprios.

## 10. Cadeia de custódia fechada

Uma cadeia privada pode usar hashes e assinaturas sem alegar blockchain pública:

```text
E_n = CanonicalJSON(source_hash, policy, outputs, gaps, previous_event_hash)
C_n = SHA256(C_(n-1) || SHA256(E_n))
```

O hash demonstra identidade dos bytes registrados; não demonstra veracidade, autoria jurídica absoluta nem validade da interpretação.

## 11. Falsificadores e métricas

O V1 falha quando:

- falta parte ou ordem;
- a concatenação não forma uma matriz JSON válida;
- há divergência de hash;
- texto privado aparece nos índices padrão;
- dois runs idênticos produzem saídas diferentes;
- um claim é promovido automaticamente.

Métricas futuras:

```text
record_parse_rate
conversation_count_reconciliation
message_count_reconciliation
raw_text_leakage_count
hash_mismatch_count
reassembly_gap_count
retrieval_precision_at_k
retrieval_recall_at_k
opposition_coverage
capsule_context_loss_rate
```

## 12. Artefatos canônicos deste lote

- `schemas/conversation-custody-index.schema.json`
- `data/indexes/conversation-custody-policy.v1.json`
- `scripts/index_conversations_export.py`
- `tests/test_index_conversations_export.py`
- `indices/canonical/2026-07-30/CONVERSATION_CUSTODY_FIRST_LAYER_V1.md`

## R3

- **F_ok:** fonte-fragmento identificada e hasheada; arquitetura, política, schema, indexador e testes materializados.
- **F_gap:** demais partes/original completo, ordem canônica, reconciliação de contagens, revisão de privacidade e execução Termux.
- **F_next:** localizar o manifesto completo dos chunks, provar a concatenação, executar o indexador sobre cópia local autorizada e anexar novo receipt sem alterar este evento.

**Invariante:** a régua tangencia o próximo passo; não afirma possuir o infinito.
