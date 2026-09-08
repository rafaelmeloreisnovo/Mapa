#!/usr/bin/env python3
import json, pathlib, struct

ROOT = pathlib.Path(__file__).resolve().parent

def fail(msg):
    print("FAIL:", msg)
    raise SystemExit(1)

manifest = json.loads((ROOT / "SYSTEM_MAP.json").read_text(encoding="utf-8"))
rights = json.loads((ROOT / "SYSTEM_RIGHTS.json").read_text(encoding="utf-8"))
dirs = json.loads((ROOT / "DIRECTIONS_7.json").read_text(encoding="utf-8"))
routes = json.loads((ROOT / "ROUTES.json").read_text(encoding="utf-8"))

folders = manifest["folders"]
if manifest["count_physical_folders"] != 41 or len(folders) != 41:
    fail("physical folder count != 41")
paths = [f["path"] for f in folders]
if len(set(paths)) != 41:
    fail("folder paths are not unique")
ids = [f["id"] for f in folders]
if len(set(ids)) != 41:
    fail("folder IDs are not unique")
for f in folders:
    p = ROOT / f["path"] / ".folder.json"
    if not p.is_file():
        fail(f"missing folder marker: {p}")
    marker = json.loads(p.read_text(encoding="utf-8"))
    if marker.get("id") != f["id"]:
        fail(f"folder marker ID mismatch: {p}")

if manifest["source_entries_received"] != 29 or manifest["source_unique_names"] != 28:
    fail("source-list accounting changed")
if manifest["duplicate_logical_entry"]["name"] != "Temas":
    fail("Temas logical duplicate was not preserved")
if len(manifest["duplicate_logical_entry"]["logical_views"]) != 2:
    fail("Temas must have two logical views")

d = dirs["directions"]
if len(d) != 7:
    fail("direction count != 7")
vectors = {x["code"]: x.get("vector") for x in d if "vector" in x}
expected = {
    "X+":[1,0,0], "X-":[-1,0,0], "Y+":[0,1,0],
    "Y-":[0,-1,0], "Z+":[0,0,1], "Z-":[0,0,-1]
}
if vectors != expected:
    fail("signed Cartesian direction basis mismatch")
omega = [x for x in d if x["code"] == "OMEGA360"]
if len(omega) != 1:
    fail("OMEGA360 missing or duplicated")

valid_rights = set(rights["legacy_letters"])
for name, letters in rights["profiles"].items():
    if not set(letters) <= valid_rights:
        fail(f"invalid rights profile {name}")
if any(x in rights["profiles"]["APPEND_ONLY_WRITER"] for x in ("E","M","A","S")):
    fail("append-only profile grants destructive/control right")

letters = [m["letter"] for m in routes["mappings"]]
if len(letters) != len(set(letters)):
    fail("virtual drive letters duplicated")
if "S" not in letters:
    fail("shared virtual drive S missing")
for m in routes["mappings"]:
    if m["profile"] not in rights["profiles"]:
        fail(f"unknown mapping rights profile: {m['profile']}")

shared = next(f for f in folders if f["id"] == "F29")
if shared["share_by_default"] is not False:
    fail("shared surface must still be explicit, not auto-share")
for f in folders:
    if f["share_by_default"] is not False:
        fail(f"unexpected auto-share folder: {f['id']}")

dbf = (ROOT / "SYSTEM_MAP.DBF").read_bytes()
if len(dbf) < 32 or dbf[0] != 0x03:
    fail("DBF is not dBASE III")
nrec = struct.unpack("<I", dbf[4:8])[0]
if nrec != 41:
    fail(f"DBF record count {nrec} != 41")

idx = (ROOT / "SYSTEM_MAP.IDX").read_text(encoding="utf-8").splitlines()
rows = [x for x in idx if x and not x.startswith("#")]
if len(rows) != 41:
    fail(f"IDX row count {len(rows)} != 41")

print("PASS CASA41: 41 folders; 7 directions; rights/routes coherent; DBF+IDX 41 records.")
