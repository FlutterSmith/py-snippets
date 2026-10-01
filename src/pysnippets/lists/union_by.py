from collections.abc import Callable, Hashable, Iterable
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K", bound=Hashable)


def union_by(a: Iterable[T], b: Iterable[T], key: Callable[[T], K]) -> list[T]:
    """Merge ``a`` and ``b``, keeping the first item for each ``key``, in order.

    >>> from math import floor
    >>> union_by([2.1], [1.2, 2.3], floor)
    [2.1, 1.2]
    >>> union_by(["Ada", "bob"], ["ADA", "Cy"], str.lower)
    ['Ada', 'bob', 'Cy']
    """
    seen: set[K] = set()
    merged = []
    for items in (a, b):
        for item in items:
            k = key(item)
            # @note first one wins, so a beats b on a tie
            if k not in seen:
                seen.add(k)
                merged.append(item)
    return merged
