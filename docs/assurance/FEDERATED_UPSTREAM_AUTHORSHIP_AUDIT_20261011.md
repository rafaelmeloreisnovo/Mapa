# Auditoria federada de autoria, upstream e direitos — 2026-10-11

**Estado:** SOURCE_AUDITED_PARTIAL / METADATA_GATE / HOLD_NO_PROMOTION.
**Autoridade:** cada repositório produtor governa seu código; Mapa governa apenas
o índice/rota federada; RLL governa a formulação e seus falsificadores científicos.
**Manifesto:** `data/assurance/federated-authorship-intake-20261011.v1.json`.
**Falsificador:** `tools/validate_federated_authorship_intake_v1.py`.
**Proibição:** NÃO promover nem importar código, binário, licença ou dados privados
apenas por nome de arquivo, licença-raiz, autodeclaração, DOI ou hash Git.

## Prioridade de leitura e classificação
1. `UPSTREAM_DERIVED` / `UPSTREAM_MODIFIED`: autoria original e licença
   do autor oficial; apenas o diferencial comprovado pode ser contribuição local.
2. `PROJECT_LOCAL_TRACEABLE_AI_ASSISTED`: primeiro aparecimento verificável
   dentro deste projeto, com contribuição do mantenedor/IA; NÃO prova
   originalidade universal nem autoriza remoção da licença upstream.
3. `PROJECT_DECLARED_AUTHORIAL`: cabeçalho declara autoria, mas ausência
   de código idêntico no upstream não é prova universal; exigir árvore ancestral,
   introdução, licença e revisão.
4. `MIXED_UNVERIFIED`, `TOKEN_VAZIO`: bloquear cópia; manter metadata pointers.
5. `RESEARCH_REFERENCE`: documentar conceito, equação e evidência científica
   separadamente de licença de software e runtime.
6. `RESTRICTED_PRIVATE`: não copiar bytes, corpus, PII/PHI ou tokens;
   registrar somente ponteiro mínimo autorizado.

## Contraste Vectras original ↔ repositório RAFAELIA

Upstream canônico: `xoureldeen/Vectras-VM-Android`, README observado
blob `311708d8f47ebc732775b2ae1baa67047ea295e5`, LICENSE GPLv2
blob `89e08fb002e48e22363b7b3789a5470ffe71fea1`.
Fork/projeto RAFAELIA: `rafaelmeloreisnovo/Vectras-VM-Android`, LICENSE GPLv2
blob `7af071d115add5c858c2373891459a9af711e73b`, com atribuição explícita
a xoureldeen e aos contribuidores.

- `app/src/main/java/com/vectras/vm/AboutActivity.java`:
  upstream blob `f447163f51fc63fef570821086c983e0e1369aef`;
  fork blob `a2aa44474765ebd21956c5bf5b53fc9e89c95cd2`.
  Corpos conservam estrutura/identificadores/imports comuns mas variam; classe
  `UPSTREAM_MODIFIED`, não autoral integral. Cálculo de merge-base e blame
  por trecho continuam pendentes. O arquivo de custódia existente
  `resources/compliance/PROVENANCE_TRANSFORM_REGISTER.jsonl` já registra esta
  incerteza e preserva origens oficiais.
- `engine/rmr/src/rmr_vector_field.c`: fork blob
  `8dfb230410b20e36236dbc3863d301e16a4c595d`; mesma rota não encontrada
  no upstream observado. Registro do fork liga a inclusão a PR #982/commit
  `2e25ec094d351c9aed068711a1f7ad676fc03632` e hardening PR #1142;
  classificar `PROJECT_LOCAL_TRACEABLE_AI_ASSISTED`, não prioridade histórica
  mundial. Cabeçalho SPDX `GPL-2.0-only` e header
  `engine/rmr/include/rmr_vector_field.h` também GPL-2.0-only.
- **Sem cópia para RafGitTools/Mapa**: ambos usam GPLv3 enquanto GPLv2-only
  não deve ser presumida compatível com redistribuição como obra GPLv3.
  Contrato de processo/dados/ABI separado é possibilidade, não licença
  automática; verificar combinação/derivação com auditoria jurídica própria.
- `LICENSES_REGISTER.md` do Vectras já bloqueia release por binários, firmware,
  assets, notices e proveniência sem fechar; esta auditoria não revoga o HOLD.

