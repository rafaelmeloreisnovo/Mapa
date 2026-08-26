> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ (ONU UDHR Art.1 · UNCRC Art.3)

# Matriz de Conformidade — norma × evidência × gap

Gerado por `codigo/matriz_conformidade.py`. Liga cada conceito evidenciado à sua **âncora normativa** (`REFERENCE`, de `biblioteconomia/08_ANCORAGEM_NORMATIVA.md`) e abre uma linha de auditoria. **Estado global: `PENDENTE`** — nada aqui é atestado de conformidade; a passagem `PENDENTE`→`CONFORME` exige auditoria real. Repos com dados pessoais têm **prioridade ALTA**, mas o nome do repo não prova aplicabilidade.

Cânone jurídico de privacidade/GNSS/IA: `docs/legal/GLOBAL_DATA_PRIVACY_GNSS_AI_GOVERNANCE_V1.md`.
Atlas semântico: `data/normative-graph/GLOBAL_DATA_PRIVACY_GNSS_AI_SEMANTIC_ATLAS_V1.json`.

> `permissão_do_SO != base_jurídica`; `data_no_dispositivo != dado_no_modelo`; `TOKEN_VAZIO != falso`. Cada fluxo deve ser provado ponta a ponta.

| prioridade | repo | conceito | norma (REFERENCE) | evidência | auditoria |
|---|---|---|---|---|---|
| ALTA | conversations_chunks_private | dados | CF/88 privacidade+dados; Marco Civil; LGPD 13.709/2018; GDPR 2016/679 quando aplicavel; ISO/IEC 27701 como REFERENCE | corpus de conversas (dados pessoais) | PENDENTE |
| ALTA | conversations_chunks_private | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| ALTA | conversations_chunks_private | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| ALTA | conversations_chunks_private | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| ALTA | conversations_chunks_private | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| ALTA | conversations_chunks_private | C11 | UNESCO Etica da IA 2021 (enquadramento) | codigo | PENDENTE |
| ALTA | conversations_chunks_private | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo+prosa | PENDENTE |
| ALTA | gaia_phi | dados | CF/88 privacidade+dados; Marco Civil; LGPD 13.709/2018; GDPR 2016/679 quando aplicavel; ISO/IEC 27701 como REFERENCE | indexacao/dataset | PENDENTE |
| ALTA | gaia_phi | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| ALTA | gaia_phi | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| ALTA | gaia_phi | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| ALTA | gaia_phi | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| ALTA | gaia_phi | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo+prosa | PENDENTE |
| ALTA | home | dados | CF/88 privacidade+dados; Marco Civil; LGPD 13.709/2018; GDPR 2016/679 quando aplicavel; ISO/IEC 27701 como REFERENCE | analise de codigo/dados do usuario | PENDENTE |
| ALTA | home | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| ALTA | home | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| ALTA | home | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| ALTA | home | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| ALTA | home | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo | PENDENTE |
| ALTA | lgpd_constituicoes | dados | CF/88 privacidade+dados; Marco Civil; LGPD 13.709/2018; GDPR 2016/679 quando aplicavel; ISO/IEC 27701 como REFERENCE | framework LGPD/direitos (proprio dominio) | PENDENTE |
| ALTA | lgpd_constituicoes | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| ALTA | lgpd_constituicoes | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| ALTA | lgpd_constituicoes | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| ALTA | lgpd_constituicoes | C11 | UNESCO Etica da IA 2021 (enquadramento) | prosa | PENDENTE |
| ALTA | lgpd_constituicoes | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | prosa | PENDENTE |
| ALTA | termux-api_rafcodephi | dados | CF/88 privacidade+dados; Marco Civil; LGPD 13.709/2018; GDPR 2016/679 quando aplicavel; ISO/IEC 27701 como REFERENCE | ponte Android com APIs de localizacao, contatos, call log, SMS, microfone, telefonia e outros dados conforme metodo/permissao | PENDENTE |
| ALTA | termux-api_rafcodephi | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| ALTA | termux-api_rafcodephi | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| ALTA | termux-api_rafcodephi | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| ALTA | termux-api_rafcodephi | C11 | UNESCO Etica da IA 2021 (enquadramento) | codigo | PENDENTE |
| ALTA | x0 | dados | CF/88 privacidade+dados; Marco Civil; LGPD 13.709/2018; GDPR 2016/679 quando aplicavel; ISO/IEC 27701 como REFERENCE | ecossistema cognitivo com dados | PENDENTE |
| ALTA | x0 | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| ALTA | x0 | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| ALTA | x0 | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| ALTA | x0 | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| ALTA | x0 | C11 | UNESCO Etica da IA 2021 (enquadramento) | codigo+prosa | PENDENTE |
| ALTA | x0 | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo+prosa | PENDENTE |
| normal | actions | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| normal | actions | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | actions | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo | PENDENTE |
| normal | actions | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | blackhole | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | prosa | PENDENTE |
| normal | blackhole | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | prosa | PENDENTE |
| normal | blackhole | C05 | IETF RFC 8032 (assinatura Ed25519) | prosa | PENDENTE |
| normal | blackhole | C11 | UNESCO Etica da IA 2021 (enquadramento) | prosa | PENDENTE |
| normal | blake3 | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| normal | blake3 | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | blake3 | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| normal | blake3 | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | blake3 | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | prosa | PENDENTE |
| normal | chipquantum | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| normal | chipquantum | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | chipquantum | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| normal | chipquantum | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | chipquantum | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo+prosa | PENDENTE |
| normal | deepseek-rafcoder | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| normal | deepseek-rafcoder | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | deepseek-rafcoder | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| normal | deepseek-rafcoder | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | deepseek-rafcoder | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | prosa | PENDENTE |
| normal | livrovivo_thisbooklives | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | prosa | PENDENTE |
| normal | livrovivo_thisbooklives | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | livrovivo_thisbooklives | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| normal | livrovivo_thisbooklives | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | livrovivo_thisbooklives | C11 | UNESCO Etica da IA 2021 (enquadramento) | codigo+prosa | PENDENTE |
| normal | livrovivo_thisbooklives | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | prosa | PENDENTE |
| normal | llamarafaelia | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| normal | llamarafaelia | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | llamarafaelia | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| normal | llamarafaelia | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | llamarafaelia | C11 | UNESCO Etica da IA 2021 (enquadramento) | prosa | PENDENTE |
| normal | llamarafaelia | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo+prosa | PENDENTE |
| normal | mapa | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| normal | mapa | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | mapa | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| normal | mapa | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | mapa | C11 | UNESCO Etica da IA 2021 (enquadramento) | codigo+prosa | PENDENTE |
| normal | mapa | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo+prosa | PENDENTE |
| normal | matem-tica- | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | prosa | PENDENTE |
| normal | matem-tica- | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | matem-tica- | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | prosa | PENDENTE |
| normal | matem-tica- | C05 | IETF RFC 8032 (assinatura Ed25519) | prosa | PENDENTE |
| normal | matem-tica- | C11 | UNESCO Etica da IA 2021 (enquadramento) | prosa | PENDENTE |
| normal | matem-tica- | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo+prosa | PENDENTE |
| normal | memrafcode | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | prosa | PENDENTE |
| normal | memrafcode | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | prosa | PENDENTE |
| normal | memrafcode | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | prosa | PENDENTE |
| normal | papers | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo | PENDENTE |
| normal | papers | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | papers | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| normal | papers | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | papers | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | prosa | PENDENTE |
| normal | pcr_rafaelia_code_seed | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| normal | pcr_rafaelia_code_seed | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | pcr_rafaelia_code_seed | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| normal | pcr_rafaelia_code_seed | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | pcr_rafaelia_code_seed | C11 | UNESCO Etica da IA 2021 (enquadramento) | codigo+prosa | PENDENTE |
| normal | pcr_rafaelia_code_seed | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo+prosa | PENDENTE |
| normal | publicacientiespiritual | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | prosa | PENDENTE |
| normal | publicacientiespiritual | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | publicacientiespiritual | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| normal | publicacientiespiritual | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | publicacientiespiritual | C11 | UNESCO Etica da IA 2021 (enquadramento) | codigo+prosa | PENDENTE |
| normal | publicacientiespiritual | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo+prosa | PENDENTE |
| normal | qemu_rafaelia | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| normal | qemu_rafaelia | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | qemu_rafaelia | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| normal | qemu_rafaelia | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | qemu_rafaelia | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo+prosa | PENDENTE |
| normal | rafaelia_private | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| normal | rafaelia_private | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | rafaelia_private | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| normal | rafaelia_private | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | rafaelia_private | C11 | UNESCO Etica da IA 2021 (enquadramento) | codigo+prosa | PENDENTE |
| normal | rafaelia_private | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo+prosa | PENDENTE |
| normal | rafgittools | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| normal | rafgittools | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | rafgittools | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| normal | rafgittools | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | rafgittools | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo+prosa | PENDENTE |
| normal | rafpolimata | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| normal | rafpolimata | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | rafpolimata | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| normal | rafpolimata | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | rafpolimata | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo+prosa | PENDENTE |
| normal | relativity-living-light | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| normal | relativity-living-light | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | relativity-living-light | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| normal | relativity-living-light | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | relativity-living-light | C11 | UNESCO Etica da IA 2021 (enquadramento) | codigo+prosa | PENDENTE |
| normal | relativity-living-light | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo+prosa | PENDENTE |
| normal | termux-app-rafacodephi | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| normal | termux-app-rafacodephi | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | termux-app-rafacodephi | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| normal | termux-app-rafacodephi | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | termux-app-rafacodephi | C11 | UNESCO Etica da IA 2021 (enquadramento) | codigo | PENDENTE |
| normal | termux-app-rafacodephi | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo+prosa | PENDENTE |
| normal | userland | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| normal | userland | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | userland | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| normal | userland | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | userland | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo+prosa | PENDENTE |
| normal | vectras-vm-android | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| normal | vectras-vm-android | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | vectras-vm-android | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| normal | vectras-vm-android | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | vectras-vm-android | C11 | UNESCO Etica da IA 2021 (enquadramento) | codigo | PENDENTE |
| normal | vectras-vm-android | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo+prosa | PENDENTE |
| normal | zipraf_omega_full | C01 | SLSA; ISO/IEC/IEEE 12207 (reprodutibilidade) | codigo+prosa | PENDENTE |
| normal | zipraf_omega_full | C03 | NIST FIPS 180-4 / FIPS 202 (hashing) | codigo+prosa | PENDENTE |
| normal | zipraf_omega_full | C04 | W3C PROV-O; ISO 15489 (proveniencia/custodia) | codigo+prosa | PENDENTE |
| normal | zipraf_omega_full | C05 | IETF RFC 8032 (assinatura Ed25519) | codigo+prosa | PENDENTE |
| normal | zipraf_omega_full | C11 | UNESCO Etica da IA 2021 (enquadramento) | prosa | PENDENTE |
| normal | zipraf_omega_full | C13 | ISO/IEC 42001; UNESCO Etica IA; UDHR; UNCRC (etica/direitos) | codigo+prosa | PENDENTE |

> Honestidade: `REFERENCE` = alvo/orientação, não conformidade demonstrada. Evidência do conceito ≠ prova de que a norma é cumprida. Cada linha é uma tarefa de auditoria, não um selo.
