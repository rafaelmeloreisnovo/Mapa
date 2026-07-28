#!/usr/bin/env python3
"""Deterministic, stdlib-only router for domain-specific review."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

SHA256 = re.compile(r"^[a-f0-9]{64}$")
DOMAINS = {"COMPUTATIONAL","SCIENTIFIC","LEGAL","ETHICAL"}

class RoutingError(ValueError): pass

def require(ok, msg):
    if not ok:
        raise RoutingError(msg)

def canonical_json_sha256(payload):
    raw=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def validate_vector_minimal(vector):
    require(vector.get("schema")=="rafaelia.longitudinal-vector-evolution/v1", "invalid vector schema")
    require(vector.get("claim_allowed") is False, "vector claim_allowed must remain false")
    require(vector.get("state") in {"EVOLVED_LOCAL","BLOCKED","TOKEN_VAZIO_VECTOR_DELTA"}, "invalid vector state")
    require(vector.get("source",{}).get("hidden_model_access") is False, "hidden model access is forbidden")
    return True

def route(envelope, registry, root):
    require(envelope.get("schema")=="rafaelia.domain-routing-envelope/v1", "invalid envelope schema")
    require(registry.get("schema")=="rafaelia.domain-authority-registry/v1", "invalid registry schema")
    require(envelope.get("claim_allowed") is False, "envelope claim_allowed must remain false")
    require(envelope.get("cross_domain_promotion_allowed") is False, "cross-domain promotion must remain false")
    require(envelope.get("semantic_domain_inference_allowed") is False, "semantic domain inference must remain false")
    require(registry.get("claim_allowed") is False and registry.get("epistemic_promotion_allowed") is False, "registry promotions must remain false")

    vref=envelope.get("vector",{})
    rel=vref.get("path")
    require(isinstance(rel,str) and rel and not Path(rel).is_absolute(), "vector path must be relative")
    vector_path=(root/rel).resolve()
    require(str(vector_path).startswith(str(root.resolve())), "vector path escapes root")
    require(vector_path.is_file(), "vector file not found")
    expected=vref.get("canonical_sha256")
    require(isinstance(expected,str) and SHA256.fullmatch(expected), "vector canonical_sha256 required")
    vector=load_json(vector_path)
    observed=canonical_json_sha256(vector)
    require(observed==expected, "vector canonical hash mismatch")
    validate_vector_minimal(vector)
    require(vector.get("vector_id")==vref.get("vector_id"), "vector_id mismatch")
    require(vector.get("revision")==vref.get("revision"), "vector revision mismatch")

    domains=registry.get("domains",{})
    require(set(domains)==DOMAINS, "registry must define exactly four authorities")
    claims=envelope.get("claims")
    require(isinstance(claims,list) and claims, "claims required")
    seen=set(); routed=[]; grouped={}
    for claim in claims:
        cid=claim.get("claim_id")
        require(isinstance(cid,str) and cid and cid not in seen, "claim_id must be unique")
        seen.add(cid)
        require(claim.get("claim_allowed") is False, f"{cid}: claim_allowed must remain false")
        domain=claim.get("declared_domain")
        require(isinstance(domain,str), f"{cid}: one explicit domain is required")
        require(domain in domains, f"{cid}: unknown domain")
        policy=domains[domain]
        ctype=claim.get("claim_type")
        require(ctype in policy.get("allowed_claim_types",[]), f"{cid}: claim type/domain mismatch")
        state=claim.get("input_state")
        require(state in policy.get("allowed_input_states",[]), f"{cid}: input state not accepted by domain")
        refs=claim.get("source_refs")
        require(isinstance(refs,list) and refs and all(isinstance(x,str) and x for x in refs), f"{cid}: source refs required")
        require(claim.get("requested_transition")=="READY_FOR_DOMAIN_SPECIFIC_REVIEW", f"{cid}: forbidden transition")
        item={
          "claim_id":cid, "declared_domain":domain, "gate_id":policy["gate_id"],
          "routing_state":"ROUTED_FOR_DOMAIN_REVIEW",
          "resulting_epistemic_state":"READY_FOR_DOMAIN_SPECIFIC_REVIEW",
          "forbidden_promotions":policy["forbidden_promotions"],
          "claim_allowed":False, "epistemic_promotion_allowed":False
        }
        routed.append(item); grouped.setdefault(policy["gate_id"],[]).append(cid)
    return {
      "schema":"rafaelia.domain-routing-receipt/v1",
      "state":"PASS",
      "routing_id":envelope.get("routing_id"),
      "vector_id":vector["vector_id"],
      "vector_canonical_sha256":observed,
      "route_count":len(routed),
      "routes":routed,
      "gate_batches":grouped,
      "cross_domain_promotion_allowed":False,
      "semantic_domain_inference_used":False,
      "claim_allowed":False,
      "epistemic_promotion_allowed":False,
      "next_gate":"Execute each gate independently; never reuse one domain result as another domain authority."
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("envelope",type=Path)
    ap.add_argument("--registry",type=Path,default=Path("config/domain-authority-registry.v1.json"))
    ap.add_argument("--root",type=Path,default=Path("."))
    ap.add_argument("--receipt",type=Path)
    a=ap.parse_args()
    try:
        result=route(load_json(a.envelope),load_json(a.registry),a.root.resolve())
    except (OSError,json.JSONDecodeError,RoutingError) as e:
        print(json.dumps({"state":"FAIL","error":str(e)},ensure_ascii=False,indent=2)); return 1
    text=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if a.receipt:
        a.receipt.parent.mkdir(parents=True,exist_ok=True)
        a.receipt.write_text(text,encoding="utf-8")
    print(text,end=""); return 0
if __name__=="__main__":
    raise SystemExit(main())
