---
slug: collect-dictionary
title: "Invert a dictionary, keeping every key"
summary: "Invert a dict so each value maps to the list of keys that had it."
category: dicts
tags: [mapping, grouping]
module: dicts/collect_dictionary.py
complexity: "O(n) time, O(n) space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [collect-dictionary]
  change: "Typed; returns a plain dict."
related: [invert-dictionary, group-by]
---

Who is 10 years old? Inverting `{name: age}` with a plain comprehension keeps only one name per age. This keeps all of them.

<?snippet "dicts/collect_dictionary.py"?>
```python
from collections import defaultdict
from collections.abc import Hashable, Mapping
from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V", bound=Hashable)


def collect_dictionary(d: Mapping[K, V]) -> dict[V, list[K]]:
    """Invert ``d``, collecting every key that shares a value into a list."""
    inverted: defaultdict[V, list[K]] = defaultdict(list)
    for key, value in d.items():
        # @note keys stay in d's order inside each list
        inverted[value].append(key)
    return dict(inverted)
```

<?snippet "dicts/collect_dictionary.py" part="examples"?>
```pycon
>>> collect_dictionary({"Peter": 10, "Isabel": 10, "Anna": 9})
{10: ['Peter', 'Isabel'], 9: ['Anna']}
>>> collect_dictionary({})
{}
```

## How it works

- `defaultdict(list)` starts an empty list for each new value.
- Keys keep the dict's order inside each list.
- It's `group_by` applied to a dict's items.
