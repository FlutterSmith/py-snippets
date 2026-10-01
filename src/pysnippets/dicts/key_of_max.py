from collections.abc import Mapping
from typing import Any, Protocol, TypeVar


class _SupportsLessThan(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K")
V = TypeVar("V", bound=_SupportsLessThan)


def key_of_max(d: Mapping[K, V]) -> K:
    """Return the key of the largest value in ``d``; on a tie, the first one.

    >>> key_of_max({"a": 4, "b": 0, "c": 13})
    'c'
    >>> key_of_max({"x": 1, "y": 1})
    'x'
    """
    # @note iterating a dict yields keys; key= ranks them by value
    return max(d, key=d.__getitem__)


def key_of_min(d: Mapping[K, V]) -> K:
    """Return the key of the smallest value in ``d``; on a tie, the first one.

    >>> key_of_min({"a": 4, "b": 0, "c": 13})
    'b'
    """
    return min(d, key=d.__getitem__)
