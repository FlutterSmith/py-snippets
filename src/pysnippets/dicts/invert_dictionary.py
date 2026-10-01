from collections.abc import Hashable, Mapping
from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V", bound=Hashable)


def invert_dictionary(d: Mapping[K, V]) -> dict[V, K]:
    """Swap the keys and values of ``d``.

    When two keys share a value, the later key wins. Use ``collect_dictionary``
    to keep all of them.

    >>> invert_dictionary({"Peter": 10, "Isabel": 11, "Anna": 9})
    {10: 'Peter', 11: 'Isabel', 9: 'Anna'}
    >>> invert_dictionary({"a": 1, "b": 1})
    {1: 'b'}
    """
    # @note values become keys, so they must be hashable
    return {value: key for key, value in d.items()}
