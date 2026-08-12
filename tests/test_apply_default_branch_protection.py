#!/usr/bin/env python3
import importlib.util
import io
import json
import os
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

MOD_PATH = Path(__file__).resolve().parents[1] / "tools" / "apply_default_branch_protection.py"
spec = importlib.util.spec_from_file_location("apply_default_branch_protection", MOD_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class FakeResponse:
    def __init__(self, status, payload):
        self.status = status
        self.payload = payload

    def read(self):
        return json.dumps(self.payload).encode("utf-8") if self.payload is not None else b""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def run_main(args, env=None):
    out = io.StringIO()
    with mock.patch.dict(os.environ, env or {}, clear=True), redirect_stdout(out):
        code = mod.main(args)
    return code, out.getvalue()


def test_dry_run():
    code, out = run_main(["--owner", "o", "--repo", "r", "--required-context", "CI"])
    assert code == 0 and "DRY_RUN" in out


def test_requires_context():
    code, out = run_main(["--owner", "o", "--repo", "r"])
    assert code == 2 and "REJECT" in out


def test_apply_requires_yes():
    code, out = run_main(["--owner", "o", "--repo", "r", "--required-context", "CI", "--apply"])
    assert code == 3 and "requires --yes" in out


def test_apply_requires_token():
    code, out = run_main(["--owner", "o", "--repo", "r", "--required-context", "CI", "--apply", "--yes"])
    assert code == 4 and "missing token" in out


def test_payload_safety():
    payload = mod.build_payload(["CI"])
    assert payload["required_status_checks"] == {"strict": True, "contexts": ["CI"]}
    assert payload["enforce_admins"] is True
    assert payload["allow_force_pushes"] is False
    assert payload["allow_deletions"] is False
    assert payload["required_pull_request_reviews"]["required_approving_review_count"] == 1


def test_apply_and_verify_pass():
    calls = []

    def opener(req):
        calls.append((req.method, req.full_url))
        if req.method == "PUT":
            return FakeResponse(200, {"url": "ok"})
        return FakeResponse(200, {
            "name": "main",
            "protected": True,
            "protection": {"enabled": True, "required_status_checks": {"enforcement_level": "non_admins"}},
        })

    _, metadata = mod.apply("o", "r", "main", ["CI"], "t", opener=opener)
    assert metadata["protected"] is True
    assert calls == [
        ("PUT", "https://api.github.com/repos/o/r/branches/main/protection"),
        ("GET", "https://api.github.com/repos/o/r/branches/main"),
    ]


def test_postcondition_fail_closed():
    def opener(req):
        if req.method == "PUT":
            return FakeResponse(200, {"url": "ok"})
        return FakeResponse(200, {
            "name": "main",
            "protected": False,
            "protection": {"enabled": False, "required_status_checks": {"enforcement_level": "off"}},
        })

    try:
        mod.apply("o", "r", "main", ["CI"], "t", opener=opener)
    except RuntimeError as exc:
        assert "postcondition failed" in str(exc)
    else:
        raise AssertionError("expected fail-closed postcondition")


def main():
    tests = [value for key, value in sorted(globals().items()) if key.startswith("test_")]
    for test in tests:
        test()
        print("PASS", test.__name__)
    print(f"PASS {len(tests)}/{len(tests)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
