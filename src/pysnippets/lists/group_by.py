from collections import defaultdict
from collections.abc import Callable, Hashable, Iterable
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K", bound=Hashable)


def group_by(items: Iterable[T], key: Callable[[T], K]) -> dict[K, list[T]]:
    """Group ``items`` into lists by the result of ``key``, keeping their order.

    >>> from math import floor
    >>> group_by([6.1, 4.2, 6.3], floor)
    {6: [6.1, 6.3], 4: [4.2]}
    >>> group_by(["one", "two", "three"], len)
    {3: ['one', 'two'], 5: ['three']}
    >>> group_by([], len)
    {}
    """
    groups: defaultdict[K, list[T]] = defaultdict(list)
    for item in items:
        groups[key(item)].append(item)
    # @note a plain dict, so a missing key raises instead of inserting
    return dict(groups)
