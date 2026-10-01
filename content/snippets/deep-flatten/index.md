---
slug: deep-flatten
title: "Flatten a nested list of any depth"
summary: "Lazily yield every value from arbitrarily nested iterables, treating strings as values."
category: lists
tags: [nested, iteration]
module: lists/deep_flatten.py
complexity: "O(n) time, O(d) stack for depth d"
since: "3.11"
published: 2026-10-01
stdlib: "For exactly one level, use `itertools.chain.from_iterable(lists)`."
fixes: "The original recursed into strings, so `deep_flatten(['ab'])` crashed with `RecursionError`."
origin:
  upstream: [deep-flatten]
  change: "Rewritten as a generator; strings and bytes are treated as values."
related: [get-nested]
---

API responses and config files nest lists inside lists. This walks all of them and yields the values in order.

<?snippet "lists/deep_flatten.py"?>
```python
from collections.abc import Iterable, Iterator


def deep_flatten(items: Iterable[object]) -> Iterator[object]:
    """Yield every non-iterable value from arbitrarily nested iterables."""
    for item in items:
        # @note without this check "ab" recurses forever: "a" is iterable too
        if isinstance(item, Iterable) and not isinstance(item, str | bytes):
            yield from deep_flatten(item)
        else:
            yield item
```

<?snippet "lists/deep_flatten.py" part="examples"?>
```pycon
>>> list(deep_flatten([1, [2], [[3], 4], 5]))
[1, 2, 3, 4, 5]
>>> list(deep_flatten(["ab", ("cd", ["ef"])]))
['ab', 'cd', 'ef']
>>> list(deep_flatten([[], [[]]]))
[]
```

## How it works

- `yield from` recurses into anything iterable.
- `str` and `bytes` are iterable, and so is each character, so without the check a string recurses until it hits the recursion limit.
- It's a generator: wrap it in `list()` when you need a list.
