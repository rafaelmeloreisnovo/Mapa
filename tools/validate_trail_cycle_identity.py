#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
UID=re.compile(r"^[A-Z0-9_]+-[0-9]{3}-[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}$")
TRAIL=re.compile(r"^[A-Z][A-Z0-9_]+$")
LEGACY=re.compile(r"^C[0-9]+$")

def validate_record(d):
    e=[]
    trail=d.get("trail_id")
    seq=d.get("trail_seq")
    uid=d.get("cycle_uid")
    legacy=d.get("legacy_local_cycle")
    if not isinstance(trail,str) or not TRAIL.fullmatch(trail): e.append("trail_id")
    if not isinstance(seq,int) or seq<1: e.append("trail_seq")
    if not isinstance(uid,str) or not UID.fullmatch(uid): e.append("cycle_uid")
    if isinstance(trail,str) and isinstance(seq,int) and isinstance(uid,str):
        prefix=f"{trail}-{seq:03d}-"
        if not uid.startswith(prefix): e.append("uid_prefix")
    if legacy is not None and (not isinstance(legacy,str) or not LEGACY.fullmatch(legacy)): e.append("legacy_local_cycle")
    if d.get("claim_allowed") is not False: e.append("claim_allowed")
    return e

def validate_many(records):
    e=[]; seen={}
    for i,d in enumerate(records):
        for x in validate_record(d): e.append(f"record[{i}].{x}")
        uid=d.get("cycle_uid")
        if uid in seen: e.append(f"duplicate_cycle_uid:{uid}")
        else: seen[uid]=i
    return e

def main():
    if len(sys.argv)<2:
        print("usage: validate_trail_cycle_identity.py <json> [<json> ...]"); return 2
    records=[]
    for p in sys.argv[1:]:
        d=json.loads(Path(p).read_text(encoding="utf-8"))
        records.append(d)
    e=validate_many(records)
    if e:
        for x in e: print("REJECT",x)
        return 1
    print(f"PASS trail-cycle-identity records={len(records)} unique_cycle_uid={len(records)}")
    return 0
if __name__=="__main__": raise SystemExit(main())
