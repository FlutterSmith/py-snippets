"""Reads a snippet module: its functions, display code and doctest examples."""

from __future__ import annotations

import ast
import doctest
import inspect
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Example:
    """One doctest example: the source typed at ``>>>`` and the expected output."""

    source: str
    want: str


@dataclass(frozen=True)
class Function:
    """A public, top-level function in a snippet module."""

    name: str
    signature: str
    summary: str
    examples: tuple[Example, ...]


@dataclass(frozen=True)
class Module:
    """A parsed snippet module."""

    path: Path
    functions: tuple[Function, ...]
    code: str
    """The module as shown on the site: docstrings cut to their summary line."""

    @property
    def examples(self) -> tuple[Example, ...]:
        return tuple(e for f in self.functions for e in f.examples)

    @property
    def pycon(self) -> str:
        """All examples as an interactive session, in function order."""
        return "\n".join(to_pycon(e) for e in self.examples)


def to_pycon(example: Example) -> str:
    """Render ``example`` the way the interactive interpreter shows it."""
    lines = example.source.rstrip("\n").split("\n")
    prompt = [f">>> {lines[0]}"] + [f"... {line}".rstrip() for line in lines[1:]]
    return "\n".join(prompt + example.want.rstrip("\n").split("\n")).rstrip("\n")


def _summary(doc: str) -> str:
    return doc.strip().split("\n\n", 1)[0].replace("\n", " ")


def markdown_summary(doc: str) -> str:
    """The summary line with reST ``literals`` turned into Markdown `code`."""
    return re.sub(r"``(.+?)``", r"`\1`", doc)


def _signature(source: str, node: ast.FunctionDef) -> str:
    """The ``def`` line(s) up to the colon, collapsed onto one line."""
    first = node.lineno - 1
    body = node.body[0].lineno - 1
    header = "\n".join(source.splitlines()[first:body])
    header = " ".join(header.strip().removeprefix("def ").rstrip(":").split())
    # Undo the formatter's line breaks: "( a, b, )" -> "(a, b)".
    return re.sub(r",?\s*\)", ")", re.sub(r"\(\s+", "(", header))


def parse_module(path: Path) -> Module:
    """Parse the snippet module at ``path``."""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    parser = doctest.DocTestParser()
    functions = []
    lines = source.splitlines()
    # Replace docstrings bottom-up so earlier line numbers stay valid.
    replacements: list[tuple[int, int, str]] = []
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef) or node.name.startswith("_"):
            continue
        doc = ast.get_docstring(node) or ""
        examples = tuple(
            Example(e.source, e.want)
            for e in parser.get_examples(inspect.cleandoc(doc))
        )
        functions.append(
            Function(node.name, _signature(source, node), _summary(doc), examples)
        )
        first = node.body[0]
        if doc and isinstance(first, ast.Expr) and first.end_lineno is not None:
            indent = lines[first.lineno - 1][: first.col_offset]
            short = f'{indent}"""{_summary(doc)}"""'
            replacements.append((first.lineno - 1, first.end_lineno, short))
    for start, end, text in sorted(replacements, reverse=True):
        lines[start:end] = [text]
    return Module(path, tuple(functions), "\n".join(lines).strip("\n") + "\n")
