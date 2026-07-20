# Repository Gap Mapper — Parte 1

## Objetivo

Transformar arquivos soltos e diretórios heterogêneos em um mapa técnico reproduzível,
sem confundir presença de arquivo com integração, compilação ou prova de execução.

O mapper é `stdlib-only` e roda em Termux, Linux, macOS, Windows e GitHub Actions.
Ele reconhece, por extensão e/ou magic bytes:

- fontes ASM (`.S`, `.s`, `.asm`, `.inc`);
- fontes nativas C/C++ e fontes JVM;
- descritores Gradle, CMake, Meson, Make e Android build;
- ELF, DEX, APK, AAR, JAR e ZIP;
- documentos e textos com `TODO`, `FIXME`, `TBD`, `TOKEN_VAZIO`,
  `PLACEHOLDER`, `STUB` ou `NOASSERTION`.

Para fontes ASM, C/C++ e JVM, o relatório também registra se o nome/caminho aparece
em algum descritor de build. Isso é uma **heurística de triagem**, não uma prova de
compilação: `build_referenced=true` significa somente que existe referência textual.

## Execução local multirrepositório

```bash
python3 tools/repository_gap_mapper.py \
  --root Vectras=../Vectras-VM-Android \
  --root qemu=../qemu_rafaelia \
  --root termux=../termux-app-rafacodephi \
  --root rafgit=../RafGitTools \
  --root androidx=../androidx_RmR \
  --output-json resultados/REPOSITORY_GAP_MAP.json \
  --output-md resultados/REPOSITORY_GAP_MAP.md \
  --fail-on none
```

O nome antes de `=` é estável e aparece no JSON/Markdown. Sem `NAME=`, o nome do
diretório é usado.

## Varredura de artefatos produzidos

Diretórios `build`, `.gradle`, `target`, `dist`, `node_modules` e equivalentes são
ignorados quando estão dentro da raiz de um repositório. Para inspecionar saídas de
build, passe o diretório de saída como outra raiz:

```bash
python3 tools/repository_gap_mapper.py \
  --root source=. \
  --root apk=app/build/outputs/apk \
  --root dex=app/build/intermediates/dex \
  --root native=app/build/intermediates/merged_native_libs \
  --output-json resultados/BUILD_ARTIFACT_MAP.json \
  --output-md resultados/BUILD_ARTIFACT_MAP.md
```

## Gates

`--fail-on` controla o código de saída:

| Valor | Falha quando |
|---|---|
| `none` | nunca; apenas inventaria |
| `markers` | encontra marcadores não resolvidos |
| `asm` | encontra ASM sem referência textual no build |
| `binary` | encontra ELF/DEX/APK/AAR/JAR sem sidecar de proveniência |
| `hash` | um hash completo não pôde ser produzido |
| `any` | qualquer gap é detectado |

Códigos de saída:

- `0`: execução válida e gate satisfeito;
- `1`: mapa gerado, mas o gate selecionado encontrou gaps;
- `2`: erro de entrada, caminho ou leitura.

## Proveniência de binários

Um artefato binário é considerado acompanhado quando existe ao menos um sidecar:

```text
arquivo.sha256
arquivo.spdx.json
arquivo.provenance.json
```

A presença do sidecar não prova que o conteúdo está correto. Ela apenas retira o
estado de “binário completamente órfão”; validação criptográfica e jurídica continua
sendo uma etapa separada.

## Contrato epistemológico

```text
arquivo existe           != integrado ao build
referenciado no build    != compilado
compilado                != empacotado
empacotado               != instalado
instalado                != executado
executado                != comportamento validado
```

Portanto:

```text
claim_allowed=false
```

até que a cadeia `código -> build -> artefato -> instalação -> execução -> evidência`
esteja registrada no repositório consumidor.

## Limites conhecidos da Parte 1

- a associação ao build é textual; não interpreta integralmente Gradle/Meson/CMake;
- APK/ZIP é identificado como contêiner, mas a inspeção profunda de DEX e ELF internos
  pertence à Parte 2;
- arquivos maiores que `--max-hash-bytes` recebem `HASH_INCOMPLETE`;
- ausência de SPDX é registrada como metadado, mas não bloqueia automaticamente,
  porque repositórios upstream podem usar licença por árvore.

## Próxima integração

A Parte 2 deve consumir este JSON para:

1. abrir mapas por repositório e por classe de risco;
2. inspecionar `classes*.dex` dentro de APK/AAB e comparar versões/contagens;
3. extrair ABI/machine de ELF e cruzar com `armeabi-v7a`/`arm64-v8a`;
4. promover, integrar ou quarentenar ASM solto;
5. alimentar `ALL_GAPS_REGISTRY.md` sem edição manual destrutiva.
