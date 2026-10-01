---
slug: sort-by-indexes
title: "Sort a list by a matching list of positions"
summary: "Order items by the number at the same position in a second list."
category: lists
tags: [sorting]
module: lists/sort_by_indexes.py
complexity: "O(n log n) time, O(n) space"
since: "3.11"
published: 2026-10-01
fixes: "The original used plain `zip`, so an index list one item short silently dropped the last item."
origin:
  upstream: [sort-by-indexes]
  change: "Sorts on the index only, rejects mismatched lengths; typed."
related: [sort-dict-by-value]
---

You have names in one list and their ranks in another. Pair them, sort by rank, keep the names.

<?snippet "lists/sort_by_indexes.py"?>
```python
from collections.abc import Iterable
from operator import itemgetter
from typing import TypeVar

T = TypeVar("T")


def sort_by_indexes(
    items: Iterable[T], indexes: Iterable[float], *, reverse: bool = False
) -> list[T]:
    """Sort ``items`` by the matching number in ``indexes``."""
    # @note strict=True: a missing index is an error, not a silent drop
    pairs = zip(indexes, items, strict=True)
    # @note sort on the index only, so items never get compared
    return [item for _, item in sorted(pairs, key=itemgetter(0), reverse=reverse)]
```

<?snippet "lists/sort_by_indexes.py" part="examples"?>
```pycon
>>> food = ["eggs", "bread", "oranges", "jam", "apples", "milk"]
>>> sort_by_indexes(food, [3, 2, 6, 4, 1, 5])
['apples', 'bread', 'eggs', 'jam', 'milk', 'oranges']
>>> sort_by_indexes(food, [3, 2, 6, 4, 1, 5], reverse=True)
['oranges', 'milk', 'jam', 'eggs', 'bread', 'apples']
>>> sort_by_indexes("abc", [1, 2])
Traceback (most recent call last):
...
ValueError: zip() argument 2 is longer than argument 1
```

## How it works

- `zip(..., strict=True)` pairs each index with its item, and raises if the lengths differ.
- The sort key is the index alone. Sorting the raw pairs would compare items whenever two indexes tie, which fails for dicts.
- `sorted` is stable: equal indexes keep their original order.
