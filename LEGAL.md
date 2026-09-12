# RAFAELIA Legal and Licensing Router

Status: DRAFT_FOR_LEGAL_REVIEW

This file is the navigation entry point for licensing, attribution, contributor rights, third-party notices, and commercial permissions.

## Current root-license fact

The repository root `LICENSE` remains GNU GPL v3.

Nothing in this legal package removes commercial or other rights already granted by GPLv3, MIT, or any third-party license.

## Legal package

1. [Licensing Policy](docs/legal/RAFAELIA_LICENSING_POLICY_V1.md)
2. [RAFAELIA Research and Non-Commercial License](LICENSES/LicenseRef-RAFAELIA-RNC-1.0.txt)
3. [Attribution and Citation Standard](docs/legal/ATTRIBUTION_AND_CITATION_STANDARD_V1.md)
4. [Commercial License Template](docs/legal/COMMERCIAL_LICENSE_TEMPLATE_V1.md)
5. [Audit and Enforcement Protocol](docs/legal/AUDIT_AND_ENFORCEMENT_PROTOCOL_V1.md)
6. [Brazilian Legal Basis](docs/legal/LEGAL_BASIS_BR_V1.md)
7. [License Compatibility Matrix](docs/legal/LICENSE_COMPATIBILITY_MATRIX_V1.md)
8. [Third-Party Notices Policy](docs/legal/THIRD_PARTY_NOTICES_POLICY_V1.md)
9. [Contributor License Agreement Template](docs/legal/CONTRIBUTOR_LICENSE_AGREEMENT_TEMPLATE_V1.md)
10. [Machine-readable legal references](data/legal/licensing_references.v1.json)
11. [Machine-readable license scope registry](data/legal/license-scope-registry.v1.jsonl)
12. [License scope schema](schemas/license-scope-record.v1.schema.json)
13. [License scope validator](tools/validate_license_scope_registry.py)
14. [License scope tests](tests/test_license_scope_registry.py)
15. [Implementation Receipt](receipts/2026-09-12_RAFAELIA_LICENSING_FRAMEWORK_V1.md)

## Scope rule

```text
ROOT_GPL -> continues to govern GPL-covered work
FILE_SPECIFIC_LICENSE -> governs only the file/material to which it validly applies
THIRD_PARTY_LICENSE -> cannot be displaced by RAFAELIA notice
COMMERCIAL_RAFAELIA_RIGHTS -> require separate written instrument where the custom RNC license applies
```

## Commercial-use rule

The custom non-commercial license is not automatically applied to this whole repository.

Only material explicitly marked `LicenseRef-RAFAELIA-RNC-1.0` after a rights/compatibility audit may use that license.

Commercial use of such eligible material requires a separate written commercial license.

## Attribution rule

Where the custom license validly applies, attribution must preserve:

- Rafael Melo Reis as author where factually correct;
- artifact/work title;
- canonical source;
- version/revision;
- license;
- modification statement;
- bibliographic citation;
- canonical biography reference when supplied;
- upstream/third-party notices separately.

## Validation

```bash
python3 tools/validate_license_scope_registry.py
python3 -m unittest tests.test_license_scope_registry
```

PASS validates the registry structure and explicit compatibility guards only. It is not a legal opinion.

## Legal review

Before execution with a real counterparty, licensed counsel should review:

- party identity;
- governing law/forum;
- currency/payment;
- consumer/adhesion issues;
- tax;
- contributor rights;
- audit scope;
- liability/indemnity;
- privacy/data protection;
- patent/trademark;
- applicable third-party licenses.
