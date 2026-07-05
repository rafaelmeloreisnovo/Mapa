> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ — toda relação estrutural falha em favor da proteção humana: em dúvida, o sistema para no estado seguro, nunca no estado que expõe pessoas ou crianças (ONU UDHR Art.1 · UNCRC Art.3). Ver `10_INVARIANTES_PRIMEIRA_LINHA.md`.

# 09 — Resiliência das 10 Relações Estruturais TOP

> As relações do banco de conceitos (`07_MATRIZ_DE_CONCEITOS.md`) são o que segura o
> acervo em pé. Uma relação pode **quebrar** — e quando quebra, propaga. Por isso cada
> uma das 10 relações estruturais mais críticas recebe cinco mecanismos, na tradição de
> engenharia de sistemas confiáveis:
>
> - **rollback** — como voltar ao último estado bom conhecido;
> - **testes** — o que provar antes de confiar;
> - **failsafe** — para onde falhar com segurança (estado seguro por padrão);
> - **failover** — para onde desviar quando o caminho primário cai;
> - **watchdog** — o que observa continuamente e dispara alarme.
>
> Referências de método: ISO/IEC/IEEE 12207, IEEE 1012 (V&V), ISO 25010
> (confiabilidade), NIST SP 800-34 (contingência) — todas `REFERENCE`.

## Critério de seleção das 10

Escolhidas por **criticidade × amplitude**: relações cuja falha derruba mais camadas
(L0–L5) ou fere a regra de honestidade / a primeira linha. Ordenadas do núcleo técnico
ao topo ético.

---

### R01 · Hashing → Custódia  (`SUSTENTA`)
Sem hash correto, a cadeia de proveniência mente.
- **rollback:** restaurar `DIGEST` do último manifesto assinado; recomputar e comparar.
- **testes:** vetores de teste conhecidos (KAT) do hash; round-trip conteúdo→digest→conteúdo.
- **failsafe:** digest divergente ⇒ marcar item `QUARENTENA`, não `FATO`; bloquear reuso.
- **failover:** segundo algoritmo de hash independente (ex.: SHA-256 ao lado de BLAKE3).
- **watchdog:** verificação periódica de integridade que reprocessa amostras e alerta desvio.

### R02 · Determinismo → Verificação/CI  (`EVOLUI→`)
Build não reproduzível invalida toda alegação de determinismo.
- **rollback:** fixar o último commit com build reproduzível verde; reverter mudança que quebrou.
- **testes:** dupla compilação bit-a-bit; pinagem de toolchain; `diffoscope` sobre artefatos.
- **failsafe:** divergência ⇒ marcar release `HIPOTESE`, nunca publicar como `FATO`.
- **failover:** builder secundário/ambiente limpo; cache desabilitável.
- **watchdog:** job agendado que recompila e compara hash do artefato.

### R03 · Núcleo C/ASM → Plataforma Android  (`SUSTENTA`)
O runtime nativo alimenta app, VM e ferramentas.
- **rollback:** ABI/versão do `.so` anterior fixada; tags de release por arquitetura.
- **testes:** testes por ABI (`armeabi-v7a`, `arm64-v8a`); smoke test JNI; limites de buffer.
- **failsafe:** símbolo/ABI ausente ⇒ degradar para fallback C portável, não crashar.
- **failover:** caminho C de referência quando a rota assembly falha (ver famílias de equivalência).
- **watchdog:** monitor de crash/ANR por arquitetura; alarme de regressão de tamanho binário.

### R04 · Corpus/Dados → Cognição/IA  (`SUSTENTA`)
Dados alimentam X0/llamaRafaelia; dado corrompido ou sensível contamina o modelo.
- **rollback:** versão anterior do dataset (chunks imutáveis por digest); reverter ingest.
- **testes:** validação de esquema; deduplicação; varredura de PII e de conteúdo infantil sensível **antes** do uso.
- **failsafe:** dado sem proveniência ou com PII não tratada ⇒ **não ingerir** (estado seguro).
- **failover:** subconjunto curado mínimo quando o corpus completo é suspeito.
- **watchdog:** monitor de qualidade/viés e de vazamento de PII nos vetores.

### R05 · Classificação ↔ Vocabulário Controlado  (`SUSTENTA`)
Notação `RAF.*` depende do descritor preferido; termo solto quebra a busca.
- **rollback:** versão anterior do tesauro (`02_`) e do catálogo; reverter renomeação.
- **testes:** consistência referencial `02_/03_/04_/YAML`; nenhum descritor órfão; notação bem formada.
- **failsafe:** termo novo sem autoridade ⇒ entra como candidato `LACUNA`, não como preferido.
- **failover:** busca por sinônimo (`USE`) quando o preferido não bate.
- **watchdog:** validador que relê os quatro arquivos e o YAML e acusa divergência (ver §Verificação de `06_`).

