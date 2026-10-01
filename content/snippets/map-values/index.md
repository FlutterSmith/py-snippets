---
slug: map-values
title: "Transform every value in a dict"
summary: "Build a new dict with a function applied to each value, keeping the keys."
category: dicts
tags: [mapping]
module: dicts/map_values.py
complexity: "O(n) time, O(n) space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [map-values]
  change: "Rewritten as a dict comprehension; typed."
related: [pluck]
---

Pull one field out of every record, or format every price: keep the keys, change the values.

<?snippet "dicts/map_values.py"?>
```python
from collections.abc import Callable, Mapping
from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V")
R = TypeVar("R")


def map_values(d: Mapping[K, V], fn: Callable[[V], R]) -> dict[K, R]:
    """Return a new dict with ``fn`` applied to every value of ``d``."""
    # @note keys and their order are untouched
    return {key: fn(value) for key, value in d.items()}
```

<?snippet "dicts/map_values.py" part="examples"?>
```pycon
>>> users = {"fred": {"age": 40, "pets": 1}, "pebbles": {"age": 1, "pets": 0}}
>>> map_values(users, lambda user: user["age"])
{'fred': 40, 'pebbles': 1}
>>> map_values({"a": "x"}, str.upper)
{'a': 'X'}
```

## How it works

- A dict comprehension applies `fn` to each value.
- Keys and their order don't change, and the input isn't modified.
