from datetime import date


def is_weekday(day: date) -> bool:
    """Return ``True`` for Monday to Friday.

    >>> from datetime import date
    >>> is_weekday(date(2024, 6, 14))
    True
    >>> is_weekday(date(2024, 6, 15))
    False
    """
    # @note weekday(): Monday is 0, Sunday is 6
    return day.weekday() < 5


def is_weekend(day: date) -> bool:
    """Return ``True`` for Saturday and Sunday.

    >>> from datetime import date
    >>> is_weekend(date(2024, 6, 15))
    True
    """
    return day.weekday() >= 5
