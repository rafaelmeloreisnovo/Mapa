# Rota federada ZIPRAF-AO42

O Mapa não contém o corpo do arquivo nem substitui as fontes de autoridade. Ele registra somente ponteiros, estados, ordem de revisão e lacunas.

```text
Matem-tica- #3       → definição, provas e verificador finito
ZIPRAF_CORE #5       → ABI binária e ponto de 64 bits
ZIPRAF_OMEGA_FULL #30→ writer/leitor append-only e quatro vistas
ChipQuantum #41      → cache matricial fixo no hot path
RafPolimata #137     → gates de privacidade, cache, append e claims
GAIA_phi #46         → recibo pointer-only e digests
papers #9            → síntese acadêmica e falsificadores
Mapa #25             → navegação sem autoridade sobre os corpos
```

## Geometria

\[
4\text{ vistas}\rightarrow\binom42=6\text{ arestas}\rightarrow6\times7=42\text{ hiperformas}.
\]

Hash e cache são camadas transversais. Não ampliam a cardinalidade das vistas de conteúdo.

## Situação D

```text
SO comum → bytes, páginas e offsets
codec AO42 → manifesto, vistas, relações, cache e provas
```

A ausência do codec significa semântica opaca, não perda física automática dos bytes.

## Ordem de rollout

1. revisar a formalização;
2. revisar a ABI binária;
3. revisar o writer append-only;
4. executar cache e core no alvo ARM32;
5. validar governança e custódia;
6. realizar ZIP64 e adaptadores gráficos reais;
7. executar ablação 36/42/48/64;
8. somente então revisar promoção acadêmica.

## Lacunas preservadas

```text
ZIP64 >4GiB = TOKEN_VAZIO
Android/ARM32 = TOKEN_VAZIO
GIF89a/JPEG ISO adapters = TOKEN_VAZIO
42 comparative superiority = TOKEN_VAZIO
remote CI = PARTIAL_BLOCKED
claim_allowed = false
```
