#!/usr/bin/env python3
import json, sys

VALID = {True, False, "TOKEN_VAZIO"}
VALID_STILL = VALID | {"TOKEN_VAZIO_REVALIDATION_REQUIRED"}

def fail(msg):
    raise SystemExit("FAIL: " + msg)

def main(path):
    x = json.load(open(path, encoding="utf-8"))
    for k in ["item_id","object_ref","scope","authority","real","done","good","still_good","dependencies","gaps","falsifier","next_probe","claim_allowed","provenance"]:
        if k not in x:
            fail("missing " + k)
    if x["claim_allowed"] is not False:
        fail("claim_allowed must remain false at record level")
    for k in ["real","done","good"]:
        if x[k]["state"] not in VALID:
            fail("invalid state " + k)
    if x["still_good"]["state"] not in VALID_STILL:
        fail("invalid still_good state")
    if x["done"]["state"] is True and x["real"]["state"] is not True:
        fail("DONE requires REAL")
    if x["good"]["state"] is True and x["done"]["state"] is not True:
        fail("GOOD requires DONE")
    if x["still_good"]["state"] is True and x["good"]["state"] is not True:
        fail("STILL_GOOD requires GOOD")
    if x["real"]["state"] is True and not x["real"].get("evidence_refs"):
        fail("REAL requires evidence_refs")
    if x["done"]["state"] is True and (not x["done"].get("obligation") or not x["done"].get("closure_gate_refs")):
        fail("DONE requires obligation and closure gate")
    if x["good"]["state"] is True and not (x["good"].get("quality_gate_refs") or x["good"].get("security_gate_refs") or x["good"].get("anti_regression_refs")):
        fail("GOOD requires at least one applied gate reference")
    if x["still_good"]["state"] is True and not x["still_good"].get("revalidation_refs"):
        fail("STILL_GOOD requires revalidation receipt")
    if not x["provenance"]:
        fail("provenance required")
    print("PASS", x["item_id"], x["scope"], "REAL=", x["real"]["state"], "DONE=", x["done"]["state"], "GOOD=", x["good"]["state"], "STILL_GOOD=", x["still_good"]["state"])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail("usage: validate_rdgs.py record.json")
    main(sys.argv[1])
