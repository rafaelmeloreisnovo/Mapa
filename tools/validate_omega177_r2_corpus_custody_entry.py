#!/usr/bin/env python3
import json, sys

def fail(msg):
    print("FAIL:", msg)
    raise SystemExit(1)

contract_path = sys.argv[1] if len(sys.argv) > 1 else "contracts/omega177/omega177_r2_corpus_custody_entry_v1.json"
d = json.load(open(contract_path, encoding="utf-8"))

if d.get("schema") != "rafaelia.omega177.r2-corpus-custody-entry/v1": fail("schema")
if d.get("claim_allowed") is not False: fail("claim_allowed must be false")
if d.get("promotion_rule") != "bytes observed before cryptographic root": fail("promotion rule")
if d.get("root_state") != "TOKEN_VAZIO_UNTIL_SCOPE_COMPLETE": fail("root must remain TOKEN_VAZIO until scope complete")
if d["population"]["input_scope_complete"] is not False: fail("entry contract must not claim complete scope")
if d["hash_policy"]["global_root"] != "forbidden_until_input_scope_complete_true": fail("global-root gate")
if d["dedup_policy"]["destructive_delete"] is not False: fail("dedup must be non-destructive")
if d["dedup_policy"]["canonicality_not_implied_by_digest_equality"] is not True: fail("digest equality must not imply canonicality")
if d["snapshot_policy"]["recency_alone_sufficient"] is not False: fail("recency alone cannot establish canonicality")
if d["sanitization_policy"]["template_reference_requires"] != "PASS_SANITIZED": fail("template reference sanitization gate")
if d["template_package"]["raw_runtime_code_is_source_only"] is not True: fail("runtime code/source boundary")
focus=set(d["initial_focus"])
need={"X0_HOME_DRIVE_GLOBAL_DEDUP","MULTI_SNAPSHOT_CANONICALITY","FORMAL_SANITIZATION","TEMPLATE_CREATOR_PACKAGE"}
if focus != need: fail("initial focus mismatch")
required=set(d["required_object_fields"])
for x in ("observed_bytes","sha256","blake3","canonical_authority","canonical_reason","sanitization_state"):
    if x not in required: fail("missing required field: "+x)
print("PASS: Ω177 R2 corpus/custody entry contract valid; global root blocked; claim_allowed=false")
