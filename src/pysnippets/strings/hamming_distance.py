def hamming_distance(a: str, b: str) -> int:
    """Return how many positions differ between two equal-length strings.

    >>> hamming_distance("karolin", "kathrin")
    3
    >>> hamming_distance("", "")
    0
    >>> hamming_distance("abc", "ab")
    Traceback (most recent call last):
    ...
    ValueError: strings must have equal length, got 3 and 2
    """
    if len(a) != len(b):
        raise ValueError(f"strings must have equal length, got {len(a)} and {len(b)}")
    # @note True counts as 1 in sum()
    return sum(x != y for x, y in zip(a, b, strict=True))
