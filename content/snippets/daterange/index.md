---
slug: daterange
title: "Iterate over a range of dates"
summary: "Yield the dates from start up to end, like range() for days, with an optional step."
category: dates
tags: [calendar, iteration]
module: dates/daterange.py
complexity: "O(1) per date, lazy"
since: "3.11"
published: 2026-10-01
origin:
  upstream: [daterange]
  change: "A lazy generator with a step; typed."
related: [months-diff, weekdays]
---

Days in a billing period, weeks in a year, dates on a chart axis.

<?snippet "dates/daterange.py"?>
```python
from collections.abc import Iterator
from datetime import date, timedelta


def daterange(start: date, end: date, step: int = 1) -> Iterator[date]:
    """Yield dates from ``start`` up to, but not including, ``end``."""
    if step < 1:
        raise ValueError(f"step must be at least 1 day, got {step}")
    # @note like range(): end is excluded, and it's lazy
    for offset in range(0, (end - start).days, step):
        yield start + timedelta(days=offset)
```

<?snippet "dates/daterange.py" part="examples"?>
```pycon
>>> from datetime import date
>>> [d.isoformat() for d in daterange(date(2024, 2, 27), date(2024, 3, 2))]
['2024-02-27', '2024-02-28', '2024-02-29', '2024-03-01']
>>> len(list(daterange(date(2024, 1, 1), date(2025, 1, 1), step=7)))
53
>>> list(daterange(date(2024, 1, 2), date(2024, 1, 1)))
[]
```

## How it works

- `(end - start).days` is the number of days between the dates.
- `range` does the stepping; `timedelta` turns each offset into a date.
- Like `range`, the end is excluded and a backwards range is empty.
