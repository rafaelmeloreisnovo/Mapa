#!/usr/bin/env python3
import argparse, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
M = json.loads((ROOT / "SYSTEM_MAP.json").read_text(encoding="utf-8"))
R = json.loads((ROOT / "ROUTES.json").read_text(encoding="utf-8"))
D = json.loads((ROOT / "DIRECTIONS_7.json").read_text(encoding="utf-8"))
P = json.loads((ROOT / "SYSTEM_RIGHTS.json").read_text(encoding="utf-8"))

def folders():
    for f in M["folders"]:
        print(f'{f["id"]}\t{f["legacy_alias"]:<8}\t{f["path"]}\t{f["display_name"]}')

def maps():
    for m in R["mappings"]:
        print(f'{m["letter"]}: -> {m["target"]} [{m["profile"]}]')

def resolve(token):
    t = token.rstrip(":").upper()
    for m in R["mappings"]:
        if m["letter"] == t:
            print(m["target"])
            return
    for f in M["folders"]:
        if token.upper() in (f["id"].upper(), f["legacy_alias"].upper()) or token == f["path"]:
            print(str(ROOT / f["path"]))
            return
    print("TOKEN_VAZIO_NOT_FOUND")
    raise SystemExit(2)

def directions():
    for d in D["directions"]:
        print(d["id"], d["code"], d.get("vector", d.get("operator")), "-", d["role"])

def rights(name=None):
    if name:
        x = P["profiles"].get(name.upper())
        if x is None:
            print("TOKEN_VAZIO_PROFILE")
            raise SystemExit(2)
        print(name.upper(), "".join(x))
        return
    for k, v in P["profiles"].items():
        print(k, "".join(v))

ap = argparse.ArgumentParser(prog="system_map")
sp = ap.add_subparsers(dest="cmd", required=True)
sp.add_parser("folders")
sp.add_parser("maps")
sp.add_parser("directions")
r = sp.add_parser("resolve"); r.add_argument("token")
q = sp.add_parser("rights"); q.add_argument("profile", nargs="?")
a = ap.parse_args()
{"folders":folders,"maps":maps,"directions":directions,
 "resolve":lambda:resolve(a.token),"rights":lambda:rights(a.profile)}[a.cmd]()
