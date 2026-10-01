---
slug: chunk-into-n
title: "Split a list into n chunks"
summary: "Split a sequence into exactly n lists whose sizes differ by at most one."
category: lists
tags: [splitting]
module: lists/chunk_into_n.py
complexity: "O(n) time, O(n) space"
since: "3.11"
published: 2026-10-01
stdlib: "For chunks of a fixed **size** rather than a fixed **count**, use `itertools.batched(items, size)` (3.12+)."
fixes: "The original rounded the chunk size up, so `chunk_into_n([1, 2, 3, 4, 5], 4)` gave `[[1, 2], [3, 4], [5], []]`: uneven, with an empty chunk at the end."
origin:
  upstream: [chunk-into-n]
  change: "Rewritten: balanced sizes, always n chunks, typed, validates n."
related: [bifurcate-by, group-by]
---

You have 10 jobs and 3 workers. You want 3 piles that are as even as possible, not piles of 4, 4 and 2.

<?snippet "lists/chunk_into_n.py"?>
```python
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def chunk_into_n(items: Sequence[T], n: int) -> list[list[T]]:
    """Split ``items`` into ``n`` lists whose sizes differ by at most one."""
    if n < 1:
        raise ValueError(f"n must be at least 1, got {n}")
    # @note the first `extra` chunks get one more item
    size, extra = divmod(len(items), n)
    chunks = []
    start = 0
    for i in range(n):
        end = start + size + (i < extra)
        chunks.append(list(items[start:end]))
        start = end
    return chunks
```

<?snippet "lists/chunk_into_n.py" part="examples"?>
```pycon
>>> chunk_into_n([1, 2, 3, 4, 5, 6, 7], 4)
[[1, 2], [3, 4], [5, 6], [7]]
>>> chunk_into_n([1, 2, 3, 4, 5], 4)
[[1, 2], [3], [4], [5]]
>>> chunk_into_n([1, 2], 3)
[[1], [2], []]
```

## How it works

- `divmod` gives the base `size` and the `extra` items left over.
- The first `extra` chunks take one more item. `i < extra` is a bool, and `True` adds as 1.
- The result always has exactly `n` lists. When there are fewer items than chunks, the last ones are empty.
