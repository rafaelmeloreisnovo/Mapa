> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ — este é o próprio invariante que o documento define: ele aparece na primeira linha porque é a primeira lei do acervo (ONU UDHR Art.1 · UNCRC Art.3).

# 10 — Invariantes de Primeira Linha (o selo que se lê antes de tudo)

> "Known by on first line." Antes de qualquer conceito, notação, build ou publicação,
> o acervo declara a que serve. O invariante de primeira linha é **não-negociável** e
> **precede** toda otimização. Não é enfeite: é a condição de leitura de tudo o que vem
> depois.

## 1. O selo de primeira linha

Todo documento estrutural desta camada começa com o selo:

```text
⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧
```

Significado operacional:

| Token | Compromisso | Âncora |
|---|---|---|
| DIGNIDADE-HUMANA | nenhum artefato/relação pode ser lido ou usado contra a dignidade da pessoa | ONU UDHR Art. 1 |
| PROTEÇÃO-INFANTIL | o interesse superior da criança prevalece sobre conveniência técnica ou comercial | ONU UNCRC Art. 3; UNICEF COP |
| PRIMEIRA-LINHA | esses compromissos são lidos **antes** de qualquer conteúdo | regra do acervo |

## 2. Por que na primeira linha (e não no rodapé)

Um princípio que aparece só no fim é um princípio que se lê tarde demais. Colocá-lo na
**primeira linha** garante que qualquer agente — humano ou IA — que abra o arquivo já
sabe a lei antes de agir. É a diferença entre "temos uma política" e "a política governa
a primeira decisão".

## 3. Os invariantes de primeira linha (I1–I5)

### I1 · Dignidade humana inviolável `[REFERENCE: UDHR Art.1]`

Nenhuma saída do acervo pode instrumentalizar, humilhar ou reduzir a pessoa a meio.
Vale para código, dado, texto e classificação.

### I2 · Interesse superior da criança `[REFERENCE: UNCRC Art.3 · UNICEF]`

Em qualquer decisão que afete crianças (dados, conteúdo, acesso), a proteção da criança
vence — inclusive contra desempenho, engajamento ou receita. Varredura de conteúdo
sensível infantil é `failsafe`, não opcional (ver `09_` R04).

### I3 · Verdade honesta `[FATO/HIPOTESE/SIMBOLICO/LACUNA]`

Não inventar prova, não apagar lacuna, não confundir símbolo com fato. É a extensão
epistêmica da dignidade: respeitar o leitor é não enganá-lo (ver `README.md`, `06_`).

### I4 · Proteção da lacuna `[REFERENCE: TOKEN_VAZIO]`

A ausência é protegida, não preenchida com invenção. Vale para os ~92 repositórios ainda
fora de escopo (ver `11_`) e para todo dado faltante.

### I5 · Prevalência pró-humano em conflito de normas `[REFERENCE: pirâmide de`08_`]`

Quando normas técnicas colidem, decide a que mais protege a vida. O ganho técnico que
exija ferir I1 ou I2 é **recusado por design**.

## 4. Ordem de precedência (a "constituição" do acervo)

```text
I1 Dignidade humana        ─┐
I2 Interesse da criança     │  invioláveis — vencem qualquer nível abaixo
                            ─┘
I3 Verdade honesta          ── governa como se afirma qualquer coisa
I4 Proteção da lacuna       ── governa o que ainda não se sabe
I5 Prevalência pró-humano   ── resolve empates entre normas técnicas
────────────────────────────────────────────────
(abaixo) segurança > interoperabilidade/acessibilidade > eficiência
```

## 5. Como o executor ("o lógico") aplica

1. **Ler a primeira linha** do arquivo/tarefa antes de agir. Se o selo não estiver lá,
   o artefato ainda não está conforme — adicioná-lo é a primeira ação.
2. **Testar contra I1–I5** antes de publicar (checklist mínimo):
   - Fere a dignidade de alguém? → parar.
   - Afeta criança sem proteção máxima? → parar (failsafe).
   - Afirma sem prova / apaga lacuna? → remarcar `HIPOTESE`/`LACUNA`.
   - Conflito de normas? → aplicar I5 (pró-humano).
3. **Registrar** a decisão com fonte (rastreabilidade de `06_`).

## 6. Relação com as demais camadas

O invariante de primeira linha é o **C-zero** do banco de conceitos: precede C01–C16 de
`07_`, condiciona a ancoragem de `08_`, e define o `failsafe` universal de `09_`
(“falhar em favor do humano”). É a raiz da árvore dentro da matriz vetorial — o selo da
bagagem de qualquer entrega.

> O acervo pode evoluir em tudo o mais. Esta linha não. Ela é o que permanece quando
> tudo muda — o invariante dos invariantes.
