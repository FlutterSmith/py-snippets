---
slug: digitize
title: "Split a number into its digits"
summary: "Turn an integer into a list of its decimal digits."
category: numbers
tags: [conversion]
module: numbers/digitize.py
complexity: "O(d) time and space for d digits"
since: "3.11"
published: 2026-10-01
fixes: "The original raised `ValueError` for negative numbers."
origin:
  upstream: [digitize]
  change: "Handles negative numbers; typed."
related: [to-roman-numeral]
---

Checksums, digit sums and number puzzles all start here.

<?snippet "numbers/digitize.py"?>
```python
def digitize(n: int) -> list[int]:
    """Return the decimal digits of ``n``, ignoring its sign."""
    # @note str(-405) has a "-" that int() can't parse, so drop the sign first
    return [int(digit) for digit in str(abs(n))]
```

<?snippet "numbers/digitize.py" part="examples"?>
```pycon
>>> digitize(123)
[1, 2, 3]
>>> digitize(-405)
[4, 0, 5]
>>> digitize(0)
[0]
```

## How it works

- `str()` gives the decimal digits as text.
- `abs()` comes first: `int('-')` would raise.
- Each character converts back with `int()`.
