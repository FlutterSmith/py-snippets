from collections import Counter
from collections.abc import Callable, Hashable, Iterable
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K", bound=Hashable)


def count_by(items: Iterable[T], key: Callable[[T], K]) -> dict[K, int]:
    """Count ``items`` by the result of ``key``.

    >>> from math import floor
    >>> count_by([6.1, 4.2, 6.3], floor)
    {6: 2, 4: 1}
    >>> count_by(["one", "two", "three"], len)
    {3: 2, 5: 1}
    >>> count_by([], len)
    {}
    """
    # @note Counter does the counting; map applies key lazily
    return dict(Counter(map(key, items)))
