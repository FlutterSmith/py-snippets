---
slug: find-keys
title: "Find the keys for a value"
summary: "Return every key whose value equals a given value."
category: dicts
tags: [search]
module: dicts/find_keys.py
complexity: "O(n) time, O(k) space for k matches"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [find-keys]
  change: "Typed; no longer shadows the dict builtin."
related: [collect-dictionary, index-of-all]
---

Dicts are fast from key to value only. Going the other way means a scan, so make it a readable one.

<?snippet "dicts/find_keys.py"?>
```python
from collections.abc import Mapping
from typing import TypeVar

K = TypeVar("K")


def find_keys(d: Mapping[K, object], value: object) -> list[K]:
    """Return every key of ``d`` whose value equals ``value``."""
    # @note a linear scan: dicts index by key, not by value
    return [key for key, v in d.items() if v == value]
```

<?snippet "dicts/find_keys.py" part="examples"?>
```pycon
>>> find_keys({"Peter": 10, "Isabel": 11, "Anna": 10}, 10)
['Peter', 'Anna']
>>> find_keys({"Peter": 10}, 99)
[]
```

## How it works

- A comprehension over `d.items()` keeps the matching keys, in dict order.
- No match gives an empty list, not an error.
- If you do this lookup often, build an inverted dict once with `collect_dictionary`.
