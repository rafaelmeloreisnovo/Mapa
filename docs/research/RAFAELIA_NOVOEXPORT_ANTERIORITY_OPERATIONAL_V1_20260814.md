# RAFAELIA — NOVOexport Anteriority Operational V1 — 2026-08-14

State: `APPEND_ONLY / EVIDENCE_FIRST / claim_allowed=false`

## Purpose

Move the existing concept-anteriority registry from a terminology-only chronology toward a reproducible evidence chain without retrodating names or promoting scientific/patent claims.

The governing lane is:

`FAMILY -> FIRST_MENTION -> FIRST_DEFINITION -> FIRST_FORMULA -> FIRST_FILE -> FIRST_COMMIT -> FIRST_RUN -> FIRST_PUBLIC_DISCLOSURE -> EXTERNAL_PRIOR_ART -> CLAIM_STATUS`

These states are intentionally independent.

## Source custody already present

The existing registry anchors the export archive and conversation source by SHA-256 and records first user-message occurrences for multiple RAFAELIA families. The NOVOexport inventory contains `chat.html`, `export_manifest.json`, and conversation shards named `conversations-000.json` through `conversations-050.json`.

No later alias is allowed to rewrite an earlier precursor. `ZRF != ZFR` unless a source explicitly proves equivalence; the same rule applies to all aliases.

## New implementation

### Extractor

`/scripts/extract_novoexport_anteriority_events_v1.py`

The extractor:

1. scans immutable `conversations-*.json` shards;
2. reads only messages with `author.role == user`;
3. fingerprints every scanned source shard with SHA-256;
4. fingerprints exact extracted user-message text with SHA-256;
5. preserves source path, conversation ID, message ID, timestamp and matched aliases;
6. emits append-only JSONL events;
7. emits an earliest-event summary per configured family;
8. leaves public disclosure, legal priority and scientific novelty as `TOKEN_VAZIO`;
9. hard-codes `claim_allowed=false` in generated evidence events.

No network or third-party Python dependency is required.

### Family query configuration

`/data/provenance/novoexport_anteriority_family_queries_20260814.v1.json`

Initial scoped families:

- RAFCODE / RAFBIT;
- BITRAF / BITRAF64;
- ZIPRAF;
- ZRF;
- ZFR;
- Fibonacci-Rafael;
- Voynich-Rafael / Voynich-Fibonacci;
- vetores fractais ocultos;
- paridades / ECC;
- Hyperforma 42/69/64;
- Tesseract / Hypercube applied layer;
- CLIMEX -> PLIMEX -> Plect;
- quantum-electron/electronics terminology.

The aliases are search keys only. Alias match does not establish semantic identity.

## Public GitHub anchor resolved

Repository: `instituto-Rafael/Eletron-efeitos-qu-ntico`

Observed public chronology:

- repository created: `2025-08-04T09:41:46Z`;
- `354181c09b599db52bf3c80157bcde2891d2bf2a` — `Initial commit` — `2025-08-04T09:41:59Z` — GitHub verified;
- `837f7b24c291ba95c4eb446f9ea9713e8e7a7f3a` — `Create TEORIA RAFAEL PROVADA` — `2025-08-04T09:43:30Z` — GitHub verified;
- `5c8ee7379214120a2211e00dcaf53b220bfec9dc` — `Create Quantum eletron` — `2025-08-04T11:27:11Z` — GitHub verified.

The `Create Quantum eletron` diff visibly contains RAFCODE-𝚽, Voynich, ZIPRAF, ZRF, NETRAF and quantum/electron symbolic-technical material. This supports `E5_PUBLIC_DISCLOSURE` for the material actually disclosed by those bytes. It does **not** prove worldwide novelty, physical validation, patentability or ownership of pre-existing scientific concepts.

## Brazil grace-period boundary

Official INPI guidance describes a 12-month grace period under Article 12 of the Brazilian Industrial Property Law for qualifying inventor-originated disclosure. As of 2026-08-14, more than 12 months have elapsed from the observed 2025-08-04 public GitHub disclosure.

