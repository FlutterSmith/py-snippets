---
slug: sort-dict-by-value
title: "Sort a dictionary by value"
summary: "Return a copy of a dict ordered by its values, ascending or descending."
category: dicts
tags: [sorting]
module: dicts/sort_dict_by_value.py
complexity: "O(n log n) time, O(n) space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [sort-dict-by-value]
  change: "itemgetter instead of a lambda; keyword-only reverse; typed."
related: [key-of-max, sort-by-indexes]
---

Dicts keep insertion order, so a sorted dict is a dict built from sorted items.

<?snippet "dicts/sort_dict_by_value.py"?>
```python
from collections.abc import Mapping
from operator import itemgetter
from typing import Any, Protocol, TypeVar


class _SupportsLessThan(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K")
V = TypeVar("V", bound=_SupportsLessThan)


def sort_dict_by_value(d: Mapping[K, V], *, reverse: bool = False) -> dict[K, V]:
    """Return a copy of ``d`` ordered by value."""
    # @note itemgetter(1) picks the value from each (key, value) pair
    return dict(sorted(d.items(), key=itemgetter(1), reverse=reverse))
```

<?snippet "dicts/sort_dict_by_value.py" part="examples"?>
```pycon
>>> d = {"one": 1, "three": 3, "five": 5, "two": 2, "four": 4}
>>> sort_dict_by_value(d)
{'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
>>> sort_dict_by_value(d, reverse=True)
{'five': 5, 'four': 4, 'three': 3, 'two': 2, 'one': 1}
```

## How it works

- `d.items()` gives `(key, value)` pairs; `itemgetter(1)` sorts them by value.
- `dict()` rebuilds the mapping in that order.
- `reverse` is keyword-only, so a call reads `reverse=True`, never a bare `True`.
