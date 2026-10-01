---
slug: get-nested
title: "Get a value from nested data"
summary: "Follow a path of keys and indexes through nested dicts and lists, with a default."
category: dicts
tags: [nested, search]
module: dicts/get_nested.py
complexity: "O(k) time for a path of length k"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [get]
  change: "Renamed from get; returns a default instead of raising; typed."
related: [deep-flatten, pluck]
---

`data['user']['posts'][0]['title']` raises somewhere in the middle when the JSON is missing a piece. This returns a default instead.

<?snippet "dicts/get_nested.py"?>
```python
from collections.abc import Hashable, Iterable
from typing import Any


def get_nested(data: Any, path: Iterable[Hashable], default: Any = None) -> Any:
    """Follow ``path`` through nested dicts and lists, or return ``default``."""
    for step in path:
        try:
            data = data[step]
        # @note missing key, index out of range, or a step into a non-container
        except (KeyError, IndexError, TypeError):
            return default
    return data
```

<?snippet "dicts/get_nested.py" part="examples"?>
```pycon
>>> users = {"fred": {"name": {"last": "Smith"}, "posts": [1, 2, 3]}}
>>> get_nested(users, ["fred", "name", "last"])
'Smith'
>>> get_nested(users, ["fred", "posts", 1])
2
>>> get_nested(users, ["fred", "posts", 9], default=0)
0
```

## How it works

- Each step indexes into the current value.
- A missing key, an index out of range, or indexing into `None` all return `default`.
- Paths can mix dict keys and list indexes.
