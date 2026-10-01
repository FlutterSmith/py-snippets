---
slug: have-same-contents
title: "Check two lists hold the same items"
summary: "Compare two collections regardless of order, counting duplicates, in linear time."
category: lists
tags: [validation, counting]
module: lists/have_same_contents.py
complexity: "O(n + m) time, O(n + m) space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [have-same-contents]
  change: "Rewritten with Counter (O(n) instead of O(n²)); typed."
related: [has-duplicates]
---

Order doesn't matter, but counts do: `[1, 1, 2]` and `[1, 2, 2]` are different, which `set(a) == set(b)` misses.

<?snippet "lists/have_same_contents.py"?>
```python
from collections import Counter
from collections.abc import Hashable, Iterable


def have_same_contents(a: Iterable[Hashable], b: Iterable[Hashable]) -> bool:
    """Return ``True`` if ``a`` and ``b`` hold the same values, in any order."""
    # @note compares counts per value in O(n), not O(n²)
    return Counter(a) == Counter(b)
```

<?snippet "lists/have_same_contents.py" part="examples"?>
```pycon
>>> have_same_contents([1, 2, 4], [2, 4, 1])
True
>>> have_same_contents([1, 1, 2], [1, 2, 2])
False
>>> have_same_contents([], ())
True
```

## How it works

- Two `Counter`s are equal when every value has the same count.
- That's one pass over each input. Calling `list.count()` per value, as the original did, is O(n²).
- Needs hashable items; for unhashable ones, compare `sorted(a) == sorted(b)`.
