from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")


def index_of_all(items: Iterable[T], value: T) -> list[int]:
    """Return every index at which ``value`` occurs in ``items``.

    >>> index_of_all([1, 2, 1, 4, 5, 1], 1)
    [0, 2, 5]
    >>> index_of_all([1, 2, 3, 4], 6)
    []
    """
    return [i for i, item in enumerate(items) if item == value]


def find_index_of_all(
    items: Iterable[T], predicate: Callable[[T], object]
) -> list[int]:
    """Return every index whose item passes ``predicate``.

    >>> find_index_of_all([1, 2, 3, 4], lambda n: n % 2 == 1)
    [0, 2]
    >>> find_index_of_all("Hello World", str.isupper)
    [0, 6]
    """
    # @note enumerate pairs each item with its index
    return [i for i, item in enumerate(items) if predicate(item)]
