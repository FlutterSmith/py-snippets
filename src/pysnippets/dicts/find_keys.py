from collections.abc import Mapping
from typing import TypeVar

K = TypeVar("K")


def find_keys(d: Mapping[K, object], value: object) -> list[K]:
    """Return every key of ``d`` whose value equals ``value``.

    >>> find_keys({"Peter": 10, "Isabel": 11, "Anna": 10}, 10)
    ['Peter', 'Anna']
    >>> find_keys({"Peter": 10}, 99)
    []
    """
    # @note a linear scan: dicts index by key, not by value
    return [key for key, v in d.items() if v == value]
