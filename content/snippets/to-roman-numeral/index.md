---
slug: to-roman-numeral
title: "Convert an integer to Roman numerals"
summary: "Convert 1 to 3999 into Roman numerals with a greedy table, rejecting values outside that range."
category: numbers
tags: [conversion]
module: numbers/to_roman_numeral.py
complexity: "O(1) time: at most 13 steps"
since: "3.11"
published: 2026-10-01
fixes: "The original returned an empty string for 0 and negative numbers instead of an error."
origin:
  upstream: [to-roman-numeral]
  change: "Validates the range; builds the result with join; typed."
related: [digitize]
---

Chapter numbers, clock faces, movie sequels.

<?snippet "numbers/to_roman_numeral.py"?>
```python
NUMERALS = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]  # fmt: skip


def to_roman_numeral(number: int) -> str:
    """Convert an integer from 1 to 3999 to a Roman numeral."""
    if not 1 <= number <= 3999:
        raise ValueError(f"Roman numerals cover 1 to 3999, got {number}")
    parts = []
    for value, numeral in NUMERALS:
        # @note how many times this numeral fits, and what's left over
        count, number = divmod(number, value)
        parts.append(numeral * count)
    return "".join(parts)
```

<?snippet "numbers/to_roman_numeral.py" part="examples"?>
```pycon
>>> to_roman_numeral(11)
'XI'
>>> to_roman_numeral(1998)
'MCMXCVIII'
>>> to_roman_numeral(0)
Traceback (most recent call last):
...
ValueError: Roman numerals cover 1 to 3999, got 0
```

## How it works

- The table lists every value with its numeral, largest first, including the subtractive pairs like 900 = CM.
- `divmod` says how many times each value fits and what's left over.
- Standard Roman numerals have no zero and stop at 3999, so anything else raises.
