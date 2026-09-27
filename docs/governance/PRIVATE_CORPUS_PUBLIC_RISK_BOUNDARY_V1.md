# Mapa — Private Corpus → Public Risk Boundary V1

Status: CANDIDATE / PUBLIC CONTROL PLANE / FAIL-CLOSED  
Date: 2026-09-26

## Purpose

Allow the public Mapa control plane to show that a private corpus/intake risk exists and is being
reviewed without disclosing the corpus or enough metadata to reconstruct or correlate it.

## Allowed public fields

- opaque `risk_handle`;
- risk classes;
- mitigation state;
- evidence state;
- opaque private evidence reference;
- optional short sanitized summary;
- explicit false privacy-leak flags;
- `claim_allowed=false`.

## Forbidden public fields

- raw JSON or excerpts;
- conversation text;
- source file name or path;
- raw SHA-256/BLAKE3 of private corpus;
- Google Drive IDs/URLs;
- private repository paths that reveal the corpus;
- embeddings or vector payloads;
- personal identifiers, credentials or secrets;
- provider capability URIs.

## Why raw hashes are forbidden

A raw digest of private material can act as a membership oracle for anyone holding a candidate copy.
The public plane therefore uses an opaque risk handle. The private custody plane retains the mapping
and raw digest.

## Workflow

```text
private intake
→ private risk review
→ sanitization gate
→ public-risk schema validation
→ Mapa risk status
```

No public record proves the private content itself; it proves only that the governance/risk state was
projected under the declared private evidence boundary.

## Invariants

`PRIVATE_CORPUS != PUBLIC_CONTROL_PLANE`

`PRIVATE_DIGEST != PUBLIC_HANDLE`

`RISK_MARKER != CLAIM_OF_HARM`

`PRIVATE_EVIDENCE_POINTER != PRIVATE_PROVIDER_ID`

## F_next

- validate one synthetic golden projection;
- bind one real private intake only through an opaque `PRIVREF`;
- add current HEAD/contract versions to the federated matrix;
- preserve all unresolved provider/physical/reproduction states as typed TOKEN_VAZIO.
