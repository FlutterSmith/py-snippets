---
slug: bifurcate-by
title: "Split a list in two with a predicate"
summary: "Partition items into those that pass a test and those that don't, in one pass."
category: lists
tags: [splitting]
module: lists/bifurcate_by.py
complexity: "O(n) time, O(n) space"
since: "3.11"
published: 2026-10-01
fixes: "The original called the predicate twice per item and walked the input twice, so with a generator the second list always came back empty."
origin:
  upstream: [bifurcate-by]
  change: "Rewritten: single pass, returns a tuple, accepts any iterable, typed."
related: [group-by, chunk-into-n]
---

Two list comprehensions work, but they walk the data twice and call your test twice per item. That's slow for an expensive check and wrong for a one-shot iterator.

<?snippet "lists/bifurcate_by.py"?>
```python
from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")


def bifurcate_by(
    items: Iterable[T], predicate: Callable[[T], object]
) -> tuple[list[T], list[T]]:
    """Split ``items`` into the ones that pass ``predicate`` and the ones that don't."""
    passed: list[T] = []
    failed: list[T] = []
    for item in items:
        # @note one pass, so `predicate` runs once per item
        (passed if predicate(item) else failed).append(item)
    return passed, failed
```

<?snippet "lists/bifurcate_by.py" part="examples"?>
```pycon
>>> bifurcate_by(["beep", "boop", "foo", "bar"], lambda w: w.startswith("b"))
(['beep', 'boop', 'bar'], ['foo'])
>>> passed, failed = bifurcate_by(range(10), lambda n: n % 3 == 0)
>>> passed, failed
([0, 3, 6, 9], [1, 2, 4, 5, 7, 8])
>>> bifurcate_by([], bool)
([], [])
```

## How it works

- One loop. The conditional expression picks which list to append to.
- Order is kept within each half.
- It returns a tuple, so `passed, failed = ...` unpacks it.
