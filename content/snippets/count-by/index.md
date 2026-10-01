---
slug: count-by
title: "Count items by a key"
summary: "Count how many items map to each key, using collections.Counter."
category: lists
tags: [counting, grouping]
module: lists/count_by.py
complexity: "O(n) time, O(k) space for k keys"
since: "3.11"
published: 2026-10-01
stdlib: "If you're counting the items themselves, `Counter(items)` is all you need."
origin:
  upstream: [count-by]
  change: "Rewritten with Counter; key is required and typed."
related: [group-by, most-frequent]
---

Like `group_by`, but when you only need the size of each group.

<?snippet "lists/count_by.py"?>
```python
from collections import Counter
from collections.abc import Callable, Hashable, Iterable
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K", bound=Hashable)


def count_by(items: Iterable[T], key: Callable[[T], K]) -> dict[K, int]:
    """Count ``items`` by the result of ``key``."""
    # @note Counter does the counting; map applies key lazily
    return dict(Counter(map(key, items)))
```

<?snippet "lists/count_by.py" part="examples"?>
```pycon
>>> from math import floor
>>> count_by([6.1, 4.2, 6.3], floor)
{6: 2, 4: 1}
>>> count_by(["one", "two", "three"], len)
{3: 2, 5: 1}
>>> count_by([], len)
{}
```

## How it works

- `map(key, items)` computes the keys lazily.
- `Counter` tallies them in one pass. Converting to `dict` gives a plain result with a predictable repr.
