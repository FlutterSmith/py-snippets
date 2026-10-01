"""Run a snippet's doctests in the browser, the way CI runs them.

Pyodide loads this file in a Web Worker and calls ``run_snippet``. It reports
every example: whether it passed, what was expected and what came back.
"""

import doctest
import json
import sys
import traceback
from types import TracebackType
from typing import Any

TRACEBACK = "Traceback (most recent call last):"


def _short(text: str) -> str:
    """Cut a full traceback down to the lines a doctest would show."""
    lines = text.rstrip("\n").split("\n")
    if TRACEBACK not in lines:
        return text
    start = lines.index(TRACEBACK)
    tail = [line for line in lines[start + 1 :] if line and not line.startswith(" ")]
    return "\n".join([*lines[:start], TRACEBACK, "...", *tail[-1:]]) + "\n"


class _Collect(doctest.DocTestRunner):
    """A runner that records each example's outcome instead of printing it."""

    def __init__(self) -> None:
        super().__init__(verbose=False)
        self.seen: dict[int, tuple[bool, str]] = {}

    def report_start(self, out: Any, test: Any, example: doctest.Example) -> None:
        pass

    def report_success(
        self, out: Any, test: Any, example: doctest.Example, got: str
    ) -> None:
        self.seen[id(example)] = (True, got)

    def report_failure(
        self, out: Any, test: Any, example: doctest.Example, got: str
    ) -> None:
        self.seen[id(example)] = (False, _short(got))

    def report_unexpected_exception(
        self,
        out: Any,
        test: Any,
        example: doctest.Example,
        exc_info: tuple[type[BaseException], BaseException, TracebackType],
    ) -> None:
        exc = "".join(traceback.format_exception_only(exc_info[0], exc_info[1]))
        self.seen[id(example)] = (False, f"{TRACEBACK}\n...\n{exc}")


def run_snippet(code: str, examples: str) -> str:
    """Execute ``code``, run ``examples`` against it, and return JSON results."""
    namespace: dict[str, Any] = {"__name__": "__snippet__"}
    try:
        exec(compile(code, "snippet.py", "exec"), namespace)
    # Report anything the reader typed, including SystemExit and KeyboardInterrupt.
    except BaseException as e:
        if isinstance(e, SyntaxError):
            detail = "".join(traceback.format_exception_only(type(e), e))
        else:
            full = traceback.format_exception(type(e), e, e.__traceback__)
            detail = _short("".join(full))
        return json.dumps({"error": detail})
    parser = doctest.DocTestParser()
    try:
        test = parser.get_doctest(examples, namespace, "examples", "examples.pycon", 0)
    except ValueError as e:
        return json.dumps({"error": f"Couldn't read the examples: {e}\n"})
    runner = _Collect()
    runner.run(test, out=lambda _: None, clear_globs=False)
    results = []
    for ex in test.examples:
        ok, got = runner.seen.get(id(ex), (True, ex.want))
        results.append({"source": ex.source, "want": ex.want, "ok": ok, "got": got})
    return json.dumps({"results": results, "python": sys.version.split()[0]})
