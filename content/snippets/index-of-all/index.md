---
slug: index-of-all
title: "Find every index of a value"
summary: "Return all positions of a value, or of items matching a predicate."
category: lists
tags: [search]
module: lists/index_of_all.py
complexity: "O(n) time, O(k) space for k matches"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [index-of-all, find-index-of-all]
  change: "Merged two snippets into one page; typed."
related: [find-keys]
---

`list.index()` finds the first match only, and raises if there is none. These return every match, and an empty list when there's none.

<?snippet "lists/index_of_all.py"?>
```python
from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")


def index_of_all(items: Iterable[T], value: T) -> list[int]:
    """Return every index at which ``value`` occurs in ``items``."""
    return [i for i, item in enumerate(items) if item == value]


def find_index_of_all(
    items: Iterable[T], predicate: Callable[[T], object]
) -> list[int]:
    """Return every index whose item passes ``predicate``."""
    # @note enumerate pairs each item with its index
    return [i for i, item in enumerate(items) if predicate(item)]
```

<?snippet "lists/index_of_all.py" part="examples"?>
```pycon
>>> index_of_all([1, 2, 1, 4, 5, 1], 1)
[0, 2, 5]
>>> index_of_all([1, 2, 3, 4], 6)
[]
>>> find_index_of_all([1, 2, 3, 4], lambda n: n % 2 == 1)
[0, 2]
>>> find_index_of_all("Hello World", str.isupper)
[0, 6]
```

## How it works

- `enumerate` pairs each item with its index.
- `index_of_all` compares with `==`; `find_index_of_all` takes any test.
- Both work on any iterable, including strings and generators.
