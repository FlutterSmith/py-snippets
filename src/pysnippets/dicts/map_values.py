from collections.abc import Callable, Mapping
from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V")
R = TypeVar("R")


def map_values(d: Mapping[K, V], fn: Callable[[V], R]) -> dict[K, R]:
    """Return a new dict with ``fn`` applied to every value of ``d``.

    >>> users = {"fred": {"age": 40, "pets": 1}, "pebbles": {"age": 1, "pets": 0}}
    >>> map_values(users, lambda user: user["age"])
    {'fred': 40, 'pebbles': 1}
    >>> map_values({"a": "x"}, str.upper)
    {'a': 'X'}
    """
    # @note keys and their order are untouched
    return {key: fn(value) for key, value in d.items()}
