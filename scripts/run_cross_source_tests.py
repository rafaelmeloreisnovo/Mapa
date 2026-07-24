#!/usr/bin/env python3
"""Run the canonical cross-source test set and emit measured evidence."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
TEST_ROOT = ROOT / "tests"
TEST_PATTERNS = (
    "test_cross_source*.py",
    "test_compare_cross_source_evidence.py",
    "test_validate_chain_of_custody.py",
)


def discover_test_files() -> tuple[str, ...]:
    """Discover the governed test surface deterministically.

    The patterns are explicit enough to avoid unrelated repository tests while
    allowing new cross-source tests to enter the measured suite without editing
    a hard-coded file tuple.
    """

    paths: set[Path] = set()
    for pattern in TEST_PATTERNS:
        paths.update(path for path in TEST_ROOT.glob(pattern) if path.is_file())
    return tuple(path.relative_to(ROOT).as_posix() for path in sorted(paths))


TEST_FILES = discover_test_files()


def load_module(path: Path, index: int) -> ModuleType:
    module_name = f"_rafaelia_cross_source_test_{index}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load test module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def build_suite() -> unittest.TestSuite:
    if not TEST_FILES:
        raise RuntimeError("canonical cross-source test discovery returned no files")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for index, relative_path in enumerate(TEST_FILES):
        path = ROOT / relative_path
        if not path.is_file():
            raise FileNotFoundError(f"canonical test file not found: {relative_path}")
        suite.addTests(loader.loadTestsFromModule(load_module(path, index)))
    return suite


def run_suite(verbosity: int = 2) -> tuple[unittest.TestResult, dict[str, object]]:
    suite = build_suite()
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    report: dict[str, object] = {
        "schema_version": "rafaelia.cross-source-test-report/v2",
        "status": "PASS" if result.wasSuccessful() else "FAIL",
        "test_patterns": list(TEST_PATTERNS),
        "test_files": list(TEST_FILES),
        "test_file_count": len(TEST_FILES),
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(getattr(result, "skipped", [])),
        "expected_failures": len(getattr(result, "expectedFailures", [])),
        "unexpected_successes": len(getattr(result, "unexpectedSuccesses", [])),
        "claim_allowed": False,
        "remote_ci_substituted": False,
        "next_verifiable_step": (
            "Evaluate the measured test result against the versioned quality floor."
            if result.wasSuccessful()
            else "Correct the failing canonical tests before producing promotion evidence."
        ),
    }
    return result, report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", type=Path)
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result, report = run_suite(verbosity=0 if args.quiet else 2)
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
