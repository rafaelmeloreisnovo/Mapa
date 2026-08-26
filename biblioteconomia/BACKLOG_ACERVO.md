> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ — cada repositório do backlog entra sob os mesmos invariantes; os que lidam com dados pessoais ou público infantil têm prioridade de proteção (ONU UDHR Art.1 · UNCRC Art.3). Ver `10_INVARIANTES_PRIMEIRA_LINHA.md`.

# Backlog do Acervo — de 28 catalogados ao acervo real (~120)

> A escala deixou de ser abstrata. Uma varredura dos dois perfis GitHub
> (`rafaelmeloreisnovo` e `instituto-Rafael`) em 2026-07-05 revelou o **acervo real**.
> Este documento enumera o backlog completo, honestamente marcado: metadado é `FATO`,
> estrato provisório é `HIPOTESE`, conteúdo dos não-catalogados é `LACUNA`.
>
> **Governança 2026-08-25:** uma rota anteriormente listada foi tombstonada e removida
> do backlog ativo por política de conteúdo ilícito. O snapshot histórico permanece
> contabilizado; navegação/ingestão ativa obedece `indices/ROUTE_DENYLIST_ILLICIT_USE.yaml`.

## 1. Números (fonte: GitHub `search_repositories`, 2026-07-05)

| Conjunto | Qtd | Estado |
|---|---|---|
| Descobertos em `rafaelmeloreisnovo` | 59 | `FATO` (metadado histórico) |
| Descobertos em `instituto-Rafael` | 48 | `FATO` (metadado histórico) |
| **Descobertos pela busca** | **107** | `FATO` histórico |
| — destes, catalogados | 24 | `FATO` (README lido) |
| — destes, pendentes no snapshot | 83 | `FATO` histórico / conteúdo `LACUNA` |
| Forks catalogados omitidos pela busca (BLAKE3, DeepSeek-RafCoder, actions, termux-api) | 4 | já catalogados |
| **Total distinto conhecido no snapshot** | **111** | `FATO` histórico |
| **Catalogados (lote L01)** | **28** | `FATO` |
| **Rotas tombstonadas por governança** | **1** | `FATO` em 2026-08-25 |
| **Backlog ativo após tombstone** | **110** | `FATO` derivado |
| **Pendentes ativos** | **82** | `FATO` derivado |

> A busca do GitHub omite forks por padrão — por isso 4 repositórios já catalogados
> (todos forks) não aparecem nos 107. O snapshot histórico totaliza 111.
> Tombstone não reescreve a história: apenas impede rota, ingestão e navegação ativas.

## 2. Backlog por estrato provisório (`HIPOTESE` — confirmar lendo o README)

O estrato abaixo é inferido do **nome/descrição** apenas. É hipótese de trabalho para
priorizar, não classificação final (a final exige o passo 1 do onboarding, `11_`).

- **Núcleo / cripto / quantum:** ZIPRAF_CORE, Rafaelia_Core, RAFAELIA_CORE, Semente,
  rafaelia-core-enterprise, GAIA-PDS-PHI, omega-rafaelia, Zrf, ziprar, Bitraf-Bit-quantum,
  QUANTUM_source_code, QUANTUM_auth_certificate, ESTADO-FRACTAL-HAJA, Tora, Geral.
- **Plataforma / apps / segurança:** RafNet-Core, Seguran-a-informacional-, StudiesArm64,
  Firewall, apk-privacy-rafaelia, apk-guardian-rafaelia, apk-gboard-insight, apk-js-zrf-privacy.
- **Cognição / IA:** nanoGPT (fork), treinarModelos, IaFcea, IA_nist, IA-Generativa, Ia-rafaelProjeto.
- **Ciência / matemática / física:** RafaelCiencias, Fisica, Catalogo-cosmologico, Cosmos,
  Clima, TeoremasTesesTeorias, teoremas, RafaelIA_Solucoes_Clay, GEOMETRIA_SOLAR_Maia_Inca,
  ASTRA-FRACTAL-PIPE, Clay-Maths, solvedClayMaths, Tegmark, Entropia-aponta-a-origem-do-feito,
  Atomic_EX_WASTE, Eletron-efeitos-qu-ntico, PlamaticGravity-, Whilehole, BIOSINTETICOS, Bio.
