from collections import defaultdict
from collections.abc import Hashable, Mapping
from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V", bound=Hashable)


def collect_dictionary(d: Mapping[K, V]) -> dict[V, list[K]]:
    """Invert ``d``, collecting every key that shares a value into a list.

    >>> collect_dictionary({"Peter": 10, "Isabel": 10, "Anna": 9})
    {10: ['Peter', 'Isabel'], 9: ['Anna']}
    >>> collect_dictionary({})
    {}
    """
    inverted: defaultdict[V, list[K]] = defaultdict(list)
    for key, value in d.items():
        # @note keys stay in d's order inside each list
        inverted[value].append(key)
    return dict(inverted)
