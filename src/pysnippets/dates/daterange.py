from collections.abc import Iterator
from datetime import date, timedelta


def daterange(start: date, end: date, step: int = 1) -> Iterator[date]:
    """Yield dates from ``start`` up to, but not including, ``end``.

    >>> from datetime import date
    >>> [d.isoformat() for d in daterange(date(2024, 2, 27), date(2024, 3, 2))]
    ['2024-02-27', '2024-02-28', '2024-02-29', '2024-03-01']
    >>> len(list(daterange(date(2024, 1, 1), date(2025, 1, 1), step=7)))
    53
    >>> list(daterange(date(2024, 1, 2), date(2024, 1, 1)))
    []
    """
    if step < 1:
        raise ValueError(f"step must be at least 1 day, got {step}")
    # @note like range(): end is excluded, and it's lazy
    for offset in range(0, (end - start).days, step):
        yield start + timedelta(days=offset)
