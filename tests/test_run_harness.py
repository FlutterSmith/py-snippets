"""The in-browser Run harness, exercised under CPython on every snippet."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest

from snip.model import Repo

ROOT = Path(__file__).resolve().parents[1]
REPO = Repo.load(ROOT)


def _harness() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "run_harness", ROOT / "site/public/run-harness.py"
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


HARNESS = _harness()


@pytest.mark.parametrize("snippet", REPO.snippets, ids=lambda s: s.slug)
def test_every_snippet_passes_in_the_harness(snippet: object) -> None:
    module = snippet.module  # type: ignore[attr-defined]
    result = json.loads(HARNESS.run_snippet(module.code, module.pycon))
    assert "error" not in result
    assert result["results"]
    assert all(r["ok"] for r in result["results"]), result


def test_a_broken_edit_fails_the_right_example() -> None:
    code = "def double(n):\n    return n + n\n"
    examples = ">>> double(2)\n4\n>>> double(3)\n7\n>>> double('a')\n'aa'\n"
    results = json.loads(HARNESS.run_snippet(code, examples))["results"]
    assert [r["ok"] for r in results] == [True, False, True]
    assert results[1]["got"] == "6\n"


def test_errors_in_the_code_are_reported() -> None:
    result = json.loads(HARNESS.run_snippet("def broken(:\n", ">>> 1\n1\n"))
    assert "SyntaxError" in result["error"]
    result = json.loads(HARNESS.run_snippet("raise ValueError('no')\n", ">>> 1\n1\n"))
    assert result["error"].endswith("ValueError: no\n")


def test_unexpected_exceptions_are_shortened() -> None:
    code = "def f():\n    return 1 / 0\n"
    results = json.loads(HARNESS.run_snippet(code, ">>> f()\n1\n"))["results"]
    assert results[0]["ok"] is False
    assert results[0]["got"].endswith("ZeroDivisionError: division by zero\n")
