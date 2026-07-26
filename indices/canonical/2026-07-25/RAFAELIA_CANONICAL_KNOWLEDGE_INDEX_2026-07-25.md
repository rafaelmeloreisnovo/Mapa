# Índice Canônico de Conhecimento e Integridade — RAFAELIA

Snapshot UTC: `2026-07-26T00:35:38.018795+00:00`  
Escopo: `101` repositórios referenciados, `99` commits HEAD observados, `2258` arquivos com triplo digest.

## Regra de leitura

Cada registro liga uma fonte a um estado verificável: `repositório → commit → caminho → Git blob (quando disponível) → MD5 + SHA-256 + BLAKE3-256`. Um hash fixa bytes; não prova por si só desempenho, segurança, autoria exclusiva ou validade científica.

| Campo | Função |
|---|---|
| MD5 | Compatibilidade e comparação legada; não usar como prova criptográfica adversarial. |
| SHA-256 | Digest principal de integridade. |
| BLAKE3-256 | Digest criptográfico rápido e paralelo; o calculador foi conferido com o vetor BLAKE3 vazio. |
| Commit Git | Referência temporal do estado do repositório. |
| Git blob | Identidade do objeto de texto devolvida pelo GitHub para o arquivo fixado. |

## Cobertura

- Arquivos-raiz enviados: `16`
- Arquivos de snapshots extraídos: `2122`
- READMEs GitHub fixados e hasheados: `89`
- Arquivos de núcleo GitHub fixados e hasheados: `28`
- Lacunas auditáveis (`TOKEN_VAZIO`): `19`

## Arquivos de conhecimento direto

