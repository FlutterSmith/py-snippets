---
slug: invert-dictionary
title: "Invert a dictionary"
summary: "Swap keys and values with a dict comprehension; the last key wins on shared values."
category: dicts
tags: [mapping]
module: dicts/invert_dictionary.py
complexity: "O(n) time, O(n) space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [invert-dictionary]
  change: "Typed; documents and tests the collision rule."
related: [collect-dictionary]
---

Turn a code-to-name table into a name-to-code table.

<?snippet "dicts/invert_dictionary.py"?>
```python
from collections.abc import Hashable, Mapping
from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V", bound=Hashable)


def invert_dictionary(d: Mapping[K, V]) -> dict[V, K]:
    """Swap the keys and values of ``d``."""
    # @note values become keys, so they must be hashable
    return {value: key for key, value in d.items()}
```

<?snippet "dicts/invert_dictionary.py" part="examples"?>
```pycon
>>> invert_dictionary({"Peter": 10, "Isabel": 11, "Anna": 9})
{10: 'Peter', 11: 'Isabel', 9: 'Anna'}
>>> invert_dictionary({"a": 1, "b": 1})
{1: 'b'}
```

## How it works

- A dict comprehension builds the new dict in one pass.
- Values become keys, so they must be hashable.
- Two keys with the same value collide, and the later one wins. If that loses data you need, use `collect_dictionary`.
