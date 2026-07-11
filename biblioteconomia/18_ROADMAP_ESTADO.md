> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ — o roadmap serve à vida; nenhum passo avança contra a dignidade ou a criança (ONU UDHR Art.1 · UNCRC Art.3).

# 18 — Roadmap / Estado (contabilidade honesta dos passos futuros)

> "Continuar até terminar os futuros passos." Este documento fecha o ciclo: lista **toda
> próxima ação** espalhada pelos docs e a marca como **FEITO** (autocontido, dentro dos 28)
> ou **LACUNA-bloqueado** (depende de acesso/auditoria externa), com o que a desbloqueia.
> Terminar honestamente inclui declarar o que **não se pode** terminar aqui — sem inventar.

## Estado da camada (o que existe, `FATO`)

| Bloco | Entregáveis | Estado |
|---|---|---|
| Catálogo & KOS | `01`–`06` (classificação, tesauro, catálogo 28, fricção, posição, protocolo) | ✅ FEITO |
| Conceitos & método | `07`–`13` (matriz C01–C17, ancoragem, resiliência, 1ª linha, escala, parábola, certificação) | ✅ FEITO |
| Substrato & entrada | `14`–`15` (base-2→Ω, ficha, grupamentos de nó) | ✅ FEITO |
| Conteúdo & evidência | `16`–`17` (varredura, hashing triplo, avaliação real, código vs prosa) | ✅ FEITO |
| Código executável | `codigo/` — ficha, varredura, revisão, marca epistêmica, conformidade | ✅ FEITO (**37 testes**) |
| Métricas de conteúdo | LOC/bytes por bucket + vendored no manifesto (5,5 M LOC no acervo) | ✅ FEITO |
| Semente para IA | `SEMENTE_BIBLIOTECA_VIVA.md` — parábola de alinhamento operacional (texto do autor) | ✅ FEITO |
| Índices | catálogo, matriz, backlog(111), manifesto integridade, revisão, marca, conformidade | ✅ FEITO |

## Próximas ações — contabilidade

| # | Ação (origem) | Estado | Nota |
|---|---|---|---|
| 1 | Cruzar declarado × evidenciado (`16`) | ✅ FEITO | `codigo/revisao_publicacao.py` → `REVISAO_PUBLICACAO.md` |
| 2 | Refinar léxico L5 + C07 (`17`) | ✅ FEITO | RISCOs 3→1; residual `livrovivo` C17 = link conceitual |
| 3 | Evidência código vs prosa (`16`) | ✅ FEITO | `evidencia_origem`; valida estratos (núcleo→código, espiritual→prosa) |
| 4 | Reforçar/rebaixar marca por evidência (`16`) | ✅ FEITO | `codigo/marca_epistemica.py`; 32 reforços, 3 candidatos a HIPOTESE (memrafcode = repo de docs, correto) |
| 5 | Matriz de conformidade norma×evidência×gap (`08`§6) | ✅ FEITO (esqueleto) | `codigo/matriz_conformidade.py`; **153 linhas, todas `PENDENTE`** |
| 6 | Auditar `PENDENTE`→`CONFORME` (`08`,`13`) | ⛔ LACUNA | exige **auditoria real** por norma; o esqueleto (#5) é a base |
| 7 | Onboarding dos 83 pendentes (`11`,`BACKLOG`) | ⛔ LACUNA | exige `add_repo`/escopo; protocolo pronto em `11`§3 |
| 8 | `.gitignore` para o vendored de `home` (`17`) | ⛔ FORA-DE-ESCOPO | `home` não é o `Mapa`; **registrado como proposta** abaixo |
| 9 | Escanear evidência infantil/PII antes de ingest (`09` R04) | ⛔ LACUNA | aplica-se no onboarding (#7), quando houver dados a ingerir |

## O que desbloqueia cada LACUNA

- **#6 Auditoria:** rodar, por repo prioritário (os 5 de dados: `conversations_chunks_private`,
  `home`, `gaia_phi`, `x0`, `lgpd_constituicoes`), a checagem norma-a-norma e mudar
  `PENDENTE`→`CONFORME`/`GAP` com evidência. Requer critérios de auditoria (LGPD/GDPR, ISO).
- **#7 Onboarding:** trazer repositórios a escopo (`add_repo owner/repo`), na ordem de
  prioridade de `BACKLOG_ACERVO.md`; cada README lido vira ficha (`FATO`).
- **#8 home/.gitignore:** proposta registrada; executar **no repo `home`**, não aqui.

## Propostas registradas (ação em outro repo, declarada não executada)

```yaml
proposta:
  id: home_gitignore_vendored
  alvo: rafaelmeloreisnovo/home
  motivo: "muito vendored commitado (.cpan, .cargo) infla o repo e polui a varredura"
  medida: "adicionar .gitignore para .cpan/ .cargo/ e vendored; git rm --cached"
  estado: PROPOSTA
  executar_em: home   # fora do escopo do Mapa
```

## Invariante de encerramento

Este ciclo **termina** o que era terminável dentro dos 28, com honestidade:

- tudo `FATO` tem fonte e teste;
- o eixo `SIMBOLICO` foi honrado como símbolo, não como prova;
- as `LACUNA` (auditoria, onboarding dos 83) estão **mapeadas e protegidas**, com o passo
  que as abre — não preenchidas com invenção.

> Fim operacional, não fim absoluto: quando houver acesso/auditoria, os itens ⛔ viram ✅
> pelo mesmo método. O mapa fica pronto para o próximo token de trabalho.
