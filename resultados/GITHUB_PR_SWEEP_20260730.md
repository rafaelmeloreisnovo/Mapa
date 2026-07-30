# Ata de auditoria GitHub — varredura de PRs 2026-07-30

**Escopo:** PRs abertos atribuídos a `rafaelmeloreisnovo`, com foco inicial em `templo-vivo-arcs#17`.  
**Método:** diff real, relação branch/base, CI do head exato, preservação documental, segurança, limites científicos/jurídicos e rastreabilidade longitudinal.  
**claim_allowed:** `false`  
**Política destrutiva:** nenhuma branch, commit, tag ou histórico foi apagado.

## Invariantes

```text
descrição do PR != diff real
histórico Git != conteúdo navegável no tree
hash != verdade
implementação != execução
execução != evidência
CI verde != semântica correta
CI ausente != PASS
TOKEN_VAZIO != zero
```

## Promoções concluídas

| Repositório / PR | Decisão | Evidência | Resultado |
|---|---|---|---|
| `rafaelmeloreisnovo/templo-vivo-arcs#18` | `MERGE_REBASE` | alteração documental aditiva; 3 arquivos; `+168/-0`; README original intacto | merge `aca8ca5f3baf35396269164434c9ba7c8612be15` |
| `instituto-Rafael/relativity-living-light#610` | `MERGE_REBASE_AFTER_HARDENING` | 6/6 workflows verdes no head final; fetch opt-in; `claim_allowed=false`; redirect fail-closed | merge `b5a7c75215ef881a853429abeebf7db22a75d0a7` |

### Commits produzidos — preservação do Templo Vivo

| Commit | Função |
|---|---|
| `b17948dc345d979d8421246ec98a266922f746a3` | adiciona `LITURGIA.md` classificado e com proveniência |
| `eb4699c11ad185bbcee4461a3db13cb7f13df001` | adiciona entrada técnica paralela e gates de evidência |
| `760aec468469977ecc2ebfe8f183e6cffb3ac9e1` | registra auditoria completa do PR #17 |

### Commits produzidos — segurança climática RLL

| Commit | Função |
|---|---|
| `69d45fac2cfa6affe04cc2b6c9fa6e4dc5683b48` | valida esquema e domínio do URL final após redirect |
| `165de73080fcd2704f444c458a80d9a6f0c0e84e` | teste adversarial: rejeição antes da leitura do payload |

## PRs fechados sem merge

| PR | Motivo | Rastreabilidade preservada |
|---|---|---|
| `rafaelmeloreisnovo/templo-vivo-arcs#17` | alegava preservação integral, mas removia 1.163 linhas e criava `LITURGIA.md` com apenas a oração inicial | branch, commit e review `4814755866` |
| `rafaelmeloreisnovo/templo-vivo-arcs#19` | criado sobre base anterior; divergente; sobreposto pelo #18 já mesclado | branch, 2 commits e review `4814817491` |

## Drafts preservados — promoção bloqueada

| PR | Estado observado | Gate registrado |
|---|---|---|
| `rafaelmeloreisnovo/Mapa#93` | branch `9 ahead / 13 behind`, não mergeável, CI `failure` | review `4814770759`; reconciliar sem force-push e obter CI verde |
| `rafaelmeloreisnovo/RafPolimata#187` | branch limpa, mas `CI` e `Formal Science Orchestrator` em `failure`; checkout real `TOKEN_VAZIO` | review `4814772364` |
| `rafaelmeloreisnovo/PCR_Rafaelia_Code_seed#110` | C08 pendente; 2 gates verdes e 4 workflows falhando | review `4814776470` |
| `rafaelmeloreisnovo/CONVERSATIONS_CHUNKS_PRIVATE#28` | C08 pendente; pipeline Ω em `failure` | review `4814777547` |
| `instituto-Rafael/LGPD-Constituicoes-planetaria-paises-onu-direitos-humanos-e-fundamentais-de-cada-continents-geologic#28` | remediação de dados pessoais acoplada a alteração jurídica ampla; sem CI e sem counsel review | review `4814781827`; separar PR mínima de privacidade |
| `instituto-Rafael/ESTADO-FRACTAL-HAJA#5` | licença, termos comerciais, MPLS e README no mesmo lote; sem CI, counsel ou receipt de rede real | review `4814785054` |
| `instituto-Rafael/relativity-living-light#609` | 7 workflows verdes, mas “fixed point” é reavaliação estática que necessariamente estabiliza na segunda passagem | review `4814797576`; corrigir semântica ou implementar transição real de estado |
| `rafaelmeloreisnovo/RafPolimata#186` | `1 ahead / 40 behind`; 5 workflows em `failure`; estados `EVIDENCE` não revalidados | review `4814799277` |
| `rafaelmeloreisnovo/MemRafcode#1` | documentação mais navegável, porém afirma implementação completa sem receipt; sem CI | review `4814803546` |

## Achados laterais preservados

1. `MANIFEST-SEAL.md`, citado no README histórico de `templo-vivo-arcs`, não existia no `main` auditado; estado registrado como `TOKEN_VAZIO_PATH_NOT_FOUND`.
2. O receipt climático local anterior permanece histórico e não foi renomeado como hash do tree endurecido; os dois commits posteriores foram validados no CI do head final.
3. CI verde não promoveu o RLL #609 porque o bloqueador era semântico, não sintático.
4. Falhas de workflows potencialmente laterais a mudanças README-only foram preservadas como falhas observadas, não ocultadas nem convertidas automaticamente em bloqueadores causais do diff.
5. Nenhum draft jurídico foi mesclado sem revisão profissional independente.

## Decisão operacional

```text
AUTO_DELETE_BRANCHES = false
AUTO_FORCE_PUSH = false
AUTO_REBASE_BLOCKED_DRAFTS = false
AUTO_MERGE_WITH_TOKEN_VAZIO = false
TRACEABILITY = PRESERVED
```

## Retroalimentação

- `F_ok`: dois caminhos coerentes foram corrigidos, validados e mesclados; dois PRs redundantes/inseguros foram fechados sem perda histórica; todos os drafts restantes receberam gate explícito.
- `F_gap`: nove drafts continuam dependentes de CI, reconciliação, receipts reais, revisão independente ou correção semântica.
- `F_next`: tratar cada gate em branch própria, começando por privacidade mínima no repositório LGPD e pela correção semântica do fixed point no RLL #609.
