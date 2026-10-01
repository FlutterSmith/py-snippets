---
slug: months-diff
title: "Whole months between two dates"
summary: "Count complete calendar months between two dates, the way people count them."
category: dates
tags: [calendar]
module: dates/months_diff.py
complexity: "O(1) time and space"
since: "3.11"
published: 2026-10-01
fixes: "The original divided days by 30 and rounded up, so 1 January to 2 January counted as one month."
origin:
  upstream: [months-diff]
  change: "Rewritten to count calendar months, not 30-day blocks."
related: [daterange]
---

From 15 January to 15 March is 2 months. From 31 January to 29 February isn't a month yet.

<?snippet "dates/months_diff.py"?>
```python
from datetime import date


def months_diff(start: date, end: date) -> int:
    """Return the number of whole calendar months from ``start`` to ``end``."""
    months = (end.year - start.year) * 12 + (end.month - start.month)
    # @note a month only counts once its day of the month comes round again
    if months > 0 and end.day < start.day:
        months -= 1
    elif months < 0 and end.day > start.day:
        months += 1
    return months
```

<?snippet "dates/months_diff.py" part="examples"?>
```pycon
>>> from datetime import date
>>> months_diff(date(2024, 1, 31), date(2024, 2, 29))
0
>>> months_diff(date(2024, 1, 15), date(2025, 3, 15))
14
>>> months_diff(date(2024, 3, 1), date(2024, 1, 1))
-2
```

## How it works

- Year and month differences give a first count.
- If the end's day of the month hasn't reached the start's, the last month isn't complete.
- It works backwards too, returning a negative count.