## Llama, GAIA, Rafaelia_Private, Termux, Packet
- `llamaRafaelia`: ggml-org/llama.cpp é upstream MIT; root LICENSE
  blob `acb96ce78e0486e9dc7602cdcdd2f491c34f335a`.
  `rafaelia-baremetal/LICENSE` blob `74efcc46f821d64496b0141749be42bd0d773b51`
  declara contribuições locais sob MIT, mas
  `rafaelia-baremetal/bitstack/raf_bitstack.c` usa
  stdlib/string/stdio/math/malloc/calloc. **NÃO é L0 sem dependências**.
- `GAIA_phi` root LICENSE MIT blob `f2a2f9fd2d04b99cd3126731640edcea3fea326b`;
  `LICENSE.md` blob `e46eb4d9ddda24723f7d1fc4c3d2de5cc95eb4b1`
  impõe cláusulas adicionais e inclui Python — contradição aberta.
  `native/raf_bl0/raf_bl0.c` blob `132f948d199f6679fcae4f33912e0a3ad69691a3`
  é candidato zero-includes declarado autoral; direitos/ancestralidade, limites
  de memória e testes independentes antes de importar. `net/gaia_phi.c`
  blob `d48a8c01bd698796bde4ce582a78b2d8f9af54ea` faz rede/saída:
  serviço do sistema operacional, NÃO kernel L0.
- `GAIA-PDS-PHI`: manifesto conceitual blob
  `8dde2aa8d63a43bfe6091220d9e8c28b28fdddc4`, licença-raiz
  não observada; nenhuma implementação adquirida por interpretação do manifesto.
  `GaiaPhiRafcode` contém acervo legado com origem fragmentária
  (`docs/10_COLLECTION_ORIGIN_TRACE_MATRIX.md` blob
  `202ed1b4956efa9f1116a0574c0f3b6dce71d549`); não renomear
  registros antigos como autoria exclusiva.
- `Rafaelia_Private`: licença custom v1000 **proposta/file-scoped**
  blob `4a8412f96ff5dff708e0b8043e8441aff27904d8`, sem
  relicenciamento de terceiros. Custódia privada permanece privada e não
  vira artefato de código público. `docs/privacy/PRIVACY_DATA_GOVERNANCE_ZERO_TRUST_V1.md`
  é política draft, não certificação.
- `termux-app-rafacodephi`: fork do termux/termux-app, GPLv3-only
  com exceções, `LICENSE.md` blob `470c7d9c51b0b61a5fc4868f293d87b4c34ccc5f`.
  `termux-packages`: `LICENSE.md` blob
  `a901a9b5b014d9e50316d300066ed0069f1f4bd8`: patches/receitas
  seguem licença de cada pacote; infraestrutura fora de packages/ etc Apache
  2.0. `docs/assurance/rafcodephi-federated-components.v1.json`
  já estabelece integração por artefatos/contratos, não transplantação de QEMU.
- `relativity-living-light`: `LICENSE.md` blob
  `09735ecfbc52903f654b87d260d96f5b7c67c9f1` atribui CC BY-SA 4.0
  a conteúdo acadêmico autoral, **não** licencia automaticamente scripts.
  Equações e limites nulos são hipóteses com falsificadores: fonte de modelo,
  não de implementação freestanding comprovada.
- `RafPolimata` L0: root LICENSE não observada, estado `P0_RIGHTS`.
  `RafGitTools` root LICENSE GPLv3-or-later, blob
  `f0433f024df053a0e11a5b8eac35a9d73da99b70`. Copiar
  fonte da Vectras GPLv2-only para este produto requer autoridade específica.

## Critério de transposição
`source origin + exact blob + authorship span + applicable per-file rights +
dependency closure + independent review + tests at exact head +
security/privacy scope -> governed integration decision`.

Sem fechar a cadeia: `METADATA_POINTER_ONLY`, `claim_allowed=false`.
Nenhuma passagem é promovida por licença MIT presumida, pela tag
"autoral" ou por compilação. Para L0: ausência de libc, heap, OS,
bibliotecas e símbolos indefinidos **deve ser testada**, não inferida do README.

## R3
F_ok = catálogo federado tipado, evidências e falsificadores negativos; a
diferença Vectras original vs fork e os riscos MIT/GPL foram registrados.
F_gap = prova global de autoria/novidade, merge-base Vectras, revisão jurídica,
licença-raiz RafPolimata, corpus/execução real, privacidade e revisão externa.
F_next = obter por arquivo a introdução/ancestralidade e razão de delta,
provar zero-dep nos candidatos, integrar via contratos sem copiar obras não
autorizadas; administrar decisão de promoção só com provas independentes.
