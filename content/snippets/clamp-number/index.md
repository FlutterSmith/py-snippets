---
slug: clamp-number
title: "Clamp a number to a range"
summary: "Limit a value to an inclusive range, accepting the bounds in either order."
category: numbers
tags: [validation]
module: numbers/clamp_number.py
complexity: "O(1) time and space"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [clamp-number]
  change: "Typed; clearer names."
related: [num-to-range]
---

Keep a volume between 0 and 100, or a page number inside the document.

<?snippet "numbers/clamp_number.py"?>
```python
def clamp_number(value: float, low: float, high: float) -> float:
    """Limit ``value`` to the range between ``low`` and ``high``, inclusive."""
    # @note sort the bounds so callers can't get them backwards
    low, high = min(low, high), max(low, high)
    return max(low, min(value, high))
```

<?snippet "numbers/clamp_number.py" part="examples"?>
```pycon
>>> clamp_number(2, 3, 5)
3
>>> clamp_number(1, -1, -5)
-1
>>> clamp_number(4.5, 0, 10)
4.5
```

## How it works

- `min(value, high)` caps the top; `max(low, ...)` lifts the bottom.
- The bounds are sorted first, so `clamp_number(x, 10, 0)` works too.
- Ints stay ints and floats stay floats.
