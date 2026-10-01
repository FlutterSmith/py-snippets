from collections.abc import Iterable
from operator import itemgetter
from typing import TypeVar

T = TypeVar("T")


def sort_by_indexes(
    items: Iterable[T], indexes: Iterable[float], *, reverse: bool = False
) -> list[T]:
    """Sort ``items`` by the matching number in ``indexes``.

    >>> food = ["eggs", "bread", "oranges", "jam", "apples", "milk"]
    >>> sort_by_indexes(food, [3, 2, 6, 4, 1, 5])
    ['apples', 'bread', 'eggs', 'jam', 'milk', 'oranges']
    >>> sort_by_indexes(food, [3, 2, 6, 4, 1, 5], reverse=True)
    ['oranges', 'milk', 'jam', 'eggs', 'bread', 'apples']
    >>> sort_by_indexes("abc", [1, 2])
    Traceback (most recent call last):
    ...
    ValueError: zip() argument 2 is longer than argument 1
    """
    # @note strict=True: a missing index is an error, not a silent drop
    pairs = zip(indexes, items, strict=True)
    # @note sort on the index only, so items never get compared
    return [item for _, item in sorted(pairs, key=itemgetter(0), reverse=reverse)]
