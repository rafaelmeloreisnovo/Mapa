#!/usr/bin/env python3
import importlib.util, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("selector", ROOT / "tools/select_required_status_check.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)

def payload(*runs):
    return {"check_runs": list(runs)}

def run(name, conclusion="success", status="completed"):
    return {"name": name, "status": status, "conclusion": conclusion}

def expect_reject(fn):
    try:
        fn()
    except ValueError:
        return
    raise AssertionError("expected rejection")

def main():
    assert M.choose(payload(run("gate")), payload(run("gate"))) == "gate"
    expect_reject(lambda: M.choose(payload(run("gate","failure")), payload(run("gate"))))
    expect_reject(lambda: M.choose(payload(run("gate")), payload(run("gate","failure"))))
    expect_reject(lambda: M.choose(payload(run("gate",None,"in_progress")), payload(run("gate"))))
    assert M.choose(payload(run("gate"), run("other")), payload(run("gate"), run("other")), "other") == "other"
    expect_reject(lambda: M.choose(payload(run("a"),run("b")), payload(run("a"),run("b"))))
    expect_reject(lambda: M.choose(payload(run("gate"),run("gate","failure")), payload(run("gate"))))
    expect_reject(lambda: M.choose(payload(run("cycle","failure"),run("evaluate","failure")),
                                     payload(run("cycle","failure"),run("branch-topology / validate","failure"))))
    print("PASS 8/8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
