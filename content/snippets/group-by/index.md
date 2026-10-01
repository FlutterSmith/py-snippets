---
slug: group-by
title: "Group items by a key"
summary: "Bucket items into lists keyed by a function, keeping the original order inside each group."
category: lists
tags: [grouping]
module: lists/group_by.py
complexity: "O(n) time, O(n) space"
since: "3.11"
published: 2026-10-01
stdlib: "`itertools.groupby` only groups *adjacent* items, so it needs sorted input. This doesn't."
origin:
  upstream: [group-by]
  change: "Typed with generic keys; prose rewritten."
related: [count-by, bifurcate-by]
---

Group words by length, orders by customer, files by extension: one function covers all of them.

<?snippet "lists/group_by.py"?>
```python
from collections import defaultdict
from collections.abc import Callable, Hashable, Iterable
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K", bound=Hashable)


def group_by(items: Iterable[T], key: Callable[[T], K]) -> dict[K, list[T]]:
    """Group ``items`` into lists by the result of ``key``, keeping their order."""
    groups: defaultdict[K, list[T]] = defaultdict(list)
    for item in items:
        groups[key(item)].append(item)
    # @note a plain dict, so a missing key raises instead of inserting
    return dict(groups)
```

<?snippet "lists/group_by.py" part="examples"?>
```pycon
>>> from math import floor
>>> group_by([6.1, 4.2, 6.3], floor)
{6: [6.1, 6.3], 4: [4.2]}
>>> group_by(["one", "two", "three"], len)
{3: ['one', 'two'], 5: ['three']}
>>> group_by([], len)
{}
```

## How it works

- `defaultdict(list)` creates each group's list the first time its key appears.
- Converting back to a plain `dict` means a later lookup of a missing key raises, instead of silently adding an empty group.
- Groups appear in the order their first item was seen.