| Componente | Papel | Metodologia/ideia | SHA-256 | BLAKE3-256 | Estado |
|---|---|---|---|---|---|
| Tora | visão de projeto | conversão e integração multi-arquitetura | 15bd4e196324 | e777a532e280 | OBSERVED_AND_HASHED |
| Tora | arquitetura | camadas Android/JNI/ASM | 70b1626b2458 | 42f25ef790a6 | OBSERVED_AND_HASHED |
| Tora | núcleo Bitraf | estrutura binária e integridade | a97aec70b12b | 616fd9d26c5f | OBSERVED_AND_HASHED |
| Tora | indexação CTI | índice/inventário de conversas | 1f4bc311bd61 | ed7b31819cb5 | OBSERVED_AND_HASHED |
| Tora | benchmark nativo | medição C/JNI | ddf35c2cff9e | 5dfed21c2b8b | OBSERVED_AND_HASHED |
| BLAKE3 snapshot | primitiva criptográfica | Merkle, streaming, SIMD | 37a8106a16f1 | 45777b9e48ea | OBSERVED_AND_HASHED |
| BLAKE3 snapshot | orquestração de build | seleção de backend/flags | de3a140cdde0 | 776f94cc18b7 | OBSERVED_AND_HASHED |
| BLAKE3 snapshot | dispatch C | detecção CPU e seleção SIMD | 3cf2fa2449ff | 70b34e961e48 | OBSERVED_AND_HASHED |
| BLAKE3 snapshot | scanner RMR | inventário e digest | 1ee8b39dcf70 | 67306142447d | OBSERVED_AND_HASHED |
| BLAKE3 snapshot | governança RMR | política e limites | db622a35c270 | 0b94a3f6291f | OBSERVED_AND_HASHED |
| BLAKE3 snapshot | arquitetura RMR | cadeia de custódia | 67134ade4928 | 66884816b5f2 | OBSERVED_AND_HASHED |
| Termux RafaCodePhi snapshot | fork Android | terminal/Android e módulos nativos | c7fc43092c18 | 89802cece4a5 | OBSERVED_AND_HASHED |
| Termux RafaCodePhi snapshot | Bitraf nativo | ponte C/JNI | a911d74c33b6 | 73cdefe48779 | OBSERVED_AND_HASHED |
| Termux RafaCodePhi snapshot | ponte RMR | API Java para núcleo | d005e827c21f | a87cc8872623 | OBSERVED_AND_HASHED |
| Termux RafaCodePhi snapshot | interface low-level | integração Android | 6e6ac4c21bd4 | 8c0e97a09e76 | OBSERVED_AND_HASHED |
| Termux RafaCodePhi snapshot | emulação/execução | ponte nativa | e01d947489d7 | ba1aa6e0ef5b | OBSERVED_AND_HASHED |
| RLL snapshot | modelo e validação | pipeline observacional | 617b83cbef6e | 35a1086a6969 | OBSERVED_AND_HASHED |
| RLL snapshot | orquestração pipeline | execução de fases e resultados | 590eee5f4da1 | 86f3a3db3c9b | OBSERVED_AND_HASHED |
| RLL snapshot | inferência estatística | comparação/modelagem | de5c93c93158 | ed74e5610b9a | OBSERVED_AND_HASHED |
| RLL snapshot | interface CLI | execução reprodutível | 4a1d5a93f2b1 | 5faf0e951705 | OBSERVED_AND_HASHED |
| RLL snapshot | auditoria de lacunas | registro de gaps | bea143c48f96 | 3f9b337e703d | OBSERVED_AND_HASHED |
| RAFBROWSER v1 | arquitetura de cliente | camadas TLS/HTTP/ASM | 6853d589de5e | 4dc26bab47f6 | OBSERVED_AND_HASHED |
| RAFBROWSER v1 | build | alvos de compilação | 3c50c38a66f3 | c3a46743a671 | OBSERVED_AND_HASHED |
| RAFBROWSER v1 | TLS 1.3 | handshake/record layer | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO:local_core_path_not_found |
| RAFBROWSER v1 | testes vetoriais | verificação criptográfica | 1eeddadb9b46 | b877f777391a | OBSERVED_AND_HASHED |
| RAFBROWSER current | arquitetura de cliente | C/ASM/HTTP/TLS | 32c3e2b40b15 | 1089ecef3d5a | OBSERVED_AND_HASHED |
| RAFBROWSER current | build CMake | targets multiplataforma | 4b115b090c0a | 0bd82b5edd5d | OBSERVED_AND_HASHED |
| RAFBROWSER current | TLS 1.3 | handshake/record layer | e307b5b372b6 | 370329dcd84f | OBSERVED_AND_HASHED |
| RAFBROWSER current | SHA-256 | digest/HMAC/HKDF | 4e11f8ce22ed | da08fa71adb3 | OBSERVED_AND_HASHED |
| RAFBROWSER current | X25519 | troca de chaves | 7b11ff686ad6 | 064b47641e34 | OBSERVED_AND_HASHED |
| Atlas | síntese interárea | mapa de 10 áreas e fórmulas | 90818112c904 | 437e13800395 | OBSERVED_AND_HASHED |
| Sessão consolidada | dossiê de sessão | separação entre evidência, hipótese e gap | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO:local_core_path_not_found |
| Sessão consolidada | índice estruturado | ingestão por máquina | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO:local_core_path_not_found |
| rafaelmeloreisnovo/Mapa | schema de orquestração | contratos, estados e gates | 596aaff0ff70 | 26eb99a73b41 | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/Mapa | índice omni-contexto | índice declarativo de referências | f24be45b5542 | e4cf0e90b239 | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/Mapa | inventário automatizado de ativos | catálogo de artefatos | 8f7748c11a7c | d4a20a79bcb7 | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/Mapa | política de custódia | proveniência e trilha de auditoria | d3b912cf935c | 673b527143a7 | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/Mapa | validador topológico | verificação de grafo e contratos | 4789040c26b2 | a3f4946413b1 | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/BLAKE3 | orquestração de build BLAKE3 | seleção de backend e flags | de3a140cdde0 | 776f94cc18b7 | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/BLAKE3 | dispatch SIMD BLAKE3 | detecção de CPU e rotas de compressão | af26d1131bcd | 6f2a09582a2c | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/BLAKE3 | scanner RMR | inventário e hashing de objetos | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO:core_file_empty |
| rafaelmeloreisnovo/BLAKE3 | política central RMR | contratos de governança | 0d41c7d975eb | 3a9ddab7973e | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/BLAKE3 | cadeia de custódia PAE | evento e hashchain | TOKEN_VAZIO | TOKEN_VAZIO | TOKEN_VAZIO:core_file_empty |
| rafaelmeloreisnovo/Vectras-VM-Android | resolver multi-ISA | seleção de binário QEMU | 71040b806cbc | 2e21f7b13702 | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/Vectras-VM-Android | partida de VM | preflight e execução de guest | e32d6d58cde9 | 7577869cb194 | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/Vectras-VM-Android | núcleo Bitraf | frame binário e integridade rápida | 0e927a48f3fa | 26a751fef3e0 | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/Vectras-VM-Android | núcleo ZIPRAF/RMR | contêiner, recibo e recuperação | 6d8c6b8df43a | a1898ee150c0 | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/Vectras-VM-Android | fluxo de execução VM | documentação de estados | 7c953e3d2611 | 42cd09916e7c | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/RafPolimata | segmento RAFSEG1 | layout binário de conversas | 9781d57f2111 | 837c1a761632 | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/RafPolimata | contrato RAFSEG1 | interface e limites de registros | c77b6ef9b648 | 94de02e2405d | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/RafPolimata | teste RAFSEG1 | teste de reader/writer | 7e1f3df1ed4d | 827534f3de18 | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/RafPolimata | estado do ecossistema | ledger de componentes | 90e17b47b85d | 6d05c7583f75 | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/RafGitTools | roteador de ferramentas | allow-list e TOKEN_VAZIO | 62a6ab263d9c | 41a596738ad4 | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/RafGitTools | gate de governança | autorização de ferramentas | 59f7e41cb293 | 3ec7eb3119b3 | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/RafGitTools | arquitetura RafGitTools | contratos de camadas | ef06ae4ed68c | 175623db97c8 | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/termux-app-rafacodephi | núcleo Bitraf nativo | C/JNI e integridade | e16c1112797f | ad5798b7c7d1 | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/termux-app-rafacodephi | ponte RMR Java | API Android para núcleo RMR | d005e827c21f | a87cc8872623 | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/termux-app-rafacodephi | build nativo Android | NDK/ABI build mapping | 2fe71d45a1c8 | 00c904dcb3bc | OBSERVED_AND_HASHED |
| rafaelmeloreisnovo/termux-app-rafacodephi | auditoria de runtime | contratos de matemática e execução | 35a6ca066dd4 | 1d061e72177c | OBSERVED_AND_HASHED |
| instituto-Rafael/relativity-living-light | pipeline científico RLL | etapas de validação e falsificação | 24d1b2b18af8 | b6be1859a0dc | OBSERVED_AND_HASHED |
| instituto-Rafael/relativity-living-light | relatório final RLL | resultado de CI e comparação | ecd8c1ecb741 | 6cc6204de429 | OBSERVED_AND_HASHED |
| instituto-Rafael/relativity-living-light | resultado Bayes | comparação de modelos | a89cbf21ee3b | b6972df13bc2 | OBSERVED_AND_HASHED |
| instituto-Rafael/relativity-living-light | ledger RLL | transições de estado | 4299fd583a82 | dec3748389de | OBSERVED_AND_HASHED |

