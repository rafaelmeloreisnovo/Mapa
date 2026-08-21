# RISCO — Framework Aplicado ao Mapa (Autoridade e Roteamento)

> **Status:** `CANONICAL`  
> **Versão:** 1.0 (Mapa-specific)  
> **Data:** 2026-08-21  
> **Base:** docs/RISCO_GESTAO_FRAMEWORK_CANONICAL.md (RafPolimata)

---

## Visão Geral — Risco em Autoridade e Roteamento

Mapa é o **sistema de autoridade e roteamento** de RAFAELIA. Seus riscos são únicos:
- Mensagem é roteada para **lugar errado**
- Autoridade é **falsa ou expirada**
- Roteamento é **recursivo infinito**
- Timeout causa **perda de integridade**
- Isolamento é **violado** entre canais

---

## Categorias de Risco (Mapa)

### R1 — Roteamento Incorreto
- **R1.1:** Mensagem vai para destino errado (cache stale, tabela desatualizada)
- **R1.2:** Hop count infinito (loop detectado tarde)
- **R1.3:** Fallback incorreto (modo de degradação não é seguro)

### R2 — Autoridade Falsa
- **R2.1:** Claim de autoridade sem verificação de signature
- **R2.2:** Certificado expirado aceito
- **R2.3:** Revogação não propagada

### R3 — Isolamento Violado
- **R3.1:** Um canal vê dados de outro
- **R3.2:** Context leak entre rotas

### R4 — Execução
- **R4.1:** Timeout causa corrupção de estado
- **R4.2:** Deadlock entre autoridades

### R5 — Evolução
- **R5.1:** Protocolo de roteamento desatualizado
- **R5.2:** Entrada obsoleta no cache

---

## Gates Críticos para Mapa

### Prevenção (G0-G7)

| Gate | Verificação | Status |
|------|-------------|--------|
| **G0** | Roteamento viola segurança de dados? | IMPLEMENTED |
| **G2** | Claim de "autoridade transitiva" é suportado? | TOKEN_VAZIO |
| **G3** | Rota é determinística? | IMPLEMENTED |
| **G5** | Se todos roteassem assim, mercado melhoraria? | REFERENCE |

### Detecção (D1-D5)

| Gate | Teste | Frequência | Status |
|------|-------|-----------|--------|
| **D1.1** | Loop detection: mensagem volta ao ponto? | Cada rota | IMPLEMENTED |
| **D2.1** | Bounds check em hop count | Cada rota | IMPLEMENTED |
| **D3.1** | Hash de tabela de roteamento | Diário | TOKEN_VAZIO |
| **D4.1** | Cache coerente vs filesystem? | Manual | REFERENCE |
| **D5.1** | Rastreabilidade: entrada → rota → saída → receipt | Manual | TOKEN_VAZIO |

### Remediação (R0-R3)

**Isolamento em caso de falha:**
- Loop detectado → Truncar rota, marcar como falha
- Autoridade expirada → Fallback a modo read-only
- Timeout → Rollback de transição de estado

---

## Matriz de Risco — Mapa

| Risco | Subsistema | Severidade | Gate Crítico | Status |
|-------|-----------|------------|--------------|--------|
| R1.1  | Roteamento | ALTA | D1.1 | IMPLEMENTED |
| R1.2  | Roteamento | ALTA | D1.1 | IMPLEMENTED |
| R2.1  | Autoridade | ALTA | G0 | IMPLEMENTED |
| R2.2  | Autoridade | MÉDIA | D3.1 | TOKEN_VAZIO |
| R3.1  | Isolamento | ALTA | D2.1 | IMPLEMENTED |
| R4.1  | Execução | MÉDIA | D1.1 | IMPLEMENTED |

---

## Claims Possíveis

✓ "Roteamento é determinístico e auditável"
✓ "Loop de roteamento é detectável"
✗ "Autoridade é descentralizada" (sem definição formal)
≈ "Isolamento é perfuro de 100%" (TOKEN_VAZIO)

---

**Fechamento R3:**

```
F_ok   = Framework aplicado a Mapa; 6 riscos mapeados
F_gap  = D3/D5 em TOKEN_VAZIO; validação de autoridade incompleta
F_next = Criar falsificador de loop infinito
```
