---
slug: intersection-by
title: "List intersection by a key"
summary: "Keep the items of one list whose key also appears in another, preserving order."
category: lists
tags: [sets]
module: lists/intersection_by.py
complexity: "O(n + m) time, O(m) space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [intersection-by]
  change: "Typed; added a case-insensitive example."
related: [difference-by, union-by]
---

Find the users in the old list that also exist in the new one, matching case-insensitively, or by ID.

<?snippet "lists/intersection_by.py"?>
```python
from collections.abc import Callable, Hashable, Iterable
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K", bound=Hashable)


def intersection_by(a: Iterable[T], b: Iterable[T], key: Callable[[T], K]) -> list[T]:
    """Return the items of ``a`` whose ``key`` matches some item of ``b``."""
    seen = {key(item) for item in b}
    # @note order and duplicates come from a, never from b
    return [item for item in a if key(item) in seen]
```

<?snippet "lists/intersection_by.py" part="examples"?>
```pycon
>>> from math import floor
>>> intersection_by([2.1, 1.2], [2.3, 3.4], floor)
[2.1]
>>> intersection_by(["Ada", "bob"], ["ADA", "Cy"], str.lower)
['Ada']
```

## How it works

- Same shape as `difference_by`, with `in` instead of `not in`.
- The result always holds items from `a`, never from `b`.
