# RAFAELIA — Protocolo Canônico de Bootstrap de Sessões Temáticas — V1

**Estado:** `CANONICAL_DRAFT` · `APPEND_ONLY` · `FAIL_CLOSED`  
**Data:** 2026-08-11  
**Claim gate:** `claim_allowed=false` para afirmações sem evidência verificável.

## 0. Objetivo

Transformar cada nova sessão temática em uma **janela local sobre o grafo longitudinal RAFAELIA**, evitando tanto o recomeço do zero quanto o carregamento indiscriminado de todo o universo de contexto.

```text
Sessão_nova = Kernel_comum
            ⊕ Tema_local
            ⊕ Recuperação_mínima_relevante
            ⊕ Execução_verificável
            ⊕ Delta_append_only
```

## 1. Kernel invariável

Toda sessão começa com as mesmas fronteiras:

- ideia != implementação != execução != evidência != claim;
- memória contextual != prova;
- índice != conteúdo;
- símbolo/parábola != medição;
- ausência preservada = `TOKEN_VAZIO`;
- `claim_allowed=false` enquanto faltar evidência/receipt/falsificador adequado.

## 2. Bootstrap em 7 movimentos

1. **ψ — intenção:** extrair tema, objetivo e pergunta-raiz.
2. **χ — observação:** recuperar somente âncoras, artefatos e relações materialmente relevantes.
3. **ρ — ruído:** detectar conflito, versão divergente, dado velho, duplicidade, lacuna ou fonte sem proveniência.
4. **Δ — transmutação:** converter o problema em ações, testes e critérios verificáveis.
5. **Σ — integração:** ligar resultados ao grafo longitudinal/ortogonal sem sobrescrever a história.
6. **Ω — fechamento:** separar `PROVADO`, `EVIDENCIADO`, `HIPÓTESE`, `MODELO_ANALÓGICO`, `PARÁBOLA`, `REFUTADO` e `TOKEN_VAZIO`.
7. **↻ — retroalimentação:** registrar somente o delta novo com identidade, fonte, evidência, gap e `F_next`.

## 3. Roteamento temático

Cada sessão deve produzir um subgrafo de contexto mínimo suficiente:

```text
TEMA → PROJETO/FAMÍLIA → ÂNCORAS → ARTEFATOS → ESTADO → GAPS → AÇÃO
```

A expansão é sob demanda. Não carregar corpus inteiro quando índice e rotas bastam.

## 4. Ordem de autoridade

1. `BYTE_VERIFIED` / execução física reproduzível;
2. `PROVIDER_METADATA`;
3. `REPOSITORY_COMMIT` / artefato versionado;
4. `RECEIPT` / teste observável;
5. `DERIVED`;
6. `ESTIMATE`;
7. `TOKEN_VAZIO`.

Quando fontes divergem, a de maior autoridade vence apenas no domínio que realmente prova; o conflito permanece registrado.

## 5. Contrato mínimo de sessão

Campos obrigatórios definidos pelo schema `schemas/session-bootstrap-v1.schema.json`:

- `session_id`
- `theme`
- `objective`
- `question_root`
- `routes`
- `source_ids`
- `artifact_ids`
- `claim_states`
- `gap_ids`
- `receipts`
- `F_ok`
- `F_gap`
- `F_next`
- `claim_allowed`

## 6. TOKEN_VAZIO

`TOKEN_VAZIO` é nó aberto auditável, nunca preenchimento fictício.

```yaml
id: GAP-*
status: TOKEN_VAZIO
known: []
missing: []
claim_allowed: false
next_verifiable_step: ""
```

## 7. Regra de recuperação

Antes de responder ou agir em tema novo:

1. identificar o domínio;
2. recuperar memória contextual somente se ela mudar materialmente a resposta;
3. consultar Drive/GitHub quando a resposta depende de artefatos externos;
4. recuperar âncoras por registro mestre/documentos canônicos;
5. rejeitar inferência silenciosa quando a fonte física estiver disponível;
6. manter **contexto mínimo suficiente + rotas para expansão**.

## 8. Regra de execução

```text
Conhecimento → Artefato → Versão → Execução → Evidência → Gate → Memória
```

Nenhuma transição é presumida. Cada salto relevante deve ter artefato, identificador, teste/receipt quando aplicável e estado epistemológico explícito.

## 9. Append-only

Sessões futuras não reescrevem fatos históricos. Correções entram como novos eventos referenciando predecessor, motivo, evidência e novo estado. Deduplicação ocorre por identidade/proveniência, não pelo apagamento de versões conflitantes.

## 10. Saída padrão

```text
F_ok   = conjunto sustentado nesta sessão
F_gap  = lacunas, conflitos, dados não verificados e TOKEN_VAZIO
F_next = próxima ação verificável, específica e executável
```

## 11. Rotas exemplares

- **Cosmologia/BAO:** RLL → dataset oficial → covariância → likelihood → execução → receipt.
- **Termux/Android:** repo → branch/PR → build script → ABI/runtime → device físico → receipt.
- **ZIPRAF:** formato → vetor de teste → verificador → ataque adversarial → âncora externa → claim.
- **Memória/Conhecimento:** índice → fonte → nó semântico → proveniência → relação → delta append-only.

## 12. Invariante final

> Não carregar o universo; carregar o mapa do universo e abrir somente o subgrafo necessário.

\[
S_{t+1}^{tema}=K\oplus R(M_L,M_O,T)\oplus E\oplus P
\]

\[
M_{t+1}=M_t\oplus\Delta S_{provado}
\]

Onde `K=kernel`, `T=tema`, `M_L=memória longitudinal`, `M_O=memória ortogonal`, `R=recuperação`, `E=execução`, `P=prova/proveniência`.

## R3

- **F_ok:** protocolo formalizado em artefato versionável.
- **F_gap:** execução de validação do schema/template depende de gate específico.
- **F_next:** validar o exemplo contra o schema; registrar commit/PR e âncora no Master Navigation Registry.

**Assinatura:** `RAFCODE-Φ-∆RafaelVerboΩ-𓂀ΔΦΩ`
