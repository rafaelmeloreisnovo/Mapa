# Security Policy

## Purpose

This repository uses an evidence-first security process. This policy is a working
security and disclosure process; it is not a claim of certification, legal
compliance, or absence of vulnerabilities.

## Reporting a vulnerability

Do **not** open a public issue containing an exploitable vulnerability, secret,
credential, personal data, private evidence, or instructions that would materially
increase abuse risk.

Preferred reporting path:

1. Use GitHub private vulnerability reporting / a private Security Advisory when
   that capability is available for this repository.
2. If a private GitHub reporting path is unavailable, report the concern to
   `rafaelmeloreisnovo@gmail.com` with the minimum information needed to reproduce
   and assess the issue.

Please avoid sending real secrets or unnecessary personal data. Redact tokens,
credentials, identifiers, and unrelated user content whenever possible.

## Helpful report fields

- affected component, path, workflow, or commit;
- impact and plausible consequence;
- minimal reproduction or failing fixture;
- preconditions and scope;
- whether personal data or credentials may be involved;
- suggested mitigation, when known.

## Handling process

Reports are triaged by evidence and consequence, not by inactivity or label alone.
The initial acknowledgement target is 72 hours when feasible; this is an operational
target, not a contractual SLA.

A finding may remain open as `TOKEN_VAZIO`, `BLOCKED`, or another explicit unresolved
state until the closure criterion is evidenced. Silence or elapsed time is not proof
of remediation.

## Disclosure and evidence

Public disclosure should be coordinated after a fix or defensible mitigation exists,
unless law or an overriding safety obligation requires another path. Sensitive
evidence should remain in an access-controlled system of record; a public repository
may retain only a safe receipt, hash, identifier, or redacted summary when adequate.

Security references, audits, scanners, or standards mappings are `REFERENCE` or
process evidence only. They do not imply certification.

`REFERENCE != IMPLEMENTED != EVIDENCED != VERIFIED != CERTIFIED`
