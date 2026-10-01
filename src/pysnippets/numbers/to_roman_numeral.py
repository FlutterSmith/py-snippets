NUMERALS = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]  # fmt: skip


def to_roman_numeral(number: int) -> str:
    """Convert an integer from 1 to 3999 to a Roman numeral.

    >>> to_roman_numeral(11)
    'XI'
    >>> to_roman_numeral(1998)
    'MCMXCVIII'
    >>> to_roman_numeral(0)
    Traceback (most recent call last):
    ...
    ValueError: Roman numerals cover 1 to 3999, got 0
    """
    if not 1 <= number <= 3999:
        raise ValueError(f"Roman numerals cover 1 to 3999, got {number}")
    parts = []
    for value, numeral in NUMERALS:
        # @note how many times this numeral fits, and what's left over
        count, number = divmod(number, value)
        parts.append(numeral * count)
    return "".join(parts)
