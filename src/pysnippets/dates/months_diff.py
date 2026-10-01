from datetime import date


def months_diff(start: date, end: date) -> int:
    """Return the number of whole calendar months from ``start`` to ``end``.

    Negative when ``end`` is before ``start``.

    >>> from datetime import date
    >>> months_diff(date(2024, 1, 31), date(2024, 2, 29))
    0
    >>> months_diff(date(2024, 1, 15), date(2025, 3, 15))
    14
    >>> months_diff(date(2024, 3, 1), date(2024, 1, 1))
    -2
    """
    months = (end.year - start.year) * 12 + (end.month - start.month)
    # @note a month only counts once its day of the month comes round again
    if months > 0 and end.day < start.day:
        months -= 1
    elif months < 0 and end.day > start.day:
        months += 1
    return months
