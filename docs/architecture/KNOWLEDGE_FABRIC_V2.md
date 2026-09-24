# Knowledge Fabric V2 — falsifiable contract

Status: implementation candidate on a feature branch; CI and merge are pending. V1 remains unchanged. This contract is a typed successor for a bounded library workflow, not a declaration that the full corpus is ingested or that any domain claim is true.

## Primitive boundaries

The bundle keeps distinct collections for:

- **Object** — stable catalog identity plus exact source surface, provider ID, ref, access class, and semantic state.
- **Relation** — directed typed edge with scope, source reference, evidence effect, promotion ceiling, guard, and supersession pointer.
- **Event** — observed transition or snapshot for mutable external records such as pull requests.
- **Context** — assembled retrieval context remains a derived view and is not persisted as source evidence.
- **Authority** — explicit actor × target × operation decision for DISCOVER, READ, EXECUTE, WRITE, and PUBLISH. Missing grants deny.
- **Evidence** — scoped test, observation, measurement, or proof pointer.
- **Receipt** — append-only record that points to evidence and a parent; it is not evidence itself.
- **State** — time-stamped value attached to an object.
- **Delta** — append-only transition from a parent State to a distinct successor State.
- **Gap** — typed unresolved item with reason, status, and exact next probe.

TOKEN_VAZIO remains an explicit epistemic/access state. It does not coerce to 0, false, deletion, PASS, or an inferred value. The validator keeps claim_allowed=false.

## Gate behavior

The dependency-free Python validator rejects duplicate object IDs, missing source identity, out-of-graph relation endpoints, under-specified edge contracts, receipts that collide with evidence IDs or do not point to evidence, claims without evidence, private publication without an explicit allow grant, attempts to read unknown tokens, pull-request objects without time-stamped source events, non-append-only deltas, and gaps without a next probe.

The fixture contains bounded synthetic examples for formula, image, DAT, conversation, unresolved token, commit, PR, execution, private file, artifact, claim, event, evidence, receipt, authority, state, delta, and gap. It does not contain user corpus content.

## Run locally

~~~sh
python3 -m py_compile scripts/validate_knowledge_fabric_v2.py tests/test_knowledge_fabric_v2.py
python3 -m json.tool schemas/knowledge-fabric-v2.schema.json >/dev/null
python3 -m unittest tests/test_knowledge_fabric_v2.py -v
python3 scripts/validate_knowledge_fabric_v2.py tests/fixtures/knowledge_fabric_v2.valid.json --report build/knowledge-fabric-v2/receipt.json
~~~

GitHub Actions repeats those gates and uploads a report plus SHA-256 manifest. A workflow run is the remote CI evidence; a local PASS does not imply remote PASS.

## Boundary / next gates

- V1's inherited source counts, message-coverage gaps, and catalog state are untouched.
- The pilot validates contract shape and adversarial behavior only. It does not ingest corpus objects or enforce provider ACLs.
- Before reusing with real private sources, bind grant subjects to authenticated identities and test the enforcement point that controls the actual read/publish operation.
- Before promotion, run exact-head CI, review the schema, and record the resulting commit/workflow/receipt. Do not merge automatically.
