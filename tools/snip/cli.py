"""Command line entry point: ``snip <command>``."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from snip.generate import generate
from snip.model import Repo
from snip.sync import sync
from snip.validate import validate


def find_root(start: Path) -> Path:
    """The nearest directory holding both pyproject.toml and content/."""
    for path in [start, *start.parents]:
        if (path / "pyproject.toml").is_file() and (path / "content").is_dir():
            return path
    raise SystemExit("snip: run this inside the py-snippets repository")


def _report(problems: list[str], ok: str) -> int:
    for problem in problems:
        print(f"  ✗ {problem}", file=sys.stderr)
    if problems:
        print(f"{len(problems)} problem(s)", file=sys.stderr)
        return 1
    print(ok)
    return 0


MODULE_TEMPLATE = '''from collections.abc import Iterable


def {name}(items: Iterable[object]) -> object:
    """One line: what it returns, in plain words.

    >>> {name}([1, 2, 3])
    TODO
    >>> {name}([])
    TODO
    """
    raise NotImplementedError
'''

PAGE_TEMPLATE = """---
slug: {slug}
title: TODO
summary: TODO
category: {category}
tags: []
module: {category}/{name}.py
complexity: O(n) time, O(1) space
since: "3.11"
published: {today}
related: []
---

One or two sentences: the problem this solves.

<?snippet "{category}/{name}.py"?>

<?snippet "{category}/{name}.py" part="examples"?>

## How it works

- TODO
"""


def cmd_new(repo: Repo, category: str, name: str) -> int:
    if category not in {c["id"] for c in repo.categories}:
        raise SystemExit(f"snip: unknown category {category!r}")
    slug = name.replace("_", "-")
    module = repo.root / "src" / "pysnippets" / category / f"{name}.py"
    page = repo.root / "content" / "snippets" / slug / "index.md"
    if module.exists() or page.exists():
        raise SystemExit(f"snip: {name} already exists")
    module.write_text(MODULE_TEMPLATE.format(name=name), encoding="utf-8")
    page.parent.mkdir(parents=True)
    page.write_text(
        PAGE_TEMPLATE.format(
            slug=slug, category=category, name=name, today=date.today().isoformat()
        ),
        encoding="utf-8",
    )
    print(f"Created {module.relative_to(repo.root)} and {page.relative_to(repo.root)}")
    print(f"Next: export {name} from {category}/__init__.py, then `snip sync`.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="snip", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("sync", help="copy code and examples into the pages")
    p.add_argument("--check", action="store_true", help="fail if anything is stale")
    sub.add_parser("validate", help="check the content rules")
    p = sub.add_parser("generate", help="write CATALOG, ATTRIBUTION and site data")
    p.add_argument("--check", action="store_true", help="fail if anything is stale")
    p.add_argument("--site", action="store_true", help="also write site/src/generated")
    p = sub.add_parser("new", help="scaffold a snippet module and page")
    p.add_argument("category")
    p.add_argument("name", help="the function name, in snake_case")
    args = parser.parse_args(argv)

    repo = Repo.load(find_root(Path.cwd()))
    if args.command == "sync":
        stale = sync(repo, check=args.check)
        if args.check:
            return _report(
                [f"{p} is out of date; run `snip sync`" for p in stale],
                "Pages match the code.",
            )
        print(f"Synced {len(stale)} page(s).")
        return 0
    if args.command == "validate":
        return _report(validate(repo), f"{len(repo.snippets)} snippets valid.")
    if args.command == "generate":
        stale = generate(repo, check=args.check, site=args.site)
        if args.check:
            return _report(
                [f"{p} is out of date; run `snip generate`" for p in stale],
                "Generated files are current.",
            )
        print(
            f"Wrote {len(stale)} file(s)."
            + (" Site data written." if args.site else "")
        )
        return 0
    return cmd_new(repo, args.category, args.name)


if __name__ == "__main__":
    raise SystemExit(main())
