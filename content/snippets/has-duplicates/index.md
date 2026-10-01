---
slug: has-duplicates
title: "Check a list for duplicates"
summary: "Return True as soon as any value repeats, even in a huge or endless iterable."
category: lists
tags: [dedupe, validation]
module: lists/has_duplicates.py
complexity: "O(n) time worst case, O(n) space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [has-duplicates]
  change: "Rewritten to exit early and accept any iterable; typed."
related: [duplicates, unique-elements]
---

`len(items) != len(set(items))` builds the whole set before it can answer. This returns at the first repeat.

<?snippet "lists/has_duplicates.py"?>
```python
from collections.abc import Hashable, Iterable


def has_duplicates(items: Iterable[Hashable]) -> bool:
    """Return ``True`` if any value occurs more than once in ``items``."""
    seen = set()
    for item in items:
        # @note stops at the first repeat, so it works on huge or endless input
        if item in seen:
            return True
        seen.add(item)
    return False
```

<?snippet "lists/has_duplicates.py" part="examples"?>
```pycon
>>> has_duplicates([1, 2, 3, 4, 5, 5])
True
>>> has_duplicates([1, 2, 3, 4, 5])
False
>>> has_duplicates(n % 7 for n in range(10**9))
True
```

## How it works

- Each item is checked against the values seen so far.
- It stops at the first repeat, which is why the example can scan a billion-item generator instantly.
- Values must be hashable.