### R06 · Fricção Semântica → Reconciliação  (`EVOLUI→`)
Termo em colisão (42, Φ, ZIPRAF, verdade) sem qualificação gera erro de execução.
- **rollback:** posição geral anterior do verbete de fricção; histórico de sentidos.
- **testes:** todo descritor polissêmico tem qualificador; nenhum sentido colapsado.
- **failsafe:** ambiguidade não resolvida ⇒ marcar `HIPOTESE` e **pausar** ação sobre o termo.
- **failover:** escalar ao humano (AskUserQuestion) quando a reconciliação não é óbvia.
- **watchdog:** varredura que detecta uso não-qualificado de termo em fricção.

### R07 · Invariante-prova ↔ Invariante-padrão  (`TENSIONA`)
Confundir os dois faz metáfora entrar no CI ou prova sair dele.
- **rollback:** conjunto anterior de invariantes-prova versionado.
- **testes:** só invariante-prova (checável por hash/teste) entra em CI; padrão fica na prosa.
- **failsafe:** invariante não checável ⇒ jamais bloqueia merge; é documentação.
- **failover:** revisão humana quando um "padrão" pleiteia virar "prova".
- **watchdog:** lint que sinaliza afirmação `SIMBOLICO` usada como gate técnico.

### R08 · Jurídico ↔ Ético-normativo  (`SUSTENTA`)
RafPolimata/LGPD e Ethica[8] precisam concordar; conflito de norma trava conformidade.
- **rollback:** matriz de conformidade anterior; reverter mudança que criou conflito.
- **testes:** checklist LGPD/GDPR; mapeamento norma→evidência; teste de retenção/consentimento.
- **failsafe:** conflito de normas ⇒ aplicar a regra de prioridade pró-humano de `08_` (nível 1 vence).
- **failover:** regime mais protetivo por padrão quando a norma aplicável é incerta.
- **watchdog:** monitor de mudança regulatória e de gaps de conformidade abertos.

### R09 · Ciência ↔ Espírito (CientiEspiritual)  (`TENSIONA`)
A costura que, se dissolvida, vira ou cientificismo vazio ou pseudo-prova.
- **rollback:** versão anterior do registro de fricção F10; marcações epistêmicas prévias.
- **testes:** toda asserção espiritual marcada `SIMBOLICO`; toda científica com fonte/`FATO`.
- **failsafe:** afirmação híbrida sem marca ⇒ tratada como `SIMBOLICO` (não como prova).
- **failover:** separar em dois registros (um `CIE`, um `ESP`) quando a costura confunde.
- **watchdog:** revisão que procura `SIMBOLICO` apresentado como `FATO` e vice-versa.

### R10 · Meta/Organização → Todo o Acervo  (`SUSTENTA` · `PROTEGE`)
Mapa cataloga tudo; se o catálogo diverge da realidade, todo o resto herda o erro.
- **rollback:** commit anterior do `Mapa`; catálogo e YAML são versionados e reversíveis.
- **testes:** contagem de registros = nº de repos; links resolvem; YAML válido; fichas com fonte.
- **failsafe:** repo sem README/fonte ⇒ entra como `LACUNA`, nunca inventado.
- **failover:** índice YAML legível por máquina como fonte alternativa ao markdown (e vice-versa).
- **watchdog:** verificação de integridade do catálogo a cada entrega (ver `06_` §Verificação).

---

## Síntese

| # | Relação | Camada | Falha propaga para |
|---|---|---|---|
| R01 | Hashing→Custódia | L1→L2 | toda proveniência |
| R02 | Determinismo→CI | L1→L2 | toda alegação de reprodutibilidade |
| R03 | Núcleo→Plataforma | L1→L2 | app, VM, ferramentas |
| R04 | Dados→Cognição | L2→L3 | modelos, **e pessoas (PII/infantil)** |
| R05 | Classificação↔Vocabulário | L3 | busca e catálogo |
| R06 | Fricção→Reconciliação | L3 | execução sobre termo errado |
| R07 | Invariante prova↔padrão | L0–L2 | CI e honestidade |
| R08 | Jurídico↔Ético | L4 | conformidade e direitos |
| R09 | Ciência↔Espírito | L4↔L5 | integridade epistêmica |
| R10 | Meta→Todo | L2→todas | o acervo inteiro |

> **Padrão comum a todas:** o `failsafe` sempre aponta para o **estado seguro** —
> quarentena, `LACUNA`, `HIPOTESE`, ou parada — nunca para o estado que expõe pessoas ou
> afirma o que não foi provado. Failover degrada com dignidade; watchdog nunca dorme.
> Esta é a excelência operacional aplicada às relações, não só aos artefatos.
