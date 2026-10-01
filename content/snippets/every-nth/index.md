---
slug: every-nth
title: "Every nth item of a list"
summary: "Take every nth item from a sequence, starting with the nth, using a slice."
category: lists
tags: [iteration]
module: lists/every_nth.py
complexity: "O(n / k) time and space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [every-nth]
  change: "Typed, validates n, works on any sequence."
related: [chunk-into-n]
---

Thin a dataset, pick every third row, sample a log: it's one slice once you know the start and step.

<?snippet "lists/every_nth.py"?>
```python
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def every_nth(items: Sequence[T], n: int) -> list[T]:
    """Return every ``n``-th item of ``items``, starting with the ``n``-th."""
    if n < 1:
        raise ValueError(f"n must be at least 1, got {n}")
    # @note start at index n - 1, step n
    return list(items[n - 1 :: n])
```

<?snippet "lists/every_nth.py" part="examples"?>
```pycon
>>> every_nth([1, 2, 3, 4, 5, 6], 2)
[2, 4, 6]
>>> every_nth(range(1, 11), 3)
[3, 6, 9]
>>> every_nth([1, 2], 5)
[]
```

## How it works

- A slice is `[start:stop:step]`. Starting at `n - 1` makes the first pick the n-th item.
- Slicing a `range` returns a `range`, so the result is wrapped in `list()`.
- `n` below 1 raises, rather than producing a confusing empty or reversed list.
