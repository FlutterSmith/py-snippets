def clamp_number(value: float, low: float, high: float) -> float:
    """Limit ``value`` to the range between ``low`` and ``high``, inclusive.

    The bounds can come in either order.

    >>> clamp_number(2, 3, 5)
    3
    >>> clamp_number(1, -1, -5)
    -1
    >>> clamp_number(4.5, 0, 10)
    4.5
    """
    # @note sort the bounds so callers can't get them backwards
    low, high = min(low, high), max(low, high)
    return max(low, min(value, high))