This is only a risk flag. It is not a legal determination that every later RAFAELIA invention is unpatentable. Patent analysis must compare the exact claimed subject matter against what was sufficiently disclosed, who disclosed it, the filing history, and the applicable jurisdiction. Other jurisdictions may not recognize the same grace period.

State: `TOKEN_VAZIO_LEGAL_SCOPE` until matter-specific review.

## Evidence levels

- `E0 TOKEN_VAZIO`: no resolved source.
- `E1 INTERNAL_DOCUMENTED`: occurrence in the internal export.
- `E2 CONTENT_FINGERPRINTED`: source and message content linked to cryptographic fingerprints.
- `E3 IMPLEMENTED`: concrete artifact or code exists.
- `E4 EXECUTED_WITH_RECEIPT`: execution is observed and recorded.
- `E5 PUBLIC_DISCLOSURE`: publicly accessible dated disclosure is resolved.
- `E6 EXTERNAL_PRIOR_ART_REVIEWED_NON_EXHAUSTIVE`: external comparison exists but is not a patentability opinion.
- `E7 CLAIM_CANDIDATE`: may be evaluated only after the relevant lower gates are satisfied.

`E7` does not set `claim_allowed=true` automatically.

## Synthetic reference test

A logic-equivalent local reconstruction of the extractor was compiled and exercised against a synthetic single-shard fixture:

- `py_compile`: PASS;
- one user message with three matched families;
- expected events: 3;
- observed events: 3;
- missing family remained `TOKEN_VAZIO_IN_SCANNED_INPUT`;
- `claim_allowed=false` preserved.

Receipt:

`/data/evidence/novoexport_anteriority_extractor_synthetic_reference_20260814.v1.json`

Important boundary: the exact GitHub blob was inspected but was not the byte-identical file executed in that synthetic reference environment. Therefore the result is `PASS_LIMITED_SYNTHETIC_REFERENCE`, not full execution evidence.

## Existing registry evolution

The effective concept registry becomes:

`v1 + v1.1.delta + v1.2.delta + v1.3.delta`

New delta:

`/data/provenance/rafaelia_concept_anteriority_registry_20260813.v1.3.delta.json`

Historical registry bytes are not replaced.

## Anti-regression falsifiers

The pipeline is invalid if any of the following occurs:

1. assistant messages are treated as user authorship evidence;
2. a later name is retroactively assigned to an earlier precursor without an explicit source;
3. a Git timestamp is represented as a patent or proof of scientific novelty;
4. internal conversation chronology is represented as public disclosure;
5. a missing field is filled by inference instead of `TOKEN_VAZIO`;
6. a synthetic test is represented as execution on the real NOVOexport;
7. an externally established object such as XOR, Fibonacci, hypercube or Tesseract is claimed merely because RAFAELIA uses it;
8. `claim_allowed` is promoted without a separate evidence gate.

## Next exact execution gate

On an immutable NOVOexport snapshot:

```bash
python scripts/extract_novoexport_anteriority_events_v1.py /path/to/NOVOexport \
  --config data/provenance/novoexport_anteriority_family_queries_20260814.v1.json \
  --events out/novoexport_anteriority_events.v1.jsonl \
  --summary out/novoexport_anteriority_summary.v1.json
```

Then freeze:

1. extractor bytes and SHA-256;
2. query config bytes and SHA-256;
3. all source-shard SHA-256 values;
4. events JSONL SHA-256;
5. summary JSON SHA-256;
6. runtime environment;
7. exit code/stdout;
8. first event for every family;
9. negative/no-hit results;
10. subsequent cross-links to first definition, formula, file, commit, run and public disclosure.

## F_ok / F_gap / F_next

**F_ok:** an operational extractor, scoped query set, schema, v1.3 append-only delta, public GitHub disclosure anchor and limited synthetic receipt now exist.

**F_gap:** exact GitHub extractor bytes have not yet been executed against the immutable real NOVOexport snapshot; first definition/formula/file/run/public disclosure remains unresolved for most families; external patent prior art remains non-exhaustive.

**F_next:** execute the exact extractor on the real snapshot, freeze outputs, then perform matter-specific public-disclosure and prior-art joins without retrodating or claim promotion.