- **Jurídico / ética / manifestos:** Judicial-, Etica-nas-Intelig-ncia-artificial-,
  Analise-juridica, Constituicao-brasileira-leis, manifesto-antioligopolio-rafaelia,
  Manifesto-publico, apk-ethics-rafaelia, apk-antitrust-rafaelia, Particula-Omega-.
- **Espiritual / publicação:** verbum-vivo, CientiEspiritual, CientiEspiritual-tiEs-,
  templo-vivo-arcs, Espiritual-espirualidade, CreFeBerna, Graditao,
  Unify_Teory_of_mission_holly_espiritual_ciencias_, cienti-espiritual-verbo-vivo,
  CIENTIESPIRITUAL_MANIFESTO, Cren-as-ESPIRITUAL-amparo-LEGAL-SAGRADO.
- **Meta / dados / indefinido:** MemRa, rafaelia_privado, Rafaelia, RAFNATIONS_CORE,
  RAFNET_CORE, RAIAREIS_FRAMEWORK, fcea-originum, Pesquisa, Img, privadoFazendo,
  Motorhall-4.x, 'new', V79-1.

Lista legível por máquina: [`../indices/BACKLOG_ACERVO.yaml`](../indices/BACKLOG_ACERVO.yaml).
O deny-gate de precedência é [`../indices/ROUTE_DENYLIST_ILLICIT_USE.yaml`](../indices/ROUTE_DENYLIST_ILLICIT_USE.yaml).

## 3. O que a descoberta já ensina (padrões `HIPOTESE`)

- O acervo tem **clusters densos** que confirmam os estratos do catálogo: um forte núcleo
  *CientiEspiritual/verbo-vivo* (L5), um cinturão *jurídico-ético* (Berna, LGPD, antitrust,
  manifestos) e uma ampla faixa *científica* (Clay-Maths, cosmologia, física quântica).
- Vários repos `apk-*` sugerem uma **família de proteção/privacidade** — candidata a
  prioridade alta pela regra I2 (proteção) se tocarem dados de usuários.
- Nomes como `QUANTUM_auth_certificate`, `Particula-Omega-` e as descrições sobre
  "Convenção de Berna" indicam **camada de custódia/direitos autorais** a mapear com cuidado.

## 4. Ordem de onboarding recomendada (aplica prioridade pró-humano de `08_`)

1. **Proteção/dados primeiro:** família `apk-*`, `IA_nist`, `Etica-nas-IA`, `Analise-juridica`,
   `Constituicao-brasileira-leis` (exposição a dados/direitos).
2. **Núcleos e dependências:** `*_CORE`, `ZIPRAF_CORE`, `Zrf`, `Bitraf-Bit-quantum`.
3. **Ciência com valor de publicação:** `Clay-Maths`, `solvedClayMaths`, `Tegmark`, `Cosmos`.
4. **Espiritual/publicação:** cluster `CientiEspiritual*`, `verbum-vivo`.
5. **Indefinidos e backups:** por último; muitos podem entrar como `SPEC`/`LACUNA`.

Antes de qualquer onboarding, aplicar o deny-gate semântico. Ocorrência ambígua vira
`TOKEN_VAZIO`, com `route_allowed=false`, até revisão.

## 5. Limite honesto

O snapshot de 2026-07-05 registrou 83 pendentes. Após a retirada de uma rota por
governança em 2026-08-25, existem **82 pendentes ativos** nesse snapshot. Conteúdo não
lido continua `LACUNA`; não se inventa classificação.

Referências jurídicas, científicas, médicas, toxicológicas ou de saúde pública não são
apagadas por palavra-chave: são preservadas quando o contexto é legítimo. Substrings
puramente técnicas também são preservadas.

## 6. Próxima ação objetiva

- Trazer repositórios a escopo (`add_repo owner/repo`) na ordem da Seção 4 e rodar o
  protocolo de `11_` §3 por lote, **sempre após o deny-gate semântico**.
- A cada lido, o estrato provisório (`HIPOTESE`) vira `FATO`, entra ficha em `03_` e
  registro em `indices/CATALOGO_BIBLIOTECONOMICO.yaml`.
- Manter contagem histórica separada de rotas ativas/tombstonadas.
- `BLOCK_ILLICIT_USE` remove rota/ingestão; `TOKEN_VAZIO` bloqueia até revisão;
  evidência jurídica e ciência neutra permanecem auditáveis.
