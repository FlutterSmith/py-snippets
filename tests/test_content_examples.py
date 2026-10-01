"""Runs the examples in content/stdlib.yaml and content/idioms.yaml as doctests."""

from __future__ import annotations

import doctest
import sys
from pathlib import Path
from typing import Any

import pytest
import yaml

CONTENT = Path(__file__).resolve().parents[1] / "content"


def _rows(name: str) -> list[dict[str, Any]]:
    data: list[dict[str, Any]] = yaml.safe_load((CONTENT / name).read_text("utf-8"))
    return data


def _version(text: str) -> tuple[int, int]:
    major, minor = text.split(".")
    return int(major), int(minor)


ROWS = [pytest.param(row, id=f"stdlib:{row['id']}") for row in _rows("stdlib.yaml")]
ROWS += [pytest.param(row, id=f"idioms:{row['id']}") for row in _rows("idioms.yaml")]


@pytest.mark.parametrize("row", ROWS)
def test_example(row: dict[str, Any]) -> None:
    since = _version(str(row.get("since", "3.11")))
    if sys.version_info[:2] < since:
        pytest.skip(f"needs Python {row['since']}")
    parser = doctest.DocTestParser()
    test = parser.get_doctest(row["example"], {}, row["id"], None, 0)
    runner = doctest.DocTestRunner(verbose=False)
    out: list[str] = []
    result = runner.run(test, out=out.append)
    assert result.failed == 0, "".join(out)
