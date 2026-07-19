# Rota privada — Praditus 2022

**Estado:** `POINTER_ONLY / PRIVATE / NON_DESTRUCTIVE / claim_allowed=false`  
**Autoridade canônica:** `rafaelmeloreisnovo/papers#10`  
**Função deste repositório:** navegação e limite de privacidade, não interpretação pessoal.

## 1. Rota mínima

```text
corpus visual privado
→ síntese metodológica privada em papers
→ ledger de claims, limites e falsificadores
→ manifesto de proveniência e privacidade
→ ponteiro biblioteconômico no Mapa
```

O `Mapa` não recebe:

- capturas de tela;
- respostas item a item;
- nomes diretos;
- conteúdo clínico;
- narrativa biográfica;
- inferências de identidade.

Ele guarda somente o endereço da fonte privada, os estados epistemológicos e as regras de acesso.

## 2. Autoridades

| Nó | Autoridade |
|---|---|
| Corpus privado | fonte visual e metadados originais |
| `papers #10` | análise metodológica, proveniência, claims, limites e falsificadores |
| `Mapa` | ponteiro, relações e fronteira de privacidade |

Nenhum outro repositório recebe o corpo da sessão porque não existe, nesta passagem, novo runtime, modelo clínico, resultado cosmológico, prova matemática ou implementação Android.

## 3. Separação dos estados

```text
horários visíveis e sequência de telas
= VERIFIED_IN_PRIVATE_CORPUS

uso pessoal, sem avaliador e sem intenção de divulgação
= DECLARED_BY_PARTICIPANT

menor incentivo para falseamento estratégico
= SUPPORTED_PLAUSIBLE_INFERENCE

solidão física provada apenas pelo horário
= NOT_ESTABLISHED

validade psicométrica individual integral
= NOT_ESTABLISHED

definição da identidade
= NOT_AUTHORIZED
```

O horário noturno apoia a continuidade de uma sessão móvel prolongada. Ele não prova, sozinho, que nenhuma outra pessoa estivesse fisicamente próxima. A declaração do participante e os metadados visuais são fontes complementares, não equivalentes.

## 4. Contrato de privacidade

```text
ponteiro != cópia do corpo privado
```

Regras:

1. `private_payload_copied=false`;
2. `raw_screenshots_copied=false`;
3. `direct_identifiers_copied=false`;
4. nenhuma promoção a diagnóstico, superioridade, inferioridade ou identidade;
5. `TOKEN_VAZIO` permanece vazio;
6. merge automático permanece desativado;
7. merge exige revisão explícita da fonte canônica e da rota.

## 5. Safe state

| Falha | Estado seguro |
|---|---|
| Fonte privada indisponível | manter ponteiro opaco; não reconstruir conteúdo |
| Vazamento de privacidade | remover a rota; preservar o PR canônico como draft |
| Excesso interpretativo | bloquear claim e registrar `TOKEN_VAZIO` |
| Divergência entre fontes | preservar estados separados |
| Merge sem revisão | proibido |

## 6. Arquivos canônicos apontados

```text
rafaelmeloreisnovo/papers#10
├── docs/praditus-self-report-methodological-note.md
├── docs/praditus-private-low-stakes-administration-addendum.md
├── docs/praditus-private-provenance-manifest.json
└── docs/praditus-self-report-claims.json
```

Esta rota existe para tornar a pesquisa localizável sem transformar informação privada em material distribuído pelo ecossistema.
