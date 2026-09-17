# OECG V1 implementation map

| Responsibility | Artifact | Authority |
| --- | --- | --- |
| Human/child/privacy/truth/authority first-line policy | `docs/governance/OPERATIONAL_EXCELLENCE_CONTROL_PLANE_V1.md` | Mapa control plane |
| Machine-readable policy | `data/contracts/operational-excellence-gate.v1.json` | Mapa control plane |
| Gate validation | `scripts/governance/validate_operational_excellence_gate.py` | Mapa validator |
| Positive/negative controls | `tests/fixtures/operational-excellence.*.json` | Mapa test evidence |
| Semantic authority separation | `schemas/mu-semantic-event.v2.schema.json` | Mapa semantic schema |
| Deterministic event check | `scripts/governance/check_semantic_event_v2.py` | Mapa validator |
| Event fixture | `tests/fixtures/mu-semantic-event.v2.valid.json` | Mapa test evidence |
| Unit/CLI tests | `tests/governance/test_*` | Mapa test evidence |
| Risk/metrics/scope | `docs/governance/OECG_V1_*` | Mapa governance |
| Draft custody receipt | `data/receipts/operational-excellence/RECEIPT_OECG_V1_20260917.json` | Mapa receipt |
| Implementation/runtime evidence outside Mapa | producer repository receipts | producer repo |
| Documentary longitudinal pointer | Drive START HERE/book-memory | Drive |

No producer implementation is copied into Mapa by this control plane.
