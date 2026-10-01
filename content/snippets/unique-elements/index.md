---
slug: unique-elements
title: "Remove duplicates and keep order"
summary: "De-duplicate a list while keeping the first occurrence of each value, in order."
category: lists
tags: [dedupe]
module: lists/unique_elements.py
complexity: "O(n) time, O(n) space"
since: "3.11"
published: 2026-10-01
fixes: "The original used `list(set(items))`, which loses order. Its example only looked right because small integers happen to hash in order."
origin:
  upstream: [unique-elements]
  change: "Rewritten to keep order; typed."
related: [duplicates, has-duplicates]
---

`list(set(items))` is the usual answer, and it scrambles the order. `dict.fromkeys` keeps it.

<?snippet "lists/unique_elements.py"?>
```python
from collections.abc import Hashable, Iterable
from typing import TypeVar

H = TypeVar("H", bound=Hashable)


def unique_elements(items: Iterable[H]) -> list[H]:
    """Remove duplicates from ``items``, keeping the first occurrence of each."""
    # @note dict keys are unique and remember insertion order; a set doesn't
    return list(dict.fromkeys(items))
```

<?snippet "lists/unique_elements.py" part="examples"?>
```pycon
>>> unique_elements([3, 1, 3, 2, 1])
[3, 1, 2]
>>> unique_elements("mississippi")
['m', 'i', 's', 'p']
>>> unique_elements([])
[]
```

## How it works

- Dict keys are unique, and since Python 3.7 dicts keep insertion order.
- `dict.fromkeys(items)` keeps the first occurrence of each value; `list()` takes the keys back out.
- Values must be hashable. For lists of dicts, de-duplicate on a key instead.