## Tabela de referências Git

| Repositório | Classe | Cobertura | Commit HEAD | README SHA-256 |
|---|---|---|---|---|
| instituto-Rafael/apk-antitrust-rafaelia | memoria_e_agentes | README_HASHED | ffe13f90181d | c6856ef2398d |
| instituto-Rafael/apk-ethics-rafaelia | memoria_e_agentes | README_HASHED | 5a141c340945 | 068c3695f3fb |
| instituto-Rafael/apk-gboard-insight | satellite_or_unclassified | README_HASHED | 52af08d29be5 | b8199ea2ea77 |
| instituto-Rafael/apk-guardian-rafaelia | memoria_e_agentes | README_HASHED | 9fcda40889d2 | 068c3695f3fb |
| instituto-Rafael/apk-js-zrf-privacy | satellite_or_unclassified | README_HASHED | bb4d962f29b2 | f341e682be57 |
| instituto-Rafael/apk-privacy-rafaelia | memoria_e_agentes | README_HASHED | 46660613537f | 068c3695f3fb |
| instituto-Rafael/BIOSINTETICOS | satellite_or_unclassified | README_HASHED | 223a4ebced77 | 0648518e1ae7 |
| instituto-Rafael/cienti-espiritual-verbo-vivo | satellite_or_unclassified | README_HASHED | dd03669f959e | 04f2bbdfe005 |
| instituto-Rafael/CIENTIESPIRITUAL_MANIFESTO | governanca_documentacao_e_conhecimento | README_HASHED | 9588a2bbd363 | 9835de465210 |
| instituto-Rafael/Cren-as-ESPIRITUAL-amparo-LEGAL-SAGRADO | satellite_or_unclassified | README_HASHED | eb42e5535238 | 26ccdd29a81c |
| instituto-Rafael/Eletron-efeitos-qu-ntico | satellite_or_unclassified | README_HASHED | 6e76984661b9 | dffefa874a13 |
| instituto-Rafael/Entropia-aponta-a-origem-do-feito | memoria_e_agentes | README_HASHED | 894580b2aadb | 85f97cf0209d |
| instituto-Rafael/Etica-nas-Intelig-ncia-artificial- | memoria_e_agentes | README_HASHED | ebc3cf5073ed | f49cb8b74707 |
| instituto-Rafael/LGPD-Constituicoes-planetaria-paises-onu-direitos-humanos-e-fundamentais-de-cada-continents-geologic | memoria_e_agentes | METADATA_ONLY | 99f9d9f4b7b3 | TOKEN_VAZIO |
| instituto-Rafael/manifesto-antioligopolio-rafaelia | memoria_e_agentes | README_HASHED | 80d96297e2bf | c5a9c6a33018 |
| instituto-Rafael/Manifesto-publico | governanca_documentacao_e_conhecimento | README_HASHED | 41c28f207811 | 5aefa1b4954d |
| instituto-Rafael/omega-rafaelia | memoria_e_agentes | README_HASHED | b236f92e6b77 | 7bf671c4b76a |
| instituto-Rafael/publicacientiespiritual | governanca_documentacao_e_conhecimento | README_HASHED | 8997bf388505 | f4ccff96646a |
| instituto-Rafael/QUANTUM_source_code | pesquisa_cientifica_e_modelagem | README_HASHED | e079602d0ade | 55c64e7b27f4 |
| instituto-Rafael/RAFAELIA_CORE | memoria_e_agentes | README_HASHED | 0860d40907fd | fbca66f7ad24 |
| instituto-Rafael/RAFNET_CORE | satellite_or_unclassified | README_HASHED | 41512c2316a7 | 8251758e26b5 |
| instituto-Rafael/relativity-living-light | pesquisa_cientifica_e_modelagem | CORE_DIRECT_SOURCE | 5d35f65f8095 | TOKEN_VAZIO |
| instituto-Rafael/Tegmark | satellite_or_unclassified | README_HASHED | a304d2f7287d | 7d2bca26d6d5 |
| rafaelmeloreisnovo/actions | satellite_or_unclassified | README_HASHED | a009669cd5de | 577fa8bf91cd |
| rafaelmeloreisnovo/android_frameworks_base_rafaelia | execucao_android_multiisa | METADATA_ONLY | f50cb1d753ff | TOKEN_VAZIO |
| rafaelmeloreisnovo/androidRom | execucao_android_multiisa | METADATA_ONLY | 238f60af8647 | TOKEN_VAZIO |
| rafaelmeloreisnovo/androidx_RmR | integridade_e_custodia | README_HASHED | 4f01fd23e91e | 39c0ed3ac2a4 |
| rafaelmeloreisnovo/BLAKE3 | integridade_e_custodia | CORE_DIRECT_SOURCE | 31419ed18928 | 37c7670e9081 |
| rafaelmeloreisnovo/Catalogo-cosmologico | governanca_documentacao_e_conhecimento | README_HASHED | 9f8ab816ff91 | 7274e529490d |
| rafaelmeloreisnovo/ChipQuantum | pesquisa_cientifica_e_modelagem | README_HASHED | 9402403bb0f6 | 651692ec04b3 |
| rafaelmeloreisnovo/CientiEspiritual | governanca_documentacao_e_conhecimento | README_HASHED | 9b90daa39d79 | bddff86647e4 |
| rafaelmeloreisnovo/CientiEspiritual-tiEs- | governanca_documentacao_e_conhecimento | README_HASHED | 0c7e9da64733 | 7ea93311cfb6 |
| rafaelmeloreisnovo/Clima | satellite_or_unclassified | README_HASHED | 188d5cd95a6b | 29000ebbee86 |
| rafaelmeloreisnovo/CONVERSATIONS_CHUNKS_PRIVATE | memoria_e_agentes | README_HASHED | 0bf0d62ee27d | 806f2d19684d |
| rafaelmeloreisnovo/Cosmos | pesquisa_cientifica_e_modelagem | README_HASHED | 93a65f1d82f6 | 00abcc24e9bb |
| rafaelmeloreisnovo/CreFeBerna | satellite_or_unclassified | README_HASHED | 56571fdc51ae | facb83e6e93c |
| rafaelmeloreisnovo/CryptoSwift_RmR | integridade_e_custodia | README_HASHED | 77a6460ee88e | 1df23d3e1cfa |
| rafaelmeloreisnovo/DeepSeek-RafCoder | satellite_or_unclassified | README_HASHED | 81182325dd85 | 5bc19a498d2f |
| rafaelmeloreisnovo/Espiritual-espirualidade | satellite_or_unclassified | README_HASHED | 81cd1f31d2a6 | a81b96cd9ff9 |
| rafaelmeloreisnovo/fcea-originum | satellite_or_unclassified | METADATA_ONLY | dc56c4f4fd1e | TOKEN_VAZIO |
| rafaelmeloreisnovo/Fisica | pesquisa_cientifica_e_modelagem | README_HASHED | 829d8511e33a | a38a3d993220 |
| rafaelmeloreisnovo/florisboard | satellite_or_unclassified | README_HASHED | c15130326dc1 | a6ed3f9759b1 |
| rafaelmeloreisnovo/frida-desktop | satellite_or_unclassified | README_HASHED | 263bafd6f294 | abdb343e07db |
| rafaelmeloreisnovo/GAIA_phi | memoria_e_agentes | README_HASHED | 224608448158 | 08c1fbb7ce7c |
| rafaelmeloreisnovo/GAIA-PDS-PHI | memoria_e_agentes | README_HASHED | 098406b6eeb5 | 2d0007893b16 |
| rafaelmeloreisnovo/GaiaPhiRafcode | memoria_e_agentes | README_HASHED | 10296c944389 | 24c4cfb4e564 |
| rafaelmeloreisnovo/GEOMETRIA_SOLAR_Maia_Inca | memoria_e_agentes | README_HASHED | a7889e7d8508 | d06d4a322895 |
| rafaelmeloreisnovo/Geral | satellite_or_unclassified | README_HASHED | 7315260bc6f2 | 8faf4a9d1014 |
| rafaelmeloreisnovo/Graditao | satellite_or_unclassified | README_HASHED | 02eecfd9d0a2 | 35a8d083bb2b |
| rafaelmeloreisnovo/gradle | satellite_or_unclassified | README_HASHED | 8ed9a557db78 | b4852e4e1e96 |
| rafaelmeloreisnovo/home | satellite_or_unclassified | README_HASHED | e827220ba9fe | fc479ec7b7b5 |
| rafaelmeloreisnovo/IA_nist | memoria_e_agentes | README_HASHED | c00cb1788167 | e496b2d543b7 |
| rafaelmeloreisnovo/IaFcea | memoria_e_agentes | README_HASHED | a8c89605ccd2 | 6bc190b70c48 |
| rafaelmeloreisnovo/Img | satellite_or_unclassified | README_HASHED | 2f31989dab8f | e028038d880a |
| rafaelmeloreisnovo/Judicial- | memoria_e_agentes | README_HASHED | 3c3ecc9292c0 | 518795176eb6 |
| rafaelmeloreisnovo/linuxkernel | satellite_or_unclassified | METADATA_ONLY | cccdbf0973ab | TOKEN_VAZIO |
| rafaelmeloreisnovo/llamaRafaelia | memoria_e_agentes | README_HASHED | df3d8f4a002c | 2ee2073dbea1 |
| rafaelmeloreisnovo/LuaJIT | satellite_or_unclassified | METADATA_ONLY | 18b087cd2cd4 | TOKEN_VAZIO |
| rafaelmeloreisnovo/Mapa | governanca_documentacao_e_conhecimento | CORE_DIRECT_SOURCE | fc73f2fd4a59 | ab4c30492e86 |
| rafaelmeloreisnovo/Matem-tica- | pesquisa_cientifica_e_modelagem | README_HASHED | 7de9b3ab8b0d | a790e3dc742e |
| rafaelmeloreisnovo/MemRa | memoria_e_agentes | README_HASHED | 4f940cdc0527 | 64aa595b23be |
| rafaelmeloreisnovo/MemRafcode | memoria_e_agentes | README_HASHED | 8d629e3be976 | 00d34ef68f21 |
| rafaelmeloreisnovo/myCat-iahelpsus | memoria_e_agentes | README_HASHED | e9fba63be25b | 2e45be71f71e |
| rafaelmeloreisnovo/nanoGPT | memoria_e_agentes | README_HASHED | b11c88b84247 | 0ec5e016d700 |
| rafaelmeloreisnovo/new | satellite_or_unclassified | METADATA_ONLY | TOKEN_VAZIO | TOKEN_VAZIO |
| rafaelmeloreisnovo/papers | governanca_documentacao_e_conhecimento | README_HASHED | 6755ab2c5b9b | 1b2665eae4cb |
| rafaelmeloreisnovo/PCR_Rafaelia_Code_seed | memoria_e_agentes | METADATA_ONLY | a9cc6cf5a363 | TOKEN_VAZIO |
| rafaelmeloreisnovo/privadoFazendo | satellite_or_unclassified | README_HASHED | 416ddd97a9a5 | 0567fef6f707 |
| rafaelmeloreisnovo/qemu_rafaelia | execucao_android_multiisa | METADATA_ONLY | dd118db9e14e | TOKEN_VAZIO |
| rafaelmeloreisnovo/RafaelCiencias | memoria_e_agentes | README_HASHED | 3dbaf7eb771f | 88fc4f827a3a |
| rafaelmeloreisnovo/Rafaelia | memoria_e_agentes | README_HASHED | 9e6808594a8b | 590e49c528b6 |
| rafaelmeloreisnovo/Rafaelia_Core | memoria_e_agentes | README_HASHED | f4c0e6ab51bc | f87c5e8353f0 |
| rafaelmeloreisnovo/rafaelia_privado | memoria_e_agentes | METADATA_ONLY | TOKEN_VAZIO | TOKEN_VAZIO |
| rafaelmeloreisnovo/Rafaelia_Private | memoria_e_agentes | README_HASHED | cebabd217800 | 5b631362d7a4 |
| rafaelmeloreisnovo/RafaelIA_Solucoes_Clay | memoria_e_agentes | README_HASHED | b37ebd523ecc | 0491bfa1e71c |
| rafaelmeloreisnovo/rafaelia-core-enterprise | memoria_e_agentes | README_HASHED | de12cfb0e387 | 472478ce6cbf |
| rafaelmeloreisnovo/RafGitTools | memoria_e_agentes | CORE_DIRECT_SOURCE | 8a2cfff6aa32 | b51f8b360166 |
| rafaelmeloreisnovo/RAFNATIONS_CORE | satellite_or_unclassified | README_HASHED | 7818b136b5a7 | 0a5143dc0f49 |
| rafaelmeloreisnovo/RafNet-Core | satellite_or_unclassified | README_HASHED | 435315c452d1 | 8251758e26b5 |
| rafaelmeloreisnovo/RafPolimata | memoria_e_agentes | CORE_DIRECT_SOURCE | 9d0163829431 | 4ab013a232ba |
| rafaelmeloreisnovo/RAIAREIS_FRAMEWORK | memoria_e_agentes | README_HASHED | 9c8a7e1214b6 | 259e12bda379 |
| rafaelmeloreisnovo/relativity-living-light | pesquisa_cientifica_e_modelagem | README_HASHED | 805f6b4a2fa6 | 9c0cad13760c |
| rafaelmeloreisnovo/ROM-emulator | satellite_or_unclassified | README_HASHED | 4c509a779b18 | 56dca8d4b343 |
| rafaelmeloreisnovo/Seguran-a-informacional- | satellite_or_unclassified | README_HASHED | 3dc4ed461b14 | 718c777d7374 |
| rafaelmeloreisnovo/Semente | satellite_or_unclassified | README_HASHED | fca23ee92d82 | 2a52868cb976 |
| rafaelmeloreisnovo/templo-vivo-arcs | satellite_or_unclassified | README_HASHED | ade5948b1487 | 84bac3297134 |
| rafaelmeloreisnovo/teoremas | pesquisa_cientifica_e_modelagem | README_HASHED | 4f24c24b122d | b2a750e0d554 |
| rafaelmeloreisnovo/TeoremasTesesTeorias | memoria_e_agentes | README_HASHED | 4987882c03f3 | 5e235e754871 |
| rafaelmeloreisnovo/termux-api_rafcodephi | execucao_android_multiisa | README_HASHED | 79cd17754e04 | 3b8746d989e9 |
| rafaelmeloreisnovo/termux-app-rafacodephi | execucao_android_multiisa | CORE_DIRECT_SOURCE | 508efb3d0159 | 9d1e7d71394f |
| rafaelmeloreisnovo/TinyGPT | memoria_e_agentes | README_HASHED | 0cb447d99f41 | 2a654fce2e14 |
| rafaelmeloreisnovo/Tora | execucao_android_multiisa | README_HASHED | 0fd5a7bf6289 | 15bd4e196324 |
| rafaelmeloreisnovo/treinarModelos | satellite_or_unclassified | README_HASHED | ed0dcc3a2778 | 8ba5751de2f0 |
| rafaelmeloreisnovo/UserLAnd | execucao_android_multiisa | README_HASHED | 95f5caa3d68c | 36e1387d7979 |
| rafaelmeloreisnovo/UserLAnd2 | execucao_android_multiisa | README_HASHED | c46771a804c9 | 96888b0990c3 |
| rafaelmeloreisnovo/V79-1 | satellite_or_unclassified | METADATA_ONLY | 12998f8798e2 | TOKEN_VAZIO |
| rafaelmeloreisnovo/Vectras-VM-Android | execucao_android_multiisa | CORE_DIRECT_SOURCE | a29392e65948 | 091f0cce5aae |
| rafaelmeloreisnovo/verbum-vivo | satellite_or_unclassified | README_HASHED | d3283299c3f8 | c7b32a8f6ca4 |
| rafaelmeloreisnovo/X0 | satellite_or_unclassified | README_HASHED | 086929b819bf | 9c5b316a8c94 |
| rafaelmeloreisnovo/ZIPRAF_CORE | integridade_e_custodia | README_HASHED | e38b774ad6e3 | aca336e61266 |
| rafaelmeloreisnovo/ZIPRAF_OMEGA_FULL | integridade_e_custodia | README_HASHED | 088a5fa5f363 | 49387c503153 |

