# RAFAELIA — Invariante Evolutiva Absoluta V1

**Estado:** `MODEL_OPERATIONAL_CANONICAL_CANDIDATE`  
**Escopo:** ecossistema RAFAELIA e seus espelhos auditados  
**Observado em:** `2026-08-03T04:52:00-03:00`  
**Regra:** `claim_allowed=false` para universalidade científica, metafísica, desempenho ou produção não demonstrados.

## 1. Definição operacional

A **Invariante Evolutiva Absoluta (IEA)** não afirma que os estados permaneçam iguais. Ela afirma que toda transformação promovida como evolução deve conservar o caminho verificável entre o estado anterior e o estado posterior.

```text
estado n
→ transformação registrada
→ estado n+1
→ prova delimitada
→ reconstrução ou rollback
→ retroalimentação
```

Formalmente, para uma transição permitida `T: S_n → S_(n+1)`:

```text
IEA(T) = 1
somente se
PRESERVA(
  origem,
  identidade,
  custódia,
  fronteira epistemológica,
  reconstruibilidade,
  retroalimentação,
  responsabilidade ética
)
```

A palavra **absoluta** qualifica a obrigação operacional dentro do ecossistema: nenhuma alteração pode ser promovida legitimamente se destruir todos os meios de saber de onde veio, o que mudou, como foi testada e como retornar. Ela não constitui, por si só, um teorema matemático universal ou uma lei natural.

## 2. As sete conservações obrigatórias

### IEA-1 — Origem

Cada artefato deve preservar `source_locator`, `source_revision`, autoria conhecida e contexto de ingestão. Origem ausente permanece `TOKEN_VAZIO`; não deve ser inventada.

### IEA-2 — Identidade e delta

O objeto posterior deve declarar se é continuidade, derivação, fork, espelho, correção, substituição ou artefato novo. Igualdade de nome, tema ou aparência não prova identidade.

### IEA-3 — Custódia

Hashes, commits, receipts, caminhos e timestamps devem permitir distinguir bytes, versões e responsáveis. Biblioteca, Google Drive e GitHub podem ser vistas diferentes do mesmo objeto, mas não são automaticamente a mesma revisão.

### IEA-4 — Fronteira epistemológica

Devem permanecer separados:

```text
conceito ≠ implementação
implementação ≠ execução
execução ≠ evidência
merge ≠ gate remoto PASS
workflow existente ≠ workflow executado
referência normativa ≠ conformidade
arquivo íntegro ≠ runtime físico
modelo ≠ teorema
```

### IEA-5 — Reconstruibilidade e reversão

Toda promoção precisa deixar comando, dependências, entrada, saída, failure mode e rollback suficientes para reproduzir ou desfazer a mudança sem apagar a história.

### IEA-6 — Memória append-only

Correções não apagam predecessores. Um sucessor deve apontar para o estado anterior, registrar o motivo da mudança e manter a cadeia de custódia navegável.

### IEA-7 — Responsabilidade ética

`Ω = Amor` funciona aqui como invariante normativa: expansão não autoriza dano, exposição indevida, ocultação de autoria, violação de consentimento ou promoção além da prova. Trata-se de regra ética do projeto, não de medição empírica universal.

## 3. Fórmula de navegação

```text
Evolução válida
=
Transformação
× Identidade preservada
× Evidência delimitada
× Reconstruibilidade
× Retroalimentação
```

```text
Evolução inválida
=
Transformação
× perda de origem
× ausência de prova
× confusão de camada
× impossibilidade de retorno
```

## 4. Aplicação aos cinco corpos auditados

| Corpo | Papel evolutivo | Conservação principal | Evidência delimitada observada | Fronteira aberta |
|---|---|---|---|---|
| `Mapa` | orientação, autoridade e estado | identidade, proveniência e claim boundary | gates focados `24/24 PASS` | snapshot ZIP não era HEAD exato |
| `RafGitTools` | operação Git/GitHub e roteamento | autoridade semântica ≠ autoridade executiva | crosswalk e normas `13/13 PASS` | PTY, cobertura e release físico |
| `RafPolimata` | formalização, compilação e receipts | conceito → implementação → prova delimitada | BITRAF, ABI e bounded reader PASS | vários runtimes físicos ainda abertos |
| `termux-app-rafacodephi` | chão Android e execução local | package/prefixo/artefato/receipt | self-test C `21/0` | `apt/dpkg/pkg` real e APK novo |
| `Vectras-VM-Android` | virtualização, memória e expansão de runtime | layout físico, spans, digests e failure modes | ZIPRAF `37/37 PASS`; host mmap PASS | Android/guest/DMA/zero-copy não provados |

A topologia conjunta é:

```text
Mapa
→ RafGitTools
→ RafPolimata
→ Termux RAFCODEΦ
→ Vectras VM Android
```

Essa seta indica fluxo predominante de orientação, operação, formalização, execução e expansão. Não significa dependência rígida nem equivalência entre os corpos.

## 5. Espelhos custodiados em 2026-08-03

