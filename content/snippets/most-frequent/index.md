---
slug: most-frequent
title: "Find the most frequent value"
summary: "Return the most common item, breaking ties by first appearance."
category: lists
tags: [counting]
module: lists/most_frequent.py
complexity: "O(n) time, O(k) space for k distinct values"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [most-frequent]
  change: "Rewritten with Counter: O(n), deterministic ties, clear empty error."
related: [count-by, duplicates]
---

The popular one-liner `max(set(items), key=items.count)` is O(n²), and on a tie its answer depends on set order.

<?snippet "lists/most_frequent.py"?>
```python
from collections import Counter
from collections.abc import Hashable, Iterable
from typing import TypeVar

H = TypeVar("H", bound=Hashable)


def most_frequent(items: Iterable[H]) -> H:
    """Return the most common value in ``items``; on a tie, the one seen first."""
    # @note most_common(1) is a single O(n) pass
    top = Counter(items).most_common(1)
    if not top:
        raise ValueError("most_frequent() arg is an empty iterable")
    return top[0][0]
```

<?snippet "lists/most_frequent.py" part="examples"?>
```pycon
>>> most_frequent([1, 2, 1, 2, 3, 2, 1, 4, 2])
2
>>> most_frequent("abracadabra")
'a'
>>> most_frequent([])
Traceback (most recent call last):
...
ValueError: most_frequent() arg is an empty iterable
```

## How it works

- `Counter.most_common(1)` finds the top value in one pass.
- Ties go to the value seen first, which is documented `Counter` behaviour.
- An empty input raises `ValueError`, the same as `max([])`.