## Fontes documentais de domínio

Os documentos abaixo são preservados como material autoral/declarativo. As fórmulas e interpretações não são promovidas a fato científico por esta indexação.

| Documento | Título | SHA-256 | BLAKE3-256 |
|---|---|---|---|
| project_sources/02-04_BIOLOGIA_BIOENGENHARIA.md | 04 — Biologia & Bioengenharia | 9cad40b2703e | 3d0cdf76352c |
| project_sources/03-01_MATEMATICA_GEOMETRIA_SAGRADA.md | 01 — Matemática & Geometria Sagrada | 61318e9c4cd9 | e8a6f3953895 |
| project_sources/06-07_IA_COMPUTACAO.md | 07 — Inteligência Artificial & Computação | 558fbe73ceb8 | da882d5e147e |
| project_sources/07-03_FISICA_QUANTICA_TOPOLOGIA.md | 03 — Física Quântica & Topologia | a23673327ea0 | b2830726fadf |
| project_sources/08-08_MATEMATICA_SIMBOLICA.md | 08 — Matemática Simbólica & Sistemas de Numeração | 48d828943918 | 7afff27c8eb2 |
| project_sources/09-06_CONSCIENCIA_ESPIRITUALIDADE.md | 06 — Consciência & Espiritualidade Científica | 31a28d6d46a2 | cbc85a1098e3 |
| project_sources/10-05_ENGENHARIA_ELETROMAGNETISMO.md | 05 — Engenharia & Eletromagnetismo | 784341dcfa8c | 1d8502572841 |
| project_sources/11-10_GEOMETRIA_CAMPOS_ATRATORES.md | 10 — Geometria de Campos & Atratores | 8b7b5c20ed51 | 8c24ca13fc22 |
| project_sources/12-09_TERMODINAMICA_SISTEMAS.md | 09 — Termodinâmica & Teoria de Sistemas | 7c41ff675c1a | 432317505b10 |

