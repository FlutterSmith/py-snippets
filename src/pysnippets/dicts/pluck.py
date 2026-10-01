from collections.abc import Iterable, Mapping
from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V")


def pluck(records: Iterable[Mapping[K, V]], key: K) -> list[V | None]:
    """Return ``record[key]`` for each record, or ``None`` where it's missing.

    >>> simpsons = [{"name": "lisa", "age": 8}, {"name": "homer", "age": 36}, {}]
    >>> pluck(simpsons, "age")
    [8, 36, None]
    >>> pluck([], "age")
    []
    """
    # @note .get keeps one result per record, even when the key is missing
    return [record.get(key) for record in records]
