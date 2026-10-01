---
slug: key-of-max
title: "Key of the largest or smallest value"
summary: "Find the key with the largest or smallest value using max() or min() with a key function."
category: dicts
tags: [search, sorting]
module: dicts/key_of_max.py
complexity: "O(n) time, O(1) space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [key-of-max, key-of-min]
  change: "Merged max and min into one page; typed."
related: [sort-dict-by-value, most-frequent]
---

Which product sold most? `max(d.values())` gives the number but not the product. Rank the keys by value instead.

<?snippet "dicts/key_of_max.py"?>
```python
from collections.abc import Mapping
from typing import Any, Protocol, TypeVar


class _SupportsLessThan(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K")
V = TypeVar("V", bound=_SupportsLessThan)


def key_of_max(d: Mapping[K, V]) -> K:
    """Return the key of the largest value in ``d``; on a tie, the first one."""
    # @note iterating a dict yields keys; key= ranks them by value
    return max(d, key=d.__getitem__)


def key_of_min(d: Mapping[K, V]) -> K:
    """Return the key of the smallest value in ``d``; on a tie, the first one."""
    return min(d, key=d.__getitem__)
```

<?snippet "dicts/key_of_max.py" part="examples"?>
```pycon
>>> key_of_max({"a": 4, "b": 0, "c": 13})
'c'
>>> key_of_max({"x": 1, "y": 1})
'x'
>>> key_of_min({"a": 4, "b": 0, "c": 13})
'b'
```

## How it works

- Iterating a dict yields its keys.
- `key=d.__getitem__` ranks each key by its value.
- On a tie, `max` and `min` return the first key, in dict order. An empty dict raises `ValueError`.
