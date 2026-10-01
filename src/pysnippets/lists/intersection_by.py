from collections.abc import Callable, Hashable, Iterable
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K", bound=Hashable)


def intersection_by(a: Iterable[T], b: Iterable[T], key: Callable[[T], K]) -> list[T]:
    """Return the items of ``a`` whose ``key`` matches some item of ``b``.

    >>> from math import floor
    >>> intersection_by([2.1, 1.2], [2.3, 3.4], floor)
    [2.1]
    >>> intersection_by(["Ada", "bob"], ["ADA", "Cy"], str.lower)
    ['Ada']
    """
    seen = {key(item) for item in b}
    # @note order and duplicates come from a, never from b
    return [item for item in a if key(item) in seen]
