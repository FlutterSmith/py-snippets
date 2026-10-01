from collections.abc import Hashable, Iterable


def has_duplicates(items: Iterable[Hashable]) -> bool:
    """Return ``True`` if any value occurs more than once in ``items``.

    >>> has_duplicates([1, 2, 3, 4, 5, 5])
    True
    >>> has_duplicates([1, 2, 3, 4, 5])
    False
    >>> has_duplicates(n % 7 for n in range(10**9))
    True
    """
    seen = set()
    for item in items:
        # @note stops at the first repeat, so it works on huge or endless input
        if item in seen:
            return True
        seen.add(item)
    return False
