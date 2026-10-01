from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def every_nth(items: Sequence[T], n: int) -> list[T]:
    """Return every ``n``-th item of ``items``, starting with the ``n``-th.

    >>> every_nth([1, 2, 3, 4, 5, 6], 2)
    [2, 4, 6]
    >>> every_nth(range(1, 11), 3)
    [3, 6, 9]
    >>> every_nth([1, 2], 5)
    []
    """
    if n < 1:
        raise ValueError(f"n must be at least 1, got {n}")
    # @note start at index n - 1, step n
    return list(items[n - 1 :: n])
