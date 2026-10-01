---
slug: union-by
title: "List union by a key"
summary: "Merge two lists, keeping the first item for each key, in a predictable order."
category: lists
tags: [sets, dedupe]
module: lists/union_by.py
complexity: "O(n + m) time, O(n + m) space"
since: "3.11"
published: 2026-10-01
fixes: "The original passed the result through `set()`, so the order depended on hashing: its own example returns `[1.2, 2.1]`, not the documented `[2.1, 1.2]`."
origin:
  upstream: [union-by]
  change: "Rewritten: deterministic order, first item wins; typed."
related: [intersection-by, difference-by, unique-elements]
---

Merge two contact lists without duplicates, where two entries match when their emails match in any case.

<?snippet "lists/union_by.py"?>
```python
from collections.abc import Callable, Hashable, Iterable
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K", bound=Hashable)


def union_by(a: Iterable[T], b: Iterable[T], key: Callable[[T], K]) -> list[T]:
    """Merge ``a`` and ``b``, keeping the first item for each ``key``, in order."""
    seen: set[K] = set()
    merged = []
    for items in (a, b):
        for item in items:
            k = key(item)
            # @note first one wins, so a beats b on a tie
            if k not in seen:
                seen.add(k)
                merged.append(item)
    return merged
```

<?snippet "lists/union_by.py" part="examples"?>
```pycon
>>> from math import floor
>>> union_by([2.1], [1.2, 2.3], floor)
[2.1, 1.2]
>>> union_by(["Ada", "bob"], ["ADA", "Cy"], str.lower)
['Ada', 'bob', 'Cy']
```

## How it works

- A set of seen keys decides whether each item is new.
- Items of `a` come first, then the new items of `b`, each in their original order.
- Duplicates inside `a` are dropped too.
