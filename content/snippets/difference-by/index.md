---
slug: difference-by
title: "List difference by a key"
summary: "Keep the items of one list whose key doesn't appear in another, preserving order."
category: lists
tags: [sets]
module: lists/difference_by.py
complexity: "O(n + m) time, O(m) space"
since: "3.11"
published: 2026-10-01
fixes: "The original documented the result as `[ { x: 2 } ]`, which is JavaScript, not Python."
origin:
  upstream: [difference-by]
  change: "Typed; fixed the example's invalid result syntax."
related: [intersection-by, union-by]
---

`set(a) - set(b)` loses order and needs hashable items. This compares on a key instead, so it works for dicts and objects.

<?snippet "lists/difference_by.py"?>
```python
from collections.abc import Callable, Hashable, Iterable
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K", bound=Hashable)


def difference_by(a: Iterable[T], b: Iterable[T], key: Callable[[T], K]) -> list[T]:
    """Return the items of ``a`` whose ``key`` matches no item of ``b``."""
    # @note a set of b's keys makes each lookup O(1)
    seen = {key(item) for item in b}
    return [item for item in a if key(item) not in seen]
```

<?snippet "lists/difference_by.py" part="examples"?>
```pycon
>>> from math import floor
>>> difference_by([2.1, 1.2], [2.3, 3.4], floor)
[1.2]
>>> difference_by([{"x": 2}, {"x": 1}], [{"x": 1}], lambda d: d["x"])
[{'x': 2}]
```

## How it works

- The keys of `b` go into a set, so each lookup is O(1).
- Items of `a` keep their order and their duplicates.
