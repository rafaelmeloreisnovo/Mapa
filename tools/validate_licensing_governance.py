#!/usr/bin/env python3
"""Fail-closed structural validator for RAFAELIA licensing governance V2.

This validates documentation invariants only. PASS is not legal advice,
license enforceability, rights ownership, or counsel approval.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"governance/licensing"
REQUIRED=[
 "README.md",
 "RAFAELIA_ORIGINAL_WORKS_NC_ATTRIBUTION_LICENSE_V1_PTBR.md",
 "ATTRIBUTION_AND_CITATION_STANDARD_V1.md",
 "COMMERCIAL_LICENSE_FRAMEWORK_V1.md",
 "THIRD_PARTY_LICENSE_BOUNDARY_V1.md",
 "NOTICE_TEMPLATE_V1.md",
 "LEGAL_BASIS_AND_REFERENCES_V1.md",
 "LICENSE_DEPLOYMENT_MANIFEST_V1.json",
 "REPOSITORY_ADOPTION_CHECKLIST_V1.md",
 "LICENSE_HEADER_TEMPLATE_V1.txt",
]
def fail(msg): raise SystemExit(f"FAIL: {msg}")
def main():
    missing=[x for x in REQUIRED if not (BASE/x).is_file()]
    if missing: fail(f"missing files: {missing}")
    m=json.loads((BASE/"LICENSE_DEPLOYMENT_MANIFEST_V1.json").read_text(encoding="utf-8"))
    if m.get("schema_version")!="rafaelia.license-deployment-manifest/v1": fail("manifest schema")
    if m.get("claim_allowed") is not False: fail("claim_allowed")
    p=m.get("policies",{})
    if p.get("commercial_use")!="SEPARATE_WRITTEN_LICENSE_REQUIRED": fail("commercial gate")
    if p.get("third_party_override") is not False: fail("third-party override")
    if p.get("raw_relicense_all_repository") is not False: fail("blanket relicensing")
    lic=(BASE/"RAFAELIA_ORIGINAL_WORKS_NC_ATTRIBUTION_LICENSE_V1_PTBR.md").read_text(encoding="utf-8")
    required_phrases=[
        "É proibido qualquer Uso Comercial sem licença comercial separada",
        "US$ 1,00",
        "não se aplica, nem altera, direitos de terceiros",
        "atribuição obrigatória",
        "núcleo contratual essencial",
        "Não se confunde com \"cláusula pétrea\"",
    ]
    for s in required_phrases:
        if s not in lic: fail(f"license invariant missing: {s}")
    legal=(BASE/"LEGAL_BASIS_AND_REFERENCES_V1.md").read_text(encoding="utf-8")
    if "nenhuma Súmula Vinculante é inventada" not in legal: fail("binding precedent honesty gate")
    print(json.dumps({
      "status":"PASS",
      "required_files":len(REQUIRED),
      "commercial_license_separate":True,
      "third_party_override":False,
      "blanket_relicense":False,
      "usd1_is_licensor_cap":True,
      "claim_allowed":False,
      "legal_enforceability":"COUNSEL_REVIEW_REQUIRED"
    },sort_keys=True))
if __name__=="__main__": main()
