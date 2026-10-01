from collections import Counter
from collections.abc import Hashable, Iterable


def have_same_contents(a: Iterable[Hashable], b: Iterable[Hashable]) -> bool:
    """Return ``True`` if ``a`` and ``b`` hold the same values, in any order.

    Duplicates count: ``[1, 1, 2]`` and ``[1, 2, 2]`` are different.

    >>> have_same_contents([1, 2, 4], [2, 4, 1])
    True
    >>> have_same_contents([1, 1, 2], [1, 2, 2])
    False
    >>> have_same_contents([], ())
    True
    """
    # @note compares counts per value in O(n), not O(n²)
    return Counter(a) == Counter(b)
