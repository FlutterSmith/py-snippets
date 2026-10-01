def digitize(n: int) -> list[int]:
    """Return the decimal digits of ``n``, ignoring its sign.

    >>> digitize(123)
    [1, 2, 3]
    >>> digitize(-405)
    [4, 0, 5]
    >>> digitize(0)
    [0]
    """
    # @note str(-405) has a "-" that int() can't parse, so drop the sign first
    return [int(digit) for digit in str(abs(n))]
