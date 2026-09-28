#!/usr/bin/env python3
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "manifold" / "ai_architecture_current_v1.json"

def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)

def main() -> int:
    obj = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if obj.get("schema") != "rafaelia.ai-architecture-manifold-current.v1":
        fail("schema")
    if obj.get("version") != "1.0.0":
        fail("version")
    if obj.get("claim_allowed") is not False:
        fail("claim_allowed")
    rp = obj.get("read_policy", {})
    if rp.get("roots_max") != 3 or rp.get("depth_default") != 1 or len(rp.get("roots", [])) != 3:
        fail("bounded read policy")
    nodes = obj.get("nodes", [])
    node_ids = {n.get("id") for n in nodes}
    if None in node_ids or len(node_ids) != len(nodes):
        fail("node ids")
    for edge in obj.get("edges", []):
        if edge.get("from") not in node_ids or edge.get("to") not in node_ids:
            fail(f"dangling edge {edge}")
    if len(obj.get("atlas_areas", [])) < 12:
        fail("atlas areas")
    if len(obj.get("agent_roles", [])) < 11:
        fail("agent roles")
    if len(obj.get("session_packets", [])) < 8:
        fail("session packets")
    for role in obj.get("agent_roles", []):
        if role.get("node") not in node_ids:
            fail(f"agent node binding {role.get('id')}")
        if not role.get("evidence_rule"):
            fail(f"agent evidence rule {role.get('id')}")
    if not any(g.get("state") == "TOKEN_VAZIO" for g in obj.get("gaps", [])):
        fail("explicit TOKEN_VAZIO gap")
    print("PASS ai_architecture_current_v1")
    print(f"nodes={len(nodes)} edges={len(obj.get('edges', []))} atlas={len(obj.get('atlas_areas', []))} roles={len(obj.get('agent_roles', []))} packets={len(obj.get('session_packets', []))}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
