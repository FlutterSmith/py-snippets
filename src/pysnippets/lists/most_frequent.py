from collections import Counter
from collections.abc import Hashable, Iterable
from typing import TypeVar

H = TypeVar("H", bound=Hashable)


def most_frequent(items: Iterable[H]) -> H:
    """Return the most common value in ``items``; on a tie, the one seen first.

    >>> most_frequent([1, 2, 1, 2, 3, 2, 1, 4, 2])
    2
    >>> most_frequent("abracadabra")
    'a'
    >>> most_frequent([])
    Traceback (most recent call last):
    ...
    ValueError: most_frequent() arg is an empty iterable
    """
    # @note most_common(1) is a single O(n) pass
    top = Counter(items).most_common(1)
    if not top:
        raise ValueError("most_frequent() arg is an empty iterable")
    return top[0][0]
