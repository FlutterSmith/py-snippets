---
slug: pluck
title: "Pluck one field from a list of dicts"
summary: "Collect the value of a key from each dict, with None where it's missing."
category: dicts
tags: [mapping, nested]
module: dicts/pluck.py
complexity: "O(n) time, O(n) space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [pluck]
  change: "Typed; added the missing-key example."
related: [map-values, get-nested]
---

Turn a list of records into a list of one field, such as every user's age.

<?snippet "dicts/pluck.py"?>
```python
from collections.abc import Iterable, Mapping
from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V")


def pluck(records: Iterable[Mapping[K, V]], key: K) -> list[V | None]:
    """Return ``record[key]`` for each record, or ``None`` where it's missing."""
    # @note .get keeps one result per record, even when the key is missing
    return [record.get(key) for record in records]
```

<?snippet "dicts/pluck.py" part="examples"?>
```pycon
>>> simpsons = [{"name": "lisa", "age": 8}, {"name": "homer", "age": 36}, {}]
>>> pluck(simpsons, "age")
[8, 36, None]
>>> pluck([], "age")
[]
```

## How it works

- `.get(key)` returns `None` for a missing key instead of raising.
- The result always has one entry per record, so it lines up with the input.
- For a required field, `[r[key] for r in records]` fails loudly instead.
