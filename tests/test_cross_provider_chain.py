#!/usr/bin/env python3
import importlib.util, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT/"tools/validate_cross_provider_chain.py"
MANIFEST = ROOT/"data/governance/cross-provider-chain-c70.v1.json"
spec = importlib.util.spec_from_file_location("v", TOOL)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def clone(x): return json.loads(json.dumps(x))
def check(name, doc, ok):
    errors = m.validate(doc)
    assert (not errors) == ok, (name, errors)
    print("PASS", name)

def main():
    base = json.loads(MANIFEST.read_text(encoding="utf-8"))
    check("valid", base, True)
    x=clone(base); x["claim_allowed"]=True; check("claim", x, False)
    x=clone(base); x["nodes"]=[n for n in x["nodes"] if n["provider"]!="GOOGLE_DRIVE"]; check("single-provider", x, False)
    x=clone(base); x["nodes"][0]["hash"]["value"]="a"; check("short-sha1", x, False)
    x=clone(base); x["nodes"][3]["hash"]["value"]="ab"; check("short-sha256", x, False)
    x=clone(base); x["nodes"][0]["hash"]["algorithm"]="MADE_UP"; check("unknown-hash", x, False)
    x=clone(base); x["nodes"][0]["parent_ids"]=["missing"]; check("missing-parent", x, False)
    x=clone(base); x["nodes"][1]["id"]=x["nodes"][0]["id"]; check("duplicate-id", x, False)
    x=clone(base); x["nodes"][1]["parent_ids"]=[]; check("edge-parent", x, False)
    x=clone(base); x["edges"][0]={"from":"github-c70-workflow","to":"github-c70-commit","type":"CONTAINS"}; check("reversed-edge", x, False)
    x=clone(base); x["nodes"][0]["parent_ids"]=["github-c70-workflow"]; x["edges"].append({"from":"github-c70-workflow","to":"github-c70-commit","type":"CONTAINS"}); check("cycle", x, False)
    x=clone(base); x["nodes"][0]["observed_at"]="yesterday"; check("timestamp", x, False)
    x=clone(base); x["nodes"][1]["observed_at"]="2026-08-13T15:00:00Z"; check("causal-time", x, False)
    x=clone(base); x["nodes"][0]["provider_id"]=""; check("provider-id", x, False)
    x=clone(base); x["nodes"][0]["generator"]=""; check("generator", x, False)
    x=clone(base); x["edges"][0]["type"]="MADE_UP"; check("edge-type", x, False)
    x=clone(base); x["edges"][2]["type"]="CONTAINS"; check("contains-cross-provider", x, False)
    x=clone(base); x["edges"][0]["type"]="EVIDENCED_BY"; check("evidenced-same-provider", x, False)
    x=clone(base); x["edges"]=[e for e in x["edges"] if e["to"]!="drive-c70-receipt"]; x["nodes"][3]["parent_ids"]=[]; check("disconnected-island", x, False)
    x=clone(base); x["edges"]=[e for e in x["edges"] if e["type"]!="EVIDENCED_BY"]; x["nodes"][3]["parent_ids"]=[]; check("no-cross-provider-transition", x, False)
    print("PASS 20/20")

if __name__ == "__main__":
    main()
