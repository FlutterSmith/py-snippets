from collections.abc import Hashable, Iterable
from typing import TypeVar

H = TypeVar("H", bound=Hashable)


def unique_elements(items: Iterable[H]) -> list[H]:
    """Remove duplicates from ``items``, keeping the first occurrence of each.

    >>> unique_elements([3, 1, 3, 2, 1])
    [3, 1, 2]
    >>> unique_elements("mississippi")
    ['m', 'i', 's', 'p']
    >>> unique_elements([])
    []
    """
    # @note dict keys are unique and remember insertion order; a set doesn't
    return list(dict.fromkeys(items))
