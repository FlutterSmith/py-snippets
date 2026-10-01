from collections.abc import Mapping
from operator import itemgetter
from typing import Any, Protocol, TypeVar


class _SupportsLessThan(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K")
V = TypeVar("V", bound=_SupportsLessThan)


def sort_dict_by_value(d: Mapping[K, V], *, reverse: bool = False) -> dict[K, V]:
    """Return a copy of ``d`` ordered by value.

    >>> d = {"one": 1, "three": 3, "five": 5, "two": 2, "four": 4}
    >>> sort_dict_by_value(d)
    {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
    >>> sort_dict_by_value(d, reverse=True)
    {'five': 5, 'four': 4, 'three': 3, 'two': 2, 'one': 1}
    """
    # @note itemgetter(1) picks the value from each (key, value) pair
    return dict(sorted(d.items(), key=itemgetter(1), reverse=reverse))
