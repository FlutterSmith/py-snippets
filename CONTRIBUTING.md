# Contributing

Thanks for helping. This collection makes one promise: every example on the page ran and passed. The rules below exist to keep that promise, and CI checks all of them.

## Quick start

```sh
uv sync                                   # Python 3.11+ and the dev tools
uv run snip new lists take_while_sum      # scaffold a module and its page
# write the function and its doctests, export it from lists/__init__.py, then:
uv run snip sync                          # copy code and examples into the page
uv run snip validate                      # content rules
uv run snip generate                      # README, CATALOG, ATTRIBUTION, cheat sheets
uv run pytest && uv run ruff check . && uv run mypy
```

Fixing a typo in the prose? Edit the Markdown and open a pull request. CI runs the checks.

## How a snippet is built

```
src/pysnippets/<category>/<name>.py   the function, with doctests in its docstring
tests/test_<category>.py              Hypothesis properties for the claims that matter
content/snippets/<slug>/index.md      frontmatter + prose + two markers
```

### The module

One module per snippet, and it must stand alone: no imports from other snippets, so a reader can copy one file.

```python
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def every_nth(items: Sequence[T], n: int) -> list[T]:
    """Return every ``n``-th item of ``items``, starting with the ``n``-th.

    >>> every_nth([1, 2, 3, 4, 5, 6], 2)
    [2, 4, 6]
    >>> every_nth([1, 2], 5)
    []
    """
    if n < 1:
        raise ValueError(f"n must be at least 1, got {n}")
    # @note start at index n - 1, step n
    return list(items[n - 1 :: n])
```

- **Type everything.** `mypy --strict` must pass. Use `TypeVar`, not `def f[T]`, while 3.11 is supported.
- **The first docstring line is the summary.** The page shows it in place of the docstring.
- **Doctests:** at least two examples per page, one of them an edge case (empty input, `n <= 0`, a tie). Results must be deterministic on every supported Python. No dates from `today()`, no unseeded randomness, no hash-order sets.
- **`# @note`** on its own line annotates the next line; at the end of a line, it annotates that line. Keep notes under about 60 characters. They are the author talking.
- **Validate arguments** that would otherwise give a confusing result, and raise `ValueError` with a message that says what was wrong.

### The page

```yaml
---
slug: every-nth                 # the folder name, kebab-case
title: "Every nth item of a list"
summary: "One sentence, at most 160 characters."
category: lists                 # from content/categories.yaml
tags: [iteration]               # from content/tags.yaml
module: lists/every_nth.py
complexity: "O(n / k) time and space"
since: "3.11"                   # oldest Python it supports: 3.11 to 3.14
published: 2026-10-01
stdlib: "Optional: the built-in that covers part of this job."
fixes: "Optional: what the original snippet got wrong."
origin:                         # only for material adapted from 30-seconds-of-python
  upstream: [every-nth]         # names from content/upstream.yaml
  change: "What we changed. CC BY 4.0 requires it."
related: [chunk-into-n]
---

One or two sentences: the problem this solves.

<?snippet "lists/every_nth.py"?>

<?snippet "lists/every_nth.py" part="examples"?>

## How it works

- Two to four short bullets.
```

`snip sync` fills in a `python` fence after the first marker and a `pycon` fence after the second. Don't edit those fences by hand; CI fails if they drift from the module.

## The cheat sheets

`content/stdlib.yaml` ("the stdlib already does this") and `content/idioms.yaml` ("Python idioms for JavaScript developers") are lists of rows. Each row's `example` is a doctest and runs in CI. A row with `since: "3.12"` is skipped on older Pythons.

If your snippet idea is a one-liner over something Python already has, it belongs in one of these files, not in `src/`.

## Voice

- Short sentences. No emoji, no hype, no "simply" or "just". `snip validate` rejects a list of these.
- Say what happens on empty input, and which version a feature needs.
- Prefer "use `Counter`" over a clever one-liner.
- At most 200 words of prose per page. It's a thirty-second read.

## Adapted material

When you adapt a snippet from 30-seconds-of-python, set `origin.upstream` and `origin.change`, and remove its name from `planned` in `content/upstream.yaml`. `snip validate` checks that each of the 160 originals has exactly one home. Never use the 30 seconds of code name, logo or images as branding.

## Pull requests

One snippet per pull request. The template has a short checklist.
