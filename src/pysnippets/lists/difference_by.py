from collections.abc import Callable, Hashable, Iterable
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K", bound=Hashable)


def difference_by(a: Iterable[T], b: Iterable[T], key: Callable[[T], K]) -> list[T]:
    """Return the items of ``a`` whose ``key`` matches no item of ``b``.

    >>> from math import floor
    >>> difference_by([2.1, 1.2], [2.3, 3.4], floor)
    [1.2]
    >>> difference_by([{"x": 2}, {"x": 1}], [{"x": 1}], lambda d: d["x"])
    [{'x': 2}]
    """
    # @note a set of b's keys makes each lookup O(1)
    seen = {key(item) for item in b}
    return [item for item in a if key(item) not in seen]
