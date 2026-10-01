---
slug: weekdays
title: "Check for a weekday or weekend"
summary: "Tell weekdays from weekends using date.weekday()."
category: dates
tags: [calendar, validation]
module: dates/weekdays.py
complexity: "O(1) time and space"
since: "3.11"
published: 2026-10-01
fixes: "The originals defaulted to `datetime.today()`, which Python evaluates once, when the function is defined. A long-running process kept answering for the day it started."
origin:
  upstream: [is-weekday, is-weekend]
  change: "Merged; the date is required instead of defaulting to import time; typed."
related: [daterange]
---

Skip weekends when scheduling, or price weekend bookings differently.

<?snippet "dates/weekdays.py"?>
```python
from datetime import date


def is_weekday(day: date) -> bool:
    """Return ``True`` for Monday to Friday."""
    # @note weekday(): Monday is 0, Sunday is 6
    return day.weekday() < 5


def is_weekend(day: date) -> bool:
    """Return ``True`` for Saturday and Sunday."""
    return day.weekday() >= 5
```

<?snippet "dates/weekdays.py" part="examples"?>
```pycon
>>> from datetime import date
>>> is_weekday(date(2024, 6, 14))
True
>>> is_weekday(date(2024, 6, 15))
False
>>> from datetime import date
>>> is_weekend(date(2024, 6, 15))
True
```

## How it works

- `weekday()` returns 0 for Monday through 6 for Sunday.
- Below 5 is a weekday, 5 and above is the weekend.
- For a calendar where Sunday comes first, use `isoweekday()`, which runs 1 to 7.
