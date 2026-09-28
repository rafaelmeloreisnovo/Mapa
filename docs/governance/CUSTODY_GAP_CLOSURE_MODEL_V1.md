# RAFAELIA Custody Gap Closure Model V1

## Purpose

This model closes what can be closed by repository implementation and keeps
provider, credential, reviewer, and historical-evidence boundaries explicit.

The machine-readable source is
`data/governance/custody/06_GAPS/CUSTODY_GAP_CLOSURE_MODEL_V1.json`.

## Closure rule

A gap may move to `PASS` only when the authority named by that gap produces
the required evidence for the exact subject and source revision.

Local code never converts an external provider, secret, or independent-review
dependency into evidence.

## Current classes

- `MODEL_AUTHORITY`: repository model or ontology change.
- `CODE_DEFECT`: deterministic source defect fixable in the producer repo.
- `PROVIDER_CONFIGURATION`: GitHub or another provider setting.
- `SERVER_ENFORCEMENT`: server-observed merge or protection behavior.
- `SECRET_BOUND`: credential presence, validity, scope, or provider use.
- `HUMAN_REVIEW`: genuine independent review or explicit policy change.
- `HISTORICAL_EVIDENCE`: execution that was not observed at the historical
  revision and must not be retroactively invented.

## Current custody delta

The repository successor closes two internal gaps subject to exact-head CI:

1. a canonical non-secret `CREDENTIAL_PERMISSION_CUSTODY` profile for
   `C09_CREDENTIAL_AUTHORITY`;
2. the Markdown MD012 regression observed on PR 684.

Four external gaps remain fail-closed until their own authorities act:
provider ruleset activation, server-side enforcement, CodeScan credential
configuration, and genuine independent review.

The missing post-merge execution on the historical PR 684 merge commit remains
`NOT_RUN`; successor CI is evidence for the successor only.

## Invariants

`SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM`

`TOKEN_VAZIO != 0`

`IMPLEMENTED_UNTESTED != PASS`

`LOCAL_FIX != EXTERNAL_PROVIDER_EVIDENCE`

`SECRET_NAME != SECRET_VALUE != VALID_SCOPE != SUCCESSFUL_USE`
