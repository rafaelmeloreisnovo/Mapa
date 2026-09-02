# RAFAELIA Federated Mirror & Custody Plane V1

State: `CANONICAL_DRAFT / FAIL_CLOSED / APPEND_ONLY / PRIVATE_BY_DEFAULT`

This directory defines the control plane for repository inventory, synchronization/mirroring eligibility, evidence, receipts, readback, reviews, risk, ancestry and artifact custody. It does **not** enable mirroring by itself.

Core chain:

`SOURCE -> TRANSFORM -> CLAIM -> TEST/EVIDENCE -> REVIEW -> RECEIPT -> INDEX -> MEMORY -> READBACK`

Core separation:

`VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM`

Synchronization states:

`DISCOVERED | REGISTERED | ELIGIBLE | MIRROR_CANDIDATE | SYNC_PLANNED | EXECUTED | VERIFIED | DIVERGED | BLOCKED | TOKEN_VAZIO`

No mirror may overwrite an authoritative repository. Every write must be bounded, reversible, provider-authorized and evidence-linked.

## Directory map

- `repositories.v1.yaml` — repository registry and authority/mirror intent.
- `contracts/sync_mirror_policy.v1.yaml` — synchronization, ancestry, conflict and rollback rules.
- `contracts/evidence_receipt.v1.yaml` — receipt/evidence/readback contract.
- `contracts/integrity_custody.v1.yaml` — SHA-256/BLAKE3, legacy MD5 handling, ZIP/layer custody, parity/ECC metadata.
- `contracts/risk_review.v1.yaml` — risks, reviews, privacy, human-impact and provider authority gates.
- `schemas/event.v1.json` — normalized event/syslog-style envelope.

## Non-negotiable invariants

1. `mirror != authority`.
2. `same_name != same_tree != same_bytes`.
3. `hash_match != authorization`.
4. `MD5` is legacy-correlational only; never a security-integrity authority.
5. SHA-256 is the minimum portable custody digest; BLAKE3 may be recorded in parallel.
6. Raw-byte custody precedes artifact-integrity claims.
7. Ancestry is proven by provider graph/tree evidence, never inferred from timestamps alone.
8. Reviews, threads, approvals and dissent are first-class evidence objects.
9. `TOKEN_VAZIO` is valid and blocks promotion when a mandatory fact is absent.
10. Child-safety, privacy, dignity and cultural/community safeguards inherit the repository governance canon.
