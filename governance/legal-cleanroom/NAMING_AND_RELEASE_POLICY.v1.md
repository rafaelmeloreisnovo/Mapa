# Naming, Authority and Release Policy V1

## Legacy names

Names such as `Termux`, `QEMU`, `llama.cpp`, `AndroidX`, and `Vectras VM` identify upstream projects/ecosystems. Their presence in provenance records is factual attribution and must not be erased to create an appearance of independent origin.

## New RAFAELIA naming

A new clean-room implementation may use a distinct RAFAELIA product/module name only after:

1. implementation scope is independently evidenced;
2. no shipped code/assets remain classified C/D inside that scope;
3. required upstream notices for retained interfaces/components are preserved;
4. public-name/trademark clearance is recorded.

### Provisional Vectras replacement name

Technical codename: **RAFAELIA Virtual Runtime** (`RVR`).

Rationale: descriptive of the new intended runtime, does not imply the legacy `Vectras` identity, and leaves VM/emulation implementation details modular.

This is a provisional engineering codename only:

`public_brand_authorized=false`

`trademark_clearance=TOKEN_VAZIO`

## Authority precedence

For licensing and origin:

`official upstream license/file notice > fork summary docs > index > memory > inference`

For RAFAELIA authorship:

`content/blob evidence + lineage + independent creation receipt > repository ownership/name`.

## No laundering rule

It is forbidden by project policy to attempt to convert third-party code into an 'original' artifact merely by:

- renaming identifiers;
- changing formatting;
- translating language;
- paraphrasing comments;
- reorganizing files;
- decompiling/recompiling;
- mechanically rewriting control flow;
- removing copyright headers;
- changing the repository/product name.

Such transformations preserve provenance/derivation risk and must remain attributed/licensed as applicable.
