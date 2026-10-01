---
slug: hamming-distance
title: "Hamming distance between strings"
summary: "Count the positions at which two equal-length strings differ."
category: strings
tags: [text, counting]
module: strings/hamming_distance.py
complexity: "O(n) time, O(1) space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [hamming-distance]
  change: "Rewritten for strings; the integer version is shown below."
related: [byte-size]
---

How many characters changed between two codes, sequences or hashes of the same length?

<?snippet "strings/hamming_distance.py"?>
```python
def hamming_distance(a: str, b: str) -> int:
    """Return how many positions differ between two equal-length strings."""
    if len(a) != len(b):
        raise ValueError(f"strings must have equal length, got {len(a)} and {len(b)}")
    # @note True counts as 1 in sum()
    return sum(x != y for x, y in zip(a, b, strict=True))
```

<?snippet "strings/hamming_distance.py" part="examples"?>
```pycon
>>> hamming_distance("karolin", "kathrin")
3
>>> hamming_distance("", "")
0
>>> hamming_distance("abc", "ab")
Traceback (most recent call last):
...
ValueError: strings must have equal length, got 3 and 2
```

## How it works

- `zip(..., strict=True)` walks both strings in step.
- `x != y` is a bool, and `sum` counts each `True` as 1.
- Different lengths raise `ValueError`: Hamming distance isn't defined for them.

For integers, count the differing bits instead:

```python
(a ^ b).bit_count()  # Python 3.10+
```