## TOKEN_VAZIO

Uma lacuna não é preenchida por inferência. Cada item abaixo conserva o próximo passo verificável: buscar o arquivo/HEAD ausente ou repetir a coleta no commit indicado.

| Escopo | Referência | Estado |
|---|---|---|
| repository_readme | instituto-Rafael/LGPD-Constituicoes-planetaria-paises-onu-direitos-humanos-e-fundamentais-de-cada-continents-geologic | TOKEN_VAZIO:README_empty |
| repository_readme | instituto-Rafael/relativity-living-light | TOKEN_VAZIO:README_not_collected_in_primary_inventory |
| repository_readme | rafaelmeloreisnovo/android_frameworks_base_rafaelia | TOKEN_VAZIO:README_empty |
| repository_readme | rafaelmeloreisnovo/androidRom | TOKEN_VAZIO:README_empty |
| repository_readme | rafaelmeloreisnovo/fcea-originum | TOKEN_VAZIO:README_empty |
| repository_readme | rafaelmeloreisnovo/linuxkernel | TOKEN_VAZIO:README_empty |
| repository_readme | rafaelmeloreisnovo/LuaJIT | TOKEN_VAZIO:README_empty |
| repository | rafaelmeloreisnovo/new | TOKEN_VAZIO:no_head_returned |
| repository_readme | rafaelmeloreisnovo/new | TOKEN_VAZIO:no_head_commit |
| repository_readme | rafaelmeloreisnovo/PCR_Rafaelia_Code_seed | TOKEN_VAZIO:README_empty |
| repository_readme | rafaelmeloreisnovo/qemu_rafaelia | TOKEN_VAZIO:README_empty |
| repository | rafaelmeloreisnovo/rafaelia_privado | TOKEN_VAZIO:no_head_returned |
| repository_readme | rafaelmeloreisnovo/rafaelia_privado | TOKEN_VAZIO:no_head_commit |
| repository_readme | rafaelmeloreisnovo/V79-1 | TOKEN_VAZIO:README_empty |
| core_file | rafaelmeloreisnovo/BLAKE3:rmr/scan.c | TOKEN_VAZIO:core_file_empty |
| core_file | rafaelmeloreisnovo/BLAKE3:rmr/PAE.py | TOKEN_VAZIO:core_file_empty |
| local_core_file | audit_work/snapshots/15-RAFBROWSER_Enterprise_v1.0/RAFBROWSER_Enterprise/src/tls13.c | TOKEN_VAZIO:local_core_path_not_found |
| local_core_file | RAFAELIA_SESSAO_CONSOLIDADA_2026-07-25.md | TOKEN_VAZIO:local_core_path_not_found |
| local_core_file | RAFAELIA_SESSAO_CONSOLIDADA_2026-07-25.index.json | TOKEN_VAZIO:local_core_path_not_found |

## Reprodução

Para cada arquivo de um manifesto, compare os três digests: `md5sum ARQUIVO`, `sha256sum ARQUIVO` e um `b3sum` BLAKE3-compatível. Os manifests JSONL preservam valores completos; esta tabela mostra apenas prefixos para leitura humana.

Os manifests detalhados estão em `manifests/`. A lista de commits está em `RAFAELIA_REPOSITORY_HEADS_2026-07-25.json`.
