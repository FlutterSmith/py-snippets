---
slug: duplicates
title: "Find duplicate and single values"
summary: "List the values that repeat, or the ones that appear exactly once."
category: lists
tags: [dedupe, counting]
module: lists/duplicates.py
complexity: "O(n) time, O(n) space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [filter-unique, filter-non-unique]
  change: "Merged and renamed (filter_unique → duplicates, filter_non_unique → singles); typed."
related: [has-duplicates, unique-elements]
---

Which IDs appear twice in the import? Which appear only once? One `Counter` answers both.

<?snippet "lists/duplicates.py"?>
```python
from collections import Counter
from collections.abc import Hashable, Iterable
from typing import TypeVar

H = TypeVar("H", bound=Hashable)


def duplicates(items: Iterable[H]) -> list[H]:
    """Return the values that appear more than once, in first-seen order."""
    return [item for item, count in Counter(items).items() if count > 1]


def singles(items: Iterable[H]) -> list[H]:
    """Return the values that appear exactly once, in first-seen order."""
    # @note Counter keeps first-seen order, so the result does too
    return [item for item, count in Counter(items).items() if count == 1]
```

<?snippet "lists/duplicates.py" part="examples"?>
```pycon
>>> duplicates([1, 2, 2, 3, 4, 4, 4, 5])
[2, 4]
>>> duplicates([1, 2, 3])
[]
>>> singles([1, 2, 2, 3, 4, 4, 4, 5])
[1, 3, 5]
>>> singles("aabbc")
['c']
```

## How it works

- `Counter(items)` counts every value in one pass.
- Its items come back in first-seen order, so the results do too.
- `duplicates` keeps counts above 1; `singles` keeps counts of exactly 1.