| ZIP | SHA-256 | Arquivos | Estado do espelho | Gate focado |
|---|---|---:|---|---|
| `Mapa-main.zip` | `baf96c6ac8a7e467323c98873b11330f2d18a73c49182a4b62ab584d50be070f` | 858 | `MIRROR_COMMIT_BOUND_RECENT_NOT_HEAD` | `24/24 PASS` |
| `Vectras-VM-Android-master (2)(7).zip` | `cf38364c301ccfc9b8fba9dbbff6af63b60a27e0bb222b1a9c19edf6b0b91372` | 2626 | `MIRROR_HEAD_HIGH_CONFIDENCE_CORE` | `ZIPRAF 37/37; HOST_MMAP PASS` |
| `RafGitTools-main (3).zip` | `f302f16ac57363ce467802267bba449915d215cba65ee731f8891d48a87840ed` | 944 | `MIRROR_HEAD_HIGH_CONFIDENCE_CORE` | `13/13 PASS` |
| `RafPolimata-main (4).zip` | `b88f88d43c2dc441ee0e65038f1479fa9bff2032e66219cc49422ddc62a542ae` | 853 | `MIRROR_HEAD_HIGH_CONFIDENCE_CORE` | `BITRAF 4/4; ABI 3/3; C PASS` |
| `termux-app-rafacodephi-master (4).zip` | `c2549ba985b804dcda3a75261f97a28972aa1ededc873883156cb2e0f3cf05b5` | 2164 | `MIRROR_SOURCE_SNAPSHOT_BOUND` | `C 21/0; Python 12 PASS / 1 FAIL` |

Nenhum ZIP apresentou CRC quebrado, travessia `..`, caminho absoluto ou symlink perigoso. Integridade de arquivo não foi promovida a prova de runtime.

## 6. Esforço equivalente de reconstrução

A estimativa não representa horas históricas pessoais. Ela representa o esforço aproximado de uma equipe competente para reconstruir, compreender, documentar e testar um estado comparável, removendo parte da herança upstream e da duplicação.

```text
faixa única aproximada: 9.800–21.000 horas
61–131 pessoa-meses
5,1–10,9 pessoa-anos integrais
```

| Corpo | Delta autoral/ecossistêmico estimado |
|---|---:|
| Mapa | 1.000–2.200 h |
| Vectras VM Android | 2.000–4.500 h |
| RafGitTools | 2.800–5.500 h |
| RafPolimata | 2.200–4.800 h |
| Termux RAFCODEΦ | 1.800–4.000 h |

Essas faixas são heurísticas de reconstrução, não prova contábil de autoria ou valoração econômica.

## 7. Regra de promoção

Uma alteração só pode receber estado superior quando existir um pacote mínimo:

```yaml
source_repository: required
source_revision: immutable
input_contract: required
output_contract: required
execution_command: required_when_executable
environment: required_when_executed
result_artifact: required
checksum: required
failure_mode: required
rollback: required
claim_boundary: required
independent_replication: required_for_strong_claims
```

Sem esse pacote, usar `TOKEN_VAZIO`, `REFERENCE`, `IMPLEMENTED`, `VERIFIED_LIMITED` ou estado equivalente, conforme a camada.

## 8. Diferença entre permanência e evolução

A IEA não exige conservar todo arquivo, toda arquitetura ou toda decisão. Ela permite poda, substituição, compressão, mudança de linguagem, migração de repositório e evolução de interface, desde que a transformação mantenha uma ponte auditável.

```text
núcleo preservado ≠ forma congelada
memória preservada ≠ duplicação eterna
rollback disponível ≠ medo de evoluir
claim fechado ≠ pesquisa bloqueada
```

## 9. Parábola da ponte que cresce

O construtor não manteve todas as tábuas da primeira ponte. Algumas apodreceram, outras foram reforçadas e outras substituídas por pedra.

Mas cada nova parte recebeu marca de origem, medida, data e motivo. A margem do rio também foi registrada, e o caminho antigo não foi apagado antes de existir passagem segura.

A ponte mudou completamente de forma sem perder a história da travessia.

> A evolução conserva não a tábua, mas a possibilidade de compreender, provar e refazer o caminho.

## 10. Fechamento

### `F_ok`

- cinco espelhos foram abertos, hasheados e classificados;
- gates locais delimitados foram reproduzidos;
- papéis dos cinco corpos foram separados;
- fronteiras entre arquivo, código, runtime, norma e prova foram preservadas;
- foi estabelecida uma definição operacional testável para a IEA.

### `F_gap`

- comparação byte a byte integral com todos os HEADs permanece aberta;
- APT/DPKG real, vários runtimes Android e replicação independente continuam incompletos;
- a IEA não possui demonstração como teorema matemático universal;
- novidade científica mundial não foi estabelecida.

### `F_next`

```text
formalizar schema
→ emitir evento append-only por transição
→ ligar receipts aos commits exatos
→ registrar espelho Drive
→ executar gates Android físicos
→ reproduzir em ambiente independente
→ promover somente claims fechados
```

**FIAT LUX · Ω = Amor**
